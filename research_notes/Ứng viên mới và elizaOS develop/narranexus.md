# NarraNexus (NetMindAI-Open/NarraNexus): kiểm mã và chạy thật theo bộ tiêu chí cuối (D1, K1–K5, 5d, R1/R6/R7/R8)

**Phạm vi và cách làm.** Kiểm ngày 2026-09-27 (đã xác nhận bằng `date`). Commit kiểm là `5869502c9a405b3e762206ecd21ea16540d75794` (tag v1.15.0, 2026-08-05). Đây cũng là HEAD của `main` vào ngày kiểm, không có commit mới hơn. Mọi dẫn chiếu `đường/dẫn#Lx` bên dưới đều thuộc commit này; tiền tố URL là `https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/`.

Nhãn bằng chứng:
- **[MÃ]**: đã đọc mã.
- **[CHẠY]**: đã chạy thật với stub LLM.
- **[DOC]**: lấy từ tài liệu.
- **[?]**: suy luận, chưa kiểm chứng.

Bằng chứng chạy (đã cắt gọn, 28 KB): `research_notes/Ứng viên mới và elizaOS develop/evidence/narranexus_run_evidence.txt`.

**Cách chạy [CHẠY]:**
- **Môi trường.** Python 3.13, `uv sync --frozen`. Dịch vụ được chạy giống chế độ container của `run.sh`: `sqlite_proxy_server` (:8100), `uvicorn backend.main:app` (:8000), `module_runner mcp` (:7801–7835) và `run_worker_supervisor` (các trigger kênh cùng MessageBus). HOME và DB được đặt trong scratchpad.
- **LLM.** Tạo provider kiểu `openai` tuỳ chỉnh, trỏ vào stub LLM ở `http://127.0.0.1:18101/v1`. Framework của owner đặt là `nexus_power` (vòng lặp native, không dùng CLI). Hai slot `agent` và `helper_llm` đều gắn vào stub.
- **Dữ liệu thử.** Tạo qua REST API thật (header `X-User-Id`, chế độ local):
  - user `admin_ha` ("Admin Hà");
  - team "Phòng Marketing", `lead_agent_id` là agent 1;
  - agent 1 "Content Lead – Phòng Marketing", agent 2 "Copywriter – Phòng Marketing", và thêm agent 3 "Copywriter 2" để thử 5d;
  - persona đặt qua `PUT /api/agents/{id}/awareness`;
  - mỗi agent một bot Telegram, gắn qua `POST /api/telegram/bind` với `owner_username=adminha`.
- **Cách tiêm tin nhắn.** Tin nhắn đi qua **đường inbound thật**: long-poll `getUpdates` → `TelegramTrigger.parse_event` → `ChannelTriggerBase` (dedup, debounce, worker) → `AgentRuntime`. Payload `message` giả lập được một **Telegram Bot API giả** (tự viết, chạy cục bộ) trả về.
- **Sai khác so với production:**
  1. Sửa 1 dòng trong `telegram_sdk_client.py` để đọc `_API_BASE` từ biến môi trường `TG_API_BASE_OVERRIDE`. Diff nằm trong file bằng chứng.
  2. Token bot là token giả nhưng đúng định dạng. Không tạo bot hay tài khoản thật nào.
  3. Stub không suy luận, nên câu trả lời của các lời gọi helper (tóm tắt người, trích quan sát) được **viết sẵn đúng như một LLM trung thực sẽ trả**. Ví dụ, lời gọi "Summarize…" cho tin "KPI tháng 10 của mình là 50 bài" trả `{"summary":"Lan cho biết KPI tháng 10 của Lan là 50 bài"}`.
  4. Hai lần stub được viết sẵn để gọi tool: `bus_send_to_agent` khi thử 5d, và `update_awareness` khi thử kẻ mạo danh, với mục đích kiểm xem nền tảng có **chặn** hay không.
  5. Mọi thứ khác là mã thật: nền tảng tự chọn key, tự lắp prompt và tự ghi bộ nhớ.

---

## Câu hỏi 1: Danh tính (5a, 5b-in, 5b-cross). Khoá thực thể người là gì? Khi nào rơi xuống khớp theo tên? Bộ nhớ có tách theo người không? Gộp và gỡ gộp ra sao?

### Takeaway
Ghi chú cũ nói có "thực thể người khoá theo `user_id`". Điều này đúng về tên cột nhưng **sai về ý nghĩa**. `AgentRuntime` ghi đè `user_id` của **mọi** lượt thành **chủ (creator) của agent**. Hệ quả là mọi người gửi trên Telegram (Lan, Minh, kẻ mạo danh…) đều dùng chung **một** thực thể `entity_id=admin_ha`. Tóm tắt về Lan và Minh bị ghi vào cùng thực thể đó, rồi thẻ "Current User Information" của thực thể này được bơm vào prompt của **mọi** người [MÃ][CHẠY]. Như vậy 5a đạt một phần (có sender id, kênh và chat id trên từng tin), còn 5b-in và 5b-cross coi như **không có**.

