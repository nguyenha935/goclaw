#!/usr/bin/env python3
"""Stub LLM server that records every request and returns scripted replies.

Speaks enough of three wire formats for agent platforms to run end to end:
  - OpenAI Chat Completions  POST /v1/chat/completions   (stream + non-stream, tool calls)
  - OpenAI Responses         POST /v1/responses          (stream + non-stream, text only)
  - Anthropic Messages       POST /v1/messages           (stream + non-stream, tool_use)
  - Embeddings               POST /v1/embeddings         (deterministic hash vectors)
  - Model list               GET  /v1/models

Usage:
  STUB_LOG=/path/requests.jsonl STUB_RULES=/path/rules.json python3 stub_llm.py --port 18080

rules.json (re-read on every request, edit freely while the server runs):
  [
    {"match": "regex on the LAST user message", "reply": "text"},
    {"match": "regex", "tool_calls": [{"name": "memory_save", "arguments": {"text": "..."}}]},
    {"match_any": "regex on the WHOLE request body", "reply": "{}"}
  ]
First matching rule wins. Default reply: "OK (stub)" ("{}" when JSON output is requested).
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG_LOCK = threading.Lock()


def log_request(path, body):
    log_path = os.environ.get("STUB_LOG", "stub_requests.jsonl")
    with LOG_LOCK, open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time(), "path": path, "body": body}, ensure_ascii=False) + "\n")


def load_rules():
    path = os.environ.get("STUB_RULES")
    if not path or not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        print(f"[stub] bad rules file: {e}", file=sys.stderr)
        return []


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict):
                parts.append(p.get("text") or p.get("input_text") or p.get("content") or "")
            elif isinstance(p, str):
                parts.append(p)
        return "\n".join(x if isinstance(x, str) else json.dumps(x, ensure_ascii=False) for x in parts)
    return "" if content is None else json.dumps(content, ensure_ascii=False)


def last_user_text(body):
    msgs = body.get("messages")
    if msgs is None and "input" in body:  # Responses API
        msgs = body["input"] if isinstance(body["input"], list) else [{"role": "user", "content": body["input"]}]
    for m in reversed(msgs or []):
        if isinstance(m, dict) and m.get("role") == "user":
            return text_of(m.get("content"))
    return ""


def wants_json(body):
    rf = body.get("response_format") or {}
    return isinstance(rf, dict) and rf.get("type") in ("json_object", "json_schema")


def pick(body):
    user = last_user_text(body)
    whole = json.dumps(body, ensure_ascii=False)
    for r in load_rules():
        if "match" in r and re.search(r["match"], user, re.S | re.I):
            return r
        if "match_any" in r and re.search(r["match_any"], whole, re.S | re.I):
            return r
    return {"reply": "{}" if wants_json(body) else "OK (stub)"}


def embed(text, dim):
    vec = []
    seed = text.encode("utf-8")
    i = 0
    while len(vec) < dim:
        h = hashlib.sha256(seed + i.to_bytes(4, "big")).digest()
        vec.extend((b - 127.5) / 127.5 for b in h)
        i += 1
    vec = vec[:dim]
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def _json(self, code, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _sse_start(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True

    def _sse(self, obj, event=None):
        chunk = ""
        if event:
            chunk += f"event: {event}\n"
        chunk += "data: " + (obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)) + "\n\n"
        self.wfile.write(chunk.encode("utf-8"))
        self.wfile.flush()

    def do_GET(self):
        if self.path.rstrip("/").endswith("/models"):
            return self._json(200, {"object": "list", "data": [{"id": "stub-model", "object": "model", "owned_by": "stub"}]})
        return self._json(200, {"ok": True})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw or b"{}")
        except ValueError:
            body = {"_raw": raw.decode("utf-8", "replace")}
        path = self.path.split("?")[0].rstrip("/")
        log_request(path, body)
        if path.endswith("/embeddings"):
            return self._embeddings(body)
        if path.endswith("/chat/completions"):
            return self._chat(body)
        if path.endswith("/responses"):
            return self._responses(body)
        if path.endswith("/messages"):
            return self._anthropic(body)
        return self._json(404, {"error": {"message": f"stub: unknown path {path}"}})

    def _embeddings(self, body):
        inputs = body.get("input", "")
        if isinstance(inputs, str):
            inputs = [inputs]
        dim = int(body.get("dimensions") or os.environ.get("STUB_EMBED_DIM", "1536"))
        data = [{"object": "embedding", "index": i, "embedding": embed(str(t), dim)} for i, t in enumerate(inputs)]
        return self._json(200, {"object": "list", "data": data, "model": body.get("model", "stub-embed"),
                                "usage": {"prompt_tokens": 1, "total_tokens": 1}})

    def _chat(self, body):
        rule = pick(body)
        model = body.get("model", "stub-model")
        cid = "chatcmpl-" + uuid.uuid4().hex[:12]
        tool_calls = [{"id": "call_" + uuid.uuid4().hex[:8], "type": "function",
                       "function": {"name": t["name"], "arguments": json.dumps(t.get("arguments", {}), ensure_ascii=False)}}
                      for t in rule.get("tool_calls", [])]
        text = rule.get("reply", "" if tool_calls else "OK (stub)")
        finish = "tool_calls" if tool_calls else "stop"
        usage = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        if not body.get("stream"):
            msg = {"role": "assistant", "content": text or None}
            if tool_calls:
                msg["tool_calls"] = tool_calls
            return self._json(200, {"id": cid, "object": "chat.completion", "created": int(time.time()), "model": model,
                                    "choices": [{"index": 0, "message": msg, "finish_reason": finish}], "usage": usage})
        self._sse_start()
        base = {"id": cid, "object": "chat.completion.chunk", "created": int(time.time()), "model": model}
        self._sse({**base, "choices": [{"index": 0, "delta": {"role": "assistant", "content": ""}, "finish_reason": None}]})
        if text:
            self._sse({**base, "choices": [{"index": 0, "delta": {"content": text}, "finish_reason": None}]})
        for i, tc in enumerate(tool_calls):
            self._sse({**base, "choices": [{"index": 0, "delta": {"tool_calls": [{**tc, "index": i}]}, "finish_reason": None}]})
        self._sse({**base, "choices": [{"index": 0, "delta": {}, "finish_reason": finish}], "usage": usage})
        self._sse("[DONE]")

    def _responses(self, body):
        rule = pick(body)
        text = rule.get("reply", "OK (stub)")
        rid = "resp_" + uuid.uuid4().hex[:12]
        item = {"id": "msg_" + uuid.uuid4().hex[:8], "type": "message", "role": "assistant", "status": "completed",
                "content": [{"type": "output_text", "text": text, "annotations": []}]}
        resp = {"id": rid, "object": "response", "created_at": int(time.time()), "status": "completed",
                "model": body.get("model", "stub-model"), "output": [item], "output_text": text,
                "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15}}
        if not body.get("stream"):
            return self._json(200, resp)
        self._sse_start()
        self._sse({"type": "response.created", "response": {**resp, "status": "in_progress", "output": []}}, "response.created")
        self._sse({"type": "response.output_item.added", "output_index": 0, "item": {**item, "content": [], "status": "in_progress"}}, "response.output_item.added")
        self._sse({"type": "response.output_text.delta", "item_id": item["id"], "output_index": 0, "content_index": 0, "delta": text}, "response.output_text.delta")
        self._sse({"type": "response.output_text.done", "item_id": item["id"], "output_index": 0, "content_index": 0, "text": text}, "response.output_text.done")
        self._sse({"type": "response.output_item.done", "output_index": 0, "item": item}, "response.output_item.done")
        self._sse({"type": "response.completed", "response": resp}, "response.completed")

    def _anthropic(self, body):
        rule = pick(body)
        tools = [{"type": "tool_use", "id": "toolu_" + uuid.uuid4().hex[:8], "name": t["name"], "input": t.get("arguments", {})}
                 for t in rule.get("tool_calls", [])]
        text = rule.get("reply", "" if tools else "OK (stub)")
        content = ([{"type": "text", "text": text}] if text else []) + tools
        stop = "tool_use" if tools else "end_turn"
        mid = "msg_" + uuid.uuid4().hex[:12]
        usage = {"input_tokens": 10, "output_tokens": 5}
        msg = {"id": mid, "type": "message", "role": "assistant", "model": body.get("model", "stub-model"),
               "content": content, "stop_reason": stop, "stop_sequence": None, "usage": usage}
        if not body.get("stream"):
            return self._json(200, msg)
        self._sse_start()
        self._sse({"type": "message_start", "message": {**msg, "content": [], "stop_reason": None}}, "message_start")
        for i, block in enumerate(content):
            if block["type"] == "text":
                self._sse({"type": "content_block_start", "index": i, "content_block": {"type": "text", "text": ""}}, "content_block_start")
                self._sse({"type": "content_block_delta", "index": i, "delta": {"type": "text_delta", "text": block["text"]}}, "content_block_delta")
            else:
                self._sse({"type": "content_block_start", "index": i, "content_block": {**block, "input": {}}}, "content_block_start")
                self._sse({"type": "content_block_delta", "index": i, "delta": {"type": "input_json_delta", "partial_json": json.dumps(block["input"], ensure_ascii=False)}}, "content_block_delta")
            self._sse({"type": "content_block_stop", "index": i}, "content_block_stop")
        self._sse({"type": "message_delta", "delta": {"stop_reason": stop, "stop_sequence": None}, "usage": {"output_tokens": 5}}, "message_delta")
        self._sse({"type": "message_stop"}, "message_stop")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=18080)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[stub] listening on http://{args.host}:{args.port}/v1  log={os.environ.get('STUB_LOG', 'stub_requests.jsonl')}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
