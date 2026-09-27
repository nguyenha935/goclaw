# Kiểm lại 5 dự án "tổ chức AI" đã bị loại: VisionClaw, FleetQ, Agentic Organization, Foundry, MDH

Ngày kiểm: 2026-09-27 (xác nhận bằng `date` trên máy: `Sun Sep 27 03:41:53 UTC 2026`). Mốc R8 "còn sống" = có release/tag từ 2026-06-27 trở đi.

Phương pháp: `git clone --filter=blob:none` cả 5 repo (có lịch sử commit + tag), đọc mã thật; ngày lấy từ `git log`/`git for-each-ref`; sao/forks lấy từ trang GitHub ngày 2026-09-27. Không cài đặt/chạy thử dự án nào → không có nhãn [CHẠY]. Nhãn: [MÃ] = đọc mã nguồn, [DOC] = chỉ README/docs, [?] = chưa kiểm chứng.

Commit đã đọc:
| Dự án | Repo | Commit HEAD đã đọc | Ngày commit HEAD |
|---|---|---|---|
| VisionClaw | https://github.com/Huskyauto/VisionClaw-Agent-Public-Release | `9ae729eb6728d89d48563cfe5b51f1f3095140ad` (= tag `r135.4-sec`) | 2026-09-23 |
| FleetQ | https://github.com/escapeboy/agent-fleet-o | `e2abe66c17e2efdeaf4615606a3e75e14f8796df` | 2026-09-21 |
| Agentic Organization | https://github.com/fab-agent/agentic-organization | `bf29743fbb0c2254b55a40261a9ca4d60406416f` | 2026-09-09 |
| Foundry | https://github.com/axislab-top/Foundry | `2daebc43f3ebd012bd875e2da058df79efb36fb1` | 2026-06-30 |
| MDH | https://github.com/MonSp/MDH | `6e406dbbfb0263b8b58e93158c58b6a7ceb7b221` | 2026-09-24 |

Quy ước link nguồn bên dưới: `VC/…` = `https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/…`; `FQ/…` = `https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/…`; `AO/…` = `https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/…`; `FD/…` = `https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/…`; `MD/…` = `https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/…`. Mọi link bên dưới đều là link đầy đủ.

---

## Câu 1 — VisionClaw (Huskyauto): có đáng khôi phục không? (backend riêng, COO/CEO tách việc thành DAG, xử lý yêu cầu mơ hồ, critic, 41 governance rules, identity, kênh, multi-tenant, plugin, nhịp phát hành)

### Takeaway
Mã thật mạnh hơn nhiều người nghĩ ở R1–R4 (backend tự gọi API model, CEO Orchestrator tách việc thành DAG `dependsOn` chạy song song, có active-clarification, critique agent, approval gate, 41 luật governance được một bộ đánh giá định kỳ thực thi thật). Nhưng R5 (identity) — tiêu chí quan trọng nhất — gần như bằng 0: kênh Telegram/Discord đổ hết vào tenant admin #1, không truyền danh tính người gửi vào engine, không có hồ sơ người dùng đa kênh, không có chức danh/phòng ban cho người. Thêm vào đó: 1 người bảo trì, ~360k dòng TS, bản public là "mirror" squash. **Kết luận: vẫn loại (không khôi phục làm ứng viên chính)**; chỉ đáng tham khảo thiết kế R3/R4.

### Cited Findings

