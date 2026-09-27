# Hermes Agent: built-in memory và Honcho — nhận diện một người qua nhóm, DM, kênh; vai trò agent (theo yêu cầu đã sửa ngày 2026-09-27)

Mã đã đọc và chạy:
- Hermes Agent: `516535b54275e963a82b4c28f866338fb768e7bc` (nhánh `main`, commit 2026-09-27T04:59:47-04:00). `hermes --version` in ra `Hermes Agent vgit.516535b (2026.9.24)`. Link mã bên dưới ghim vào commit này: `H/<path>#L<n>` = `https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/<path>#L<n>`.
- Honcho server: `2eb27b6cc0595d3f8deb693f0560e7241c2aeaff` (2026-09-25), `pyproject.toml` ghi `version = "3.2.1"`. SDK Python mà Hermes ghim: `honcho-ai==2.2.0`.
- Plugin Zalo: `tinovn/hermes-zalo-oa-plugin@88e0bd4b` và `tinovn/hermes-zalo-plugin@e3f3c4fd`.

Nhãn dùng trong ghi chú:
- **[CHẠY]**: đã chạy thật trên máy lab ngày 2026-09-27, LLM là stub.
- **[MÃ]**: đọc từ mã nguồn.
- **[DOC]**: lấy từ tài liệu.
- **[?]**: suy luận, chưa kiểm chứng.

Toàn bộ thư mục chạy (clone, venv, cụm Postgres, log stub) đã xoá sau khi xong. Các trích đoạn request dưới đây được chép lại từ log trước khi xoá.

---

## 1. Cách chạy thật: môi trường, đường tiêm tin nhắn, và các chỗ lệch so với production

### Takeaway
Cả hai cấu hình đều chạy end-to-end bằng **tiến trình gateway thật** (`python -m gateway.run`), bơm tin qua một plugin nền tảng giả. LLM là stub nên mọi request gửi tới model đều được ghi lại.

Honcho **tự host được hoàn toàn** mà không cần Docker: Postgres 16 + pgvector 0.6.0 từ apt, FastAPI server và worker deriver. Mọi lệnh LLM và embedding của Honcho đều trỏ về stub. Không có lệnh nào ra mạng ngoài, trừ lần tải file mã hoá tiktoken lúc khởi động, đã xử lý bằng bản sao offline.

