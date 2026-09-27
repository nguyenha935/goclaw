# Rakazo (elie222/rakazo): kiểm chứng bằng mã và chạy thật theo bộ tiêu chí cuối (D1, K1–K5, 5d, R1/R6/R7/R8)

Phạm vi: repo `github.com/elie222/rakazo`, commit `449f109d95d0df1dc7f04a381de778307133a2ad` (HEAD ngày 2026-09-27 17:41 UTC). Ngày kiểm: 2026-09-27 (đã xác nhận bằng `date`). Nhãn: [MÃ] = đọc mã; [CHẠY] = chạy thật với stub LLM; [DOC] = tài liệu trong repo; [?] = chưa kiểm chứng. Bằng chứng chạy đã rút gọn: `evidence/rakazo_run_evidence.json` (21,6 KB). Ghi chú cũ trong `new_candidates_global.md` được dùng làm bối cảnh, mọi điểm đều được kiểm lại trên commit mới.

Link mã đều trỏ tới `https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/…` (đường dẫn trong repo + số dòng).

## Câu hỏi 1 — Mô hình triển khai: một bản cài có chạy được "agent công ty" phục vụ nhiều người trong nhóm chung không?

### Takeaway
Không. Rakazo là nền tảng "trợ lý riêng cho từng người". Mỗi bot thuộc đúng một chủ (`Bot.userId`). Trên kênh nhắn tin, mỗi địa chỉ chat chỉ trỏ tới một bot của một chủ, và mỗi bot chỉ nhận đúng một địa chỉ chat (`MessagingIdentity.botId @unique`). Telegram, WhatsApp và Lark chỉ hỗ trợ DM, còn tin nhắn nhóm bị bỏ. Ngoại lệ duy nhất có dáng "agent dùng chung" là cầu Slack TeamChat. Ở đó đúng một bot cho cả deployment (`TEAM_CHAT_BOT_ID`) trả lời mọi người trong workspace Slack, nhưng bot chỉ thấy tên hiển thị của người gửi, và bộ nhớ trộn lẫn giữa mọi người, đã chạy thật và thấy rò rỉ.

