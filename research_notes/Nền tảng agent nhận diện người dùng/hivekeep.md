# Hivekeep: nhận diện cùng một người qua nhóm, DM và kênh; vai trò agent (kiểm theo yêu cầu đã sửa ngày 2026-09-27)

Phạm vi: `MarlBurroW/hivekeep` tại commit `7d023c952e46861070683825ff545daf981910f0` (commit cuối trên nhánh mặc định, ngày 2026-09-17; `package.json` ghi version 1.10.0). Đã clone và **chạy thật** ngày 2026-09-27 với LLM giả (stub). Nhãn dùng trong ghi chú: [CHẠY] = thấy trong request mà Hivekeep thực sự gửi tới stub hoặc trong DB sau khi chạy; [MÃ] = đọc mã; [DOC] = tài liệu trong repo; [?] = chưa kiểm chứng.

Mọi link mã trỏ tới `https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/<path>#L<n>`. Bằng chứng chạy thử được lưu tại `file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/`, gồm `evidence_trimmed.txt` (22 request đã cắt gọn), `requests.jsonl` (bản đầy đủ), `outbound.jsonl`, `rules.json`, `testchan_plugin/`. Đây là thư mục scratchpad, có thể bị xoá sau phiên; các trích đoạn quan trọng đã chép vào ghi chú này.

## Cách chạy thử và cách bơm tin nhắn (đọc trước để đánh giá độ tin cậy của nhãn [CHẠY])

### Takeaway
Đã chạy được trọn kịch bản 1–6 (và thêm bước 7, `send_message`) trên Hivekeep thật: bun 1.3.11, SQLite, `bun src/server/index.ts` ở cổng 4178. LLM là stub OpenAI-compatible ở cổng 18084. Tin nhắn đi vào qua **route webhook chuẩn dành cho kênh plugin**. Từ `handleIncomingChannelMessage` trở đi, đường xử lý giống hệt kênh có sẵn. Khác biệt duy nhất là tên platform (`testchan-tg` thay cho `telegram`) và phần vận chuyển Telegram (polling hoặc webhook tới api.telegram.org) không được chạy.

