# Kiểm chứng lại GoClaw, Paperclip, SwarmClaw, Synkora từ mã nguồn (2026-09-27)

Ngày kiểm: 2026-09-27 (xác nhận bằng `date`: Sun Sep 27 03:41 UTC 2026). Mọi repo được clone mới (`git clone --filter=blob:none`) rồi đọc mã; không dùng README làm bằng chứng. Nhãn: [MÃ] đọc mã/git, [DOC] chỉ tài liệu/trang web, [CHẠY] đã cài chạy (lần này KHÔNG cài chạy gì), [?] chưa kiểm chứng. Commit đã đọc:
- GoClaw upstream `dev` = `16ba6a5a7c67` (2026-09-26T18:32:22+07:00); `main` = `549c81fd2406` (2026-09-15T02:01:48+07:00). Fork của người dùng `/home/user/goclaw` (nguyenha935/goclaw) HEAD `4d3c6bcb` (2026-07-04) — chỉ đọc, không sửa; commit này nằm trong lịch sử upstream và đang chậm 227 commit so với upstream `dev`.
- Paperclip `master` = `640dee18029f` (2026-09-26T21:23:33-05:00).
- SwarmClaw `main` = `ed38ba5329c2` (2026-06-30T21:58:09+01:00) — không có commit nào sau ngày này.
- Synkora `master` = `2acc1a5832d3` (2026-09-26T14:33:00+08:00).
- dewee-web-v2 (site + docs của Dewee, repo công khai của nextlevelbuilder) = `6fd9cb2356f1` (2026-09-26T00:18:20+07:00).

## GoClaw — giấy phép, kích thước, độ "sống", issue #565

### Takeaway
LICENSE upstream đúng là CC BY-NC 4.0 thuần (38 dòng, không có điều khoản kinh doanh kèm theo hay ngoại lệ thương mại); con đường dùng cho mục đích thương mại chính thức là sản phẩm đóng Dewee ($500/năm để kết nối kênh chat). Nhánh `dev` vẫn chạy nhờ contributor cộng đồng và tag beta tự động, nhưng bản stable cuối là v3.14.0 (2026-06-15), `main` gần như đóng băng, và các maintainer sáng lập không commit từ tháng 6/2026.