**Repo & sức sống**
- Repo chính xác: `Huskyauto/VisionClaw-Agent-Public-Release`, MIT, "Copyright (c) 2026 Robert Washburn" [MÃ] — [LICENSE](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/LICENSE)
- Sao/forks: 26 sao, 10 fork, 1 issue mở (thấy ngày 2026-09-27) — [GitHub repo page](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release)
- Là "public mirror snapshot": nhánh main chỉ có **1 commit**; 67 tag, mỗi release là 1 snapshot. Tag mới nhất `r135.4-sec` ngày 2026-09-23; trước đó `r132.6` 2026-09-20… Số tag theo tháng (git): 2026-04: 2, 2026-06: 1, 2026-07: 20, 2026-08: 12, 2026-09: 32. Không đo được nhịp commit thật vì lịch sử bị squash; `git log --all` qua các snapshot: 76 commit của Robert Washburn + 31 dependabot + 2 "Platform Agent" + 2 bot [MÃ] — [Releases](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/releases/tag/r135.4-sec)
- Tự nhận "solo-maintained" — [docs/KNOWN_LIMITATIONS.md](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/docs/KNOWN_LIMITATIONS.md)
- LOC thực đo [MÃ]: `server/` 293.219 dòng TS (1.059 file), `client/` 59.604 (197 file), `shared/` 7.172 (18 file) → **359.995 dòng / 1.274 file** không tính test/scripts; toàn repo 487.559 dòng TS / 2.092 file. README ghi "Roughly 320k lines of TypeScript across 1,100+ files" → lệch — [README.md#L52](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/README.md#L52)

**R1 — backend riêng** [MÃ]
- `server/providers.ts` dùng SDK `openai` với `baseURL` cho nhiều nhà cung cấp, key giải mã bằng `decryptApiKey` (bảng `tenant_provider_keys`); có "claude-runner" (Claude Agent SDK bridge, cổng 7779) là đường tuỳ chọn cho subscription token — [server/providers.ts#L1](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/providers.ts#L1), [server/claude-runner.ts#L1](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/claude-runner.ts#L1)

**R3 — "COO tách việc thành đồ thị phụ thuộc"** [MÃ]
- Trong mã là **"CEO Orchestrator"** (`generateExecutionPlan`), không có agent tên "COO"; README gọi Felix là "CEO / COO" và "the COO automatically decomposes complex requests into DAG task graphs" — [README.md#L344](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/README.md#L344), [README.md#L407](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/README.md#L407)
- `OrchestrationStep` có `assignedPersona`, `dependsOn: number[]`, trạng thái `awaiting_approval` — [server/ceo-orchestrator.ts#L44](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/ceo-orchestrator.ts#L44)
- Prompt planner liệt kê 14 phòng ban/chuyên gia (Marketing & Growth = Teagan, Content = Scribe, Review = Proof…) và bắt trả JSON `{task_id, description, required_skill_type, depends_on}`; tối đa 6–8 task, ưu tiên song song — [server/ceo-orchestrator.ts#L260](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/ceo-orchestrator.ts#L260)
- Trình thực thi `_executePlanImpl` chỉ chạy step khi mọi `dependsOn` đã xong (dòng ~723) — [server/ceo-orchestrator.ts#L636](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/ceo-orchestrator.ts#L636)
- Yêu cầu mơ hồ: `active-clarification.ts` — Stage 1 heuristic regex **tiếng Anh** (`it|this|that…`, `thing|stuff…`, <4 từ không ngữ cảnh), Stage 2 gọi model judge cứng `gpt-5.6-sol`, ngân sách 1.500 ms, **fail-open** (lỗi thì bỏ qua hỏi lại) — [server/active-clarification.ts#L1](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/active-clarification.ts#L1); được gọi trong luồng chat chính (depth 0) — [server/chat-engine.ts#L2121](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/chat-engine.ts#L2121)
- "Acceptance criteria": `GoalContract {endState, verificationMethod, invariants, errorBudget…}` do LLM trích xuất và dùng cho **completion evaluator** (model khác model làm việc) chấm sau khi chạy, không phải để hỏi người dùng trước — [server/agentic/goal-contract.ts#L27](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/agentic/goal-contract.ts#L27), [server/tools.ts#L5879](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/tools.ts#L5879)
- Có thêm tool `deep-interview` (phỏng vấn nhiều lượt) gọi qua tool — [server/deep-interview.ts](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/deep-interview.ts)

**R4 — critic & 41 governance rules** [MÃ]
- `critique-agent.ts`: chấm 4 chiều (accuracy/completeness/relevance/clarity), ngưỡng 6.0, tự refine; chạy như lời gọi độc lập (không chia sẻ lịch sử) — [server/critique-agent.ts#L1](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/critique-agent.ts#L1); gắn vào pipeline chat với `{ name: "critique-agent", onFail: "fix" }` — [server/chat-engine.ts#L4408](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/chat-engine.ts#L4408)
- Human approval: `createApproval()` ghi `agent_approvals` (TTL mặc định 48h) và **pause** `agent_runs` tới khi duyệt — [server/agentic/approvals.ts#L17](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/agentic/approvals.ts#L17)
- 41 luật: mảng `RULES` trong `seedGovernanceRules()` có đúng **41** mục (đếm được), mỗi mục là JSON `condition` + `action` (vd `content-review-enforcement`: "Ensure all Scribe content goes through Proof before publishing"; `conflict-of-interest-prevention`: agent không tự duyệt việc của mình) — [server/seed-infrastructure.ts#L222](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/seed-infrastructure.ts#L222)
- Thực thi: `process-governor.ts` nạp luật từ DB theo `tenant_id` và `evaluateCondition()` switch trên `cond.check` (39 loại check khác nhau; 38 có `case`, `procedure_edit_apply` không có case) rồi áp action (throttle, escalate, block_delegation, kill_switch…) — [server/process-governor.ts#L293](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/process-governor.ts#L293); được gọi định kỳ bởi heartbeat task `process_governance` — [server/heartbeat.ts#L1510](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/heartbeat.ts#L1510). → Là **giám sát/khắc phục định kỳ bằng mã**, không phải prompt, nhưng cũng không phải cổng chặn trước mỗi hành động (vd luật Scribe→Proof chỉ phát hiện "bypassed reviews" sau đó).
- Chính docs của dự án ghi con số "governance 41" là **⚠️unverified** và chưa rõ "đo cái gì" — [docs/architecture-notes.md#L76](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/docs/architecture-notes.md#L76)

**R5 — identity** [MÃ]
- Telegram: chỉ user đã "pair" (bảng `telegram_approved_users`) mới được trả lời; conversation theo `chat.id`; gọi `processMessage(conversationId, text, { tenantId: ADMIN_TENANT_ID, source: "telegram" })` — **không truyền ai gửi** — [server/telegram.ts#L176](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/telegram.ts#L176); chú thích "Single-tenant platform: Telegram channel owned by admin tenant" — [server/telegram.ts#L222](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/telegram.ts#L222)
- Discord tương tự, cứng `ADMIN_TENANT_ID` — [server/discord.ts#L93](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/discord.ts#L93); `ADMIN_TENANT_ID = 1` — [server/tenant-constants.ts#L5](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/tenant-constants.ts#L5)
- WhatsApp đi qua "channel kernel" với `fromIdentifier` (JID) nhưng kernel **bỏ `fromIdentifier`** khi gọi engine (chỉ truyền `tenantId`, `source`) — [server/channels/kernel.ts#L180](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/channels/kernel.ts#L180); `ChatEngineOptions` không có trường người gửi/user — [server/chat-engine.ts#L97](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/chat-engine.ts#L97)
- Mô hình dữ liệu người: `tenants` (1 tenant = 1 tài khoản email/password, cờ `is_admin`), `team_members` (email, display_name, `role` mặc định `viewer`); **không có** chức danh, phòng ban cho người, không có bảng liên kết danh tính đa kênh; `department_budgets` là ngân sách theo phòng ban **của agent** — [shared/schema.ts#L12](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/shared/schema.ts#L12), [shared/schema.ts#L2472](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/shared/schema.ts#L2472), [shared/schema.ts#L1087](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/shared/schema.ts#L1087)

**R6 — kênh** [MÃ]
- Có Telegram, Discord, WhatsApp (Baileys), Twilio SMS, email, Slack slash command, "glasses gateway"; README liệt kê "WhatsApp, Telegram, Discord (with approval workflows)" — [README.md#L659](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/README.md#L659)
- Thêm adapter mới phải sửa lõi: `ChannelName` là union type cứng + `KNOWN_CHANNELS` (hướng dẫn "Add an entry to KNOWN_CHANNELS below") — [server/channels/kernel.ts#L71](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/channels/kernel.ts#L71). Không có Zalo.

**R10/R11 — multi-tenant & plugin** [MÃ]
- Có `tenants`, `tenant_id` khắp bảng, nhiều báo cáo audit cách ly tenant trong `docs/`; nhưng kênh chat gắn tenant 1; bảng `mcp_servers` không có `tenant_id` (`listMcpServers` không lọc tenant) — [server/mcp-client.ts#L28](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/mcp-client.ts#L28); demo chính thức là "single-tenant showcase" — [docs/KNOWN_LIMITATIONS.md#L15](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/docs/KNOWN_LIMITATIONS.md#L15)
- Plugin: không có cơ chế nạp plugin. `registerHook()` chỉ đăng ký bằng code trong tiến trình — [server/hooks.ts#L49](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/hooks.ts#L49); thêm tool = sửa `server/tools.ts` (~20.000 dòng) — [docs/adding-a-tool.md](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/docs/adding-a-tool.md); có thể gắn MCP server ngoài qua DB/UI (`addMcpServer`) — [server/mcp-client.ts#L63](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/mcp-client.ts#L63)
- R9: trang `agent-diagram.tsx` (624 dòng) chỉ hiển thị agent sống, không có kéo-thả/mutation → trang trí — [client/src/pages/agent-diagram.tsx](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/client/src/pages/agent-diagram.tsx)

**README tự mâu thuẫn** [MÃ]/[DOC]
- README: "420 tools · 141 capabilities · 18 personas · 41 governance rules · 839 indexes · 78 models"; `docs/release-facts.json` ngày 2026-09-19 khớp các số này; nhưng `docs/fable5-handoff.md` ghi "~394 tools… 16 personas, ~623 indexes"; ảnh "Command Center" trong docs ghi "15 specialist agents / 220 connected tools / 37+ model routes"; snippet tìm kiếm cũ của mô tả repo ghi "137 capabilities · 777 indexes · 80 models" — [README.md#L52](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/README.md#L52), [docs/fable5-handoff.md](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/docs/fable5-handoff.md), [docs/images/tour-command-center.jpg](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/docs/images/tour-command-center.jpg)

**Ảnh thật (UI)**: `docs/images/screenshot-home.jpg`, `screenshot-chat.jpg`, `tour-command-center.jpg`, `tour-agent-activity.jpg`, thư mục `screenshots/` (23 ảnh). Đã lưu bản sao: `screenshots/visionclaw-screenshot-home.jpg`, `screenshots/visionclaw-tour-command-center.jpg` (ảnh Command Center: giao diện tối, 3 thẻ số liệu, danh sách việc "Complete/Ready/Reviewed") — [docs/images](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/tree/9ae729eb6728d89d48563cfe5b51f1f3095140ad/docs/images)

**Bảng kiểm claim của phiên trước**
| Claim | Kết quả | Bằng chứng |
|---|---|---|
| MIT | Đúng [MÃ] | LICENSE |
| Backend riêng | Đúng [MÃ] | providers.ts (OpenAI SDK + baseURL, key mã hoá) |
| Multi-tenant | Một phần/Đã thay đổi nghĩa [MÃ] | có tenant_id, nhưng Telegram/Discord cứng tenant 1, mcp_servers toàn cục |
| "COO agent" tách việc thành đồ thị phụ thuộc | Đúng về bản chất, sai tên [MÃ] | `ceo-orchestrator.ts` (CEO Orchestrator), `dependsOn` + thực thi theo phụ thuộc |
| Critic agent | Đúng [MÃ] | critique-agent.ts + completion evaluator |
| 41 governance rules | Đúng số lượng, thực thi bằng mã theo chu kỳ [MÃ] | seed 41 mục; process-governor; docs tự ghi "unverified" |
| Kênh Telegram/Discord/WhatsApp | Đúng (+SMS, email, Slack) [MÃ] | telegram.ts, discord.ts, whatsapp.ts |
| Một người bảo trì | Đúng [MÃ] | git log --all; KNOWN_LIMITATIONS |
| ~320k dòng | Sai (thực ~360k dòng TS không tính test; 488k toàn repo) [MÃ] | đếm `wc -l` |
| README tự mâu thuẫn số liệu | Đúng [MÃ]/[DOC] | xem trên |

**Chấm 12 tiêu chí**
| # | Điểm | Bằng chứng ngắn |
|---|---|---|
| R1 | Đạt [MÃ] | OpenAI SDK + baseURL, key tenant mã hoá; claude-runner chỉ là tuỳ chọn |
| R2 | Đạt [MÃ] | 18 persona theo phòng ban, CEO Orchestrator phân công, chạy song song |
| R3 | Một phần [MÃ] | có clarify (heuristic tiếng Anh, fail-open, model cứng), DAG, GoalContract; tiếng Việt mơ hồ có thể lọt heuristic [?] |
| R4 | Đạt [MÃ] | critique-agent onFail fix, approvals pause run, completion evaluator khác model; governance định kỳ |
| R5a | Một phần [MÃ] | biết kênh (`source`) và chat; không biết người gửi cụ thể |
| R5b | Không [MÃ] | không có bảng liên kết danh tính đa kênh |
| R5c | Không [MÃ] | team_members chỉ có role; không chức danh/phòng ban/quyền yêu cầu |
| R5d | Không [MÃ] | delegation mang tenant/persona, không mang "thay mặt ai" |
| R6 | Một phần [MÃ] | nhiều kênh nhưng thêm adapter phải sửa kernel.ts; không Zalo |
| R7 | Đạt [MÃ] | MIT, self-host Docker |
| R8 | Đạt [MÃ] | tag r135.4-sec 2026-09-23; 64 tag từ 2026-07 đến 2026-09 |
| R9 | Không [MÃ] | agent-diagram chỉ hiển thị |
| R10 | Một phần [MÃ] | tenant_id có, nhưng kênh gắn tenant 1, MCP toàn cục |
| R11 | Một phần [MÃ] | chỉ MCP server ngoài + skills; tool/hook phải sửa lõi |
| R12 | Một phần [MÃ]/[DOC] | docs tiếng Anh nhiều, ảnh thật; nhưng số liệu mâu thuẫn, rất phức tạp |

**Pháp lý (MIT)** [MÃ]: công ty tự host nội bộ được dùng, sửa, bán lại, không phải công bố mã; chỉ cần giữ thông báo bản quyền + giấy phép trong bản sao — [LICENSE](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/LICENSE)

**R5 có làm được mà không fork?** Không. Điểm phải vá tối thiểu (fork): (1) `server/channels/kernel.ts` `dispatchInbound(turn: InboundTurn, opts: DispatchOptions)` (dòng ~150–190) truyền `turn.fromIdentifier` xuống; (2) `server/chat-engine.ts:97` thêm trường `sender` vào `ChatEngineOptions` và chèn vào system prompt; (3) `server/telegram.ts:176 handleTextMessage(ctx)` và `server/discord.ts:93` truyền `ctx.from.id`; (4) mở `ChannelName` ở `kernel.ts:71`. Hook `registerHook(hook: HookHandler)` (`server/hooks.ts:49`) chỉ nhận sự kiện fire-and-forget (`emitHookEvent` gọi qua `import().then` ở `chat-engine.ts:2475`), không sửa được ngữ cảnh lượt chat; MCP tool ngoài không biết người đang nói.

### Inferences
- VisionClaw bị loại vì "1 người bảo trì + 320k dòng" là lý do đúng về rủi ro, nhưng lý do quyết định nên là R5: nền tảng được thiết kế như "một chủ doanh nghiệp + đội agent", không có khái niệm nhiều nhân viên người với vai trò khác nhau.
- Heuristic clarify dùng regex tiếng Anh → với yêu cầu tiếng Việt kiểu "làm chiến dịch Tết đi", Stage 1 có thể không kích hoạt (chỉ bắt được nếu <4 từ) — suy luận từ mã, chưa chạy thử.
- Nhiều model ID cứng (`gpt-5.6-sol` cho planner/judge, `gemini-2.5-flash` cho evaluator) → "chạy chỉ với 1 key" có thể rơi về fallback; rủi ro chi phí/tương thích [?].

### Gaps
- Chưa chạy thử; chưa kiểm hành vi fallback khi chỉ có 1 key Anthropic.
- Lịch sử commit thật bị squash trong public mirror → không đo được commit/tháng.
- Chưa đọc hết `server/routes/*` để xác nhận mọi route đều kiểm tenant.

---

## Câu 2 — FleetQ (escapeboy/agent-fleet-o): AGPL có cản dùng nội bộ không? multi-tenant, team phân cấp, inbox duyệt có SLA, 8 kênh, ví credit tự dừng, identity, tách việc, plugin, release

### Takeaway
FleetQ là dự án có kiến trúc mở rộng tốt nhất trong 5 (hệ plugin Laravel thật: connector vào/ra, AI middleware, MCP tools, panel, workflow node), R1/R2/R4/R10/R11 đạt. AGPL-3.0 **cho phép** công ty self-host nội bộ, kể cả sửa. Điểm yếu: R5 — Telegram bỏ ID người gửi, mọi chat Telegram chạy **với quyền chủ team (owner)**; không có hồ sơ người đa kênh/chức danh/phòng ban; release cuối v1.27.0 ngày 2026-06-09 (trước mốc 2026-06-27) và commit giảm dần. **Kết luận: khôi phục làm ứng viên (hạng "nền để xây R5 bằng plugin")**, kèm điều kiện: tự viết lớp identity + adapter Zalo dạng plugin, và kiểm lại nhịp phát hành.

### Cited Findings

**Repo & sức sống** [MÃ]
- Repo: https://github.com/escapeboy/agent-fleet-o ; 70 sao, 11 fork, 2.293 commit, 3 issue mở (2026-09-27) — [GitHub repo page](https://github.com/escapeboy/agent-fleet-o)
- Tag/release mới nhất: `v1.27.0` ngày 2026-06-09, `v1.26.0` 2026-05-18, `v1.25.0` 2026-05-07 — [Releases](https://github.com/escapeboy/agent-fleet-o/releases); CHANGELOG `## [1.27.0] - 2026-06-09` — [CHANGELOG.md](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/CHANGELOG.md)
- Commit/tháng (git): 2026-03: 805, 04: 406, 05: 450, 06: 181, 07: 67, 08: 40, 09: 32; commit cuối 2026-09-21. 2.286/2.293 commit của Nikola Katsarov → gần như 1 người.
- Stack: `laravel/framework ^13.0`, `prism-php/prism ^0.100.0`, PHP 8.4; ~380k dòng PHP (không tính tests/database) — [composer.json](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/composer.json)

**R1** [MÃ]: gateway `PrismAiGateway` (gọi API trực tiếp, BYOK), `LocalAgentGateway`/`LocalBridgeGateway` là tuỳ chọn cho Claude Code/Codex — [app/Infrastructure/AI/Gateways](https://github.com/escapeboy/agent-fleet-o/tree/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Infrastructure/AI/Gateways)

**R2/R3 — crew & tách việc** [MÃ]
- `CrewProcessType`: sequential, parallel, **hierarchical** ("Coordinator dynamically decides what to do next"), self_claim, adversarial, fanout, chat_room; vai trò thành viên: coordinator, qa, worker, process_reviewer, output_reviewer, judge — [app/Domain/Crew/Enums/CrewProcessType.php](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Crew/Enums/CrewProcessType.php), [CrewMemberRole.php](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Crew/Enums/CrewMemberRole.php)
- `DecomposeGoalAction`: coordinator LLM trả JSON `title, description, assigned_to, dependencies (0-based), expected_output` (+ `skip_condition`); giới hạn `max_delegation_depth` 5; có `CyclicDependencyException` — [DecomposeGoalAction.php#L94](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Crew/Actions/DecomposeGoalAction.php#L94)
- Clarify: middleware `DetectClarificationNeeded` chấm `ambiguity_score`, sinh câu hỏi + form cho người trả lời, nhưng **opt-in từng agent** (`clarification_detection_enabled`, mặc định tắt, ngưỡng 0.75) — [DetectClarificationNeeded.php#L19](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Agent/Pipeline/Middleware/DetectClarificationNeeded.php#L19)

**R4 — duyệt/SLA/làm lại** [MÃ]
- QA agent chấm output → `Validated` hoặc `NeedsRevision` — [ValidateTaskOutputAction.php#L81](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Crew/Actions/ValidateTaskOutputAction.php#L81)
- `ApprovalRequest` có `sla_deadline`, `escalation_chain`, `escalation_level`; `sla_deadline->isPast()` — [ApprovalRequest.php#L188](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Approval/Models/ApprovalRequest.php#L188); migration `2026_02_15_200002_enhance_approval_requests_and_dag_columns.php` thêm index SLA — [database/migrations](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/database/migrations/2026_02_15_200002_enhance_approval_requests_and_dag_columns.php)
- Action proposals + `PolicyEvaluator`, `EscalateHumanTaskAction`, `ExpireStaleApprovalsAction` — [app/Domain/Approval](https://github.com/escapeboy/agent-fleet-o/tree/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Approval)

**"Ví credit tự dừng"** [MÃ]
- `CheckBudgetAction`: cap theo experiment (`budget_cap_credits`) → hết thì `PauseOnBudgetExceeded` tự pause experiment; nhưng kiểm số dư team **bị bỏ qua nếu team chưa từng mua credit** ("Community/self-hosted installs never have purchase entries, so we skip this check") — [CheckBudgetAction.php#L38](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Budget/Actions/CheckBudgetAction.php#L38), [ReserveBudgetAction.php#L30](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Budget/Actions/ReserveBudgetAction.php#L30), [PauseOnBudgetExceeded.php](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Budget/Listeners/PauseOnBudgetExceeded.php)

**R5 — identity** [MÃ]
- Webhook Telegram chỉ lấy `chat.id`, `text`, `username` rồi dispatch job — **bỏ `from.id`** (không phân biệt người trong nhóm) — [TelegramWebhookController.php#L48](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Http/Controllers/TelegramWebhookController.php#L48)
- `TelegramChatBinding` tạo với `user_id => null`; user xử lý = `$binding->user ?? resolveTeamUser()` = **owner của team**; không có mã nào gán `user_id` cho binding; không có allowlist người gửi (chỉ kiểm secret header của webhook) — [ProcessTelegramMessageAction.php#L57](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Telegram/Actions/ProcessTelegramMessageAction.php#L57), [#L170](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Telegram/Actions/ProcessTelegramMessageAction.php#L170)
- Vai trò người: `TeamRole` owner/admin/member/viewer (pivot team_user) — [app/Domain/Shared/Enums/TeamRole.php](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Shared/Enums/TeamRole.php); không có chức danh/phòng ban cho người.
- Crew execution: `resolveUserId()` = user của experiment hoặc **owner team**, dùng cho metering/AiRequestDTO `userId`, không đưa vào prompt — [CrewExecution.php#L116](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Crew/Models/CrewExecution.php#L116)

**R6 — kênh** [MÃ]/[DOC]
- "8 kênh" = **8 kênh chat OUTBOUND**: Telegram, Slack, Discord, Microsoft Teams, Google Chat, Matrix, Signal, Supabase Realtime (+ Email SMTP, Webhook, ntfy) — [README.md#L207](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/README.md#L207); thư mục connector ra có thêm WhatsApp — [app/Domain/Outbound/Connectors](https://github.com/escapeboy/agent-fleet-o/tree/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Outbound/Connectors)
- Hội thoại 2 chiều: assistant Telegram; chatbot `ChannelType` = web_widget, api, telegram, slack, webhook, ticket_system — [ChannelType.php](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Chatbot/Enums/ChannelType.php); 36 "signal connector" vào (WhatsApp webhook, Discord webhook, Matrix, Signal, IMAP, RSS…) — [app/Domain/Signal/Connectors](https://github.com/escapeboy/agent-fleet-o/tree/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Signal/Connectors). Không có Zalo (grep "zalo" = 0).

**R10/R11** [MÃ]
- Multi-tenant: `TeamScope` global scope + trait `BelongsToTeam` dùng ở 148 file — [app/Domain/Shared/Scopes/TeamScope.php](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Shared/Scopes/TeamScope.php). Không có team lồng nhau (Team fillable chỉ name, slug…) — "team phân cấp" thực chất là crew `hierarchical` + delegation lồng nhau.
- Plugin: `abstract class FleetPluginServiceProvider` với mảng khai báo `$listen`, `$mcpTools`, `$livewire`, `$signals` (InputConnectorInterface), `$outbound` (OutboundConnectorInterface), `$commands`, `$aiMiddleware` (AiMiddlewareInterface), `$integrations`, `$panels`, `$workflowNodes`, `$socialiteProviders`; auto-discovery qua `composer.json extra.laravel.providers` + `extra.fleet.plugin` — [FleetPluginServiceProvider.php#L52](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Providers/FleetPluginServiceProvider.php#L52)
- `AiMiddlewareInterface::handle(AiRequestDTO $request, Closure $next): AiResponseDTO` — chạy quanh mọi lời gọi LLM; `AiRequestDTO` có `systemPrompt`, `userId`, `teamId`, `agentId`, `purpose` — [AiMiddlewareInterface.php](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Infrastructure/AI/Contracts/AiMiddlewareInterface.php), [AiRequestDTO.php#L13](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Infrastructure/AI/DTOs/AiRequestDTO.php#L13)
- R9: `crew-org-chart.blade.php` vẽ 2 tầng coordinator → QA + workers, kéo-thả để **sắp thứ tự** worker (Alpine `draggedId`, `ReorderCrewMembersAction`); không phải sơ đồ tổ chức nhiều tầng — [crew-org-chart.blade.php#L95](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/resources/views/components/crew-org-chart.blade.php#L95)

**Ảnh thật**: thư mục `screenshots/` (29 ảnh: `qa-dashboard.png`, `agents.png`, `qa-workflows.png`, `assistant-sidebar.png`…); một số ảnh cũ (tiêu đề "Agent Fleet v1.0"). Đã lưu: `screenshots/fleetq-qa-dashboard.png` (sidebar tối: Projects, Experiments, Agents, Crews, Workflows, Skills, Tools, Credentials, Memory, Marketplace, Approvals…; thẻ Active Runs, Success Rate 21.9%, Pending Approvals), `screenshots/fleetq-agents.png` — [screenshots/](https://github.com/escapeboy/agent-fleet-o/tree/e2abe66c17e2efdeaf4615606a3e75e14f8796df/screenshots)

**Bảng kiểm claim**
| Claim | Kết quả | Bằng chứng |
|---|---|---|
| AGPL-3.0 | Đúng [MÃ] | LICENSE |
| Laravel | Đúng [MÃ] | composer.json laravel ^13 |
| Multi-tenant | Đúng [MÃ] | TeamScope, 148 model |
| Team phân cấp | Sai một phần [MÃ] | chỉ crew `hierarchical` + delegation ≤5 tầng; không có team/phòng ban lồng nhau |
| Inbox duyệt có SLA | Đúng [MÃ] | sla_deadline, escalation_chain |
| 8 kênh | Đúng nhưng là 8 kênh chat **outbound** [MÃ]/[DOC] | README#L207 |
| Ví credit tự dừng | Một phần / sai với self-host [MÃ] | kiểm số dư bị bỏ qua nếu chưa mua credit; cap theo experiment thì có pause |

**Chấm 12 tiêu chí**
| # | Điểm | Bằng chứng |
|---|---|---|
| R1 | Đạt [MÃ] | PrismAiGateway BYOK |
| R2 | Đạt [MÃ] | agent role/goal/backstory, crew 7 kiểu, QA/judge |
| R3 | Một phần [MÃ] | decompose có dependencies + expected_output; clarify chỉ opt-in từng agent |
| R4 | Đạt [MÃ] | QA NeedsRevision, approval SLA+escalation, policy proposals |
| R5a | Không [MÃ] | Telegram bỏ from.id, gán owner |
| R5b | Không [MÃ] | không liên kết đa kênh |
| R5c | Một phần [MÃ] | web user có TeamRole; không chức danh/phòng ban |
| R5d | Một phần [MÃ] | userId (experiment/owner) đi theo AiRequestDTO, không vào prompt |
| R6 | Một phần→gần Đạt [MÃ] | nhiều connector, mở rộng bằng plugin; hội thoại 2 chiều chủ yếu Telegram/web/Slack; không Zalo |
| R7 | Đạt (có nghĩa vụ AGPL) [MÃ] | xem pháp lý |
| R8 | Một phần [MÃ] | tag cuối 2026-06-09 (< 2026-06-27) nhưng vẫn commit tới 2026-09-21 |
| R9 | Một phần [MÃ] | org chart crew 2 tầng, kéo-thả chỉ đổi thứ tự; DAG workflow builder riêng |
| R10 | Đạt [MÃ] | TeamScope |
| R11 | Đạt [MÃ] | FleetPluginServiceProvider |
| R12 | Đạt [DOC] | docs tiếng Anh, ảnh thật (một phần cũ) |

**Pháp lý AGPL-3.0 khi công ty tự host nội bộ** [MÃ – trích văn bản giấy phép trong repo]
- Chạy nguyên bản, không sửa: không phát sinh nghĩa vụ công bố mã. Văn bản GPL/AGPL: "You may make, run and propagate covered works that you do not convey, without conditions"; "Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying" — [LICENSE (FleetQ)](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/LICENSE)
- **Điều 13 (network-use)**: "if you modify the Program, your modified version must prominently offer all users interacting with it remotely through a computer network … an opportunity to receive the Corresponding Source of your version" — [LICENSE#L186-L188](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/LICENSE)
- README của dự án: "You can self-host, modify, and run FleetQ for free — including commercial use. If you offer FleetQ as a hosted service to others, you must open-source your modifications" — [README.md#L830](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/README.md#L830)
- Thực tế cho công ty VN: (1) dùng nội bộ, kể cả mục đích thương mại (chạy phòng Marketing) = được phép; (2) nếu **sửa** FleetQ và nhân viên dùng qua web → phải cho *những người dùng đó* nhận mã nguồn bản đã sửa (nội bộ nên chi phí gần 0); (3) nếu bản đã sửa **tương tác với khách hàng bên ngoài** (chatbot web widget, bot Telegram/Zalo trả lời khách) → khách là "users interacting with it remotely" → phải cung cấp mã nguồn phần sửa cho họ (vd link tải) — đây là điểm cần luật sư xác nhận; (4) plugin viết riêng: nếu là "work based on" FleetQ (liên kết chặt vào lớp PHP) thì có khả năng bị coi là phái sinh và chịu AGPL [?]; (5) bí mật/API key không thuộc "Corresponding Source".

**R5 có làm được mà không fork?** Phần lớn **có**, qua plugin:
- Thêm bảng identity (người ↔ Telegram/Zalo/web, chức danh, phòng ban, quyền) bằng migration của plugin; `bootAddon()` (`FleetPluginServiceProvider.php:188`) là nơi gọi `loadMigrationsFrom()`/`loadRoutesFrom()` chuẩn Laravel (suy luận: class kế thừa `Illuminate\Support\ServiceProvider`).
- Adapter Zalo: route/controller webhook riêng trong plugin + `OutboundConnectorInterface::send(OutboundProposal $proposal): OutboundAction` / `supports(string $channel): bool` (khai báo trong `$outbound`), gọi `SendAssistantMessageAction::executeStreaming(AssistantConversation $conversation, string $userMessage, User $user, ?string $contextType, ?string $contextId, ?callable $onChunk, …)` với **User đã resolve** — [SendAssistantMessageAction.php#L598](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Assistant/Actions/SendAssistantMessageAction.php#L598)
- Chèn "ai đang nói / chức danh / quyền" vào mọi lời gọi LLM: `$aiMiddleware` → `AiMiddlewareInterface::handle(AiRequestDTO $request, Closure $next)` sửa `systemPrompt` dựa trên `userId/teamId/purpose`.
- Telegram có sẵn: không vá được sạch vì controller đã bỏ `from.id` (`TelegramWebhookController.php:48-53`); cách không-fork: tắt bot tích hợp, tự viết webhook Telegram trong plugin (hoặc rebind `ProcessTelegramMessageAction` qua container — job resolve action bằng DI tại `ProcessTelegramMessageJob.php:30`, nhưng vẫn thiếu `from.id` trong nhóm).

### Inferences
- Lý do loại cũ (nếu vì AGPL) là sai: AGPL không cấm dùng nội bộ thương mại; nghĩa vụ chỉ phát sinh khi sửa và cho người khác dùng qua mạng.
- Lỗ hổng "mọi người nhắn bot Telegram đều thành owner" là rủi ro bảo mật thật nếu bật bot Telegram cho nhóm/khách [MÃ, chưa chạy thử].
- Nhịp commit giảm (805 → 32/tháng) + 1 tác giả → rủi ro bảo trì trung bình–cao.

### Gaps
- Chưa chạy thử; chưa kiểm plugin có thể đăng ký route/migration thực tế (không có plugin mẫu trong repo được đọc).
- Chưa xác nhận luật sư về phạm vi "users" của AGPL §13 với khách qua chatbot/Telegram.
- gnu.org, choosealicense.com bị proxy chặn → chỉ trích nguyên văn LICENSE trong repo.

---

## Câu 3 — Agentic Organization (fab-agent): Commons Clause + MIT nghĩa là gì cho dùng nội bộ? đa công ty, phòng ban lồng nhau, sơ đồ cây, duyệt 2 cấp, identity, kênh, release

### Takeaway
Phát hiện quan trọng: **file LICENSE hiện là MIT thuần** (đổi từ "MIT + Commons Clause" về MIT ngày 2026-07-18, commit `3be141e`), nhưng README vẫn ghi "Commons Clause + MIT" → mâu thuẫn. Dù theo cách đọc nào, dùng nội bộ công ty đều được phép. Mô hình dữ liệu tổ chức tốt nhất trong 5 dự án (Personnel người/agent có title, role, department, manager; CompanyMember founder/executive/dept_head/agent_owner/user; phòng ban lồng nhau điều khiển định tuyến; duyệt 2 cấp). Nhưng: agent **không được biết ai đang chat** (web bỏ `current_user`, Telegram tự gán "công ty đầu tiên"), cách ly tenant yếu, không có release/tag, 3 sao, mã phần lớn do agent AI commit. **Kết luận: vẫn loại làm nền tảng chính; ghi nhận làm "mẫu mô hình dữ liệu identity/tổ chức" để tham khảo.**

### Cited Findings
- Repo: https://github.com/fab-agent/agentic-organization (tổ chức Fabrika Yazılım, Istanbul); 3 sao, 0 fork, 177 commit, không có release/tag (2026-09-27) — [GitHub repo page](https://github.com/fab-agent/agentic-organization), [org page](https://github.com/fab-agent)
- Commit/tháng (git): 2026-05: 8, 06: 7, 07: 111, 08: 0, 09: 51; commit cuối 2026-09-09. Tác giả: "3rdParty Agent" 116 commit, Kuntay Kunt (3 email) 61 [MÃ]. Nhiều commit "Co-Authored-By: Claude Sonnet 4.6".
- Lịch sử LICENSE [MÃ]: `c1bcc35` 2026-06-08 thêm MIT → `7686820` 2026-07-15 "replace MIT with MIT + Commons Clause" → `3be141e` 2026-07-18 "LICENSE: replace MIT + Commons Clause with pure MIT (OSI-compliant, required for hackathon submission)" — [commit 3be141e](https://github.com/fab-agent/agentic-organization/commit/3be141ed7d08b96034997966f44edc3b3ea94ac8), [commit 7686820](https://github.com/fab-agent/agentic-organization/commit/768682010cc1eaa42ecd939d840dc59c926f66aa); LICENSE hiện tại = MIT — [LICENSE](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/LICENSE); README vẫn ghi "**Commons Clause + MIT** — Free to use, fork, and self-host for your own organization. Selling, white-labeling, or offering this software as a hosted or managed service to third parties requires a commercial license." — [README.md#L397](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/README.md#L397)
- Văn bản Commons Clause (bản 2026-07-15): không cấp quyền "Sell" = "provide to third parties, for a fee or other consideration (including … fees for hosting, white-labeling, reselling, or consulting/support services related to the Software), a product or service whose value derives, entirely or substantially, from the functionality of the Software"; commit message: "Self-use and internal company use remain free" — [commit 7686820](https://github.com/fab-agent/agentic-organization/commit/768682010cc1eaa42ecd939d840dc59c926f66aa); định nghĩa chuẩn cùng nội dung — [fossas/commons-clause](https://github.com/fossas/commons-clause)
- Stack [MÃ]: FastAPI + SQLModel + Alembic, Svelte frontend; ~25,7k dòng Python, ~18k dòng Svelte/TS — [backend/requirements.txt](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/requirements.txt)
- R1 [MÃ]: gọi trực tiếp `genai.Client` (Gemini), `anthropic.Anthropic(...).messages.create`, `client.chat.completions.create` (OpenAI-compatible, Qwen/DashScope) — [agent_runtime.py#L679](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/services/agent_runtime.py#L679), [#L1017](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/services/agent_runtime.py#L1017); UI ẩn Anthropic/Google (`HIDDEN_CLOUD_PROVIDERS`, backend vẫn giữ) từ commit `d06c045` 2026-07-20 — [settings/+page.svelte#L57](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/frontend/src/routes/settings/+page.svelte#L57). "Workstation" sandbox chạy opencode (agent CLI) là nhánh riêng "agentic-os", không phải đường thực thi chính — [sandbox/README.md](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/sandbox/README.md)
- Mô hình tổ chức [MÃ]: `Department.parent_id` (lồng nhau), `Personnel{title, role, type human|agent, department_id, manager_id, user_id}`, `User`, `CompanyMember{role founder|executive|dept_head|agent_owner|user, scope_id}` — [models.py#L19](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/models.py#L19), [models.py#L37](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/models.py#L37), [models.py#L181](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/models.py#L181)
- Duyệt 2 cấp [MÃ]: `ChangeRequest` (sửa cấu hình/skill/policy agent) draft → submitted → dept_head_approved → admin_approved → committed (commit lên GitHub) — [models.py#L198](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/models.py#L198); `A2ARequest` ủy quyền agent→agent "with two-stage human approval" (duyệt giao việc + duyệt kết quả, người duyệt = người phụ trách agent nhận) — [models.py#L237](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/models.py#L237); policy engine chặn deny/ask ở chế độ enforce — [agent_runtime.py#L334](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/services/agent_runtime.py#L334)
- Cây phòng ban **điều khiển định tuyến** [MÃ]: `_route_agent()` tìm agent active trong phòng ban được yêu cầu → đi ngược `parent_id` → toàn công ty, lọc theo skill — [task_requests.py#L96](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/task_requests.py#L96). Trang org-chart chỉ xem (zoom, chuyển chế độ personnel/department), **không kéo-thả** — [org-chart/+page.svelte](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/frontend/src/routes/org-chart/+page.svelte)
- Tách việc [MÃ]: không có clarify/acceptance criteria; agent "orchestrator" chỉ được prompt "you MUST call your delegation tools to assign sub-tasks" — [agent_runtime.py#L102](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/services/agent_runtime.py#L102)
- Identity khi chạy [MÃ]: `build_system_prompt(person, dept, …)` chỉ mô tả **agent** (tên, title, role, phòng ban, policy), không có người yêu cầu — [agent_runtime.py#L63](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/services/agent_runtime.py#L63); API sessions nhận `_: User = Depends(get_current_user)` rồi bỏ đi, `AgentSession` không có user_id — [sessions.py#L85](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/sessions.py#L85), [models.py#L135](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/models.py#L135)
- Telegram [MÃ]: `_get_or_create_state(chat_id)` "Auto-link to first company" (`select(CompanyMember).first()`), `TelegramBotState.user_id` không bao giờ được gán; callback nút bấm cho phép duyệt/từ chối task & A2A mà không kiểm người bấm — [telegram_bot.py#L127](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/telegram_bot.py#L127), [telegram_bot.py#L280](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/telegram_bot.py#L280); chuỗi bot tiếng Thổ Nhĩ Kỳ ("Görev onaylandı…").
- Đa công ty [MÃ]: có `Company`, `company_id`; nhưng `require_manager` chỉ kiểm "dept_head ở **bất kỳ** công ty nào"; `check_company_membership` chỉ dùng trong 4 file API (auth, personnel, companies, departments) trên 31 router; `create_task_request` không kiểm thành viên của `body.company_id` — [auth.py#L66](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/auth.py#L66), [task_requests.py#L179](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/task_requests.py#L179)
- Kênh [DOC]/[MÃ]: Telegram (1 bot), Instagram Business + WhatsApp Cloud API dưới dạng skill của agent; UI i18n TR/EN — [README.md#L38](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/README.md#L38)
- Ảnh UI: không có ảnh chụp màn hình trong repo (không file png/jpg) [MÃ].

**Bảng kiểm claim**
| Claim | Kết quả | Bằng chứng |
|---|---|---|
| Commons Clause + MIT | Đã thay đổi [MÃ] | LICENSE = MIT thuần từ 2026-07-18; README chưa cập nhật |
| Đa công ty | Đúng, nhưng cách ly yếu [MÃ] | Company/CompanyMember; thiếu kiểm membership ở nhiều router |
| Phòng ban lồng nhau | Đúng [MÃ] | Department.parent_id |
| Sơ đồ cây | Đúng (chỉ xem, không kéo-thả) [MÃ] | org-chart page |
| Duyệt 2 cấp | Đúng [MÃ] | ChangeRequest, A2ARequest |

**Chấm 12 tiêu chí**
| # | Điểm | Bằng chứng |
|---|---|---|
| R1 | Đạt [MÃ] | SDK anthropic/openai/genai trực tiếp |
| R2 | Đạt [MÃ] | agent là Personnel trong phòng ban, A2A delegation |
| R3 | Không [MÃ] | chỉ định tuyến theo phòng ban/skill + prompt delegate; không clarify/acceptance |
| R4 | Một phần [MÃ] | human gate mạnh (task, A2A 2 bước, CR 2 cấp), không có critic/rework AI |
| R5a | Không [MÃ] | web bỏ current_user; Telegram không biết người |
| R5b | Không [MÃ] | không liên kết |
| R5c | Một phần [MÃ] | dữ liệu có (title/department/role/manager) nhưng không đưa vào agent |
| R5d | Một phần [MÃ] | A2ARequest có from_agent_id; TaskRequest lưu requester_user_id, không vào prompt |
| R6 | Một phần [MÃ] | Telegram + IG/WA skill; không có khung adapter |
| R7 | Đạt [MÃ] | MIT (README ghi CC — xem pháp lý) |
| R8 | Không [MÃ] | không tag/release (dù commit tới 2026-09-09) |
| R9 | Một phần [MÃ] | cây phòng ban điều khiển routing, nhưng không kéo-thả |
| R10 | Một phần [MÃ] | company_id có, kiểm membership thiếu |
| R11 | Một phần [MÃ] | skill kiểu http/mcp/function/database cấu hình trong DB; không có plugin code |
| R12 | Một phần [DOC] | README EN/TR, không ảnh; nhiều chuỗi TR cứng |

**Pháp lý** [MÃ]: Theo LICENSE hiện tại (MIT) → tự do hoàn toàn, chỉ giữ thông báo bản quyền. Nếu dùng bản cũ trong khoảng 2026-07-15 → 2026-07-18 (MIT + Commons Clause) → vẫn được dùng/sửa/tự host **nội bộ**; chỉ cấm "Sell" (bán/host thu phí cho bên thứ ba, white-label, dịch vụ tư vấn/hỗ trợ thu phí dựa trên phần mềm). Vì README và LICENSE mâu thuẫn, nên ghim commit sau `3be141e` và lưu bản LICENSE MIT làm bằng chứng; nếu định bán dịch vụ dựa trên nó, hỏi tác giả (bilgi@kuntaykunt.com) cho chắc.

**R5 có làm được mà không fork?** Không có cơ chế plugin (router đăng ký cứng trong `backend/main.py`, 31 `include_router`). Phải fork, nhưng vá nhỏ vì mô hình dữ liệu đã có: `backend/api/sessions.py:85/304` (giữ `current_user` thay vì `_`), thêm `user_id` cho `AgentSession` (`models.py:135`), thêm tham số người yêu cầu cho `run_session(session_id, user_message, attachments)` (`agent_runtime.py:1087`) và `build_system_prompt(person, dept, skills, …)` (`agent_runtime.py:63`); Telegram: `_get_or_create_state(chat_id)` (`telegram_bot.py:127`) map `from.id` → `TelegramBotState.user_id` → `Personnel`.

### Inferences
- Lý do loại "Commons Clause → không phải open source thuần" không còn đúng về mặt văn bản LICENSE, và kể cả khi đúng thì Commons Clause không cấm dùng nội bộ.
- Lý do loại nên chuyển sang: cách ly tenant/ủy quyền yếu (duyệt qua Telegram không kiểm người), identity runtime không có, dự án nhỏ (3 sao), không release.

### Gaps
- Không truy cập được commonsclause.com (proxy chặn) để trích FAQ nguyên văn.
- Chưa chạy thử để xác nhận lỗ hổng cross-company/Telegram trên runtime.

---

## Câu 4 — Foundry (axislab-top): GPL-3.0, sơ đồ tổ chức kéo-thả có điều khiển định tuyến không, số commit, release, backend

### Takeaway
Foundry có backend riêng (NestJS + LangChain, pool key LLM), multi-tenant bằng PostgreSQL RLS thật, CEO v2 chia việc theo phòng ban với acceptance criteria và bước xác nhận trước khi phát lệnh. Nhưng **README nói "drag-and-drop org chart" — mã không có kéo-thả** (bố cục thẻ phòng ban + nút), không có kênh chat nào, UI cứng tiếng Trung, **ngừng commit từ 2026-06-30** và release duy nhất v1.0.0 ngày 2026-06-24 (trước mốc). **Kết luận: vẫn loại** (lý do đổi: không phải "13 commit" mà là đứng im 3 tháng + không kênh + UI tiếng Trung).

### Cited Findings
- Repo: https://github.com/axislab-top/Foundry ; 442 sao, 8 fork, 84 commit (2026-09-27) — [GitHub repo page](https://github.com/axislab-top/Foundry)
- Release duy nhất `v1.0.0` ngày 2026-06-24 (git: `2026-06-24 14:47:26 +0800`) — [Releases](https://github.com/axislab-top/Foundry/releases)
- Commit theo ngày (git): 2026-03-27: 3, 2026-04-05: 4, 2026-04-12: 2, 2026-06-21→06-30: 75; **0 commit trong 2026-07, 08, 09**; commit cuối `2daebc4` 2026-06-30 ("fix: 修复 RMQ_URL…"). Tác giả: wantsmoney 75, Okxinx 9 [MÃ].
- GPL-3.0 [MÃ] — [LICENSE](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/LICENSE)
- Backend [MÃ]: monorepo turbo (apps/api, gateway, worker, runner, temporal-worker, webhooks), ~339k dòng TS; `CeoChatModelFactory` dùng `ChatAnthropic`/`ChatOpenAI` của LangChain với key/model do billing router chọn — [ceo-chat-model.factory.ts](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/apps/worker/src/modules/autonomous/ceo-chat-model.factory.ts)
- README: "Drag-and-drop custom organization structure" và bảng so sánh "✅ Drag-and-drop" — [README.md#L243](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/README.md#L243), [README.md#L500](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/README.md#L500)
- Mã thực tế [MÃ]: `OrgBoard.tsx` là bố cục thẻ phòng ban với nút `onAddDepartment`, `onAppointDirector`, `onHireEmployee`; grep `drag|onDrop|draggable` trong `client/src` và `admin/src` chỉ khớp `TaskKanbanBoard.tsx` (kéo task Kanban); `@xyflow/react` có trong `client/package.json` nhưng **không được import** trong `client/src` — [OrgBoard.tsx](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/client/src/features/organization/components/OrgBoard.tsx). → README-vs-code: SAI.
- Ảnh `screenshot-org.png` (đã lưu `screenshots/foundry-screenshot-org.png`): tiêu đề "组织架构", thẻ CEO trên cùng, lưới thẻ phòng ban (工程部, 设计部, 营销部, 付费媒体部, 销售部, 金融财务部, 人力资源部, 法务部, 供应链部, 产品部), mỗi thẻ có "部门主管" + "员工" + nút "添加" — không có nút/cạnh nối kiểu node graph — [.github/images/screenshot-org.png](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/.github/images/screenshot-org.png)
- Cấu trúc phòng ban **có** điều khiển định tuyến [MÃ]: bridge phân phối tạo `departmentTasks` với `departmentSlug`, `directorAgentId`, `dependsOnDepartmentSlugs`, song song tối đa 4 phòng ban, và `pendingDepartmentDispatchConfirm: true` (chờ xác nhận trước khi phát) — [main-room-orchestration-distribution.bridge.ts#L45](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/apps/worker/src/modules/collaboration/pipeline-v2/main-room-orchestration-distribution.bridge.ts#L45), [#L100](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/apps/worker/src/modules/collaboration/pipeline-v2/main-room-orchestration-distribution.bridge.ts#L100)
- Acceptance criteria [MÃ]: `acceptanceCriteria` trong CEO v2 supervision và gói task của employee — [ceo-v2-supervision.service.ts#L771](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/apps/worker/src/modules/collaboration/ceo/v2/ceo-v2-supervision.service.ts#L771)
- Duyệt/giám sát [MÃ, đọc nông]: module approval (approval flow, board decision, Temporal bridge, policy version) và `supervisor-review.service.ts` gọi LLM — [apps/api/src/modules/approval](https://github.com/axislab-top/Foundry/tree/2daebc43f3ebd012bd875e2da058df79efb36fb1/apps/api/src/modules/approval)
- Multi-tenant [MÃ]: 45 lệnh `ENABLE ROW LEVEL SECURITY` trong baseline schema, policy `company_id = current_setting('app.current_tenant')`, `SELECT set_config('app.current_tenant', $1, true)` — [tenant.constants.ts#L16](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/infrastructure/tenant/src/constants/tenant.constants.ts#L16), [baseline-schema.sql](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/infrastructure/postgres/migrations/baseline-schema.sql)
- Identity [MÃ]: `company_memberships(company_id, user_id, role DEFAULT 'member')`, role owner/admin/superadmin trong mã; không có chức danh/phòng ban cho người; không có kênh chat (grep telegram/feishu/dingtalk/wecom/slack/discord/whatsapp/zalo trong `apps`, `packages` = 0 file) — [baseline-schema.sql#L1608](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/infrastructure/postgres/migrations/baseline-schema.sql#L1608)
- Ngôn ngữ: README EN + zh-CN; commit message, chú thích mã và chuỗi UI (vd `开始搭建你的 AI 组织`) bằng tiếng Trung [MÃ].
- Ảnh thật: `.github/images/screenshot-register.png`, `screenshot-org.png`, `screenshot-chat.png`, `screenshot-dashboard.png`; đã lưu `foundry-screenshot-org.png`, `foundry-screenshot-chat.png`.

**Bảng kiểm claim**
| Claim | Kết quả | Bằng chứng |
|---|---|---|
| GPL-3.0 | Đúng [MÃ] | LICENSE |
| Org chart kéo-thả | Sai [MÃ] | OrgBoard không có drag; xyflow không dùng; README sai |
| Chỉ 13 commit | Đã thay đổi [MÃ] | 84 commit, nhưng dừng từ 2026-06-30 |

**Chấm 12 tiêu chí**
| # | Điểm | Bằng chứng |
|---|---|---|
| R1 | Đạt [MÃ] | LangChain ChatOpenAI/ChatAnthropic + key pool |
| R2 | Đạt [MÃ] | CEO → giám đốc phòng ban → nhân viên agent |
| R3 | Một phần [MÃ] | chia task theo phòng ban + dependsOn + acceptanceCriteria; clarify chưa kiểm sâu [?] |
| R4 | Một phần [MÃ] | approval flow, supervisor review, xác nhận trước dispatch; chưa kiểm vòng rework [?] |
| R5a | Một phần [MÃ] | chỉ web user (chủ công ty) |
| R5b | Không [MÃ] | không có kênh |
| R5c | Không [MÃ] | membership role only |
| R5d | Chưa kiểm [?] | |
| R6 | Không [MÃ] | không có kênh chat |
| R7 | Đạt (có nghĩa vụ GPL) [MÃ] | |
| R8 | Không [MÃ] | v1.0.0 2026-06-24; 0 commit sau 2026-06-30 |
| R9 | Một phần [MÃ] | cấu trúc phòng ban/giám đốc điều khiển dispatch; không kéo-thả |
| R10 | Đạt [MÃ] | PG RLS |
| R11 | Một phần [DOC]/[MÃ] | skills + MCP tools; không plugin code |
| R12 | Một phần [MÃ] | ảnh thật, README EN; UI & mã tiếng Trung |

**Pháp lý GPL-3.0** [MÃ – LICENSE trong repo]: "You may make, run and propagate covered works that you do not convey, without conditions"; "Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying" — [LICENSE](https://github.com/axislab-top/Foundry/blob/2daebc43f3ebd012bd875e2da058df79efb36fb1/LICENSE). → Tự host nội bộ, kể cả sửa, **không** phải công bố mã (GPL không có điều khoản network như AGPL). Nghĩa vụ chỉ phát sinh khi **phân phối bản sao** (vd phát binary/Docker image cho công ty khác, bán bản cài đặt) → phải kèm mã nguồn GPL. Chuyển bản cài cho công ty con/đối tác là pháp nhân khác có thể bị coi là "convey" [?].

**R5 không fork?** Không: không có plugin code, không có kênh; phải fork để thêm adapter + identity (điểm vào: `apps/api/src/modules/collaboration/*` cho luồng tin nhắn, `company_memberships` cho hồ sơ). Chưa xác định file:line chính xác cho hook vì dự án đã dừng — không đáng đầu tư.

### Inferences
- Số sao cao (442) nhưng đứng im 3 tháng sau đợt commit dồn (75 commit trong 10 ngày cuối tháng 6/2026) → giống dự án "ra mắt rồi bỏ".

### Gaps
- Chưa đọc sâu vòng rework/approval runtime; chưa chạy thử.

---

## Câu 5 — MDH (MonSp): Apache; luồng CEO phân tích → thảo luận → bỏ phiếu → giao → làm → review; quality gate; multi-tenant; kênh chat; ngôn ngữ docs; release

### Takeaway
MDH còn sống (tag v0.5.5 ngày 2026-08-26; 699 commit trong 2026-08; commit cuối 2026-09-24), Apache-2.0, backend tự gọi API (DeepSeek/OpenAI/Anthropic/DashScope). Luồng CEO → phân loại độ phức tạp → (phức tạp) dự án → đội → họp/thảo luận/bỏ phiếu → coordinator thực thi → review là có thật, nhưng thiết kế cho **phát triển phần mềm** (workspace git worktree, gate lint/pytest). Không có khái niệm người dùng/hồ sơ (RBAC theo API key), **không có kênh chat**, multi-tenant sơ khai, 1 sao, 1 tác giả, docs chi tiết tiếng Trung. **Kết luận: vẫn loại.**

### Cited Findings
- Repo: https://github.com/MonSp/MDH ; 1 sao, 0 fork, 1.064 commit (2026-09-27) — [GitHub repo page](https://github.com/MonSp/MDH); thuộc "umbrella" MatrixDahuang cùng MDH-Game, agent-kernel C++ — [MonSp/MatrixDahuang](https://github.com/MonSp/MatrixDahuang)
- Tag: 44 tag, mới nhất `v0.5.5` 2026-08-26 (git `2026-08-26 11:34:40 +0800`), v0.3.2→v0.5.5 đều trong 2026-08-25/26 — [Tags](https://github.com/MonSp/MDH/tags)
- Commit/tháng (git): 2026-05: 37, 06: 83, 07: 169, 08: 699, 09: 76; commit cuối 2026-09-24; 1.061/1.064 commit của MonSp [MÃ].
- Apache-2.0 [MÃ] — [LICENSE](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/LICENSE)
- R1 [MÃ]: `llm_client.py` gọi httpx tới DeepSeek/OpenAI/Anthropic/DashScope (`PROVIDER_DEFAULTS`) — [llm_client.py#L27](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/llm_client.py#L27); `adapters/claude-code` là adapter A2A tuỳ chọn bọc Claude Code CLI — [adapters/claude-code/package.json](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/adapters/claude-code/package.json)
- README ghi "AI: AgentScope + DeepSeek API" — [README.en.md#L193](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/README.en.md#L193); nhưng `backend/requirements.txt` không có agentscope và không có `import agentscope` nào trong backend (chỉ nhắc trong comment `llm_guard.py`) → README-vs-code lệch [MÃ] — [backend/requirements.txt](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/requirements.txt)
- Luồng CEO [MÃ]: `process_message` → "CEO：收到任务…正在分析意图" → `complexity_classifier.classify` → nếu `simple` và confidence ≥ 0.7 thì `_execute_simple` (bỏ qua thảo luận/bỏ phiếu/review đầy đủ), ngược lại `_execute_complex`: tạo project → tạo task → hỏi xác nhận workspace → họp → coordinator — [ceo_agent.py#L204](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/ceo_agent.py#L204), [ceo_agent.py#L244](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/ceo_agent.py#L244); agenda có pha `VOTING` → ACCEPTED/REJECTED — [agenda.py#L12](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/agenda.py#L12); đồng thuận theo lập trường cuối của từng agent, coordinator không bỏ phiếu — [discussion_manager.py#L183](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/discussion_manager.py#L183)
- Acceptance criteria [MÃ]: `EarsValidator` kiểm câu tiêu chí nghiệm thu dạng EARS (WHEN/IF … SHALL, cấm từ mơ hồ); `SpecManager.generate_spec_tree(clarified_brief)` — nhận "bản brief đã làm rõ" làm đầu vào (không tìm thấy nơi sinh brief làm rõ trong backend) — [ears_validator.py](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/ears_validator.py), [spec_manager.py#L67](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/spec_manager.py#L67)
- Quality gate [MÃ]: `GateEngine` "确定性门禁引擎" kiểm lint/test (pytest, pylint), fail-open khi thiếu công cụ — [gate_engine.py](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/gate_engine.py); `ApprovalManager(default_timeout=300.0)` lưu trong bộ nhớ — [approval_manager.py#L48](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/approval_manager.py#L48)
- 10 phòng ban [MÃ]: `roles_config.yaml` có dept-software (12 vai), dept-ai-movie 6, dept-data 6, dept-content 5, dept-ppt 4, dept-design 3, dept-marketing 2, dept-sales 2, dept-finance 1, dept-product 1 — [roles_config.yaml](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/roles_config.yaml)
- Multi-tenant [MÃ]: `TenantManager` (SQLite `tenants.db`, mỗi tenant 1 API key), `TenantMiddleware` gán `request.state.tenant_id` từ Bearer key, NULL khi dùng BACKEND_TOKEN; `tenant_id` chỉ xuất hiện ở 10 file backend (projects, team, experience…) — [tenant_middleware.py](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/tenant_middleware.py), [tenant_manager.py](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/tenant_manager.py)
- Identity [MÃ]: RBAC chỉ là vai trò **API key** admin/agent/viewer — [rbac.py](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/rbac.py); `user_id` chỉ xuất hiện 1 lần trong backend không-test.
- Kênh [MÃ]: grep telegram/feishu/lark/dingtalk/wecom/slack/discord/whatsapp/zalo trong backend = 0 file; `webhook_manager.py` chỉ bắn sự kiện ra (task.completed, agent.promoted, rule.demoted, rule.evolved, health.alert) — [webhook_manager.py](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/webhook_manager.py)
- Docs: đã có `README.en.md` (tiếng Anh); `docs/user-guide.md` tiếng Trung; `docs/quickstart.md` song ngữ Trung/Anh — [README.en.md](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/README.en.md), [docs/user-guide.md](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/docs/user-guide.md)
- Ảnh: không có ảnh chụp màn hình trong repo; chỉ có trang demo HTML `office-scene-demo.html`, `agent-role-cards-demo.html` [MÃ].
- Mở rộng: `skill_packs/` (brand_voice, brand_strategy, content_writing, competitive_analysis…), `A2ARegistry.register(agent_id, card)`, router marketplace/mcp_config — [a2a_registry.py#L71](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/backend/a2a_registry.py#L71)

**Bảng kiểm claim**
| Claim | Kết quả | Bằng chứng |
|---|---|---|
| Apache | Đúng [MÃ] | LICENSE |
| 2 sao | Đã thay đổi → 1 sao (2026-09-27) | GitHub page |
| FastAPI + AgentScope | FastAPI đúng; AgentScope **sai theo mã** (không import) [MÃ] | requirements.txt |
| 10 phòng ban | Đúng [MÃ] | roles_config.yaml |
| CEO phân tích→thảo luận→bỏ phiếu→giao→làm→review | Đúng một phần [MÃ] | chỉ ở nhánh "complex"; nhánh simple bỏ qua |
| Quality gate | Đúng (gate lint/test cho code) [MÃ] | gate_engine.py |
| Multi-tenant | Một phần [MÃ] | tenant theo API key, 10 file |
| Chỉ webhook, không kênh chat | Đúng [MÃ] | grep = 0 |
| Docs tiếng Trung | Đã thay đổi một phần [MÃ] | có README.en.md; docs chi tiết vẫn Trung |

**Chấm 12 tiêu chí**
| # | Điểm | Bằng chứng |
|---|---|---|
| R1 | Đạt [MÃ] | httpx tới 4 provider |
| R2 | Đạt [MÃ] | vai trò theo 10 phòng ban, họp nhóm |
| R3 | Một phần [MÃ] | complexity classifier, spec tree + EARS; clarify chưa thấy sinh ra |
| R4 | Một phần [MÃ] | review pipeline, gate code, approval 300s in-memory |
| R5a–d | Không [MÃ] | không có mô hình người dùng |
| R6 | Không [MÃ] | không kênh chat |
| R7 | Đạt [MÃ] | Apache-2.0 |
| R8 | Đạt [MÃ] | v0.5.5 2026-08-26, commit tới 2026-09-24 |
| R9 | Không [MÃ] | 3D office; không org chart điều khiển routing (grep org chart trong `src/` = 0) |
| R10 | Một phần [MÃ] | API-key tenant |
| R11 | Một phần [MÃ] | skill packs, A2A registry, MCP |
| R12 | Một phần [MÃ] | README EN; docs chi tiết Trung; không ảnh |

**Pháp lý Apache-2.0** [MÃ]: dùng nội bộ, sửa, thương mại đều được; khi phân phối phải giữ LICENSE/NOTICE và ghi chú file đã sửa; có cấp quyền bằng sáng chế — [LICENSE](https://github.com/MonSp/MDH/blob/6e406dbbfb0263b8b58e93158c58b6a7ceb7b221/LICENSE)

**R5 không fork?** Không: không có mô hình người dùng; RBAC theo API key; không có kênh. A2A registry chỉ cho thêm agent ngoài, không đổi ngữ cảnh người gửi.

### Inferences
- MDH hướng tới "đội phần mềm ảo" (gate pytest/pylint, git worktree), phòng marketing chỉ 2 vai → lệch mục tiêu người dùng.
- 699 commit/tháng bởi 1 người + nhiều tag trong 2 ngày → khả năng cao là commit tự động bởi agent; rủi ro ổn định [?].

### Gaps
- Chưa đọc TS `orchestrator/` để xem có bước clarify ở tầng TS không.

---

## Câu 6 — Tổng hợp: khôi phục hay vẫn loại, và lý do cũ có sai không

### Takeaway
Chỉ **FleetQ** nên được khôi phục làm ứng viên (điều kiện: tự xây lớp identity + adapter Zalo bằng plugin, chấp nhận nghĩa vụ AGPL nếu sửa lõi). VisionClaw, Agentic Organization, Foundry, MDH vẫn loại — nhưng lý do loại phải sửa: AGPL/GPL/Commons Clause không cấm dùng nội bộ thương mại; Agentic Organization hiện là MIT; lý do thật là R5 (identity) yếu ở cả 5 dự án, cộng với sức sống/bảo mật.

### Cited Findings
| Dự án | Sao (2026-09-27) | Release/tag mới nhất | Commit cuối | Giấy phép (LICENSE thực) | R5 tổng | Phán quyết |
|---|---|---|---|---|---|---|
| VisionClaw | 26 | r135.4-sec 2026-09-23 | 2026-09-23 (snapshot) | MIT | rất yếu | Vẫn loại (tham khảo R3/R4) |
| FleetQ | 70 | v1.27.0 2026-06-09 | 2026-09-21 | AGPL-3.0 | yếu nhưng mở rộng được bằng plugin | **Khôi phục làm ứng viên** |
| Agentic Organization | 3 | không có | 2026-09-09 | MIT (README ghi CC+MIT) | dữ liệu tốt, runtime không dùng | Vẫn loại (tham khảo data model) |
| Foundry | 442 | v1.0.0 2026-06-24 | 2026-06-30 | GPL-3.0 | yếu, không kênh | Vẫn loại |
| MDH | 1 | v0.5.5 2026-08-26 | 2026-09-24 | Apache-2.0 | không có | Vẫn loại |

Nguồn: các bảng và link ở Câu 1–5 (GitHub repo pages; `git for-each-ref`; LICENSE từng repo).

Rủi ro nổi bật:
- Bảo mật: FleetQ Telegram → mọi người gửi chạy với quyền owner ([ProcessTelegramMessageAction.php#L57](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Telegram/Actions/ProcessTelegramMessageAction.php#L57)); Agentic Organization Telegram duyệt task không kiểm người bấm ([telegram_bot.py#L280](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/telegram_bot.py#L280)); VisionClaw `mcp_servers` không phân tenant ([mcp-client.ts#L28](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/mcp-client.ts#L28)).
- Chi phí token: VisionClaw gọi thêm judge clarify, critique, completion evaluator, MoA jury cho mỗi yêu cầu phức tạp; model ID cứng ([active-clarification.ts#L20](https://github.com/Huskyauto/VisionClaw-Agent-Public-Release/blob/9ae729eb6728d89d48563cfe5b51f1f3095140ad/server/active-clarification.ts#L20)); FleetQ không chặn chi tiêu team khi self-host chưa "mua credit" ([CheckBudgetAction.php#L38](https://github.com/escapeboy/agent-fleet-o/blob/e2abe66c17e2efdeaf4615606a3e75e14f8796df/app/Domain/Budget/Actions/CheckBudgetAction.php#L38)) → phải tự đặt budget cap.
- Bảo trì: cả 5 dự án về thực chất là 1 tác giả chính (git shortlog).

### Inferences
- Không dự án nào đạt R5b (một người trên Telegram/Zalo/web = một hồ sơ) → nếu chọn bất kỳ dự án nào, lớp identity phải tự xây; FleetQ là dự án duy nhất cho phép làm việc này phần lớn **không fork** (plugin + AI middleware).
- Với yêu cầu Zalo: không dự án nào có Zalo; FleetQ là nơi duy nhất thêm adapter mà không sửa lõi.

### Gaps
- Không cài đặt/chạy thử dự án nào ([CHẠY] = 0); mọi kết luận runtime là suy luận từ mã.
- Trang gnu.org, choosealicense.com, commonsclause.com, tldrlegal.com bị proxy chặn → phần pháp lý dựa trên văn bản LICENSE nằm trong repo; khuyến nghị luật sư xác nhận phạm vi AGPL §13 khi bot phục vụ khách hàng bên ngoài.
- Ảnh đã lưu vào `research_notes/Nền tảng agent cho phòng Marketing/screenshots/`: `visionclaw-screenshot-home.jpg`, `visionclaw-tour-command-center.jpg`, `fleetq-qa-dashboard.png`, `fleetq-agents.png`, `foundry-screenshot-org.png`, `foundry-screenshot-chat.png` (đều lấy từ repo, không tự chụp). Agentic Organization và MDH không có ảnh trong repo.