### Cited Findings
- **Cấu hình [CHẠY]:** tạo admin, onboarding và mọi đối tượng bằng REST API thật (`/api/auth/sign-up/email`, `/api/onboarding/profile`, `/api/providers`, `/api/models/:id`, `/api/settings/default-llm`, `/api/settings/embedding-model`, `/api/plugins/testchan/enable`, `/api/agents`, `/api/channels`, `/api/channels/:id/activate`). Provider có type `openai-compatible`, `baseUrl=http://127.0.0.1:18084/v1`, model `stub-model`, embedding `stub-embed` — [setup.ts](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/setup.ts)
- **Hai agent [CHẠY]:** "Content Lead" (slug `content-lead`, `role` = "Content Lead – Phòng Marketing") và "Copywriter" (slug `copywriter`, `role` = "Copywriter – Phòng Marketing"). Cả hai được gán toolbox dựng sẵn `all` — [setup.ts](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/setup.ts)
- **Lưu ý toolbox [CHẠY]:** ở lần chạy đầu, agent tạo qua API mà không truyền `toolboxIds` chỉ nhận 14 tool: attach_file, edit_file, grep, list_directory, list_tools, multi_edit, notify, prompt_human, prompt_secret, read_file, request_tool_access, run_shell, think, write_file. Khi đó `set_contact_note` trả lỗi: `Tool "set_contact_note" exists but is not in your current toolset. It must be granted by one of your active toolboxes…`. Nghĩa là tool contacts, memory, tasks và inter-agent phải được cấp qua toolbox. Tạo agent qua UI có mặc định khác hay không thì chưa kiểm [?] — [evidence lần đầu, request #2 trước khi reset DB] (log đã bị ghi đè khi reset; nội dung lỗi được chép nguyên văn ở đây)
- **Bơm tin nhắn [CHẠY]:** viết plugin nghiên cứu `plugins/testchan/` (`plugin.json` + `index.ts`, khoảng 100 dòng). Plugin export `channels: { 'testchan-tg', 'testchan-zalo' }`; mỗi adapter cài `ChannelAdapter` với `handleInboundWebhook`. Payload giả được POST tới `POST /api/channels/plugin/<platform>/webhook/<channelId>`. Host tìm adapter, gọi `handleInboundWebhook`, rồi gọi `handleIncomingChannelMessage(channelId, incoming)`, cũng là hàm mà adapter có sẵn gọi qua `onMessage` — [routes/channels.ts L136–182](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/routes/channels.ts#L136), [docs-site plugins/developing.md L246](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/docs-site/src/content/docs/plugins/developing.md#L246)
- `testchan-tg` nhận một Telegram Bot API `Update` giả và ánh xạ y hệt `TelegramAdapter.processUpdate` có sẵn: `platformUserId=from.id`, `platformDisplayName=first_name+last_name`, `platformChatId=chat.id`, `content=text`, **không có `metadata`** — [telegram.ts L221–247](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/channels/telegram.ts#L221)
- `testchan-zalo` nhận một sự kiện giả theo kiểu Zalo OA. Adapter này **có** phát `metadata` gồm `{chatId, chatType, chatTitle, senderPlatformId}`, để kiểm đường `<channel-context>` — [testchan_plugin/index.ts](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/testchan_plugin/index.ts)
- **Hai kênh [CHẠY]:** kênh TG giả bật `autoCreateContacts=true`. Kênh Zalo giả để `autoCreateContacts=false`, tức mọi người lạ phải qua cổng duyệt.
- **Stub [CHẠY]:** dùng một bản sao `stub_llm_cap.py`; bản gốc không bị sửa. Bản sao thêm hai trường cho rule:
  - `captures`: điền `@@CID@@` bằng regex trên body request, để lấy contact id từ prompt giống như model thật đọc id trong prompt.
  - `last_role`: `"user"` hoặc `"tool"`, để tránh vòng lặp gọi tool.
  - Mọi lời gọi tool và câu trả lời đều do rule viết sẵn, không phải model suy luận — [rules.json](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/rules.json)
- **Kịch bản đã chạy [CHẠY]:**
  - (1) G1 (chat -100111): A=1001 "Lan" gửi "Mình là Lan, phụ trách fanpage X, thích giọng văn hài hước.", stub gọi `set_contact_note(<id>, "global", …)`. B=1002 "Minh" gửi "Mình là Minh.", stub gọi `set_contact_note` cho B.
  - (2) G2 (chat -100222): A gửi "Nhớ giúp: KPI tháng 10 của mình là 50 bài.", stub gọi `memorize(content, category=fact, subject="Lan")`.
  - (3) DM(A) (chat 1001): "Bạn biết gì về mình? KPI của mình bao nhiêu?", stub gọi `recall("KPI tháng 10")`.
  - (4) DM(B): "Bạn biết gì về mình?", stub gọi `recall("KPI tháng 10")`.
  - (5) A nhắn trên Zalo giả (sender `zl-9001`, nhóm `zg-777` "Nhóm Zalo Content"), admin duyệt bằng `link` vào contact của Lan.
  - (6) DM(A): "Nhờ Copywriter viết 3 caption…", stub gọi `spawn_agent`.
  - (7) DM(A): "Hỏi Copywriter…", stub gọi `send_message(type=request)`.
  - Tổng cộng 22 request LLM — [evidence_trimmed.txt](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/evidence_trimmed.txt)
- **Dọn dẹp:** đã dừng server và stub theo đúng PID, đã xoá clone (2,1 GB gồm cả node_modules) và thư mục data. Không có ảnh chụp màn hình, vì phải build frontend bằng Vite và đây là phần không bắt buộc.

### Inferences
- Khác biệt giữa `testchan-tg` và `telegram` chỉ nằm ở chuỗi platform: prefix `[testchan-tg:Lan]`, và không có dòng gợi ý định dạng Telegram trong `buildCurrentMessageHint`. Contact, lịch sử, ghi chú, participants, memory và ủy quyền đều không phụ thuộc chuỗi này. Vì vậy kết luận [CHẠY] áp dụng được cho Telegram thật, trừ lớp vận chuyển.

### Gaps
- Chưa chạy adapter Telegram thật (không có bot token, không được tạo). Chưa chạy compaction, nên phần "agent profile" và "summaries" dưới đây chỉ là [MÃ].

## R2' — Agent có chức danh, phòng ban không, và nền tảng có dùng cấu trúc đó không?

### Takeaway
Mỗi agent có trường `role` dạng chữ tự do (bắt buộc), cùng với `character` và `expertise`. Hivekeep **không có** bảng team, phòng ban hay cấp trên. `role` chỉ được chèn vào prompt: vào câu tự giới thiệu của agent đó, và vào "Agent directory" mà các agent khác nhìn thấy. Việc chọn ai để ủy quyền do model tự quyết theo slug. Việc định tuyến tin nhắn đi theo kênh nào thuộc agent nào, không theo role. **Một phần.**

### Cited Findings
- Bảng `agents` có `name`, `slug`, `role` (notNull), `character`, `expertise`, `kind` ('regular'|'configurator'), `model`, `providerId`, `toolboxIds`. Không có trường phòng ban, team hay cấp trên [MÃ] — [schema.ts L127–164](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L127)
- Danh sách bảng trong `schema.ts` không có bảng team hay department [MÃ] — [schema.ts](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L1)
- System prompt của Content Lead có câu "You are Content Lead (slug: content-lead), Content Lead – Phòng Marketing." [CHẠY request #1] — [evidence_trimmed.txt](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/evidence_trimmed.txt)
- Prompt của Content Lead có mục "## Agent directory" với dòng "Copywriter (slug: copywriter) — Copywriter – Phòng Marketing". Kèm theo là hướng dẫn "delegate to the most appropriate Agent via send_message(slug, …)" và "spawn_agent(slug)" [CHẠY #1]. Prompt task của Copywriter liệt kê ngược lại "Content Lead (slug: content-lead) — Content Lead – Phòng Marketing" [CHẠY #17]
- Resolver chỉ tra slug hoặc UUID. `role` chỉ được đọc để đưa vào danh sách agent (`inter-agent.ts` L250, `inter-agent-tools.ts` L115) [MÃ] — [agent-resolver.ts](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-resolver.ts#L1), [inter-agent.ts L250](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/inter-agent.ts#L250)
- Mỗi kênh gắn với đúng một agent (`channels.agentId`). Tin nhắn vào kênh luôn đến agent chủ kênh (`enqueueMessage({agentId: channel.agentId…})`) [MÃ] — [schema.ts L784–801](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L784), [channels.ts L788–800](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/channels.ts#L788)

### Inferences
- Viết "Content Lead – Phòng Marketing" là làm được ngay. Nhưng đó chỉ là chữ trong persona và danh bạ agent: không có logic nào lọc hay định tuyến theo phòng ban, và không có khái niệm "trưởng nhóm được giao việc cho thành viên".

### Gaps
- Chưa kiểm UI để xem có trường phòng ban ẩn nào không; mã server không có trường này.

## 5a — Mỗi tin nhắn, agent có thấy định danh ổn định của người gửi (ID nền tảng + tên), kênh và nhóm không?

### Takeaway
**Một phần.** Mỗi lượt đều có:
- tên người gửi ở prefix `[platform:Tên]`;
- khối "## Current speaker" với tên, `Role: external` và contact id (UUID ổn định theo người);
- dòng "Current message from: **platform** (sender: …)".

Tuy vậy, **platform user ID không hiện** với contact đã biết, và với adapter Telegram có sẵn thì **không có chat id hay tên nhóm**. Khối "Active participants" còn tính sai: DM bị gọi là "group conversation", còn nhóm G1 ở lượt đầu lại bị gọi là "one-on-one". Adapter plugin có thể đưa id, loại và tên nhóm vào prompt qua `metadata`, được chèn thành `<channel-context>` (đã chạy với Zalo giả).

### Cited Findings
- Request #1 (A viết trong nhóm G1). Khối `<system-reminder>` được đính vào tin nhắn user của lượt hiện tại [CHẠY]:
  ```
  ## Current speaker
  Name: Lan
  Role: external
  You know nothing about this person yet (contact id: 47fed3c9-7fbf-4a54-a699-7e03767ce548). … Save what you learn via set_contact_note(47fed3c9-…, "global", ...)
  ## Active participants
  This is a **one-on-one conversation** with Lan. …
  - Lan via testchan-tg (1 msg, last active just now)
  Current message from: **testchan-tg** (sender: Lan)
  ```
  và nội dung tin: `[testchan-tg:Lan] Mình là Lan, phụ trách fanpage X, thích giọng văn hài hước.`. Không có chuỗi `-100111` hay "G1 Marketing" ở bất kỳ đâu trong request — [evidence #1](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/evidence_trimmed.txt)
- Request #8 (DM của A) và #11 (DM của B) đều ghi "This is a **group conversation** with 2 participants", dù đây là tin nhắn riêng [CHẠY]. Request #5 (A ở G2, nhóm chỉ có A) cũng liệt kê "Lan … Minh" [CHẠY]
- Nguyên nhân: participants được tính từ **toàn bộ lịch sử của agent** bằng cách parse prefix `[platform:Tên]`. "Group" chỉ có nghĩa là có hơn một tên khác nhau trong lịch sử [MÃ] — [agent-engine.ts L3432–3460](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L3432), [prompt-builder.ts L933–966](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/prompt-builder.ts#L933)
- Prefix chỉ gồm platform và tên. `platform_id`/`username` chỉ được thêm khi contact chưa xác định (nhánh `(unknown, …)`) [MÃ] — [channels.ts L728–735](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/channels.ts#L728)
- `platformChatId` chỉ đi vào metadata hàng đợi để gửi trả lời đúng chat (DM(A) được trả về chatId 1001, G2 về -100222). Nó không đi vào prompt [CHẠY outbound.jsonl], [MÃ] — [channels.ts L802–815](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/channels.ts#L802)
- Adapter Telegram có sẵn không phát `metadata` [MÃ] — [telegram.ts L238–247](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/channels/telegram.ts#L238). Trong các adapter có sẵn, chỉ whatsapp-web phát metadata inbound `{whatsappWeb:{group}}` [MÃ] — [whatsapp-web.ts L206](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/channels/whatsapp-web.ts#L206)
- Nếu adapter truyền `IncomingMessage.metadata`, dữ liệu được lưu vào `messages.metadata.channel` và chèn vào nội dung gửi LLM dưới dạng `<channel-context>{json}</channel-context>` [MÃ] — [agent-engine.ts L3098–3117](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L3098), [sdk index.ts L302–317](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/packages/sdk/src/index.ts#L302)
- Request #14 (A nhắn trên Zalo giả) [CHẠY]:
  ```
  <channel-context>
  {"channel":{"chatId":"zg-777","chatType":"group","chatTitle":"Nhóm Zalo Content","senderPlatformId":"zl-9001"}}
  </channel-context>
  [testchan-zalo:Lan] Chào, mình nhắn từ Zalo nè. Nhắc lại giúp KPI của mình?
  ```
- "Role" của người gửi qua kênh bị gán cứng `'external'` [MÃ], và quả thật hiện "Role: external" [CHẠY]. Điều này **không** cản trở nhận diện: tên và ghi chú vẫn được chèn — [agent-engine.ts L1397–1430](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L1397)

### Inferences
- Với yêu cầu "agent thấy nhóm nào", Telegram có sẵn không đáp ứng. Một adapter plugin (Zalo, hoặc một adapter Telegram viết lại) thì đáp ứng được. Khối participants hiện tại dễ gây hiểu sai trong môi trường nhiều nhóm.

### Gaps
- Chưa kiểm Discord/Slack inbound: grep chỉ thấy metadata ở `listDestinations`, không thấy ở luồng inbound [?].

## 5b-in — Cùng kênh, A ở G1, G2 và DM có được nhận là MỘT người, và điều biết về A có dùng lại được theo người không?

### Takeaway
**Đạt, với lưu ý.** Contact được tra theo cặp `(platform, platformUserId)`, không theo chat, nên A ở G1, G2 và DM là cùng một contact [CHẠY]. Có ba cơ chế "nhớ", mỗi cơ chế một kiểu:

- **Contact notes: tự động và khóa theo người.** Ghi chú global của A tự xuất hiện trong "Current speaker" mỗi khi A nói, ở bất kỳ chat nào [CHẠY]. Tuy vậy, việc *ghi* ghi chú phụ thuộc vào model có gọi `set_contact_note` hay không (prompt có nhắc).
- **Lịch sử hội thoại: tự động nhưng khóa theo agent.** Mọi nhóm và DM dồn vào một thread duy nhất. Vì vậy câu KPI nói ở G2 hiện nguyên văn trong request của DM(A) [CHẠY]; tác dụng phụ là rò sang B (xem mục Privacy).
- **`memorize`/`recall`: dựa vào tool và không lọc theo người.** Bản ghi khóa theo agent; `subject` là chữ tự do do model đặt. `recall` gọi từ lượt của B vẫn trả KPI của A [CHẠY].

### Cited Findings
- `findContactByPlatformId(platform, platformId)` và `resolveChannelContact(channel, incoming)` tra theo `channel.platform` + `incoming.platformUserId`, không dùng `platformChatId` [MÃ] — [channels.ts L1647–1655](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/channels.ts#L1647), [channels.ts L1706–1712](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/channels.ts#L1706)
- Chỉ mục duy nhất `(platform, platform_id)` trên `contact_platform_ids` [MÃ] — [schema.ts L313–323](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L313)
- DB sau khi chạy [CHẠY]:
  - `contact_platform_ids`: Lan có `testchan-tg:1001` và `testchan-zalo:zl-9001`; Minh có `testchan-tg:1002`.
  - `contacts`: Lan có `first_name=null`, nickname "Lan", do auto-create lấy từ display name.
- Chế độ auto-create (`autoCreateContacts`) **luôn tạo contact mới**, không bao giờ tự nối vào contact có sẵn dựa trên danh tính người gửi tự xưng [MÃ] — [channels.ts L1662–1700, L1714–1722](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/channels.ts#L1662)
- Request #8 (DM(A)) có trong reminder, **được chèn tự động** [CHẠY]:
  ```
  ## Current speaker
  Name: Lan
  Role: external
  Shared notes (visible to all Agents):
  - Lan phụ trách fanpage X, thích giọng văn hài hước.
  ```
  Ghi chú này được tạo ở G1, bước 1.
- Cũng trong request #8, KPI **không** có trong system prompt hay reminder. KPI chỉ xuất hiện trong phần lịch sử được gửi kèm: `[user] '[testchan-tg:Lan] Nhớ giúp: KPI tháng 10 của mình là 50 bài.'` và lời gọi `memorize` của bước 2 [CHẠY]
- Request #10: `recall({"query":"KPI tháng 10"})` trả về `{"memories":[{"content":"KPI tháng 10 của Lan là 50 bài.","category":"fact","subject":"Lan","scope":"private",…}]}` [CHẠY]
- Cách chèn ghi chú: `enrichSpeakerFromContact` đọc `contact_notes` theo `contactId`. Ghi chú `global` (của mọi agent) và `user` được đọc hết; ghi chú `private` chỉ lấy của agent hiện tại. Số ghi chú và độ dài bị cắt theo `config.contacts.speakerMaxNotesPerScope` / `speakerMaxNoteChars` [MÃ] — [agent-engine.ts L1293–1321](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L1293), [prompt-builder.ts L886–930](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/prompt-builder.ts#L886)
- `contact_notes` có chỉ mục duy nhất `(contactId, agentId, userId, scope)`. Tool `set_contact_note` ghi đè ghi chú cùng scope ("Replaces any existing note of the same scope"). Như vậy mỗi agent chỉ có một ghi chú global cho mỗi người [MÃ] — [schema.ts L325–343](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L325), [contact-tools.ts L245–250](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/tools/contact-tools.ts#L245)
- Lịch sử: `buildMessageHistory(agentId)` lấy `messages WHERE agent_id=? AND task_id IS NULL AND session_id IS NULL`, không lọc theo kênh, chat hay người [MÃ] — [agent-engine.ts L3009–3014](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L3009). DB [CHẠY] cho thấy Content Lead có 18 tin ở main thread, gồm 8 tin từ kênh (G1, G2, DM(A), DM(B), Zalo) trong cùng một luồng
- Prompt nền nói thẳng mô hình này: "Your session is continuous and permanent — there is no "new conversation"… Multiple users may talk to you. Each message is prefixed with the sender's identity." [MÃ][CHẠY #1] — [prompt-builder.ts L550–556](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/prompt-builder.ts#L550)
- `memories` có khóa `agentId`, `subject` là chữ tự do và `scope` 'private'|'shared'. Không có khóa ngoại tới contact [MÃ] — [schema.ts L241–270](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L241). Tìm kiếm dùng điều kiện `(agent_id = ? OR scope = 'shared')`; bộ lọc `subject` là tùy chọn và do model tự truyền [MÃ] — [memory.ts L423, L476](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/memory.ts#L423), [memory-tools.ts L46–100](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/tools/memory-tools.ts#L46). Bản ghi thực tế trong DB: `agent_id=<Content Lead>, subject='Lan', scope='private'` [CHẠY]
- Memory v2: `agent_profiles` là **một tài liệu cho mỗi agent**, luôn được chèn vào system prompt và được viết lại khi compaction. Thiết kế nói danh tính người dùng thuộc về contact notes; `memories` chỉ truy cập qua `recall` [DOC/MÃ] — [memory.md](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/memory.md), [schema.ts L272–281](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L272)

### Inferences
- Nhận diện một người trong cùng kênh: đạt hoàn toàn ở mức hạ tầng.
- "Điều đã biết về A" chỉ được khóa theo người khi nó nằm trong contact notes, và ghi chú bị ghi đè nên không tích lũy nhiều fact rời. Các fact kiểu KPI mà model `memorize` thì chỉ tìm lại được bằng `recall`, và không bị lọc theo người.
- DM(A) trả lời được KPI chủ yếu nhờ lịch sử chung của agent, chứ không phải nhờ bộ nhớ khóa theo người. Khi lịch sử bị compaction, fact này chuyển vào summary và agent profile, là các thành phần khóa theo agent [MÃ].

### Gaps
- Chưa kiểm giá trị mặc định của `speakerMaxNotesPerScope`/`speakerMaxNoteChars`.
- Chưa chạy compaction để xem agent profile có chép fact của A hay không.

## 5b-cross — A trên Telegram và A trên kênh khác được nối thành một người thế nào?

### Takeaway
**Đạt, nhưng việc nối do admin làm thủ công** [CHẠY]. Một contact giữ được nhiều `(platform, platformId)`. Có ba cách nối:
- admin duyệt người lạ bằng hành động `link` vào contact có sẵn (ApprovalDialog);
- admin thêm platform id trên trang contact (API `POST /api/contacts/:id/platform-ids`);
- tài khoản web được nối qua `contacts.linkedUserId`.

Không có tự liên kết bằng mã, không tự gộp. Agent đọc được platform id nhưng không có tool để thêm.

### Cited Findings
- Bước 5 [CHẠY]:
  - A nhắn từ Zalo giả (`zl-9001`, display name "Lan Nguyen"). Kênh bật cổng duyệt, nên tin bị giữ lại và adapter gửi "Your access is pending approval…". `GET /api/channels/:id/user-mappings` trả `{"platformUserId":"zl-9001","platformDisplayName":"Lan Nguyen","bufferedCount":1}`.
  - Admin gọi `POST /api/channels/:id/user-mappings/:mapId/approve {"action":"link","contactId":"47fed3c9…"}` và nhận `{"success":true}`. Adapter gửi "Your access has been approved!", sau đó tin bị giữ được phát lại thành một lượt (request #14).
  - Trong request #14, "Current speaker: Name: Lan" kèm ghi chú "Lan phụ trách fanpage X…" được tạo từ Telegram giả.
- `approveChannelUser` với `link` chèn `contact_platform_ids(contactId, channel.platform, platformUserId)`, phát lại tin bị giữ, rồi dọn các mapping đang chờ của cùng user trên các kênh **cùng platform** [MÃ] — [channels.ts L1837–1950](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/channels.ts#L1837), [routes/channels.ts L488–520](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/routes/channels.ts#L488)
- `POST /api/contacts/:id/platform-ids` trả 409 nếu id đó đã thuộc contact khác [MÃ] — [routes/contacts.ts L435–463](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/routes/contacts.ts#L435). UI tương ứng: `src/client/components/contacts/ContactPlatformIds.tsx` và `src/client/components/channel/ApprovalDialog.tsx` (lựa chọn create hoặc link) [MÃ] — [ApprovalDialog.tsx L46–131](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/client/components/channel/ApprovalDialog.tsx#L46)
- Tool của agent `get_contact`/`search_contacts` trả `platformIds` (chỉ đọc). Không có tool thêm platform id [MÃ] — [contact-tools.ts L30–51](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/tools/contact-tools.ts#L30)
- Người dùng web: khi user có contact liên kết (`contacts.linkedUserId`), lượt chat từ web cũng được làm giàu từ contact đó, nên web và các kênh chat có thể là cùng một người [MÃ] — [schema.ts L283–290](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L283), [agent-engine.ts L1323–1341](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L1323)
- Nếu đã bật auto-create trên kênh thứ hai, người đó sẽ thành contact MỚI. Muốn gộp thì phải xoá platform id khỏi contact mới rồi thêm vào contact cũ, vì có chỉ mục duy nhất [MÃ] — [channels.ts L1714–1722](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/channels.ts#L1714)

### Inferences
- Nối xuyên kênh rất sạch về dữ liệu nhưng tốn công quản trị khi nhiều người: mỗi người, mỗi kênh cần một thao tác admin. Muốn người dùng tự nối (ví dụ gõ mã liên kết) thì phải viết plugin, bằng tool hoặc route. Plugin không có API SDK nào để thêm `contact_platform_ids`; chỉ có cách gọi REST nội bộ bằng quyền admin [?].

### Gaps
- Chưa kiểm route contacts có yêu cầu quyền admin hay chỉ cần đăng nhập.

## 5d — Khi agent 1 ủy quyền cho agent 2, agent 2 có biết mình đang làm cho A không?

### Takeaway
**Không** [CHẠY]. Cả hai đường ủy quyền đều không mang danh tính A vào context của agent 2:
- `spawn_agent` (sub-task): prompt của Copywriter chỉ có "## Your mission" bằng đúng `task_description` mà agent 1 viết.
- `send_message` (inter-agent request): Copywriter nhận "[Message from Agent "Content Lead"] …" và khối "Channel origin context" chỉ nói tin bắt nguồn từ `testchan-tg`.

Không có "Current speaker", contact id, ghi chú hay platform id của A. Chỉ khi model của agent 1 tự viết tên A vào nội dung giao việc thì agent 2 mới biết.

### Cited Findings
- Request #17, lượt task đầu tiên của Copywriter sau `spawn_agent` (stub truyền `task_description` = "Viết 3 caption cho fanpage X theo giọng văn phù hợp."). System prompt bắt đầu bằng "You are Copywriter, a specialized AI agent on Hivekeep, executing a delegated task… ## Your mission / Viết 3 caption cho fanpage X theo giọng văn phù hợp." Reminder chỉ có Language, Workspace và Context. Kiểm bằng regex trên toàn bộ request: không có `\bLan\b`, `1001`, contact id `47fed3c9`, "hài hước", "KPI" hay "Current speaker". Chữ "fanpage X" có mặt chỉ vì stub đã viết nó vào task_description [CHẠY] — [evidence #17](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/evidence_trimmed.txt)
- Request #22, lượt của Copywriter ở main thread sau `send_message(type="request")`, nội dung tin cuối [CHẠY]:
  ```
  [Message from Agent "Content Lead"] (Inter-agent request — reply with request_id="e1b5f2fb-…")
  Gợi ý giúp 3 slogan cho fanpage X.
  ```
  Reminder của lượt này:
  - có "## Known contacts" liệt kê *mọi* contact (Admin, Lan, Minh);
  - có "## Active participants … one-on-one conversation with Unknown";
  - có "## Channel origin context / This turn is part of a conversation chain that originated from **testchan-tg**…";
  - không có "Current speaker" và không nói người yêu cầu là ai.
- Mã: `sendInterAgentMessage` chỉ mang `message`, `senderAgentId`, `type`, `channelOriginId` [MÃ] — [inter-agent.ts L67–118](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/inter-agent.ts#L67). `pendingChannelContext` gán cứng `senderName: 'user'`, và giá trị này cũng không được in vào khối prompt [MÃ] — [agent-engine.ts L1433–1447](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L1433), [prompt-builder.ts L1007–1018](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/prompt-builder.ts#L1007). `spawn_agent` chỉ chuyển `title`, `task_description` và `channelOriginId` [MÃ] — [task-tools.ts L125–197](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/tools/task-tools.ts#L125)
- DB [CHẠY]: bảng `tasks` có `parent_agent_id=<Content Lead>`, `source_agent_id=<Copywriter>`, `channel_origin_id=<id lượt DM(A)>`. Bảng `channel_origins` lưu `platformUserId` của A [MÃ] — [schema.ts L859–869](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L859). Như vậy danh tính A **có** trong DB (qua `channel_origin_id` → `channel_origins.platform_user_id`) nhưng không được đưa vào prompt của agent 2.

### Inferences
- Không cần fork vẫn có thể lách: thêm chỉ dẫn vào persona hoặc global prompt của agent 1, kiểu "khi giao việc, luôn ghi 'thay mặt <tên> (contact id …)'". Agent 2 có tool `get_contact` để tự đọc ghi chú. Cách này phụ thuộc model [?]. Muốn chắc chắn thì phải sửa core.

### Gaps
- Chưa kiểm trường hợp agent 2 trả kết quả về và kết quả đó được gửi tự động ra kênh gốc.

## Privacy — Fact của A có lọt vào hội thoại với B không?

### Takeaway
**Có lọt (Không đạt)** [CHẠY]. Các nguồn rò:
- Vì một agent chỉ có một thread lịch sử, request DM(B) chứa nguyên văn mọi tin của A ở G1, G2 và DM(A), gồm cả câu KPI và câu trả lời "KPI tháng 10 là 50 bài".
- `recall` gọi từ lượt của B trả KPI của A.
- Khối "Known contacts" liệt kê tên và id của mọi contact trong mọi lượt.

Contact notes thì tách đúng: B chỉ thấy ghi chú của B trong "Current speaker".

### Cited Findings
- Request #11 (DM(B), "Bạn biết gì về mình?"). Current speaker = Minh với ghi chú "Minh là thành viên nhóm G1." [CHẠY]. Nhưng phần lịch sử gửi kèm có:
  - `[testchan-tg:Lan] Mình là Lan, phụ trách fanpage X, thích giọng văn hài hước.`
  - `[testchan-tg:Lan] Nhớ giúp: KPI tháng 10 của mình là 50 bài.` cùng tool call `memorize` "KPI tháng 10 của Lan là 50 bài."
  - `[testchan-tg:Lan] Bạn biết gì về mình? KPI của mình bao nhiêu?` và `[assistant] 'Bạn là Lan; KPI tháng 10 là 50 bài (stub).'`

  Nguồn: [evidence #11](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/evidence_trimmed.txt)
- Request #13 (lượt của B, sau `recall("KPI tháng 10")`): tool result `{"memories":[{"content":"KPI tháng 10 của Lan là 50 bài.","subject":"Lan","scope":"private",…}]}` [CHẠY]
- Nguyên nhân [MÃ]:
  - lịch sử lấy theo agent ([agent-engine.ts L3009–3014](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L3009));
  - memory tìm theo agent ([memory.ts L423](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/memory.ts#L423));
  - danh sách contact cho prompt là toàn bộ bảng `contacts` ([contacts.ts L921–960](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/contacts.ts#L921), [prompt-builder.ts L700](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/prompt-builder.ts#L700));
  - agent profile và compaction summaries theo agent, luôn được chèn ([schema.ts L223–239, L272–281](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L223)).
- Ngoài ra, bất kỳ agent nào cũng gọi được `get_contact(id)` để đọc chi tiết và ghi chú của contact khác [MÃ] — [contact-tools.ts L30–51](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/tools/contact-tools.ts#L30)
- Mức "quyền riêng tư" duy nhất có sẵn là scope của notes: `private` (theo agent), `global`, `user` [MÃ]. Scope này không ngăn được rò qua lịch sử.

### Inferences
- Đây là hệ quả của thiết kế "gia đình, vài người dùng, một phiên liên tục": câu "serving a small group of users" nằm ngay trong prompt nền. Với một agent ngồi trong nhiều nhóm của phòng Marketing, đây là rủi ro thực: fact của người này sẽ tới người khác, cả ở lượt kế tiếp lẫn sau khi compaction. Không có cấu hình nào tách lịch sử theo chat; `config.channels` không có tuỳ chọn nào như vậy [MÃ] — [config.ts L607–632](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/config.ts#L607)

### Gaps
- Chưa kiểm xem sau compaction, summary có chứa fact của A hay không (không chạy compaction). Theo cách thiết kế thì gần như chắc chắn có [?].

## Kênh có sẵn, SDK plugin kênh, công sức làm adapter Zalo, và mức sống của dự án

### Takeaway
Các kênh có sẵn: telegram, discord, slack, whatsapp, whatsapp-web, signal, matrix. Không có Zalo [CHẠY `/api/channels/platforms`]. Plugin thêm kênh được mà **không fork**, và đã chạy thật: `PluginExports.channels` + `ChannelAdapter` + `handleInboundWebhook`, với route webhook có sẵn. Dự án còn sống nhưng nhịp chậm lại rõ rệt: commit cuối ngày 2026-09-17, tag cuối v1.10.0 ngày 2026-07-29, khoảng 40 commit/tháng kể từ tháng 8/2026 so với khoảng 500 commit/tháng trong tháng 5–6/2026, gần như chỉ một tác giả.

### Cited Findings
- `GET /api/channels/platforms` trả `telegram, discord, slack, whatsapp, whatsapp-web, signal, matrix`, cộng thêm `testchan-tg, testchan-zalo` sau khi bật plugin [CHẠY]
- Log server: "Plugin activated … channels: 2" [CHẠY]. Hàm đăng ký là `channelAdapters.registerPlugin(adapter)` [MÃ] — [plugins.ts L1067–1105](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/plugins.ts#L1067)
- Hợp đồng SDK [MÃ]:
  - `ChannelAdapter { platform; meta?; configSchema?; start(); stop(); sendMessage(); listDestinations?(); handleInboundWebhook?() }` — [sdk index.ts L457–600](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/packages/sdk/src/index.ts#L457)
  - `IncomingMessage { platformUserId, platformUsername?, platformDisplayName?, platformMessageId, platformChatId, content, attachments?, metadata? }` — [sdk index.ts L302–317](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/packages/sdk/src/index.ts#L302)
  - `PluginExports { tools, providers, channels, routes, hooks, onCardAction, activate, deactivate }` — [sdk index.ts L2677–2712](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/packages/sdk/src/index.ts#L2677)
- Plugin được nạp từ `<cwd>/plugins/<name>/plugin.json`. Entry point export mặc định một hàm `(ctx) => PluginExports`. Sau khi bật, trạng thái được lưu trong DB [MÃ][CHẠY] — [plugins.ts L780–850, L895–935](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/plugins.ts#L780)
- Hook [MÃ]:
  - `beforeChat` chỉ được await; kết quả bị bỏ qua, nên plugin không sửa được prompt hay lịch sử — [agent-engine.ts L1365–1369](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L1365).
  - `beforeToolCall`: giá trị handler trả về cũng bị bỏ qua trong wrapper, dù JSDoc của SDK nói có thể thay `toolArgs`. Sửa trực tiếp object có thể có tác dụng [?] — [tools/index.ts L60–93](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/tools/index.ts#L60), [sdk index.ts L2244–2245](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/packages/sdk/src/index.ts#L2244)
- Tag và commit (git clone ngày 2026-09-27) [CHẠY]:
  - Tag: v1.10.0 (2026-07-29), v1.9.0 (2026-06-20), v1.8.0 (2026-06-19).
  - Commit theo tháng: 2026-05: 507; 2026-06: 493; 2026-07: 21; 2026-08: 40; 2026-09 (đến ngày 27): 42.
  - Từ 2026-07-01: MarlburroW/marlburrow 77 commit, kdegeek 12, dependabot 8.
  - Commit cuối `7d023c9` ngày 2026-09-17: "fix: integrate reviewed chat, installer, provider and dependency updates (#49)".
- npm: `@hivekeep/sdk` bản latest là 0.10.0 (phát hành 2026-06-07), trong khi repo đang ở `packages/sdk` 0.13.0 [CHẠY registry.npmjs.org]. Bản SDK trên npm tụt sau repo.
- Giấy phép MIT (`package.json` "license": "MIT") [MÃ] — [package.json](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/package.json)

### Inferences
- Công sức làm adapter Zalo OA dạng plugin: một file cài `ChannelAdapter` gồm các phần sau:
  - `handleInboundWebhook`: kiểm chữ ký Zalo và parse sự kiện `user_send_text` (và sự kiện nhóm nếu OA có quyền nhóm) thành `IncomingMessage`, có `metadata` về nhóm;
  - `sendMessage`: gọi API gửi tin của OA;
  - quản lý access token OA (refresh);
  - tuỳ chọn `listDestinations`.

  Host đã lo phần contact, duyệt, lịch sử, gửi trả lời và thử lại. Plugin thử nghiệm khoảng 100 dòng đã chạy trọn đường inbound và outbound. Adapter thật ước chừng vài trăm dòng cộng phần xử lý token [?]. Giới hạn của Zalo OA (quyền nhóm, cửa sổ nhắn tin) nằm ngoài phạm vi ghi chú này.

### Gaps
- Không truy cập api.github.com (theo yêu cầu), nên không có số sao, issue hay trạng thái release trên GitHub; chỉ dùng git tag.

## Bảng kết luận (theo yêu cầu đã sửa)

### Takeaway
Hivekeep nhận ra đúng một người qua nhóm, DM và cả kênh khác sau khi admin nối. Ghi chú về người đó được tự động chèn khi họ nói. Nhưng vì mỗi agent chỉ có một thread lịch sử, dữ liệu của người này lọt sang người khác. Ủy quyền giữa agent không mang danh tính người yêu cầu, và vai trò agent chỉ là chữ tự do.

### Cited Findings

| Tiêu chí | Kết luận | Bằng chứng chính | Nhãn |
|---|---|---|---|
| R2' (chức danh, phòng ban cho agent) | **Một phần** | `agents.role` là chữ tự do (bắt buộc). Prompt có "You are Content Lead (slug: content-lead), Content Lead – Phòng Marketing." và Agent directory liệt kê role (request #1, #17). Không có bảng team hay phòng ban; ủy quyền do model chọn theo slug; định tuyến theo `channels.agentId` | [CHẠY]+[MÃ] |
| 5a (định danh ổn định + kênh + nhóm) | **Một phần** | Có tên, contact id ổn định và platform trong "Current speaker" và "Current message from" (#1). Không có platform user ID với contact đã biết. Không có chat id hay tên nhóm với Telegram có sẵn. "Active participants" gọi sai DM là group (#8, #11). Plugin đưa được nhóm qua `<channel-context>` (#14) | [CHẠY]+[MÃ] |
| 5b-in (cùng kênh, G1/G2/DM là một người) | **Đạt, có lưu ý** | Tra contact theo `(platform, platformUserId)`. Ghi chú global của A tự hiện ở DM(A) (#8). Ghi ghi chú phụ thuộc model gọi `set_contact_note`. `memorize`/`recall` dựa vào tool, khóa theo agent, không lọc theo người (#10). Lịch sử khóa theo agent | [CHẠY]+[MÃ] |
| 5b-cross (Telegram + kênh khác thành một người) | **Đạt (admin nối thủ công)** | Duyệt `link` → `contact_platform_ids` có `testchan-tg:1001` + `testchan-zalo:zl-9001`. Lượt Zalo thấy "Current speaker: Lan" kèm ghi chú (#14). Không có tự liên kết hay mã liên kết; agent không thêm được platform id | [CHẠY]+[MÃ] |
| 5d (agent 2 biết đang làm cho A) | **Không** | `spawn_agent` (#17): chỉ có mission text. `send_message` (#22): "[Message from Agent "Content Lead"]" + "originated from testchan-tg". Không có tên, id hay ghi chú của A | [CHẠY]+[MÃ] |
| Privacy (fact của A không lọt sang B) | **Không (rò)** | DM(B) (#11) chứa nguyên văn tin G1, G2, DM(A) của Lan, gồm KPI và câu trả lời. `recall` từ lượt của B trả KPI của Lan (#13). "Known contacts" liệt kê mọi người | [CHẠY]+[MÃ] |

Nguồn các request: [evidence_trimmed.txt](file:///tmp/claude-0/-home-user-goclaw/bb0a0706-f1f8-5f7e-9855-c8b1acfcb3b8/scratchpad/verify/hivekeep/run/evidence_trimmed.txt). Nguồn mã: các link GitHub cố định theo commit ở trên.

Tiêu chí khác thay đổi theo bằng chứng mới:
- **R6 (mở rộng kênh):** xác nhận Đạt bằng [CHẠY] — đã chạy thật một adapter plugin qua `handleInboundWebhook`.
- **R8 (còn sống):** giữ Đạt nhưng yếu. Đã kiểm lại: tag cuối v1.10.0 ngày 2026-07-29, commit cuối 2026-09-17, khoảng 40 commit/tháng, gần như một tác giả. SDK trên npm dừng ở 0.10.0.
- **R1:** thêm [CHẠY] — provider `openai-compatible` trỏ vào endpoint riêng hoạt động.
- **R7:** không đổi (MIT).

### Inferences
- So với ghi chú cũ (`Nền tảng agent cho phòng Marketing/new_candidates_global.md`): kết luận "R5b Đạt" vẫn đúng ở mức nhận diện. Tuy vậy, bản cũ bỏ sót vấn đề **một thread cho mỗi agent**. Chính điều này làm 5b-in "đạt" một phần nhờ lịch sử chung, và đồng thời làm Privacy thất bại.
- Hạn chế "role 'external' gán cứng" không còn quan trọng, vì yêu cầu đã bỏ phân quyền người dùng.

### Gaps
- Chưa có ảnh chụp UI (ApprovalDialog, trang contact, cài đặt agent).

## Phải tự xây gì, có cần fork không

### Takeaway
Hai việc làm được bằng plugin, **không fork**: adapter Zalo (có thông tin nhóm) và các tool bổ trợ. Hai yêu cầu cốt lõi còn thiếu thì **phải fork hoặc sửa core**: (1) tách lịch sử và memory theo chat hoặc theo người để chặn rò, và (2) truyền danh tính người yêu cầu sang agent được ủy quyền (5d). Nguyên nhân là SDK không có điểm nào để sửa prompt hay lịch sử: `beforeChat` chỉ quan sát, và giá trị trả về của `beforeToolCall` bị bỏ qua.

### Cited Findings
- **Không cần fork (plugin):**
  1. **Kênh Zalo:** thêm `PluginExports.channels['zalo-oa']` cài `ChannelAdapter` với `handleInboundWebhook`, `sendMessage`, `start/stop` (tuỳ chọn thêm `listDestinations`). Host cung cấp route `POST /api/channels/plugin/<platform>/webhook/<channelId>`. Nên phát `metadata` gồm chat id, loại và tên nhóm; phần này sẽ vào prompt thành `<channel-context>`, giải quyết 5a cho Zalo — đã chạy mô phỏng [CHẠY] — [sdk index.ts L457–600](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/packages/sdk/src/index.ts#L457), [routes/channels.ts L136](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/routes/channels.ts#L136), [agent-engine.ts L3098–3117](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L3098)
  2. **Nhóm cho Telegram:** adapter có sẵn không phát metadata, nên phải chọn một trong hai. (a) Vá khoảng 5 dòng trong `telegram.ts` `processUpdate` để thêm `metadata: {chatId, chatType, chatTitle}`; đây là **sửa core**, nhỏ, có thể gửi upstream (MIT). (b) Viết một adapter Telegram dạng plugin với tên platform riêng. `registerPlugin` ghi đè theo key platform, nên về kỹ thuật có thể dùng lại tên `telegram`, nhưng chưa kiểm chứng [?] — [telegram.ts L238–247](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/channels/telegram.ts#L238), [channels/index.ts L24–27](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/channels/index.ts#L24)
  3. **Chức danh và phòng ban của agent ở mức mô tả:** ghi vào `role`/`expertise` là đủ để hiện trong prompt [CHẠY]. Muốn có sơ đồ tổ chức dạng dữ liệu, có thể viết plugin tool (ví dụ `org_lookup`) lưu trong `ctx.storage`; nhưng việc dùng dữ liệu đó vẫn do model tự quyết [MÃ] — [sdk index.ts L2657–2670](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/packages/sdk/src/index.ts#L2657)
  4. **Tự liên kết xuyên kênh** (ví dụ người dùng gõ mã): viết tool và route của plugin. SDK không có API để ghi `contact_platform_ids`, nên phải gọi REST `POST /api/contacts/:id/platform-ids` bằng phiên admin, hoặc import thẳng module server (không được SDK hỗ trợ) [?] — [routes/contacts.ts L435](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/routes/contacts.ts#L435)
  5. **Lách 5d không cần fork:** thêm chỉ dẫn vào persona hoặc global prompt (`PUT /api/settings/global-prompt`) để agent 1 luôn ghi "thay mặt <tên> (contact id …)" trong `task_description`/`message`, rồi agent 2 gọi `get_contact`. Cách này phụ thuộc model [?] — [settings.ts L110](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/routes/settings.ts#L110)
- **Cần fork hoặc vá core:**
  1. **Chặn rò (Privacy) mà vẫn giữ 5b-in:** sửa `buildMessageHistory(agentId)` ([agent-engine.ts L2986–3014](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L2986)) để lọc theo chat hoặc theo contact. Dữ liệu cần thiết đã có: `messages.channel_origin_id` → `channel_origins.platform_chat_id/platform_user_id` ([schema.ts L859–869](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L859)). Đồng thời phải sửa ba chỗ:
     - tính participants theo chat ([agent-engine.ts L3432–3460](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L3432));
     - compaction summaries và `agent_profiles` theo phạm vi ([schema.ts L223–281](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L223));
     - `searchMemories` lọc theo contact, ví dụ thêm cột `contact_id` vào `memories` ([memory.ts L423, L476](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/memory.ts#L423)).

     Không có hook nào làm được việc này.
  2. **5d chắc chắn:** truyền contact của người khởi tạo, tra qua `channel_origins.platformUserId` → `findContactByPlatformId`, vào ba chỗ: prompt của task (`spawnTask`), tin inter-agent (`sendInterAgentMessage`), và khối "Channel origin context" (hiện gán cứng `senderName: 'user'` và không in ra). Có thể dùng lại `enrichSpeakerFromContact` để chèn tên và ghi chú của A — [agent-engine.ts L1307–1321, L1433–1447](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L1307), [inter-agent.ts L67–118](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/inter-agent.ts#L67), [task-tools.ts L170–190](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/tools/task-tools.ts#L170)
  3. **Chèn ngữ cảnh theo người từ plugin:** nếu muốn plugin tự chèn fact theo người vào mỗi lượt, cần sửa `hookRegistry.execute('beforeChat', …)` để dùng kết quả trả về (ví dụ một trường `extraContext`) — [agent-engine.ts L1365–1369](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/agent-engine.ts#L1365)
  4. **Phòng ban có ý nghĩa vận hành** (định tuyến hay ủy quyền theo phòng ban): cần bảng mới và logic mới. Không có sẵn điểm mở rộng.

### Inferences
- Hướng ít fork nhất: chấp nhận fork nhỏ ở hai điểm (lọc lịch sử theo chat/contact, và truyền danh tính người khởi tạo sang task hoặc inter-agent), cộng một plugin Zalo. Nếu bỏ qua fork, Hivekeep chỉ dùng an toàn được khi mọi người trong mọi nhóm của agent được phép thấy thông tin của nhau.
- Cần cảnh báo: phần mã lõi liên quan (`agent-engine.ts` khoảng 3.600 dòng) đang ít thay đổi (khoảng 40 commit/tháng). Nhờ vậy duy trì fork bớt khó, nhưng khả năng upstream nhận bản vá "tách phiên theo chat" là chưa rõ, vì nó đi ngược thiết kế "một phiên liên tục".

### Gaps
- Chưa thử viết bản vá. Công sức sửa `buildMessageHistory` và compaction (tách summary theo phạm vi) chưa được ước lượng bằng thực nghiệm.
