# UniEmployee (zj-unicom-ai/UniEmployee): đánh giá theo bộ yêu cầu cuối (D1, K1–K5, 5d, R1/R6/R7/R8), có chạy thử với stub LLM

Phạm vi: commit `7d5edf5480d077ba30d9ab3605aa95d8ba327f21` (tag `v0.20.0`, 2026-09-24), trùng commit với lần đọc trước (`7d5edf5`) nên không có thay đổi mã giữa hai lần. Ngày kiểm: 2026-09-27 (đã xác nhận bằng `date`).

Nhãn: [MÃ] đọc mã · [CHẠY] chạy thật với stub LLM · [DOC] tài liệu/README · [?] chưa kiểm chứng.

Tệp bằng chứng: [evidence/uniemployee_run_evidence.json](evidence/uniemployee_run_evidence.json) (khoảng 137 KB). Tệp gồm các request đã cắt gọn mà nền tảng gửi tới model, phản hồi HTTP của webhook, log RAGFlow giả/outbound, và bảng DB approvals/conversations/store/users sau khi chạy.

**Cách chạy và các chỗ lệch so với production** [CHẠY]:
- **Cài đặt:** `uv venv` (Python 3.12) + `backend/requirements.lock.txt`. Server **không khởi động được** chỉ với lock file (`ModuleNotFoundError: No module named 'sqlglot'`), phải cài thêm `backend/requirements.txt` — [requirements.txt#L27](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/requirements.txt#L27). README nói lock file "fully reproducible", điều này sai.
- **DB:** chạy `DB_BACKEND=sqlite`. Mã hỗ trợ đường này và test dùng nó ([app/db.py#L1-L20](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/db.py#L1-L20)), còn production theo tài liệu là PostgreSQL với 7 database. `MCP_DISABLED=1`, `AUTOMATIONS_DISABLED=1`.
- **Model:** stub LLM (bản sao `stub_llm.py`, chỉ sửa một chỗ: nếu tin cuối là tool result thì trả text để khỏi lặp tool) ở cổng 18103 qua OpenAI Chat Completions.
  - Tên model `stub-model` làm **warmup lỗi** "Unable to infer model provider" vì `init_chat_model(base_model)` được gọi mà không truyền provider ([compiler.py#L432-L454](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L432-L454), [ai_models.py#L169-L204](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/ai_models.py#L169-L204)).
  - Đổi tên thành `gpt-4o-mini` thì chạy được.
- **Tri thức:** UniEmployee không có kho tài liệu riêng, tri thức đến từ RAGFlow. Tôi dựng một **RAGFlow giả** ở cổng 18104, trả `/api/v1/retrieval` và `/api/v1/datasets`. Cổng này cũng làm đích cho `outbound_webhook`.
- **Đường vào tin nhắn:** qua đường thật `POST /api/im/channels/{id}/incoming` với `{sender_id, message, employee_id, secret}`. Kênh `provider=generic` có secret. Không dùng token bot thật nào.
- **Frontend:** không build, chỉ xem ảnh chụp trong repo.
- **Dọn dẹp:** đã dừng mọi tiến trình đã khởi động và xoá clone, venv, dữ liệu.

## 1. Kênh IM và danh tính (K2-5a, K2-5b-in, K2-5b-cross, R6)

### Takeaway
Webhook chung `/api/im/channels/{id}/incoming` cho một cầu nối Zalo gửi tin vào mà không phải sửa lõi. Nhưng payload chỉ có `sender_id` và `message`: **không có group id, không có tên người gửi**. Người gửi thành chuỗi `im:{channel_id}:{sender_id}`, không nằm trong bảng `users`, và **không được đưa vào prompt**.

Mỗi (kênh, người, nhân viên) chỉ có một hội thoại, nên nhóm và DM của cùng một người bị trộn thành một thread. Khái niệm "nhóm" không tồn tại. Bộ nhớ dài hạn keyed theo (người, nhân viên), nhưng **người dùng IM không ghi được bộ nhớ** vì thiếu tool `edit_file`. Không có cơ chế liên kết danh tính giữa các kênh.

### Cited Findings
- **Schema inbound** [MÃ]: `ImIncomingMessage` chỉ có `sender_id: str`, `message: str`, `employee_id: str | None`, `secret: str | None` — [models.py#L95-L99](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/models.py#L95-L99)
  - [CHẠY]: gửi thêm `group_id` và `sender_name` thì pydantic lặng lẽ bỏ. Trong request tới model không có chữ nào về nhóm hay tên người gửi, tin user chỉ là nội dung thô — [evidence, bước S3a](evidence/uniemployee_run_evidence.json)
- **Người gửi → user** [MÃ]: `_external_user_id()` trả `f"im:{channel_id}:{sender_id}"` — [routes/im.py#L61-L62](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/im.py#L61-L62)
  - Hội thoại được tìm hoặc tạo theo `(channel_id, user_id, employee_id)` — [routes/im.py#L176-L186](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/im.py#L176-L186), [conversations.py#L650-L662](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/conversations.py#L650-L662)
  - Không có bản ghi `users` nào được tạo. Sau khi chạy, bảng `users` chỉ có `u_admin` và user web tôi tự tạo [CHẠY].
- **Nhóm và DM bị trộn** [CHẠY]: tin của Lan ở "G1", "G2" và "DM" (cùng một kênh) đều vào **cùng hội thoại** `c_im_202609271757054047673` (message_count 6).
  - Khi Lan hỏi trong DM "Bạn biết gì về mình? KPI của mình bao nhiêu?", request chứa hai tin trước ở G1/G2 **dưới dạng lịch sử hội thoại**, không phải bộ nhớ theo người.
  - Trong "G1", thread của Lan **không thấy** câu "Mình là Minh." của Minh vì Minh có thread riêng. Tức là không có ngữ cảnh nhóm — [evidence, bước S3a–S3d, db_conversations](evidence/uniemployee_run_evidence.json)
- **Tách kênh theo nhóm thì danh tính bị tách** [CHẠY]: tôi thử phương án B, mỗi nhóm một kênh (kênh "Zalo G1", kênh "Zalo DM").
  - Khi đó Lan thành hai user khác nhau (`im:<G1>:1001`, `im:<DM>:1001`).
  - DM của Lan không còn chút thông tin nào từ G1 — [evidence, followup:B_G1_Lan / B_DM_Lan](evidence/uniemployee_run_evidence.json)
- **Bộ nhớ dài hạn** [MÃ]:
  - Namespace là `(user_id or "default", emp_id)`, tức mỗi người một bộ nhớ **riêng cho từng nhân viên số**, không dùng chung giữa các nhân viên — [compiler.py#L493-L505](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L493-L505)
  - `/memories/AGENTS.md` được **tự động** nạp vào system prompt qua `memory=["/memories/AGENTS.md"]` — [compiler.py#L655-L668](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L655-L668)
  - Template khởi tạo được seed theo người — [runtime.py#L167-L178](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/runtime.py#L167-L178)
- **Người dùng IM không ghi được bộ nhớ** [MÃ][CHẠY]:
  - `_fs_tools_for_user()` chỉ cấp `write_file`/`edit_file` cho user có `role == "admin"` trong bảng `users`. Mọi người khác, kể cả user IM (không có trong bảng), chỉ được `ls, read_file, glob, grep` — [compiler.py#L75-L77](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L75-L77), [compiler.py#L544-L555](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L544-L555)
  - Khi chạy, Lan nói "Nhớ giúp: KPI…" và model gọi `edit_file`. Kết quả tool là `Error: edit_file is not a valid tool, try one of [ls, read_file, glob, grep, task, create_ticket, kb_search, get_current_time]`. `/AGENTS.md` của `im:…:1001` vẫn chỉ là template "## 用户档案（随着对话积累）" — [evidence, S3c + db_store_memory](evidence/uniemployee_run_evidence.json)
  - Đối chứng: admin qua web gọi `edit_file` thì thành công, và ở hội thoại mới khối `<agent_memory>` có "Lan: KPI tháng 10 = 50 bài" (đây là bộ nhớ riêng của admin) — [evidence, followup:admin_web_recall_newconv](evidence/uniemployee_run_evidence.json)
  - User web thường cũng nhận lỗi "edit_file is not a valid tool" [CHẠY].
- **Hồ sơ người dùng chỉ có cho user web** [MÃ][CHẠY]: `_build_user_context()` chèn khối "## 当前用户信息" (称呼/职位/职责/偏好) lấy từ `user_profiles` — [compiler.py#L252-L272](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L252-L272)
  - `upsert_profile` từ chối user không có trong bảng `users` — [catalog/users.py#L138-L145](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/users.py#L138-L145)
  - Khi chạy: khối này xuất hiện cho `minh_web` ("称呼：Minh", "职责背景：Chạy ads Facebook"), nhưng không có cho bất kỳ người gửi IM nào — [evidence, followup:web_user_profile](evidence/uniemployee_run_evidence.json)
- **Xuyên kênh (5b-cross)** [MÃ][CHẠY]:
  - Liên kết danh tính duy nhất trong hệ là `user_identities(issuer, subject)`, và chỉ dùng cho đăng nhập OIDC SSO — [catalog/db.py#L83-L88](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/db.py#L83-L88), [catalog/users.py#L79-L122](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/users.py#L79-L122)
  - Khi chạy: kênh thứ hai ("Telegram bridge") với cùng `sender_id=1001` ra user `im:<tg>:1001` mới, thread mới, không có dữ kiện nào của Lan — [evidence, followup:X_TG_Lan](evidence/uniemployee_run_evidence.json)
- **Outbound** [MÃ][CHẠY]:
  - `outbound_webhook` nhận `{conversation_id, channel_id, message}`, **không có người nhận hay nhóm** — [routes/im.py#L81-L94](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/im.py#L81-L94)
  - Cầu nối phải tự nhớ ánh xạ conversation_id → người/nhóm. Nó cũng có thể lấy `reply` ngay trong phản hồi HTTP đồng bộ.
  - Webhook chạy agent **đồng bộ trong request HTTP** — [routes/im.py#L188-L192](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/im.py#L188-L192)
- **Provider IM ngoài chưa có** [DOC]: README nói WeChat/企业微信/飞书/钉钉 "仍在规划中" — [README.md#L27](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/README.md#L27)
  - Roadmap ghi việc "接入一个企业 IM 渠道并做身份映射、消息幂等…" vẫn là việc tương lai — [enterprise-readiness-roadmap.md#L79](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/docs/guide/enterprise-readiness-roadmap.md#L79)
  - `routes/im.py` không đổi từ commit đầu tiên ngày 2026-08-15, và không có test nào cho `incoming` [MÃ].

### Inferences
- **R6:** một cầu nối Zalo bên ngoài chỉ gửi được DM 1-1 mà không phải sửa lõi.
  - Muốn có nhóm thật (ngữ cảnh chung, biết ai nói), tên người gửi, hay danh tính người gửi trong prompt thì phải sửa `models.py`, `routes/im.py`, `streaming.py` và `compiler.py`, tức là fork.
- **5b-in:** việc Lan "được nhớ" trong DM chỉ là hệ quả phụ của việc trộn mọi tin của Lan vào một thread. Đây không phải bộ nhớ theo người, và sẽ mất khi thread bị tóm tắt hoặc Lan chuyển sang nhân viên khác.

### Gaps
- Chưa chạy với PostgreSQL. Hành vi namespace store và checkpointer được kỳ vọng như SQLite, nhưng chưa kiểm chứng.
- Chưa kiểm hành vi khi hội thoại dài bị `SummarizationMiddleware` tóm tắt (ngưỡng 85% context).

## 2. Mô hình "nhân viên số": chức danh, phòng ban, chia việc, duyệt, uỷ quyền (D1, 5d)

### Takeaway
Nhân viên số chỉ có `name`, `role` (chuỗi) và `persona`. **Không có phòng ban cho nhân viên số, không có chia việc hay giao việc theo vai, không có kênh để một nhân viên gọi nhân viên khác.** "Duyệt" chỉ là human-in-the-loop theo từng tool.

Uỷ quyền nội bộ chỉ có subagent inline (tool `task` của deepagents) bên trong một nhân viên. Subagent chỉ nhận chuỗi mô tả nhiệm vụ, **không biết đang làm cho ai**.

### Cited Findings
- **Schema nhân viên** [MÃ]: bảng `employees(id, name, role, model, persona, backend, mcp_servers, interrupt_on, subagents, subagent_policy, …, kind, quick_prompts)`, không có cột phòng ban hay cấp trên — [catalog/db.py#L63-L67](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/db.py#L63-L67)
  - Bảng `orgs` (cây phòng ban) chỉ gắn với **người dùng** (`users.org_id`) — [catalog/db.py#L74-L82](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/db.py#L74-L82)
  - Phòng ban dùng để chia sẻ **tệp sản phẩm** trong phòng — [routes/workspace.py#L109-L129](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/workspace.py#L109-L129)
- **Cộng tác nhiều nhân viên chưa có** [DOC]: roadmap còn ghi "群聊与多员工协作：一个会话内多数字员工分工" là việc tương lai — [README.md#L326](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/README.md#L326)
  - Nhân viên mẫu chỉ "khuyên người dùng đi hỏi 小经" bằng lời trong persona, không gọi được nhân viên đó — [employees/market-intel.yaml#L17](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/employees/market-intel.yaml#L17)
- **Subagent** [MÃ]:
  - Được cấu hình trong từng nhân viên với `name`, `description`, `system_prompt`, `tools`, rồi đưa vào `create_deep_agent(subagents=…)` — [compiler.py#L457-L491](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L457-L491)
  - System prompt của nhân viên chỉ liệt kê tên và mô tả subagent — [compiler.py#L235-L249](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L235-L249)
- **5d khi chạy** [CHẠY]: tôi gắn subagent `copywriter` vào `emp_lead` vì đây là đường gần nhất với "agent 1 giao cho agent 2".
  - Từ thread DM của Lan, model gọi `task(subagent_type="copywriter", description="Viết 3 caption cho fanpage X, giọng hài hước")`.
  - Request của subagent chỉ có system prompt của copywriter và **một tin user là chuỗi mô tả**. Không có tên Lan, không có sender id, không có lịch sử. Tool của nó: `ls, read_file, glob, grep, get_current_time` — [evidence, followup:S6_clean, req 44](evidence/uniemployee_run_evidence.json)
- **Duyệt (HITL)** [MÃ]:
  - `interrupt_on` được suy ra từ cờ `needs_approval` của từng tool — [catalog/employees.py#L9-L21](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/employees.py#L9-L21)
  - Khi interrupt, hệ tạo phiếu duyệt — [streaming.py#L556-L565](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/streaming.py#L556-L565)
  - Phiếu được quyết định bởi chủ hội thoại hoặc admin, qua JWT web — [routes/conversations.py#L261-L287](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/conversations.py#L261-L287)
  - Luồng cứng duy nhất viết bằng StateGraph là `workflows/refund.py`.
- **HITL qua IM** [CHẠY]:
  - `create_ticket` (cần duyệt) sinh phiếu `pending` cho `user_id=im:…:1001`. Người dùng IM nhận `reply: ""` và không có outbound.
  - Sau khi admin duyệt trên web, kết quả chỉ stream về HTTP của admin. Số lần gọi `outbound_webhook` trước/sau vẫn là 12/12, nên người dùng IM không bao giờ nhận kết quả.
  - Nếu có tin IM mới đến trước khi duyệt, tool đang chờ bị huỷ ("Tool call create_ticket … was cancelled - another message came in"). Lần duyệt sau đó không sinh lời gọi model nào.
  - User web khác (minh_web) duyệt phiếu của Lan thì nhận 403 — [evidence, db_approvals + web_checks](evidence/uniemployee_run_evidence.json)
- **Automations** [MÃ]: cron/webhook chạy một nhân viên với `run_as` và `role="user"`, rồi đẩy kết quả ra kênh. Đây là cơ chế hẹn giờ, không phải chia việc — [automations.py#L361-L376](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/automations.py#L361-L376)

### Inferences
- **D1:** cấu trúc "phòng Marketing gồm Leader/Content/Designer/Ads/SEO…" có thể đặt tên và persona được, nhưng **không hề điều khiển định tuyến hay uỷ quyền**. Mọi phần điều phối (bảng việc, giao theo vai, review bởi Leader) phải tự xây.
- **HITL:** HITL theo tool là điểm mạnh thật, nhưng là duyệt "hành động nguy hiểm", không phải "Leader duyệt bản nháp của Copywriter".

### Gaps
- Chưa thử subagent kiểu `CompiledSubAgent` hoặc async subagent của deepagents. Cấu hình catalog không phơi ra chúng, nên chỉ đọc mã, chưa kiểm chứng.

## 3. Kho tri thức dùng chung (K1) và luật persona (K3)

### Takeaway
**K1: Một phần.**
- Tri thức "thật" nằm ở **RAGFlow bên ngoài**. UniEmployee chỉ lưu con trỏ `ragflow_dataset_id`, gán KB cho từng nhân viên, và truy xuất bằng **tool `kb_search`** chứ không tự chèn vào prompt. Tài liệu phải được nạp trong RAGFlow.
- Đường thứ hai là **SOP**: văn bản do admin dán vào, gán theo nhân viên. **80 ký tự đầu được tự chèn vào system prompt**, còn toàn văn đọc bằng `read_file /sops/<id>.md`.
- Không có phạm vi theo phòng ban cho nhân viên số. Kho tri thức tách khỏi bộ nhớ riêng từng người.

**K3: Đạt.** Persona của nhân viên nằm ở đầu system prompt của mọi request chính, bất kể người gửi hay kênh.

### Cited Findings
- **Chỉ có RAGFlow** [MÃ]:
  - `knowledge.py` ghi rõ "运行时知识只来自 RAGFlow". Nếu chưa cấu hình `RAGFLOW_API_KEY` thì trả "【知识库未配置】" — [knowledge.py#L1-L35](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/knowledge.py#L1-L35)
  - Gọi `POST /api/v1/retrieval` với `dataset_ids` — [connectors/ragflow_client.py#L82-L100](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/connectors/ragflow_client.py#L82-L100)
  - Bảng `knowledge_bases(id, name, description, ragflow_dataset_id)` — [catalog/db.py#L57-L58](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/db.py#L57-L58)
  - API admin chỉ có tạo/sửa/xoá KB và liệt kê dataset RAGFlow, **không có upload tài liệu** — [routes/admin.py#L273-L292](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/admin.py#L273-L292)
- **`kb_search` theo từng nhân viên** [MÃ]: là closure theo nhân viên và người dùng, lấy KB từ `get_effective_config` (template cộng override theo người) — [compiler.py#L79-L118](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L79-L118), [catalog/employees.py#L121-L146](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/employees.py#L121-L146)
- **Bước 2 khi chạy** [CHẠY]:
  - Agent 2 (Copywriter) trong DM của Minh nhận "Slogan công ty là gì?". Agent 1 (Content Lead) nhận "Gói Pro giá bao nhiêu?" từ Lan.
  - Cả hai gọi `kb_search`. RAGFlow giả nhận `{"question": "slogan công ty", "dataset_ids": ["ds_brand"], "top_k": 3, …}` và `{"question": "giá gói Pro", "dataset_ids": ["ds_brand"], …}`.
  - Kết quả tool là "[1] 来源：brand_guideline.md | 相似度：0.9 Brand guideline: slogan 'Nhanh như chớp'; giá gói Pro 199.000đ" — [evidence, S2a/S2b + ragflow_and_outbound_log](evidence/uniemployee_run_evidence.json)
- **SOP tự chèn một phần** [MÃ][CHẠY]:
  - `_extract_sop_preview` lấy 80 ký tự đầu, và `_build_sop_routing` đưa vào system prompt — [compiler.py#L161-L188](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L161-L188)
  - Khi chạy, system prompt của cả hai nhân viên có dòng "- sop_brand：Brand guideline: slogan 'Nhanh như chớp'; giá gói Pro 199.000đ" (tài liệu ngắn hơn 80 ký tự nên lọt trọn) — [evidence, S3a req 0](evidence/uniemployee_run_evidence.json)
  - SOP được đồng bộ vào store theo namespace `(user_id, emp_id)` — [runtime.py#L246-L272](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/runtime.py#L246-L272)
- **Bản thể nghiệp vụ (ontology)** [MÃ]:
  - Đây là kho sự thật có cấu trúc dùng chung toàn tenant. Nhân viên được cấp `ontology_write` có thể ghi vào, và "其他数字员工都会读到" — [compiler.py#L220-L230](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L220-L230)
  - Nó dùng được cho dữ liệu kiểu CRM, nhưng không phải kho tài liệu văn bản.
- **Persona** [MÃ][CHẠY]:
  - `system_prompt = spec.persona` rồi nối thêm phần định tuyến. Persona đứng đầu prompt — [compiler.py#L636-L668](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L636-L668)
  - Khi chạy, các luật "Luôn xưng em, gọi người dùng là anh/chị / Không dùng emoji / Không bàn chính trị" có trong **mọi** request chính của `emp_lead`: IM Lan, Minh, 9001, 1003, `u_admin`, cả hai phương án kênh, kênh "Telegram", admin web và user web — [evidence, cờ `persona_rules_present`](evidence/uniemployee_run_evidence.json)
  - Subagent **không kế thừa** persona của nhân viên cha, vì dùng `system_prompt` riêng (req 44).
  - Vì không có nhóm, "áp dụng nhất quán trong nhóm và DM" chỉ có nghĩa là mọi thread của cùng một nhân viên.
- **Chi phí prompt** [CHẠY]:
  - Với persona chỉ 132 ký tự, system prompt đã dài 7.488 ký tự: boilerplate Skills/Memory của deepagents bằng tiếng Anh, định tuyến SOP/subagent bằng tiếng Trung.
  - Schema tool thêm khoảng 9.100 ký tự. Tổng body mỗi request khoảng 17.000 ký tự — [evidence, S3a req 0](evidence/uniemployee_run_evidence.json)
  - Tin đầu tiên của mỗi hội thoại còn tốn thêm một lời gọi sinh tiêu đề (`_gen_title`).

### Inferences
- Để có brand guideline, bảng giá và SOP dùng chung cho cả phòng, cần vận hành thêm **RAGFlow**, một stack nặng. Cách khác là dán SOP (chỉ tự chèn 80 ký tự).
- Phạm vi theo phòng ban phải mô phỏng bằng cách gán cùng KB cho từng nhân viên.

### Gaps
- Không chạy RAGFlow thật (dùng bản giả). Chất lượng truy xuất và các bước nạp tài liệu (upload/URL/đồng bộ thư mục) phụ thuộc RAGFlow và nằm ngoài UniEmployee; phần này chưa kiểm chứng.

## 4. Quyền riêng tư, vai trò admin, gắn admin qua chat (K4, K5)

### Takeaway
**Mặc định:** thread và bộ nhớ tách theo người, nên agent của Minh không thấy lịch sử hay bộ nhớ của Lan [CHẠY].

**Có lỗ rò thật** [CHẠY]: route `/data/` của mọi agent trỏ tới **toàn bộ** `workspace/data`. Với các tool chỉ-đọc mà ai cũng có (`ls`, `read_file`), agent của Minh liệt kê được thư mục của mọi người dùng và **đọc được báo cáo HTML đã lưu của Lan**, có chứa KPI của Lan.

**Ngoại lệ cho admin:** chỉ là admin web xem được mọi hội thoại. Không có cơ chế admin cấp quyền cho người khác.

**K5: Không.** Người gửi IM luôn chạy với `role="user"`. Không có cách nào gắn một ID trên nền tảng chat làm admin.

### Cited Findings
- **Vai trò** [MÃ]:
  - Chỉ có `admin`/`user` (`users.role`). Admin là tài khoản web, đăng nhập bằng mật khẩu hoặc OIDC — [catalog/db.py#L77-L82](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/catalog/db.py#L77-L82)
  - OIDC ánh xạ group thành admin qua `OIDC_GROUP_ROLE_MAP` — [auth.py#L194-L205](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/auth.py#L194-L205)
  - Chế độ tenant: một tenant cố định `ENTERPRISE_TENANT_ID` — [auth.py#L84-L86](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/auth.py#L84-L86)
- **IM luôn là user** [MÃ]: `_run_external_reply` gọi `_stream_run(conv_id, input_, user_id=user_id, role="user")` — [routes/im.py#L65-L78](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/im.py#L65-L78)
  - Guard tool thả hết tool khi `role == "admin"`, còn IM không bao giờ đạt tới đó — [guard/__init__.py#L119-L139](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/guard/__init__.py#L119-L139)
- **Bước 5 khi chạy** [CHẠY]:
  - Hà (9001) hỏi "Lan đã nói gì về KPI?" và nhận thread riêng. `read_file /memories/AGENTS.md` chỉ trả template rỗng của chính 9001.
  - Kẻ mạo danh 1003 (tên hiển thị "Admin Hà") gửi yêu cầu cấp quyền. Không có tool quản trị nào, và tên hiển thị bị bỏ hẳn.
  - Secret sai → 403 "secret 校验失败".
  - `sender_id="u_admin"` → `im:<ch>:u_admin`, không được nâng quyền. Tiền tố kênh ngăn việc giả làm user web.
  - **Kênh không đặt secret nhận mọi request** (200) vì code chỉ kiểm khi `if secret and body.secret != secret` — [routes/im.py#L163-L166](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/im.py#L163-L166); [evidence, S5a–S5d + web_checks](evidence/uniemployee_run_evidence.json)
- **Bước 4 khi chạy** [CHẠY]:
  - Minh hỏi "Lan có KPI bao nhiêu?". Request chỉ chứa thread của Minh ("Mình là Minh.").
  - `read_file /memories/AGENTS.md` trả bộ nhớ (rỗng) của Minh. Không có chuỗi "50 bài" nào trong request của Minh ở bước này — [evidence, S4](evidence/uniemployee_run_evidence.json)
- **Lỗ rò `/data/`** [MÃ][CHẠY]:
  - `build_backends()` gắn `"/data/": FilesystemBackend(root_dir=str(WORKSPACE_DATA), virtual_mode=True)` chung cho mọi người, không lọc theo user — [compiler.py#L570-L593](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L570-L593)
  - Báo cáo HTML nội tuyến được lưu ở `.artifact-store/<sha256(user_id)[:24]>/<sha256(conv_id)[:24]>/inline-reports/` — [report_artifacts.py#L102-L112](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/report_artifacts.py#L102-L112)
  - Khi chạy: Lan nhận một báo cáo "KPI tháng 10 của Lan: 50 bài (bí mật)". Sau đó agent của Minh:
    - `ls /data/` → thấy `/data/.artifact-store/` và thư mục của từng người gửi (`/data/im:<ch>:1001/`, `…:1003/`, `…:9001/`…), tức lộ luôn danh sách ID người dùng;
    - `ls` sâu vào `.artifact-store/…/inline-reports/` → thấy tệp;
    - `read_file` → nhận nguyên văn "KPI tháng 10 của Lan: 50 bài (bí mật)" — [evidence, leak:M_ls, leak:M_ls2, leak:M_read](evidence/uniemployee_run_evidence.json)
  - `glob **/*.html` từ gốc `/data/` thì không thấy (bỏ thư mục chấm), nhưng `ls` thì thấy.
- **Ngoại lệ admin** [CHẠY]:
  - Admin web gọi `GET /api/im/channels/{ch}/conversations` thấy hội thoại của mọi người gửi. Gọi `…/conversations/{conv_id}` đọc được lượt "Nhớ giúp: KPI tháng 10 của mình là 50 bài." của Lan.
  - `minh_web` gọi cùng API → 403 — [routes/im.py#L218-L248](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/routes/im.py#L218-L248); [evidence, web_checks](evidence/uniemployee_run_evidence.json)
  - Không tìm thấy API hay tool nào để admin "cho phép Minh xem thông tin của Lan" [MÃ, grep toàn bộ `routes/`].

### Inferences
- **K4:** cách ly mặc định chỉ đứng vững ở mức thread và bộ nhớ. Tệp sản phẩm (báo cáo, upload trong `workspace/data/<uid>/uploads`) rò chéo qua các tool đọc tệp. Không có cơ chế ngoại lệ có kiểm soát.
- **K5:** phải xây từ đầu:
  - principal IM → bảng `users`;
  - lệnh admin qua chat;
  - buộc webhook có secret hoặc chữ ký, vì hiện một kênh không secret cho phép giả `sender_id` tuỳ ý.

### Gaps
- Chưa thử upload tệp qua web (`/api/conversations/{id}/attachments`). Rò tệp upload được suy ra từ cùng route `/data/` nhưng chưa kiểm chứng.
- Lỗi OIDC: `auth.py` dùng `urlencode` mà không import (pyflakes báo `backend/app/auth.py:147: undefined name 'urlencode'`), nên luồng đăng nhập SSO có thể lỗi `NameError` — [auth.py#L141-L147](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/auth.py#L141-L147). Chưa chạy luồng OIDC thật.

## 5. Giấy phép, phát hành, ngôn ngữ tài liệu/UI, backend model (R1, R7, R8)

### Takeaway
MIT, tự host được (PostgreSQL, Docker Compose), backend Python riêng dùng API key của mình, không cần CLI lập trình. Dự án rất mới (commit đầu 2026-08-15) nhưng phát hành dày: 21 tag từ v0.4.0 ngày 2026-08-27 đến v0.20.0 ngày 2026-09-24.

Tài liệu hướng dẫn và bài viết **đều bằng tiếng Trung**, chỉ có `README.en.md` bằng tiếng Anh. UI Vue tiếng Trung, không có i18n.

### Cited Findings
- **Giấy phép** [MÃ]: MIT, "Copyright (c) 2026 ZJ-Unicom-AI" — [LICENSE](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/LICENSE). Skill `frontend-design` theo Apache-2.0 — [README.en.md](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/README.en.md)
- **Phát hành** [MÃ, git]:
  - Tag v0.20.0 ngày 2026-09-24, v0.19.1 và v0.19.0 ngày 2026-09-20, v0.18.0 ngày 2026-09-19, …, v0.4.0 ngày 2026-08-27.
  - 90 commit, tất cả sau 2026-06-27. Commit đầu ngày 2026-08-15 có tiêu đề "从 UniEmployeePro 整体复制当前项目".
  - Hai tên tác giả: wanrengang (67) và wrg (23) — [CHANGELOG.md#L3](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/CHANGELOG.md#L3)
- **Trang GitHub** (xem ngày 2026-09-27): 277 sao, 14 fork, 1 issue mở. Trang không hiện mục Releases, nên có GitHub Release hay chỉ có tag là điều chưa kiểm chứng — [GitHub](https://github.com/zj-unicom-ai/UniEmployee)
- **Ngôn ngữ** [MÃ]:
  - Tỉ lệ chữ Hán trong các tệp `docs/guide/*.md` và `docs/articles/*.md` từ 0,24 đến 0,70. `README.en.md` gần như 0.
  - `frontend/src` không có i18n.
  - Ảnh chụp `assets/screenshots/12-admin-employee.png` cho thấy UI "员工管理" với các trường 员工 ID/名称/角色/模型/运行后端/人设 bằng tiếng Trung — [assets/screenshots](https://github.com/zj-unicom-ai/UniEmployee/tree/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/assets/screenshots)
  - Có 7 ảnh chụp: chat, skills, history, trace, ontology, admin-employee, chat-approval.
- **Backend model (R1)** [MÃ][CHẠY]:
  - Dùng LangChain `init_chat_model` qua endpoint tương thích OpenAI. Key lưu trong bảng `ai_models` hoặc env — [compiler.py#L432-L454](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L432-L454)
  - Runtime là deepagents 0.7.5 / LangGraph 1.2.9 chạy trong tiến trình — [requirements.lock.txt](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/requirements.lock.txt)
  - Tên model mà LangChain không suy ra được provider sẽ lỗi khi biên dịch. Đã thấy khi chạy với `stub-model`.
  - Nhân viên dùng backend `local_shell` chạy lệnh trên máy chủ khi sandbox tắt — [compiler.py#L523-L583](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/backend/app/compiler.py#L523-L583)
- **Độ chín** [DOC]:
  - Roadmap tự nhận là "可以进入有业务负责人、只读数据、人工兜底的单企业试点" — [enterprise-readiness-roadmap.md#L18](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/docs/guide/enterprise-readiness-roadmap.md#L18)
  - Kênh ngoài vẫn là "后续工作" — [enterprise-readiness-roadmap.md#L31](https://github.com/zj-unicom-ai/UniEmployee/blob/7d5edf5480d077ba30d9ab3605aa95d8ba327f21/docs/guide/enterprise-readiness-roadmap.md#L31)

### Inferences
- **R7 và R8 đạt về hình thức**, nhưng tuổi đời 6 tuần và thực tế một người phát triển chính là rủi ro bảo trì lớn.
- Có dòng "Enterprise Support … +86" và nguồn gốc "UniEmployeePro" cho thấy có thể tồn tại một bản thương mại nội bộ. Đây là suy luận, chưa kiểm chứng.

### Gaps
- Không rõ wanrengang và wrg có phải cùng một người không.
- Chưa kiểm build Docker. Docker có thể không chạy được trong môi trường này.

## 6. Kết luận: có dùng làm nền hoặc thành phần cho "công ty agent" phòng Marketing không

### Takeaway
**Không nên dùng làm nền.** UniEmployee mạnh ở vài chỗ: HITL theo tool, trace, SOP/skill routing, persona theo nhân viên, gán nhân viên và KB cho người dùng web.

Nhưng nó yếu hoặc thiếu đúng những phần cốt lõi của yêu cầu:
- nhóm chat và danh tính người gửi trong prompt;
- bộ nhớ theo người cho người dùng IM;
- liên kết danh tính xuyên kênh;
- admin qua chat;
- phòng ban và uỷ quyền giữa các nhân viên mang theo người yêu cầu;
- cách ly tệp giữa người dùng.

Phần lớn các thứ này nằm ở lõi (`routes/im.py`, `streaming.py`, `compiler.py`, schema catalog), nên **bắt buộc fork**. Chỉ đáng dùng làm tài liệu tham khảo cho HITL, trace và SOP.

### Cited Findings
- Bảng dưới tổng hợp từ các mục 1–5 và tệp [evidence/uniemployee_run_evidence.json](evidence/uniemployee_run_evidence.json). Mọi dòng mã trích ở commit `7d5edf5480d077ba30d9ab3605aa95d8ba327f21`.

### Inferences

#### Bảng chấm điểm

| Tiêu chí | Kết quả | Bằng chứng | Nhãn |
|---|---|---|---|
| D1 Vận hành phòng ban | **Không** | Nhân viên chỉ có `name/role/persona`, không có phòng ban (`catalog/db.py#L63-L67`). Không chia việc, không giao theo vai, không gọi nhân viên khác. Roadmap còn ghi "群聊与多员工协作" (`README.md#L326`). Duyệt chỉ là HITL theo tool (`catalog/employees.py#L9-L21`, `routes/conversations.py#L261-L287`) | [MÃ][DOC] |
| K1 Kho tri thức chung | **Một phần** | Chỉ qua RAGFlow bên ngoài, gán KB theo nhân viên, truy xuất bằng tool `kb_search`. Khi chạy, cả hai agent nhận `dataset_ids:["ds_brand"]` và ra slogan/giá. SOP tự chèn 80 ký tự đầu vào system prompt. Không có phạm vi phòng ban, không upload trong UniEmployee. Tách khỏi `/memories/` | [MÃ][CHẠY] |
| K2-5a Người gửi + kênh + nhóm | **Một phần** | Có `sender_id` ổn định và `channel_id` (`im:{ch}:{sender}`). **Không có group id, không có tên**, trường thừa bị bỏ. Danh tính **không vào prompt** | [MÃ][CHẠY] |
| K2-5b-in Cùng người qua nhóm/DM, nhớ theo người | **Không** | Không có khái niệm nhóm. Nhóm và DM cùng kênh bị trộn thành một thread; tách kênh thì tách người. Bộ nhớ theo (người, nhân viên) nhưng người dùng IM **không có `edit_file`** nên không ghi được (lỗi "edit_file is not a valid tool") | [MÃ][CHẠY] |
| K2-5b-cross Cùng người xuyên kênh | **Không** | `user_id` chứa `channel_id`. Kênh thứ hai ra người mới. `user_identities` chỉ dành cho OIDC | [MÃ][CHẠY] |
| K3 Luật persona | **Đạt** | Persona đứng đầu mọi system prompt chính (IM và web, mọi người gửi). Subagent không kế thừa | [MÃ][CHẠY] |
| K4 Riêng tư, ngoại lệ admin | **Một phần** (có lỗ rò) | Thread và bộ nhớ tách theo người (Minh không thấy KPI của Lan). **Rò:** Minh `ls`/`read_file` đọc được báo cáo của Lan trong `/data/.artifact-store` (`compiler.py#L588`). Không có cơ chế admin cấp quyền, admin web xem được tất cả | [MÃ][CHẠY] |
| K5 Gắn admin qua chat | **Không** | IM cứng `role="user"` (`routes/im.py#L67`). Không gắn được ID nền tảng làm admin. Kênh không secret nhận `sender_id` giả tuỳ ý | [MÃ][CHẠY] |
| 5d Uỷ quyền mang theo người yêu cầu | **Không** | Subagent chỉ nhận chuỗi mô tả, không có Lan hay sender id (req 44). Không có uỷ quyền giữa các nhân viên | [MÃ][CHẠY] |
| R1 Backend riêng + API key riêng | **Đạt** (có lưu ý) | LangChain/deepagents trong tiến trình, endpoint OpenAI-compat, key trong DB/env. Tên model phải để LangChain suy ra được provider | [MÃ][CHẠY] |
| R6 Kênh mở rộng được, Zalo không sửa lõi | **Một phần** | Webhook chung chạy được, cầu nối ngoài gửi DM không cần sửa lõi. Nhóm, tên người gửi, người nhận outbound, kết quả sau duyệt, xử lý bất đồng bộ đều cần sửa lõi. Chưa có provider ngoài nào | [MÃ][CHẠY][DOC] |
| R7 Tự host + giấy phép kinh doanh được | **Đạt** | MIT, Docker Compose + PostgreSQL. Lock file thiếu `sqlglot` (lỗi nhỏ) | [MÃ][CHẠY] |
| R8 Còn sống (từ 2026-06-27) | **Đạt** | v0.20.0 ngày 2026-09-24, 21 tag từ 2026-08-27, 90 commit. Nhưng dự án mới 6 tuần tuổi, 1–2 tác giả | [MÃ] |

#### Phải tự xây gì, có cần fork không

**Có, bắt buộc fork.** Chỉ cầu nối Zalo (DM 1-1) là làm được như plugin bên ngoài. Ước lượng tính theo người-tuần của một kỹ sư quen Python/LangGraph, chưa gồm kiểm thử chấp nhận:

1. **Mô hình người và nhóm (K2), sửa lõi.** Khoảng 2–3 tuần.
   - Thêm `group_id`, `sender_name` và loại hội thoại vào `ImIncomingMessage`.
   - Thêm thread theo nhóm và khối "người đang nói" trong prompt.
   - Thêm bảng person/contact với liên kết đa kênh.
   - Đưa người gửi IM vào `users` hoặc một bảng principal.
   - Cấp tool ghi bộ nhớ riêng cho `/memories/` (không mở `edit_file` toàn cục).
   - Chuyển bộ nhớ theo người sang dùng chung giữa các nhân viên nếu cần.
2. **Admin qua chat (K5) và ngoại lệ riêng tư (K4), sửa lõi.** Khoảng 1,5–2 tuần.
   - Ánh xạ `(channel, platform_id)` → admin, bỏ `role="user"` cứng.
   - Thêm lệnh hoặc tool admin trong chat.
   - Thêm bảng cấp quyền "A được xem thông tin của B".
   - Bắt buộc secret hoặc chữ ký HMAC cho webhook.
3. **Vá rò `/data/`, sửa lõi.** Khoảng 2–4 ngày: gốc `FilesystemBackend` theo `user_id`, chặn `.artifact-store` với người không sở hữu.
4. **Phòng ban và điều phối (D1, 5d), sửa lõi và xây mới.** Khoảng 4–6 tuần.
   - Thêm cột phòng ban và cấp trên cho nhân viên số.
   - Xây tool "giao việc cho nhân viên X" gọi agent của nhân viên khác, mang theo `requester` và ngữ cảnh.
   - Xây bảng task, trạng thái, review của Leader.
   - Xử lý kết quả sau duyệt: đẩy ra outbound và xử lý bất đồng bộ.
5. **Cầu nối Zalo (plugin ngoài).** Khoảng 1 tuần cộng phần riêng của API Zalo.
6. **Việt hoá UI và prompt scaffolding (tiếng Trung).** Khoảng 1–2 tuần. Chưa có i18n.
7. **Tổng:** khoảng **10–15 người-tuần**. Kèm chi phí liên tục để rebase theo upstream đang ra khoảng 5 tag mỗi tuần.

So với một nền đã có sẵn mô hình người, nhóm và uỷ quyền, chi phí này cao hơn đáng kể.

#### Rủi ro đáng chú ý
- **Bảo trì:** dự án mới 6 tuần, copy từ bản nội bộ "UniEmployeePro", 1–2 tác giả, API đổi nhanh (v0.4 → v0.20 trong 4 tuần). `routes/im.py` không được động tới từ commit đầu và không có test. Fork sẽ khó theo upstream.
- **Giấy phép:** MIT sạch. Có dấu hiệu mô hình "open core và hỗ trợ doanh nghiệp" (số điện thoại tư vấn trong README), chưa kiểm chứng. Phụ thuộc RAGFlow (Apache-2.0) để có KB.
- **Chi phí token:** mỗi lời gọi mang khoảng 17.000 ký tự (system 7,5k gồm boilerplate tiếng Anh/Trung, cộng khoảng 9k schema tool) dù persona chỉ 132 ký tự. Có thêm một lời gọi đặt tiêu đề cho mỗi hội thoại mới. Webhook chạy đồng bộ, và mỗi tin IM đi kèm toàn bộ lịch sử thread (nhóm và DM bị trộn).
- **Bảo mật:**
  - rò tệp chéo người dùng qua `/data/` (đã chạy);
  - webhook IM không cần xác thực khi kênh không đặt secret, và so sánh secret không dùng constant-time;
  - `JWT_SECRET` mặc định chỉ cảnh báo;
  - OIDC có `NameError` tiềm ẩn;
  - nhân viên `local_shell` chạy lệnh trên máy chủ khi sandbox tắt;
  - kết quả sau khi duyệt HITL không tới được người dùng IM, và tin mới huỷ tool đang chờ duyệt.
- **Vận hành:** production cần PostgreSQL 7 DB, thêm RAGFlow (stack nặng) cho tri thức, và tuỳ chọn OpenSandbox.

### Gaps
- Ước lượng công sức là suy luận của người kiểm, không dựa trên số liệu dự án.
- Chưa đo chất lượng câu trả lời thật, vì dùng stub LLM.