### Cited Findings
- **Nguyên tắc thiết kế:**
  - Docstring: "One (provider, address) = one user + Space + one bot ("their agent")" [MÃ] — [packages/db/src/messaging.ts L38–46](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/messaging.ts#L38-L46)
  - Khi bật open-signup, người lạ được tạo tự động một user, một Space riêng và một bot tên "Assistant" với chỉ dẫn "You are the owner's personal agent" [MÃ] — [messaging.ts L103–128](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/messaging.ts#L103-L128)
- **Ràng buộc một địa chỉ ↔ một bot:**
  - Schema có `botId String @unique` và `@@unique([provider, address])` [MÃ] — [schema.prisma L1129–1149](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/prisma/schema.prisma#L1129-L1149)
  - Redeem code bắt lỗi unique "botId is unique (one chat app per bot)" [MÃ] — [messaging.ts L280–285](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/messaging.ts#L280-L285)
  - Chạy thật: admin xin mã thứ hai cho bot "Content Lead" (đã gắn Telegram 1001 của Lan) thì API trả `400: That bot is already linked to a chat app; unlink it first.` [CHẠY] — [router.ts L4301](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/router.ts#L4301); `evidence/rakazo_run_evidence.json` → `phaseA_T3_second_link_code`
- **Bot thuộc về một người:**
  - `listBots` lọc theo `spaceId` và `userId: actor.userId` [MÃ] — [packages/db/src/repos.ts L284–290](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/repos.ts#L284-L290)
  - `scoped()` từ chối bản ghi có `userId` khác người gọi [MÃ] — [packages/db/src/scope.ts L46–56](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/scope.ts#L46-L56)
  - Chạy thật: user web thứ hai (Minh) không phải deployment owner và có Space riêng. `threads.send` tới bot của admin → 500 (IsolationError); `messaging.link.start` cho bot của admin → 404 [CHẠY] — evidence → `web_isolation_minh`
- **Nhóm chat trên đường "personal line":**
  - Khi có người chưa liên kết, bot đăng lời chào "This line hosts Rakazo personal agents…" [MÃ] — [apps/api/src/messaging-inbound.ts L551–558](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/messaging-inbound.ts#L551-L558)
  - Tin nhóm được fan-out tới **bot riêng của từng thành viên đã duyệt** [MÃ] — [messaging-inbound.ts L572–629](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/messaging-inbound.ts#L572-L629)
  - Khả năng nhóm theo nền tảng:
    - Telegram `groups: false` — [packages/adapters/src/messaging-platforms.ts L153–156](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/messaging-platforms.ts#L153-L156)
    - WhatsApp `groups: false` — [L139–141](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/messaging-platforms.ts#L139-L141)
    - Lark `groups: false` — [L179–182](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/messaging-platforms.ts#L179-L182)
    - Chú thích mã: "Group conversations stay sendblue-only" — [L62–66](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/messaging-platforms.ts#L62-L66)
  - Tin nhóm bị bỏ tại `if (!isDirect && !platform.capabilities.groups) return null;` [MÃ] — [packages/adapters/src/chat-sdk-surface.ts L265–266](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/chat-sdk-surface.ts#L265-L266)
  - Chạy thật: gửi update Telegram `chat.type=supergroup` (G1, Lan) → HTTP 200 nhưng 0 hàng `messaging_channels` và 0 lời gọi LLM [CHẠY] — evidence → `phaseA_telegram_group_T5`
  - CHANGELOG ghi: "Connect Slack, WhatsApp Business Cloud, or Telegram DMs to a bot… Each app can use a different bot. Group conversations remain iMessage-only." [DOC] — [CHANGELOG.md](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/CHANGELOG.md)
- **Cầu Slack TeamChat, chế độ duy nhất có agent dùng chung:**
  - Khi `TEAM_CHAT_BOT_ID` được đặt, mọi sự kiện Slack (hoặc có `workspaceId`) đi vào `TeamChatBridge` với `providerId: "slack"` và **một** `botId` [MÃ] — [apps/api/src/team-chat-startup.ts L18–28](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/team-chat-startup.ts#L18-L28), [app.ts L691–720](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/app.ts#L691-L720), [env.ts L165–166](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/env.ts#L165-L166)
  - Mỗi kênh hoặc DM Slack thành một `ExternalConversation` có thread riêng, nhưng luôn gắn với bot đích đó [MÃ] — [team-chat-bridge.ts L210–243](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/team-chat-bridge.ts#L210-L243)
  - Chạy thật: 6 hội thoại (C_G1, C_G2, D1001, D1002, D9001, D1003) đều gắn bot "Content Lead" [CHẠY] — evidence → `phaseB_external_conversations`
- **VISION.md:** "One bot has one continuous visible thread…"; "Spaces are authorization boundaries…" [DOC] — [VISION.md](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/VISION.md), mục "Current decisions" và "Trust is explicit and verified"
- **Cách chạy thật và các điểm lệch so với production** [CHẠY]:
  - API và worker chạy từ mã nguồn (`tsx`, `NODE_ENV=development`) trên PostgreSQL 16 cục bộ. Không dùng image Docker vì Docker daemon không có.
  - `SANDBOX_PROVIDER=desktop`: sandbox thư mục trên host, là chế độ của app desktop. Với `none`, mọi run đều lỗi "Computers unavailable". Vậy **mọi run đều cần một "computer"**.
  - Mô hình: provider `local` (`RAKAZO_LOCAL_MODELS=stub-model`, `RAKAZO_LOCAL_MODELS_URL=http://127.0.0.1:18102/v1`) trỏ tới stub. Mỗi user web phải tự "connect" một credential `local` (key giả), nếu không sẽ gặp `needsModel`.
  - Telegram và Slack giả lập bằng server giả Bot API/Web API, qua biến môi trường mà adapter upstream (Vercel Chat SDK) vốn hỗ trợ: `TELEGRAM_API_BASE_URL`, `SLACK_API_URL`. Không sửa mã Rakazo.
  - Inbound đi qua đường thật:
    - Telegram: `POST /api/v1/messaging/webhook/telegram` kèm header `X-Telegram-Bot-Api-Secret-Token`.
    - Slack: `POST /api/v1/messaging/webhook/slack`, ký HMAC `v0`, sự kiện `message`/`app_mention`.
  - Slack dùng ID dạng `U1001/U1002/U9001/U1003` thay cho số. Kẻ mạo danh U1003 có `real_name` = "Admin Hà".
  - Giữa chừng, thư mục `/tmp/claude-0` bị đổi quyền thành 700 làm Postgres (chạy bằng user `postgres`) chết. Đã dời data sang `/var/tmp`, tạo lại DB và **chạy lại toàn bộ từ đầu**. Toàn bộ đã được xoá sau khi xong.

### Inferences
- Đây là quyết định kiến trúc, không phải tính năng còn thiếu. "Chủ sở hữu" là khái niệm trung tâm: bộ nhớ, bot directory, lời nhắc ("the owner…") và mirror outbound đều xoay quanh chủ. Muốn "agent 1 ngồi trong nhiều nhóm Telegram phục vụ nhiều người" thì phải đổi các bất biến lõi này.
- Có hai cách "lách" để dùng chung, cả hai đã chạy thử và đều hỏng yêu cầu riêng tư:
  - (a) Admin sở hữu mọi bot, rồi gắn Telegram của từng nhân viên vào một bot khác nhau. Cách này hỏng K2/K4/5d (xem câu 2–4).
  - (b) Dùng cầu Slack TeamChat. Chỉ được một bot, chỉ Slack, và người gửi chỉ có tên hiển thị.

### Gaps
- Chế độ open-signup (mỗi người lạ nhắn vào thì tự có tài khoản và bot riêng) chưa chạy. Chế độ này đòi `deploymentModelKey` của `openrouter`/`anthropic` (xem `isMessagingSurfaceEnabled`, [messaging-platforms.ts L211–217](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/messaging-platforms.ts#L211-L217)) và sẽ gọi mạng ngoài, nên chỉ kiểm bằng [MÃ].
- Đường nhóm iMessage/SMS qua Sendblue (nền tảng duy nhất có nhóm) chưa chạy, vì không giả lập Sendblue.

## Câu hỏi 2 — Danh tính: MessagingIdentity, mã liên kết, kênh, bộ nhớ theo người, xử lý nhóm (K2, một phần K5)

### Takeaway
Việc liên kết dùng đúng platform ID đã xác minh (`message.author.userId` từ webhook), nên người mạo danh chưa liên kết thì bị im lặng. Tuy vậy, liên kết chỉ nói "địa chỉ này là **chủ** của bot X". Trong prompt DM không có ID hay tên người gửi: mọi tin được coi là của chủ. Ở Slack TeamChat, prompt chỉ có tên hiển thị. Admin thật (U9001) và kẻ mạo danh (U1003, cùng tên "Admin Hà") cho ra prompt giống hệt nhau. Bộ nhớ gắn theo chủ và bot, không theo người đang nói.

### Cited Findings
- **Đường DM:**
  - Tra `(provider, address=event.from)`. Chưa liên kết thì im lặng, trừ khi tin là một mã liên kết hợp lệ hoặc open-signup đang bật [MÃ] — [messaging-inbound.ts L86–111](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/messaging-inbound.ts#L86-L111)
  - `from` là `message.author.userId` của nền tảng, còn `fromLabel` là tên hiển thị [MÃ] — [chat-sdk-surface.ts L267–277](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/chat-sdk-surface.ts#L267-L277)
  - Chạy thật:
    - Lan (1001) nhắn trước khi liên kết → 0 lời gọi LLM (T1).
    - Kẻ mạo danh 1003 "Admin Hà" → 0 lời gọi LLM (T4) [CHẠY] — evidence → `phaseA_telegram_steps`
- **Mã liên kết:**
  - Mã 8 ký tự, sống 10 phút, mỗi user chỉ có một mã hoạt động; phát hành từ web cho **bot của chính mình** [MÃ] — [messaging.ts L177–216](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/messaging.ts#L177-L216)
  - Redeem gắn địa chỉ gửi vào user và bot của người phát mã. Địa chỉ đã thuộc user khác thì bị từ chối [MÃ] — [messaging.ts L232–287](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/messaging.ts#L232-L287)
  - Chạy thật: admin phát mã cho "Content Lead", Lan 1001 gửi mã → `messaging_identities` có `telegram | 1001 | userId=<admin> | botId=<Content Lead>`, kèm tin xác nhận `Linked. Messages here now reach "Content Lead".` [CHẠY] — evidence → `phaseA_identities`, `phaseA_outbound_rows`
- **Prompt DM không mang danh tính người gửi:**
  - `sendUserMessage({ userId: ids.userId, blocks:[{kind:"text", text}], prompt: text })`: chỉ có văn bản, và `userId` là của **chủ** [MÃ] — [messaging-inbound.ts L142–151](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/messaging-inbound.ts#L142-L151)
  - System note: "Chat surface: the owner also reaches you over a messaging app…" [MÃ] — [packages/core/src/messaging-prompts.ts L3–10](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/core/src/messaging-prompts.ts#L3-L10)
  - Chạy thật: prompt T8 của "Content Lead" có lượt user `Mình là Lan, phụ trách fanpage X…` nhưng không có ID, tên hay kênh. Bot hiểu người nhắn là "owner", tức admin [CHẠY] — evidence → `phaseA_prompt_T8_agent1_LanDM`
- **Nhóm (chỉ Sendblue):**
  - Prompt `[Group "<tên nhóm>", <tên đầu của chủ>]: …` [MÃ] — [messaging-inbound.ts L581–598](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/messaging-inbound.ts#L581-L598)
  - Có khối riêng tư "Never reveal … the owner's personal information… in the group"; bộ nhớ, scratchpad và công cụ nhớ bị tắt trong channel run [MÃ] — [messaging-prompts.ts L12–20](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/core/src/messaging-prompts.ts#L12-L20), [executor.ts L1398–1413](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/executor.ts#L1398-L1413), [L4642–4649](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/executor.ts#L4642-L4649)
- **Slack TeamChat:**
  - `teamChatPrompt` = `` `${Provider} message from ${senderName}:\n\n${content}` `` [MÃ] — [team-chat-bridge.ts L82–85](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/team-chat-bridge.ts#L82-L85), [L1047–1049](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/team-chat-bridge.ts#L1047-L1049)
  - `senderId` được lưu trong DB (`ExternalMessage`) nhưng không đưa vào prompt [MÃ] — [packages/adapters/src/team-chat-messaging.ts L35–36](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/team-chat-messaging.ts#L35-L36)
  - Chạy thật: prompt của U9001 và U1003 đều là `Slack message from Admin Hà:\n\nLan đã nói gì về KPI?`. Mô hình không có cách nào phân biệt hai người [CHẠY] — evidence → `phaseB_prompt_B7_admin_U9001`, `phaseB_prompt_B8_impostor_U1003`
  - Chạy thật: trong lịch sử thread của kênh G1, các dòng transcript mirror (kể cả tin ambient bị bỏ qua như "Hôm nay team họp lúc 3h nhé") vào dưới dạng lượt `user` **không ghi người nói** [CHẠY] — evidence → `phaseB_prompt_B4m_G1_history`
- **Bộ nhớ theo người (5b-in):**
  - Bộ nhớ được khoá theo `(spaceId, userId=chủ, scope, botId)` [MÃ] — [packages/memory/src/index.ts L27–37](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/memory/src/index.ts#L27-L37)
  - Tool `remember` luôn ghi vào scope `bot` [MÃ] — [executor.ts L2660–2672](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/executor.ts#L2660-L2672)
  - Lời gọi `commit` **ghi đè** cả tài liệu, không nối thêm [MÃ] — [memory/src/index.ts L71–100](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/memory/src/index.ts#L71-L100)
  - Chạy thật: trong DM Telegram, Lan nói KPI; đến lượt hỏi lại (T8), system prompt có `## bot: MEMORY.md … KPI tháng 10 là 50 bài` và lịch sử hội thoại [CHẠY] — evidence → `phaseA_prompt_T8_agent1_LanDM`. Nội dung ghi nhớ do stub soạn sẵn, nhưng đường "ghi nhớ rồi tự tiêm vào prompt" là hành vi thật của nền tảng.
- **Liên kết đa kênh (5b-cross):**
  - Nhiều địa chỉ trên nhiều nền tảng có thể cùng trỏ về một `User`, nhưng mỗi địa chỉ phải trỏ tới một bot khác nhau (`botId @unique`) [MÃ/CHẠY, xem T3]
  - Tài liệu `user` scope ("Shared documents") dùng chung cho mọi bot của cùng user trong Space [MÃ] — [packages/adapters/src/memory-context.ts L9–35](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/memory-context.ts#L9-L35)
  - Ở TeamChat, người gửi Slack không được nối với `MessagingIdentity`. `MessagingIdentity` chỉ được dùng để quyết định có được đánh thức routine hay không [MÃ] — [messaging-inbound.ts L263–291](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/messaging-inbound.ts#L263-L291)
- **Allowlist phía adapter:** adapter Telegram của Chat SDK tự đọc `TELEGRAM_ALLOWED_USER_IDS`, nhưng Rakazo không dùng tới [MÃ, trong `node_modules/@chat-adapter/telegram` 4.40.0, dist L1058–1060].

### Inferences
- 5a trong DM đạt ở mức định tuyến vì dùng ID đã xác minh, nhưng không đạt ở mức mô hình: mô hình không biết ai đang nói. Ở mức mô hình, kết quả thực tế là "chủ = bất kỳ ai cầm địa chỉ đã liên kết".
- Ở TeamChat, danh tính mà mô hình nhận được là tên hiển thị do người dùng tự sửa, nên không dùng được cho quyền admin hay cho quyền riêng tư.

### Gaps
- Chưa chạy liên kết thật hai kênh (Telegram + WhatsApp) cho cùng một người. Việc này cần giả lập thêm WhatsApp Cloud API; đã kết luận từ mã và ràng buộc unique đã chạy.

## Câu hỏi 3 — Đa agent, vai trò/phòng ban, giao việc và việc giao việc có mang theo người yêu cầu không (D1, 5d)

### Takeaway
Có chức danh (`title`), mô tả (`description`) và chỉ dẫn (`instructions`) cho từng bot. Các bot của cùng một chủ nhắn cho nhau qua `message_bot`, và có group chat trên web với `handoff_to_bot`. Không có thực thể phòng ban, không định tuyến theo vai trò và không có vòng review giữa các agent. Việc chọn ai làm do mô hình tự quyết dựa trên danh bạ. Khi giao việc, agent nhận chỉ biết "một bot khác của **user** bạn" gửi tới, không biết đang làm cho ai; kết quả còn được mirror tới người đã liên kết với bot nhận, tức là sai người.

### Cited Findings
- **Chức danh và danh bạ đồng đội:**
  - `Bot.title`/`description`/`instructions`/`teamChatRules` [MÃ] — [schema.prisma L338–373](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/prisma/schema.prisma#L338-L373)
  - Danh bạ = các bot khác **cùng `userId`** trong Space [MÃ] — [executor.ts L3700–3714](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/executor.ts#L3700-L3714)
  - Danh bạ được render thành "Your teammates — the user's other bots" [MÃ] — [packages/core/src/bot-messages.ts L99–108](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/core/src/bot-messages.ts#L99-L108)
  - Chức danh chỉ vào prompt ở lần chạy "created". Các lần sau chỉ còn `bot.instructions` (nếu khác rỗng) [MÃ/CHẠY] — [executor.ts L4741–4756](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/executor.ts#L4741-L4756). Trong log, request đầu có `Name/Title/Description`; từ request thứ ba, system bắt đầu thẳng bằng chuỗi persona.
- **Group chat trên web (`ChatGroup`, cũng thuộc một `userId`):** roster có title/description, kèm quy tắc "A handoff transfers ownership…" [MÃ] — [schema.prisma L429–448](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/prisma/schema.prisma#L429-L448), [bot-messages.ts L114–132](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/core/src/bot-messages.ts#L114-L132)
- **Phê duyệt:**
  - Phê duyệt là phê duyệt **hành động có hiệu ứng bên ngoài** do người làm: thẻ "Review before …", `ActionApprovalRule` theo Space/user [MÃ] — [packages/adapters/src/approval-ask.ts L22](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/approval-ask.ts#L22), [schema.prisma L117–131](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/prisma/schema.prisma#L117-L131)
  - Không có trạng thái review/duyệt kết quả giữa agent với agent [MÃ]
- **Kết nối giữa hai chủ khác nhau:** một agent xin nối với agent của người khác bằng lời mời "`{Owner}'s agent (…) wants to connect… Reply YES`", và phải được chủ bên kia duyệt [MÃ] — [packages/adapters/src/agent-connections.ts L36, L101](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/agent-connections.ts#L101)
- **5d — prompt đánh thức khi giao việc:**
  - Prompt: `[bot] A message just arrived from another of your user's bots: <name> (id: …)`, thân tin nằm trong `<bot_message>` [MÃ] — [bot-messages.ts L151–180](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/core/src/bot-messages.ts#L151-L180)
  - Chạy thật: Lan (Telegram 1001 → "Content Lead") nhờ giao "viết 3 caption". Prompt của "Copywriter" chỉ có `…another of your user's bots: Content Lead…<bot_message from="Content Lead">Viết 3 caption cho fanpage X</bot_message>`, không có "Lan" hay 1001 [CHẠY] — evidence → `phaseA_prompt_T13_agent2_woken_by_agent1_for_Lan`
  - Mirror chỉ áp cho run `messaging` và `bot_message`, và đi tới **identity của bot đang chạy** [MÃ] — [packages/adapters/src/messaging-delivery.ts L77–117](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/messaging-delivery.ts#L77-L117)
  - Chạy thật: lúc 18:06:50.315, trả lời của "Copywriter" (run `bot_message`, làm việc Lan yêu cầu) được gửi vào Telegram **1002 (Minh)**, vì Copywriter đang gắn với Minh [CHẠY] — evidence → `phaseA_outbound_rows`
- **Giới hạn vòng lặp:**
  - `BOT_MESSAGE_MAX_HOPS = 6` [MÃ] — [bot-messages.ts L14](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/core/src/bot-messages.ts#L14)
  - Giới hạn số tool call mỗi lượt mặc định là **không giới hạn** (`MAX_TOOL_CALLS_PER_TURN` để trống thì bằng 0, nghĩa là vô hạn) [MÃ] — [packages/adapters/src/pi-runtime.ts L113–120](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/pi-runtime.ts#L113-L120)
  - Chạy thật: một luật stub lặp lại khiến một lượt của "Content Lead" gọi `message_bot` khoảng 780 lần, sinh khoảng 1.400 request LLM trong khoảng 2 phút. Phải huỷ tay 292 run đang chờ [CHẠY] — evidence → `phaseB_loop_incident`. Đây là hiện vật của stub, nhưng nó cho thấy không có cầu chì mặc định.

### Inferences
- D1 chỉ đạt ở mức "persona có chức danh, và mô hình tự chọn đồng đội qua danh bạ". Cấu trúc tổ chức không điều khiển việc định tuyến, và không có phòng ban hay bảng việc.
- 5d thất bại theo hai cách. Agent nhận không biết người yêu cầu. Kết quả lại đi tới người đang gắn với agent nhận.

### Gaps
- Chưa chạy group chat trên web (`ChatGroup` + `handoff_to_bot`). Kết luận dựa vào mã.

## Câu hỏi 4 — Kho tri thức chung, persona, riêng tư có ngoại lệ admin, admin qua chat (K1, K3, K4, K5)

### Takeaway
- **K3 đạt:** `instructions` đứng đầu system prompt ở mọi kênh (đã chạy).
- **K1 chỉ một phần:** "Shared documents" (`user` scope MEMORY.md) được tiêm tự động toàn văn (tới 32 KB) vào mọi bot của **cùng một chủ**, nhưng không chia sẻ giữa các người dùng. Không có upload, URL hay folder sync, và không phân quyền theo phòng ban.
- **K4 không đạt:** tách người theo Space an toàn chỉ vì không ai dùng chung. Bất kỳ cấu hình dùng chung nào (TeamChat Slack; hoặc bot do admin sở hữu gắn với nhiều nhân viên) đều rò rỉ, đã chạy thật. Không có cơ chế ngoại lệ admin.
- **K5 không đạt:** admin là người đăng ký web đầu tiên. Không có cách gắn admin qua chat. Lệnh chat chỉ có YES/NO/LEAVE.

### Cited Findings
- **K1:**
  - `loadAgentMemoryContext` đọc `scope:"bot"` của bot và `scope:"user"` của chủ, tiêm vào `<durable_memory>`, giới hạn 32 KB [MÃ] — [memory-context.ts L3, L9–35](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/memory-context.ts#L9-L35)
  - Chạy thật: admin sửa `user` MEMORY.md thành "Brand guideline: slogan 'Nhanh như chớp'; giá gói Pro 199.000đ". Cả "Content Lead" (DM Lan, T9 "Gói Pro giá bao nhiêu?") lẫn "Copywriter" (DM Minh, T10 "Slogan công ty là gì?") đều có đoạn này trong system prompt [CHẠY] — evidence → `phaseA_prompt_T10_agent2_MinhDM_slogan`, `phaseA_prompt_T8_agent1_LanDM`
  - Cả bot TeamChat Slack cũng có đoạn này [CHẠY] — evidence → `phaseB_prompt_*`
  - Không chia sẻ sang người khác: `read()` lọc theo `userId: context.userId` [MÃ] — [memory/src/index.ts L27–37](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/memory/src/index.ts#L27-L37)
  - Tìm kiếm của store markdown chỉ là so khớp chuỗi con (`includes`) [MÃ] — [L49–69](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/memory/src/index.ts#L49-L69)
  - Nạp tài liệu: sửa trực tiếp trong Settings → Memory (e2e `apps/web/e2e/knowledge-panel.spec.ts`) hoặc `importMarkdown` [MÃ]
  - Bộ nhớ ngữ nghĩa là nhà cung cấp ngoài (Supermemory/Serenity) cấu hình theo Space, chỉ deployment owner được cấu hình endpoint riêng [MÃ] — [packages/adapters/src/memory-provider-factory.ts L158–181](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/memory-provider-factory.ts#L158-L181)
    - Scope `shared` dùng tag `rakazo:workspace:<spaceId>` [MÃ] — [supermemory-memory-provider.ts L89–94](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/supermemory-memory-provider.ts#L89-L94)
    - Auto-recall chỉ bật khi thread đã được nén lịch sử; ngoài ra phải qua tool `recall_memory` [MÃ] — [executor.ts L1382–1397](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/executor.ts#L1382-L1397)
  - Team Computer dùng chung file giữa các bot "inside the same trust boundary" [DOC] — [VISION.md](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/VISION.md), mục "Computers are durable places"
- **K3:**
  - `userTurnInstructions` đặt `botInstructions` đầu tiên [MÃ] — [executor.ts L4667–4686](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/executor.ts#L4667-L4686)
  - TeamChat ambient có thêm "Standing rules" (`teamChatRules`, tối đa 4000 ký tự) [MÃ] — [team-chat-bridge.ts L100–123](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/team-chat-bridge.ts#L100-L123)
  - Chạy thật: persona "Luôn xưng em, gọi người dùng là anh/chị, không dùng emoji, không bàn chính trị" có trong mọi request của "Content Lead", gồm DM Telegram, @mention trong kênh Slack G1/G2, DM Slack của Lan/Minh/Admin/kẻ mạo danh, và lượt đánh thức từ bot khác (`persona=True` ở mọi dòng) [CHẠY] — evidence → `phaseA_*`, `phaseB_*`
- **K4, rò rỉ đã chạy:**
  - (1) TeamChat Slack: Lan nói KPI trong kênh G2 và bot gọi `remember`. Sau đó, trong **DM của Minh** (hội thoại khác, người khác), system prompt chứa `## bot: MEMORY.md … KPI tháng 10 là 50 bài` [CHẠY] — evidence → `phaseB_prompt_B5m_MinhDM_after_Lan_G2_remember`. Nội dung ghi nhớ do stub soạn, còn việc tiêm vào prompt của người khác là hành vi của nền tảng.
  - (2) Bot của admin gắn với nhiều nhân viên: Minh hỏi "Copywriter": "Lan có KPI bao nhiêu?" → Copywriter `message_bot` sang "Content Lead" → prompt của Content Lead chứa **toàn bộ lịch sử DM của Lan** và bộ nhớ "Lan: KPI tháng 10 là 50 bài…", kèm lời "A message just arrived from another of your user's bots… Answer it if you can" [CHẠY] — evidence → `phaseA_prompt_T11_agent1_woken_by_agent2_for_Minh`
  - (3) Trả lời của Content Lead cho câu hỏi ấy cũng được mirror vào Telegram của Lan (18:06:20.168), còn trả lời của Copywriter đi vào Telegram của Minh [CHẠY] — evidence → `phaseA_outbound_rows`
  - Các biện pháp riêng tư có sẵn: khối "Never reveal the owner's personal information…" cùng việc tắt memory và tool nhớ **chỉ** trong channel run nhóm Sendblue [MÃ] — [messaging-prompts.ts L12–20](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/core/src/messaging-prompts.ts#L12-L20), [executor.ts L1398–1413](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/executor.ts#L1398-L1413)
  - Không có cơ chế "admin cho phép Minh xem thông tin Lan" [MÃ]
- **K5:**
  - Deployment owner = người đăng ký web đầu tiên [DOC/MÃ] — [docs/self-host.md](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/docs/self-host.md) ("The first registered user becomes the deployment owner"), [packages/db/src/bootstrap-user.ts L96–107](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/bootstrap-user.ts#L96-L107)
  - `isDeploymentOwner` chỉ dùng cho các thiết lập deployment trên web [MÃ] — [scope.ts L35–43](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/db/src/scope.ts#L35-L43)
  - Lệnh chat chỉ gồm `YES|NO|LEAVE` để trả lời lời mời vào nhóm hoặc kết nối agent [MÃ] — [packages/core/src/messaging-commands.ts L7–13](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/core/src/messaging-commands.ts#L7-L13)
  - Chạy thật: admin đăng ký đầu tiên nên `isDeploymentOwner=true`; Minh `false` [CHẠY]
  - Trong TeamChat, U9001 và kẻ mạo danh U1003 cho ra prompt giống hệt nhau [CHẠY]
  - Trong personal line, kẻ mạo danh chưa liên kết bị im lặng vì liên kết dùng ID đã xác minh [CHẠY]

### Inferences
- Nếu cho mỗi nhân viên một bot riêng trong Space riêng, riêng tư tốt nhờ tách hẳn. Nhưng khi đó không còn "agent công ty" dùng chung, và không có K1 chung.
- Mọi cách dùng chung đều rò rỉ, vì bộ nhớ và thread gắn với bot/chủ chứ không với người nói.
- Vì không có vai trò admin trong chat, không thể có "ngoại lệ admin" đúng nghĩa.

### Gaps
- Chưa thử mời nhiều người vào cùng một Space (lời mời Organization của Better Auth). Theo mã, dù chung Space, bot và bộ nhớ vẫn lọc theo `userId`.

## Câu hỏi 5 — R1, R6 (mở rộng kênh, Zalo), R7 giấy phép, R8 nhịp phát hành, tài liệu

### Takeaway
- **R1 đạt:** runtime pi chạy trong tiến trình, dùng key của người dùng hoặc của deployment, đã chạy với provider OpenAI-compatible `local`.
- **R6 chỉ một phần:** kênh là adapter của Vercel Chat SDK (MIT), nhưng danh sách nền tảng được dựng cứng trong core, nên Zalo phải sửa core. Đã có adapter cộng đồng `chat-adapter-zalo` 0.1.0, chỉ DM.
- **R7 đạt:** Apache-2.0.
- **R8 đạt, nhưng rất non:** dự án bắt đầu 2026-08-13; bản gắn tag cuối v0.1.6 ngày 2026-09-08; commit liên tục tới 2026-09-27; README tự nhận "in beta".

### Cited Findings
- **R1:**
  - Provider `local` đăng ký từ env, dùng API `openai-completions` [MÃ] — [packages/adapters/src/pi-local-provider.ts L10–20, L90–109](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/pi-local-provider.ts#L90-L109)
  - Key của deployment chỉ cho `openrouter`/`anthropic` [MÃ] — [deployment-model.ts L9–27](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/deployment-model.ts#L9-L27)
  - Chạy thật: mọi request tới stub là `POST /v1/chat/completions` với `model: stub-model`. System prompt dài khoảng 6.000–6.800 ký tự trước bộ nhớ; mỗi request mang 37–51 định nghĩa tool (40 trong run nhắn tin) [CHẠY]
  - Không dùng CLI lập trình. Tuy vậy, mọi run bắt buộc có một "computer" (docker, e2b, daytona, box hoặc desktop); `none` thì run lỗi [CHẠY] — [packages/adapters/src/none-sandbox.ts L14–15](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/none-sandbox.ts#L14-L15)
- **R6:**
  - `MessagingPlatform { provider; capabilities; adapter: Adapter (từ "chat"); participants?; channelName?; enrichTeamRoom? }` [MÃ] — [chat-sdk-surface.ts L32–54](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/chat-sdk-surface.ts#L32-L54)
  - Nền tảng được dựng trong `messagingPlatformsFromEnv`, gồm Sendblue, Slack, WhatsApp, Telegram, Lark. Không có plugin loader [MÃ] — [messaging-platforms.ts L82–198](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/packages/adapters/src/messaging-platforms.ts#L82-L198)
  - Env được đọc trong API ([env.ts L145–166](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/env.ts#L145-L166)) và trong worker
  - Adapter cộng đồng `chat-adapter-zalo` 0.1.0 (MIT, tác giả Nhat Bui, 2026-04-06; khoảng 16 KB; Zalo Bot Platform `bot-api.zaloplatforms.com`; `isDM` luôn `true`, tức chỉ DM) [MÃ, đọc tarball npm] — [npm chat-adapter-zalo](https://www.npmjs.com/package/chat-adapter-zalo), [repo](https://github.com/buiducnhat/chat-adapter-zalo)
  - `chat` (Vercel Chat SDK) 4.41.0, MIT, ngày 2026-09-18 [MÃ, registry npm] — [npm chat](https://www.npmjs.com/package/chat)
- **R7:**
  - `LICENSE` Apache-2.0; `package.json` L6 `"license": "Apache-2.0"` [MÃ] — [LICENSE](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/LICENSE)
  - Tự host bằng Docker Compose images (`ghcr.io/elie222/rakazo/app`, tag `edge`; "Do not assume `latest` is present until a stable release exists") [DOC] — [docs/self-host.md](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/docs/self-host.md)
- **R8:**
  - Tag: v0.1.0-beta (2026-08-13), v0.1.0 và v0.1.1 (2026-09-03), v0.1.2 (2026-09-06), v0.1.3 và v0.1.4 (2026-09-07), v0.1.5 và v0.1.6 (2026-09-08) [MÃ, `git tag`]
  - 951 commit từ 2026-08-13 tới 2026-09-27; 150 commit từ 2026-09-08; 74 commit từ 2026-09-20 [MÃ, `git log`]
  - 76 tác giả. Nhiều nhất: Elie Steinbock 345 (thêm 76 dưới tên "Eliezer Steinbock"), "Cursor Agent" 168, Zhang Ning 84 [MÃ, `git shortlog`]
  - README L12: "Rakazo is in beta." [DOC]
- **Tài liệu:**
  - `docs/` có khoảng 1.600 dòng: self-host, secrets, sandbox providers, restricted network, bot-secrets, computer-runtime… [DOC]
  - Không có tài liệu về "agent công ty" hay phòng ban [DOC]
  - CHANGELOG được ghi chi tiết [DOC]

### Inferences
- Thêm Zalo DM tốn khoảng 1–3 ngày: thêm dependency, một khối trong `messagingPlatformsFromEnv`, biến env ở API và worker, rồi kiểm webhook. Nhưng việc này là sửa core, tức phải fork hoặc gửi PR lên upstream.
- Zalo nhóm thì còn phải ánh xạ ngữ nghĩa nhóm, mà Rakazo hiện chỉ làm cho Sendblue. Adapter cộng đồng lại chỉ hỗ trợ DM.

### Gaps
- Chưa kiểm adapter Zalo cộng đồng chạy với Rakazo [?]. Chưa kiểm Zalo Bot Platform có API cho nhóm hay không [?].

## Câu hỏi 6 — Kết luận: có dùng Rakazo làm nền (hoặc thành phần) cho "agent company" phòng Marketing không?

### Takeaway
Không nên dùng làm nền. Mô hình cốt lõi của Rakazo là "mỗi người một (vài) trợ lý riêng", ngược với "agent công ty dùng chung trong nhóm". Các tiêu chí quyết định (K2, K4, K5, 5d, D1) đều hỏng ở mức kiến trúc, và đã chạy thật để xác nhận. Nếu dùng được gì, thì là tham khảo hoặc tái dùng lớp kênh Vercel Chat SDK (MIT, gói riêng, có sẵn Telegram, Slack, WhatsApp, Lark và Zalo cộng đồng), mẫu mã liên kết một lần dùng dựa trên ID nền tảng đã xác minh, và khối thẻ phê duyệt hành động.

### Cited Findings
- Tổng hợp từ các câu 1–5; bằng chứng chạy trong `evidence/rakazo_run_evidence.json` (các khoá `phaseA_*`, `phaseB_*`, `web_isolation_minh`).

### Gaps
- Chưa chạy: open-signup, nhóm Sendblue, group chat trên web, bộ nhớ ngữ nghĩa Supermemory/Serenity, liên kết hai kênh thật cho cùng một người. Các phần này được đánh giá bằng [MÃ].
- Stub trả lời theo luật regex. Mọi câu trả lời hay nội dung `remember` trong log là kịch bản; chỉ **cấu trúc prompt và đường đi dữ liệu** là hành vi thật của nền tảng.
- Sự cố vận hành trong lúc chạy: một lệnh `pkill -f "tsx src/index.ts"` (khoảng 17:59 UTC 2026-09-27) được chạy trên máy dùng chung trước khi chuyển sang kill theo PID/đường dẫn. Lệnh này có thể đã chạm vào tiến trình `sh -c "tsx src/index.ts"` của nhóm nghiên cứu khác chạy song song [?].

### Inferences

#### Bảng tiêu chí

| Tiêu chí | Kết quả | Bằng chứng chính | Nhãn |
|---|---|---|---|
| D1 Vận hành phòng ban | Một phần (yếu) | Có `title`/`description`/`instructions`; danh bạ đồng đội + `message_bot`; group web + `handoff_to_bot`; phê duyệt hành động ngoài. Không có phòng ban, không định tuyến theo vai trò, không review giữa agent. Mọi bot thuộc một chủ (`executor.ts` L3700–3714, `bot-messages.ts` L99–132) | [MÃ] |
| K1 Kho tri thức chung | Một phần | `user` MEMORY.md tự tiêm vào mọi bot **cùng chủ** (đã chạy với slogan/giá Pro ở cả hai agent). Không chia giữa người dùng, không upload/URL/folder sync, không scope phòng ban. Bộ nhớ ngữ nghĩa `shared` phụ thuộc Supermemory/Serenity | [CHẠY]/[MÃ] |
| K2-5a ID ổn định + kênh + nhóm trên mỗi tin | Một phần | Định tuyến DM dùng ID đã xác minh (kẻ mạo danh bị im lặng). Nhưng prompt DM không có ID/tên người gửi; Slack chỉ có `senderName`, admin và kẻ mạo danh ra prompt giống hệt; transcript nhóm không ghi người nói | [CHẠY] |
| K2-5b-in Cùng người qua nhóm và DM, nhớ theo người | Không | Telegram bỏ tin nhóm; bộ nhớ theo chủ/bot, không theo người nói (Slack: KPI của Lan xuất hiện trong DM của Minh) | [CHẠY] |
| K2-5b-cross Cùng người qua nhiều kênh | Một phần | Nhiều địa chỉ → một `User` qua mã liên kết, nhưng mỗi địa chỉ phải trỏ bot khác (`botId @unique`, mã thứ hai bị từ chối). Slack TeamChat không nối danh tính | [CHẠY]/[MÃ] |
| K3 Persona | Đạt | `instructions` đứng đầu system prompt ở DM Telegram, kênh/DM Slack, lượt bot-to-bot (`executor.ts` L4667–4686). Riêng chức danh chỉ vào prompt ở lần "created" | [CHẠY] |
| K4 Riêng tư + ngoại lệ admin | Không | Rò rỉ đã chạy: bộ nhớ Slack Lan→Minh; `message_bot` đưa lịch sử và bộ nhớ của Lan vào prompt khi Minh hỏi; kết quả việc của Lan mirror sang Telegram của Minh. Không có cơ chế ngoại lệ admin | [CHẠY] |
| K5 Admin gắn qua chat | Không | Owner = người đăng ký web đầu tiên. Chat chỉ có YES/NO/LEAVE. Liên kết dùng ID đã xác minh nhưng chỉ gắn "chủ bot", không gắn quyền admin | [CHẠY]/[MÃ] |
| 5d Giao việc mang theo người yêu cầu | Không | Prompt đánh thức: "another of your user's bots: Content Lead", không có Lan; kết quả mirror tới Minh (18:06:50.315) | [CHẠY] |
| R1 Backend riêng, key riêng, không CLI | Đạt | pi-agent-core trong tiến trình; provider `local` và credential người dùng chạy được với stub. Cần sandbox "computer" cho mọi run | [CHẠY] |
| R6 Kênh mở rộng bằng code, Zalo không sửa core | Một phần | Adapter Chat SDK, nhưng danh sách nền tảng dựng cứng trong `messaging-platforms.ts` L82–198. Có `chat-adapter-zalo` 0.1.0 (chỉ DM). Nhóm chỉ Sendblue/Slack | [MÃ] |
| R7 Tự host, giấy phép dùng kinh doanh | Đạt | Apache-2.0; Compose images; đã chạy từ mã nguồn | [MÃ]/[CHẠY] |
| R8 Còn sống (từ 2026-06-27) | Đạt | v0.1.6 ngày 2026-09-08; 150 commit sau đó; HEAD ngày 2026-09-27. Beta, dự án mới 6 tuần tuổi | [MÃ] |

#### Phải tự xây gì, có cần fork không

Phải fork. Hầu hết thay đổi đụng vào bất biến lõi: `Bot.userId`, "một bot một thread", `MessagingIdentity.botId @unique`, bộ nhớ khoá theo chủ, và danh sách nền tảng dựng cứng. Không có plugin hay hook để làm từ bên ngoài. Ước lượng cho một lập trình viên TypeScript senior quen codebase:

1. **Agent công ty dùng chung trên kênh nhắn tin (2–3 tuần).** Tách `MessagingIdentity` thành "người ↔ địa chỉ", bỏ ràng buộc một địa chỉ ↔ một bot. Định tuyến DM/nhóm tới bot công ty theo handle, với thread riêng cho từng hội thoại (tổng quát hoá `ExternalConversation` hiện chỉ cho Slack).
2. **Nhóm Telegram và Zalo (1–2 tuần).** Bật `groups`, nhận diện mention, danh sách thành viên. Tích hợp `chat-adapter-zalo` (DM) rồi mở rộng cho nhóm nếu Zalo Bot Platform cho phép [?].
3. **Danh tính cấp người (khoảng 2 tuần).** Bảng `people` và liên kết đa kênh. Header prompt cho mỗi tin gồm ID đã xác minh, kênh và nhóm. Ghi transcript kèm người nói.
4. **Bộ nhớ theo người và lớp riêng tư (khoảng 2 tuần).** Scope bộ nhớ theo người; lọc khi tiêm bộ nhớ và khi `message_bot`; bỏ mirror sai người; thêm cơ chế cấp quyền ngoại lệ do admin.
5. **Admin hệ thống gắn qua chat (khoảng 1 tuần).** Gắn `(provider, address)` đã xác minh vào vai trò admin, thêm lệnh admin trong chat.
6. **5d, người yêu cầu đi theo việc được giao (3–5 ngày).** Thêm `requester` vào block `bot_message`, vào prompt đánh thức và vào đích mirror.
7. **Phòng ban, vai trò, chia và duyệt việc (2–4 tuần).**
8. **K1 đúng nghĩa (2–3 tuần).** Upload, URL, folder sync; RAG; phân quyền theo phòng ban; tách khỏi bộ nhớ riêng.

Tổng cộng khoảng **12–18 người-tuần** (3–4,5 tháng), chưa tính chi phí rebase liên tục theo upstream đang thay đổi rất nhanh. Với khối lượng này, thực chất là viết lại lớp nhắn tin, danh tính và bộ nhớ. Không đáng so với việc chọn một nền có sẵn mô hình agent dùng chung. Cách dùng hợp lý hơn: **chỉ lấy lớp kênh Vercel Chat SDK** (`chat` + `@chat-adapter/*`, MIT, gói độc lập, không phụ thuộc Rakazo) và mẫu mã liên kết để ghép vào nền khác.

#### Rủi ro đáng chú ý

- **Bảo trì:**
  - Dự án 6 tuần tuổi, beta, khoảng 20 commit/ngày (951 commit từ 2026-08-13).
  - 168 commit của "Cursor Agent".
  - Chưa có bản stable; images mặc định tag `edge`.
  - Một fork sẽ lệch rất nhanh.
- **Giấy phép:**
  - Apache-2.0 (Rakazo) và MIT (Chat SDK, `chat-adapter-zalo`) đều dùng kinh doanh được.
  - Adapter Zalo là 0.1.0 của một tác giả, không chính thức.
- **Chi phí token:**
  - Mỗi request có khoảng 6–7 nghìn ký tự system prompt cộng 37–51 định nghĩa tool, cộng tới 32 KB bộ nhớ tiêm toàn văn, cộng toàn bộ lịch sử thread duy nhất của bot [CHẠY].
  - `MAX_TOOL_CALLS_PER_TURN` mặc định là vô hạn. Giới hạn hop bot-to-bot (6) chỉ chặn độ sâu, không chặn độ rộng. Trong lần chạy với stub, đã thấy khoảng 780 tool call trong một lượt [CHẠY].
  - Open-signup tính tiền vào key của deployment [MÃ] — [messaging-inbound.ts L39–43](https://github.com/elie222/rakazo/blob/449f109d95d0df1dc7f04a381de778307133a2ad/apps/api/src/messaging-inbound.ts#L39-L43)
- **Bảo mật:**
  - Mọi run cần một "computer". Sandbox `desktop` chạy shell ngay trên host; Docker supervisor cần token riêng.
  - TeamChat tin theo tên hiển thị Slack, nên người khác có thể mạo danh admin [CHẠY].
  - Trả lời bot-to-bot tự mirror ra chat của người đang gắn với bot, có thể lộ nội dung sang người khác [CHẠY].
  - Lịch sử một-thread-mỗi-bot trộn DM của chủ với mọi yêu cầu từ bot khác [CHẠY].
- **Vận hành:**
  - Cần Postgres, API, worker (Graphile) và nhà cung cấp computer.
  - Yêu cầu Node `^22.22.2`; một dependency (`@composio/core`) đòi `>=22.22.3`, phải cài với `engine-strict=false` [CHẠY].
