# Chấm lại các nền tảng mạnh về "tổ chức agent" theo yêu cầu danh tính đã sửa (2026-09-27)

Phạm vi: AgentTeams/HiClaw, Clawith, Bunkhouse, Agentic Organization, Markus, SwarmClaw, Synkora, GoClaw. Sau đó sàng lọc lại các tên từng bị hạ hạng chỉ vì tiêu chí cũ "chức danh/quyền cho người dùng".

Yêu cầu đã sửa (người dùng làm rõ ngày 2026-09-27): chức danh và phòng ban dành cho **agent** (ví dụ phòng Marketing gồm Leader, Content, Designer, Ads, SEO, Dev), **không** dành cho người. Người dùng không có chức danh hay quyền; mỗi người chỉ là "user A" đang chat với agent 1, và agent 1 có mặt trong nhiều nhóm.

Cách làm và quy ước:
- Mọi repo được clone nông (`--depth 1`) vào scratchpad, đọc mã rồi xoá clone. GoClaw đọc từ bản local chỉ-đọc `/home/user/goclaw`, commit `0c2264989c39` (nhánh `claude/dreamy-johnson-snk1l3` trên fork `nguyenha935/goclaw`; phần mã giống nhánh `dev` `4d3c6bc`).
- Commit đã đọc:
  - AgentTeams `89562fb3` (2026-09-23)
  - Clawith `45fc701c` (2026-08-25)
  - Bunkhouse `3239432c` (2026-09-25)
  - Agentic Organization `bf29743f` (2026-09-09)
  - Markus `bc6f1200` (2026-09-25)
  - SwarmClaw `ed38ba53` (2026-06-30)
  - Synkora `2acc1a58` (2026-09-26)
  - Để sàng lọc lại: Hivekeep `7d023c95` (2026-09-17) và NarraNexus `5869502c` (2026-08-05)
- Nhãn bằng chứng:
  - [MÃ] = đã đọc mã
  - [CHẠY] = đã chạy thử; **vòng này không chạy gì**
  - [DOC] = tài liệu
  - [?] = suy luận hoặc chưa kiểm chứng
- Ký hiệu trong bảng: ✅ đạt, ◐ một phần, ✗ không.

## Câu hỏi 1 — Tổng hợp: tiêu chí đã sửa làm thay đổi thứ hạng thế nào?

### Takeaway
Khi chức danh và phòng ban chuyển sang agent, **Bunkhouse, Agentic Organization và Markus** đạt R2' rõ nhất: có cột DB cho chức danh, phòng ban hoặc đội, và quan hệ báo cáo được dùng thật để định tuyến hoặc giao việc. **GoClaw** đạt mức gần đủ: đội có lead/member/reviewer, nhưng chức danh chỉ là `frontmatter` dạng chữ. **Clawith** tụt hạng, vì mô hình phòng ban và chức danh phong phú của nó dành cho **người** (đồng bộ từ Feishu/DingTalk); còn agent chỉ có `role_description`, và trường này thậm chí bị bỏ ra khỏi prompt.

Về danh tính, **không nền tảng nào đạt 5b-in**. Cả tám đều gắn trí nhớ theo chat/session hoặc theo agent, không theo người. Nghĩa là không có trường hợp user A nói chuyện với agent 1 ở nhóm G1, nhóm G2 và DM mà được nhận ra là cùng một người, với kiến thức dùng chung giữa ba nơi. Về 5a, chỉ **GoClaw** và **SwarmClaw** đưa được "tên + ID người gửi + kênh + nhóm" vào mọi lượt trên Telegram. Về 5d, không nền tảng nào đưa đầy đủ "tên + ID người yêu cầu gốc" vào prompt của agent được giao việc. GoClaw gần nhất: agent được giao nhận ID người gửi, nhưng không có tên.

### Cited Findings

**Bảng tổng hợp** (chi tiết và dòng mã ở các mục Câu hỏi 2–9):