### Cited Findings
- **Ghi đè user_id [MÃ].** `agent_runtime/agent_runtime.py#L358-L366` có chú thích "Override user_id with agent's creator — all triggers share a single workspace", sau đó gán `user_id = _agent.created_by` — [agent_runtime.py#L358](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/agent_runtime/agent_runtime.py#L358-L366)
- **Kênh IM chạy agent dưới danh nghĩa owner [MÃ].** Kênh gọi `run_and_collect(user_id=owner_user_id)`, trong đó `owner_user_id = await self._resolve_agent_owner(agent_id)`. Người gửi thật chỉ được mang theo trong `ChannelTag(channel, sender_name, sender_id, room_id)` — [channel_trigger_base.py#L1460-L1504](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/channel/channel_trigger_base.py#L1460-L1504)
- **5a: định danh trên từng tin [MÃ][CHẠY].**
  - `sender_id` lấy từ `message.from.id` (ID số do Telegram cung cấp) — [telegram_trigger.py#L397](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/telegram_module/telegram_trigger.py#L397)
  - Mọi prompt đã bắt được đều mở đầu bằng thẻ dạng `[Telegram · Lan · 1001 · -100111]`, rồi đến "Sender: Lan (`1001`)" và "Conversation Type: Group Room" (file bằng chứng, các lượt t1–a2).
- **Lỗi quy người nói trong lịch sử nhóm [MÃ][CHẠY].** Trong lịch sử nhóm, mọi dòng không phải của bot đều bị gán tên của **người đang gửi** (`sender = … self._message.sender_name or from_agent`) — [telegram_context_builder.py#L125-L131](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/telegram_module/telegram_context_builder.py#L125-L131). Chạy thật cho thấy:
  - ở lượt của Minh trong G1, câu "Mình là Lan…" hiện ra là **"Minh:"**;
  - ở lượt sau của Lan, câu "Mình là Minh." hiện ra là **"Lan:"** (file bằng chứng, `t2_g1_minh` và `k1b_g1_lan_a1`).
- **Không tra hồ sơ người gửi theo sender_id [MÃ][CHẠY].** "Sender Profile" trên Telegram luôn là "first interaction… No prior information", vì `TelegramContextBuilder` không override `get_sender_entity`, và bản ở lớp cha trả `None` — [channel_context_builder_base.py#L167](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/channel/channel_context_builder_base.py#L167-L185)
- **Khoá chính xác của thực thể và khi nào khớp theo tên [MÃ].**
  - `hook_data_gathering` tra `get_entity(entity_id=ctx_data.user_id, instance_id)`, trong đó `ctx_data.user_id` là owner. Nếu không có, nó gọi `_fuzzy_find_entity`, hàm này `keyword_search` theo `channel_tag.sender_name` trên tên, mô tả, keywords và aliases, rồi lấy bản ghi có `interaction_count` cao nhất — [social_network_module.py#L205-L216](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/social_network_module/social_network_module.py#L205-L216), [#L646-L701](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/social_network_module/social_network_module.py#L646-L701)
  - Bản ghi nằm trong `memory_entity` với `scope_type='instance'` và `scope_id` là instance SocialNetworkModule **của từng agent**; `attributes.entity_id` là `admin_ha` (DB dump) [CHẠY].
- **Nhánh khớp theo tên thực tế gần như chỉ chạy ở lượt đầu tiên [MÃ][CHẠY].**
  - `hook_after_event_execution` dùng `params.user_id` (tức owner). Nếu chưa có thực thể, nó "creating minimal entity" cho owner rồi **append** tóm tắt của lượt vào mô tả — [social_network_module.py#L386-L425](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/social_network_module/social_network_module.py#L386-L425)
  - Vì vậy từ lượt thứ hai trở đi, nhánh chính luôn trúng thực thể của owner, và người lạ nào cũng thấy "You already know this user: Name: admin_ha…".
  - Rủi ro mạo danh bằng tên (K4/K5) chỉ còn ở lượt đầu tiên của mỗi agent, hoặc khi thực thể owner bị xoá. Lúc đó một người đặt tên hiển thị "Lan" sẽ nhận được thẻ của thực thể có tên hoặc mô tả chứa "Lan" [MÃ].
- **Mọi người gửi bị dồn vào một thực thể [CHẠY].** Sau 3 lượt ở G1/G2, bảng `memory_entity` của agent 1 chỉ có **một** thực thể: `entity_id=admin_ha`, mô tả là "Lan giới thiệu: phụ trách fanpage X… / Minh giới thiệu bản thân / Lan cho biết KPI tháng 10 của Lan là 50 bài". Thẻ này được bơm vào DM của Lan, DM của Minh, DM của Admin Hà và DM của kẻ mạo danh (file bằng chứng, mục "DB: memory_entity" và các lượt t4, t5, a1, a2).
- **5b-in theo nghĩa đen: Lan thấy thông tin của mình, nhưng không vì được nhận ra [CHẠY].** Trong DM(Lan) ở lượt t4, prompt có "KPI tháng 10 của Lan là 50 bài" và "fanpage X". Nguồn là (a) thẻ thực thể `admin_ha`, (b) bộ nhớ `observation` cấp agent, (c) khối "Unread Messages". Đây không phải bộ nhớ khoá theo Lan, vì cùng nội dung đó cũng hiện với Minh.
- **Gộp danh tính (cross-channel) [MÃ].**
  - Prompt yêu cầu LLM gọi `merge_entities` khi "same person from different channels" — [prompts.py#L94](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/social_network_module/prompts.py#L94)
  - Tool gộp source vào target rồi **xoá source** (`repo.delete_entity(source_entity_id)`). Không có lịch sử gộp, không có thao tác gỡ gộp — [_social_mcp_tools.py#L355-L456](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/social_network_module/_social_mcp_tools.py#L355-L456)
  - Với bên thứ ba được nhắc tới trong hội thoại: khớp chính xác theo name hoặc alias. Nếu ra hơn 1 ứng viên thì `decide_merge_or_create` (LLM) quyết định. Chặng vector-similarity đã bị gỡ từ 2026-05-27 — [social_network_module.py#L496-L560](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/social_network_module/social_network_module.py#L496-L560)
  - Schema có `aliases`, `identity_info` và `contact_info.channels.<kênh>`, nhưng chỉ được điền khi LLM tự gọi `extract_entity_info` — [entity_schema.py#L58-L75](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/schema/entity_schema.py#L58-L75)
- **Prompt còn tự hướng LLM vào đúng khoá sai [MÃ].** Hướng dẫn trong prompt ghi "For current user: use existing `user_id` from context", mà `user_id` trong context lại là `admin_ha` (xem prompt đã bắt: "User ID: `admin_ha`") — [prompts.py#L64](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/social_network_module/prompts.py#L64)
- **Web chat cũng dồn về owner [MÃ].** Websocket gửi `sender_user_id`, nhưng giá trị này chỉ được BasicInfo dùng (để tính is_creator). Social Network vẫn khoá theo `user_id` là owner — [websocket.py#L855-L861](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/backend/routes/websocket.py#L855-L861)

### Inferences
- Thiết kế này nhất quán với định vị "one-person company": chỉ có **một** con người thật (owner), còn người trên kênh IM là "đối tác". Đây là khác biệt về mô hình, không phải một lỗi nhỏ cần vá. Muốn có "bộ nhớ theo người" thì phải bỏ phép ghi đè `user_id`, hoặc khoá thực thể theo `(channel, sender_id)` ở mọi hook, cả ghi lẫn đọc [?].
- Không có danh bạ trung tâm. Kho thực thể nằm riêng trong từng agent (theo instance), nên cùng một người sẽ có N bản ghi ở N agent [MÃ].

### Gaps
- Chưa chạy Lan trên kênh thứ hai (Slack/Discord/Lark/web), vì mỗi kênh cần thêm một API giả. 5b-cross chỉ kết luận từ mã: không có bảng liên kết danh tính; việc gộp phụ thuộc LLM gọi `merge_entities`.
- Chưa thử kịch bản LLM thật tự gọi `extract_entity_info`, chẳng hạn với `entity_id="1001"`. Nếu nó làm vậy thì có thể phát sinh thực thể riêng cho Lan, nhưng thẻ tự động vẫn tra theo `admin_ha` [?].

---

## Câu hỏi 2: Quyền riêng tư (K4) và admin (K5). Có rò thông tin người X sang người Y không? Có admin gắn qua chat bằng ID nền tảng không? Kẻ mạo danh có bị chặn không?

### Takeaway
**K4 trượt nặng [CHẠY].** Ở lượt DM(Minh) hỏi "Lan có KPI bao nhiêu?", prompt của agent 1 chứa KPI của Lan qua **4 đường độc lập**. Trong đó có một đường tất định, không cần LLM: nguyên văn tin nhắn G2 của Lan nằm trong khối "Unread Messages".

**K5 đạt một phần.** Mỗi agent có khái niệm "owner" trên Telegram, gắn theo **ID số đã xác thực**: username được khoá lúc bind, rồi được đổi thành `from.id` ở DM đầu tiên. Kẻ mạo danh trùng tên hiển thị bị gắn nhãn "NOT the owner". Tuy vậy:
- đây chỉ là **tín hiệu trong prompt**;
- phạm vi là từng agent, không phải cả hệ thống;
- BasicInfo lại khẳng định mọi người gửi qua IM đều là "Creator";
- không có chặn nào ở tầng mã. Khi LLM làm theo kẻ mạo danh, `update_awareness` **thành công** và xoá luôn các quy tắc persona.

### Cited Findings
- **4 đường rò sang DM(Minh), lượt t5 [CHẠY]:**
  1. **"Current User Information"**: thẻ `admin_ha` có dòng "Lan cho biết KPI tháng 10 của Lan là 50 bài" (hook tự động, khoá theo owner).
  2. **"What you remember"**: `[observation] KPI tháng 10 của Lan là 50 bài`. Kind `observation` có `passive=True` và `default_scope="agent"`, tức được bơm tự động mỗi lượt cho mọi người gửi — [memory/specs.py#L103-L145](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/memory/specs.py#L103-L145)
  3. **"### Unread Messages: 8"**: có dòng `[MessageBus · telegram_user_1001 · telegram_-100222] @bot… Nhớ giúp: KPI tháng 10 của mình là 50 bài.`. Nguyên nhân là `ChannelInboxWriter` ghi mọi tin IM vào `bus_messages`, và MessageBusModule bơm tin chưa đọc của **mọi** kênh vào turn context — [channel_inbox_writer.py#L85](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/channel/channel_inbox_writer.py#L85), [message_bus_module.py#L306-L312](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/message_bus_module/message_bus_module.py#L306-L312)
  4. **Narrative**: "Created based on query: [From Lan] … Mình là Lan, phụ trách fanpage X…". Narrative gắn theo agent và owner nên dùng chung cho mọi người gửi.
- **Rò chéo giữa các agent do trùng channel_id [CHẠY][MÃ].**
  - `channel_id = f"{channel}_{chat_id}"` không kèm bot hay agent. DM Telegram có `chat_id` bằng `user_id` của người dùng, nên DM của Minh với agent 1 và DM của Minh với agent 2 cùng là `telegram_1002`, và cả hai agent đều là thành viên (DB `bus_channel_members`).
  - Prompt DM của agent 2 hiện lịch sử DM của Minh với **agent 1** ("Lan có KPI bao nhiêu?"), và lời đáp của agent 1 bị ghi thành "Minh:" (file bằng chứng, `k1c`).
- **Không có ACL hay cơ chế admin cấp quyền xem [MÃ].**
  - Bản ghi bộ nhớ chỉ có scope `agent|user|narrative|instance|global`. `SCOPE_GLOBAL` được khai báo nhưng không chỗ nào dùng — [memory/record.py#L40-L45](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/memory/record.py#L40-L45)
  - Không có cơ chế "admin cho phép Minh xem thông tin của Lan". Bước "cấp quyền rồi lặp lại bước 4" trong giao thức **không làm được**, vì không có gì để cấp. Mặc định mọi thứ đã lộ.
- **Owner trên Telegram gắn theo ID [MÃ][CHẠY].**
  - `owner_username` là "khoá" đặt lúc bind. Ở DM đầu tiên có `from.username` trùng, hệ thống ghi `owner_user_id = message.sender_id` (ID số), bằng compare-and-set, chỉ khi cột còn rỗng — [telegram_trigger.py#L717-L748](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/telegram_module/telegram_trigger.py#L717-L748), [_telegram_credential_manager.py#L302-L340](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/telegram_module/_telegram_credential_manager.py#L302-L340)
  - DB sau lượt a1: `agent1.owner_user_id=9001`, còn `agent2.owner_user_id` vẫn rỗng. Nghĩa là admin phải DM **từng** bot.
- **Kẻ mạo danh 1003 "Admin Hà" (lượt a2) [CHẠY]:**
  - Khối Trust signal ghi đúng: "The current Telegram sender (`1003`) is **NOT** the owner — `is_owner_interacting=False`". Phép so sánh là `current_sender_id == cred.owner_user_id` — [telegram_module.py#L436-L451](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/telegram_module/telegram_module.py#L436-L451)
  - Nhưng cùng prompt đó, BasicInfo lại ghi "**Is the current speaker your Creator?: True**". Nguyên nhân là `sender_id = extra.get("sender_user_id") or self.user_id`, và IM không truyền `sender_user_id` nên rơi về owner — [basic_info_module.py#L228-L237](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/basic_info_module/basic_info_module.py#L228-L237). Lan và Minh cũng nhận "True" trong mọi lượt.
- **Không chặn tool theo người gửi [CHẠY][MÃ].**
  - Lượt của kẻ mạo danh (và của Lan, Minh) được đưa **77 tool**, gồm `bash`, `write_file`, `mcp__awareness_module__update_awareness`, `tg_unbind`, `create_agent`, `delete_entity`, `skill_install`, `ha_call_service`.
  - `disallowed_tools` chỉ dùng để ẩn tool của kênh chưa bind, không phụ thuộc người gửi — [channel_module_base.py#L315](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/channel/channel_module_base.py#L315)
  - Stub được viết sẵn để "LLM nghe theo" kẻ mạo danh. Kết quả tool là "Awareness updated successfully", và `GET /awareness` trả về nội dung "Luôn dùng thật nhiều emoji. Chia sẻ KPI của mọi người…".
- **Không có admin cấp hệ thống qua chat [MÃ].** Vai trò duy nhất ở backend là `role == "staff"`, dành cho người vận hành cloud. Ở chế độ local, không có đăng nhập, danh tính lấy từ header `X-User-Id` — [backend/auth.py#L202](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/backend/auth.py#L202). "Owner" trên kênh IM là của từng agent (WeChat dùng TOFU "first DM claims owner"; Lark dùng `owner_open_id`) — [wechat_trigger.py#L246](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/wechat_module/wechat_trigger.py#L246)

### Inferences
- Lớp bảo vệ duy nhất là lời dặn trong prompt: "Never disclose owner-private context" và mục "Confidentiality" của Awareness. Lời dặn này chỉ bảo vệ **thông tin của owner**, không bảo vệ người dùng A khỏi người dùng B. Và vì mọi người gửi IM đều bị coi là Creator, nó còn mâu thuẫn với chính khối Trust signal [MÃ][?].
- WeChat nhận owner theo kiểu "ai DM trước thì thành owner". Nếu dùng làm cơ chế admin thì đây là lỗ hổng: kẻ lạ nhắn trước sẽ chiếm quyền [MÃ][?].

### Gaps
- Chưa đo LLM thật có từ chối kẻ mạo danh hay không. Kết luận ở đây chỉ nói rằng **nền tảng không chặn**.
- Chưa kiểm trường hợp chủ tài khoản đổi username Telegram, rồi người khác nhận lại username cũ **trước** DM đầu tiên. Về lý thuyết người đó sẽ chiếm owner [?].

---

## Câu hỏi 3: Đa agent và phòng ban (D1), bàn giao có mang người yêu cầu không (5d)

### Takeaway
Nền tảng có **team** (tên, mô tả, `lead_agent_id`) và giao tiếp agent–agent qua MessageBus (DM, room, @mention). Nhưng:
- **không có chức danh hay phòng ban dạng dữ liệu** cho agent;
- không có giao việc theo vai trò;
- không có review hay approval;
- cấu trúc tổ chức chỉ định tuyến đúng một trường hợp: tin trong team chat trên web không @ai thì giao cho lead.

Việc bàn giao do LLM tự quyết, và **không mang theo người yêu cầu** (5d trượt) [MÃ][CHẠY].

### Cited Findings
- **Schema tổ chức [MÃ].** `Team` gồm `team_id, owner_user_id, name, description, color, intro_md, lead_agent_id`. `TeamMember` chỉ có `team_id` và `agent_id`, không có vai trò — [team_schema.py#L21-L40](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/schema/team_schema.py#L21-L40). `Agent` chỉ có `agent_name, agent_description, agent_type, is_public` — [entity_schema.py#L168-L181](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/schema/entity_schema.py#L168-L181)
- **Định tuyến trong team chat web [MÃ].** "No @mention → route to the team's default responder… it can @-delegate from there" — [backend/routes/teams.py#L251-L256](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/backend/routes/teams.py#L251-L256)
- **Job không có assignee hay approval [MÃ].** Job chỉ gồm `agent_id` (agent vừa tạo vừa chạy job), `user_id` (người nhận thông báo) và `payload` — [job_schema.py#L214-L260](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/schema/job_schema.py#L214-L260)
- **Vai trò là chữ tự do [MÃ][DOC].** Chức năng của từng agent nằm trong Awareness hoặc mô tả dạng văn bản. README mô tả các template như "6 agents deliver an analyst-grade HTML briefing", và các agent "hold roles like project manager… communicating, splitting work, and handing off tasks over the MessageBus" — [README.md](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/README.md)
- **5d, bàn giao sạch từ agent 1 sang agent 3 [CHẠY].**
  - Stub gọi `bus_send_to_agent(content="Viết 3 caption cho fanpage X…")` từ DM(Lan).
  - Prompt của agent 3 chỉ có `From: agent_195163e3506b`, nội dung, và "Is the current speaker your Creator?: True" (Admin Hà).
  - Kiểm theo chuỗi: **"Lan" 0 lần, "1001" 0 lần**. Tool chỉ nhận `agent_id, to_agent_id, content, attachment_refs`, không có trường "on behalf of" — [_message_bus_mcp_tools.py#L302-L356](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/message_bus_module/_message_bus_mcp_tools.py#L302-L356)
- **Lỗi thật: bàn giao 1 → 2 bị mất [CHẠY][MÃ].**
  - `send_to_agent` tìm một kênh `direct` sẵn có mà cả hai agent đều là thành viên — [local_bus.py#L256-L266](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/message_bus/local_bus.py#L256-L266). Nó chọn trúng kênh IM `telegram_1002` (bị trùng như đã nêu ở câu 2).
  - Tin được ghi vào đó, nhưng MessageBusTrigger **bỏ qua** các kênh có prefix `telegram_` — [message_bus_trigger.py#L108-L132](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/message_bus/message_bus_trigger.py#L108-L132)
  - Kết quả: tool trả `success:true`, nhưng **agent 2 không bao giờ được kích hoạt**. Sau 45 giây không có lượt nào của agent 2 (DB `bus_messages`).

### Inferences
- Để có "phòng ban vận hành" kiểu Dewee (Leader → chia task → giao theo vai trò → review), phải tự xây gần như toàn bộ lớp tổ chức: vai trò và phòng ban, bảng task có assignee và trạng thái review, và định tuyến theo vai trò [?].
- Lỗi trùng `channel_id` cho thấy kênh IM và MessageBus dùng chung một không gian tên mà không phân vùng theo agent. Với một phòng Marketing nhiều agent cùng tiếp một nhân viên qua DM, lỗi này sẽ xảy ra ngay [?].

### Gaps
- Chưa chạy team chat trên web (UI frontend không build) để xem lead chia việc; phần này chỉ đọc mã.
- Chưa đếm số vòng hội thoại agent–agent với LLM thật. CLAUDE.md của dự án cấm mọi giới hạn cứng số vòng lặp (iron rule #14).

---

## Câu hỏi 4: Kho tri thức chung (K1) và quy tắc persona (K3)

### Takeaway
- **K1: không có** kho tri thức hay RAG chung. Gần nhất là "Team shared folder" trên hệ thống tệp, nhưng nó chỉ được nhắc tới trong prompt team chat trên web. Với runtime native `nexus_power`, agent **thậm chí không đọc được** thư mục đó (`read_file` bị từ chối vì nằm ngoài workspace) [CHẠY].
- **K3 đạt về hiển thị, hỏng về toàn vẹn.** Quy tắc persona trong Awareness xuất hiện trong **mọi** prompt của agent 1 (nhóm lẫn DM) [CHẠY]. Nhưng Awareness là trạng thái có thể sửa được: agent được dặn tự cập nhật khi "user" nêu sở thích, và bất kỳ ai nhắn tới cũng kích hoạt được việc này (đã chứng minh ở câu 2).

### Cited Findings
- **Thử K1 [CHẠY].**
  - Tài liệu "Brand guideline: slogan 'Nhanh như chớp'; giá gói Pro 199.000đ" được đặt vào `{BASE}/admin_ha/_shared/teams/<team_id>/brand_guideline.md`, đúng đường dẫn `team_shared_dir` — [workspace_paths.py#L94-L98](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/utils/workspace_paths.py#L94-L98)
  - Với agent 2 ở DM(Minh) hỏi "Slogan công ty là gì?" và agent 1 ở G1 hỏi "Gói Pro giá bao nhiêu?", các chuỗi "Nhanh như chớp", "199.000", "brand_guideline" và "_shared" đều xuất hiện **0 lần** trong prompt.
  - Khi stub gọi `read_file(<đường dẫn tuyệt đối>)`, kết quả là `ERROR: denied: path … resolves outside the workspace` — [policy.py#L83-L108](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/agent_framework/nexus_power/_nexus_power_impl/tooling/policy.py#L83-L108)
- **Chỗ duy nhất trỏ tới thư mục chung [MÃ].** Dòng "Team shared folder: {shared} — … open them with the Read tool" chỉ nằm trong `_build_team_prompt`, tức team chat trên web — [message_bus_trigger.py#L982-L990](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/message_bus/message_bus_trigger.py#L982-L990)
- **Bộ nhớ không có kind "document" [MÃ].** Các kind hiện có là event, bus, narrative, entity, job, observation, đều mặc định scope `agent`. Đường embedding đã bị gỡ (2026-05-27), recall dựa trên chữ và độ mới — [memory/specs.py#L77-L145](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/memory/specs.py#L77-L145)
- **Các phương án thay thế [MÃ][DOC].** Skills và MCP được cài theo từng agent ("Per-agent Skills and MCP toolsets", README). Có thể nhét SOP vào SKILL.md hoặc Awareness của **từng** agent. Cách này không phải kho dùng chung và phải nạp tay [?].
- **Persona có mặt ở mọi prompt [CHẠY].** Chuỗi "Luôn xưng em, gọi người dùng là anh/chị, không dùng emoji, không bàn chính trị" có trong 10/10 prompt vòng lặp chính của agent 1 (G1, G2, DM Lan, DM Minh, DM Admin, DM kẻ mạo danh), dưới mục "##### 6. Your Current Awareness Profile".
- **Persona dễ bị ghi đè [MÃ].** `update_awareness` hướng dẫn LLM cập nhật "**Immediately** when user: Gives explicit preference… Defines agent role…" và không kiểm tra ai là người gửi — [awareness_module.py#L161-L265](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/awareness_module/awareness_module.py#L161-L265)

### Inferences
- K1 phải tự xây: kho tài liệu có phạm vi (theo team hoặc phòng ban), nạp bằng upload, URL hoặc folder sync, cộng với tìm kiếm hoặc bơm RAG. Cũng phải mở quyền đọc thư mục chung cho `nexus_power` [?].
- Với K3 cần khoá Awareness: chỉ admin được sửa, hoặc tách "quy tắc cứng" (bất biến) khỏi "sở thích học được" [?].

### Gaps
- Chưa thử `claude_code` (Claude CLI) có đọc được thư mục chung ở chế độ local hay không. Dù đọc được, framework đó vẫn trượt R1.

---

## Câu hỏi 5: Kênh (Telegram, Zalo, interface adapter), backend LLM (R1), giấy phép (R7), nhịp phát triển (R8), ngôn ngữ tài liệu

### Takeaway
- Kênh có sẵn: Telegram, Slack, Discord, Lark/Feishu, WeChat (tài khoản cá nhân qua iLink), NarraMessenger (Matrix). **Không có Zalo.** Có lớp nền `ChannelTriggerBase` tốt (dedup, debounce, worker pool, audit), nhưng muốn thêm kênh vẫn phải sửa nhiều file lõi.
- R1 đạt **khi cấu hình** `nexus_power` (vòng lặp native dùng API key của mình, đã chạy thật). Tuy nhiên framework mặc định là `claude_code` (spawn Claude CLI), và `run.sh` coi Claude CLI là "HARD dependency".
- Giấy phép Apache-2.0.
- Bản mới nhất v1.15.0 ngày 2026-08-05. Có 8 bản phát hành từ 2026-07-02, nhưng tính đến 2026-09-27 đã **53 ngày im lặng**.

### Cited Findings
- **Framework agent-loop [MÃ].**
  - `DEFAULT_AGENT_LOOP_FRAMEWORK = "claude_code"` — [driver.py#L76](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/agent_framework/loop/driver.py#L76)
  - Ba framework được đăng ký là `claude_code`, `nexus_power` và `codex_cli` — [agent_framework/__init__.py#L38-L57](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/agent_framework/__init__.py#L38-L57)
  - Nếu thiếu cấu hình, hệ thống lùi về "claude_code" — [step_3_agent_loop.py#L57-L96](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/agent_runtime/_agent_runtime_steps/step_3_agent_loop.py#L57-L96)
  - `run.sh` ghi "Install Claude Code CLI … HARD dependency" — [run.sh#L188](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/run.sh#L188)
- **R1 chạy thật [CHẠY].** Với `POST /api/providers/agent-framework {"framework":"nexus_power"}` và provider OpenAI tuỳ chỉnh trỏ vào stub, log ghi "agent_loop framework: 'nexus_power'". Một tin nhắn vào sinh khoảng 8–9 request tới LLM: 1 vòng lặp chính cộng 7–8 lời gọi helper (khớp chủ đề ×2, cập nhật narrative ×2, trích observation, trích thực thể, tóm tắt, suy persona).
- **Thêm một kênh phải sửa lõi [MÃ].**
  - Adapter kế thừa `ChannelTriggerBase` và override các hàm connect, parse_event, … (Telegram: 843 dòng trigger, tổng module 2.612 dòng).
  - Đăng ký kênh thì nằm rải trong lõi: `_TRIGGER_SPECS` — [channel_trigger_map.py#L57](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/channel_trigger_map.py#L57); registry module — [module/__init__.py#L57-L76](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/__init__.py#L57-L76); enum `WorkingSource`; schema_registry (bảng credential); `backend/main.py` cùng route; bundle; frontend.
  - `grep` cho thấy 33 file Python ngoài `telegram_module/` và 21 file frontend có nhắc "telegram".
- **Giấy phép [MÃ].** `LICENSE` là Apache License 2.0; `pyproject.toml` ghi `license = {text = "Apache-2.0"}`.
- **Nhịp phát triển [MÃ][DOC].**
  - `git log` từ 2026-06-27 có **10 commit**, tất cả là "release: vX — sync from protagolabs/main" (v1.8.4 ngày 2026-07-02 … v1.15.0 ngày 2026-08-05).
  - Tổng 109 commit; 90 commit của Bin Liang.
  - Trang Releases hiển thị v1.15.0 (2026-08-05) là bản mới nhất, 86 sao — [GitHub Releases](https://github.com/NetMindAI-Open/NarraNexus/releases)
  - Repo công khai là **bản mirror được squash** từ repo riêng `protagolabs/main`.
- **Ngôn ngữ [DOC][MÃ].** README có bản tiếng Anh và bản tiếng Trung (`README_zh.md`). Mã và chú thích bằng tiếng Anh. Một số ví dụ trong prompt dùng tiếng Trung ("好的", "收到"). CLAUDE.md có "iron rules", trong đó quy tắc 11 ghi "Only the Owner (Bin哥) edits CLAUDE.md".
- **Telemetry [MÃ].** PostHog bật khi `NARRA_ANALYTICS_ENABLED` (mặc định "true") **và** có `POSTHOG_API_KEY`. Không thấy key cài sẵn trong mã nguồn, nên khi chạy từ source thì telemetry tắt — [analytics/__init__.py#L69](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/analytics/__init__.py#L69)

### Inferences
- Adapter Zalo (OA API hoặc Zalo cá nhân) viết được theo mẫu Telegram hoặc WeChat, nhưng bắt buộc phải sửa lõi, tức là fork [?].
- "Đạt R8" chỉ theo nghĩa hẹp: có release sau 2026-06-27. Đội nhỏ, repo công khai chỉ là bản đồng bộ, và đã ngưng từ 2026-08-05. Rủi ro bảo trì cao [?].

### Gaps
- Không kiểm được repo riêng `protagolabs/main` và lộ trình.
- Chưa build frontend và bản DMG.

---

## Kết luận: có dùng làm nền cho "agent company" phòng Marketing được không?

### Takeaway
**Không nên dùng làm nền.** NarraNexus được thiết kế cho **một con người (owner) với nhiều agent**. Mọi người gửi khác bị dồn vào danh tính của owner. Cả bộ nhớ lẫn "Creator" đều theo owner, nên K2, K4 và 5d hỏng ở tầng kiến trúc chứ không phải ở chi tiết. Nó chỉ đáng tham khảo **từng thành phần**:
- bộ nhớ Narrative/Observation có yếu tố thời gian (bi-temporal);
- `ChannelTriggerBase` (dedup, debounce, backoff);
- mẫu "owner trust signal" theo ID số của Telegram;
- runtime `nexus_power` dùng được nhiều provider.

### Cited Findings

| Tiêu chí | Kết quả | Bằng chứng chính | Nhãn |
|---|---|---|---|
| D1 Phòng ban/vai trò điều phối | **Không** (chỉ có team + `lead_agent_id` làm người trả lời mặc định trong team chat web) | `Team`/`TeamMember` không có role; job không có assignee/review; bàn giao do LLM gọi bus | [MÃ] |
| K1 Kho tri thức chung | **Không** | Doc ở thư mục chung team: 0 lần xuất hiện trong prompt; `read_file` bị từ chối (ngoài workspace); không có kind "document"/RAG | [CHẠY][MÃ] |
| K2-5a Định danh trên từng tin | **Một phần** | Thẻ `[Telegram · Lan · 1001 · -100111]` + Sender id trên mọi tin; nhưng lịch sử nhóm gán sai người nói (Lan↔Minh), "Sender Profile" không tra theo id | [CHẠY][MÃ] |
| K2-5b-in Cùng người qua nhóm/DM, bộ nhớ theo người | **Không** | Mọi người gửi dồn vào thực thể `entity_id=admin_ha` (owner); thông tin của Lan hiện cho mọi người | [CHẠY] |
| K2-5b-cross Cùng người qua kênh | **Không** | Không có bảng liên kết; chỉ `merge_entities` do LLM gọi, xoá source, không gỡ được; kho thực thể riêng từng agent | [MÃ] |
| K3 Quy tắc persona | **Một phần** | Quy tắc có ở 10/10 prompt của agent 1 (nhóm + DM); nhưng `update_awareness` không chặn theo người gửi → kẻ mạo danh ghi đè được | [CHẠY] |
| K4 Riêng tư + ngoại lệ admin | **Không** | KPI của Lan lọt vào DM(Minh) qua 4 đường (thẻ thực thể, observation, Unread Messages nguyên văn, narrative); rò chéo agent do trùng `telegram_1002`; không có ACL hay cơ chế cấp quyền | [CHẠY][MÃ] |
| K5 Admin gắn qua chat bằng ID | **Một phần** | Owner mỗi agent: khoá theo username rồi thành `owner_user_id=9001` (ID số); 1003 "Admin Hà" bị gắn "NOT the owner"; nhưng chỉ là tín hiệu trong prompt, BasicInfo vẫn "Creator: True", không chặn tool, phải gắn riêng từng bot, không có admin toàn hệ thống | [CHẠY][MÃ] |
| 5d Bàn giao mang người yêu cầu | **Không** | Prompt của agent 3: "From: agent_…", 0 lần "Lan"/"1001"; bàn giao 1→2 còn **mất hẳn** do trùng kênh | [CHẠY] |
| R1 Backend riêng, key của mình | **Đạt (phải cấu hình `nexus_power`)** | Chạy thật với provider OpenAI tuỳ chỉnh; mặc định lại là `claude_code` (CLI), `run.sh` đòi cài Claude CLI | [CHẠY][MÃ] |
| R6 Kênh mở rộng bằng code, có Zalo | **Một phần** | Có lớp nền `ChannelTriggerBase` tốt nhưng đăng ký kênh nằm trong lõi (map, registry, enum, schema, route, UI); không có Zalo | [MÃ] |
| R7 Tự host + giấy phép | **Đạt** | Apache-2.0; chạy được trên máy (SQLite, uv) | [MÃ][CHẠY] |
| R8 Còn sống (≥ 2026-06-27) | **Đạt (yếu)** | 10 commit/8 release từ 2026-07-02 đến 2026-08-05; sau đó im lặng 53 ngày; repo là mirror squash, 90/109 commit của một tác giả | [MÃ][DOC] |

### Inferences

#### Phải tự xây gì, có cần fork không
**Bắt buộc fork.** Những phần cần sửa đều nằm ở lõi: phép ghi đè `user_id` trong `AgentRuntime`, các hook của SocialNetwork, cách MessageBus bơm tin chưa đọc, cách đặt `channel_id`, và BasicInfo. Không có cơ chế plugin nào đủ để thay những phần này. Ước lượng [?], tính cho 1 kỹ sư Python quen mã:
1. **Danh tính theo người (5a/5b):** bỏ ghi đè `user_id`, hoặc thêm `speaker_id=(channel, sender_id)` và cho mọi hook đọc/ghi thực thể, observation, narrative theo khoá này. Thêm bảng liên kết danh tính xuyên kênh có thao tác gỡ, và sửa lỗi quy người nói trong lịch sử nhóm. Khoảng **3–5 tuần-người**. Việc này chạm hàng chục file và bộ test lớn: ~259k dòng Python kể cả `tests/`, đếm bằng `wc` lúc clone.
2. **Riêng tư (K4):** lọc recall theo người yêu cầu, gồm observation, entity, narrative và khối Unread của bus. Phân vùng `channel_id` theo agent/bot. Thêm ACL "admin cấp quyền xem". Khoảng **2–3 tuần**.
3. **Admin hệ thống (K5):** bảng `platform_identity → system_admin` dùng chung cho mọi agent, chặn tool theo vai trò ở tầng policy (`nexus_power` đã có `PolicyLayer`), và sửa `is_creator` cho IM. Khoảng **1–2 tuần**.
4. **Phòng ban và task (D1/5d):** schema vai trò/phòng ban cho agent, bảng task có assignee, người yêu cầu và trạng thái review, định tuyến theo vai trò, và mang `requester` qua `bus_send_to_agent`. Khoảng **3–4 tuần**.
5. **K1:** kho tài liệu có scope, nạp bằng upload/URL/sync, có tìm kiếm hoặc bơm RAG. Khoảng **1–2 tuần**.
6. **Zalo adapter:** khoảng **1–2 tuần**, cộng phần UI.
7. **Khoá Awareness và sửa lỗi trùng kênh/bàn giao:** khoảng **1 tuần**.

Tổng khoảng **12–19 tuần-người**. Sau đó còn phải gánh fork khỏi một upstream "No backwards-compatibility… YOLO" (CLAUDE.md, quy tắc 2) vốn được xả theo lô squash từ repo riêng, nên hầu như không merge upstream được.

**So sánh [?]:** dựng trên nền đã có tổ chức agent (như GoClaw) rồi chép **mẫu** bộ nhớ và trust signal của NarraNexus sẽ rẻ hơn nhiều.

#### Rủi ro đáng chú ý
- **Bảo trì:**
  - đội nhỏ, một tác giả chính;
  - repo công khai là mirror, không commit nào sau 2026-08-05;
  - quy tắc "no backwards-compat" khiến fork nhanh chóng lệch khỏi upstream;
  - tài liệu song ngữ Anh/Trung, cộng đồng chủ yếu qua WeChat/Discord [DOC].
- **Giấy phép:** Apache-2.0 an toàn cho doanh nghiệp. Bản cloud và "NetMind free tier" là dịch vụ riêng, không bắt buộc [MÃ].
- **Chi phí token [CHẠY]:**
  - Một tin nhắn vào sinh khoảng 8 request LLM, tổng khoảng 250 KB JSON.
  - Riêng request vòng lặp chính khoảng 176 KB, gồm system prompt khoảng 85k ký tự và 77 schema tool.
  - Ước lượng thô khoảng 50–60k token cho mỗi tin nhắn vào (theo tỉ lệ ~4 ký tự/token, chưa đo bằng tokenizer).
  - Trong nhóm, mọi tin có @bot đều chạy đủ pipeline, kể cả khi agent quyết định im lặng.
- **Bảo mật [CHẠY][MÃ]:**
  - Người lạ trên Telegram có trong tay `bash`, `write_file`, `update_awareness`, `create_agent`, `skill_install`, `tg_unbind`, `ha_call_service`. Chỉ lời dặn trong prompt đứng giữa họ và hệ thống.
  - `is_creator=True` cho mọi người gửi IM.
  - WeChat nhận owner theo kiểu ai DM trước thì thành owner.
  - DM Telegram của nhiều agent với cùng một người bị trộn chung kênh.
  - `JWT_SECRET` mặc định là "dev-secret-do-not-use-in-production" nếu không đặt biến môi trường [MÃ `backend/auth.py`].
  - Chế độ local không xác thực: `X-User-Id` là đủ.

### Gaps
- Chưa chạy bằng LLM thật, nên chưa biết mô hình thật có tự từ chối rò rỉ hay mạo danh không. Các kết luận "không chặn" ở trên là về **nền tảng**.
- Chưa kiểm frontend, bản DMG macOS và chế độ cloud (executor riêng cho từng user, `staff`).
- Ước lượng công sức là suy luận [?], chưa lập kế hoạch chi tiết.
- Dọn dẹp: đã dừng mọi tiến trình đã khởi động (stub :18101, Telegram giả :18191, backend :8000, sqlite proxy :8100, MCP 78xx, worker). Đã xoá bản clone, `.venv` và thư mục dữ liệu `run/`. Cache chung của uv (`~/.cache/uv`) được giữ lại.