### Cited Findings
- [MÃ] `LICENSE` dòng 1: "Creative Commons Attribution-NonCommercial 4.0 International"; dòng 20: "NonCommercial — You may not use the material for commercial purposes." Không có dual license, không có ngoại lệ thương mại; `main` và `dev` giống hệt nhau; chỉ có 2 commit chạm file này (b9a1808a 2026-03-15 "chore: add CC BY-NC 4.0 license", 17965bcf 2026-04-11 "Update copyright holder") — [LICENSE @16ba6a5a](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/LICENSE); README dòng 371–373 cũng ghi CC BY-NC 4.0 — [README.md](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/README.md#L371-L373)
- [MÃ] Chỉ có đúng một chỗ trong repo nhắc tới "commercial license": `skills/anysearch/MAINTENANCE.md:130` "GoClaw's repository license is CC BY-NC 4.0 (plus a commercial license for production use)". Đây là tài liệu của một skill do contributor thêm vào ngày 2026-09-24 (commit c4be30cc, múi giờ +08:00), không phải văn bản pháp lý của dự án — [MAINTENANCE.md](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/skills/anysearch/MAINTENANCE.md#L130)
- [DOC] FAQ của Dewee (cập nhật 2026-09-25): "dewee grew out of GoClaw, but it is a separate, closed-source product … GoClaw remains open and free for non-commercial use." — [dewee faq.md](https://github.com/nextlevelbuilder/dewee-web-v2/blob/6fd9cb23/src/content/docs/en/resources/faq.md#L13-L15)
- [MÃ] Mã nguồn GoClaw không có bước kiểm tra license key nào (grep `license key|LicenseKey` trong `internal/` và `cmd/` không ra kết quả). Việc khóa kênh chat bằng license chỉ có ở Dewee — [goclaw @16ba6a5a](https://github.com/nextlevelbuilder/goclaw/tree/16ba6a5a)
- [MÃ] Kích thước ở `dev` 16ba6a5a: 4.623 file được track; 2.526 file `.go` với 557.562 dòng Go; 1.097 file ts/tsx với 126.058 dòng; tổng số dòng của mọi file text ≈ 849k. Con số cũ "~2.411 file, 532k dòng" khớp nếu chỉ đếm file `.go` ở một thời điểm trước đây — nay đã tăng — [repo tree](https://github.com/nextlevelbuilder/goclaw/tree/16ba6a5a)
- [MÃ/git] Tag mới nhất: `v3.15.0-beta.219` (2026-09-26 11:42 UTC), do `github-actions[bot]` tạo. Có 173 tag từ 2026-06-27 đến nay, gần như toàn bộ là beta tự sinh sau mỗi lần push lên `dev`. Stable cuối: `v3.14.0` (2026-06-15 15:50 +07:00). Trước đó: v3.13.2/3.13.1/3.13.0 (2026-06-03), v3.12.0 (2026-05-20). Bản desktop cuối: `lite-v3.9.1` (2026-04-27) — [tags](https://github.com/nextlevelbuilder/goclaw/tags)
- [MÃ/git] Số commit theo tháng (commit date, mọi commit reachable / không tính merge / first-parent): **dev** — 2026-03: 826/822/818; 04: 628/599/544; 05: 165/132/53; 06: 177/141/97; 07: 154/147/126; 08: 42/27/23; 09 (tới 2026-09-26): 45/33/29. Riêng 2026-09-01→09-12: 25 commit (19 không tính merge); 2026-09-13→09-26: thêm 20 commit. **main** — 06: 93; 07: 4; 08: 5; 09: 2 — [commits dev](https://github.com/nextlevelbuilder/goclaw/commits/dev)
- [MÃ/git] `main` chậm hơn `dev` **315 commit** (`git rev-list --count origin/main..origin/dev`); `dev` thiếu 1 commit của `main` (549c81fd, fix vault, được forward-port qua PR #1580) — [compare](https://github.com/nextlevelbuilder/goclaw/compare/main...dev)
- [MÃ/git] Maintainer sáng lập đã ngừng: `viettranx` (1.181 commit, nhiều nhất) commit cuối 2026-06-03; "Goon" commit cuối 2026-06-15; "Duy /zuey/" commit cuối 2026-06-21. Từ 2026-07-01, 31/34 merge commit là của "Clark Cant"; 62 tác giả khác nhau commit trong 90 ngày gần nhất — [commits](https://github.com/nextlevelbuilder/goclaw/commits/dev)
- [DOC] Issue #565 "feat: Enterprise Identity — Keycloak SSO, org structure, per-project RBAC, channel pairing": **vẫn Open**, mở ngày 2026-03-30 bởi `duhd-vnpay` (contributor bên ngoài, không phải maintainer). Nhãn: enhancement, agent:github-maintain, maintain:triaged. Không có comment, PR liên kết, milestone hay assignee. Trích nguyên văn: "No verified identity: sender_id is a platform-specific number. Agent can't distinguish a CTO from a random group member." và "Users are opaque string IDs — agents don't know who they're talking to, can't gate tools by permission, and can't route work to the right person." Issue đề xuất các bảng org_users, departments, department_members, project_members, pairing_verifications — [issue #565](https://github.com/nextlevelbuilder/goclaw/issues/565)
- [MÃ] Không file `.go` hay `.sql` nào chứa `org_users`, `department_members`, `pairing_verifications` hay `keycloak`, tức đề xuất #565 chưa được triển khai — [goclaw @16ba6a5a](https://github.com/nextlevelbuilder/goclaw/tree/16ba6a5a)

### Inferences
- Nói "#565 thừa nhận…" thì chưa chính xác. Đó là đề xuất của một người ngoài dự án. Maintainer không phản hồi mà chỉ gắn nhãn "triaged". Tuy vậy, mô tả trong issue khớp với mã hiện tại (xem phần identity bên dưới).
- Tiêu chí R8 chỉ đạt theo nghĩa hẹp: tag beta sinh tự động mỗi ngày, trong khi stable cuối (2026-06-15) đã nằm ngoài cửa sổ 3 tháng (mốc 2026-06-27). Người sáng lập ngừng commit gần như cùng lúc Dewee/AgentBrain ra mắt. Vì vậy GoClaw OSS có dấu hiệu chuyển sang chế độ do cộng đồng duy trì.
- Dùng GoClaw để vận hành phòng Marketing của một doanh nghiệp rất khó được coi là "phi thương mại" theo điều khoản NonCommercial. Chính nhà phát triển cũng hướng việc dùng thương mại sang Dewee.

### Gaps
- Định nghĩa pháp lý "NonCommercial" trong legalcode CC BY-NC 4.0 chưa đọc trực tiếp được vì creativecommons.org bị proxy chặn [?]. Kết luận ở trên dựa vào LICENSE trong repo và FAQ của Dewee.
- Không biết ai là người bấm merge thực tế và vai trò chính thức của "Clark Cant", vì không được gọi api.github.com.

## GoClaw — chế độ điều phối, bộ định tuyến team-work, duyệt task, tách việc

### Takeaway
Code định nghĩa 3 chế độ spawn / delegate / team dựa trên cấu hình tổ chức, không phải "auto/explicit/manual" như README ghi. Bộ định tuyến team-work đúng như mô tả cũ: embedding làm bằng chứng, LLM arbiter quyết định, rồi khóa tool. Tuy nhiên arbiter được dặn chỉ chọn team khi người dùng yêu cầu rõ ràng. Không có bộ tách việc/planner. Duyệt task là tùy chọn, và approve/reject nằm ở `teams_tasks.go` chứ không ở `teams_tasks_human.go`.

### Cited Findings
- [MÃ] `internal/agent/orchestration_mode.go`: `ModeSpawn="spawn"`, `ModeDelegate="delegate"`, `ModeTeam="team"`. `ResolveOrchestrationMode` chọn theo thứ tự ưu tiên team > delegate > spawn, dựa vào việc agent có thuộc team hay có delegate link. `orchModeDenyTools` ẩn `delegate`/`team_tasks` tùy mode — [orchestration_mode.go#L11-L58](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/orchestration_mode.go#L11-L58)
- [MÃ] README vẫn ghi "3 orchestration modes (auto/explicit/manual)" ([README.md#L67](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/README.md#L67)); UI i18n cũng ghi "Three delegation modes: auto, explicit, and manual" ([agents.json#L96](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/ui/web/src/i18n/locales/en/agents.json#L96)). Trong code không có hằng số auto/explicit/manual; tham số `mode` của delegate tool chỉ nhận `sync`/`async`, mặc định `async` ([delegate_tool.go#L275-L277](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/tools/delegate_tool.go#L275-L277)). **README lệch với code.**
- [MÃ] `internal/teamworkclassify/classifier.go`: `DefaultCloseMargin = 0.08`, `defaultTeamThreshold = 0.35`, evidence timeout 8s, arbiter timeout 30s. Nếu |diff| ≤ margin thì chọn self; nếu diff > margin và collabScore ≥ 0.35 thì chọn team. `ClassifyWithLLM` dùng kết quả embedding làm bằng chứng/fallback, sau đó gọi LLM arbiter (max_tokens 300, temperature 0) — [classifier.go#L33-L36](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/teamworkclassify/classifier.go#L33-L36), [#L157-L201](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/teamworkclassify/classifier.go#L157-L201)
- [MÃ] Prompt của arbiter: "If uncertain, choose self…"; "Choose team only when the user explicitly asks to assign, delegate, split work, ask other members, create tasks, gather opinions, or perform new multi-role work." Tin nhắn trông giống chat thường thì trả về self ngay (`looksCasualOrSmallDirect`) — [classifier.go#L283-L300](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/teamworkclassify/classifier.go#L283-L300)
- [MÃ] Khi chọn team: chèn khối `## TEAM WORK ROUTING LOCK` ([team_work_directive.go#L42](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/team_work_directive.go#L42)). Nếu vòng đầu model không gọi đúng tool thì retry với `OptToolChoice = "required"` ([#L86](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/team_work_directive.go#L86)). Được gọi từ `internal/gateway/methods/chat.go:296` và `cmd/gateway_team_work_classify.go:53`.
- [MÃ] Approve/Reject của con người nằm ở `internal/gateway/methods/teams_tasks.go:174` (`handleTaskApprove`) và `:238` (`handleTaskReject`). File `teams_tasks_human.go` có thật nhưng được thêm ngày 2026-09-09 (commit 60cf79de, #1559) và chỉ chứa `handleTaskCancel` (:35) và `handleTaskRetry` (:129). Comment đầu file viết: "Until now a human could only … approve/reject one sitting in in_review" — [teams_tasks_human.go#L17-L25](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/gateway/methods/teams_tasks_human.go#L17-L25), [teams_tasks.go#L174](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/gateway/methods/teams_tasks.go#L174). Fork của người dùng (2026-07-04) chưa có file này.
- [MÃ] Task chỉ vào `in_review` khi lead agent (LLM) tự truyền `require_approval=true`; mô tả tham số là "Require user approval before claim (for create, default false)" ([team_tasks_create.go#L128-L131](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/tools/team_tasks_create.go#L128-L131), [team_tasks_tool.go#L76-L78](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/tools/team_tasks_tool.go#L76-L78)). Comment trong code: "Note: reviewer role not yet active. All approvals flow through leader or dashboard." ([team_tasks_lifecycle.go#L187](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/tools/team_tasks_lifecycle.go#L187))
- [MÃ] Không có bộ tách việc: grep `decompos|task_planner|TaskPlanner|subtask tree|acceptance criteria` trong `internal/` và `cmd/` (bỏ test) chỉ ra 2 kết quả nói về chuẩn hóa Unicode (`internal/workstation/security/normalize.go:31`, `internal/agent/media_filename.go:35`). `intent_classify.go` chỉ phân loại status_query/cancel/steer/new_task khi agent đang bận — [intent_classify.go](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/intent_classify.go)
- [MÃ/git] Chạy `git log origin/dev -i -E --grep='decompos|planner|subtask|acceptance criteria|clarif'`: không commit nào thêm tính năng tách việc; các kết quả khớp đều là commit docs/fix ngẫu nhiên (ví dụ 83f5fd17 "docs: clarify Zalo Bot API integration", 2026-09-22) — [commits dev](https://github.com/nextlevelbuilder/goclaw/commits/dev)

### Inferences
- Với yêu cầu mơ hồ kiểu "làm chiến dịch Tết cho sản phẩm X", arbiter được hướng về self (tức lead tự làm), trừ khi người dùng nói rõ "giao cho team". Nghĩa là R3 trượt đúng ở trường hợp người dùng cần nhất.
- Duyệt task phụ thuộc việc LLM có tự bật `require_approval` hay không. Không có cổng bắt buộc trước khi đăng bài hay chi tiền.

### Gaps
- Chưa chạy thực tế để xem tỉ lệ arbiter chọn team với các prompt tiếng Việt mơ hồ [?].

## GoClaw — danh tính (R5), kênh chat, điểm mở rộng không cần fork

### Takeaway
Agent biết nền tảng, loại chat, tên/ID nhóm và tên/ID người gửi. Việc "gộp" danh tính (contact → tenant_user) có thật nhưng phải làm tay và **chỉ dùng cho tra cứu credential**; phiên, bộ nhớ và USER.md vẫn gắn theo ID kênh. Hồ sơ tenant_user chỉ có display_name + role RBAC dashboard + metadata JSON, không có chức danh/phòng ban, và không được đưa vào prompt. Delegation có mang theo UserID/SenderID/Role để phân quyền, nhưng không mang tên hay hồ sơ người yêu cầu. Có 10 loại kênh; muốn thêm kênh phải sửa core.

### Cited Findings
- [MÃ] `internal/agent/user_identity_resolver.go:11-13`: `type UserIdentityResolver interface { ResolveTenantUserID(ctx context.Context, channelType, senderID string) (string, error) }`. Comment tại :10: "Used by the agent loop to set CredentialUserID in context before tool execution." Với chat nhóm, resolver thử group contact trước rồi mới tới người gửi (#1482, 2026-07-28) — [user_identity_resolver.go#L10-L95](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/user_identity_resolver.go#L10-L95)
- [MÃ] `internal/agent/loop_context.go:74-81`: "Keeps UserID unchanged (session/workspace scoping) but sets a separate CredentialUserID for SecureCLI, MCP, and other per-user features." ID đã gộp chỉ được dùng ở credentialed_exec, MCP theo từng user, cron và cookie — [loop_context.go#L70-L81](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/loop_context.go#L70-L81)
- [MÃ] SQL gộp danh tính: `channel_contacts cc JOIN tenant_users tu ON cc.merged_id = tu.id WHERE cc.tenant_id=$1 AND cc.channel_type=$2 AND cc.sender_id=$3` (có cache TTL 60s) — [contact_resolve.go#L62-L90](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/store/pg/contact_resolve.go#L62-L90). Việc gộp làm thủ công qua `POST /v1/contacts/merge` hoặc trang Contacts — [contact_merge_handlers.go#L16](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/http/contact_merge_handlers.go#L16)
- [MÃ] `TenantUserData` gồm ID, TenantID, UserID, DisplayName, Role, Metadata (JSON), CreatedAt, UpdatedAt ([tenant_store.go#L43-L52](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/store/tenant_store.go#L43-L52)). Role chỉ có owner/admin/operator/member/viewer ([#L24-L28](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/store/tenant_store.go#L24-L28)), là quyền RBAC trên dashboard. Không có trường chức danh hay phòng ban (grep `job title|department` trong Go chỉ ra prompt của knowledge graph). Trong `internal/agent/` chỉ `loop_mcp_user.go` và `user_identity_resolver.go` đụng tới tenant user, và không đoạn nào đưa role/metadata vào system prompt.
- [MÃ] Prompt "## Current Chat Context" (thêm 2026-05-31, commit 2a523e3f) gồm Platform, Chat type, Group name, Group ID và dòng "- User: {SenderName} (ID: {SenderID})", có ghi chú "untrusted platform metadata" — [systemprompt.go#L564-L603](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/systemprompt.go#L564-L603); các trường cấu hình ở [systemprompt.go#L108-L112](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/systemprompt.go#L108-L112)
- [MÃ] Delegation: `DelegateRequest` sao chép `UserID`, `SenderID` ("real acting sender preserved…", #915) và `Role` từ context ([delegate_tool.go#L347-L367](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/tools/delegate_tool.go#L347-L367)). `buildAgentLinkRunRequest` đặt cho agent con `Channel: "delegate"` và giữ UserID/SenderID/Role, nhưng **không có SenderName** ([cmd/gateway_delegate.go#L18-L37](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/cmd/gateway_delegate.go#L18-L37)). Team task lưu `user_id`, `channel` ([team_store.go#L106-L107](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/store/team_store.go#L106-L107))
- [MÃ] Trong nhóm, UserID của phiên là ID ghép dạng `group:{channel}:{chatID}` ([telegram/commands.go#L110](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/channels/telegram/commands.go#L110)). Vì vậy USER.md và bộ nhớ theo user trong nhóm là của **cả nhóm**, không phải của từng người gửi.
- [MÃ] Kênh (`internal/channels/channel.go:76-85`): bitrix24, discord, facebook, feishu, pancake, slack, telegram, whatsapp, zalo_oa, zalo_personal, tổng 10 loại. Danh sách cũ (7 kênh) thiếu Facebook, Pancake (pages.fm) và Bitrix24 — [channel.go#L76-L85](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/channels/channel.go#L76-L85)
- [MÃ] Kênh "zalo_oa" thực chất gọi **Zalo Bot API** (`https://bot-api.zaloplatforms.com`), chỉ DM, không có nhóm, giới hạn 2.000 ký tự ([zalo/zalo.go#L1-L5](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/channels/zalo/zalo.go#L1-L5), [#L38](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/channels/zalo/zalo.go#L38)). Hai nhánh OA API thật (`feat/zalo-oa-oauth-966`, cuối 2026-04-27; `feat/zalo-oa-webhook-966-clean`, cuối 2026-05-02) chưa merge vào `dev`, đang đi trước dev lần lượt 78 và 148 commit [MÃ/git].
- [MÃ] Cách đăng ký kênh: `type ChannelFactory func(name string, creds json.RawMessage, cfg json.RawMessage, msgBus *bus.MessageBus, pairingSvc store.PairingStore) (Channel, error)` ([instance_loader.go#L33-L34](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/channels/instance_loader.go#L33-L34)); `(*InstanceLoader).RegisterFactory` ở :90. Tất cả được gọi cứng trong `cmd/gateway.go` các dòng 906–914 và 930 ([gateway.go#L906-L930](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/cmd/gateway.go#L906-L930)). Thêm kênh mới nghĩa là phải sửa core và build lại; thư mục `extensions/` chỉ chứa một Chrome extension đồng bộ cookie.
- [MÃ] Hook không cần fork: sự kiện `user_prompt_submit`, handler kiểu `command|http|prompt|script` ([hooks/types.go#L24-L80](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/hooks/types.go#L24-L80)). Handler kiểu script (Goja ES5.1, chạy sandbox) có thể trả về `AdditionalContext`, phần này được nối vào `ExtraSystemPrompt` ([pipeline/context_stage.go#L53-L71](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/pipeline/context_stage.go#L53-L71), [script_result.go#L16-L19](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/hooks/script_result.go#L16-L19)). Tuy nhiên `hooks.Event` chỉ mang SessionID/TenantID/AgentID/RawInput, không có SenderID hay tên người gửi ([types.go#L217-L239](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/hooks/types.go#L217-L239)). Session key có dạng `agent:%s:%s:%s:%s` = agentID:channel:kind:chatID ([sessions/key.go#L48-L49](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/sessions/key.go#L48-L49)).
- [MÃ] API ghi hồ sơ theo từng user: `PUT /v1/agents/{id}/instances/{userID}/files/{fileName}` (cần admin), chỉ cho phép `USER.md` ([http/agents.go#L207](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/http/agents.go#L207), [agents_instances.go#L79-L97](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/http/agents_instances.go#L79-L97)).

### Inferences
- **Điểm mở rộng để tự xây R5 mà không fork GoClaw** (đều có giới hạn):
  1. Ghi hồ sơ (chức danh, phòng ban, quyền) vào `USER.md` của từng user qua `PUT /v1/agents/{id}/instances/{userID}/files/USER.md`. Chỉ hiệu quả với DM, vì trong nhóm userID là ID của cả nhóm.
  2. Viết script hook `user_prompt_submit` trả về `additionalContext`. Script đọc được chatID qua session key nhưng không thấy người gửi trong nhóm, và sandbox không có mạng, nên dữ liệu hồ sơ phải nhúng sẵn trong script.
  3. Làm một MCP server có tool `who_is(channel, sender_id)`. Agent thấy "User: tên (ID: …)" trong Current Chat Context nên có thể gọi tool, nhưng không có gì buộc nó phải gọi.
  4. Dùng `POST /v1/contacts/merge` để gộp ID các kênh, nhưng việc gộp chỉ ảnh hưởng credential.
- Muốn làm R5 đầy đủ (hồ sơ được tiêm vào prompt cho từng người gửi trong nhóm, và ủy quyền mang theo hồ sơ người yêu cầu) thì phải sửa `SystemPromptConfig`/`buildCurrentChatUserLine` (systemprompt.go:108-112, :589), `UserIdentityResolver` và `DelegateRequest`. Tức là phải fork, trong khi license NC vẫn còn nguyên.

### Gaps
- Chưa kiểm chứng bằng cách chạy rằng USER.md của agent kiểu predefined thực sự được tiêm vào prompt đúng như CLAUDE.md mô tả [?].
- Chưa kiểm handler kiểu `prompt`/`http` có đưa được context vào prompt theo đường khác hay không. Trong code chỉ thấy `script.go:211` đặt AdditionalContext.

## GoClaw — Dewee và AgentBrain (sản phẩm thương mại kế nhiệm)

### Takeaway
Docs Dewee (repo công khai) xác nhận Dewee là bản đóng, phát triển từ GoClaw. Giá: tự cài miễn phí nhưng cần license **$500/năm** để kết nối kênh chat; AaaS $500/năm; Dedicated $500 + $99 credit TOSE; On-Prem từ $5.000. Dewee **có Telegram**. Về AgentBrain chỉ có snippet tìm kiếm ("runs … on GoClaw v4"; danh sách kênh web, Slack, Teams, LINE, Zalo); giá $790–$3.600/năm chưa kiểm chứng được.

### Cited Findings
- [DOC] Bảng giá Dewee: "Self-install: Free to install; $500 per year licence to connect channels | AaaS $500 per year | Dedicated $500 per year licence + $99 TOSE credit deposit | On-Premises From $5K … includes the $500/year licence" (docs cập nhật 2026-09-25) — [deployment-options.md#L16](https://github.com/nextlevelbuilder/dewee-web-v2/blob/6fd9cb23/src/content/docs/en/get-started/deployment-options.md#L16); điều khoản: [terms.ts#L108-L114](https://github.com/nextlevelbuilder/dewee-web-v2/blob/6fd9cb23/src/content/legal/terms.ts#L108-L114)
- [DOC] Ưu đãi Early Access: "the first 50 licences get 50% off the first year, $250 instead of $500, until 23:59 on 15 October 2026, Vietnam time" — [self-install.md#L64-L67](https://github.com/nextlevelbuilder/dewee-web-v2/blob/6fd9cb23/src/content/docs/en/get-started/self-install.md#L64-L67)
- [DOC] Kênh của Dewee (cập nhật 2026-09-25): Telegram, Slack, Discord, WhatsApp, Feishu/Lark, Zalo OA, Zalo Bot, Zalo Personal, Facebook, Pancake, Bitrix24. Docs ghi: "Telegram has been validated in production with real users. Slack, Discord, WhatsApp, Feishu/Lark, Zalo OA and Zalo Personal are implemented but have not yet been tested end to end in production." Biến môi trường vẫn giữ tiền tố `GOCLAW_*` — [channels.md](https://github.com/nextlevelbuilder/dewee-web-v2/blob/6fd9cb23/src/content/docs/en/integrations/channels.md), [install-and-run.md#L17](https://github.com/nextlevelbuilder/dewee-web-v2/blob/6fd9cb23/src/content/docs/en/runtime/install-and-run.md#L17)
- [DOC] Chữ "GoClaw v4" không có trong docs Dewee (grep repo dewee-web-v2 không ra). Kết quả tìm kiếm tự tóm tắt Dewee là "GoClaw v4" nhưng không trích được câu gốc [?] — [dewee.sh (bị proxy chặn)](https://dewee.sh/)
- [DOC] Snippet tìm kiếm của agentbrain.sh: "AgentBrain centralizes business data, governs AI agents with RBAC, and runs secure workflows on GoClaw v4"; "deploy agents to web, Slack, Teams, LINE, Zalo, or your own API"; mô tả là runtime tự chứa, có thể triển khai trên cloud riêng hoặc môi trường air-gapped — [agentbrain.sh](https://agentbrain.sh/)
- [DOC] Org nextlevelbuilder có các repo `dewee-web-v2` (cập nhật 2026-09-25), `agentbrain-cli` (2026-08-07), `goclaw-docs` (2026-08-09) — [github.com/orgs/nextlevelbuilder](https://github.com/orgs/nextlevelbuilder/repositories?type=public)

### Inferences
- Nhận định cũ "Dewee từ $500/năm" là đúng. Cần nói thêm: phí $500 là để **kết nối kênh chat**; agent, provider và skill dùng không cần license.
- Nhận định "AgentBrain không có Telegram" chỉ khớp với một snippet liệt kê kênh. Chưa đủ để kết luận chắc.

### Gaps
- dewee.sh, agentbrain.sh và creativecommons.org đều bị proxy egress chặn. Giá AgentBrain ($790–$3.600/năm) và danh sách kênh đầy đủ của AgentBrain chưa kiểm chứng được [?].

## GoClaw — bảng đối chiếu nhận định cũ và chấm 12 tiêu chí

### Takeaway
Phần lớn nhận định cũ về cơ chế đúng. Các chỗ sai/đã thay đổi: approve/reject không nằm trong `teams_tasks_human.go`, danh sách kênh thiếu 3 kênh, các con số (kích thước, cadence, số commit main chậm hơn dev, beta tag) đã thay đổi, và cách mô tả issue #565. Về tiêu chí: GoClaw trượt R7 (license) và R3; R5 chỉ đạt 5a.

### Cited Findings
Bảng đối chiếu nhận định cũ (commit 16ba6a5a):

| Nhận định cũ | Kết luận | Bằng chứng |
|---|---|---|
| Go, ~2.411 file, 532k dòng | Đã thay đổi | [MÃ] Hiện 2.526 file .go / 557.562 dòng Go; 4.623 file tổng; ≈849k dòng text — [tree](https://github.com/nextlevelbuilder/goclaw/tree/16ba6a5a) |
| License CC BY-NC 4.0, cấm dùng thương mại | Đúng | [MÃ] [LICENSE#L1-L20](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/LICENSE); không có dual license; con đường thương mại là Dewee ([faq](https://github.com/nextlevelbuilder/dewee-web-v2/blob/6fd9cb23/src/content/docs/en/resources/faq.md#L15)) |
| Backend riêng: anthropic.go, openai.go, adapter_dashscope.go, aimlapi.go; claude_cli.go chỉ là adapter tùy chọn | Đúng | [MÃ] `anthropicAPIBase = "https://api.anthropic.com/v1"`, `(*AnthropicProvider).Chat` — [anthropic.go#L15](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/providers/anthropic.go#L15), [#L135](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/providers/anthropic.go#L135); ngoài ra có vertex.go, codex.go, acp/ |
| README ghi "auto/explicit/manual" nhưng code là spawn/delegate/team | Đúng | [MÃ] [orchestration_mode.go](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/orchestration_mode.go#L11-L23) vs [README#L67](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/README.md#L67) |
| Router teamworkclassify: embedding rồi LLM arbiter; ngưỡng 0.35, margin 0.08; khối ROUTING LOCK; retry với tool_choice=required | Đúng | [MÃ] [classifier.go#L33-L34](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/teamworkclassify/classifier.go#L33-L34); [team_work_directive.go#L42-L86](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/team_work_directive.go#L42-L86) |
| teams_tasks_human.go cho người approve/reject task in_review | Sai một phần | [MÃ] Approve/reject ở [teams_tasks.go#L174/L238](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/gateway/methods/teams_tasks.go#L174); teams_tasks_human.go (thêm 2026-09-09) = cancel/retry |
| Gộp danh tính: ResolveTenantUserID(channelType, senderID) | Đúng (cần nói thêm) | [MÃ] Có thật, nhưng chỉ đặt CredentialUserID — [loop_context.go#L74-L81](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/loop_context.go#L74-L81) |
| Không có bộ tách việc; không commit nào nói decompos/planner | Đúng | [MÃ/git] grep code và git log (xem phần trên) |
| Kênh: Telegram, Discord, Slack, Zalo OA, Zalo Personal, Feishu/Lark, WhatsApp | Sai (thiếu) | [MÃ] Thêm Facebook, Pancake, Bitrix24; "Zalo OA" thực chất dùng Zalo Bot API — [channel.go#L76-L85](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/channels/channel.go#L76-L85) |
| dev còn sống: commit cuối 12/9/2026, beta v3.15.0-beta.212 | Đã thay đổi | [MÃ/git] Commit cuối 2026-09-26 (16ba6a5a), tag v3.15.0-beta.219 (2026-09-26); beta.212 là tag ngày 2026-09-12 — [tags](https://github.com/nextlevelbuilder/goclaw/tags) |
| Cadence: tháng 3 = 827, tháng 8 = 39, 12 ngày đầu tháng 9 = 24 | Gần đúng / đã thay đổi | [MÃ/git] Tháng 3 = 826 (tính mọi commit) / 822 (bỏ merge); tháng 8 = 42 / 27; 1→12/9 = 25 / 19; cả tháng 9 tới 26/9 = 45 |
| main gần như đóng băng (7: 4, 8: 5, 9: 2), chậm dev 295 commit | Đúng / đã thay đổi | [MÃ/git] 4/5/2 đúng; nay chậm **315** commit |
| Stable cuối v3.14.0 ngày 15/6/2026 | Đúng | [MÃ/git] tag v3.14.0 2026-06-15 15:50 +07:00 |
| Dewee (runtime, từ $500/năm), AgentBrain ($790–3.600/năm) trên "GoClaw v4" | Đúng một phần / chưa kiểm | [DOC] Giá Dewee đúng ([deployment-options.md#L16](https://github.com/nextlevelbuilder/dewee-web-v2/blob/6fd9cb23/src/content/docs/en/get-started/deployment-options.md#L16)); giá AgentBrain chưa kiểm; "GoClaw v4" chỉ thấy trong snippet AgentBrain |
| AgentBrain có Zalo, LINE, Slack, Teams, không có Telegram | Chưa kiểm (khớp snippet) | [DOC] [agentbrain.sh](https://agentbrain.sh/) — chỉ có snippet |
| Issue #565 open, thừa nhận sender_id chỉ là số của nền tảng, agent không phân biệt được CTO với người lạ trong nhóm | Đúng một phần | [DOC] Open, có câu trích đó; nhưng đây là đề xuất của contributor bên ngoài (duhd-vnpay, 2026-03-30), không phải maintainer thừa nhận — [#565](https://github.com/nextlevelbuilder/goclaw/issues/565) |

Chấm 12 tiêu chí (GoClaw upstream dev 16ba6a5a):

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 Backend riêng | Đạt | [MÃ] provider HTTP gốc (anthropic.go, openai*.go, vertex.go, adapter_dashscope.go); Claude CLI là tùy chọn — [providers/](https://github.com/nextlevelbuilder/goclaw/tree/16ba6a5a/internal/providers) |
| R2 Nhiều agent/team | Đạt | [MÃ] team (lead/member/reviewer), team_tasks, delegate, agent links — [orchestration_mode.go](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/orchestration_mode.go) |
| R3 Tự làm rõ và tách việc từ yêu cầu mơ hồ | Không | [MÃ] Không có planner; arbiter "If uncertain, choose self", chỉ chọn team khi được yêu cầu rõ — [classifier.go#L283-L300](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/teamworkclassify/classifier.go#L283-L300) |
| R4 Review/duyệt | Một phần | [MÃ] `require_approval` tùy chọn (mặc định false); approve/reject trên dashboard; vai trò reviewer "not yet active" — [team_tasks_lifecycle.go#L187](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/tools/team_tasks_lifecycle.go#L187) |
| R5a Biết ai nhắn, kênh nào, nhóm nào | Đạt | [MÃ] Current Chat Context — [systemprompt.go#L564-L603](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/systemprompt.go#L564-L603) |
| R5b Một người trên nhiều kênh = 1 hồ sơ | Một phần | [MÃ] Gộp tay; chỉ dùng cho credential; session/memory/USER.md vẫn tách theo kênh — [loop_context.go#L74-L81](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/agent/loop_context.go#L74-L81) |
| R5c Hồ sơ có chức danh/phòng ban/quyền | Không | [MÃ] tenant_users chỉ có display_name, role RBAC dashboard, metadata; không đưa vào prompt; #565 chưa làm — [tenant_store.go#L43-L52](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/store/tenant_store.go#L43-L52) |
| R5d Delegate biết đang làm thay ai | Một phần | [MÃ] Truyền UserID/SenderID/Role (để phân quyền), không truyền tên/hồ sơ — [gateway_delegate.go#L18-L37](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/cmd/gateway_delegate.go#L18-L37) |
| R6 Nhiều kênh, mở rộng không sửa core | Một phần | [MÃ] 10 kênh, nhưng kênh mới phải RegisterFactory trong cmd/gateway.go — [gateway.go#L906-L930](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/cmd/gateway.go#L906-L930) |
| R7 Tự host + license cho phép kinh doanh | Không | [MÃ] CC BY-NC 4.0 — [LICENSE](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/LICENSE) |
| R8 Còn sống (release ≥ 2026-06-27) | Một phần | [MÃ/git] Beta tự động tới 2026-09-26; stable cuối 2026-06-15 (ngoài cửa sổ); founder ngừng commit từ tháng 6 |
| R9 Org chart kéo-thả điều khiển định tuyến | Không | [MÃ] ui/web chỉ dùng @dnd-kit cho file tree và các chuỗi fallback; không có org chart — [ui/web/package.json](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/ui/web/package.json) |
| R10 Multi-tenant | Đạt | [MÃ] tenants/tenant_users, migration 000027 (chỉ bản Standard; Lite thì không) — [000027_tenant_foundation.up.sql](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/migrations/000027_tenant_foundation.up.sql) |
| R11 Plugin không cần fork | Một phần | [MÃ] Hook (command/http/prompt/script), MCP, skill; không có plugin cho kênh — [hooks/types.go](https://github.com/nextlevelbuilder/goclaw/blob/16ba6a5a/internal/hooks/types.go#L69-L80) |
| R12 UI/docs/ảnh chụp | Một phần | [MÃ] README có 26 bản dịch (có tiếng Việt: `_readmes/README.vi.md`); UI có i18n vi; README chỉ có sơ đồ kiến trúc (`_statics/*.jpg`), không có ảnh chụp UI thật — [_statics](https://github.com/nextlevelbuilder/goclaw/tree/16ba6a5a/_statics) |

### Inferences
- Với người dùng muốn rời GoClaw: rào cản lớn nhất không phải kỹ thuật mà là R7 (license NC) và R8 (nhịp phát triển OSS đã chuyển sang Dewee). R5 cũng chỉ đạt 5a.

### Gaps
- Chưa chạy UI GoClaw để chụp ảnh thật; site docs.goclaw.sh chưa kiểm.

## Paperclip — đối chiếu, 12 tiêu chí, điểm mở rộng danh tính

### Takeaway
Paperclip vẫn **không có vòng lặp agent riêng gọi thẳng model API**. Mọi adapter tích hợp sẵn đều dựa vào harness bên ngoài. `paperclip_runner` mới có driver "claude_managed", gọi API Managed Agents của Anthropic bằng key của người dùng, nhưng vòng lặp agent vẫn chạy trên hạ tầng Anthropic. MIT, phát hành dày (v2026.916.1 ngày 2026-09-21). Mới có chat connector (thử nghiệm) cho Slack/Discord/Teams/Telegram/GitHub/AgentMail/iMessage, kèm liên kết danh tính đã xác minh vào user Paperclip. Không có Zalo. Có plugin SDK mạnh.

### Cited Findings
- [MÃ] `BUILTIN_ADAPTER_TYPES`: acpx_local, claude_local, codex_local, paperclip_runner, cursor_cloud, cursor, gemini_local, grok_local, hermes_gateway, hermes_local, kimi_local, openclaw_gateway, opencode_local, pi_local, process, http — [builtin-adapter-types.ts#L4-L21](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/adapters/builtin-adapter-types.ts#L4-L21)
- [MÃ] Native runner (thêm từ 2026-08-24, commit fdbc69172): các provider codex, opencode, `claude_managed` (backend `claude_managed_agents_api`), `aws_agentcore` (`aws_agentcore_harness_api`), acpx — [provider-profile.ts#L27-L52](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/services/native-runtime/provider-profile.ts#L27-L52). Driver Claude Managed dùng `ANTHROPIC_ORIGIN = "https://api.anthropic.com"`, beta `managed-agents-2026-04-01` — [claude_managed_provider.rs#L27-L29](https://github.com/paperclipai/paperclip/blob/640dee18/packages/paperclip-runner/runner/crates/runner-core/src/claude_managed_provider.rs#L27-L29). Onboarding không bao giờ tạo sẵn agent kiểu `paperclip_runner` ("Native runner rollout is an explicit post-onboarding configuration choice") — [onboarding-seed.ts#L34-L44](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/services/onboarding-seed.ts#L34-L44)
- [MÃ/git] Tag stable mới nhất: `v2026.916.1` (2026-09-21 12:19 -0700), `v2026.916.0` (2026-09-15 16:48 -0700). Canary `v2026.927.0-canary.2` (2026-09-26). Số commit không tính merge: 2026-06: 341, 07: 499, 08: 675, 09: 535. Trang releases ghi v2026.916.0 ngày 2026-09-16 và liệt kê "experimental chat connectors for Slack/Discord/Teams/Telegram" — [releases](https://github.com/paperclipai/paperclip/releases)
- [MÃ] License MIT ("Copyright (c) 2025 Paperclip AI"); `engines.node >= 24.11.0` — [LICENSE](https://github.com/paperclipai/paperclip/blob/640dee18/LICENSE), [package.json#L102-L104](https://github.com/paperclipai/paperclip/blob/640dee18/package.json#L102-L104)
- [MÃ] Org chart: `OrgChart.tsx` có zoom (0.2–2) và pan. Biến `dragging` chỉ dùng để kéo canvas, và code bỏ qua kéo khi bấm vào card ("Don't drag if clicking a card"). Không có kéo-thả để đổi cấp trên — [OrgChart.tsx#L25-L26](https://github.com/paperclipai/paperclip/blob/640dee18/ui/src/pages/OrgChart.tsx#L25-L26), [#L260-L309](https://github.com/paperclipai/paperclip/blob/640dee18/ui/src/pages/OrgChart.tsx#L260-L309)
- [MÃ] `AGENT_ROLES` = ceo, cto, cmo, cfo, security, engineer, designer, pm, qa, devops, researcher, general — [constants.ts#L46-L59](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L46-L59)
- [MÃ] Chế độ mặc định `local_trusted` không cần xác thực nhưng **bắt buộc bind vào loopback**: "local_trusted mode requires loopback host binding" và "only supports private exposure" — [index.ts#L654-L662](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/index.ts#L654-L662); host mặc định 127.0.0.1 ([config.ts#L196](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/config.ts#L196))
- [MÃ] Chat: `CHAT_PROVIDERS` = slack, github, discord, microsoft-teams, telegram, agentmail, imessage-photon ([chat-channels.ts#L2-L10](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/types/chat-channels.ts#L2-L10)), khóa bằng DB CHECK constraint ([chat_channels.ts#L259-L304](https://github.com/paperclipai/paperclip/blob/640dee18/packages/db/src/schema/chat_channels.ts#L259-L304)). Cả tính năng bị chặn sau cờ thử nghiệm `enableChatConnectors` ([routes/chat-channels.ts#L100-L101](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/routes/chat-channels.ts#L100-L101)); thêm vào ngày 2026-09-09 (#13100 "opt-in chat provider and data foundation").
- [MÃ] Danh tính chat: bảng `chat_external_principals` (provider, externalId, displayName, handle) và `chat_identity_links` (principal → `paperclip_user_id`, trạng thái pending/linked/revoked/expired, có `confirmation_token_hash`), tức liên kết có xác minh bằng token ([chat_channels.ts#L305-L358](https://github.com/paperclipai/paperclip/blob/640dee18/packages/db/src/schema/chat_channels.ts#L305-L358)). Người gửi chưa liên kết (guest) chạy dưới quyền `endpoint.sponsorUserId` (chat-channels.ts khoảng dòng 16041).
- [MÃ] Hồ sơ người: `auth` users chỉ có name/email/image. Membership role gồm owner/admin/operator/viewer/member ([constants.ts#L964-L977](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L964-L977)). Grant quyền theo `PERMISSION_KEYS` (ví dụ `tasks:assign`, `agents:create`, `joins:approve`) ([#L1003-L1024](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L1003-L1024)). Không có chức danh hay phòng ban cho người.
- [MÃ] `run_identity_contexts`: `responsibleUserId`, `parentContextId`, `cause` ("Immutable attribution records") — [run_identity_contexts.ts#L17-L30](https://github.com/paperclipai/paperclip/blob/640dee18/packages/db/src/schema/run_identity_contexts.ts#L17-L30). Dùng cho "use the responsible person's GitHub for shared agent operations" (#13005, 2026-09-07).
- [MÃ] Tách việc/duyệt: issues có `parentId` ([issues.ts#L39](https://github.com/paperclipai/paperclip/blob/640dee18/packages/db/src/schema/issues.ts#L39)). `APPROVAL_TYPES` = hire_agent, approve_ceo_strategy, budget_override_required, request_board_approval; trạng thái có `revision_requested` ([constants.ts#L689-L701](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L689-L701)). Stage thực thi của issue gồm `review`/`approval` ([#L521](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L521)). Hướng dẫn cho CEO: ghi `documents/plan` → `request_confirmation` → chuyển issue sang `in_review` "and wait for acceptance before delegating implementation subtasks"; mỗi lần bàn giao phải có "acceptance criteria" ([ceo/AGENTS.md#L36-L44](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/onboarding-assets/ceo/AGENTS.md#L36-L44)). Skill `paperclip-converting-plans-to-tasks` hướng dẫn tách task theo "qualifying boundary" ([SKILL.md](https://github.com/paperclipai/paperclip/blob/640dee18/skills/paperclip-converting-plans-to-tasks/SKILL.md))
- [MÃ] Plugin SDK: `definePlugin` ([define-plugin.ts#L563](https://github.com/paperclipai/paperclip/blob/640dee18/packages/plugins/sdk/src/define-plugin.ts#L563)); `ctx.events.on(name, fn)` với các sự kiện như `issue.created`, `issue.comment.created` ([types.ts#L553](https://github.com/paperclipai/paperclip/blob/640dee18/packages/plugins/sdk/src/types.ts#L553), [constants.ts#L1683-L1693](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L1683-L1693)); `PluginContext` có issues, approvals, agents, access, authorization ([types.ts#L2125-L2192](https://github.com/paperclipai/paperclip/blob/640dee18/packages/plugins/sdk/src/types.ts#L2125-L2192)); tạo session và gửi tin cho agent qua `sessions.create/sendMessage` ([types.ts#L1676-L1742](https://github.com/paperclipai/paperclip/blob/640dee18/packages/plugins/sdk/src/types.ts#L1676-L1742)); plugin khai báo được webhook (`PluginWebhookDeclaration`).
- [MÃ] Ảnh chụp và docs: thư mục `screenshots/` (ảnh PR), `doc/assets`, `docs/` (Mintlify `docs.json`, tiếng Anh), README nhúng video — [screenshots/](https://github.com/paperclipai/paperclip/tree/640dee18/screenshots), [docs/](https://github.com/paperclipai/paperclip/tree/640dee18/docs)

Bảng đối chiếu nhận định cũ:

| Nhận định cũ | Kết luận | Bằng chứng |
|---|---|---|
| Đã cài v2026.916.0 (Node ≥ 24.11, Postgres nhúng, localhost:3100) | Chưa kiểm phần [CHẠY]; phiên bản và Node đúng | [MÃ] Tag v2026.916.0 tồn tại; engines node >=24.11.0; Postgres nhúng (index.ts#L517-L622); cổng 3100 chưa kiểm — [package.json](https://github.com/paperclipai/paperclip/blob/640dee18/package.json#L102-L104) |
| Không có backend riêng, chỉ là lớp quản lý; chạy qua adapter claude_local…http | Đúng, nhưng đã thay đổi | [MÃ] Danh sách adapter có thêm acpx_local, paperclip_runner, cursor_cloud, grok_local, hermes_gateway, kimi_local, pi_local; runner có claude_managed/aws_agentcore (harness được host) — [builtin-adapter-types.ts](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/adapters/builtin-adapter-types.ts#L4-L21) |
| Org chart dạng cây, zoom được, KHÔNG kéo-thả; đổi cấp trên qua ô "Reports to" | Đúng | [MÃ] [OrgChart.tsx#L260-L309](https://github.com/paperclipai/paperclip/blob/640dee18/ui/src/pages/OrgChart.tsx#L260-L309); ô "Reports to" chưa kiểm trong UI [?] |
| Role có sẵn ceo…general, không có vai marketing | Đúng | [MÃ] [constants.ts#L46-L59](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L46-L59) |
| Chế độ local-trusted mở API không cần xác thực | Đúng (cần nói thêm) | [MÃ] Đúng là không xác thực, nhưng bị ép bind loopback và exposure private — [index.ts#L654-L662](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/index.ts#L654-L662) |

Chấm 12 tiêu chí (Paperclip 640dee18):

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 | Không | [MÃ] Mọi adapter đều dùng harness ngoài; claude_managed = vòng lặp agent chạy trên hạ tầng Anthropic — [provider-profile.ts](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/services/native-runtime/provider-profile.ts#L27-L52) |
| R2 | Đạt | [MÃ] Công ty → agent có role, reportsTo, org chart, giao issue — [constants.ts#L46](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L46) |
| R3 | Một phần (gần Đạt) | [MÃ] Cổng plan doc + request_confirmation + in_review, cây issue parentId/blockedBy, acceptance criteria. Nhưng đây là chỉ dẫn prompt cho CEO chạy trên CLI agent — [ceo/AGENTS.md#L36-L44](https://github.com/paperclipai/paperclip/blob/640dee18/server/src/onboarding-assets/ceo/AGENTS.md#L36-L44) |
| R4 | Đạt | [MÃ] Loại approval (có revision_requested), stage review/approval, budget override — [constants.ts#L689-L701](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L689-L701) |
| R5a | Chưa kiểm | [MÃ] Có lưu displayName/handle của principal; chưa kiểm cách chúng được đưa vào prompt của agent |
| R5b | Đạt (thử nghiệm) | [MÃ] chat_identity_links có xác minh token → 1 paperclip user; không có Zalo — [chat_channels.ts#L305](https://github.com/paperclipai/paperclip/blob/640dee18/packages/db/src/schema/chat_channels.ts#L305) |
| R5c | Một phần | [MÃ] Membership role + permission grants; không có chức danh/phòng ban — [constants.ts#L964-L1024](https://github.com/paperclipai/paperclip/blob/640dee18/packages/shared/src/constants.ts#L964-L1024) |
| R5d | Một phần | [MÃ] run_identity_contexts.responsibleUserId + parentContextId; chưa kiểm agent có thấy thông tin này không — [run_identity_contexts.ts](https://github.com/paperclipai/paperclip/blob/640dee18/packages/db/src/schema/run_identity_contexts.ts#L17-L30) |
| R6 | Một phần | [MÃ] 7 provider cứng + DB CHECK, cờ thử nghiệm, không Zalo; plugin có thể làm cầu nối qua webhook + sessions API (chưa thử) |
| R7 | Đạt | [MÃ] MIT |
| R8 | Đạt | [MÃ/git] v2026.916.1 ngày 2026-09-21; 535 commit trong tháng 9 |
| R9 | Một phần | [MÃ] Có org chart và reportsTo quyết định chuỗi giao việc (CEO giao cho cấp dưới trực tiếp), nhưng không kéo-thả |
| R10 | Đạt | [MÃ] Nhiều company trong một instance, dữ liệu scope theo company_id |
| R11 | Đạt | [MÃ] Plugin SDK chạy worker ngoài tiến trình, có capability, events, webhook, UI contribution; README: "Extend Paperclip without forking it" — [README.md#L261](https://github.com/paperclipai/paperclip/blob/640dee18/README.md#L261) |
| R12 | Đạt (chỉ tiếng Anh) | [MÃ] docs/ + screenshots/ + README có video |

### Inferences
- **Tự làm R5 mà không fork Paperclip:** viết plugin (`definePlugin`) đăng ký `ctx.events.on("issue.created" | "issue.comment.created")`. Khi issue sinh ra từ chat, plugin tra hồ sơ trong DB namespace riêng của plugin (chức danh, phòng ban, quyền), rồi dùng `ctx.issues` ghi comment hoặc document "Người yêu cầu: …" vào issue, và dùng `ctx.authorization`/`ctx.access` để kiểm quyền. Danh tính liên kết đa kênh đã có sẵn ở `chat_identity_links`. Riêng Zalo: plugin khai báo webhook và gọi `sessions.create/sendMessage` để bắc cầu (chưa thử).
- Rào cản lớn nhất vẫn là R1: người dùng muốn nền tảng tự gọi API bằng key của mình, còn Paperclip cần Claude Code/Codex/OpenCode hoặc Anthropic Managed Agents làm bộ thực thi.

### Gaps
- Chưa cài chạy lần này. Chưa xem agent có nhận tên người gửi hoặc responsibleUserId trong prompt/env hay không.
- Chưa kiểm số sao GitHub của Paperclip.

## SwarmClaw — đối chiếu, 12 tiêu chí, vì sao khó vận hành

### Takeaway
SwarmClaw không có release nào sau 2026-06-30 (v1.9.40), và **không có cả commit nào** sau ngày đó. Nhịp phát triển đã giảm từ 190 commit (tháng 3) xuống 9 (tháng 6) rồi 0. Org chart kéo-thả có thật và có ghi `parentId`, nhưng chỉ giới hạn đích giao việc khi agent cha có role `coordinator` **và** `delegationTargetMode = 'selected'`, trong khi mặc định là `'all'`. Template "Virtual Company" chỉ có trong README, không có trong code.

### Cited Findings
- [MÃ/git] Tag mới nhất `v1.9.40` (2026-06-30 21:58 +01:00); trước đó v1.9.39 (2026-06-11), v1.9.38 (2026-06-08). Commit cuối ed38ba53 ngày 2026-06-30. Số commit không tính merge theo tháng: 2026-02: 96, 03: 190, 04: 140, 05: 55, 06: 9, từ tháng 7 đến tháng 9: 0 — [tags](https://github.com/swarmclawai/swarmclaw/tags)
- [DOC] Trang repo: 681 sao, 138 fork, không archive, 10 issue mở, 10 PR mở — [github.com/swarmclawai/swarmclaw](https://github.com/swarmclawai/swarmclaw)
- [MÃ] MIT ("Copyright (c) 2026 SwarmClaw Contributors"); package.json `"license": "MIT"`, `"version": "1.9.40"` — [LICENSE](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/LICENSE)
- [MÃ] Org chart: `AgentOrgChart { parentId, teamLabel, teamColor, x, y }` ([types/agent.ts#L35-L41](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/types/agent.ts#L35-L41)); hook kéo-thả gọi `onDrop(agentId, newParentId, …)` ([use-org-chart-drag.ts#L18](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/components/org-chart/use-org-chart-drag.ts#L18)). Khi thả, `orgChart.parentId` được cập nhật; agent chỉ được thêm vào hoặc gỡ khỏi `delegationTargetAgentIds` nếu cha là `role === 'coordinator'` và `delegationTargetMode === 'selected'` ([lib/org-chart.ts#L155-L213](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/org-chart.ts#L155-L213)).
- [MÃ] Mặc định `delegationTargetMode: body.delegationTargetMode === 'selected' ? 'selected' : 'all'` ([agent-service.ts#L149](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/agents/agent-service.ts#L149)). `isAllowedDelegateTarget` trả về true với mọi đích khi mode khác 'selected' ([delegation-advisory.ts#L161-L167](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/agents/delegation-advisory.ts#L161-L167)). `parentId` còn quyết định phạm vi `ask_peer`, `team_context` và phần prompt về team (worker thấy peers + coordinator; agent mồ côi thì ở chế độ 'flat') ([team-resolution.ts#L1-L65](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/agents/team-resolution.ts#L1-L65)).
- [MÃ] "Virtual Company" chỉ xuất hiện ở README.md:334 như một "pattern" ("These aren't exclusive templates — they're patterns you combine", :444). Danh sách starter kit trong code là personal_assistant, research_copilot, builder_studio, content_studio, operator_swarm, openclaw_fleet, inbox_triage, data_analyst, blank_workspace; **không có** virtual company — [setup-defaults.ts#L565-L751](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/setup-defaults.ts#L565-L751), [README.md#L334-L352](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/README.md#L334-L352)
- [MÃ] README dài 1.160 dòng, phần lớn là changelog. README không giải thích coordinator/worker hay `delegationTargetMode`; grep README chỉ ra các câu mô tả org chart để "visualizing agent teams, delegation, and live activity". Thư mục `docs/` trong repo chỉ có 3 file kế hoạch release; docs thật nằm ở swarmclaw.ai/docs (bị proxy chặn) — [README.md](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/README.md), [docs/release](https://github.com/swarmclawai/swarmclaw/tree/ed38ba53/docs/release)
- [MÃ] Ảnh chụp thật: `doc/assets/screenshots/org-chart.png`, `doc/assets/screenshots/agent-chat.png` — [org-chart.png](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/doc/assets/screenshots/org-chart.png)
- [MÃ] R3: nếu classifier đánh dấu `isBroadGoal`, prompt được chèn `GOAL_DECOMPOSITION_BLOCK`: "Break it into 3-7 concrete, sequentially-executable subtasks before taking action … Execute the first substantive subtask immediately — do not stop after planning." Không có bước làm rõ yêu cầu hay acceptance criteria — [prompt-builder.ts#L268-L277](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/chat-execution/prompt-builder.ts#L268-L277), [#L452](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/chat-execution/prompt-builder.ts#L452)
- [MÃ] R4: stage của execution policy là `['review', 'approval', 'verification']`, quyết định gồm approved/changes_requested/reset (thêm 2026-05-06, commit 658099c) — [task-execution-policy.ts#L13](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/tasks/task-execution-policy.ts#L13), [types/task.ts#L36-L50](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/types/task.ts#L36-L50). ApprovalCategory có tool_access, human_loop, connector_sender, agent_create, budget_change… ([types/approval.ts#L3-L11](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/types/approval.ts#L3-L11)).
- [MÃ] R5: prompt từ connector: `The user "${msg.senderName}" (ID: ${msg.senderId}) is messaging from channel "…"`; trong nhóm, lịch sử được đánh tiền tố `[SenderName]` ([connector-inbound.ts#L1073-L1075](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/connectors/connector-inbound.ts#L1073-L1075)). "Chủ" được xác định bằng một `ownerSenderId` duy nhất cho mỗi connector ([access.ts#L82-L94](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/connectors/access.ts#L82-L94)). `contact-boundaries.ts` nhận diện người gửi bằng heuristic khớp nhãn trong memory với tên/ID. Không có mô hình danh tính xuyên kênh, không có role hay chức danh.
- [MÃ] R1: provider gốc anthropic.ts, openai.ts, ollama.ts, openai-compatible-endpoint.ts…, còn các CLI provider (claude-cli, codex-cli, gemini-cli…) là tùy chọn — [src/lib/providers](https://github.com/swarmclawai/swarmclaw/tree/ed38ba53/src/lib/providers)
- [MÃ] R6/R11: connector có sẵn gồm telegram, discord, slack, whatsapp, teams, googlechat, signal, matrix, bluebubbles, email, openclaw, swarmdock ([connectors/](https://github.com/swarmclawai/swarmclaw/tree/ed38ba53/src/lib/server/connectors)). Extension có thể khai báo `connectors` (`ExtensionConnectorDefinition { id, name, sendMessage, startListener(onMessage) }`) ([types/extension.ts#L395-L407](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/types/extension.ts#L395-L407)), được nạp trong `connector-lifecycle.ts:82-83`; manifest extension có hooks, tools, ui, providers, connectors… ([extensions.ts#L524](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/server/extensions.ts#L524)).
- [MÃ] R10: grep "tenant" trong `src/lib/server` không ra kết quả; mô hình là một instance với access key (storage-auth.ts).

Bảng đối chiếu nhận định cũ:

| Nhận định cũ | Kết luận | Bằng chứng |
|---|---|---|
| MIT | Đúng | [MÃ] [LICENSE](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/LICENSE) |
| 654 sao | Đã thay đổi | [DOC] Nay 681 sao — [repo](https://github.com/swarmclawai/swarmclaw) |
| Org chart kéo-thả | Đúng | [MÃ] [use-org-chart-drag.ts](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/components/org-chart/use-org-chart-drag.ts) |
| Template "Virtual Company" | Sai (chỉ có trong README) | [MÃ] Không có starter kit nào như vậy — [setup-defaults.ts#L565-L751](https://github.com/swarmclawai/swarmclaw/blob/ed38ba53/src/lib/setup-defaults.ts#L565-L751) |
| Release cuối 30/6/2026 | Đúng | [MÃ/git] v1.9.40 2026-06-30; không có commit nào sau đó |

Chấm 12 tiêu chí (SwarmClaw ed38ba53):

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 | Đạt | [MÃ] provider HTTP gốc |
| R2 | Đạt | [MÃ] coordinator/worker, team theo org chart, delegation, chatroom |
| R3 | Một phần | [MÃ] Prompt tách goal thành 3–7 subtask rồi làm ngay; không làm rõ yêu cầu |
| R4 | Một phần→Đạt | [MÃ] Stage review/approval/verification với changes_requested, approval human_loop/budget; phải bật cho từng task |
| R5a | Đạt | [MÃ] connector-inbound.ts#L1075 |
| R5b | Không | [MÃ] Không có liên kết danh tính xuyên kênh |
| R5c | Không | [MÃ] Chỉ phân biệt chủ và không phải chủ (ownerSenderId) |
| R5d | Chưa kiểm | — |
| R6 | Đạt (không có Zalo) | [MÃ] Hơn 12 connector + connector qua extension |
| R7 | Đạt | [MÃ] MIT |
| R8 | Một phần (sắp trượt) | [MÃ/git] v1.9.40 ngày 2026-06-30 chỉ vừa trong cửa sổ (mốc 2026-06-27); 0 commit trong 3 tháng; từ 2026-09-30 sẽ trượt |
| R9 | Một phần | [MÃ] Kéo-thả có ghi parentId; chỉ giới hạn delegate khi coordinator + 'selected' (mặc định 'all') |
| R10 | Không | [MÃ] Không có khái niệm tenant |
| R11 | Đạt | [MÃ] Extension system |
| R12 | Một phần | [MÃ] 2 ảnh chụp thật; README dạng changelog; docs ngoài repo; Virtual Company chỉ là README |

### Inferences
- **Vì sao người dùng khó hiểu cách vận hành:**
  1. Kéo-thả trên org chart trông như "phân công", nhưng với cấu hình mặc định (`delegationTargetMode='all'`) nó không giới hạn ai được giao việc cho ai. Muốn chart có tác dụng phải đổi role agent cha thành `coordinator` và chuyển mode sang `selected`, mà README không nói điều này.
  2. README quảng cáo "Virtual Company" (CEO/CTO/CFO/CMO/COO) nhưng trình hướng dẫn cài đặt không có kit đó, người dùng phải tự dựng từ đầu.
  3. Docs trong repo gần như trống; README 1.160 dòng chủ yếu là changelog.
  4. Dự án đứng im từ 2026-06-30 nên issue/PR không được xử lý.
- **Tự làm R5 mà không fork:** viết extension có hook và tool, hoặc một connector qua `ExtensionConnectorDefinition.startListener(onMessage)` (types/extension.ts:395-407). Connector này tự tra hồ sơ (chức danh, phòng ban) và gắn vào `InboundMessage.senderName`/nội dung trước khi đẩy vào. Làm cách này thì mất các connector có sẵn (phải viết lại connector cho kênh cần danh tính).

### Gaps
- Chưa đọc được docs swarmclaw.ai/docs (bị proxy chặn). Chưa kiểm 5d.

## Synkora — đối chiếu, 12 tiêu chí, điểm mở rộng danh tính

### Takeaway
Synkora còn sống (tag v1.17.29 ngày 2026-09-26; 65 commit trong tháng 9), dùng MIT, là nền tảng đầy đủ: tự gọi LLM qua litellm/openai/anthropic, multi-tenant, có HITL phê duyệt tool qua Slack/WhatsApp/chat. Nói "không có phân cấp" là sai một phần: Synkora có quan hệ agent cha→con (`agent_sub_agents`) và trang "Agent Hierarchy" dạng cây tĩnh, nhưng không có org chart hay phòng ban. Danh tính người chat chỉ ở mức tên hiển thị theo từng kênh. Không có Zalo.

### Cited Findings
- [MÃ/git] Tag mới nhất `v1.17.29` (2026-09-26 14:33 +08:00); v1.17.24–28 trong khoảng 2026-09-24 đến 2026-09-25. Commit không tính merge theo tháng: 2026-06: 58, 07: 20, 08: 40, 09: 65 — [tags](https://github.com/getsynkora/synkora-ai/tags)
- [DOC] 38 sao, 6 fork, 4 issue mở, 0 PR mở, không archive — [github.com/getsynkora/synkora-ai](https://github.com/getsynkora/synkora-ai)
- [MÃ] MIT ("Copyright (c) 2025 Synkora Contributors") — [LICENSE](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/LICENSE)
- [MÃ] R1: `litellm>=1.83.7`, `openai>=2.8.0`, `anthropic>=0.42.0` — [api/pyproject.toml#L56-L58](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/pyproject.toml#L56-L58)
- [MÃ] Phân cấp: `AgentSubAgent` là "Junction table for parent-child agent relationships" (`parent_agent_id`, `sub_agent_id`, `execution_order`) ([agent_sub_agent.py#L14-L26](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/models/agent_sub_agent.py#L14-L26)). UI có trang "Agent Hierarchy — Visual overview of the parent-child agent structure" ([sub-agents/page.tsx#L480-L490](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/web/app/(dashboard)/agents/%5BagentName%5D/sub-agents/page.tsx#L480-L490)). `workflow_type` gồm sequential, loop, parallel, custom; có thêm debate_executor ([agent.py#L196-L200](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/models/agent.py#L196-L200)).
- [MÃ] Role mẫu (`AgentRoleType`): project_manager, product_owner, qa_engineer, code_reviewer, business_analyst, scrum_master, tech_lead, custom, tức toàn vai phần mềm, không có vai marketing — [agent_role.py#L16-L27](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/models/agent_role.py#L16-L27)
- [MÃ] HITL: `AgentApprovalRequest` (tool_name, tool_args, notification_channel slack|whatsapp|whatsapp_web|chat, expires_at) ([agent_approval.py#L33-L56](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/models/agent_approval.py#L33-L56)). Cổng kiểm được gọi trước khi chạy các action tool ([adk_tools.py#L1871-L1874](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/services/agents/adk_tools.py#L1871-L1874)), cấu hình qua `require_approval_tools` ([platform_tools.py#L1999](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/services/agents/internal_tools/platform_tools.py#L1999)). Phản hồi được phân loại approve/reject/unclear; có `_fire_feedback_run` để gửi ý kiến và bắt agent làm lại ([human_approval_service.py#L161](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/services/human_approval_service.py#L161), [#L421](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/services/human_approval_service.py#L421)).
- [MÃ] Kênh: có model và service cho Slack, Teams, Telegram, WhatsApp (webhook Cloud + WhatsApp Web qua device link), widget, phone/voice, email ([api/src/models](https://github.com/getsynkora/synkora-ai/tree/2acc1a58/api/src/models), [services/](https://github.com/getsynkora/synkora-ai/tree/2acc1a58/api/src/services)). grep "zalo" không ra; Discord chỉ xuất hiện trong enum output config.
- [MÃ] Danh tính: Telegram đưa vào agent dòng `[Telegram Context: {chat_type} chat '{chat_display}', User: {user_display} (@{user_name})]` ([telegram_polling_service.py#L258](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/services/telegram/telegram_polling_service.py#L258), [telegram_webhook_service.py#L248](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/services/telegram/telegram_webhook_service.py#L248)). Slack lấy `real_name` qua users_info. `HumanContact` (name, email, slack_user_id, whatsapp_number, preferred_channel) dùng cho **escalation chiều ra**, tức agent liên hệ người, không dùng để nhận diện người nhắn tới ([human_contact.py#L33-L63](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/models/human_contact.py#L33-L63)). Role và permission (`role.py`, `permission.py`) áp cho tài khoản nền tảng, không cho người chat.
- [MÃ] R3: grep `decompos|planner|subtask|acceptance criteria` trong `api/src/services` không có planner (chỉ có `script.decompose()` của BeautifulSoup và vài connector) — [services/agents](https://github.com/getsynkora/synkora-ai/tree/2acc1a58/api/src/services/agents)
- [MÃ] R11: không có hệ plugin (grep "plugin" trong services chỉ ra parser webhook và chart). Mở rộng được qua `CustomTool`, `AgentMCPServer`, `AgentContextFile`, webhook — [custom_tool.py#L26](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/models/custom_tool.py#L26), [agent_mcp_server.py#L16](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/models/agent_mcp_server.py#L16)
- [MÃ] R10: `TenantMixin` trên các model; có tenant.py, okta_tenant.py, saml_config.py, scim_* — [api/src/models](https://github.com/getsynkora/synkora-ai/tree/2acc1a58/api/src/models)
- [MÃ] R12: docs Docusaurus (`docs/`, tiếng Anh); 9 ảnh chụp thật trong `web/public/images/screenshot-*.png` được nhúng ở README — [web/public/images](https://github.com/getsynkora/synkora-ai/tree/2acc1a58/web/public/images)

Bảng đối chiếu nhận định cũ:

| Nhận định cũ | Kết luận | Bằng chứng |
|---|---|---|
| MIT | Đúng | [MÃ] [LICENSE](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/LICENSE) |
| 34 sao | Đã thay đổi | [DOC] Nay 38 |
| Nền tảng đầy đủ, nhiều kênh, có human approval | Đúng | [MÃ] Xem các finding ở trên |
| Không có phân cấp hay org chart | Sai một phần | [MÃ] Có phân cấp cha→con và trang cây "Agent Hierarchy"; không có org chart công ty hay phòng ban — [agent_sub_agent.py](https://github.com/getsynkora/synkora-ai/blob/2acc1a58/api/src/models/agent_sub_agent.py#L14-L26) |

Chấm 12 tiêu chí (Synkora 2acc1a58):

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 | Đạt | [MÃ] litellm/openai/anthropic |
| R2 | Một phần | [MÃ] Sub-agent, project, workflow, role mẫu vai phần mềm; không có team/phòng ban |
| R3 | Không | [MÃ] Không có planner hay bước làm rõ |
| R4 | Một phần | [MÃ] HITL cho tool + phản hồi yêu cầu làm lại; không có stage review giữa các agent |
| R5a | Đạt | [MÃ] Dòng Telegram Context; real_name từ Slack |
| R5b | Không | [MÃ] Không liên kết danh tính người nhắn qua các kênh |
| R5c | Không | [MÃ] Role/permission chỉ cho tài khoản nền tảng |
| R5d | Chưa kiểm | — |
| R6 | Một phần | [MÃ] Slack/Teams/Telegram/WhatsApp/widget/API/voice/email; không Zalo; thêm kênh phải sửa core |
| R7 | Đạt | [MÃ] MIT |
| R8 | Đạt | [MÃ/git] v1.17.29 ngày 2026-09-26 |
| R9 | Không | [MÃ] Chỉ có cây cha-con tĩnh cho từng agent |
| R10 | Đạt | [MÃ] TenantMixin, SAML/SCIM |
| R11 | Một phần | [MÃ] Custom tool/MCP/webhook; không có plugin system |
| R12 | Đạt (tiếng Anh) | [MÃ] Docusaurus + 9 ảnh chụp |

### Inferences
- **Tự làm R5 mà không fork Synkora:** gắn cho agent một MCP server (`AgentMCPServer`) hoặc `CustomTool` HTTP kiểu `lookup_person(channel, username)`. Agent nhìn thấy `@username` trong dòng "[Telegram Context: …]" nên có thể gọi tool đó. Kết hợp với `AgentContextFile` hoặc system prompt để buộc agent tra hồ sơ trước khi làm. Còn muốn tiêm hồ sơ một cách chắc chắn thì phải sửa chuỗi ở telegram_polling_service.py:258 / telegram_webhook_service.py:248 và Slack handler, tức là fork.
- Synkora mạnh ở R1/R7/R8/R10 nhưng thiếu R3, R5b-c, R9 và Zalo, nên hợp làm "nền chat + HITL" hơn là "phòng ban có tổ chức".

### Gaps
- Chưa kiểm sub-agent có nhận thông tin người yêu cầu gốc không (5d) và chưa kiểm GitHub Releases (mới kiểm tag git).