### Cited Findings
- **Đường tiêm tin nhắn [CHẠY].** Mô phỏng theo harness chaos có sẵn trong repo. Harness này nạp một plugin `kind: platform` thật, rồi chạy entry point production `python -m gateway.run`: "Nothing in the runner is patched" — [H/tests/e2e/core/chaos/_gateway_fake_platform.py#L1-L19](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/tests/e2e/core/chaos/_gateway_fake_platform.py#L1).
  - Tôi viết hai plugin `lab-telegram` (nền tảng `labgram`) và `lab-zalo` (`labzalo`). Mỗi plugin mở một cổng TCP loopback và nhận JSON `{chat_id, chat_type, chat_name, user_id, user_name, text}`.
  - Plugin gọi `self.build_source(...)`, tạo `MessageEvent`, rồi gọi `await self.handle_message(event)`. Đây đúng là đường mọi adapter bên thứ ba dùng.
  - Plugin đăng ký bằng `ctx.register_platform(...)` — [H/hermes_cli/plugins.py#L807-L836](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/plugins.py#L807).
- **Chỗ lệch so với production.**
  - (1) Tên nền tảng là `labgram`/`labzalo`, không phải adapter Telegram hay Zalo thật. Vì vậy không có bước lọc "phải @mention bot trong nhóm" của adapter Telegram. Lớp session, prompt và memory là mã chung cho mọi nền tảng.
  - (2) Cho phép mọi người dùng bằng `LABGRAM_ALLOW_ALL_USERS=true` trong `.env` của profile. Gateway đọc cờ `allow_all_env` của plugin qua secret có phạm vi theo profile, nên đặt biến môi trường của tiến trình là không đủ — [H/gateway/authz_mixin.py#L614-L676](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/authz_mixin.py#L614).
  - (3) Model là `provider: custom` trỏ vào stub `127.0.0.1:18082`.
- **Cài đặt [CHẠY].**
  - Hermes chỉ kéo đủ dependency trên Python 3.14. Cần uv mới (0.12.19) mới tải được CPython 3.14.7; uv 0.8.17 có sẵn chỉ biết 3.14.0rc2.
  - Lệnh `uv pip install -e ".[honcho]"` chạy sạch.
  - Honcho cần Python ≥3.13 (`requires-python = ">=3.13"`), cài bằng `uv sync` — [HO/pyproject.toml#L3-L9](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/pyproject.toml#L3). README lại ghi "The minimum python version is `3.10`", mâu thuẫn với `pyproject.toml` — [HO/README.md#L339-L420](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/README.md#L339).
- **Tự host Honcho không Docker [CHẠY].**
  - Docker daemon trên máy lab không chạy được. Tôi tạo cụm Postgres 16 riêng ở cổng 5439, cài `postgresql-16-pgvector` 0.6.0 từ apt, chạy `alembic upgrade head`, rồi khởi động `fastapi run src/main.py` và `python -m src.deriver`.
  - Không dùng Redis (`CACHE_ENABLED=false`). File compose mẫu dùng `pgvector/pgvector:pg15` và `redis:8.2` — [HO/docker-compose.yml.example#L112-L136](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/docker-compose.yml.example#L112).
- **Chặn mạng khi khởi động Honcho [CHẠY].**
  - Honcho gọi `tiktoken` để tải `o200k_base.tiktoken` từ `openaipublic.blob.core.windows.net`, và proxy của phiên chặn host này (403).
  - Cách xử lý: lấy file từ module Go `pkoukk/tiktoken-go-loader@v0.0.2` qua proxy.golang.org, đặt vào `TIKTOKEN_CACHE_DIR`. SHA-256 khớp `expected_hash` của tiktoken: `446a9538…1a2d`.
  - Hàm ý khi tự host trong mạng kín: phải đặt sẵn file này.
- **Trỏ LLM của Honcho vào stub [MÃ][CHẠY].**
  - Dùng `LLM_OPENAI_BASE_URL` và `LLM_OPENAI_API_KEY` cho mọi module (`LLMSettings`, `env_prefix="LLM_"`) — [HO/src/config.py#L774-L787](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/src/config.py#L774).
  - Embedding cần thêm `EMBEDDING_MODEL_CONFIG__OVERRIDES__BASE_URL` để client chuyển sang `encoding_format=float` — [HO/src/config.py#L860-L873](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/src/config.py#L860).
  - `DERIVER_FLUSH_ENABLED=true` để deriver không chờ gom đủ 512 token. Tắt dream bằng `DREAM_ENABLED=false`.
  - Model mặc định trong cấu hình mẫu là `gpt-5.4-mini`, còn embedding là `text-embedding-3-small` 1536 chiều — [HO/config.toml.example#L54-L90](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/config.toml.example#L54).
- **Các lệnh LLM Honcho thực sự gọi trong cả kịch bản [CHẠY], đếm từ log stub phía Honcho:**
  - 68 lệnh `/v1/embeddings`: embed tin nhắn và câu truy vấn.
  - 24 lệnh chat "You are Honcho's dialectic: a recall agent…", có kèm `tools`, tức vòng lặp công cụ của dialectic.
  - 13 lệnh chat deriver "Analyze messages to extract **explicit atomic facts**…" với `response_format: json_schema`.
  - Summary không kích hoạt, vì cần 20 tin cho một bản tóm tắt ngắn — [HO/config.toml.example#L204-L209](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/config.toml.example#L204).
  - Stub được lập kịch bản để trả JSON quan sát giống output model thật (xem mục 4).
- **Kịch bản chạy trên cả hai cấu hình:**
  - Agent 1 là profile `default`, SOUL.md "Content Lead – Phòng Marketing".
  - Agent 2 là profile `copywriter`, SOUL.md "Copywriter – Phòng Marketing".
  - A = user 1001 "Lan", B = 1002 "Minh".
  - G1 = chat `-100111`, G2 = `-100222`, DM = `chat_id` trùng user id.

### Inferences
- Cách tiêm tin này đi qua đúng lớp authz → session key → dựng prompt → memory provider của production. Kết quả về identity và memory vì thế đại diện cho Telegram thật. Riêng phần lọc mention nằm trong adapter Telegram nên không được kiểm.

### Gaps
- Chưa chạy adapter Telegram hay Zalo thật (không có token, theo ràng buộc).
- Chưa kiểm Honcho khi bật Redis, dream và summary.

---

## 2. Cấu hình (1) — memory built-in (MEMORY.md / USER.md): 5a, 5b-in, 5b-cross, privacy

### Takeaway
Built-in memory gắn theo **profile, không theo người**.
- `USER.md` là **một file chung** cho mọi người nói chuyện với agent 1.
- Mọi dòng trong file được tiêm **tự động** vào system prompt của **mọi** session mới: DM của A, DM của B, cả nhóm.
- Vì vậy "A được nhận ra ở DM" chỉ là tác dụng phụ. Chính cơ chế đó làm lộ dữ kiện của A sang B **[CHẠY]**.
- Session key tách theo chat và theo người. Prompt chỉ ghi **tên hiển thị**, không có user ID.
- `session_search` tìm trên toàn profile, không lọc theo người **[CHẠY]**.

### Cited Findings
- **Đường dẫn và cách nạp [MÃ].**
  - Docstring: "MEMORY.md = agent notes, USER.md = user profile). Both enter the system prompt as a FROZEN snapshot at session start".
  - `get_memory_dir()` = `get_hermes_home() / "memories"`, tức "Profile-scoped".
  - [H/tools/memory_tool.py#L1-L5, L38-L40](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/tools/memory_tool.py#L1)
- **[CHẠY] Sau G1 và G2, `…/.hermes/memories/USER.md` chứa ba dòng của hai người khác nhau.**
  - Model stub được lập kịch bản gọi `memory(action=add, target=user, …)`, giống cách một model thật ghi nhớ.

  ```
  Lan: phụ trách fanpage X, thích giọng văn hài hước.
  §
  Minh: thành viên nhóm G1.
  §
  Lan: KPI tháng 10 là 50 bài.
  ```
  - Tên người trong mỗi dòng là do model tự viết. Không có khoá theo người.
- **[CHẠY] DM(A) "Bạn biết gì về mình? KPI của mình bao nhiêu?"**
  - System prompt tự động chứa khối sau. Không cần model gọi tool nào.

  ```
  USER PROFILE (who the user is) [8% — 110/1,375 chars]
  Lan: phụ trách fanpage X, thích giọng văn hài hước.
  §
  Minh: thành viên nhóm G1.
  §
  Lan: KPI tháng 10 là 50 bài.
  ...
  ## Current Session Context
  **Source:** Labgram ("DM with Lan")
  **User:** "Lan"
  ```
- **[CHẠY] Privacy — DM(B) "Bạn biết gì về mình?"** nhận **đúng khối USER PROFILE ở trên**, gồm cả fanpage X và KPI 50 bài của Lan. Ngay trong G1, lượt đầu tiên của Minh cũng đã thấy dòng "Lan: phụ trách fanpage X…".
- **[CHẠY] 5b-cross.** A nhắn từ nền tảng thứ hai (`labzalo`, user `zl-777`, tên "Lan Nguyễn") và cũng nhận nguyên khối USER PROFILE.
  - Đây **không** phải liên kết người. Mọi người trên mọi kênh đều thấy cùng một file.
- **[CHẠY] Tool-based: `session_search` không lọc theo người.**
  - Tool này là "deferred". Model phải gọi `tool_call` với `{"name":"session_search"}`, vì gọi thẳng thì bị báo "does not exist".
  - Gọi từ DM(B) với `query="KPI"`, kết quả gồm session G2 của Lan ("Nhớ giúp: KPI tháng 10 của mình là 50 bài.") và cả DM của Lan. Kết quả không kèm `user_id`.
  - Mã chỉ ẩn các nguồn `("kanban", "subagent", "tool")` — [H/tools/session_search_tool.py#L21-L23, L354-L372](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/tools/session_search_tool.py#L21).
- **[CHẠY] Session key trong `sessions.json` và bảng `gateway_routing`:**
  - `agent:main:labgram:group:-100111:1001` (G1, A)
  - `agent:main:labgram:group:-100111:1002` (G1, B)
  - `agent:main:labgram:group:-100222:1001` (G2, A)
  - `agent:main:labgram:dm:1001`, `agent:main:labgram:dm:1002`, `agent:main:labzalo:dm:zl-777`
  - Mặc định `group_sessions_per_user=True` thêm participant id vào key nhóm — [H/gateway/session.py#L673-L714](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/session.py#L673).
- **5a — danh tính trong prompt [CHẠY][MÃ].**
  - Prompt có `**Source:** Labgram ("group: G1 Marketing")` và `**User:** "Lan"`.
  - **User ID chỉ xuất hiện khi không có user_name**: nhánh `elif src.user_name` … `elif src.user_id` — [H/gateway/session.py#L375-L434](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/session.py#L375).
  - Trong session nhóm dùng chung (`group_sessions_per_user: false`), mỗi tin chỉ được thêm tiền tố `[Lan]`. Riêng Slack có thêm `<@U…>` — [H/gateway/run_inbound.py#L1415-L1429](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/run_inbound.py#L1415). Đã quan sát thấy `[Lan] Chào cả nhóm…` trong request [CHẠY].
  - `chat_id` và `user_id` được lưu trong DB (`sessions.user_id` = `1001`/`1002`), nhưng **không** đưa vào prompt.
- **Dấu hiệu thiết kế một người dùng [CHẠY][MÃ].**
  - Lượt đầu tiên của Lan nhận "[System note: This is the user's very first message ever…]". Lượt đầu tiên của Minh thì không.
  - Cờ `onboarding.seen.*` nằm trong `config.yaml` của profile, không theo người — [H/agent/onboarding.py#L130-L135, L195-L216](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/agent/onboarding.py#L130).

### Inferences
- Với built-in, 5b-in "đạt" chỉ theo nghĩa hẹp: agent ở DM thấy dữ kiện A đã kể ở nhóm. Nhưng dữ kiện không được khoá theo A, và bất kỳ B nào cũng thấy. Với phòng Marketing nhiều người dùng chung một agent, đây là rò rỉ theo thiết kế.
- Model chỉ biết tên hiển thị. Hai người trùng tên "Lan" sẽ bị trộn trong USER.md.

### Gaps
- Chưa đo cơ chế "background review" tự ghi memory sau N lượt (`agent/background_review.py`), vì stub không lập kịch bản cho nó. Dù vậy nó vẫn ghi vào cùng USER.md theo profile [?].

---

## 3. Honcho server: license, tự host, các lệnh LLM và embedding

### Takeaway
- Honcho server dùng **AGPL-3.0**; SDK Python dùng Apache-2.0.
- Tự host được hoàn toàn: FastAPI + worker deriver + Postgres/pgvector; Redis tuỳ chọn.
- Mọi lệnh LLM (deriver, dialectic, summary, dream) và embedding đều cấu hình được theo từng module (`transport` openai/anthropic/gemini + `base_url` override). Nhờ vậy trỏ được vào model nội bộ; đã chạy với stub **[CHẠY]**.
- Có sẵn `src/mock_provider` (OpenAI-compatible, không suy luận) để chạy CI.

### Cited Findings
- **License:**
  - `LICENSE` là "GNU AFFERO GENERAL PUBLIC LICENSE Version 3" — [HO/LICENSE](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/LICENSE).
  - README: "Honcho is open source under AGPL-3.0. To **run** a personal instance, install the CLI (`uv tool install honcho-cli`) and then `honcho start --setup`" — [HO/README.md#L339-L341](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/README.md#L339).
  - SDK Python: `license = "Apache-2.0"` — [HO/sdks/python/pyproject.toml#L6](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/sdks/python/pyproject.toml#L6).
- **Phiên bản:** `CHANGELOG.md` ghi "## [3.2.1] - 2026-09-22" và "## [3.2.0] - 2026-09-15". Commit gần nhất là 2026-09-25 — [HO/CHANGELOG.md#L8](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/CHANGELOG.md#L8).
- **Thành phần (theo CLAUDE.md của repo):**
  - API server "Hosts the **Dialectic** agent inline".
  - Deriver worker "Runs the **Deriver**, **Summarizer**, and **Dreamer** off the queue" và một Reconciler embed tin nhắn.
  - [HO/CLAUDE.md#L140-L141](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/CLAUDE.md#L140)
- **Cấu hình LLM theo module [MÃ]:**
  - "Supported transports: openai, anthropic, gemini. Base URLs are set per-module via model_config.overrides.base_url".
  - Các khối `[deriver.model_config]`, `[dialectic.levels.*.model_config]`, `[summary.model_config]`, `[dream.*_model_config]`, `[embedding.model_config]`.
  - [HO/config.toml.example#L54-L237](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/config.toml.example#L54)
- **Mock provider có sẵn:** "Deterministic OpenAI-compatible provider for local and CI use" — [HO/src/mock_provider/__init__.py](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/src/mock_provider/__init__.py).
- **Deriver lưu quan sát theo cặp peer (observer, observed), không theo session [MÃ][CHẠY].**
  - `RepresentationManager(workspace_name=…, observer=observer, observed=observed)` — [HO/src/deriver/deriver.py#L225-L240](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/src/deriver/deriver.py#L225); [HO/src/crud/representation.py#L60-L72](https://github.com/plastic-labs/honcho/blob/2eb27b6cc0595d3f8deb693f0560e7241c2aeaff/src/crud/representation.py#L60).
  - Truy vấn bảng `documents` sau G1 và G2 [CHẠY]. `session_name` chỉ là nguồn gốc; khoá truy xuất là cặp `observer/observed`:

  ```
  observer     | observed | session_name                          | content
  1001         | 1001     | agent-main-labgram-group--100111-1001 | 1001 tên là Lan
  content-lead | 1001     | agent-main-labgram-group--100111-1001 | 1001 phụ trách fanpage X
  content-lead | 1001     | agent-main-labgram-group--100111-1001 | 1001 thích giọng văn hài hước
  content-lead | 1002     | agent-main-labgram-group--100111-1002 | 1002 tên là Minh
  content-lead | 1001     | agent-main-labgram-group--100222-1001 | KPI tháng 10 của 1001 là 50 bài
  ```
- **Yêu cầu khi tự host [MÃ][CHẠY]:**
  - Postgres có pgvector. Đã chạy được với PG16 + pgvector 0.6.0; compose mẫu dùng PG15.
  - Python ≥3.13.
  - Hai tiến trình: API và deriver.
  - Một endpoint LLM có JSON schema/structured output (cho deriver) và tool calling (cho dialectic).
  - Một endpoint embedding: mặc định 1536 chiều, `VECTOR_DIMENSIONS` đổi được.
  - Các file mã hoá tiktoken, nếu mạng kín.
  - Auth JWT tắt được bằng `AUTH_USE_AUTH=false`.

### Inferences
- AGPL-3.0 chỉ ràng buộc khi **sửa mã server** rồi cung cấp qua mạng cho người khác. Khi đó phải công bố mã đã sửa. Chạy nguyên bản làm dịch vụ nội bộ, hay gọi qua SDK Apache-2.0, thì không kéo Hermes (MIT) vào AGPL. Đây là cách hiểu thông thường về AGPL, chưa qua tư vấn pháp lý [?].
- Deriver cần model tuân thủ JSON schema, dialectic cần tool calling. Model nội bộ yếu có thể sinh quan sát kém [?].

### Gaps
- Chưa kiểm `honcho start --setup` (CLI) hay Docker Compose vì Docker daemon không chạy.
- Chưa đo chi phí token thật.

---

## 4. Cấu hình (2) — Honcho: peer trong nhóm, tiêm ngữ cảnh tự động, alias xuyên kênh, privacy

### Takeaway
Với Honcho, **mỗi người gửi là một peer riêng**, keyed bằng user id thô của nền tảng (`1001`), không phải theo chat.

- **5b-in đạt tự động [CHẠY].** Ở DM(A), lượt đầu tiên đã được tiêm `<memory-context>` gồm dữ kiện A nói ở **G1 và G2**. Model không phải gọi tool.
- **DM(B) chỉ thấy dữ kiện của B [CHẠY].**
- **5b-cross đạt nhưng cấu hình tay.** Thêm `userPeerAliases {"zl-777": "1001"}` vào honcho.json thì A trên nền tảng thứ hai nhận đủ dữ kiện; không cần khởi động lại, chỉ cần `/new` [CHẠY].
- **Ba lỗ hổng privacy [CHẠY]:**
  - (a) Tool `honcho_search(peer="1001")` gọi từ DM của B trả về tin nhắn gốc của A.
  - (b) Session nhóm dùng chung phát lại `<memory-context>` của A vào request ở lượt của B.
  - (c) Peer id không kèm tên nền tảng: người **khác** có id `1001` trên nền tảng khác nhận hồ sơ của Lan.

### Cited Findings
- **Peer người dùng lấy từ user id của phiên gateway [MÃ].**
  - `HonchoSessionManager(..., runtime_user_peer_name=kwargs.get("user_id") …)` — [H/plugins/memory/honcho/__init__.py#L352-L362](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/__init__.py#L352).
  - Thứ tự phân giải: `pinUserPeer`/`peerName` → `userPeerAliases[runtime_id]` → `runtimePeerPrefix + id` → id thô → `peerName` → lỗi `HonchoPeerUnresolvedError` — [H/plugins/memory/honcho/session_peers.py#L81-L106](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/session_peers.py#L81).
  - Tài liệu tóm cùng thứ tự đó: "`pinUserPeer` → `userPeerAliases[id]` → `runtimePeerPrefix + id` → raw runtime ID → `peerName` → session-key fallback" — [H/website/docs/user-guide/features/honcho.md#L187](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/website/docs/user-guide/features/honcho.md#L187).
- **Ý nghĩa ba khoá cấu hình [DOC][MÃ]:**
  - `pinUserPeer`: "every platform user collapses to `peerName`".
  - `userPeerAliases`: "Map of runtime IDs to peers (`{"7654321": "alice"}`). Many-to-one".
  - `runtimePeerPrefix`: "Namespaces unknown runtime IDs (`telegram_7654321`) when no alias matches".
  - [H/website/docs/user-guide/features/honcho.md#L134-L136](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/website/docs/user-guide/features/honcho.md#L134); cách đọc cấu hình tại [H/plugins/memory/honcho/client.py#L293-L310](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/client.py#L293).
  - `runtimePeerPrefix` là **một chuỗi chung** cho mọi nền tảng, không phải bảng prefix theo từng nền tảng. Khoá alias là id thô, không kèm nền tảng.
- **[CHẠY] Peer trong nhóm.** Bảng `peers` sau G1 và G2 gồm `1001`, `content-lead`, `1002`. Mỗi người gửi là một peer; nhóm không phải peer. Session Honcho = session key của gateway đã làm sạch, ví dụ `agent-main-labgram-group--100111-1001`, theo luật "Messaging gateways keep their stable per-chat session key" — [H/plugins/memory/honcho/client.py#L509-L539](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/client.py#L509).
- **[CHẠY] DM(A)** — đoạn nối vào tin nhắn người dùng. Dòng "OK (stub)" là phần bổ sung dialectic do LLM phía Honcho sinh:

  ```
  Bạn biết gì về mình? KPI của mình bao nhiêu?

  <memory-context>
  [System note: The following is recalled memory context, NOT new user input. ...]
  ## User Representation
  ## Explicit Observations
  [2026-09-27 09:31:02] 1001 tên là Lan
  [2026-09-27 09:31:02] 1001 thích giọng văn hài hước
  [2026-09-27 09:31:02] 1001 phụ trách fanpage X
  [2026-09-27 09:31:04] KPI tháng 10 của 1001 là 50 bài
  OK (stub)
  </memory-context>
  ```
  - Cơ chế: `get_prefetch_context` lấy representation mà `observer=assistant peer` giữ về `target=user peer`, trên mọi session — [H/plugins/memory/honcho/session_context.py#L123-L178](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/session_context.py#L123).
  - Khối được nối vào nội dung tin nhắn người dùng qua `build_memory_context_block` — [H/agent/turn_context.py#L83-L103](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/agent/turn_context.py#L83).
- **[CHẠY] DM(B):** `<memory-context>` chỉ có "1002 tên là Minh", không có dữ kiện nào của Lan.
- **[CHẠY] 5b-cross.**
  - Trước khi có alias: A trên `labzalo` (`zl-777`) nhận `<memory-context>` rỗng, chỉ có "OK (stub)". Honcho tạo peer mới `zl-777`.
  - Sau khi thêm `"userPeerAliases": {"zl-777": "1001"}` vào `~/.honcho/config.json` và gửi `/new`: `<memory-context>` có đủ bốn dữ kiện của `1001`.
  - Cách liên kết: **quản trị viên sửa file cấu hình bằng tay**. Không có lệnh hay luồng để người dùng tự liên kết, không có xác minh. Cũng không có liên kết tự động theo email hay số điện thoại.
- **[CHẠY] Id thô trùng giữa nền tảng.** Một người khác, "Tuấn", trên `labzalo` có user id `1001` → `<memory-context>` hiện đủ hồ sơ của Lan.
  - Telegram và Discord truyền id số thô, ví dụ `user_id=str(interaction.user.id)` — [H/plugins/platforms/discord/adapter.py#L4681](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/platforms/discord/adapter.py#L4681).
  - Hai plugin Zalo tự thêm tiền tố `zalo:` / `zalo-oa:` (mục 7), nên với Zalo va chạm khó xảy ra.
- **[CHẠY] Privacy qua tool.** Từ DM(B), stub gọi `honcho_search {"query":"KPI fanpage","peer":"1001"}` và nhận:

  ```
  [1001 · agent-main-labgram-group--100222-1001] Nhớ giúp: KPI tháng 10 của mình là 50 bài.
  [1001 · agent-main-labgram-group--100111-1001] Mình là Lan, phụ trách fanpage X, thích giọng văn hài hước.
  [1001 · agent-main-labgram-dm-1001] Bạn biết gì về mình? KPI của mình bao nhiêu?
  ```
  - Schema tool ghi rõ: "Or pass any peer ID from this workspace. Spans every session that peer took part in" — [H/plugins/memory/honcho/tool_schemas.py#L49-L50](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/tool_schemas.py#L49).
  - Mã tìm theo `peer_perspective`, không kiểm tra người đang hỏi — [H/plugins/memory/honcho/session_context.py#L224-L243](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/session_context.py#L224).
  - `honcho_profile`, `honcho_context` và `honcho_reasoning` cũng nhận `peer` tuỳ ý — [H/plugins/memory/honcho/__init__.py#L918-L972](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/__init__.py#L918).
- **[CHẠY] Nhóm dùng chung (`group_sessions_per_user: false`, nhóm G3).**
  - Lan nói trước, Minh nói sau. Request ở lượt của Minh vẫn chứa tin `[Lan] Chào cả nhóm…` **kèm nguyên `<memory-context>` của Lan**, gồm cả KPI 50 bài mà Lan chỉ nói ở G2.
  - Nguyên nhân: nội dung đã tiêm được lưu thành sidecar và phát lại ở các lượt sau, "what turn N sends is what turn N+1 replays" — [H/agent/turn_context.py#L93-L103](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/agent/turn_context.py#L93).
  - Transcript trong DB thì sạch, chỉ có `[Lan] Chào cả nhóm…`.
  - Phần ghi thì đúng người: "Each turn is written under the peer of whoever wrote it" — [H/website/docs/user-guide/features/honcho.md#L189](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/website/docs/user-guide/features/honcho.md#L189); `resolve_author_peer_id` tại [H/plugins/memory/honcho/session_peers.py#L151-L171](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/session_peers.py#L151).
  - Cache agent có đưa `user_id` vào khoá, nhằm tránh gán nhầm peer — [H/gateway/run_agent_cache.py#L98-L135](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/run_agent_cache.py#L98).
- **Workspace và aiPeer [MÃ].**
  - `workspace_id` mặc định = host key, tức mỗi profile một workspace, trừ khi đặt `workspace` chung. `ai_peer` mặc định = host — [H/plugins/memory/honcho/client.py#L283-L284](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/client.py#L283).
  - Host key của profile có tên là `hermes_<profile>` — [H/plugins/memory/honcho/client.py#L58-L95](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/client.py#L58).
  - Lần chạy lab dùng `workspace: "marketing"` chung, `aiPeer` là `content-lead` và `copywriter`.
- **Honcho song song với built-in [CHẠY][DOC].** `memory.provider: honcho` vẫn giữ tool `memory` (USER.md). Tài liệu mô tả Honcho "adds … on top of Hermes's built-in memory system" — [H/website/docs/user-guide/features/honcho.md#L9](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/website/docs/user-guide/features/honcho.md#L9). Nếu model vẫn ghi USER.md, rò rỉ ở mục 2 vẫn còn.

### Inferences
- Honcho giải được bài toán chính của phòng Marketing: một người, nhiều nhóm và DM, khoá theo người, tiêm tự động. Điều kiện:
  - (1) giữ `group_sessions_per_user=true`, là mặc định;
  - (2) tắt `user_profile_enabled` của built-in, hoặc dặn model không ghi USER.md;
  - (3) dùng `recallMode: context` để **ẩn** tool `honcho_*`, hoặc chặn tham số `peer` bằng `pre_tool_call`. Không thì B có thể hỏi về A.
- Liên kết xuyên kênh là bảng alias tĩnh trong file JSON. Với vài chục nhân viên thì quản được. Nhưng không có quy trình xác minh, và id thô không kèm nền tảng.

### Gaps
- Chưa kiểm `pinUserPeer: true`. Theo mã, mọi người sẽ gộp về một peer, tức là tệ hơn cho nhiều người dùng.
- Chưa kiểm peer card (`honcho_profile` / `honcho_conclude`) và dream.
- Chưa kiểm vì sao lượt đầu của Minh trong G3 dùng chung không có "User Representation" của chính Minh. Nhiều khả năng do prefetch chạy bất đồng bộ ở lượt đầu, `firstTurnBaseWait` = 3 giây [?].

---

## 5. 5d — agent 1 giao việc cho agent 2: danh tính của A có tới prompt của agent 2 không? Kèm PoC plugin

### Takeaway
**Không, ở cả hai cấu hình [CHẠY].**
- Worker kanban (profile `copywriter`) chỉ nhận "work kanban task t_…". `kanban_show`/`build_worker_context` trả về tiêu đề, Assignee, Status, Workspace, Body. Không có Lan, không có 1001.
- Task lưu `created_by='default'`, tức tên profile.
- Subagent `delegate_task` bỏ qua memory hoàn toàn.
- Với Honcho, worker báo "Honcho memory is off … no user peer".
- **Đường plugin thì chạy được mà không cần fork [CHẠY]:** `post_tool_call(kanban_create)` ghi task → người yêu cầu, và `pre_llm_call` trong worker đọc `HERMES_KANBAN_TASK` để tiêm "làm thay mặt Lan (labgram user_id=1001)…".

### Cited Findings
- **[CHẠY] Kanban, built-in.** Từ DM(A), stub gọi `kanban_create {title:"Viết 3 caption cho fanpage X", assignee:"copywriter"}`. Dispatcher trong gateway spawn worker `copywriter`.
  - System prompt của worker có `Platform: cli`, không có "Lan", "1001", "USER PROFILE" hay "Current Session Context".
  - Worker gọi `kanban_show` và nhận `worker_context`:

  ```
  # Kanban task t_b4785bc3: Viết 3 caption cho fanpage X
  Assignee: copywriter
  Status:   running
  Workspace: scratch @ .../kanban/workspaces/t_b4785bc3
  ## Body
  Viết 3 caption giọng hài hước cho fanpage X.
  ```
  - Hàm dựng header: `_ctx_header` chỉ gồm Assignee, Status, Tenant, Workspace, Max runtime, Branch, Body — [H/hermes_cli/kanban_db.py#L4048-L4071](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/kanban_db.py#L4048).
- **[CHẠY] Dòng `tasks` trong `kanban.db`:** `created_by='default'`, `tenant=None`. `session_id` đôi khi được điền (`20260927_092547_87eadf54`), đôi khi `None`.
  - `created_by` luôn là tên profile: "Never taken from tool args … a caller-supplied identity could forge an authoritative-looking author" — [H/tools/kanban_tools.py#L139-L150](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/tools/kanban_tools.py#L139).
  - **Chỉ** bảng `kanban_notify_subs` lưu `user_id='1001'`, `chat_id='1001'`, `platform='labgram'`, `delivery_mode='notify+wake'`. Dữ liệu này dùng để báo kết quả về DM của A. Đã quan sát "[kanban] Task t_8a780a62 completed." đánh thức lại session DM(A) [CHẠY]. Tức là danh tính chỉ nằm trong một cột DB, không tới agent 2.
- **[CHẠY] Kanban + Honcho.** Worker nhận đúng khối sau; log profile ghi `Honcho background session init failed: … no user peer for session 't_9dd66742'`:

  ```
  work kanban task t_9dd66742
  <memory-context>
  [Honcho memory status] Honcho memory is off for this session. Honcho has no user peer for session
  't_9dd66742': the transport supplied no user identity and honcho.json declares no peerName. ...
  </memory-context>
  ```
- **[CHẠY] `delegate_task` (subagent cùng profile).** Request của subagent có `Platform: subagent` và 3 tool. Không có "Lan", "1001", USER PROFILE hay session context. Nó chỉ nhận `goal` và `context` do agent 1 tự viết.
  - Mã: `skip_context_files=True, skip_memory=True` — [H/tools/delegate_tool.py#L241](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/tools/delegate_tool.py#L241).
  - Subagent cũng bị ẩn khỏi `session_search` — [H/tools/session_search_tool.py#L23](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/tools/session_search_tool.py#L23).
- **Bot Mode `message_agent` [MÃ].** Tool này chỉ được tiêm vào session "Bot Chat" trên bản cài quản lý bằng Bot Mode, "never in the registry or any toolset". Không dùng được trong session gateway Telegram — [H/tools/bot_mode_dm.py#L1-L13](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/tools/bot_mode_dm.py#L1). Chưa kiểm chứng tool này có mang người khởi xướng hay không.
- **[CHẠY] PoC plugin `lab-identity`** (khoảng 50 dòng Python, kind `standalone`, đặt ở `plugins/` của cả hai profile và bật trong `plugins.enabled`). Không sửa core.
  - `post_tool_call`: khi `tool_name == "kanban_create"`, parse `result` lấy `task_id`, đọc `gateway.session_context.get_session_env("HERMES_SESSION_USER_ID" / "_USER_NAME" / "_PLATFORM" / "_CHAT_ID" / "_CHAT_TYPE" / "_CHAT_NAME")`, rồi ghi `<hermes root>/lab_requesters.json`. Kết quả ghi được:

    ```json
    {"t_98c182e4": {"platform": "labgram", "user_id": "1001", "user_name": "Lan", "chat_id": "1001", "chat_type": "dm", "chat_name": "Lan"}}
    ```
  - `pre_llm_call` trong worker: có `HERMES_KANBAN_TASK` thì tra bảng và trả `{"context": …}`. Tin nhắn đầu của worker lúc đó là:

    ```
    work kanban task t_98c182e4

    [lab-identity] Bạn đang làm việc THAY MẶT người yêu cầu: Lan (labgram user_id=1001), yêu cầu gốc từ dm "Lan" (chat_id=1001).
    ```
  - `pre_llm_call` trong gateway (lượt của agent 1) tiêm `[lab-identity] Người gửi lượt này: platform=labgram user_id=1001 name=Lan chat=dm:1001`. Điều này vá luôn khe hở 5a "prompt không có user ID".
  - Nguồn các hook:
    - `pre_llm_call` nhận `session_id, task_id, user_message, conversation_history, is_first_turn, model, platform, parent_session_id, sender_id` và tiêm vào tin nhắn người dùng — [H/agent/turn_context.py#L749-L800](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/agent/turn_context.py#L749).
    - Danh sách ContextVar `HERMES_SESSION_*` — [H/gateway/session_context.py#L36-L47, L173-L179](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/session_context.py#L36).
  - Lưu ý khi chạy: task được tạo **trước** khi bật plugin (`t_04838591`) thì không có bản ghi, nên worker không được tiêm gì.

### Inferences
- Lõi Hermes cố ý không cho người yêu cầu đi theo task: người yêu cầu không được ghi ở đâu mà prompt của worker đọc tới, và `created_by` không nhận giá trị từ tham số tool. Plugin hai hook là đủ cho kanban.
- Với `delegate_task`, `pre_llm_call` của subagent có `parent_session_id`, nên plugin có thể tra ngược người gửi của session cha. Cách này chưa chạy thử [?].
- Muốn agent 2 cũng **nhớ** A qua Honcho, worker cần user peer. Hiện `initialize` lấy peer từ `user_id` của gateway [H/plugins/memory/honcho/__init__.py#L352-L362](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/__init__.py#L352), mà worker không có. Có hai cách không fork, cả hai chưa kiểm chứng [?]:
  - plugin đặt `HERMES_HONCHO_HOST`/`peerName` riêng cho từng task;
  - dùng tool Honcho với `peer="1001"`.

### Gaps
- Chưa chạy PoC trên `delegate_task` và Bot Mode.
- Chưa kiểm PoC khi worker chạy trên máy khác. Bảng `lab_requesters.json` dùng filesystem chung, nên production cần DB dùng chung.

---

## 6. R2' — vai trò, chức danh, phòng ban của agent

### Takeaway
Hermes có **mô tả profile** (1–2 câu văn tự do trong `profile.yaml`) và **SOUL.md** (persona). Không có trường chức danh hay phòng ban, cũng không có nhóm "team/department".
- Mô tả profile **được dùng thật** ở một chỗ: bộ decomposer kanban (LLM phụ trợ) xem danh sách profile kèm mô tả để chọn assignee cho task triage.
- Agent 1 khi tự gọi `kanban_create` **không** được thấy danh sách hay mô tả profile [CHẠY]. Nó phải tự biết tên profile.
- Trường `role` duy nhất là `"setup"` (quyền backend), không phải vai trò tổ chức.

### Cited Findings
- **`profile.yaml`:** `read_profile_meta` trả về `description, description_auto, display_name, bot_title (ui_meta.hermes-bots.title), previous_names, role`, trong đó `role` chỉ nhận giá trị thuộc `PROFILE_ROLES = frozenset({SETUP_ROLE})` và `SETUP_ROLE = "setup"` — [H/hermes_cli/profiles.py#L96-L97, L851-L883](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/profiles.py#L851).
  - Comment ở `write_profile_meta`: "``role`` grants backend capabilities, so no client-facing writer passes it through".
  - `bot_title` chỉ được đưa ra web UI — [H/hermes_cli/web_routers/profiles.py#L95](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/web_routers/profiles.py#L95).
- **[CHẠY]** Tạo được `hermes profile create copywriter --description "Copywriter – Phòng Marketing: …"` và `hermes profile describe default --text "Content Lead – Phòng Marketing: …"`. CLI mô tả lệnh là "Read or set a profile's description (used by the kanban orchestrator)".
- **Decomposer dùng mô tả để định tuyến:**
  - `_build_roster()` đọc `p.description` hoặc "(no description; profile named …)".
  - Prompt: "Pick assignees from the roster by matching the task to the profile's DESCRIPTION (not just the name). When nothing matches well, use null…".
  - Cấu hình `kanban.orchestrator_profile` và `kanban.default_assignee`.
  - [H/hermes_cli/kanban_decompose.py#L1-L12, L72-L74, L97-L105, L156-L183, L213-L214](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/kanban_decompose.py#L156)
- **[CHẠY] Agent 1 không thấy mô tả của copywriter.**
  - System prompt của agent 1 không chứa chuỗi "viết caption, bài đăng" hay tên profile "copywriter". Chỉ có SOUL.md của chính nó.
  - Mô tả tham số `assignee` của `kanban_create` chỉ là: "Profile name that should execute this task (e.g. 'researcher-a', 'reviewer', 'writer'). Required".
- **Định tuyến tin nhắn tới profile** theo `user_id`/`thread_id`/`chat_id`/`guild_id` (`gateway.profile_routes`), không theo vai trò — [H/gateway/profile_routing.py#L1-L10](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/profile_routing.py#L1).
- **Không có khái niệm "department" [MÃ].** `grep -rl department` trên `hermes_cli/ gateway/ agent/ tools/` không có kết quả. Kanban có "boards" (tên, mô tả, icon, màu, thư mục làm việc) nhưng không có danh sách thành viên hay quyền theo board — [H/hermes_cli/kanban_boards.py#L16-L190](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/kanban_boards.py#L16).

### Inferences
- Có thể mô phỏng "Content Lead – Phòng Marketing" bằng description, SOUL.md và `display_name`. Chỉ decomposer "hiểu" cấu trúc này, và nó hiểu qua văn bản tự do.
- Không có cây tổ chức, không có "trưởng nhóm duyệt", không có định tuyến theo phòng ban. Muốn có thì phải tự làm, ví dụ plugin `pre_llm_call` tiêm danh sách đồng đội kèm mô tả vào prompt của agent 1.

### Gaps
- Chưa chạy decomposer với stub trong lần này. Lần nghiên cứu trước đã chụp màn hình trang "Orchestration settings", xem thư mục `Nền tảng agent cho phòng Marketing/screenshots/`.

---

## 7. Kiểm lại plugin Zalo cho Hermes

### Takeaway
Hai plugin vẫn thuộc owner `tinovn`, commit cuối lần lượt 2026-09-11 và 2026-09-14. **Cả hai không có file LICENSE.**
- `hermes-zalo-oa-plugin`: `plugin.yaml` ghi "MIT — dùng tự chịu trách nhiệm…".
- `hermes-zalo-plugin` (Zalo cá nhân): `plugin.yaml` **không** ghi MIT; chỉ có "Dùng tự chịu trách nhiệm — xem README". Ghi chú trước từng gắn MIT cho OA plugin; riêng plugin cá nhân thì thực tế **chưa có license mã nguồn mở rõ ràng**.
- Cả hai đều truyền `user_id` có tiền tố (`zalo:` / `zalo-oa:`) vào gateway.

### Cited Findings
- **`tinovn/hermes-zalo-oa-plugin`** [MÃ, clone 2026-09-27]:
  - HEAD `88e0bd4bbc99e78d51e6891e63bf629bd659c9aa`, 2026-09-11T14:18:46+07:00, "Merge pull request #1 from tinovn/fix/mo-ta-tool-dung-kenh".
  - 15 commit; commit đầu 2026-09-04.
  - `plugin.yaml:12` `license: "MIT — dùng tự chịu trách nhiệm, tuân thủ điều khoản Zalo OA."`; không có file LICENSE.
  - Gọi `build_source(chat_id=msg.user_id, chat_type="dm", user_id=f"zalo-oa:{msg.user_id}")` (`adapter.py:509-513`).
  - [repo](https://github.com/tinovn/hermes-zalo-oa-plugin)
- **`tinovn/hermes-zalo-plugin`** [MÃ, clone 2026-09-27]:
  - HEAD `e3f3c4fdd2041bd773bacf5a1e0ee4573fc28cc5`, 2026-09-14T15:03:37+07:00, "Merge pull request #26 from tinovn/feat/zalo-group-memory".
  - 90 commit; commit đầu 2026-06-04.
  - `plugin.yaml:12` `license: "Dùng tự chịu trách nhiệm — xem README (rủi ro khoá tài khoản Zalo)."`. README mục "Giấy phép / miễn trừ" ghi: "Cung cấp 'nguyên trạng' (as-is), **không bảo hành**. Dùng API Zalo không chính thức có rủi ro khoá tài khoản."
  - Tin vào: `user_id = f"zalo:{from_uid}"`, `chat_type = "group" if is_group else "dm"` (`adapter.py:2140-2169`).
  - Có `group_memory.py`: "Per-group memory ('sổ tay nhóm') … Owner-only append-only fact/rule store per Zalo chat". Đây là bộ nhớ **theo nhóm**, không theo người.
  - [repo](https://github.com/tinovn/hermes-zalo-plugin)

### Inferences
- Nhờ tiền tố `zalo:`, peer Honcho của người dùng Zalo sẽ là `zalo-<uid>`, vì dấu `:` bị làm sạch thành `-`. Liên kết với Telegram cần alias kiểu `{"zalo:123…": "1001"}`, dùng đúng chuỗi id thô trước khi làm sạch. Suy ra từ `sanitize_peer_id` và `_peer_aliases`, chưa chạy với plugin thật [?].
- Không có LICENSE thì về pháp lý mặc định là "giữ mọi quyền". Muốn dùng hay fork `hermes-zalo-plugin` trong sản phẩm cần xin phép tác giả [?].

### Gaps
- Không gọi api.github.com theo ràng buộc, nên không có số sao và issue mới.
- Chưa chạy hai plugin với tài khoản Zalo thật.

---

## 8. Bảng chấm theo cấu hình

### Takeaway
- **Built-in:** chỉ 5a đạt một phần. 5b-in nhìn như đạt nhưng thực chất là bộ nhớ chung, rò rỉ sang B. 5d không. Privacy không.
- **Honcho (tự host):** 5b-in đạt tự động và khoá theo người. 5b-cross đạt với alias viết tay. 5d không (worker tắt Honcho). Privacy một phần: có ba đường rò đã chứng minh.
- **R2'** như nhau ở cả hai: chỉ có mô tả văn bản, dùng cho decomposer.

### Cited Findings

**Cấu hình (1) — Built-in memory (MEMORY.md/USER.md), Hermes `516535b5`**

| Tiêu chí | Kết quả | Bằng chứng | Nhãn |
|---|---|---|---|
| R2' vai trò/phòng ban của agent | **Một phần** | Có `description`, SOUL.md, `display_name`; `role` chỉ là `setup`; decomposer dùng description để chọn assignee. Không có phòng ban hay nhóm. Agent 1 không thấy roster khi tự `kanban_create`. [profiles.py#L851](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/profiles.py#L851), [kanban_decompose.py#L156](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/kanban_decompose.py#L156) | [MÃ][CHẠY] |
| 5a danh tính người gửi | **Một phần** | Prompt có `**Source:** Labgram ("group: G1 Marketing")` và `**User:** "Lan"`. User ID chỉ hiện khi thiếu tên; nhóm dùng chung chỉ có tiền tố `[Lan]`. ID có trong DB. [session.py#L375](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/session.py#L375) | [CHẠY][MÃ] |
| 5b-in cùng kênh: G1, G2, DM là một người | **Không (khoá theo profile)** | DM(A) tự động thấy dữ kiện G1/G2 qua USER.md, nhưng USER.md là một file chung cho mọi người; `session_search` không lọc theo người. | [CHẠY] |
| 5b-cross xuyên kênh | **Không** | A trên `labzalo` thấy cùng USER.md như mọi người; không có liên kết danh tính. | [CHẠY] |
| 5d agent 2 biết làm thay A | **Không** | Worker kanban chỉ thấy header/body; `created_by=default`; subagent có `skip_memory=True`. | [CHẠY][MÃ] |
| Privacy | **Không** | DM(B) nhận "Lan: KPI tháng 10 là 50 bài"; `session_search` từ DM(B) trả về session của Lan. | [CHẠY] |

**Cấu hình (2) — Honcho self-hosted (server 3.2.1 AGPL-3.0, PG16 + pgvector, `honcho-ai` 2.2.0), `recallMode: hybrid`**

| Tiêu chí | Kết quả | Bằng chứng | Nhãn |
|---|---|---|---|
| R2' | **Một phần** | Như built-in; Honcho chỉ thêm `aiPeer` theo profile, không có chức danh hay phòng ban. | [MÃ] |
| 5a | **Một phần** | Như built-in. Honcho dùng `user_id` để chọn peer nhưng không đưa ID vào prompt; khối context viết "1001 tên là Lan" chỉ vì deriver chép peer id vào câu. | [CHẠY] |
| 5b-in | **Đạt (tự động, khoá theo người)** | Mỗi người gửi là một peer (`1001`, `1002`); quan sát lưu theo (observer=`content-lead`, observed=`1001`); DM(A) lượt đầu được tiêm cả 4 dữ kiện từ G1/G2. Điều kiện: giữ `group_sessions_per_user=true`. | [CHẠY] |
| 5b-cross | **Một phần → Đạt khi cấu hình tay** | `userPeerAliases {"zl-777":"1001"}` trong honcho.json + `/new` là đủ; không có luồng tự liên kết hay xác minh; id thô không kèm nền tảng nên dễ gộp nhầm ("Tuấn" id 1001 trên nền tảng khác nhận hồ sơ Lan). | [CHẠY] |
| 5d | **Không** | Worker kanban: "Honcho memory is off … no user peer"; subagent `skip_memory=True`. | [CHẠY][MÃ] |
| Privacy | **Một phần** | Tiêm tự động thì tách đúng (DM(B) chỉ thấy Minh). Nhưng: (a) `honcho_search(peer="1001")` từ DM(B) trả về tin gốc của Lan; (b) nhóm dùng chung phát lại `<memory-context>` của A ở lượt của B; (c) USER.md built-in vẫn bật song song. | [CHẠY] |

### Inferences
- Nếu chọn Hermes làm nền, **Honcho là bắt buộc** để đạt 5b. Kèm theo phải khoá lại privacy: bật `recallMode: context` hoặc chặn tham số `peer`, tắt USER.md, không dùng nhóm dùng chung.

### Gaps
- Chưa chạy lại R3/R4 (decompose, review) trong đợt này. Các tiêu chí R1, R3, R4, R6–R12 giữ nguyên như ghi chú trước; bằng chứng mới không làm đổi kết luận, trừ ghi chú license Zalo ở mục 7.

---

## 9. Phải tự xây gì, có cần fork không

### Takeaway
**Không cần fork** để đạt 5a đầy đủ, 5d và vá privacy. Mọi điểm móc dưới đây đều có sẵn và đã chạy được hai trong số đó.
- `pre_llm_call`, `post_tool_call`, `pre_tool_call` là hook plugin.
- Cấu hình Honcho gồm `recallMode`, `userPeerAliases`, `group_sessions_per_user`.

**Cần sửa core hoặc sửa plugin Honcho** (plugin Honcho nằm trong repo, nên sửa nó cũng coi như fork) nếu muốn:
- (1) peer id kèm tên nền tảng hoặc bảng alias theo từng nền tảng;
- (2) Honcho hoạt động trong worker kanban dưới danh nghĩa người yêu cầu;
- (3) chặn phát lại memory-context trong nhóm dùng chung.

Lưu ý: CONTRIBUTING.md đã đóng cửa với memory provider mới. Không thể thêm một provider "identity-aware" vào repo; muốn vậy thì phải là plugin ngoài [MÃ, ghi chú trước].

### Cited Findings
- **5a đầy đủ (ID ổn định trong mọi lượt).** Dùng plugin `pre_llm_call` với `sender_id`, `platform` và `get_session_env("HERMES_SESSION_CHAT_ID"/"_CHAT_TYPE"/"_USER_NAME")`. **[CHẠY]** đã tiêm được `platform=labgram user_id=1001 name=Lan chat=dm:1001` — [H/agent/turn_context.py#L749-L771](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/agent/turn_context.py#L749), [H/gateway/session_context.py#L173-L179](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/gateway/session_context.py#L173).
- **5d.** `post_tool_call(kanban_create)` ghi bảng requester, rồi `pre_llm_call` trong worker đọc `HERMES_KANBAN_TASK`. **[CHẠY]** mục 5.
  - Production cần một bảng dùng chung, ví dụ plugin DB hoặc Postgres. Cũng nên hook thêm `kanban_task_claimed` / `on_kanban_worker_spawned` để kiểm tra chéo — [H/hermes_cli/plugins.py#L108-L202](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/hermes_cli/plugins.py#L108).
  - Với `delegate_task`, tra ngược qua `parent_session_id` truyền cho `pre_llm_call` của subagent. Chưa chạy [?].
- **Privacy — không fork:**
  - (a) `recallMode: "context"` ẩn tool `honcho_*` ("context — auto-injection only, tools hidden") — [H/website/docs/user-guide/features/honcho.md#L155](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/website/docs/user-guide/features/honcho.md#L155). Hoặc dùng plugin `pre_tool_call` từ chối `honcho_*` khi `peer` khác `user`/`ai`/peer của người gửi [?].
  - (b) Giữ `group_sessions_per_user: true`, là mặc định.
  - (c) Đặt `memory.user_profile_enabled: false` để tắt USER.md dùng chung — [H/tools/memory_tool.py#L258-L261](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/tools/memory_tool.py#L258).
- **5b-cross — không fork:** quản lý bảng `userPeerAliases` trong `~/.honcho/config.json` hoặc `$HERMES_HOME/honcho.json`. Có thể viết plugin lệnh (`register_command`, ví dụ `/link <mã>`) để người dùng tự liên kết rồi ghi file này. Theo mã, config được đọc lại mỗi lần `initialize` session, và đã quan sát alias có hiệu lực sau `/new` mà không cần khởi động lại [CHẠY].
- **Cần sửa core hoặc plugin Honcho:**
  - (1) **Peer id theo nền tảng.** `_resolve_user_peer_id` chỉ có một `runtime_peer_prefix` toàn cục và alias theo id thô — [H/plugins/memory/honcho/session_peers.py#L81-L106](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/session_peers.py#L81). Cách tránh không cần fork: yêu cầu mọi adapter tự thêm tiền tố vào `user_id`, như hai plugin Zalo đã làm. Telegram và Discord core thì không thêm.
  - (2) **Honcho trong worker.** `initialize` lấy peer từ `kwargs["user_id"]` của gateway — [H/plugins/memory/honcho/__init__.py#L352-L362](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/plugins/memory/honcho/__init__.py#L352). Worker không có giá trị này, nên cần sửa để đọc người yêu cầu từ task.
  - (3) **Phát lại memory-context trong nhóm dùng chung** là hành vi cố ý vì prompt cache — [H/agent/turn_context.py#L93-L103](https://github.com/NousResearch/hermes-agent/blob/516535b54275e963a82b4c28f866338fb768e7bc/agent/turn_context.py#L93).
  - (4) **R2':** chức danh và phòng ban có cấu trúc, định tuyến theo phòng ban. Có thể làm bằng plugin tiêm roster vào prompt; nếu muốn UI hay RBAC thật thì phải sửa core.
- **Zalo.** Không có trong core. Có thể dùng plugin `tinovn` bằng `register_platform` mà không fork Hermes, nhưng phải để ý license (mục 7).

### Inferences
- Cấu hình khuyến nghị nếu dùng Hermes:
  - Honcho tự host với `recallMode: context`, `group_sessions_per_user: true`, `user_profile_enabled: false`;
  - bảng `userPeerAliases` do một plugin `/link` quản lý;
  - plugin identity (`pre_llm_call` + `post_tool_call`) cho 5a và 5d.

  Phần còn thiếu thực sự là agent 2 **nhớ** A qua Honcho khi làm task (cần sửa plugin Honcho), và cấu trúc phòng ban.

### Gaps
- Chưa đo độ trễ hay chi phí của Honcho khi dùng model thật.
- Chưa kiểm plugin `pre_tool_call` chặn `honcho_*` và chưa kiểm plugin `/link`.
