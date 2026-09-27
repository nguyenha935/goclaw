# elizaOS nhánh `develop`: hướng phát triển, và mức đáp ứng yêu cầu "agent company" cho phòng Marketing (kiểm mã + chạy thật với stub LLM, 2026-09-27)

Phạm vi: nhánh `develop` của `github.com/elizaOS/eliza`, HEAD **`83f63ba0b940cc76d8f6b4413be99064627ece8a`** (2026-09-27 10:49 -0700, "fix(agent,core,plugin-sql): export secrets opt-in, atomic media, WS backpressure…", #32836). Ngày kiểm: 2026-09-27 (đã xác nhận bằng `date`).

Mọi link mã dưới đây có gốc `https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/`. Ký hiệu: [MÃ] đọc mã, [CHẠY] chạy thật với stub LLM, [DOC] tài liệu/trang web, [?] chưa rõ. Bằng chứng chạy (trích request đã rút gọn) nằm ở `evidence/elizaos_develop_run_evidence.txt` (17 KB); số `#n` trong ghi chú này là số thứ tự request trong file đó.

So với lần kiểm trước (commit `eb157cac`, 2026-09-26, ghi trong `Nền tảng agent nhận diện người dùng/elizaos.md`), HEAD mới hơn 18 commit (105 file, +6.525/−750 dòng). Các đường dẫn mã quan trọng vẫn còn nguyên [MÃ].

## 1. Hướng phát triển: `develop` đang đi về "agent company" (tổ chức/phòng ban nhiều agent) hay "agentic OS" cá nhân?

### Takeaway
Bằng chứng nghiêng hẳn về **agentic OS cá nhân, xoay quanh một chủ sở hữu (OWNER)**. Ngày 2026-06-25, README bỏ dòng "Multi-Agent Architecture… orchestrating groups of specialized agents" và thay bằng "Your agentic operating system". Trong ~25 nghìn commit kể từ 2026-06-18, không commit nào nói về phòng ban hay tổ chức agent. Các commit có chữ "multi-agent" chỉ là kiểm thử (voice group, "arena" đánh giá hội thoại). Chữ "org" gần như luôn là tổ chức tính tiền của Eliza Cloud. `the-org` vẫn 404 và không có bản kế nhiệm trong monorepo. Với người dùng, điều này có nghĩa là muốn có "phòng Marketing" thì phải tự xây lớp phòng ban, và nó đi **ngược** thiết kế mặc định: người lạ là GUEST, tài liệu thuộc về owner, mọi thứ quy về một chủ.

### Cited Findings
- **README đổi định vị.** Hiện tại: "**Your agentic operating system.**" ([README.md#L4](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/README.md#L4)). Mô tả Eliza liệt kê "calendar, reminders, inbox, goals, health, and other personal-assistant domains", "camera, phone, messages, contacts, location… native device bridges", "EVM and Solana wallet". README hiện không có chữ "multi-agent", "group", "team", "organization" hay "business" (grep, 0 kết quả) [MÃ].
- Tại commit gốc `f7a6b0fea5` ("elizaOS v2.0.4 — clean baseline", 2026-06-18), README còn ghi "🤖 **Multi-Agent Architecture**: Designed from the ground up for creating and orchestrating groups of specialized agents" và "dashboard for managing agents, groups". Commit `12d52627d4` (2026-06-25, Shaw, #9703) "docs(readme): recast elizaOS as the agentic OS + Eliza app" đã viết lại: "Eliza = the application (desktop, mobile, web): assistant, voice, connectors, wallet…; elizaOS = the application runtime + a full OS on Linux and Android" [MÃ git].
- **Lịch sử bị viết lại.** Commit cũ nhất trên `develop` là `f7a6b0fea5` ngày 2026-06-18 ("clean baseline"). Từ đó đến HEAD có 24.974 commit (11.762 commit first-parent). Theo tháng (first-parent/tất cả): 2026-06 (từ ngày 18): 2.282/4.865; 2026-07: 3.251/6.377; 2026-08: 5.381/9.547; 2026-09 (đến ngày 27): 848/4.185 [MÃ git].
- **Chủ đề commit** (đếm scope conventional-commit trên 19.591 commit có scope, 2026-06-18→2026-09-27): cloud 2.948, ui 2.181, core 1.608, agent 1.178, ci 813, app 679, app-core 441, orchestrator 376, android 358, voice 348, local-inference 312, lifeops 273, personal-assistant 149, calendar 143, discord 129, computeruse 128; trong khi telegram 39, memory 37, documents 33, relationships 7, identity 6, knowledge 4, roles 3 [MÃ git].
- **Từ khoá tổ chức/đa agent** (grep tiêu đề commit trong cùng khoảng):
  - "department": 0.
  - "multi-agent|multiagent|multiple agents": 6, đều là voice/kiểm thử. Ví dụ "feat(voice): VOICE_GROUP multi-agent room turn-taking policy (#8786)" (2026-06-21), "test(scenarios): … multi-agent pile-on conversation-quality scenarios" (2026-08-23), "feat(scenarios): add multi-runtime agent arena" (2026-08-27, PR #29533/#29557).
  - "team": 8 (cloud "team credential pool", "discord: keep team members out of owner aliases").
  - "company": 2 (chuyển website công ty sang repo khác).
  - "a2a|agent-to-agent": 32, toàn bộ là giao thức A2A tính phí của **Eliza Cloud**, ví dụ "fix(cloud): fail closed A2A credits summary", "fix(a2a): enforce caller role trust boundary".
  - "delegat": 31, chủ yếu là LifeOps ủy quyền trên connector của owner ("feat(lifeops): process delegated connector turns") và Android JNI.
  - "\borg\b|organization": 74, phần lớn là tổ chức thanh toán trên cloud ("feat(cloud): enforce coherent organization quota authority").

  [MÃ git]
- **"Arena" nhiều agent là công cụ kiểm thử.** `packages/testing/scenario-runner/src/multi-agent-arena.ts` "Runs bounded shared-room evaluations across independently stateful Eliza runtimes" ([L1-L4](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/testing/scenario-runner/src/multi-agent-arena.ts#L1-L4)). Mỗi "seat" là một `AgentRuntime` với thư mục PGlite riêng. Có assertion `storageIsolation` kiểm các `pgliteDir` khác nhau ([L670-L690](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/testing/scenario-runner/src/multi-agent-arena.ts#L670-L690)). Agent "nghe" nhau vì harness lấy câu trả lời của một seat rồi tự gọi `messageService.handleMessage` của các seat khác ([L214-L250](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/testing/scenario-runner/src/multi-agent-arena.ts#L214-L250), [L620-L667](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/testing/scenario-runner/src/multi-agent-arena.ts#L620-L667)). Kịch bản "Lighthouse" dựng một đội bán hàng (Riley "account executive", Sam "solutions architect", Casey "compliance"), nhưng vai trò chỉ nằm trong `bio` ([multi-agent-sales-lighthouse.ts#L11-L37](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/testing/scenario-runner/src/multi-agent-sales-lighthouse.ts#L11-L37)) [MÃ]
- **Không có mã tổ chức/phòng ban.** Grep "department", "org-chart", "the-org" trong `*.ts/*.tsx/*.md/*.json` chỉ ra dữ liệu benchmark (`packages/benchmarks/...`) [MÃ]. `github.com/elizaOS/the-org` trả HTTP 404 [DOC, 2026-09-27].
- **Issue.** Tìm `is:open "multiple agents"` trên issue của repo: 0 kết quả, trên tổng 61 issue mở. Tìm "multi-agent" chỉ ra issue refactor/SQLite không liên quan, ví dụ #32099 "Add durable per-agent SQLite runtime database adapter", #31532 "refactor(core): implement lean Node-only runtime, consolidate packages" [DOC, trang issues GitHub].
- **Hạ tầng hướng thiết bị cá nhân.** Có `plugins/plugin-sqlite`, rất nhiều `plugin-native-*` (camera, phone, contacts, location, wifi…), `packages/os` (Linux/Android). `AGENTS.md` yêu cầu "Preserve authorization, tenant isolation…", nhưng tenant chỉ tồn tại ở Eliza Cloud [MÃ].

### Inferences
- `develop` là sản phẩm "một người – một trợ lý – nhiều thiết bị/connector". Đa agent chỉ còn ở hai nơi: dịch vụ cloud (`packages/cloud/services/agent-server`, xem §2) và bộ kiểm thử (arena). Không có tín hiệu nào cho thấy lộ trình "agent company".
- Hệ quả cho người dùng: có thể dùng elizaOS làm **thư viện runtime** (AgentRuntime, plugin, danh tính, vai trò), nhưng lớp phòng ban phải tự viết. Các mặc định an toàn của elizaOS (GUEST, tài liệu thuộc owner) sẽ phải được nới có chủ đích cho từng nhân viên. Sản phẩm lõi sẽ tiếp tục đổi nhanh theo hướng OS/mobile, không theo hướng doanh nghiệp.

### Gaps
- Không đọc được docs.elizaos.ai (lần trước bị chặn). Không có ROADMAP hay CHANGELOG trong repo: `find -iname '*roadmap*' -o -iname 'CHANGELOG*'` ở độ sâu 3 không thấy [MÃ].
- Không đọc nội dung Discussions.

## 2. Nhiều agent trong một triển khai, và agent nhắn/giao việc cho nhau

### Takeaway
Host độc lập `packages/agent` vẫn chỉ đọc `agents.list[0]` [MÃ]. Khoá `agentToAgent` chỉ có trong type và schema, không có nơi nào đọc [MÃ]. Có hai cách đã được chứng minh để chạy nhiều agent:
1. Tự tạo nhiều `new AgentRuntime(...)` trong một process. Nghiên cứu này làm vậy với 2 agent và đi qua đường Telegram thật [CHẠY]; bộ arena của elizaOS cũng làm vậy [MÃ].
2. Dịch vụ cloud `agent-server`: một pod giữ `Map` nhiều runtime, dùng chung `POSTGRES_URL` [MÃ].

Không có cơ chế nào để agent A **giao việc** cho agent B.

### Cited Findings
- `config.agents?.list?.[0]` được đọc ở:
  - [first-time-setup.ts#L280](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/runtime/first-time-setup.ts#L280)
  - [build-character-config.ts#L40](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/runtime/build-character-config.ts#L40)
  - [plugin-collector.ts#L80](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/runtime/plugin-collector.ts#L80), `#L141`
  - `server.ts:2255`, `agent-admin-routes.ts:46`
  - `packages/app/src/runtime/build-character-from-config.ts:42,51`

  Commit `00a7c80914` (2026-08-23) "fix(agent): restore an explicitly empty agents.list after an app launch" vẫn theo mô hình một agent [MÃ].
- `agentToAgent?: { enabled?: boolean; allow?: string[] }` "Enable agent-to-agent messaging tools. Default: false" ([types.tools.ts#L379-L384](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/config/types.tools.ts#L379-L384)). `session.agentToAgent.maxPingPongTurns` ([channel-config.ts#L166-L169](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/types/channel-config.ts#L166-L169)) có hình dạng giống hệt config của OpenClaw. Grep toàn repo chỉ thấy khoá này trong `types.tools.ts`, `channel-config.ts`, `zod-schema*.ts`, `schema.ts`. Tên tool `sessions_send`/`sessions_spawn` chỉ xuất hiện trong danh sách chuỗi ở `packages/core/src/types/tools.ts#L60-L99`, không có triển khai [MÃ].
- Cloud: `AgentManager` "Maintains an in-memory Map of loaded agents and their runtimes… Publishes server/agent state to Redis for gateway routing" ([agent-manager.ts#L189-L199](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/cloud/services/agent-server/src/agent-manager.ts#L189-L199)). Mỗi agent được tạo bằng `new AgentRuntime({ character, plugins })` với `POSTGRES_URL: process.env.POSTGRES_URL` ([#L340](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/cloud/services/agent-server/src/agent-manager.ts#L340), [#L372](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/cloud/services/agent-server/src/agent-manager.ts#L372)), tức nhiều agent dùng chung một Postgres. Dịch vụ này cần Redis và gateway của cloud [MÃ].
- Kiểu `Project { agents: ProjectAgent[] }` vẫn còn ([types/plugin.ts#L1331-L1332](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/types/plugin.ts#L1331-L1332)) nhưng không có lớp `ElizaOS` điều phối [MÃ].
- **Chạy thật hai agent trong một process.** "Content Lead" (agentId `4bb9216b…`) và "Copywriter" (`0d9ba76d…`), mỗi agent một thư mục PGlite. Cả hai nhận tin Telegram qua `MessageManager.handleMessage` [CHẠY]. PGlite khoá thư mục theo agent, nên muốn dùng chung DB thì phải dùng Postgres (lần trước đã gặp lỗi `PGlite lock file is held`).
- **Giao việc thực tế** [CHẠY]:
  - S10: Lan (GUEST) nhắn DM "Giao Copywriter viết 3 caption cho fanpage X nhé." Planner chỉ có `DISCOVER_ACTIONS, REPLY, IGNORE, STOP` (#86).
  - S10b: Admin (ADMIN) gửi cùng yêu cầu. Planner có thêm `MESSAGE_SEND` (#92). Đây là gửi tin qua connector tới người/phòng, không phải tới runtime agent khác.
  - Copywriter không nhận request LLM nào liên quan đến việc được giao. Khi Lan tự nhắn Copywriter (S11), prompt Stage 1 của Copywriter không có gì về Lan (#101).
- `plugin-agent-orchestrator` chỉ spawn coding sub-agent qua ACP. Nó ghi `userId: message.entityId` vào metadata phiên ([tasks.ts#L1158](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-agent-orchestrator/src/actions/tasks.ts#L1158), `#L2080`) [MÃ]. Các action `AWAIT_CHILD_AGENT_DECISION`, `RETRIEVE_CHILD_AGENT_RESULTS`, `TUNNEL_CREDENTIAL_TO_CHILD_SESSION` trong `plugin-assistant/src/features/sub-agent-credentials/` phục vụ "PTY session id of the spawned child coding agent" [MÃ].

### Inferences
- Mẫu "N runtime + relay bằng `messageService.handleMessage`" chính là cách chính elizaOS dùng trong arena. Đây là điểm bám tự nhiên cho host phòng ban, không cần fork core.
- 5d phải tự xây hoàn toàn. Vì UUID entity băm theo agentId, người yêu cầu phải được truyền bằng khoá tự nhiên (platform + id), không phải bằng UUID.

### Gaps
- Chưa chạy `agent-server` của cloud (cần Redis, gateway) [?].
- Chưa đọc mã A2A của Eliza Cloud (`packages/cloud`) ngoài tiêu đề commit. Chưa rõ nó có dùng được cho agent tự host hay không (chưa kiểm chứng).

## 3. Chấm develop theo D1, K1–K5, 5d và baseline (kèm kết quả chạy)

### Takeaway
Chạy được toàn bộ giao thức qua đường vào Telegram thật với stub LLM. Kết quả:
- **Đạt:** K3 (persona có trong system prompt của mọi lượt, cả nhóm lẫn DM), K2-5b-in (fact theo người, tự chèn), R1, R7.
- **Một phần:** K2-5a, K4 (DM cách ly tốt, nhưng bí mật kể trong DM **có** trong prompt khi người đó nói ở nhóm; không có cơ chế cấp quyền X→Y), K5 (ràng buộc admin theo Telegram id qua cấu hình thì chạy đúng, kẻ giả tên bị từ chối; nhưng không bind qua chat), K2-5b-cross [MÃ], R6, R8.
- **Không:** D1, 5d, và K1 cho người dùng Telegram thường. Tài liệu tri thức mặc định chỉ OWNER đọc được: người dùng GUEST không có context `knowledge`, và kể cả ADMIN hay tài liệu đã pin cho toàn agent cũng không vào prompt.

### Cách chạy và các chỗ lệch khỏi production
- Clone blobless `develop` @ `83f63ba0` (29.296 file, 749 MB). Cài tối thiểu bằng bun 1.3.11 `install --ignore-scripts` với `package.json` gốc bị cắt còn 6 workspace: `packages/core`, `packages/auth`, `plugins/plugin-assistant`, `plugin-sql`, `plugin-openai`, `plugin-telegram`. Đã xoá `devDependencies` và các phụ thuộc `workspace:*` không dùng. Kết quả: 629 gói, `node_modules` 385 MB.
  - Lệch: repo ghim bun 1.4.2 và Node 24.15.0 (`package.json` `packageManager`, `engines`, AGENTS.md). Postinstall (build views, fused inference…) không chạy.
- Chạy mã TS thẳng bằng `bun --conditions=eliza-source`. Harness tự dựng 2 `AgentRuntime` với bộ plugin theo `createAssistantPlugins()` ([assistant-plugins.ts#L23-L66](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/runtime/assistant-plugins.ts#L23-L66)): `createAssistantPlugin()`, `ConnectorAccountManager`, `documentsPlugin`, `trajectoriesPlugin`, relationships services, cộng `plugin-sql` và `plugin-openai`.
  - Lệch: không dùng host `packages/agent` (chỉ chạy một agent). Không đăng ký `identityHttpPlugin` và roles capability của host (`eliza.ts#L4672`). Việc giải vai trò vẫn chạy trong core và đọc thẳng `ELIZA_ROLES_CONNECTOR_ADMINS_JSON`.
- Tin nhắn đi qua đường vào thật: `plugins/plugin-telegram/src/messageManager.ts` `MessageManager.handleMessage(ctx)` ([#L1538](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-telegram/src/messageManager.ts#L1538)), với `telegraf.Context` dựng từ update giả. Telegraf trỏ `apiRoot` tới một Bot API giả (Bun.serve). Không khởi động `TelegramService` (polling) và không dùng token hay tài khoản thật nào. Bot API giả ghi nhận 19 lần `sendMessage`, tức trả lời thực sự đi ra đường gửi.
- Cờ môi trường: `TELEGRAM_AUTO_REPLY=true`, `ELIZA_LIFEOPS_PASSIVE_CONNECTORS=false`. Mặc định connector ở chế độ passive LifeOps (chỉ lưu, không trả lời) — [messageManager.ts#L1830-L1886](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-telegram/src/messageManager.ts#L1830-L1886) [MÃ].
- `LOAD_DOCS_ON_STARTUP=true` phải đặt bằng biến môi trường. Đặt trong settings của character thì không kích hoạt nạp tài liệu (quan sát khi chạy; chưa tìm nguyên nhân).
- Stub LLM là bản sao `stub_llm_tpl.py`, thêm khoá `match_all` và `capture`/`{{G1}}` để trả `sourceMessageIds` đúng cho evaluator `factMemory`. Stub chạy ở **cổng 18114**, không phải 18104, vì 18104 đang bị `stub_ragflow.py` của nghiên cứu khác chiếm (PID 7473; không đụng tới). Stub quyết định định tuyến Stage 1 (ví dụ chọn `general`, `knowledge`), nên hành vi với LLM thật có thể khác. Embedding của stub là vector băm giả, nên điểm tìm kiếm ngữ nghĩa không có ý nghĩa. Tuy vậy, kết luận K1 dựa trên quy tắc hiển thị tài liệu, không phụ thuộc embedding.
- Pin tài liệu: harness gọi `DocumentService.setDocumentPinsWithAccessContext` với AccessContext `OWNER`/`trusted-local`, giống cách route dashboard của plugin-knowledge làm ([plugin-knowledge/src/plugin.ts#L44-L62](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-knowledge/src/plugin.ts#L44-L62)).
- Cast: agent 1 "Content Lead – Phòng Marketing", agent 2 "Copywriter – Phòng Marketing". Lan = 1001 (`lan_mkt`), Minh = 1002, Admin Hà = 9001 (`ha_admin`), kẻ giả mạo = 1003 với tên hiển thị cũng là "Admin Hà" (`ha_admln`). G1 = -100111 "G1 Marketing", G2 = -100222 "G2 KPI". Cấu hình admin: `ELIZA_ROLES_CONNECTOR_ADMINS_JSON={"telegram":["9001"]}`.

### Cited Findings theo tiêu chí

**D1 — vận hành phòng ban**
- `Character` không có trường nào cho chức danh, phòng ban hay cấp trên. Vai trò OWNER/ADMIN/USER/GUEST là của **người gửi** trong một World ([roles.ts#L1-L23](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/roles.ts#L1-L23)) [MÃ].
- Chạy thật: "Cấp dưới của bạn là Copywriter" chỉ nằm trong system text. Không có action phân rã hay giao việc theo vai trò (S10, #86, #92) [CHẠY]. Không có hàng đợi review/duyệt giữa agent. `ApprovalService`/`PendingUserAction` phục vụ duyệt của owner (ghi chú trước) [MÃ].

**K1 — kho tri thức chung**
- Nạp tài liệu có bốn đường: thư mục (`DOCUMENTS_PATH` → mặc định `./docs`, chỉ quét lúc khởi động, không theo dõi thay đổi — [docs-loader.ts#L1-L10](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/docs-loader.ts#L1-L10), [service.ts#L450-L480](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/service.ts#L450-L480), bật bằng `LOAD_DOCS_ON_STARTUP` [#L512](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/service.ts#L512)); upload/URL qua HTTP route của `plugin-knowledge`; action chat `DOCUMENT`; và `character.documents` [MÃ].
- Phạm vi hiển thị: `global | owner-private | user-private | agent-private` ([types.ts#L191-L195](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/types.ts#L191-L195)). Mọi truy vấn tài liệu đều lọc theo `agentId`. `DocumentService` luôn truyền `agentId: this.runtime.agentId` (ví dụ [service.ts#L1418](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/service.ts#L1418), [#L1442](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/service.ts#L1442)). Adapter SQL đặt điều kiện `eq(memoryTable.agentId, params.agentId)` trong các truy vấn tài liệu (ví dụ [plugin-sql base.ts#L2769](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-sql/src/base.ts#L2769), [#L2793](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-sql/src/base.ts#L2793), ngay trước `getDocument` ở [#L2798](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-sql/src/base.ts#L2798)). Vì vậy **không có kho dùng chung giữa các agent**, kể cả khi hai agent cùng một Postgres [MÃ].
  - Chạy thật: cùng một thư mục `shared_docs/brand_guideline.md` được nạp thành **hai bản riêng**: `de66b1c5…` (agentId `4bb9216b…`) và `f4ab9c0e…` (agentId `0d9ba76d…`), đều có `scope:"global"`, `addedByRole:"RUNTIME"` [CHẠY].
- **Quy tắc đọc** ([document-list-query.ts#L497-L530](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/database/document-list-query.ts#L497-L530)):
  - Chỉ `OWNER`/`AGENT`/`RUNTIME` thấy mọi tài liệu ([#L258-L262](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/database/document-list-query.ts#L258-L262)).
  - GUEST chỉ thấy tài liệu `global` thuộc phòng mà họ đang tham gia.
  - ADMIN/USER cũng phải tham gia phòng gốc của tài liệu, trừ khi có `directGrantEntityIds` (tham số `readerEntityIds` của action `DOCUMENT`).

  [MÃ]
- Trong một cuộc trò chuyện, tài liệu chỉ được dùng nếu **mọi** người tham gia (trừ agent) đều đọc được ([service.ts#L1200-L1225](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/service.ts#L1200-L1225)) [MÃ].
- **Truy xuất**: provider `DOCUMENTS` là RAG tự chèn, nhưng `dynamic` và chỉ chạy khi Stage 1 chọn context `documents`/`knowledge` ([provider.ts#L88-L101](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/provider.ts#L88-L101)). Hai context này yêu cầu `minRole: "USER"` ([default-contexts.ts#L45-L68](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/runtime/default-contexts.ts#L45-L68)). `PINNED_DOCUMENTS` là provider luôn chèn (GUEST cũng được), nhưng chỉ hiện pin mà cả phòng đọc được ([pinned-provider.ts#L5-L14](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/documents/pinned-provider.ts#L5-L14)) [MÃ].
- **Chạy thật** (`evidence` #45–#52, #63–#64, #128–#135):
  - S6 (Minh DM Copywriter "Slogan công ty là gì?") và S7 (Lan hỏi giá gói Pro ở G1): `role=GUEST`, "Available Contexts" chỉ có `simple, general`, prompt không chứa "Nhanh như chớp" hay "199.000".
  - S8b (Admin DM, Stage 1 chọn `knowledge,general`): planner có tool `DOCUMENT` và một mục `# Documents` **rỗng**.
  - Sau khi OWNER pin tài liệu cho toàn agent (`pinTargets.agent=true`), S15 và S16 vẫn không có tài liệu hay "Pinned" trong prompt.

  [CHẠY]

**K2-5a — danh tính người gửi, kênh, nhóm**
- Prompt planner DM(Lan) (#33) có "# People in the Room / Lan aka lan_mkt ID: 431eff90…" và "World: 1001; current channel: Lan (DM), participants=2". Prompt ở G1 (#116) có "World: -100111; current channel: G1 Marketing (GROUP), participants=3". "Current message" chứa `"source":"telegram"` và `"channelType":"GROUP"` [CHẠY].
- Không có Telegram user id thô (1001). UUID là `createUniqueUuid(runtime, "default:1001")`, tức băm theo agent ([identity.ts#L68-L95](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-telegram/src/identity.ts#L68-L95)) [MÃ]. Với Copywriter, Lan là một UUID khác [CHẠY lần trước].

**K2-5b-in — cùng một người qua G1, G2 và DM**
- Evaluator hậu lượt `factMemory` ghi fact theo người nói. Bảng facts của agent 1: "KPI tháng 10 của Lan là 50 bài" (entity Lan, phòng G2) và "Lan phụ trách fanpage X và thích giọng văn hài hước" (entity Lan, phòng G1) [CHẠY].
- S4 DM(Lan) "Bạn biết gì về mình? KPI của mình bao nhiêu?": planner (#33) có "Things Content Lead knows about the speaker: [durable.goal] KPI tháng 10 của Lan là 50 bài / [durable.business_role] Lan phụ trách fanpage X…". Tức là tự chèn, không cần tool [CHẠY]. Nguồn: provider `FACTS` ([facts.ts#L344-L352](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L344-L352), [#L364-L416](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L364-L416), [#L507](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L507)).
  - Điều kiện 1: Stage 1 phải chọn context `general`. Ở Stage 1 (#32) không có fact nào.
  - Điều kiện 2: evaluator phải trích được fact với `sourceMessageIds` đúng.
- Điểm lạ: `FACTS` khai báo `roleGate: { minRole: "USER" }` ([facts.ts#L352](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L352)), nhưng Lan (GUEST) vẫn nhận được khối fact [CHẠY]. Nguyên nhân chưa kiểm chứng.
- Fact "Minh là thành viên nhóm G1" không được ghi trong lần chạy này, nhiều khả năng do luật stub (chưa kiểm chứng).

**K2-5b-cross — cùng một người qua nhiều kênh**
- Route `POST /api/identity/person-links/attest` và `/verify` chỉ cho OWNER/ADMIN ([identity-person-link-routes.ts#L20-L21](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/api/identity-person-link-routes.ts#L20-L21), [#L63-L67](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/api/identity-person-link-routes.ts#L63-L67)) [MÃ].
- Tự gộp khi `AUTO_MERGE_CONFIDENCE_THRESHOLD = 0.85` và `AUTO_MERGE_MIN_EVIDENCE = 2` ([relationships.ts#L464-L465](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/services/relationships.ts#L464-L465), [#L2110-L2111](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/services/relationships.ts#L2110-L2111)) [MÃ].
- FACTS mở rộng theo cụm `getRelatedEntityIds` (gồm cả liên kết suy ra chưa xác minh); `getVerifiedRelatedEntityIds` có tồn tại nhưng không được dùng ([identity-clusters.ts#L50](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/identity-clusters.ts#L50), [#L74](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/identity-clusters.ts#L74)) [MÃ].
- Liên kết chỉ có hiệu lực trong một agent. **Chưa chạy**, vì harness không có kênh thứ hai.

**K3 — quy tắc persona**
- `buildCanonicalSystemPrompt` = `system` + `# About` (bio) + `# User Role` ([system-prompt.ts#L59-L82](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/runtime/system-prompt.ts#L59-L82)). `buildCharacterStyleDirections` chèn `style.all` + `style.chat` dưới dạng khối tĩnh "# Message Directions" vào prefix cache được, "never through the per-room CHARACTER provider" ([#L93-L118](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/runtime/system-prompt.ts#L93-L118)) [MÃ].
- Provider `CHARACTER` chỉ chạy với role USER trở lên và context `general`/`agent_internal` ([character.ts#L50-L58](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/basic-capabilities/providers/character.ts#L50-L58)). Provider này chèn thêm adjectives, topics và messageExamples. Với feed/thread thì dùng `style.post` [MÃ]. Hệ quả: với GUEST, `adjectives`, `topics` và `messageExamples` **không** vào prompt; chỉ `system`, `bio` và `style.all/chat` là luôn có [MÃ; khớp #3].
- Chạy thật: cả 3 quy tắc "Luôn xưng em, gọi người dùng là anh/chị / Không dùng emoji / Không bàn chính trị" nằm trong **system message** của mọi request Stage 1 và planner của agent 1: G1, G2, DM; Lan, Minh (GUEST), Admin (ADMIN), kẻ giả mạo (#3, #10, #18, #32–#33, #39–#40, #51–#52, #57–#58, #69–#75, #79–#80, #85–#86, #91–#97, #106, #115–#116, #122–#123, #134–#135). Không có trong prompt của evaluator hậu lượt (#7, #11…), vì đó không phải lượt trả lời [CHẠY].
- Persona sửa được qua chat: action `CHARACTER` (roleGate ADMIN, [character.ts action#L142-L144](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/advanced-capabilities/personality/actions/character.ts#L142-L144)). Admin được đưa tool `CHARACTER_UPDATE_IDENTITY` (#70); kẻ giả mạo thì không (#80) [CHẠY].

**K4 — riêng tư, và ngoại lệ do admin cho phép**
- S5, Minh DM "Lan có KPI bao nhiêu?": planner (#40) chỉ có Minh trong "People in the Room", **không** có fact nào của Lan [CHẠY].
- S8, Admin DM "Lan đã nói gì về KPI?": planner (#58) cũng không có fact của Lan [CHẠY].
- **Rò rỉ theo ngữ cảnh.** S12: Lan DM "Nhớ giúp: mình sắp nghỉ việc, đừng nói với ai." Sau đó S13: Lan nói ở G1, nơi Minh cũng có mặt. Planner (#116) chứa "Things Content Lead knows about the speaker: … [durable.life_event] **Lan sắp nghỉ việc (bí mật, không nói với ai)**" [CHẠY]. Model có thể nói ra bí mật trong nhóm. Chưa kiểm câu trả lời với LLM thật.
- S14, Minh hỏi ở G1 "Lan có kế hoạch gì sắp tới không?": planner (#123) có "Known facts in this room (about other participants): Lan phụ trách fanpage X…". Đây là fact Lan tự nói **trong G1**, không phải fact từ DM [CHẠY].
- **Cơ chế cho admin cấp quyền X→Y:** không có. Thứ gần nhất là action `MESSAGE` (roleGate ADMIN, [message.ts#L6599](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/advanced-capabilities/actions/message.ts#L6599)) với các thao tác `read_channel`, `read_with_contact`, `search_inbox` đọc lịch sử qua connector ([#L370-L380](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/advanced-capabilities/actions/message.ts#L370-L380)) [MÃ]. Admin được đưa `MESSAGE_SEARCH_INBOX`, `MESSAGE_GET_USER`… (#58) [CHẠY]. Tức là ADMIN có quyền đọc rộng, không có bước cấp riêng cho từng cặp người. `checkSenderPrivateAccess` ([roles.ts#L927-L993](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/roles.ts#L927-L993)) không được plugin-assistant gọi [MÃ].

**K5 — bind admin qua chat bằng ID nền tảng đã xác minh**
- `roles.connectorAdmins = { "telegram": ["telegramUserId1"] }` ([roles/src/index.ts#L1-L15](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/runtime/roles/src/index.ts#L1-L15)) được chuyển thành `ELIZA_ROLES_CONNECTOR_ADMINS_JSON` ([runtime-settings.ts#L292-L296](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/runtime/runtime-settings.ts#L292-L296)). Core so khớp với `metadata.telegram.userId|id` mà connector đóng dấu vào Memory. Resolver không tin `content.metadata` do client gửi ([roles.ts#L702-L724](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/roles.ts#L702-L724), [#L831-L838](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/roles.ts#L831-L838), [#L840-L925](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/roles.ts#L840-L925)). Kết quả là ADMIN, không phải OWNER [MÃ].
- **Chạy thật:**
  - 9001: "# User Role ADMIN", Available Contexts có 14 mục (`simple, general, memory, documents, knowledge, files, email, contacts, messaging, social_posting, media, connectors, settings, world`) (#57).
  - Kẻ giả mạo 1003 cùng tên hiển thị "Admin Hà": `GUEST`, chỉ có `simple, general`. Cùng yêu cầu "Sửa tính cách…" thì không được đưa tool `CHARACTER_UPDATE_IDENTITY` (#79–#80, so với #69–#70).

  Tức là nhận diện theo ID nền tảng, không theo tên [CHẠY].
- **OWNER** được công nhận qua `ELIZA_ADMIN_ENTITY_ID`/owner contacts ([roles.ts#L120-L121](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/roles.ts#L120-L121), [#L392-L416](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/roles.ts#L392-L416)). OWNER lưu trong world chỉ được tính nếu nguồn là `"manual"` ([#L870-L880](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/core/src/roles.ts#L870-L880)) [MÃ].
- **Bind qua chat:** owner (dashboard) phát một mã 6 chữ số, hết hạn sau 5 phút. Người dùng gửi `/eliza_pair <code>` trong Telegram. Backend ghi Telegram id đã xác minh vào entity owner ([owner-binding.ts#L1-L20](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/packages/agent/src/services/owner-binding.ts#L1-L20), [plugin-telegram owner-pairing-service.ts#L1-L21](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-telegram/src/owner-pairing-service.ts#L1-L21), [identity.ts#L68-L95](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-telegram/src/identity.ts#L68-L95)) [MÃ; chưa chạy, vì cần host `packages/agent`].
- Action `ROLE` (gán/thu hồi vai trò trong một world qua chat) chỉ dành cho OWNER ([role.ts#L683-L684](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-assistant/src/features/advanced-capabilities/actions/role.ts#L683-L684)) [MÃ].
- Cả cấu hình lẫn pairing đều theo **từng agent**, vì setting và entity owner đều gắn với runtime.

**5d — ủy quyền mang theo người yêu cầu**
- Không đạt (xem §2): không có kênh agent→agent, agent 2 không biết gì về Lan (#101) [CHẠY+MÃ].

**Baseline**
- **R1:** `plugin-openai` với `OPENAI_BASE_URL` trỏ tới endpoint riêng chạy trọn luồng (Stage 1, planner, evaluator, embeddings) mà không cần coding CLI [CHẠY]. Còn có `plugin-anthropic` và `plugin-local-inference` (thư mục `plugins/`) [MÃ].
- **R6:** đường vào Telegram trên `develop` hoạt động [CHẠY]. Bản vá `bot.launch()` của Telegraf nằm ở [service.ts#L969-L985](https://github.com/elizaOS/eliza/blob/83f63ba0b940cc76d8f6b4413be99064627ece8a/plugins/plugin-telegram/src/service.ts#L969-L985) [MÃ]. Có plugin Discord, Slack, X, iMessage [MÃ]. Zalo:
  - npm `@elizaos/plugin-zalo` và `@elizaos/plugin-zalouser`: dist-tags `latest=2.0.0-alpha`, `next=2.0.0-alpha.6`, bản cuối **2026-02-17** [MÃ registry, 2026-09-27].
  - Không có trong `plugins/` của `develop` [MÃ].
  - Connector là plugin (services, `MessageConnector`), nên thêm được mà không sửa core [MÃ].
- **R7:** MIT, "Copyright (c) 2026 Shaw Walters and elizaOS Contributors" (`LICENSE`) [MÃ].
- **R8:**
  - Hoạt động cực mạnh: 24.974 commit trong ~3,3 tháng, 168 tác giả. Shaw/lalalune/Shaw Walters chiếm ~14.769 commit (~59%). Có 369 commit do "Claude Fable 5" ký [MÃ git].
  - Mega-refactor gộp trong 2026-09-25/26 (#32784…#32813, "lean Node-only runtime, consolidate packages") [MÃ git; DOC issue #31532].
  - npm đứng yên: `@elizaos/core` `latest 1.7.2`, `beta 2.0.3-beta.7` (2026-06-28); `@elizaos/agent` `latest 0.25.9`. Package trong repo vẫn ghi `2.0.3-beta.7` [MÃ registry].
  - Trang Actions lọc `develop` hiển thị "Develop Full" #2628/#2629 thành công. Có hàng chục nghìn lượt workflow "Claude Code" (#67094) [DOC; tóm tắt do công cụ fetch, không tự đếm].

### Bảng chấm (develop @ 83f63ba0, 2026-09-27)

| Tiêu chí | Điểm | Bằng chứng chính | Tag |
|---|---|---|---|
| **D1** Phòng ban, chức danh, chia việc theo vai trò, duyệt | **Không** | Không có trường tổ chức cho agent. Vai trò là của người gửi. Chức danh chỉ là text trong `system`. Không có action phân rã/giao việc/duyệt giữa agent (#86, #92) | [MÃ+CHẠY] |
| **K1** Kho tri thức chung | **Không** (với người dùng chat thường); Một phần cho OWNER | Tài liệu lọc theo `agentId` (mỗi agent một bản, hai id khác nhau). Context `documents/knowledge` yêu cầu USER. GUEST/ADMIN phải tham gia phòng gốc của tài liệu. Pin toàn agent vẫn không vào prompt của GUEST (S15, S16). Nạp: thư mục lúc khởi động, upload/URL, action `DOCUMENT`. RAG tự chèn khi Stage 1 chọn context. Có scope `user-private`/`owner-private` riêng với fact theo người | [MÃ+CHẠY] |
| **K2-5a** Danh tính + kênh + nhóm | **Một phần (gần đạt)** | Tên, username, UUID ổn định; `source:"telegram"`, `channelType`; "World: -100111; current channel: G1 Marketing (GROUP)". Không có Telegram id thô. UUID khác nhau giữa các agent | [CHẠY] |
| **K2-5b-in** Cùng người qua nhóm/DM | **Đạt (tự động)** | DM(Lan) có fact từ G1 và G2, dưới tiêu đề "Things Content Lead knows about the speaker" (#33). Phụ thuộc Stage 1 chọn `general` và evaluator trích được fact | [CHẠY] |
| **K2-5b-cross** Cùng người qua kênh | **Một phần** | person-link attest/verify (OWNER/ADMIN), auto-merge ≥0,85 & ≥2 bằng chứng, FACTS theo cụm. Chỉ trong một agent. Chưa chạy | [MÃ] |
| **K3** Persona mọi kênh | **Đạt** | 3 quy tắc `style.all` có trong system message của mọi Stage 1/planner, cả G1/G2/DM, GUEST/ADMIN. adjectives/topics/examples chỉ vào khi role ≥ USER | [CHẠY+MÃ] |
| **K4** Riêng tư + ngoại lệ admin | **Một phần** | DM cách ly (S5 #40). Bí mật kể trong DM **có trong prompt** khi Lan nói ở nhóm có Minh (S13 #116). Fact phòng hiện cho người khác cùng nhóm (S14 #123). Không có cơ chế admin cấp quyền X→Y. ADMIN có quyền đọc hộp thư/kênh rộng qua `MESSAGE` | [CHẠY+MÃ] |
| **K5** Bind admin theo ID nền tảng | **Một phần** | `connectorAdmins {"telegram":["9001"]}` → ADMIN. Kẻ giả tên (1003) → GUEST, không có tool admin (#57, #69–#80). OWNER bind qua mã pairing từ dashboard + `/eliza_pair`, chưa chạy. Không bind hoàn toàn trong chat. Cấu hình theo từng agent | [CHẠY+MÃ] |
| **5d** Ủy quyền mang người yêu cầu | **Không** | `agentToAgent` không có nơi đọc. Không có action giao việc cho agent. Copywriter không biết Lan (#101) | [MÃ+CHẠY] |
| **R1** Backend riêng, key riêng | **Đạt** | plugin-openai với base URL riêng chạy đủ luồng | [CHẠY] |
| **R6** Kênh mở rộng bằng code, có Zalo | **Một phần** | Telegram chạy. Connector là plugin. Zalo chỉ có npm alpha.6 (2026-02-17), ngoài cây `develop`, cần port | [CHẠY+MÃ] |
| **R7** Tự host, giấy phép dùng kinh doanh | **Đạt** | MIT | [MÃ] |
| **R8** Còn sống, ổn định | **Một phần** (sống mạnh, kém ổn định) | ~25k commit từ 2026-06-18 (lịch sử bị viết lại); mega-refactor 2026-09-25/26; npm dừng ở beta.7 2026-06-28; ~59% commit từ một người | [MÃ git/registry; DOC] |

### Inferences
- Các điểm mạnh thật của `develop` là trí nhớ theo người (5b-in), persona ổn định (K3) và vai trò gắn ID nền tảng chống giả tên (K5). Chúng rất sát yêu cầu, và đã được chứng minh bằng chạy thật.
- Các điểm yếu (K1, K4, D1, 5d) có cùng một gốc: mô hình "một chủ sở hữu". Tài liệu là của owner, người lạ là GUEST, fact theo người được coi là của chính người đó ở mọi nơi. Muốn thành "phòng ban" thì phải thay chính sách chứ không chỉ thêm tính năng.
- Chi phí token mỗi lượt khá cao. Mỗi tin trả lời tốn 2–4 lời gọi LLM (Stage 1, planner, evaluator hậu lượt; với action có hiệu lực thì thêm vòng planner và evaluator hoàn tất — S9a tốn 7 lời gọi, #69–#75), cộng 3–4 lời gọi embedding. Prompt Stage 1 của lượt đầu khoảng 5,3 nghìn ký tự (system 613 + user 4.694). Evaluator hậu lượt khoảng 15,4 nghìn ký tự (đo ở lần chạy thử đầu, trước khi viết file bằng chứng).

### Gaps
- Chưa chạy với LLM thật, nên chưa biết tỷ lệ Stage 1 chọn `general`/`knowledge`, cũng chưa biết model có thật sự nói ra bí mật ở S13 hay không.
- Chưa chạy OWNER pairing `/eliza_pair`, person-link đa kênh và hai agent dùng chung Postgres (không có Docker hay Postgres server trong môi trường).
- Chưa kiểm lại ở HEAD luật regex tiếng Anh `POST_TURN_SEMANTIC_SIGNAL` (lần trước thấy ở `post-turn-policy.ts`). Evaluator vẫn chạy trong lần này nhờ "fallback interval" ("Detected extraction signal: fallback interval").
- Chưa rõ vì sao `FACTS` (roleGate USER) vẫn chạy cho GUEST, và vì sao `LOAD_DOCS_ON_STARTUP` trong character settings không có tác dụng.

## 4. Phải tự xây gì, có cần fork không (và rủi ro)

### Takeaway
Về kỹ thuật, **không cần sửa core**: mọi phần thiếu làm được bằng một host tự viết cộng các plugin, với cơ chế override provider (xem lần trước: `registerProvider` → `resolveComponentCollision`). Nhưng vì `develop` không có bản phát hành npm (npm dừng ở 2.0.3-beta.7, 2026-06-28), trên thực tế bạn sẽ phải **vendor một snapshot `develop` (fork mềm)** và tự rebase. Ước lượng cho MVP lớp phòng ban: **khoảng 2–3 người-tháng**, cộng chi phí bám `develop` liên tục. Kết luận: không nên chọn elizaOS `develop` làm nền cho "agent company" trừ khi chấp nhận tự duy trì một nhánh. Nên dùng nó làm tham chiếu thiết kế cho danh tính, vai trò và trí nhớ theo người.

### Cited Findings (điểm bám có sẵn)
- Mẫu đa runtime cộng relay `messageService.handleMessage` đã có trong arena và cloud agent-server (§2) [MÃ].
- Harness của nghiên cứu này chạy 2 runtime chỉ với API công khai của `@elizaos/core` và các plugin, không sửa file core nào [CHẠY].
- Có sẵn các thành phần: `Character.settings.extra` (JsonObject), `ComponentTypeDefinition`, `runtime.createComponent`, `Plugin{actions, providers, evaluators, services, routes}` (xem `known_platforms.md` §3) [MÃ ghi chú trước; đường dẫn vẫn tồn tại ở HEAD].

### Inferences — danh sách việc và ước lượng (1 kỹ sư TypeScript quen elizaOS)

| # | Hạng mục | Cách làm (plugin/host, không sửa core) | Công |
|---|---|---|---|
| 1 | Host nhiều agent | Process tạo N `AgentRuntime` theo cấu hình phòng ban. Dùng chung một Postgres có pgvector (PGlite khoá theo agent). Mỗi agent một bot Telegram, tái dùng `TelegramService`. Healthcheck, khởi động lại | 1–2 tuần |
| 2 | Sơ đồ tổ chức (D1) | `settings.extra.org = {title, department, reportsTo, skills}`. Provider `ORG_CHART` luôn chèn (`alwaysInResponseState`). Registry agent dùng chung trong host | 3–5 ngày |
| 3 | Giao việc + người yêu cầu (5d) | Action `DELEGATE_TO_AGENT` chọn agent theo role/department, gọi `target.messageService.handleMessage` với `metadata.onBehalfOf = {platform, platformUserId, name, sourceAgent, sourceRoom}`. Provider `REQUESTER_CONTEXT` ở agent đích. Callback trả kết quả về phòng gốc. Chống vòng lặp (giới hạn ping-pong) | 1–2 tuần |
| 4 | Task, phân rã, review/duyệt (D1) | Bảng task riêng (component hoặc bảng SQL plugin), trạng thái `todo/doing/review/approved/rejected`. Leader phân rã bằng LLM (action). Reviewer là agent hoặc admin qua chat. Tận dụng `ApprovalService` nếu phù hợp (chưa kiểm chứng) | 2–3 tuần |
| 5 | Kho tri thức chung (K1) | Hoặc (a) plugin KB riêng: bảng tài liệu và vector có `department_id`, provider tự chèn cho mọi role (bỏ qua quy tắc owner-only), nạp qua thư mục/upload/URL; hoặc (b) nạp cùng một nguồn vào từng agent, rồi cấp `directGrantEntityIds` cho từng người (không mở rộng được vì UUID theo agent). Khuyến nghị (a) | 1–2 tuần |
| 6 | Vai trò mặc định cho nhân viên | Nhân viên trong allowlist (Telegram id) được USER tự động, nếu không thì mọi người là GUEST và mất `memory/documents/knowledge`. Dùng hook hoặc plugin gán `roles` trong world lúc tạo phòng | 2–4 ngày |
| 7 | Riêng tư theo ngữ cảnh + ngoại lệ admin (K4) | Override `FACTS`: không đưa fact học trong DM vào lượt ở nhóm; chỉ dùng cụm `getVerifiedRelatedEntityIds`. Thêm bảng "grant" do admin tạo qua chat (X cho phép Y xem nhóm fact Z) và provider tôn trọng grant. Giới hạn `MESSAGE read_*` cho ADMIN nếu cần | 1–2 tuần |
| 8 | Admin hệ thống bind qua chat (K5) | Giữ `connectorAdmins` theo ID nền tảng (đã chạy đúng), đồng bộ cho mọi agent từ cấu hình host. Nếu cần bind hoàn toàn trong chat: lệnh `/bind_admin <code>` với mã phát từ CLI của host (tương tự `OwnerBindingService`) | 3–5 ngày |
| 9 | Danh tính dùng chung giữa agent (5b giữa agent) | Bảng `person` của host (khoá `telegram:1001`, `zalo:…`), đồng bộ `identity_link` đã xác minh vào từng agent | 1 tuần |
| 10 | Zalo (R6) | Port `plugin-zalo` (OA, chỉ DM) hoặc `plugin-zalouser` (zca-cli, không chính thức) từ alpha.6 sang API connector hiện tại. Khoá entity `${accountId}:${userId}` | 1–3 tuần |
| 11 | Bám `develop` | Ghim commit, vendor monorepo đã cắt gọn, test hồi quy bằng stub (như harness này), rebase định kỳ | liên tục, ~2–4 ngày/tháng (ước lượng) |

Tổng MVP (1–10): khoảng 9–15 tuần công, tức 2–3 người-tháng. Đây là ước lượng suy luận, chưa kiểm chứng.

### Rủi ro đáng chú ý
- **Bám `develop`:**
  - Lịch sử nhánh bị viết lại ngày 2026-06-18 ("clean baseline"), nên fork cũ mất liên tục lịch sử.
  - Tốc độ ~3.000–5.000 commit first-parent mỗi tháng (tháng 7–8), cộng mega-refactor 2026-09-25/26 gộp package ("lean Node-only runtime, consolidate packages").
  - Plugin tự viết sẽ vỡ theo API nội bộ (ví dụ `messageService`, `contextGate`, cấu trúc Stage 1). Không có semver hay CHANGELOG.
  - npm không phát hành từ 2026-06-28.
- **Hướng sản phẩm ngược nhu cầu:** OS/mobile/wallet/cloud chiếm phần lớn commit. Tính năng doanh nghiệp đa người dùng (tenant, phòng ban) chỉ có trên Eliza Cloud (dịch vụ hosted).
- **Bus factor:** ~59% commit từ một người (Shaw/lalalune). Rất nhiều commit do agent AI tạo (369 commit "Claude Fable 5", workflow "Claude Code" chạy liên tục).
- **Kích thước và công cụ:** 29.296 file, 749 MB (blobless). Ghim bun 1.4.2 và Node 24.15.0. Postinstall build nhiều thứ (inference, views). Bản cài tối thiểu 6 package vẫn là 629 gói, 385 MB.
- **Chi phí token:** 2–7 lời gọi LLM mỗi tin, prompt evaluator hậu lượt ~15 nghìn ký tự. Có thể tách model cho evaluator: commit `#32829` "feat(assistant): add opt-in evaluator-only model selection" (2026-09-27) [MÃ git].
- **Bảo mật:**
  - Tốt: mặc định GUEST (fail-closed), vai trò theo ID nền tảng, bọc nội dung `EXTERNAL_UNTRUSTED_CONTENT`.
  - Rủi ro: ADMIN nhận quyền rất rộng (`MESSAGE` đọc hộp thư/kênh, `CHARACTER`, `settings`, `connectors`, `files`, `email`). Monorepo kèm wallet, computer-use, terminal (OWNER). Cảnh báo `SECRET_SALT` tạm thời khi không đặt (thấy trong log). Fact hiện chéo DM→nhóm (K4).
- **Giấy phép:** MIT cho mã. Các model local (Eliza-1 dựa trên Gemma 4) có giấy phép riêng, chưa kiểm chứng. Ghi chú trước từng thấy `plugins/plugin-slack/LICENSE` là JSON lỗi (chưa kiểm lại ở HEAD).

### Gaps
- Ước lượng công là suy luận, chưa có prototype cho lớp phòng ban.
- Chưa kiểm `ApprovalService` có dùng được cho luồng review giữa agent hay không.
- Dọn dẹp: stub (cổng 18114) đã dừng. Đã xoá clone, `node_modules` và thư mục dữ liệu PGlite dưới `scratchpad/verify2/elizaos`. Cache cài đặt bun dùng chung (`/root/.bun/install/cache`, 2,5 GB) được giữ lại vì không phải clone hay data của riêng nghiên cứu này.
