# elizaOS — nhận diện cùng một người dùng qua nhóm/DM/kênh và mô hình vai trò agent (kiểm chạy thật với stub LLM, 2026-09-27)

Phạm vi: yêu cầu đã sửa ngày 2026-09-27 (chức danh/phòng ban là của AGENT; người dùng chỉ là "user A"). Ba bản được kiểm, vì chúng hành xử khác nhau rất nhiều:

| Ký hiệu | Bản | Nguồn | Cách kiểm |
|---|---|---|---|
| **S1** | 1.7.2 — dist-tag `latest` (bản ổn định cuối), 2026-01-19 | npm `@elizaos/core@1.7.2`, `plugin-bootstrap@1.7.2`, `plugin-sql@1.7.2`, `plugin-openai@1.6.0`, `plugin-telegram@1.6.4` | [CHẠY] Node 22 |
| **B7** | 2.0.3-beta.7 — dist-tag `beta`, 2026-06-28 | npm `@elizaos/core|plugin-sql|plugin-openai|plugin-telegram@2.0.3-beta.7` | [CHẠY] Node 22 |
| **DEV** | nhánh `develop` commit `eb157cac4767dfc0268f6995e09de109d8468ff8` (2026-09-26), chưa phát hành npm | mã nguồn TS chạy thẳng bằng bun 1.3.11 `--conditions=eliza-source` (core, plugin-assistant, plugin-sql, plugin-openai, MessageManager của plugin-telegram) | [CHẠY] |

Link mã DEV dưới đây dùng gốc `https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/`. Số dòng của S1/B7 là số dòng trong file dist của tarball npm (link unpkg trỏ tới đúng file).

## 0. Cách chạy, cách bơm tin nhắn, và các chỗ lệch khỏi đường production

### Takeaway
Cả ba bản đều chạy được đến tầng LLM với stub. Tin nhắn được bơm qua **adapter Telegram thật của elizaOS** (S1: Telegraf poll từ Bot API giả; B7/DEV: gọi thẳng `MessageManager.handleMessage` với `telegraf.Context` thật dựng từ update giả, vì B7 có lỗi làm handler không bao giờ được gắn). Không dùng bot token hay tài khoản thật nào.