| Nền tảng @commit | R2' (tổ chức agent) | 5a (người gửi mỗi lượt) | 5b-in (cùng người trong một kênh) | 5b-cross (liên kết đa kênh) | 5d (agent được giao biết người yêu cầu gốc) | Riêng tư | Kết luận theo tiêu chí mới |
|---|---|---|---|---|---|---|---|
| **GoClaw** @0c226498 | ◐+ Đội (team) có role `lead/member/reviewer` trong DB. Lead giao việc qua `team_tasks(assignee)` và TEAM.md được đưa vào prompt. Chức danh chỉ là `display_name` + `frontmatter` (chữ); reviewer "chưa hoạt động" | ✅ Telegram: prompt có "Current Chat Context" gồm Platform, Group name/ID, `User: Tên (ID: …)`, và tin nhắn có tiền tố `[From: @user (Tên)]` | ✗ Trong nhóm, `UserID = group:{channel}:{chatID}`, nên USER.md, memory, KG và episodic tự-inject đều theo **nhóm**. DM tính riêng theo người gửi. Ngoại lệ: Discord (`guild:{g}:user:{sender}`) | ◐ Admin gộp contact vào `tenant_user`, **chỉ áp dụng cho DM**. Khi gộp, chuyển USER.md, overrides, profile, `memory_documents/chunks`; không chuyển episodic và KG | ◐ Team task: member nhận `SenderID` gốc (hiện "User: ID …", **không có tên**). Nếu nguồn là nhóm thì `UserID` vẫn là scope nhóm. `delegate`: `UserID` = actor; tên không được truyền | DM tách theo người. Trong nhóm, mọi thành viên dùng chung một USER.md/memory. Bật `share_memory`/`share_kg` thì lộ toàn agent | **Lên hạng ở R2'** (mô hình đội là tổ chức agent), nhưng 5b-in trong nhóm là lỗ hổng chính |
| **AgentTeams (HiClaw)** @89562fb3 | ◐ `Team` CR có `team_leader/worker` (có cấu trúc, quyết định phòng và luồng giao việc). Chức danh là chữ tự do trong `identity/soul`. Không có trường phòng ban (Team đóng vai phòng ban) | ◐ Matrix nhóm: tiền tố `DisplayName: …`, không có mxid. DM: không có tiền tố. Session mặc định theo phòng (room) | ✗ Memory theo worker, session theo room. Không có trí nhớ theo từng người | ✗ `Human` chỉ có OIDC `IdentitySource` + tài khoản Matrix. Kênh DingTalk không map về `Human` | ◐ `requester` chỉ lưu trong project JSON phía Leader để định tuyến báo cáo. Worker chỉ nhận `spec.md` do Leader viết | Memory của worker dùng chung cho mọi người | **Không đổi**: R2' tạm được, 5a/5b yếu và phụ thuộc runtime |
| **Clawith** @45fc701c | ◐− Agent chỉ có `role_description` (chữ, **bị loại khỏi prompt**) và `soul.md`. Phòng ban/chức danh (`OrgDepartment`, `OrgMember.title`) là **của người**. Quan hệ agent↔agent (`relation`) là điều kiện bắt buộc để gọi A2A | ◐ Feishu: mọi tin có tiền tố `[飞书发送者: tên \| user_id \| open_id]`. Nhóm web có hồ sơ người gửi. Chat 1:1 runtime v2 **không có tên** | ✗ `memory/memory.md` ở mức agent được tự inject. Không có trí nhớ theo người. Session nhóm Feishu thuộc về creator của agent | ◐ `channel_user_service` quy người gửi IM về `User` qua OrgMember/email/mobile. Gộp danh tính nhưng không có trí nhớ theo người để gộp | ✗ A2A: goal chỉ ghi "Source Agent" + request. `origin_user_id` chỉ nằm trong DB và dùng để kiểm quyền | memory.md dùng chung toàn agent, nên dễ lộ chuyện của A cho B | **Xuống hạng**: điểm mạnh cũ (hồ sơ người) giờ không còn được tính |
| **Bunkhouse** @3239432c | ✅ `people` (kind `agent`) có `title`, `responsibilities`, `reports_to_id`, `department_id`. Prompt ghi "You are X, Title" kèm danh bạ có cấp trên. `delegate_to_colleague` chặn giao việc ngược lên; `invoke_report` chỉ đi xuống. `departments` chỉ là "nơi chốn" trên sơ đồ | ◐ Web chat có tên, chức danh và quan hệ của người yêu cầu. Slack/Teams **bỏ `event.user`**. Không có Telegram/Zalo | ✗ `memories.scope` chỉ có `agent/company`. Không có trí nhớ theo người | ◐ `people.user_id` ↔ tài khoản đăng nhập (khớp qua email). Không liên kết kênh chat | ◐ Người nhận chỉ thấy "`{fromName}` has delegated…" + brief. `rootRunId` lưu trong DB | Logbook của agent dùng chung cho mọi người yêu cầu | **Lên hạng ở R2'** (mô hình tổ chức agent tốt nhất); 5a/5b và kênh vẫn yếu |
| **Agentic Organization** @bf29743f | ✅ Cây `Department.parent_id` và `Personnel(type=agent, title, role, department_id, manager_id)`. Task được định tuyến theo phòng ban, leo dần lên phòng cha. Prompt có Title/Role/Department/Goals | ✗ Telegram: trạng thái theo `chat_id`, gán "CompanyMember đầu tiên", `run_session(session_id, message)` không có người gửi | ✗ Memory theo agent (`personnel_id`), inject vào mọi phiên | ✗ | ✗ `delegate_to_agent` chỉ truyền `task` + `context` | Memory của agent inject cho mọi người | **R2' đạt rõ, nhưng vẫn loại** vì danh tính gần như bằng 0 |
| **Markus** @bc6f1200 | ✅/◐ `agents.team_id`, `role_id/role_name` (theo template), `agent_role manager/worker`; `teams.lead_agent_id`. Manager nhận ngữ cảnh quản lý đội | ◐ Web: có "You are now talking to **Tên** (role)". Luồng kênh (Feishu) chỉ truyền `senderId`, không có tên. Adapter Telegram có trong mã nhưng **không được nối** vào `start.ts` | ✗ `memories.agent_id`, không có user | ✗ | ✗ Prompt task chỉ là `description`; `createdBy` là agent đã tạo | Memory của agent dùng chung | **Không đổi** (R2' tốt nhưng tầng kênh mỏng) |
| **SwarmClaw** @ed38ba53 | ◐ `orgChart.parentId` + `teamLabel`, `role worker/coordinator`, `delegationTargetAgentIds`. `resolveTeam` giới hạn phạm vi `ask_peer` và phần team trong prompt. Chức danh chỉ là `description/soul` | ✅ `The user "Tên" (ID: …) is messaging from channel "…"`, kèm ghi chú nhóm và lịch sử đánh tiền tố `[SenderName]` | ✗ Mặc định session DM = `channel-peer`, nhóm = `channel`. Memory của connector bị ép theo session. Có thể cấu hình scope `peer` (một session cho mỗi người trong connector) [? chưa chạy] | ✗ | ✗ Subagent chạy với `user: 'agent'`; execution brief không có người gửi | Tốt: memory của connector tách theo session | **Không đổi**; R8 đáng lo (commit cuối 2026-06-30) |
| **Synkora** @2acc1a58 | ◐ Template `agent_roles` (PM/QA/BA…), `category` dạng chữ, `agent_sub_agents` (cha→con, `execution_order`) dùng để chạy workflow/spawn | ◐ Telegram: `[Telegram Context: {type} chat '{title}', User: Tên (@username)]`, không có ID số | ✗ Hội thoại theo (bot, chat, user), memory theo hội thoại | ✗ `HumanContact` chỉ dùng để escalate ra ngoài | ✗ Spawn chỉ truyền `task_description` | Memory tách theo hội thoại, nhưng runtime `user_id` = **người tạo bot** cho mọi người dùng Telegram | **Không đổi** |

**Bằng chứng then chốt cho các ô trong bảng** (chi tiết ở các câu hỏi sau):
- GoClaw đổi UserID sang scope nhóm: [cmd/gateway_consumer_normal.go#L709-L736](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/cmd/gateway_consumer_normal.go#L709-L736) [MÃ]
- Clawith cố ý bỏ `role_description` khỏi prompt: [agent_context.py#L441-L445](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/agent_context.py#L441-L445) [MÃ]
- Bunkhouse chặn giao việc ngược lên cấp trên: [agent-abilities.ts#L759-L791](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/apps/web/src/lib/agent-abilities.ts#L759-L791) [MÃ]
- Agentic Organization định tuyến theo cây phòng ban: [task_requests.py#L96-L130](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/task_requests.py#L96-L130) [MÃ]

### Inferences
- Theo tiêu chí mới, "tổ chức agent" (R2') đã có sẵn ở nhiều nơi. Chỗ còn thiếu thật sự là **trí nhớ theo người, dùng xuyên nhóm và DM (5b-in)**. Đây là thay đổi ở tầng lõi (khoá scope), không phải thêm trường dữ liệu.
- Với GoClaw (nền tảng người dùng đang tự vận hành), lỗ hổng chỉ nằm ở một điểm quyết định: nhánh `default` của `deriveGroupUserID`. Discord đã có mẫu `guild:{g}:user:{sender}`. Làm tương tự cho Telegram/Zalo, tức scope `{channel}:user:{sender}`, rồi tách "ngữ cảnh chung của nhóm" ra một scope riêng, thì sẽ có 5b-in mà vẫn giữ được ngữ cảnh nhóm. Đây là suy luận thiết kế [?], chưa làm và chưa chạy.
- Clawith không còn lợi thế cạnh tranh ở R2', vì cấu trúc agent của nó (`role_description`, `relation`) yếu hơn GoClaw. Lợi thế còn lại là tự quy người gửi IM về `User` (5b-cross); nhưng vì trí nhớ không theo người, lợi thế này chưa tạo ra 5b-in.

### Gaps
- Vòng này không chạy thử nền tảng nào ([CHẠY] = 0). Mọi kết luận về prompt thực tế là [MÃ] hoặc suy luận.
- Chưa đo xem runtime QwenPaw/OpenClaw (worker của AgentTeams) có đưa `meta.sender_id` vào prompt hay không.

## Câu hỏi 2 — GoClaw (bằng chứng chi tiết)

### Takeaway
GoClaw đạt 5a trên Telegram, và mô hình đội lead/member/reviewer là R2' thật. Nhưng trong nhóm, `UserID` bị thay bằng `group:{channel}:{chatID}`, nên USER.md, memory, KG và episodic tự-inject đều theo nhóm, không theo người. Việc gộp contact chỉ áp dụng cho DM và phải làm tay. Delegation truyền ID người gửi nhưng không truyền tên.

### Cited Findings
- **R2' [MÃ]:**
  - Vai trò trong đội là hằng `TeamRoleLead = "lead"`, `TeamRoleMember`, `TeamRoleReviewer` — [internal/store/team_store.go#L34-L36](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/team_store.go#L34-L36)
  - Agent chỉ có `display_name` và `frontmatter` ("short expertise summary"). Không có trường chức danh hay phòng ban — [internal/store/agent_store.go#L48-L49](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/agent_store.go#L48-L49)
- **R2' [MÃ]:** `buildTeamMD` đưa vào prompt "Role: lead/member", danh sách thành viên kèm `frontmatter`, và (với lead) danh sách Reviewers. Luật cho lead: "Always specify `assignee` — match member expertise from the list above" — [internal/agent/resolver_helpers.go#L17-L84](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/agent/resolver_helpers.go#L17-L84)
- **R2' [MÃ]:**
  - `team_tasks create` phân biệt lead và member, và cấm lead tự giao việc cho mình — [internal/tools/team_tasks_create.go#L24-L28](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/team_tasks_create.go#L24-L28), [#L121-L125](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/team_tasks_create.go#L121-L125)
  - Chú thích "reviewer role not yet active" — [internal/tools/team_tasks_lifecycle.go#L117](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/team_tasks_lifecycle.go#L117)
- **5a [MÃ]:**
  - Tiền tố `[From: …]` có ở cả nhóm lẫn DM: [internal/channels/telegram/handlers.go#L556-L579](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/channels/telegram/handlers.go#L556-L579)
  - Nhãn người gửi có dạng `@username (Tên)`: [handlers.go#L241-L246](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/channels/telegram/handlers.go#L241-L246)
  - System prompt có mục "## Current Chat Context" gồm Platform, Chat type, Group name, Group ID và `- User: Tên (ID: …)`. Mục này nằm dưới cache boundary nên được dựng lại mỗi lượt — [internal/agent/systemprompt.go#L492-L494](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/agent/systemprompt.go#L492-L494), [#L557-L601](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/agent/systemprompt.go#L557-L601)
  - `SenderName` lấy từ metadata của kênh: [cmd/gateway_consumer_normal.go#L467](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/cmd/gateway_consumer_normal.go#L467)
- **5b-in [MÃ]:** `deriveGroupUserID` trả về `msg.UserID` cho DM. Với nhóm, thứ tự ưu tiên là:
  1. Discord `guild:{guildID}:user:{senderID}`
  2. openline participant (Bitrix24)
  3. mặc định `group:{channel}:{chatID}`, "shared by everyone in the chat"

  Kết quả này được dùng làm scope cho "context files, memory, traces, and seeding" — [cmd/gateway_consumer_normal.go#L86-L90](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/cmd/gateway_consumer_normal.go#L86-L90), [#L709-L736](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/cmd/gateway_consumer_normal.go#L709-L736)
- **5b-in [MÃ]:** Các hàm `MemoryUserID`, `ContextUserID` và `KGUserID` đều trả `UserIDFromContext` (tức scope nhóm trong nhóm), trừ khi bật cờ shared, lúc đó trả "". `ActorIDFromContext` chỉ dùng cho quyền và audit, và ghi rõ "DO NOT use for memory / KG / session scope" — [internal/store/context.go#L217-L255](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/context.go#L217-L255), [#L289-L330](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/context.go#L289-L330)
- **5b-in, dạng tự động [MÃ]:** episodic L0 auto-inject gọi `UserID: store.MemoryUserID(ctx)` — [internal/agent/loop_pipeline_adapter.go#L291-L307](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/agent/loop_pipeline_adapter.go#L291-L307)
- **5b-in, dạng qua tool [MÃ]:**
  - Tool memory/KG cũng dùng `MemoryUserID`/`KGUserID` — [internal/tools/memory.go#L100](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/memory.go#L100), [internal/tools/knowledge_graph.go#L74](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/knowledge_graph.go#L74)
  - Truy vấn FTS lọc `(user_id IS NULL OR user_id = $4)` — [internal/store/pg/memory_search.go#L102-L116](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/pg/memory_search.go#L102-L116)
- **5b-in [MÃ]:** Tuỳ chọn chia sẻ chỉ có dạng "tất cả hoặc không": `shared_dm`, `shared_group`, `shared_users`, `share_memory`, `share_knowledge_graph`, `share_sessions`. Không có chế độ "theo người xuyên nhóm" — [internal/store/agent_store.go#L360-L367](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/agent_store.go#L360-L367), [internal/agent/loop_context.go#L166-L186](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/agent/loop_context.go#L166-L186)
- **5b-in [MÃ]:** Gợi ý "Known user info… Name=" khi bootstrap chỉ chạy cho DM ("group chats have… multiple senders") — [internal/agent/loop_history.go#L95-L106](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/agent/loop_history.go#L95-L106)
- **5b-cross [MÃ]:**
  - `ResolveTenantUserID` chỉ chạy khi `peerKind == PeerDirect`; chú thích ghi "Group sessions keep the group-scoped userID" — [cmd/gateway_consumer_normal.go#L133-L150](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/cmd/gateway_consumer_normal.go#L133-L150)
  - Truy vấn nối `channel_contacts.merged_id → tenant_users` — [internal/store/pg/contact_resolve.go#L60-L100](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/pg/contact_resolve.go#L60-L100)
- **5b-cross [MÃ]:**
  - Việc gộp do admin làm qua `POST /v1/contacts/merge` (`adminAuth`) — [internal/http/channel_instances.go#L111](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/http/channel_instances.go#L111)
  - Khi gộp, `MigrateUserDataOnMerge` chuyển `user_context_files`, `user_agent_overrides`, `user_agent_profiles`, `memory_documents` và `memory_chunks` sang ID mới. Không thấy episodic summaries hay KG trong hàm này — [internal/http/contact_merge_handlers.go#L191-L212](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/http/contact_merge_handlers.go#L191-L212), [internal/store/pg/agents_context.go#L125-L215](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/pg/agents_context.go#L125-L215)
  - Ghi chú trước đó ("chỉ dùng cho tra cứu credential") **chưa chính xác**. Gộp còn chuyển USER.md và memory docs của DM.
- **5d, team task [MÃ]:**
  - Nội dung giao việc chỉ gồm `[Assigned task #n]: subject`, description và hướng dẫn, không có người yêu cầu — [internal/tools/team_tool_dispatch.go#L95-L120](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/team_tool_dispatch.go#L95-L120)
  - Metadata mang theo `origin_user_id`, `origin_sender_id` và `origin_role` — [team_tool_dispatch.go#L139-L190](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/team_tool_dispatch.go#L139-L190)
  - Member chạy với `SenderID: teammateSenderID`. Nếu nguồn là nhóm thì `UserID` = `group:…`. Không có `SenderName` — [cmd/gateway_consumer_handlers.go#L211-L258](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/cmd/gateway_consumer_handlers.go#L211-L258)
  - Vì vậy prompt của member có "Platform: telegram… User: ID 123…" nhưng không có tên [MÃ, chưa chạy].
- **5d, delegate [MÃ]:**
  - `DelegateRequest.UserID = ActorIDFromContext` (người gửi thật) — [internal/tools/delegate_tool.go#L142-L159](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/delegate_tool.go#L142-L159)
  - `RunRequest` của agent đích có `UserID`, `Channel: "delegate"` và không có `SenderID`/`SenderName` — [cmd/gateway_managed.go#L453-L462](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/cmd/gateway_managed.go#L453-L462)
  - Tuy vậy `ctx` được kế thừa (kể cả qua `context.WithoutCancel` ở chế độ async), mà `SenderIDFromContext` đọc giá trị ctx trước RunContext. Vì thế prompt của agent đích **có thể** vẫn hiện "User: ID …" [? suy luận luồng ctx, chưa chạy] — [delegate_tool.go#L250](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/tools/delegate_tool.go#L250), [internal/store/context.go#L206-L215](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/store/context.go#L206-L215), [internal/agent/loop_context.go#L60-L69](https://github.com/nguyenha935/goclaw/blob/0c2264989c39de37ea11361683074aaf5f3de065/internal/agent/loop_context.go#L60-L69)

### Inferences
- **R2'.** Có thể gán "Content Lead – Phòng Marketing" theo cách sau: đội "Phòng Marketing", agent Leader có role `lead`, và `display_name`/`frontmatter` "Content Lead…". Cấu trúc này được dùng thật: lead giao việc cho member, và đích giao việc bị giới hạn theo `agent_links`. Tuy vậy "chức danh" không phải trường có cấu trúc, và chưa có cây phòng ban nhiều cấp.
- **5b-in.** Mô hình hiện tại cho ra ba scope khác nhau khi A nói chuyện ở G1, G2 và DM. Muốn đạt yêu cầu phải sửa lõi (fork), vì đây là quyết định khoá scope nằm ở consumer.
- **Riêng tư.** Scope nhóm làm cho USER.md của nhóm chứa thông tin cá nhân của A, và B cũng thấy khi B nói trong G1. Scope theo người sẽ chặt hơn, nhưng cần kèm quy tắc "chỉ nhắc chuyện riêng của A khi đang nói với A".

### Gaps
- Chưa chạy thử để xác nhận agent đích của `delegate` thực sự thấy "User: ID …".
- Chưa kiểm kênh Zalo của GoClaw có điền `sender_name`/`display_name` vào metadata hay không, nên dòng "User:" có thể thiếu tên.

## Câu hỏi 3 — AgentTeams/HiClaw (bằng chứng chi tiết)

### Takeaway
Đội có cấu trúc Leader/Worker thật (CRD). Nhưng chức danh chỉ là chữ trong `identity/soul`, người gửi trong nhóm Matrix chỉ hiện tên hiển thị, không có trí nhớ theo từng người, và người yêu cầu gốc chỉ nằm ở phía Leader.

### Cited Findings
- **R2' [MÃ]:**
  - `WorkerSpec` có `Identity`, `Soul`, `Agents` dạng chuỗi, không có title/department — [agentteams-controller/api/v1beta1/types.go#L185-L231](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/agentteams-controller/api/v1beta1/types.go#L185-L231)
  - `TeamSpec` có `WorkerMembers[]{Name, Role: team_leader|worker}`; `TeamReconciler` dựng phòng Matrix và đưa ngữ cảnh runtime vào — [types.go#L453-L491](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/agentteams-controller/api/v1beta1/types.go#L453-L491)
- **R2'/R3 [MÃ]:** Skill giao việc bắt Leader tra Worker trong roster rồi viết spec bằng `taskflow`. `delegate_task` tự @mention Worker — [plugins/teamharness/skills/team/task-delegation/SKILL.md#L45-L56](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/plugins/teamharness/skills/team/task-delegation/SKILL.md#L45-L56)
- **5a [MÃ]:**
  - Trong nhóm, tin nhắn có tiền tố `f"{sender_name}: {text}"` với tên hiển thị lấy từ `_get_display_name`. DM không có tiền tố — [plugins/agentteams-matrix-channel/agentteams_matrix/channel.py#L2439-L2455](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/plugins/agentteams-matrix-channel/agentteams_matrix/channel.py#L2439-L2455)
  - `session_id = f"matrix:{room_id}"`. Mặc định `share_session_in_group=True`, nên `user_id = room_id` ("all participants in the room share one session") — [channel.py#L3222-L3252](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/plugins/agentteams-matrix-channel/agentteams_matrix/channel.py#L3222-L3252), [#L407-L409](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/plugins/agentteams-matrix-channel/agentteams_matrix/channel.py#L407-L409)
- **5b-in [MÃ]:**
  - Manager chỉ đồng bộ **một** tệp `USER.md` thành `PROFILE.md` — [manager/scripts/init/start-qwenpaw-manager.sh#L101-L103](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/manager/scripts/init/start-qwenpaw-manager.sh#L101-L103)
  - Leader có thư mục `memory/` với "durable notes from prior sessions" ở mức agent — [manager/agent/team-leader-agent/AGENTS.md#L9](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/manager/agent/team-leader-agent/AGENTS.md#L9)
  - Không tìm thấy trí nhớ theo từng Human (grep `USER.md`, `per-human` trên manager/plugins/controller).
- **5b-cross [MÃ]:**
  - `HumanSpec` gồm `DisplayName`, `Email`, `PermissionLevel`, `AccessibleTeams/Workers` và `IdentitySource{Issuer, Subject}` (OIDC, để đăng nhập) — [types.go#L620-L650](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/agentteams-controller/api/v1beta1/types.go#L620-L650)
  - Kênh ngoài Matrix chỉ có `ChannelsSpec{DingTalk}` gắn theo worker — [types.go#L374-L376](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/agentteams-controller/api/v1beta1/types.go#L374-L376)
  - Grep `staff_id` trong controller không thấy chỗ nào map người gửi DingTalk về `Human`.
- **5d [MÃ]:**
  - Project lưu `"requester"` và `reply_route` để gửi báo cáo cho người yêu cầu — [plugins/teamharness/mcp/server.py#L3744-L3757](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/plugins/teamharness/mcp/server.py#L3744-L3757)
  - Worker chỉ nhận `spec.md` do Leader viết — [server.py#L3772](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/plugins/teamharness/mcp/server.py#L3772)
  - Khi `submit_task`, sự kiện hoàn thành @mention Leader và "the human members of the team (the task initiator)" — [plugins/teamharness/skills/team/task-execution/SKILL.md#L177-L183](https://github.com/agentscope-ai/AgentTeams/blob/89562fb342564f83ed7c88c1d9d2f5f981897d41/plugins/teamharness/skills/team/task-execution/SKILL.md#L177-L183)

### Inferences
- Worker biết mình làm cho "các thành viên người trong team". Worker chỉ biết đích danh A nếu Leader viết A vào spec.
- Vì 5a/5b phụ thuộc runtime (QwenPaw/OpenClaw), muốn thêm trí nhớ theo người phải làm ở tầng runtime hoặc skill, không phải controller.

### Gaps
- Chưa kiểm QwenPaw có đưa `channel_meta.sender_id` vào prompt khi `share_session_in_group=True` hay không.

## Câu hỏi 4 — Clawith (bằng chứng chi tiết)

### Takeaway
Clawith mô hình hoá tổ chức **con người** rất kỹ, nhưng với agent chỉ có mô tả dạng chữ và quan hệ agent↔agent. Trường `role_description` bị bỏ khỏi prompt một cách có chủ ý. Người gửi IM được quy về `User` ổn định, nhưng trí nhớ nằm ở mức agent, nên chưa có 5b-in.

### Cited Findings
- **R2' [MÃ]:**
  - `Agent.role_description` là `String(500)`, còn `bio` là Text — [backend/app/models/agent.py#L39-L40](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/models/agent.py#L39-L40)
  - `build_agent_context` chứa chú thích "`role_description` remains product metadata and is intentionally ignored by model context assembly", sau đó gọi `del role_description` — [backend/app/services/agent_context.py#L433-L445](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/agent_context.py#L433-L445)
- **R2' [MÃ]:**
  - `OrgDepartment` và `OrgMember{title, department_id}` được "synced from Feishu", tức dành cho người — [backend/app/models/org.py#L1-L63](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/models/org.py#L1-L63)
  - `AgentAgentRelationship.relation` là chuỗi, ví dụ "collaborator", "supervisor", "okr_coordinator" — [org.py#L84-L99](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/models/org.py#L84-L99), [schemas.py#L618](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/schemas/schemas.py#L618)
  - A2A báo `a2a_relationship_missing` khi hai agent không có quan hệ — [agent_runtime/a2a_runtime.py#L441-L462](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/agent_runtime/a2a_runtime.py#L441-L462)
- **5a [MÃ]:**
  - Feishu: `executable_content = f"[{sender_identity}] {content}"` với `飞书发送者: tên | user_id | open_id`, áp dụng cho cả nhóm lẫn p2p — [backend/app/api/feishu.py#L424-L451](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/api/feishu.py#L424-L451)
  - Nhóm nội bộ: `sender_profile` gồm title và department — [agent_runtime/group_context_builder.py#L261-L291](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/agent_runtime/group_context_builder.py#L261-L291)
  - Runtime v2 gọi `prompt_builder(agent.id, agent.name, "", …)` mà không truyền `current_user_name` — [agent_runtime/model_step_service.py#L1601-L1606](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/agent_runtime/model_step_service.py#L1601-L1606)
- **5b-in [MÃ]:**
  - Trí nhớ tự inject là `{agent_id}/memory/memory.md` (tối đa 2000 ký tự), ở mức agent — [agent_context.py#L463-L470](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/agent_context.py#L463-L470)
  - Trí nhớ nhóm là `groups/{id}/agents/{agent}/memory/memory.md` — [group_file_service.py#L125](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/group_file_service.py#L125)
  - Session nhóm Feishu có dạng `feishu_group_{chat_id}` với `user_id=agent.creator_id`; p2p là `feishu_p2p_{sender}` — [feishu.py#L424-L437](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/api/feishu.py#L424-L437)
- **5b-cross [MÃ]:** `resolve_channel_user` đi theo thứ tự:
  1. OrgMember đã liên kết
  2. OrgMember chưa liên kết
  3. khớp email/mobile
  4. tạo User mới

  Kênh được hỗ trợ: dingtalk, wecom, wechat, feishu — [backend/app/services/channel_user_service.py#L74-L208](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/channel_user_service.py#L74-L208)
- **5d [MÃ]:**
  - `_target_goal` chỉ có "Source Agent: {name}. Request: {message}" — [a2a_runtime.py#L700-L707](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/agent_runtime/a2a_runtime.py#L700-L707)
  - `owner_user_id = source_run.origin_user_id or …` chỉ dùng để kiểm quyền và ghi DB — [a2a_runtime.py#L810-L820](https://github.com/dataelement/Clawith/blob/45fc701c366c69f89dff26d91d6a4a9cbc38e6f8/backend/app/services/agent_runtime/a2a_runtime.py#L810-L820)

### Inferences
- Kho `memory.md` dùng chung cho mọi người là rủi ro riêng tư: chuyện của A ghi vào đó sẽ được inject khi B chat.
- Muốn đạt R2' theo đúng nghĩa (chức danh + phòng ban của agent được dùng) thì phải tự thêm. Bảng `OrgDepartment` hiện là của người.

### Gaps
- Chưa kiểm handoff trong nhóm (`group_handoff.py`) để biết agent được giao có thấy tên người khởi tạo qua transcript nhóm hay không.
- Clawith không có Telegram/Zalo (thư mục `api/` chỉ có dingtalk, discord, feishu, slack, wechat, wecom, whatsapp).

## Câu hỏi 5 — Bunkhouse (bằng chứng chi tiết)

### Takeaway
Bunkhouse có mô hình tổ chức agent tốt nhất trong nhóm: chức danh, trách nhiệm và cấp trên nằm trong DB, được đưa vào prompt, và quy tắc giao việc thực thi đúng chiều báo cáo. Nhưng Slack/Teams bỏ người gửi, không có trí nhớ theo người, và không có Telegram/Zalo.

### Cited Findings
- **R2' [MÃ]:**
  - `people` có `kind human|hand` (đổi tên thành `agent` ở migration 0017), `title NOT NULL`, `responsibilities`, `reports_to_id` — [migrations/0002_core.sql#L1-L41](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/migrations/0002_core.sql#L1-L41)
  - Prompt mở đầu bằng `You are ${agent.name}, ${agent.title} at ${company.name}` và có "Company directory" liệt kê chức danh, "reports to" của từng người — [packages/runtime/src/prompt.ts#L156](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/packages/runtime/src/prompt.ts#L156), [#L178-L190](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/packages/runtime/src/prompt.ts#L178-L190)
- **R2' [MÃ]:**
  - `delegate_to_colleague` trả "above you in the reporting line — you cannot assign work upward" — [apps/web/src/lib/agent-abilities.ts#L759-L791](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/apps/web/src/lib/agent-abilities.ts#L759-L791)
  - `invoke_report` chỉ gọi được người "who reports to you" — [#L650-L660](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/apps/web/src/lib/agent-abilities.ts#L650-L660)
  - `departments` là "PLACES" trên sơ đồ, kèm backdrop SVG — [migrations/0040_departments.sql#L1-L20](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/migrations/0040_departments.sql#L1-L20)
  - Grep `department` trong `agent-abilities.ts`/`agent-runs.ts`/`packages/runtime` không có kết quả, tức phòng ban không tham gia định tuyến [MÃ].
- **5a [MÃ]:**
  - `handleSlackEvent` kiểm tra `!event.user` nhưng gọi `executeAgentRun({... input: {type:'chat', message}})` mà không truyền người gửi; Teams cũng vậy — [apps/web/src/lib/chat-bridge.ts#L540-L565](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/apps/web/src/lib/chat-bridge.ts#L540-L565), [#L605-L618](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/apps/web/src/lib/chat-bridge.ts#L605-L618)
  - Web chat: `requesterOf` tra `people` để lấy tên, chức danh và quan hệ manager/colleague — [chat-threads.ts#L635-L668](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/apps/web/src/lib/chat-threads.ts#L635-L668)
  - Prompt có dòng "Authenticated in-app request from {name}, {title}" — [prompt.ts#L250-L260](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/packages/runtime/src/prompt.ts#L250-L260)
- **5b-in [MÃ]:** `memory_scope` chỉ có `'hand','company'` (sau đổi thành `agent`), còn `memories.person_id` là agent sở hữu — [0002_core.sql#L8](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/migrations/0002_core.sql#L8), [#L125-L139](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/migrations/0002_core.sql#L125-L139)
- **5b-cross [MÃ]:** chỉ có "A workspace login and its human directory record are one business identity" (`people.user_id`) — [migrations/0050_person_accounts.sql#L1-L16](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/migrations/0050_person_accounts.sql#L1-L16)
- **5d [MÃ]:** Tin giao việc có dạng `${input.fromName} has delegated a task to you` (tên agent giao) — [prompt.ts#L262-L263](https://github.com/braedonsaunders/bunkhouse/blob/3239432ce2a09df5512fb445b8e259ec2cc060a1/packages/runtime/src/prompt.ts#L262-L263)

### Inferences
- Nếu chọn làm nền, Bunkhouse cho sẵn R2' (sơ đồ tổ chức agent thật), nhưng phải tự viết 5a (Slack/Telegram/Zalo), 5b (trí nhớ theo người) và 5d. Lượng việc lớn hơn so với sửa GoClaw.

### Gaps
- 4★, một tác giả, chưa có release chính thức (theo ghi chú trước). Vòng này không kiểm lại R8.

## Câu hỏi 6 — Agentic Organization (bằng chứng chi tiết)

### Takeaway
R2' đạt trọn vẹn nhất về dữ liệu và định tuyến: cây phòng ban, chức danh và role nằm trong prompt, và task được định tuyến theo phòng ban. Danh tính người dùng thì gần như bằng 0.

### Cited Findings
- **R2' [MÃ]:**
  - `Department.parent_id`, goals, policies — [backend/models.py#L19-L35](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/models.py#L19-L35)
  - `Personnel{department_id, title, role, type human|agent, manager_id}` — [models.py#L37-L50](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/models.py#L37-L50)
- **R2' [MÃ]:**
  - `build_system_prompt` đưa vào Title, Role, Department và Department Goals — [backend/services/agent_runtime.py#L63-L86](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/services/agent_runtime.py#L63-L86)
  - `_route_agent` ưu tiên agent thuộc phòng được yêu cầu, rồi leo lên `parent_id` — [backend/api/task_requests.py#L96-L130](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/task_requests.py#L96-L130)
- **5a [MÃ]:**
  - `_get_or_create_state(chat_id)` gán `company_id` của `CompanyMember` đầu tiên — [backend/api/telegram_bot.py#L127-L142](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/telegram_bot.py#L127-L142)
  - `_run_agent(session_id, message)` không có người gửi — [telegram_bot.py#L239-L247](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/api/telegram_bot.py#L239-L247)
- **5b-in / riêng tư [MÃ]:** `load_agent_memories(person.id)` đưa "Context from your previous sessions" vào **mọi** phiên của agent — [agent_runtime.py#L116-L124](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/services/agent_runtime.py#L116-L124)
- **5d [MÃ]:** `delegate_to_agent` chỉ nhận `task` và `context` — [backend/services/mcp_client.py#L122-L154](https://github.com/fab-agent/agentic-organization/blob/bf29743fbb0c2254b55a40261a9ca4d60406416f/backend/services/mcp_client.py#L122-L154)

### Inferences
- Nên giữ Agentic Organization làm **mẫu tham khảo cho mô hình tổ chức agent** (cây phòng ban kèm định tuyến). Không nên dùng làm nền.

### Gaps
- Không kiểm lại cách ly tenant và R8 trong vòng này.

## Câu hỏi 7 — Markus (bằng chứng chi tiết)

### Takeaway
Markus có đội, role theo template và manager/worker trong DB, nên R2' khá tốt. Nhưng luồng kênh chỉ truyền `senderId` (không có tên), Telegram chưa được nối, và trí nhớ theo agent.

### Cited Findings
- **R2' [MÃ]:**
  - `teams{lead_agent_id, manager_id}` — [packages/storage/src/sqlite-storage.ts#L53-L62](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/storage/src/sqlite-storage.ts#L53-L62)
  - `agents{team_id, role_id, role_name, agent_role DEFAULT 'worker'}` — [sqlite-storage.ts#L64-L85](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/storage/src/sqlite-storage.ts#L64-L85)
  - Manager của đội được xác định qua `agentRole === 'manager'` — [packages/core/src/agent-manager.ts#L4056](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/core/src/agent-manager.ts#L4056)
- **5a [MÃ]:**
  - Handler kênh gọi `agent.sendMessage(text, message.senderId)` mà không có `senderInfo`. Khi khởi động chỉ đăng ký `webui` và `feishu` — [packages/cli/src/commands/start.ts#L1963-L1971](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/cli/src/commands/start.ts#L1963-L1971), [#L2001-L2008](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/cli/src/commands/start.ts#L2001-L2008)
  - `senderInfo` chỉ được dựng khi có `metadata.senderName` — [packages/core/src/agent.ts#L1839-L1845](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/core/src/agent.ts#L1839-L1845)
  - Dòng "You are now talking to **{name}** ({role})" — [packages/core/src/context-engine.ts#L1139-L1143](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/core/src/context-engine.ts#L1139-L1143)
- **5b-in [MÃ]:** bảng `memories(agent_id, type, content)` không có cột user — [sqlite-storage.ts#L131-L138](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/storage/src/sqlite-storage.ts#L131-L138)
- **5d [MÃ]:**
  - Prompt task gồm `[TASK EXECUTION — Task ID]` và `description` — [agent.ts#L5972-L5975](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/core/src/agent.ts#L5972-L5975)
  - Task do agent tạo có `createdBy: ctx.agentId` — [packages/core/src/tools/task-tools.ts#L1597](https://github.com/markus-global/markus/blob/bc6f1200a096e0dac005e8a678b66178e1f084ae/packages/core/src/tools/task-tools.ts#L1597)

### Inferences
- Theo tiêu chí mới, Markus lên hạng ở R2'. Nhưng nó cần một bridge kênh viết lại hoàn toàn (Telegram/Zalo có `senderInfo`) và thêm trí nhớ theo người, nên vị trí tổng thể không đổi.

### Gaps
- Chưa kiểm tầng `requirement` (có thể chứa người yêu cầu) khi đi qua luồng kênh.

## Câu hỏi 8 — SwarmClaw (bằng chứng chi tiết)

### Takeaway
5a tốt nhất cùng GoClaw. R2' ở mức có sơ đồ cha–con và coordinator. Trí nhớ connector bị ép theo session, nên riêng tư tốt nhưng không có 5b-in. Dự án có vẻ đã ngừng: commit cuối 2026-06-30.

### Cited Findings
- **R2' [MÃ]:**
  - `AgentRole = 'worker' | 'coordinator'`, `AgentOrgChart{parentId, teamLabel}`, `delegationTargetAgentIds` — [src/types/agent.ts#L32-L41](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/types/agent.ts#L32-L41), [#L67-L70](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/types/agent.ts#L67-L70), [#L91](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/types/agent.ts#L91)
  - `resolveTeam` là nguồn cho peers, coordinator và directReports, được dùng bởi `ask_peer`, `team_context` và prompt — [src/lib/server/agents/team-resolution.ts#L1-L66](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/lib/server/agents/team-resolution.ts#L1-L66)
- **5a [MÃ]:** Prompt: `The user "${msg.senderName}" (ID: ${msg.senderId}) is messaging from channel "…"`, kèm ghi chú nhóm — [src/lib/server/connectors/connector-inbound.ts#L1066-L1075](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/lib/server/connectors/connector-inbound.ts#L1066-L1075)
- **5b-in [MÃ]:**
  - Scope mặc định: DM `channel-peer`, nhóm `channel` — [connectors/policy.ts#L38-L39](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/lib/server/connectors/policy.ts#L38-L39)
  - Có sẵn scope `peer` (khoá `connector:{id}:agent:{a}:peer:{sender}`) — [policy.ts#L207-L247](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/lib/server/connectors/policy.ts#L207-L247)
  - Memory của connector bị ép `'session'` — [src/lib/server/memory/session-memory-scope.ts#L22-L33](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/lib/server/memory/session-memory-scope.ts#L22-L33)
  - Sở thích của người gửi được lọc theo `entry.sessionId === sessionId` và bỏ qua hoàn toàn trong nhóm — [connectors/contact-preferences.ts#L42-L73](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/lib/server/connectors/contact-preferences.ts#L42-L73)
- **5d [MÃ]:**
  - Session con có `user: 'agent'`; `parentContext` là execution brief — [src/lib/server/agents/subagent-runtime.ts#L300-L326](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/lib/server/agents/subagent-runtime.ts#L300-L326)
  - Brief chỉ gồm Objective, Summary, Facts, Plan…, không có người gửi — [src/lib/server/execution-brief.ts#L244-L259](https://github.com/swarmclawai/swarmclaw/blob/ed38ba5329c20e48c03b4a4028f4a76a1a75e2d1/src/lib/server/execution-brief.ts#L244-L259)
- **R8 [MÃ/git]:** HEAD `ed38ba53` ngày 2026-06-30, tag mới nhất `v1.9.40` (`git ls-remote`). Kết quả khớp ghi chú trước ("sắp trượt từ 2026-09-30").

### Inferences
- Đặt scope `peer` sẽ gộp session DM và các nhóm của A trong cùng một connector. Nhưng khi đó agent mất ngữ cảnh chung của nhóm, và session chứa lẫn nội dung của nhiều nhóm. Cách này không đạt đúng yêu cầu [? chưa chạy].

### Gaps
- Chưa chạy scope `peer` để xem hành vi khi trả lời trong nhóm.

## Câu hỏi 9 — Synkora (bằng chứng chi tiết)

### Takeaway
Synkora có role template và cây sub-agent dùng được cho workflow. Telegram có tên/username nhưng không có ID số. Trí nhớ theo hội thoại. Runtime chạy với `user_id` của người tạo bot.

### Cited Findings
- **R2' [MÃ]:**
  - `AgentRole{role_type, role_name, system_prompt_template}` — [api/src/models/agent_role.py#L45-L63](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/models/agent_role.py#L45-L63)
  - `agent.category`, `role_id`, `human_contact_id` — [api/src/models/agent.py#L98-L125](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/models/agent.py#L98-L125)
  - `AgentSubAgent{parent_agent_id, sub_agent_id, execution_order}` — [api/src/models/agent_sub_agent.py#L24-L27](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/models/agent_sub_agent.py#L24-L27)
  - Sub-agent được nạp theo thứ tự `execution_order` để `WorkflowFactory.create_executor` dựng workflow — [api/src/services/agents/chat_stream_service.py#L940-L960](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/services/agents/chat_stream_service.py#L940-L960)
- **5a [MÃ]:**
  - `context_message = "[Telegram Context: {chat_type} chat '{chat_display}', User: {user_display} (@{user_name})]"` — [api/src/services/telegram/telegram_polling_service.py#L240-L259](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/services/telegram/telegram_polling_service.py#L240-L259)
  - `user_id=str(telegram_bot.created_by)` — [#L320](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/services/telegram/telegram_polling_service.py#L320)
- **5b-in [MÃ]:**
  - Hội thoại được khoá theo `telegram_bot_id + telegram_chat_id + telegram_user_id` — [telegram_polling_service.py#L442-L446](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/services/telegram/telegram_polling_service.py#L442-L446)
  - Memory gồm cửa sổ tin gần, tóm tắt hội thoại và RAG từ KB — [api/src/services/agents/conversation_memory_service.py#L1-L10](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/services/agents/conversation_memory_service.py#L1-L10)
- **5b-cross [MÃ]:** `HumanContact{email, slack_user_id, whatsapp_number, account_id}` chỉ được dùng trong `roles/human_escalation_service` và tool role. Grep `HumanContact` trong `services/slack|whatsapp|telegram` = 0 — [api/src/models/human_contact.py#L33-L47](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/models/human_contact.py#L33-L47)
- **5d [MÃ]:** `execute_spawn_agent_task.delay(tenant_id, parent_agent_id, task_description, target_agent_name, …)` — [api/src/services/agents/internal_tools/spawn_agent_tool.py#L147-L153](https://github.com/getsynkora/synkora-ai/blob/2acc1a5832d32d57627fdcbf5421bd98e5144e63/api/src/services/agents/internal_tools/spawn_agent_tool.py#L147-L153)

### Inferences
- Với `user_id` = người tạo bot, token OAuth và tính năng cấp user của người tạo bị áp cho mọi người chat trên Telegram. Đây là rủi ro riêng tư/bảo mật [? hệ quả chưa chạy].

### Gaps
- Chưa kiểm kênh Slack/WhatsApp của Synkora có truyền người gửi hay không.

## Câu hỏi 10 — Sàng lọc lại các tên từng bị hạ hạng vì tiêu chí cũ "chức danh/quyền của người dùng"

### Takeaway
Hai tên đáng xem kỹ lại vì mạnh đúng ở chỗ còn thiếu (5b-in) mà trước đây bị trừ điểm vì "người không có chức danh/role cứng":
- **Hivekeep:** hồ sơ contact ↔ nhiều platform ID, ghi chú về người được tự inject mỗi lượt.
- **NarraNexus:** thực thể xã hội theo `user_id`, được tự inject.

Hai tên có thể xem nhanh: **Rakazo** (liên kết danh tính bằng mã) và **UniEmployee**. Các tên còn lại bị loại vì lý do khác (R1, R8, không có kênh, bỏ người gửi), nên tiêu chí mới không cứu được.

### Cited Findings
- **Hivekeep** (`MarlBurroW/hivekeep` @7d023c95, MIT), **nên đánh giá sâu lại:**
  - Trước đây bị trừ vì người gửi từ kênh bị gán cứng role `'external'` và không có chức danh/phòng ban cho người. Cả hai lý do đều không còn quan trọng.
  - Mã [MÃ]: `contacts` ↔ `contact_platform_ids(platform, platform_id)` ↔ `contact_notes(scope private|global|user, agentId)` — [src/server/db/schema.ts#L283-L333](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L283-L333)
  - Mỗi lượt có khối "## Current speaker" gồm tên, shared notes, notes của user nền tảng và "Your personal notes" về **người đó**. Đây là 5b-in dạng **tự động, theo người** — [src/server/services/prompt-builder.ts#L886-L932](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/services/prompt-builder.ts#L886-L932)
  - Điểm yếu mới lộ ra theo R2': `agents` chỉ có `role` và `expertise` dạng chữ, không có team hay phòng ban — [schema.ts#L127-L141](https://github.com/MarlBurroW/hivekeep/blob/7d023c952e46861070683825ff545daf981910f0/src/server/db/schema.ts#L127-L141)
  - Có `inter-agent-tools.ts` nhưng chưa đọc, nên chưa rõ 5d.
- **NarraNexus** (`NetMindAI-Open/NarraNexus` @5869502c, Apache-2.0), **nên xem lại:**
  - `hook_data_gathering` tự nạp thực thể theo `ctx_data.user_id`, và dự phòng bằng fuzzy match theo `sender_name` — [src/xyz_agent_context/module/social_network_module/social_network_module.py#L172-L230](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/module/social_network_module/social_network_module.py#L172-L230)
  - Thực thể có `aliases` (ID xuyên hệ thống) và `identity_info` — [schema/entity_schema.py#L36-L65](https://github.com/NetMindAI-Open/NarraNexus/blob/5869502c9a405b3e762206ecd21ea16540d75794/src/xyz_agent_context/schema/entity_schema.py#L36-L65)
  - Kho thực thể gắn theo **instance của agent** (mỗi agent một kho), không phải danh bạ trung tâm. Theo ghi chú trước, việc gộp đa kênh do LLM quyết định.
  - R2' (vai trò/phòng ban agent) và nhịp phát triển (tag v1.15.0 ngày 2026-08-05) chưa kiểm.
- **Rakazo** (`elie222/rakazo`), **xem nhanh**, theo ghi chú trước, vòng này chưa kiểm lại mã:
  - `MessagingIdentity(provider, address) → userId`, gắn bằng `MessagingLinkCode` (5b-cross tốt).
  - Lý do bị trừ trước đây một phần là "`User` chỉ có name/email, không có chức danh", nay không còn tính.
  - Vẫn còn cản trở: mô hình "trợ lý riêng cho mỗi user" (`botId @unique` cho mỗi địa chỉ); nhóm chat chỉ có tên hiển thị; nhóm là "sendblue-only"; `Bot` có `title`/`parentBotId` nhưng không có phòng ban — [ghi chú trước: new_candidates_global.md, mục C](https://github.com/elie222/rakazo/blob/11476f472c2a0c978a41cceadc635666dd7eea66/packages/db/prisma/schema.prisma#L1129)
- **UniEmployee** (`zj-unicom-ai/UniEmployee`), **tuỳ chọn**, theo ghi chú trước, chưa kiểm lại:
  - Người gửi IM được biểu diễn là `im:{channel}:{sender}` (5a/5b-in tính theo từng kênh). Phần "OIDC ánh xạ department" là cho người, nên nay mất ý nghĩa.
  - R6 chỉ có webhook chung. Chỉ đáng xem nếu cần tham khảo HITL — [ghi chú trước: new_candidates_asia.md](https://github.com/zj-unicom-ai/UniEmployee)
- **Không cần xem lại**, vì lý do loại không nằm ở chức danh/quyền của người (theo ghi chú trước):
  - Hezo: trượt R1, runtime là CLI.
  - OpenVort: trượt R8, release cuối 2026-04-27.
  - CowAgent: một `USER.md`, hướng một người dùng.
  - OneManCompany: không có kênh chat, "CEO là người duy nhất".
  - FleetQ: Telegram bỏ ID người gửi, chạy với quyền owner.
  - VisionClaw: mọi kênh đổ về tenant admin #1.
  - Foundry: không có kênh chat.
  - AutoBot-AI: gateway không tra danh bạ `llc`.
  - Wegent: executor dựa trên Codex, hướng lập trình.

  Nguồn: [rejected_recheck.md / new_candidates_*.md trong research_notes](https://github.com/hezo-ai/hezo/blob/0fd10878bf9771b190f879998946ba8641d0b383/packages/server/src/services/chat-channels/ingest.ts)

### Inferences
- Nếu mục tiêu là "GoClaw (R2' đã có) + 5b-in", thì Hivekeep là **mẫu thiết kế** tốt nhất để chép: khoá theo contact, map platform ID, ghi chú có scope, và khối "Current speaker" tự inject. Đây là mẫu tham khảo, không phải nền thay thế, vì Hivekeep thiếu tổ chức agent.
- NarraNexus cho thấy một cách khác: mỗi agent tự học hồ sơ từng người. Nhưng việc gộp danh tính dựa trên xác suất (LLM, fuzzy theo tên) nên không hợp làm nguồn chuẩn.

### Gaps
- Rakazo, UniEmployee, Wegent, CowAgent và các tên khác trong danh sách "không cần xem lại" chưa được kiểm lại mã trong vòng này; kết luận dựa trên ghi chú trước.
- Hivekeep: chưa đọc `inter-agent-tools.ts` (5d) và chưa kiểm ghi chú `private` có thực sự tách giữa các agent hay không.
- NarraNexus: chưa kiểm `ctx_data.user_id` trong nhóm Telegram là người gửi hay là nhóm.