### Cited Findings
- Stub LLM: bản gốc `stub_llm.py` chạy cổng 18081 cho S1 và B7. Riêng DEV dùng **bản sao** `stub_llm_tpl.py` (thêm đúng một tính năng: thay `{{MSGID}}` trong reply bằng nhóm bắt regex từ request), vì evaluator `factMemory` của DEV bắt buộc `sourceMessageIds` phải trỏ đúng ID tin nhắn — [reflection-items.ts#L1516-L1530](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/evaluators/reflection-items.ts#L1516-L1530) [CHẠY]
- Bot API giả (`fake_tg.py`, cổng 18781): trả `getMe`, `deleteWebhook`, `getUpdates` (lấy từ hàng đợi), `sendMessage`, `sendChatAction`, `getChatAdministrators`, `getChat`. S1 trỏ `TELEGRAM_API_ROOT` vào đây — plugin 1.6.4 đọc biến này ở `dist/index.js:878-881` — [unpkg plugin-telegram@1.6.4](https://unpkg.com/@elizaos/plugin-telegram@1.6.4/dist/index.js) [CHẠY]
- Kịch bản: agent 1 "Content Lead" (bio/system: "Content Lead – Phòng Marketing… Cấp dưới: Copywriter"), agent 2 "Copywriter", chạy chung một process. A = Telegram id 1001 "Lan"/`lan_mkt`; B = 1002 "Minh"/`minh_mkt`; C = 1003 "Hoa" (chỉ dùng ở vòng 2). G1 = chat -100111 "G1 Marketing", G2 = -100222 "G2 KPI". Các bước: G1(A), G1(B), G2(A), DM(A) hỏi, DM(B) hỏi, G2(A) hỏi lại (đối chứng), DM(A) "Giao Copywriter viết 3 caption"; vòng 2: DM(A)→agent 1, DM(B)→agent 1, DM(A)→agent 2, DM(C)→agent 2 [CHẠY]
- Lệch khỏi production, S1: (1) phải tự tạo adapter và chạy migration plugin-sql **trước** `runtime.initialize()` vì 1.7.2 gọi `ensureAgentExists` trước migration (bảng `agents` chưa có → crash; server 1.7.2 làm việc này hộ) — `core dist/node/index.node.js:49074-49110`, [unpkg core@1.7.2](https://unpkg.com/@elizaos/core@1.7.2/dist/node/index.node.js); (2) `conversationLength: 4` để evaluator REFLECTION chạy sau ≥2 tin (mặc định 32 → chờ >8 tin/phòng) — `plugin-bootstrap dist/index.js:5071-5090`, [unpkg plugin-bootstrap@1.7.2](https://unpkg.com/@elizaos/plugin-bootstrap@1.7.2/dist/index.js) [CHẠY]
- Lệch, B7: `plugin-telegram@2.0.3-beta.7` làm `await bot.launch(...)` (`dist/index.js:3608`) với Telegraf 4.16.3, mà `launch()` của Telegraf 4.16 chỉ resolve khi polling DỪNG → `setupMiddlewares()/setupMessageHandlers()` không bao giờ chạy: update được giao (log Bot API giả ghi `getUpdates delivered [1]`) nhưng không có request LLM nào — [unpkg plugin-telegram@2.0.3-beta.7](https://unpkg.com/@elizaos/plugin-telegram@2.0.3-beta.7/dist/index.js). DEV đã sửa và ghi rõ nguyên nhân trong comment — [service.ts#L969-L981](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-telegram/src/service.ts#L969-L981) [CHẠY + MÃ]
- Lệch, B7/DEV: mặc định kết nối ở chế độ "passive" (LifeOps): `lifeOpsPassiveConnectorsEnabled()` trả `true` khi không cấu hình, nên tin Telegram chỉ được lưu, không trả lời, trừ khi `ELIZA_LIFEOPS_PASSIVE_CONNECTORS=false` **và** `TELEGRAM_AUTO_REPLY=true` — B7 `core dist/node/index.node.js:215060-215094`, `plugin-telegram dist/index.js:1720-1735`; DEV [messageManager.ts#L1821-L1834](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-telegram/src/messageManager.ts#L1821-L1834) [CHẠY + MÃ]
- Lệch, DEV: host `packages/agent` không dùng được cho hai agent (xem §5), nên harness tự dựng hai `AgentRuntime` với đúng bộ plugin mà host dùng (`createAssistantPlugin()` + dịch vụ relationships) — [assistant-plugins.ts#L23-L40](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/runtime/assistant-plugins.ts#L23-L40). PGlite của DEV khoá thư mục dữ liệu theo agent (`getOrCreatePgliteManagerForAgent`), nên mỗi agent phải có một thư mục DB riêng — [plugin-sql/src/index.ts#L229-L232](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-sql/src/index.ts#L229-L232) (lần chạy đầu với thư mục chung báo `PGlite lock file is held by running process`) [CHẠY]
- Luồng model của từng bản (quan sát từ request thu được): S1 = XML qua OpenAI Responses API (`shouldRespond` → `messageHandlerTemplate` → REPLY → REFLECTION). B7/DEV = Chat Completions có tool: Stage 1 `HANDLE_RESPONSE` (tool_choice required, có sẵn trường `facts`, `relationships`) → planner (`DISCOVER_ACTIONS`/`REPLY`) → evaluator hậu lượt dạng `json_schema` (`factMemory`, `relationships`, `identities`…) [CHẠY]

### Inferences
- Với B7, "cài từ npm rồi chạy bot Telegram" không nhận được tin nhắn nào ở chế độ polling. Đây là tín hiệu chất lượng quan trọng cho R8: bản beta công khai mới nhất không dùng được cho kênh chính của kịch bản này.

### Gaps
- Không chạy host thật `packages/agent` (bun 1.4.2 + postinstall build toàn monorepo) và không chạy `@elizaos/server@1.7.2`. Kết luận về host/server là [MÃ].
- Evaluator của DEV chạy nền (TaskService, worker `POST_TURN_MEMORY`), nên fact chỉ có sau vài giây tới vài chục giây. Trong B7 có một lượt DM(A) hỏi khi fact chưa được ghi; vòng 2 chạy lại để loại yếu tố thời gian.

## 1. Mô hình Entity: A có phải MỘT entity ở G1, G2 và DM (cùng một agent, cùng Telegram) không?

### Takeaway
Có, ở cả ba bản [CHẠY]. ID entity chỉ phụ thuộc Telegram user id và agentId, không phụ thuộc chat. Nhưng mỗi agent có không gian entity riêng: cùng một A thì agent 2 thấy một UUID khác.

### Cited Findings
- `createUniqueUuid(runtime, base)` = `stringToUuid(\`${base}:${runtime.agentId}\`)` — [entities.ts#L90-L100](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/entities.ts#L90-L100) [MÃ]
- S1 (`plugin-telegram@1.6.4`): `entityId = createUniqueUuid(runtime, ctx.from.id)`, `roomId = createUniqueUuid(runtime, chat.id)`; không có nhánh riêng cho DM hay group — `dist/index.js:580-616`, [unpkg](https://unpkg.com/@elizaos/plugin-telegram@1.6.4/dist/index.js) [MÃ]. Chạy thật: tin của A ở G1, G2 và DM đều mang entity `0ffd6650-b23d-030e-805b-674e1bf0bf62`, và `getRoomsForParticipant(A)` trả về 3 phòng [CHẠY]. Có một điểm lạ: phòng DM của A cũng có id `0ffd6650…`, trùng với entity id, vì cả hai đều băm từ chuỗi "1001" [CHẠY]
- DEV: `resolveTelegramRuntimeEntityId` = `createUniqueUuid(runtime, \`${accountId}:${telegramUserId}\`)`, trừ khi user là owner đã ghép cặp — [identity.ts#L68-L95](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-telegram/src/identity.ts#L68-L95); phòng/world theo chat id — [messageManager.ts#L1540-L1568](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-telegram/src/messageManager.ts#L1540-L1568) [MÃ]. Chạy thật: A = `431eff90-6688-0b5d-9cce-5714375f8d63` ở cả G1, G2 và DM của agent 1. Ở agent 2 (Copywriter), A = `a9c44d27-37f3-0eb3-be1b-264f22fe10ed` [CHẠY]
- B7: `entityId = createUniqueUuid(runtime, scopedTelegramKey(userId))`, với tài khoản "default" thì key chính là "1001" — `dist/index.js:1577-1594`, [unpkg](https://unpkg.com/@elizaos/plugin-telegram@2.0.3-beta.7/dist/index.js) [MÃ]. Chạy thật: A = `0ffd6650…` ở mọi phòng [CHẠY]

### Inferences
- Trong một agent, 5b-in chỉ còn là chuyện trí nhớ có được lưu và truy xuất theo entity hay không. Việc định danh A ở tầng entity đã đúng (xem §2).
- Vì UUID gắn với agentId, "A của agent 1" và "A của agent 2" là hai bản ghi không nối với nhau. Điều này quyết định kết quả của 5d (§5).

### Gaps
- Không kiểm Discord/Slack. Theo mẫu chung, các plugin dùng cùng `createUniqueUuid(runtime, platformUserId…)` (chưa kiểm chứng từng plugin).

## 2. Agent tự động thấy gì về người gửi (5a), và điều nó học về A ở G2 có được đưa vào khi A hỏi trong DM không (5b-in)

### Takeaway
- **S1:** Không. Đường ghi fact bị hỏng (REFLECTION không bao giờ lưu được fact). Ngay cả khi có fact, FACTS vẫn lọc theo phòng và chỉ chạy khi model tự chọn provider này.
- **B7:** fact được lưu theo người và tự động vào prompt Stage 1. Nhưng truy vấn không lọc theo người, nên thực chất là "đưa mọi fact vào mọi lượt" (§3).
- **DEV:** **Đạt**. Fact lưu theo người (entityId + agentId). Khi Stage 1 định tuyến sang context `general`, FACTS được tự chèn vào prompt planner với tiêu đề "Things Content Lead knows about the speaker"; model không phải gọi tool tìm kiếm. DM(A) thấy cả fact từ G1 lẫn G2 [CHẠY].

### Cited Findings
**5a — định danh người gửi trong prompt**
- S1: prompt có "# People in the Room" với `"Lan" aka "lan_mkt"` và `ID: 0ffd6650…` (UUID), dòng hội thoại dạng `[0ffd6650…] Lan: …`. Không có Telegram id 1001, không có tên nhóm "G1 Marketing", không ghi nguồn "telegram". Loại kênh chỉ lộ gián tiếp qua đoạn chữ của provider ANXIETY cho DM. Metadata entity được lưu chỉ là `{"telegram": {}}` [CHẠY]
- B7: prompt Stage 1 **không có** tên hay ID người gửi, cũng không có kênh. Tin nhắn bị bọc thành `SECURITY NOTICE … <<<EXTERNAL_UNTRUSTED_CONTENT>>> Source: API --- <văn bản>`; tên "Lan" chỉ xuất hiện vì chính A tự giới thiệu. "People in the Room" và "Sender entity ID" chỉ có trong prompt evaluator hậu lượt [CHẠY]
- DEV: Stage 1 và planner đều có "# People in the Room" (tên + username + UUID). "Current message" là JSON có `"source":"telegram"` và `"channelType":"GROUP"|"DM"`. Planner có thêm dòng `World: -100111; current channel: G1 Marketing (GROUP), participants=3`; trong DM là `World: 1001; current channel: Lan (DM)` [CHẠY]

**5b-in — trí nhớ theo người hay theo phòng**
- S1, đường ghi: REFLECTION ghi fact với **`entityId: agentId`** (ID của chính agent, không phải người nói) và `roomId` là phòng hiện tại — `plugin-bootstrap@1.7.2 dist/index.js:4999-5005`, [unpkg](https://unpkg.com/@elizaos/plugin-bootstrap@1.7.2/dist/index.js) [MÃ]
- S1, đường ghi bị hỏng: evaluator đọc `reflection.facts.fact`, nhưng `parseKeyValueXml` của core 1.7.2 chỉ phân tích XML phẳng, nên `facts` là một chuỗi và `.fact` là `undefined` → `factsArray = []` — `core dist/node/index.node.js:45108-45215`, `plugin-bootstrap dist/index.js:4995-4998` [MÃ]. Chạy thật với reply đúng định dạng mẫu `<facts><fact><claim>…` ở G1 và G2: bảng `facts` vẫn **rỗng** sau vòng 1, log ghi `Getting reflection failed - invalid facts structure` [CHẠY]
- S1, đường đọc: FACTS là `dynamic: true`, và cả hai truy vấn `searchMemories` đều có `roomId: message.roomId` — `plugin-bootstrap dist/index.js:5991-6024` [MÃ]. Provider dynamic bị loại khỏi `composeState` mặc định (`!p.private && !p.dynamic`, `core dist/node/index.node.js:49914`); chỉ vào prompt khi model liệt kê `FACTS` trong `<providers>` (theo luật "If the message asks about facts… include FACTS", `:46532-46539`) [MÃ]
- S1, vòng 2: chèn thẳng fact đúng hình dạng mà REFLECTION ghi (entityId=agentId, roomId=G1/G2), thêm một biến thể gắn theo người (entityId=A, roomId=G2). Kết quả: DM(A) "KPI của mình bao nhiêu?" → prompt REPLY ghi **"No facts available."**; G2(A) cùng câu hỏi → `Key facts that Content Lead knows: (person-keyed) Lan muốn nhận báo cáo KPI mỗi thứ Hai / KPI tháng 10 của Lan là 50 bài` [CHẠY]
- S1: RECENT_MESSAGES có lấy `recentInteractions`, tức tin nhắn ở **mọi phòng khác** mà A và agent cùng tham gia (limit 20) — `dist/index.js:6118-6143`. Nhưng dữ liệu này chỉ nằm trong `values` và không template mặc định nào dùng `{{recentInteractions}}` [MÃ]; prompt DM(A) không chứa câu nào từ G1/G2 [CHẠY]
- B7: fact hậu lượt ghi với `entityId: ctx.message.entityId` (người nói) và `roomId` phòng gốc — `core@2.0.3-beta.7 dist/node/index.node.js:192821-192845`, [unpkg](https://unpkg.com/@elizaos/core@2.0.3-beta.7/dist/node/index.node.js) [MÃ]. Chạy thật: 4 fact (3 của A, 1 của B) mang đúng entity người nói [CHẠY]. FACTS có trong prompt Stage 1 (`provider:FACTS:`) mà model không phải chọn [CHẠY]
- DEV, đường ghi (evaluator `factMemory` chạy nền): `insertFact` ghi `entityId: ctx.message.entityId, agentId, roomId` — [reflection-items.ts#L871-L912](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/evaluators/reflection-items.ts#L871-L912). Đường Stage 1 gán fact cho **chủ thể được giải tên** trong phòng, không mặc định cho người nói — [facts-and-relationships.ts#L780-L833](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/runtime/facts-and-relationships.ts#L780-L833) [MÃ]
- DEV, đường đọc: FACTS lấy hai nhóm. (1) Nhóm phòng: `roomId` + `worldId`. (2) Nhóm theo người: cho mỗi entity trong cụm danh tính của người gửi (`getRelatedEntityIds`), truy vấn `entityId`, `authorEntityIds: [entityId]`, `agentId: runtime.agentId`; **không lọc theo phòng**. Tiêu đề "Things X knows about <sender>" chỉ dùng cho fact thuộc cụm người gửi — [facts.ts#L344-L422](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L344-L422), [#L505-L521](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L505-L521) [MÃ]. plugin-sql DEV áp `authorEntityIds` thành `inArray(memoryTable.entityId, …)` — [base.ts#L3395-L3402](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-sql/src/base.ts#L3395-L3402) [MÃ]
- DEV, chạy thật. Bảng facts: `KPI tháng 10 của Lan là 50 bài` (entity A, phòng G2), `Lan phụ trách fanpage X` và `Lan thích giọng văn hài hước` (entity A, phòng G1), `Minh là thành viên nhóm G1` (entity B, phòng G1). Prompt planner khi A hỏi trong DM [CHẠY]:
  ```
  # People in the Room
  Content Lead  ID: 4bb9216b-…
  Lan aka lan_mkt  ID: 431eff90-6688-0b5d-9cce-5714375f8d63
  Standing preferences the speaker has expressed (apply any that are relevant to this reply):
  [durable.preference conf=0.70] Lan thích giọng văn hài hước
  Things Content Lead knows about the speaker:
  [durable.goal conf=0.70] KPI tháng 10 của Lan là 50 bài
  [durable.business_role conf=0.70] Lan phụ trách fanpage X
  World: 1001; current channel: Lan (DM), participants=2; …
  ```
- DEV, điều kiện: FACTS có `contextGate: { anyOf: ["general"] }` — [facts.ts#L344-L352](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L344-L352). Prompt Stage 1 của DM(A) không có fact nào; fact chỉ vào prompt planner sau khi Stage 1 chọn `general` (trong lần chạy, stub trả `general` cho câu hỏi) [CHẠY]. Luật Stage 1 cấm dùng `simple` khi cần "private state, person lookup… memory" (thấy trong prompt Stage 1 của B7) [CHẠY]
- DEV, điều kiện ghi: evaluator hậu lượt chỉ được xếp lịch khi Stage 1 trích được fact, hoặc lượt không phải trả lời đơn giản, hoặc tin khớp regex **tiếng Anh** `POST_TURN_SEMANTIC_SIGNAL` (`i am|my|remember|goal…`) — [post-turn-policy.ts#L22-L38](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/services/message/post-turn-policy.ts#L22-L38) [MÃ]

### Inferences
- Theo thang của đề bài, DEV xếp vào **"tự động"**: không cần tool tìm trí nhớ, và kết quả gắn theo người. Nhưng tính tự động phụ thuộc quyết định định tuyến của Stage 1 (`general` so với `simple`).
- Với tiếng Việt, nếu Stage 1 của model thật không điền `facts` thì regex tiếng Anh sẽ không kích hoạt trích xuất hậu lượt. Đây là rủi ro bỏ sót fact cần kiểm thêm với model thật (chưa kiểm chứng).
- S1 tuy có entity đúng theo người, nhưng đường trí nhớ fact thực tế không hoạt động. Muốn 5b-in thì phải tự viết lại evaluator/provider.

### Gaps
- Chưa chạy với LLM thật nên chưa biết tỷ lệ Stage 1 chọn `general` cho các câu kiểu "bạn biết gì về mình".
- Không kiểm provider "long-term memory"/documents khác của DEV (ví dụ `advancedMemory`).

## 3. Riêng tư: fact của A có lọt sang cuộc trò chuyện của B không

### Takeaway
- **S1:** không lọt giữa các DM, vì fact theo phòng. Trong nhóm, fact của phòng hiện với mọi người trong phòng.
- **B7:** **rò rỉ nặng** [CHẠY]. Mọi fact trong DB hiện ra với mọi người nói, kể cả người mới hoàn toàn, và với cả agent khác dùng chung DB. Tất cả lại bị gắn nhầm là "about the speaker".
- **DEV:** không lọt giữa các DM hay giữa các agent [CHẠY]. Còn hai rủi ro ngữ cảnh: fact của A (kể cả học trong DM) hiện ra khi A nói trong nhóm; và fact phòng của người khác hiện dưới tiêu đề riêng.

### Cited Findings
- B7, nguyên nhân: FACTS truy vấn `getMemories({tableName:"facts", entityId, count})` — `core@2.0.3-beta.7 dist/node/index.node.js:194226-194240`. Nhưng `getMemories` của plugin-sql beta.7 **không thêm điều kiện `entityId`**; `entityId` chỉ được dùng làm ngữ cảnh RLS — `plugin-sql@2.0.3-beta.7 src/dist/node/index.node.js:5555-5580`, [unpkg](https://unpkg.com/@elizaos/plugin-sql@2.0.3-beta.7/src/dist/node/index.node.js). Adapter PGlite bỏ qua hẳn entityId (`withEntityContext(_entityId, cb)`, `:8170-8172`); adapter Postgres chỉ đặt `app.entity_id` khi `ENABLE_DATA_ISOLATION=true` (`:8117-8139`) [MÃ]. DEV ghi nhận đúng lỗi này trong comment: "Live 2026-09-05 on a database without RLS policies, the principal-only query returned the entire facts table (127 rows from every Discord channel)…" — [facts.ts#L402-L420](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L402-L420) [MÃ]
- B7, chạy thật. Stage 1 khi **Minh** hỏi trong DM "Bạn biết gì về mình?" [CHẠY]:
  ```
  provider:FACTS:
  Things Content Lead knows about the speaker:
  [durable.identity conf=0.70] Minh là thành viên nhóm G1
  [durable.goal conf=0.70] KPI tháng 10 của Lan là 50 bài
  [durable.preference conf=0.70] Lan thích giọng văn hài hước
  [durable.business_role conf=0.70] Lan phụ trách fanpage X
  ```
  Danh sách y hệt xuất hiện khi **Hoa** (user mới 1003) nhắn DM cho **Copywriter**: "Things Copywriter knows about the speaker: … KPI tháng 10 của Lan là 50 bài …". Nghĩa là rò cả sang agent 2, người chưa từng nói chuyện với Lan [CHẠY]
- DEV, chạy thật. Minh hỏi trong DM → chỉ thấy `Things Content Lead knows about the speaker: [durable.identity] Minh là thành viên nhóm G1`. Lan nhắn DM cho Copywriter, và Hoa nhắn DM cho Copywriter → không có mục fact nào [CHẠY]
- DEV, trong nhóm: khi Minh nói ở G1, planner có `Known facts in this room (about other participants): … Lan thích giọng văn hài hước / Lan phụ trách fanpage X`. Đây là nhóm fact theo phòng: B thấy fact A đã nói trong **cùng** phòng G1 [CHẠY]. Khi A nói ở G2, planner hiện fact A học ở G1 ("Lan phụ trách fanpage X") dưới tiêu đề về người nói [CHẠY]. Suy ra: fact A kể trong DM cũng sẽ vào prompt khi A nói trong một nhóm có B, vì nhóm fact theo người không lọc phòng. Lớp che duy nhất là `shouldMinimizePrivateFactsForTurn`, và nó chỉ áp cho câu hỏi lịch/sẵn sàng liên quan bên thứ ba — [facts.ts#L205-L228](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L205-L228) [MÃ; phần DM→nhóm chưa chạy]
- DEV, cụm danh tính dùng cho FACTS là `getRelatedEntityIds`. Hàm này gộp cả liên kết `identity_link` đã xác nhận **lẫn** các entity trùng cặp (platform, handle) trong `entity_identities` (liên kết suy ra, chưa xác minh). Bản "verified" (`getVerifiedRelatedEntityIds`) có tồn tại nhưng FACTS không dùng — [identity-clusters.ts#L50-L90](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/identity-clusters.ts#L50-L90), [relationships.ts#L2855-L2876](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/services/relationships.ts#L2855-L2876) [MÃ]

### Inferences
- Không được đưa B7 (npm beta) vào môi trường có nhiều người dùng.
- Với DEV, nếu B tự nhận handle của A đủ nhiều lần để kích hoạt auto-merge (§4), B có thể kéo được fact của A. Đây là giả thuyết từ mã, chưa kiểm chứng bằng chạy.

### Gaps
- Chưa chạy trường hợp "A kể điều riêng tư trong DM, sau đó nói trong nhóm có B" với DEV.
- Chưa kiểm B7/DEV trên Postgres có bật `ENABLE_DATA_ISOLATION` (RLS).

## 4. Liên kết đa kênh (5b-cross): A trên Telegram với A trên Discord/web/Zalo

### Takeaway
DEV có đủ máy móc: PrincipalService/IdentityClaim, API person-link cho OWNER/ADMIN, ứng viên gộp, và **auto-merge** khi cùng (platform, handle) xuất hiện với độ tin ≥0.85 và ≥2 bằng chứng. Sau khi gộp, FACTS tự mở rộng sang cả cụm, nên trí nhớ được hợp nhất trong ngữ cảnh [MÃ]. Không có luồng tự nhận bằng mã xác minh cho người dùng thường; chỉ owner có ghép cặp `/eliza_pair`. Liên kết chỉ có hiệu lực trong phạm vi một agent. Chưa chạy.

### Cited Findings
- Kiểu dữ liệu: `Principal`, `IdentityClaim{namespace, connectorId, externalSubjectId, handle, verification: unverified|observed|verified|owner_bound, status, confidence…}`, `abstract class PrincipalService` — [types/identity.ts#L1-L80](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/identity.ts#L1-L80) [MÃ]
- Đường quản trị: `POST /api/identity/person-links/attest` và `/verify`, chỉ cho vai trò `OWNER`/`ADMIN` (sai vai trò trả 403 `IDENTITY_PERSON_LINK_AUTHORITY_REQUIRED`) — [identity-person-link-routes.ts#L21-L22](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/api/identity-person-link-routes.ts#L21-L22), [#L62-L69](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/api/identity-person-link-routes.ts#L62-L69) [MÃ]
- Auto-merge: `upsertIdentity` ghi bằng chứng; nếu (platform, handle) đã gắn với entity khác và `confidence >= 0.85` với `>= 2` message bằng chứng thì gọi `proposeMerge` rồi `acceptMerge` ngay — [relationships.ts#L464-L465](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/services/relationships.ts#L464-L465), [#L2085-L2124](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/services/relationships.ts#L2085-L2124) [MÃ]. Nguồn handle là evaluator hậu lượt `identities` (`{entityId, platform, handle, confidence, sourceMessageId}`, thấy trong schema của request thu được); prompt yêu cầu "confidence 0-1: higher for self-claims" [CHẠY — schema và prompt; auto-merge chưa chạy]
- Cụm dùng cho trí nhớ: FACTS gọi `getRelatedEntityIds(runtime, message.entityId)` rồi truy vấn fact của từng thành viên cụm, lọc theo `agentId` — [facts.ts#L364-L420](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L364-L420) [MÃ]
- S1 có action `UPDATE_CONTACT` với mô tả "This is for the agent to relate entities across platforms", thấy trong danh sách action của prompt [CHẠY — chỉ quan sát mô tả]. Không có cơ chế gộp trí nhớ tương ứng (chưa kiểm chứng sâu).
- Trên server 1.7.2 (web/central bus), entity của người dùng là `author_id` thô, **không** băm theo agent (`ensureAuthorEntityExists` tạo entity với `id: message.author_id`) — `@elizaos/server@1.7.2 dist/index.js:28607-28621`, [unpkg](https://unpkg.com/@elizaos/server@1.7.2/dist/index.js) [MÃ]

### Inferences
- Liên kết Telegram với Discord/web khả thi trên DEV qua API admin, không cần fork. Nhưng phải làm riêng cho **từng** agent, vì cụm và fact đều lọc theo `agentId`.
- Auto-merge dựa trên việc người dùng tự khai handle (không có mã xác minh). Với mục tiêu riêng tư, nên tắt tính năng này hoặc đặt sau bước xác minh.

### Gaps
- Chưa chạy liên kết đa kênh (không có kênh thứ hai sẵn trong harness).
- Chưa rõ `upsertExtractedIdentity` đếm bằng chứng thế nào qua nhiều lượt ("one original assertion is one observation").

## 5. Nhiều agent và ủy quyền (5d): agent 2 có biết mình làm việc cho A không

### Takeaway
Không bản nào có cơ chế agent eliza giao việc cho agent eliza khác kèm danh tính người yêu cầu. S1: action SEND_MESSAGE thất bại và Copywriter không nhận được gì [CHẠY]. DEV: khoá cấu hình `agentToAgent` có khai báo nhưng không có mã nào dùng. Orchestrator chỉ spawn coding-agent qua ACP; `userId` của người yêu cầu chỉ nằm trong metadata phiên [MÃ]. Nhiều agent trong một process: S1 có lớp `ElizaOS`/server; host DEV chỉ chạy `agents.list[0]`.

### Cited Findings
- S1 chạy thật: DM(A) "Giao Copywriter viết 3 caption cho fanpage X nhé.", stub trả `<actions>REPLY,SEND_MESSAGE</actions>` và mục tiêu `copywriter_bot@telegram`. Kết quả: bot trả lời A "I couldn't find the user you want me to send a message to…", bộ nhớ ghi "Target user not found"; **0** request LLM nào mang persona Copywriter [CHẠY]. SEND_MESSAGE chỉ nhắm "a user or room" trên một nền tảng — `plugin-bootstrap@1.7.2 dist/index.js:2263-2420` [MÃ]
- S1 hỗ trợ nhiều agent trong một process: `class ElizaOS` có `addAgents`, `registerAgent`, `handleMessage(agentId, …)` — `core@1.7.2 dist/node/index.node.js:51553-51760` [MÃ]; harness chạy 2 agent bằng đúng lớp này [CHẠY]. Server 1.7.2 khởi động nhiều agent (`startAgents`); agent nào là participant của một channel central bus thì nhận mọi tin trong channel đó, trừ tin do chính nó viết (`validateNotSelfMessage`) — `@elizaos/server@1.7.2 dist/index.js:21952-21965, 28573-28680` [MÃ]
- B7/DEV không còn lớp `ElizaOS` (import trả `undefined` ở B7 [CHẠY]; không tìm thấy `class ElizaOS` trong `packages/core/src` của DEV [MÃ]). Host DEV đọc `config.agents?.list?.[0]` — [build-character-config.ts#L40](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/runtime/build-character-config.ts#L40), [plugin-collector.ts#L80](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/runtime/plugin-collector.ts#L80), [first-time-setup.ts#L280](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/runtime/first-time-setup.ts#L280) [MÃ]
- DEV: `agentToAgent?: { enabled?: boolean; allow?: string[] }` ("Enable agent-to-agent messaging tools. Default: false") — [types.tools.ts#L379-L384](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/config/types.tools.ts#L379-L384). Grep toàn repo (`*.ts`, `*.tsx`) chỉ thấy khoá này trong file type/schema/config, không có nơi đọc nó [MÃ]
- DEV: `plugin-agent-orchestrator` "spawning and orchestrating coding sub-agents via the Agent Client Protocol (ACP)" (adapter elizaos, pi-agent, claude, codex, kimi, grok) — [README](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-agent-orchestrator/README.md). Khi spawn, `userId: message.entityId` được đặt vào `metadata` của phiên, cạnh `roomId`, `worldId`, `messageId` — [tasks.ts#L1150-L1160](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-agent-orchestrator/src/actions/tasks.ts#L1150-L1160) [MÃ; chưa kiểm chứng việc prompt của agent con có chứa danh tính A hay không]
- DEV/B7 chạy thật: Copywriter nhận DM từ Lan → "People in the Room: Lan aka lan_mkt ID: a9c44d27…" (ID khác với ở agent 1), không có fact nào về Lan (DEV). Agent 2 không có đường nào biết những gì agent 1 đã học [CHẠY]

### Inferences
- 5d phải tự xây: một action "giao việc" chuyển tin sang runtime của agent 2 (`runtime.messageService.handleMessage`), kèm khối "yêu cầu thay mặt A" (tên, ID nền tảng, fact đã chọn) được một provider của agent 2 đưa vào prompt.
- Trên server 1.7.2, cách gần nhất là cho A và hai agent vào **cùng** một channel central bus. Agent 2 sẽ thấy tin của A và "lệnh" của agent 1 trong lịch sử phòng. Đó là hội thoại chung, không phải ủy quyền (chưa kiểm chứng bằng chạy).

### Gaps
- Chưa chạy `@elizaos/server@1.7.2` với channel có nhiều agent.
- Chưa đọc hết `packages/cloud/services/agent-server` (đa agent bản cloud).

## 6. R2': vai trò/chức danh/phòng ban của AGENT

### Takeaway
Không có cấu trúc tổ chức cho agent. "Content Lead – Phòng Marketing" chỉ là chữ tự do trong `bio`/`system`, được chèn nguyên văn vào prompt và không dùng cho định tuyến hay ủy quyền [MÃ + CHẠY]. Vai trò OWNER/ADMIN/MEMBER/GUEST là của **người dùng** trong một World, không phải của agent.

### Cited Findings
- `Character` gồm `name, username, system, templates, bio, postExamples, topics, adjectives, plugins, settings, secrets, messageExamples, documents, knowledge, style, advancedPlanning, advancedMemory`. `CharacterSettings` có `extra?: JsonObject`. Không có trường role/title/department/reportsTo — [types/agent.ts#L24-L98](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/agent.ts#L24-L98) [MÃ]. Grep "department" trong `packages/core/src`, `packages/agent/src`, `plugins/plugin-assistant/src` không có kết quả [MÃ]
- Chạy thật (cả 3 bản): prompt chỉ chứa `[system] Bạn là Content Lead (chức danh) của Phòng Marketing (phòng ban). Cấp dưới: Copywriter.` và `# About Content Lead / Content Lead – Phòng Marketing…`. Không có khối tổ chức, không có danh sách đồng nghiệp hay action giao việc tương ứng [CHẠY]
- Mọi prompt ở B7/DEV có `user_role: GUEST` / `# User Role GUEST`, tức vai trò của người gửi. Các gate `roleGate {minRole}` áp lên action/provider theo vai trò người dùng trong World (ví dụ MESSAGE `roleGate: { minRole: "ADMIN" }`, FACTS `minRole: "USER"`) [CHẠY + MÃ, [facts.ts#L352](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/providers/facts.ts#L352)]
- Repo `elizaOS/the-org` ("Agents for organizations") trả 404 (ghi nhận ở vòng trước, chưa kiểm lại) [?]

### Inferences
- Có thể mô hình hoá R2' bằng `settings.extra` (ví dụ `org: {title, department, reportsTo, subordinates}`) cộng một provider và một action tự viết. Nền tảng không đọc các trường này.

### Gaps
- Không kiểm các template agent trong `packages/app` xem có preset "team" nào không.

## 7. Zalo

### Takeaway
Có `@elizaos/plugin-zalo` và `@elizaos/plugin-zalouser` trên npm, nhưng chỉ ở bản **2.0.0-alpha.6 (2026-02-17)**, không có trong cây mã `develop`, và chưa kiểm tương thích với core hiện tại. Giao diện chỉ còn giữ id connector `zalo`/`zalouser` [MÃ npm + repo].

### Cited Findings
- npm `@elizaos/plugin-zalo`: dist-tags `latest=2.0.0-alpha` (2026-02-06), `next=2.0.0-alpha.6` (2026-02-17); không có trường `repository`; maintainers `shawticus`, `odilitime`. Mã dùng Zalo OA Open API `ZALO_OA_API_BASE = "https://openapi.zalo.me/v2.0/oa"` (biến `ZALO_APP_ID`, `ZALO_SECRET_KEY`, `ZALO_ACCESS_TOKEN`, `ZALO_REFRESH_TOKEN`, webhook/polling), entity `createUniqueUuid(this.runtime, userId)` — [npm](https://www.npmjs.com/package/@elizaos/plugin-zalo), [unpkg dist](https://unpkg.com/@elizaos/plugin-zalo@2.0.0-alpha.6/dist/index.js) [MÃ]
- npm `@elizaos/plugin-zalouser` (2.0.0-alpha.6, 2026-02-17, repo `elizaos/eliza`): tài khoản cá nhân qua **spawn CLI `zca`** (`spawn(ZCA_BINARY, …)`, "zca-cli"), có action `ZALO_SHOW_GROUPS`, `ZALO_SEND…`, entity `createUniqueUuid(runtime, sender.id)`, room theo `threadId` — [npm](https://www.npmjs.com/package/@elizaos/plugin-zalouser), [unpkg dist](https://unpkg.com/@elizaos/plugin-zalouser@2.0.0-alpha.6/dist/index.js) [MÃ]
- Thư mục `plugins/` của DEV không có plugin zalo. Chỉ còn tham chiếu tên ở [connector-mode-registry.ts#L532-L540](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/ui/src/components/connectors/connector-mode-registry.ts#L532-L540) và [plugin-discovery-helpers.ts#L1157-L1204](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/api/plugin-discovery-helpers.ts#L1157-L1204) [MÃ]

### Inferences
- Zalo OA (plugin-zalo) chỉ phục vụ chat 1-1 với người theo dõi OA; nhóm cần plugin-zalouser, vốn dựa trên thư viện không chính thức (rủi ro khoá tài khoản; chưa kiểm chứng). Cả hai là điểm xuất phát để port, không dùng ngay được.

### Gaps
- Chưa cài hay chạy hai plugin Zalo với core 1.7.2 hoặc DEV.

## 8. Độ sống (R8) và kênh phát hành

### Takeaway
Bản ổn định cuối vẫn là 1.7.2 (2026-01-19). Beta công khai là 2.0.3-beta.7 (2026-06-28). Nhánh `develop` hoạt động mạnh (commit 2026-09-26), nhưng các bản sửa quan trọng về riêng tư và Telegram chưa lên npm. Trang GitHub Releases đang dùng làm kho ảnh bằng chứng CI, không phải release sản phẩm.

### Cited Findings
- npm `@elizaos/core`: `latest 1.7.2` (2026-01-19), `next 2.0.0-alpha.32` (2026-03-09), `alpha 2.0.0-alpha.537` (2026-05-04), `beta 2.0.3-beta.7` (2026-06-28); `@elizaos/server` và `@elizaos/cli` dừng ở `latest 1.7.2`, `alpha 1.7.3-alpha.4` (2026-02-08) — [registry @elizaos/core](https://registry.npmjs.org/@elizaos/core), [registry @elizaos/server](https://registry.npmjs.org/@elizaos/server) [MÃ registry]
- Tag git mới nhất `v2.0.3-beta.11` (2026-07-16, commit `d84b58ad`); `v2.0.11-beta.7` là tag cũ hơn (2026-06-20). Nhánh mặc định `develop` HEAD `eb157cac` (2026-09-26 19:43 -0700); `package.json` gốc `version 2.0.4`, `packageManager bun@1.4.2`; core beta.7 yêu cầu `node >=24` — [repo](https://github.com/elizaOS/eliza/tree/eb157cac4767dfc0268f6995e09de109d8468ff8) [MÃ]
- Trang Releases: "PR evidence assets 14 (headless-agent attachments)" 2026-09-26 (pre-release), "PR #26518 revised structured metadata visuals" 2026-08-23 được gắn "Latest", cùng nhiều mục "[internal] CI evidence asset store" — [GitHub releases](https://github.com/elizaOS/eliza/releases) [DOC]
- Lỗi thấy khi chạy trên bản npm: S1 không lưu được fact nào (§2); B7 không nhận được tin Telegram (§0) và rò fact giữa người dùng và giữa các agent (§3) [CHẠY]

### Inferences
- Muốn có hành vi 5b-in và riêng tư như DEV thì phải chạy từ mã nguồn `develop` (bun, monorepo lớn) hoặc chờ một bản beta mới. Cả hai đều là rủi ro vận hành cho doanh nghiệp.

### Gaps
- Không biết lịch phát hành 2.x ổn định.

## 9. Bảng chấm (yêu cầu đã sửa 2026-09-27)

| Tiêu chí | S1 = 1.7.2 (npm latest) | B7 = 2.0.3-beta.7 (npm beta) | DEV = develop eb157cac (chưa phát hành) | Bằng chứng chính |
|---|---|---|---|---|
| **R2'** chức danh/phòng ban agent, có dùng cho định tuyến/ủy quyền | **Không** [MÃ+CHẠY] | **Không** [MÃ+CHẠY] | **Không** [MÃ+CHẠY] | `Character` không có trường tổ chức; persona chỉ là text trong `system`/`bio` (§6) |
| **5a** định danh người gửi + kênh + nhóm trong mọi tin | **Một phần** [CHẠY]: UUID theo agent + tên + username; không có Telegram id, không có tên nhóm | **Một phần (yếu)** [CHẠY]: Stage 1 không có người gửi/kênh; Telegram nhận không được | **Một phần, gần đạt** [CHẠY]: tên + username + UUID ổn định, `source:"telegram"`, `channelType`, "World: -100111; current channel: G1 Marketing (GROUP)"; thiếu Telegram user id thô | §1, §2 |
| **5b-in** A ở G1/G2/DM là một người, điều học được ở G2 có trong DM | **Không** [CHẠY]: entity đúng nhưng fact không lưu được (lỗi parse); fact theo phòng và dynamic → DM(A) "No facts available" | **Một phần** [CHẠY]: lưu theo người, **tự động** chèn ở Stage 1, nhưng không lọc theo người | **Đạt – tự động** [CHẠY]: fact theo entity+agent, planner DM(A) có "KPI tháng 10 của Lan là 50 bài" (G2) và "Lan phụ trách fanpage X" (G1); điều kiện: Stage 1 chọn context `general` | §2 |
| **5b-cross** gộp A Telegram + A kênh khác | **Không/không rõ** [MÃ] (chỉ có `UPDATE_CONTACT` dạng danh bạ) | Chưa kiểm | **Một phần** [MÃ, chưa chạy]: API person-link OWNER/ADMIN, merge candidate, auto-merge ≥0.85 & ≥2 bằng chứng; FACTS mở rộng theo cụm; chỉ trong một agent; không có self-claim bằng mã | §4 |
| **5d** giao việc cho agent 2, agent 2 biết làm cho A | **Không** [CHẠY+MÃ]: SEND_MESSAGE → "Target user not found", Copywriter 0 request | **Không** [MÃ] | **Không** [MÃ+CHẠY]: `agentToAgent` không có consumer; orchestrator ACP chỉ lưu `userId` trong metadata; agent 2 không biết gì về A | §5 |
| **Privacy** fact của A không lọt sang B | **Đạt** giữa các DM [CHẠY]; fact phòng nhóm hiện với cả nhóm | **Không** [CHẠY]: fact của Lan hiện cho Minh, cho user mới Hoa, và ở agent Copywriter, dưới nhãn "about the speaker" | **Đạt** giữa DM/agent [CHẠY]; rủi ro: fact theo người (kể cả từ DM) hiện khi A nói trong nhóm; cụm suy ra từ handle chưa xác minh [MÃ] | §3 |

Các tiêu chí khác có thay đổi so với ghi chú trước:
- **R6:** có `plugin-zalo` (OA) và `plugin-zalouser` (zca-cli) bản alpha 2026-02-17 trên npm, nay mồ côi (§7).
- **R8:** stable 1.7.2 (2026-01-19); beta npm hỏng Telegram và rò riêng tư; phần sửa chỉ có ở `develop` (§8).
- Các tiêu chí R1, R3, R4, R7, R9–R12 không có bằng chứng mới.

## 10. Phải tự xây gì, có cần fork không

### Takeaway
Nếu chọn elizaOS, nên dựa trên mã `develop` (hoặc bản 2.x tiếp theo có các sửa đổi này), không dùng npm 1.7.2 hay 2.0.3-beta.7. Hầu hết phần còn thiếu làm được bằng plugin, **không cần fork**. Riêng việc chạy nhiều agent cần một host tự viết, vì host `packages/agent` chỉ chạy `agents.list[0]`. Host tự viết chỉ dùng API công khai của `@elizaos/core`, harness của nghiên cứu này là ví dụ.

### Cited Findings
- Điểm mở rộng có sẵn: `Plugin{actions, providers, evaluators, services, componentTypes, routes, events, …}` — [types/plugin.ts#L1119-L1322](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/plugin.ts#L1119-L1322) [MÃ]. Provider/action trùng tên có thể **thay thế** provider mặc định khi đặt `override` (`registerProvider` → `resolveComponentCollision`) — [runtime.ts#L2338-L2360](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/runtime.ts#L2338-L2360) [MÃ]. `runtime.messageService` do plugin assistant gắn vào — [plugin-assistant/src/index.ts#L13-L31](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/index.ts#L13-L31) [MÃ]
- Chạy nhiều agent trong một process bằng `new AgentRuntime(...)` cho từng agent, rồi `createDatabaseAdapter` + `runtime.registerDatabaseAdapter` + `initialize()`, đã chạy được với DEV (PGlite mỗi agent một thư mục; muốn dùng chung DB thì cần Postgres) [CHẠY]

### Inferences — danh sách cần xây (điểm mở rộng cụ thể)
1. **Host đa agent** (R2', 5d): tự viết process tạo N `AgentRuntime` với cùng bộ plugin như `createAssistantPlugins()`, dùng chung Postgres (PGlite khoá theo agent). Không cần fork; bỏ host `packages/agent` hoặc chạy mỗi agent một host.
2. **Sơ đồ tổ chức agent** (R2'): chứa trong `character.settings.extra.org = {title, department, reportsTo, subordinates}` (`extra?: JsonObject`, [types/agent.ts#L47](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/agent.ts#L47)). Thêm plugin "org" gồm: provider `ORG_CHART` (luôn chèn chức danh, phòng, cấp trên, cấp dưới, có `contexts`/`alwaysInResponseState` để lên planner) và action `DELEGATE_TO_AGENT` chọn agent đích theo phòng/chức danh.
3. **Ủy quyền mang danh tính A** (5d): trong action `DELEGATE_TO_AGENT`, gọi `targetRuntime.messageService.handleMessage(targetRuntime, memory, cb)`. `memory.metadata.onBehalfOf = {platform:"telegram", platformUserId:"1001", name:"Lan", sourceAgent, sourceRoom, selectedFacts}`. Ở agent đích cần provider `REQUESTER_CONTEXT` đọc metadata này vào prompt, cùng một callback trả kết quả về phòng gốc. Vì entity id của A ở agent 2 khác (`createUniqueUuid` gắn agentId), phải truyền khoá tự nhiên (platform + user id) chứ không truyền UUID.
4. **Danh tính người dùng dùng chung giữa các agent** (5b giữa các agent): một service/bảng "person" riêng (khoá `telegram:1001`, `zalo:…`) được tất cả agent đọc. Hoặc dùng PrincipalService làm nguồn chuẩn và ghi `identity_link` đã xác nhận cho từng agent. Không cần sửa `createUniqueUuid`.
5. **Chính sách lộ fact theo ngữ cảnh** (privacy): plugin thay `FACTS` (`override`) để lọc nhóm fact theo người theo loại phòng gốc (fact học trong DM không hiện khi đang ở nhóm), và chỉ dùng cụm `getVerifiedRelatedEntityIds`. Tắt auto-merge theo handle tự khai, hoặc thêm bước xác minh bằng mã (action `LINK_ACCOUNT` + route xác minh); đường attest/verify của admin đã có sẵn.
6. **Tiếng Việt cho trích xuất hậu lượt**: bổ sung evaluator/hook để không phụ thuộc regex tiếng Anh `POST_TURN_SEMANTIC_SIGNAL`, hoặc đảm bảo Stage 1 luôn điền `facts`.
7. **Zalo** (R6): port `plugin-zalo` (OA, DM) / `plugin-zalouser` (nhóm, zca-cli) bản alpha sang API hiện tại. Khoá entity nên theo mẫu Telegram `${accountId}:${userId}`. Plugin connector không cần fork.
8. **Tránh bản npm hiện có**: 1.7.2 cần viết lại evaluator/provider fact (parse lỗi, fact theo phòng). 2.0.3-beta.7 phải vá plugin-sql hoặc bật RLS (`ENABLE_DATA_ISOLATION=true` trên Postgres) và vá `await bot.launch`. Nếu buộc dùng beta.7 thì đây là **fork/patch**.

### Gaps
- Chưa thử viết plugin override FACTS thật, nên chưa chắc thứ tự đăng ký plugin cho phép ghi đè provider của plugin assistant như mong muốn (chưa kiểm chứng).
- Chưa đo chi phí vận hành khi chạy `develop` từ mã nguồn (bun 1.4.2, postinstall build nhiều gói).
