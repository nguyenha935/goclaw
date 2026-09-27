# Markus và Clawith — đánh giá 12 tiêu chí từ mã nguồn (kiểm chứng ngày 2026-09-27)

Quy ước nhãn: **[MÃ]** đọc mã nguồn; **[CHẠY]** đã cài và chạy thử; **[DOC]** chỉ từ tài liệu/trang web; **[?]** chưa kiểm chứng.
Ngày hôm nay xác nhận bằng `date`: 2026-09-27 (UTC).

Commit đã đọc:
- **Markus**: `main` @ `bc6f1200a096e0dac005e8a678b66178e1f084ae` (commit 2026-09-25T20:04:41+08:00). Link mã bên dưới dùng tiền tố `https://github.com/markus-global/markus/blob/bc6f1200a096/…`.
- **Clawith**: `main` @ `45fc701c366c69f89dff26d91d6a4a9cbc38e6f8` (commit 2026-08-25T20:05:07+08:00; nhánh `develop` mới hơn một chút, commit cuối 2026-08-27). Link mã dùng tiền tố `https://github.com/dataelement/Clawith/blob/45fc701c366c/…`.
- Ảnh chụp màn hình tự chụp (Playwright + Chromium) nằm trong `screenshots/` cạnh file này, tên bắt đầu bằng `markus_` hoặc `clawith_`.

---

## Markus — thông tin chung: repo, license, sao, kích thước, bản phát hành, nhịp commit

### Takeaway
Markus (github.com/markus-global/markus) là monorepo TypeScript, còn rất non: commit đầu ngày 2026-02-24, đang ở v0.10.1 (2026-09-23), 195 sao. Dự án đổi license từ AGPL-3.0 sang Apache-2.0 kèm một license thương mại tùy chọn vào ngày 2026-08-16. Gần như một người viết toàn bộ mã.

### Cited Findings
- Repo: https://github.com/markus-global/markus. Mô tả: "The all-in-one AI workforce platform, to build AI agent teams. You are the boss." Khi xem ngày 2026-09-27 repo có **195 sao, 14 fork, 6 issue mở, 1 PR mở** [DOC] — [GitHub repo page](https://github.com/markus-global/markus)
- License [MÃ]:
  - `LICENSE` là Apache-2.0 ("Copyright (c) 2026 Markus Contributors"). Mọi `packages/*/package.json` đều khai `"license": "Apache-2.0"`, gồm a2a, chrome-extension, cli, comms, core, desktop, gui, org-manager, remote, shared, storage, web-ui — [LICENSE](https://github.com/markus-global/markus/blob/bc6f1200a096/LICENSE)
  - `LICENSE-COMMERCIAL.md` mô tả mô hình license kép. Bản Apache-2.0 "free to use… including commercial use… SaaS". License thương mại chỉ dành cho SLA/hỗ trợ, bồi hoàn (indemnification), OEM/nhúng không cần ghi công, white-label. Trong repo không có thư mục EE/commercial riêng — [LICENSE-COMMERCIAL.md](https://github.com/markus-global/markus/blob/bc6f1200a096/LICENSE-COMMERCIAL.md)
- Lịch sử license [MÃ]: commit `965e8d94` ngày 2026-08-16 có thông điệp "license: AGPL-3.0 切换为 Apache-2.0 + 商业扩展双授权". Commit trước đó `0bcfad44` (2026-03-15) có LICENSE là GNU AGPL. Các bài blog cũ trên Medium/dev.to vẫn ghi "AGPL-3.0", tức đã lỗi thời — [search: dev.to/Medium mô tả AGPL](https://dev.to/jsyqrt/build-your-first-ai-team-with-markus-in-5-minutes-3oj1)
- Có cổng tính năng "Enterprise" ngay trong mã Apache [MÃ]:
  - `shared/src/types/license.ts` định nghĩa `PlanTier = 'free'|'basic'|'plus'|'pro'|'max'|'team'|'enterprise'` và `ENTERPRISE_FEATURES = ['multi_user','unlimited_teams','unlimited_tools','sso','audit_enhanced','multi_instance']` — [license.ts](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/shared/src/types/license.ts#L1-L27)
  - Chỉ thấy một chỗ thực thi: đăng nhập Hub cho người dùng Hub thứ hai trả về 403 `MULTI_USER_REQUIRED` ("Multi-user requires Enterprise license") — [api-server.ts#L3324-L3343](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L3324-L3343)
  - Endpoint tạo user cục bộ `POST /api/users` **không** kiểm license — [api-server.ts#L6479-L6554](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L6479-L6554)
- Phát hành [MÃ]:
  - Tag mới nhất là `v0.10.1` (2026-09-23 11:57 +0800), trước đó `v0.10.0` (2026-09-20), `v0.9.9` (2026-08-31), `v0.9.8` (2026-08-21), `v0.9.7` (2026-08-20). Tổng cộng 155 tag, gồm cả rc và tag "superseded/…"
  - Trang Releases hiển thị v0.10.1 là "Latest" với nhãn "23 Sep" (GitHub ẩn năm; năm 2026 suy ra từ ngày tag trong git) — [Releases](https://github.com/markus-global/markus/releases)
  - Có bản npm: `npm view @markus-global/cli` trả về version 0.10.1, time.modified 2026-09-23 [CHẠY]
- Nhịp commit [MÃ, `git log`]. Nhánh main: 2026-06: 183 · 2026-07: 47 · 2026-08: 243 · 2026-09: 201. Mọi nhánh cộng lại: 244 / 109 / 251 / 297. Tổng 1.504 commit trên main, commit đầu 2026-02-24. — [commits](https://github.com/markus-global/markus/commits/main)
- Người đóng góp từ 2026-06-01, theo `git shortlog --all` [MÃ]: "Jason Carter <jsyqrt@gmail.com>" 757 + "Jason" 105 commit. Các tác giả còn lại là agent tự động ("首席科学家 <agent@markus.local>" 18+14, "CTO" 2…) và 1 người ngoài (3 commit). Bus factor ≈ 1.
- Kích thước [MÃ]: cây làm việc ~29 MB. Khoảng 300 nghìn dòng TS/TSX tính cả test, ~210 nghìn dòng không tính test. Storage **chỉ có SQLite**: `packages/storage/src/` chỉ có `sqlite-storage.ts`, không có mã PostgreSQL, dù README ghi "SQLite by default (PostgreSQL supported)" — [README.md#L53](https://github.com/markus-global/markus/blob/bc6f1200a096/README.md) — **README khác mã**.
- Issue: 6 issue mở. Riêng #286 "comms: add a Discord adapter following the Slack/Telegram/WhatsApp pattern" (mở 2026-08-16 bởi chính maintainer). Không có issue nào về danh tính/vai trò/multi-tenant [DOC] — [Issues](https://github.com/markus-global/markus/issues?q=is%3Aissue)

### Inferences
- Về pháp lý, bản mới nhất dùng được cho kinh doanh nội bộ (Apache-2.0). Cổng `multi_user` chỉ chặn đăng nhập qua Markus Hub. Vì là Apache-2.0 nên có quyền sửa bỏ cổng này, nhưng như vậy nghĩa là phải fork.
- Rủi ro bảo trì cao: v0.x, 7 tháng tuổi, một maintainer chính.

### Gaps
- Không truy cập được markus.global (proxy chặn), nên chưa đối chiếu trang giá/Enterprise và docs site.
- Chưa kiểm chứng telemetry gửi đi đâu. Mã chỉ cho thấy `telemetry-service.ts` bật mặc định (`return { enabled: true }` khi chưa có file cấu hình).

---

## Markus — CÂU HỎI QUAN TRỌNG NHẤT: người gửi tin Telegram có được ánh xạ sang bảng `users` không?

### Takeaway
**Không.** Adapter Telegram là **mã chết**: runtime không đăng ký nó, không có polling, webhook trỏ cứng vào `http://localhost`, và router không bao giờ gắn agent vào kênh. Kể cả nếu được đăng ký, handler chỉ truyền `message.senderId` thô (Telegram user id) và **không** truyền `senderInfo`, nên không tra bảng `users` và không chèn danh tính vào prompt. Kênh ngoài duy nhất chạy thật là Feishu, và Feishu gán **mọi** người gửi vào phiên của **owner** với nhãn `Feishu:<tên>`, role `'user'`. Không có liên kết danh tính xuyên kênh.

### Cited Findings
- Interface `CommAdapter { platform; connect; disconnect; sendMessage; sendReply; onMessage; isConnected }` [MÃ] — [adapter.ts#L12-L20](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/comms/src/adapter.ts#L12-L20)
- Telegram adapter:
  - Chỉ nhận update qua webhook. `setupWebhook()` tạo `webhookUrl = http://localhost:${webhookPort}${webhookPath}` (comment "assuming localhost for development") rồi gọi `setWebhook` [MÃ] — [telegram/adapter.ts#L202-L258](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/comms/src/telegram/adapter.ts#L202-L258)
  - Telegram yêu cầu URL HTTPS công khai cho webhook. Đây là kiến thức nền, chưa chạy thử với Telegram [?].
  - `processUpdate` bỏ qua tin không phải text và đặt `senderId = message.from.id`, `senderName = username|first_name`, `channelId = chat.id` [MÃ] — [telegram/adapter.ts#L260-L292](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/comms/src/telegram/adapter.ts#L260-L292)
- "Polling" chỉ là một trường cấu hình: `pollingEnabled?: boolean` có trong `TelegramClientConfig`, nhưng `client.ts` không có `getUpdates` hay vòng lặp poll nào (grep chỉ ra đúng dòng khai báo) [MÃ] — [telegram/client.ts#L9](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/comms/src/telegram/client.ts#L9)
- Runtime chỉ đăng ký WebUI và Feishu [MÃ]:
  - `start.ts` gọi `messageRouter.registerAdapter(webUIAdapter)`, và chỉ khi có FEISHU_APP_ID/SECRET mới đăng ký `FeishuAdapter` — [start.ts#L1963-L2025](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/cli/src/commands/start.ts#L1963-L2025)
  - `TelegramAdapter`, `SlackAdapter`, `WhatsAppAdapter` chỉ xuất hiện trong `packages/comms/src/index.ts` và trong test.
- Chạy thử v0.10.1 [CHẠY]:
  - Log khởi động in "Gateway … webhook adapter: WebUI only".
  - Trang Settings → Integrations chỉ có một mục "飞书 (Feishu / Lark)" — [ảnh](screenshots/markus_settings_integrations.png)
- Router bỏ tin nếu không có agent [MÃ]:
  - `routeIncomingMessage` lấy `agentId = message.agentId || agentChannelMap.get("platform:channelId")`, không có thì log "No agent bound to channel, skipping message".
  - `bindAgentToChannel` không được gọi ở đâu ngoài chính định nghĩa của nó — [router.ts#L18-L75](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/comms/src/router.ts#L18-L75)
- Handler router bỏ mất danh tính [MÃ]: `messageRouter.setAgentHandler(async (agentId, message) => agent.sendMessage(message.content.text ?? '', message.senderId))`, không có đối số `senderInfo`. Audit ghi cứng `orgId: 'default'` — [start.ts#L1967-L1995](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/cli/src/commands/start.ts#L1967-L1995)
- Chỉ đường Web UI mới có danh tính [MÃ]:
  - `Agent.sendMessage(userMessage, senderId?, senderInfo?: {name, role, isFirstConversation?, locale?, timezone?}, options?)` — [agent.ts#L1136-L1140](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/agent.ts#L1136-L1140)
  - Prompt chỉ có khối "## Current Conversation — You are now talking to **{name}** ({role})" khi `senderIdentity` được truyền. Có câu riêng cho `owner`, `admin`, `guest` — [context-engine.ts#L1139-L1162](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/context-engine.ts#L1139-L1162)
  - Web chat lấy `senderId = authUser.userId` rồi `orgService.resolveHumanIdentity(senderId)` — [api-server.ts#L4633-L4660](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L4633-L4660)
  - `resolveHumanIdentity` chỉ tra map `humans` theo **user id nội bộ** và trả về `{id, name, role, locale, timezone}`, không có team/chức danh — [org-service.ts#L157-L171](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/org-service.ts#L157-L171)
- Feishu, kênh ngoài duy nhất chạy thật, đi đường khác [MÃ]:
  - `FeishuNotifier` (Lark SDK, `im.message.receive_v1`) phát `feishu:message_received` → `handleFeishuUserMessage` — [feishu-notifier.ts#L476](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/feishu-notifier.ts#L476), [api-server.ts#L2519-L2525](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L2519-L2525)
  - Hàm này luôn chuyển tới Secretary của org, lấy `ownerUserId = ensureAdminUser('default')`, lưu tin vào **main session của owner**, rồi gọi `secretary.sendMessageStream(text, …, ownerUserId, { name: 'Feishu:<senderName>', role: 'user' })` — [api-server.ts#L2621-L2835](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L2747-L2835)
- Schema không có chỗ cho ID ngoài [MÃ]:
  - Bảng `users(id, org_id, name, email UNIQUE, role DEFAULT 'member', team_id, password_hash, invite_token, invite_expires_at, preferences, created_at, last_login_at)` không có cột ID Telegram/Zalo/Feishu và không có bảng liên kết danh tính — [sqlite-storage.ts#L389-L402](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/storage/src/sqlite-storage.ts#L389-L402)
  - `HumanRole = 'owner'|'admin'|'member'|'guest'` — [org.ts#L3-L16](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/shared/src/types/org.ts#L3-L16)
- Phản hồi A2A mang `senderRole: 'agent'`, tức danh tính người khởi xướng bị thay bằng agent [MÃ] — [api-server.ts#L2200](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L2200)

### Inferences
- Với phòng Marketing chạy qua Telegram/Zalo, Markus hiện **không đáp ứng R5**. Mọi tin từ kênh ngoài sẽ hoặc bị bỏ (Telegram), hoặc bị trộn vào phiên của chủ (Feishu). Trộn như vậy còn là **rủi ro rò rỉ**: nhân viên nhắn qua Feishu sẽ thấy/ghi chung lịch sử với owner.
- Nhận định cũ "Telegram adapter truly bidirectional" là **sai**.

### Gaps
- Chưa chạy thử với bot Telegram thật. Kết luận "không hoạt động" dựa trên mã và log khởi động.

---

## Markus — tự phân rã yêu cầu mơ hồ, review bắt buộc, trust level, cổng duyệt của người

### Takeaway
Trong mã, Markus **có** khung ràng buộc thật: task phải gắn requirement đã duyệt, bắt buộc có reviewer, luồng `in_progress → review → completed`, trả lại để làm lại, subtask chưa xong thì không nộp được, và task do agent tạo cần người duyệt. Tuy vậy, việc **phân rã** do prompt LLM điều khiển, và vai trò mẫu **cố ý chờ người xác nhận** chứ không tự chạy. **Trust level (probation → senior) là mã chết**: được khởi tạo nhưng không nối vào đâu.

### Cited Findings
- Máy trạng thái task [MÃ]: `in_progress` chỉ đi tới `review|blocked|failed|cancelled`, và `review` đi tới `completed|in_progress|cancelled`. `updateTaskStatus()` từ chối chuyển trạng thái không có trong bảng — [task.ts#L16-L29](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/shared/src/types/task.ts#L16-L29)
  - Ngoại lệ: `pending` được phép nhảy thẳng tới `completed`.
- Reviewer bắt buộc [MÃ]: `if (!request.reviewerId) throw 'Task creation failed: reviewerId is required'`; reviewer có thể là agent hoặc `human` — [task-service.ts#L2349-L2362](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L2349-L2362)
- Task cấp trên cùng phải gắn requirement đã duyệt [MÃ]: "Task creation blocked: top-level tasks must reference an approved requirement… Use requirement_propose…" — [task-service.ts#L2376-L2377](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L2376-L2377)
- Cổng duyệt của người [MÃ]:
  - `determineApprovalTier`: nếu chưa cấu hình governance policy thì task do agent (worker/manager) tạo → `'human'`; task do người tạo hoặc từ plan/workflow đã duyệt → `'auto'` — [task-service.ts#L4029-L4045](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L4029-L4045)
  - Task ở trạng thái `pending` do agent tạo sẽ gọi `hitlService.requestApprovalAndWait(...)`; duyệt thì `approveTask`, từ chối hoặc lỗi thì `rejectTask` — [task-service.ts#L2546-L2572](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L2546-L2572)
  - Task do người tạo luôn bắt đầu ở `pending` và chỉ chạy khi người bấm "start" — [task-service.ts#L2428-L2441](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L2428-L2441)
- Làm lại và nộp review [MÃ]:
  - Prompt thêm "### 🔴 REVISION REQUIRED — Your previous work was REJECTED by the reviewer" khi bị trả lại.
  - Nếu agent quên `task_submit_review`, hệ thống tự thử lại rồi đánh `failed` sau số lần tối đa — [task-service.ts#L1153-L1160](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L1153-L1160), [#L2024-L2058](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L2024-L2058)
- Subtask chưa xong thì không nộp được. Prompt ghi "submission rejects if any subtask is still `pending`" [MÃ] — [context-engine.ts#L642](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/context-engine.ts#L642)
- Phân rã do prompt điều khiển, và cố ý chờ người [MÃ]:
  - `templates/roles/org-manager/ROLE.md` ghi "**NEVER** create tasks proactively… Only create tasks when a human user explicitly asks you to break down a specific requirement"; "Create no more than 5 tasks at a time"; "Only after the user confirms this plan should you call `create_task`"; "Ensure every task has clear acceptance criteria before assignment" — [ROLE.md#L50-L113](https://github.com/markus-global/markus/blob/bc6f1200a096/templates/roles/org-manager/ROLE.md)
  - Prompt thực thi có các pha "Negotiate the contract… If acceptance criteria are vague, clarify via `task_note`" và "PLAN: Decompose… `subtask_create`" — [context-engine.ts#L1571-L1594](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/context-engine.ts#L1571-L1594)
- Tự động hóa thật chỉ có ở một nhánh [MÃ]:
  - Khi một requirement **do agent đề xuất** được người duyệt, hệ thống nhắn cho agent đó "You should create tasks to fulfill it… use `task_create`".
  - Hàm có `if (req.source !== 'agent') return;`, nên requirement do người tạo không kích hoạt gì — [requirement-service.ts#L704-L733](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/requirement-service.ts#L704-L733)
  - UI [CHẠY] hứa "Agents will break them into tasks automatically" — [ảnh](screenshots/markus_work.png). **UI/README hứa nhiều hơn mã.**
- Trust level [MÃ]:
  - `TrustService` tính các mức `probation → standard → trusted → senior` (probation nếu score<40 hoặc <3 lần giao; senior nếu ≥85 điểm và ≥25 lần), và `adjustApprovalTier` nâng/hạ cấp duyệt. Toàn bộ nằm **trong bộ nhớ** — [trust-service.ts](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/trust-service.ts#L86-L107)
  - Runtime chỉ có đúng một dòng `const _trustService = new TrustService();` (tiền tố `_` = không dùng). Grep không thấy lời gọi `recordDeliveryAccepted` hay `adjustApprovalTier` nào ngoài file định nghĩa — [start.ts#L760](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/cli/src/commands/start.ts#L760)
  - **README "trust levels" khác mã.**
- ReviewService (core) là pipeline checker kiểu CI (lệnh shell, file thay đổi), dùng cho review mã, không phải review nội dung marketing [MÃ] — [review-service.ts#L38-L60](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/review-service.ts#L38-L60)
- Duyệt chi tiền/đăng bài [MÃ]:
  - Không có cổng cứng theo loại hành động.
  - Chỉ có hai cơ chế:
    - `SecurityPolicy.requireApproval` theo **từ khóa lệnh shell** — [security.ts#L5-L62](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/security.ts#L5-L62)
    - Tool `request_user_input`/`userApprovalRequester`, mà **agent tự quyết** có gọi hay không — [agent.ts#L8455-L8480](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/agent.ts#L8455-L8480)

### Inferences
- R3 chỉ ở mức "Một phần". Khung (requirement → task → subtask DAG → review) rất tốt để kiểm soát. Nhưng một yêu cầu mơ hồ như "làm chiến dịch Tết" sẽ **không tự** thành cây task: Secretary/manager phải được người yêu cầu, và vai trò mẫu còn bắt người duyệt kế hoạch.
- R4 gần Đạt về review/rework. Cổng "trước khi chi tiền/đăng bài" thì phải tự cấu hình bằng hook (xem phần mở rộng).

### Gaps
- Chưa chạy thử một vòng review thật vì không cấu hình LLM key trong bản chạy thử.

---

## Markus — model API, mở rộng kênh (CommAdapter), plugin, multi-tenant, sơ đồ tổ chức

### Takeaway
Markus có backend riêng, tự gọi API model bằng key của người dùng qua nhiều provider. Thêm kênh mới **phải sửa core** (`start.ts`) vì không có registry hay nạp động. Không có hệ plugin, chỉ có MCP, skills, template và hook nội bộ. "Multi-tenant" chỉ là cột `org_id`, với 43 chỗ ghi cứng `'default'`. Không có sơ đồ tổ chức kéo-thả; `@xyflow/react` chỉ dùng cho DAG phụ thuộc task.

### Cited Findings
- Gọi model trực tiếp [MÃ]:
  - `AnthropicProvider` fetch `${baseUrl}/v1/messages` (mặc định https://api.anthropic.com) — [anthropic.ts#L92-L141](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/llm/anthropic.ts#L92-L141)
  - Router đăng ký `anthropic`, `openai`, `google`, `ollama`, `markus` (OpenRouter qua key do Hub cấp — [markus-provider.ts#L1-L6](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/llm/markus-provider.ts#L1-L6)), cộng các provider OpenAI-compatible tùy ý (`createOpenAICompatible`) — [router.ts#L1575-L1605](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/llm/router.ts#L1575-L1605)
  - Có file riêng cho dashscope, fireworks, minimax, openai-codex (ChatGPT OAuth).
- Thêm adapter kênh [MÃ]:
  - `MessageRouter.registerAdapter(adapter)` có sẵn, nhưng `messageRouter` là **biến cục bộ** trong `startServer` của `start.ts`, không được xuất ra — [start.ts#L1963](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/cli/src/commands/start.ts#L1963)
  - Không có cơ chế nạp adapter theo cấu hình. Muốn có Zalo phải viết adapter **và** sửa `start.ts`, sửa handler để truyền `senderInfo`, gọi `bindAgentToChannel`, và thêm `'zalo'` vào union `MessagePlatform`/`IntegrationPlatform` ([message.ts#L2](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/shared/src/types/message.ts#L2), [integration.ts#L11](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/shared/src/types/integration.ts#L11))
- Plugin [MÃ]:
  - Không có plugin loader. Các điểm mở rộng không cần fork:
    - MCP servers: `mcpServers` toàn cục và theo skill — [agent-manager.ts#L319](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/agent-manager.ts#L319), [#L1523](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/agent-manager.ts#L1523)
    - Skills từ `~/.markus/skills/` và `~/.claude/skills/` (định dạng SKILL.md) — [skills/index.ts#L37-L38](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/skills/index.ts#L37-L38)
    - Mô tả connector JSON cho **nền tảng agent ngoài** (OpenClaw, Hermes) trong `~/.markus/connectors/*.json` — [connector.ts#L1-L10](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/shared/src/types/connector.ts#L1-L10)
  - Hook trong tiến trình (`ToolHookRegistry`, `GuardrailPipeline`) có API công khai trên `Agent` nhưng chỉ đăng ký được bằng mã.
- Multi-tenant [MÃ]:
  - Có bảng `organizations(id, name, owner_id, plan, max_agents, manager_agent_id, settings…)`, và `teams`/`agents`/`tasks`/`users` có `org_id` — [sqlite-storage.ts#L41-L90](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/storage/src/sqlite-storage.ts#L41-L90)
  - `api-server.ts` có 43 chỗ `orgId: 'default'`/`?? 'default'` và chỉ 1 chỗ dùng `authUser.orgId`. `POST /api/users` lấy `orgId` **từ body** (mặc định `'default'`) — [api-server.ts#L6484](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L6484)
  - `group_chats.org_id DEFAULT 'default'`; `integrations` có `org_id` — [sqlite-storage.ts#L560-L665](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/storage/src/sqlite-storage.ts#L560-L665)
- Sơ đồ tổ chức [MÃ][CHẠY]:
  - `@xyflow/react` chỉ được import trong `components/TaskDAG.tsx`. Ở đó kéo nối cạnh (`onConnect → handleConnect`) tạo phụ thuộc `blockedBy` giữa các task, có kiểm tra vòng — [TaskDAG.tsx#L639-L716](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/web-ui/src/components/TaskDAG.tsx#L639-L716)
  - Trang Team là danh sách PEOPLE/AGENTS kèm chat — [ảnh](screenshots/markus_team.png)
- Nhóm chat người + agent [MÃ]: `group_chat_members(member_type CHECK IN ('human','agent'))` — [sqlite-storage.ts#L570-L578](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/storage/src/sqlite-storage.ts#L570-L578)
- UI và docs [CHẠY][MÃ]:
  - UI có English/中文/Español — [ảnh Settings](screenshots/markus_settings.png)
  - README có bản EN và zh-CN. `docs/` có 30 file trộn Anh–Trung (ví dụ ARCHITECTURE.md có 120 dòng chứa chữ Hán). Log khởi động bằng tiếng Trung.
  - Ảnh `docs/images/dashboard.png` là ảnh marketing dàn dựng (khung "All-in-One AI Workspace" kèm dashboard 54 agent), không phải ảnh chụp thô — [dashboard.png](https://github.com/markus-global/markus/blob/bc6f1200a096/docs/images/dashboard.png)
- Chạy thử [CHẠY]:
  - `npm i @markus-global/cli@0.10.1` + `markus start` khởi động được trong ~2 giây với SQLite, không cần key (provider bị disable).
  - Đăng nhập local account bằng mật khẩu mặc định **`markus123`** (trang login in rõ "First time? Use your email + default password: markus123"; mã: `process.env['ADMIN_PASSWORD'] ?? 'markus123'` — [api-server.ts#L1594](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L1594)) — ảnh: [login](screenshots/markus_login.png), [onboarding](screenshots/markus_onboarding_welcome.png), [team](screenshots/markus_team.png), [work](screenshots/markus_work.png)

### Inferences
- Nhận định cũ "CommAdapter interface → thêm Zalo = implement interface" chỉ đúng một nửa. Interface có thật, nhưng việc đăng ký và truyền danh tính đều phải sửa core.

### Gaps
- Không kiểm UI đa org (/api/orgs POST có tồn tại) vì cách ly dữ liệu đã hỏng ngay từ mã.

---

## Markus — bảng 12 tiêu chí

### Takeaway
Markus mạnh ở khung task/review (R4) và backend riêng (R1). Nó yếu ở đúng những gì phòng Marketing Việt Nam cần nhất: danh tính (R5), kênh Telegram/Zalo (R6) và multi-tenant (R10).

### Cited Findings
| # | Điểm | Bằng chứng ngắn |
|---|---|---|
| R1 Backend riêng | **Đạt** [MÃ] | Provider native Anthropic/OpenAI/Google/Ollama + OpenAI-compatible; fetch trực tiếp `/v1/messages` — [router.ts#L1575-L1605](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/llm/router.ts#L1575-L1605). CLI lập trình (coding tools) chỉ là tùy chọn. |
| R2 Nhiều agent, vai trò, team | **Đạt** [MÃ][CHẠY] | Bảng `teams(lead_agent_id, manager_id)`, `agents(role_id, agent_role manager/worker, team_id)`; template vai trò có `marketing`, `content-writer`; team mẫu `content-team`; nhóm chat người+agent; A2A. |
| R3 Tự phân rã yêu cầu mơ hồ | **Một phần** [MÃ] | Khung requirement → task → subtask + DAG có thật trong mã; phân rã/làm rõ/tiêu chí nghiệm thu chỉ nằm trong prompt, và ROLE.md bắt chờ người xác nhận; chỉ requirement do agent đề xuất mới tự kích hoạt tạo task. |
| R4 Phê bình & duyệt | **Một phần (gần Đạt)** [MÃ] | Bắt buộc reviewer, trạng thái review, trả lại làm lại, task do agent tạo phải có người duyệt (HITL). Không có cổng cứng "trước khi chi tiền/đăng bài". Trust level là mã chết. |
| R5a Biết ai nhắn, kênh nào, nhóm nào | **Một phần** [MÃ] | Web UI: tên + role vào prompt. Feishu: chỉ nhãn `Feishu:<tên>`, role 'user', gộp vào phiên owner. Telegram: không hoạt động. |
| R5b Một người nhiều kênh = 1 hồ sơ | **Không** [MÃ] | Không có bảng/cột liên kết ID ngoài; không có logic hợp nhất. |
| R5c Chức danh/phòng ban/quyền | **Một phần** [MÃ] | Chỉ `role` owner/admin/member/guest (+team_id không đưa vào prompt); không có chức danh, phòng ban, quyền "được yêu cầu gì". |
| R5d Ủy quyền mang theo người yêu cầu | **Một phần (yếu)** [MÃ] | `task.createdBy`/`requirement.createdBy` được lưu nhưng prompt task chỉ hiện tiêu đề/mô tả requirement ([task-service.ts#L1723-L1743](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L1723-L1743)); tin A2A mang `senderRole:'agent'`. |
| R6 Nhiều kênh, thêm kênh không sửa core | **Không** [MÃ][CHẠY] | Chạy thật chỉ có WebUI + Feishu; Telegram/Slack/WhatsApp là mã chưa đăng ký; thêm kênh phải sửa `start.ts`. |
| R7 Tự host + license kinh doanh | **Đạt** [MÃ][CHẠY] | Apache-2.0 từ 2026-08-16 (trước đó AGPL-3.0); chạy offline bằng tài khoản local; lưu ý cổng `multi_user` cho đăng nhập Hub. |
| R8 Còn sống | **Đạt** [MÃ] | v0.10.1 ngày 2026-09-23; 201 commit trên main trong 2026-09. Bus factor ≈1. |
| R9 Sơ đồ tổ chức kéo-thả điều phối | **Không** [MÃ][CHẠY] | Không có sơ đồ tổ chức; xyflow chỉ cho DAG phụ thuộc task. |
| R10 Multi-tenant | **Không** [MÃ] | Chỉ có cột `org_id`; 43 chỗ ghi cứng `'default'`. |
| R11 Plugin | **Một phần** [MÃ] | Không có plugin API; mở rộng qua MCP, skills, template, connector JSON; hook chỉ đăng ký được bằng mã. |
| R12 UI/docs/ảnh thật | **Một phần** [CHẠY][MÃ] | UI gọn, EN/中文/ES; docs trộn EN/ZH; ảnh trong repo là ảnh marketing; đã tự chụp 7 ảnh `markus_*`. |

### Inferences
- Nếu chọn Markus thì gần như chắc chắn phải fork (hoặc gửi PR upstream) cho lớp kênh và danh tính.

### Gaps
- R4, R3: chưa chạy vòng LLM thật.

---

## Markus — dựng lớp danh tính (R5) KHÔNG fork: điểm mở rộng cụ thể

### Takeaway
Chỉ làm được **một phần** mà không fork. Cách khả thi nhất là **một bridge chạy ngoài** (bot Telegram/Zalo riêng) đăng nhập vào Markus **dưới tên từng user đã ánh xạ** rồi gọi REST chat. Khi đó web path tự chèn "tên + role" vào prompt. Chức danh, quyền, chặn theo vai trò và truyền người yêu cầu qua ủy quyền cần mã chạy trong tiến trình (wrapper quanh `startBackend()`, dựa vào API nội bộ không có cam kết ổn định) hoặc fork.

### Cited Findings
- (a) Sổ đăng ký người + vai trò [MÃ]:
  - Đã có bảng `users` (role, team_id, email) và REST `POST /api/users` — [api-server.ts#L6479-L6554](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L6479-L6554)
  - ID Telegram/Zalo không có cột. Có thể nhét vào `users.preferences` (JSON) qua `OrganizationService.updateHumanPreferences(userId, preferences)` (không fork, nhưng lạm dụng trường) — [org-service.ts#L173-L185](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/org-service.ts#L173-L185). Hoặc giữ registry trong CSDL riêng của bridge.
- (b) Chèn "ai đang nói + vai trò + quyền" vào prompt [MÃ]:
  - Điểm vào chuẩn: `Agent.sendMessage(userMessage: string, senderId?: string, senderInfo?: { name: string; role: string; isFirstConversation?; locale?; timezone? }, options?)` — [agent.ts#L1136-L1140](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/agent.ts#L1136-L1140). Kết quả hiển thị ở [context-engine.ts#L1139-L1162](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/context-engine.ts#L1139-L1162). `role` là chuỗi tự do và được in nguyên văn "({role})", nên có thể truyền "Trưởng phòng Content – duyệt ngân sách ≤ 5 triệu".
  - Không fork, cách 1 (bridge REST): đăng nhập bằng email/mật khẩu của user tương ứng để lấy cookie `markus_token` (JWT; `getAuthUser` đọc `cookies['markus_token']` — [api-server.ts#L1618-L1642](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L1618-L1642)), rồi `POST /api/agents/:id/message` → `resolveHumanIdentity` → prompt có tên + role. Chức danh/phòng ban chỉ đưa vào được bằng mẹo đặt `users.name` kiểu "Lan (Trưởng phòng Content)".
  - Không fork, cách 2 (wrapper tiến trình): `import { startBackend } from '@markus-global/cli/backend'` ([backend.ts#L44](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/cli/src/backend.ts#L44)) trả về `BackendInstance.apiServer`; `APIServer` có `public orgService` ([api-server.ts#L886-L889](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L886-L889)) → `orgService.getAgentManager().getAgent(id).sendMessage(text, senderId, {name, role})`. Không có cam kết API ổn định, dễ vỡ khi nâng cấp.
- (c) Chặn hoặc bắt duyệt hành động theo vai trò [MÃ]:
  - `Agent.addToolHook(hook: ToolHook)` — [agent.ts#L3055](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/agent.ts#L3054-L3062) với `ToolHook.before(ctx: {agentId, toolName, arguments, attempt}) → {proceed:false, reason}` — [tool-hooks.ts#L4-L33](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/tool-hooks.ts#L4-L33)
  - Nhưng `ToolHookContext` **không có người gửi**. Muốn biết thì phải đọc trường private `currentInteractingUserId` ([agent.ts#L1839-L1840](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/agent.ts#L1839-L1840)).
  - `InputGuardrail.check(input, {agentId, senderId})` thêm qua `agent.getGuardrails().addInputGuardrail(...)` có thể từ chối tin theo người gửi — [guardrails.ts#L13-L37](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/guardrails.ts#L13-L37), [agent.ts#L3050](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/core/src/agent.ts#L3050)
  - Luồng duyệt của người có sẵn: `hitlService.requestApprovalAndWait(...)`, bảng `approvals(approver_user_ids, target_user_id…)` — [sqlite-storage.ts#L536-L558](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/storage/src/sqlite-storage.ts#L536-L558)
  - Cả ba điểm trên chỉ gắn được qua wrapper tiến trình, không có file cấu hình nào nạp hook.
- (d) Mang người yêu cầu qua ủy quyền [MÃ]:
  - Không có trường nào đi vào prompt.
  - Mẹo không fork: bridge chèn "[Yêu cầu bởi: tên, chức danh, kênh]" vào **mô tả requirement** hoặc **task note**, vì cả hai đều được đưa vào prompt task (`**Requirement Description:**`, `## Task Notes`) — [task-service.ts#L1723-L1756](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/task-service.ts#L1723-L1756)

### Inferences
- Cách "bridge + tài khoản cho từng người" chấp nhận được cho (a)(b) ở mức cơ bản.
- Phần (c) theo vai trò cần wrapper dựa trên API nội bộ, nên thực tế khuyên **fork nhẹ hoặc gửi PR upstream**: thêm bảng `user_identities(platform, external_id, user_id)`, truyền `senderInfo` trong handler router/Feishu, thêm `requester` vào `ToolHookContext`.

### Gaps
- Chưa thử bridge thật, cũng chưa kiểm cơ chế API key cho user (CLI có cờ `--api-key`, nhưng `getAuthUser` chỉ đọc cookie) [?].

---

## Markus — kiểm tra các nhận định của phiên trước

### Takeaway
Phần mô tả cấu trúc (package, bảng) đúng. Các nhận định về kênh Telegram và khả năng mở rộng kênh thì sai. License đã đổi.

### Cited Findings
| Nhận định cũ | Kết quả | Bằng chứng |
|---|---|---|
| Apache-2.0 + bản thương mại | **Đã thay đổi / cần sắc thái** | Apache-2.0 **chỉ từ 2026-08-16** (commit 965e8d94; trước đó AGPL-3.0). "Thương mại" là license dịch vụ/OEM riêng, không có mã EE; nhưng có cổng license `multi_user` cho đăng nhập Hub [MÃ] |
| Monorepo TS: core, comms, org-manager, storage, gui, desktop, web-ui, a2a, remote | **Đúng** (thiếu cli, shared, chrome-extension) | `ls packages` [MÃ] |
| Backend riêng, nhiều provider | **Đúng** | router.ts#L1575-L1605 [MÃ] |
| Bảng organizations → users(org_id, name, email, role, team_id), group_chat_members (human/agent), audit_logs, memory_embeddings | **Đúng** | sqlite-storage.ts#L41, #L389, #L570, #L580, #L404 [MÃ]. Lưu ý: chỉ SQLite, README nói có PostgreSQL là sai |
| packages/comms có telegram, slack, whatsapp, feishu, webui | **Đúng (thư mục có)** nhưng chỉ webui+feishu được nối vào runtime | start.ts#L1963-L2025 [MÃ][CHẠY] |
| Telegram adapter hai chiều thực sự (onMessage, polling, setWebhook) | **Sai** | Không có polling; webhook `http://localhost`; adapter không được đăng ký; router không bind agent [MÃ][CHẠY] |
| CommAdapter → thêm Zalo = implement interface | **Sai (một nửa)** | Interface có, nhưng đăng ký cứng trong start.ts, phải sửa core [MÃ] |
| Chưa rõ Telegram sender có map sang users không; có vẻ dừng ở chat_id | **Đã kiểm: không map** | Handler chỉ truyền `message.senderId` thô, không có senderInfo, không tra users [MÃ] |
| Docs nói phân rã thành cây task, review bắt buộc, trust level probation→senior | **Một phần** | Review bắt buộc: Đúng trong mã. Phân rã: chỉ do prompt, chờ người. Trust level: mã chết (`_trustService` không dùng) [MÃ] |

### Inferences
- Phiên trước đã tin README/cấu trúc thư mục. Kết luận về kênh cần sửa lại hoàn toàn.

### Gaps
- Không có.

---

## Markus — rủi ro đáng chú ý

### Takeaway
Rủi ro lớn nhất là bảo trì (một người, v0.x), bảo mật mặc định kém, và độ vênh giữa README/UI với mã.

### Cited Findings
- Bảo trì: từ 2026-06-01 (mọi nhánh), 862/901 commit là của Jason Carter; phần lớn số còn lại do agent tự động ký tên, chỉ 3 commit từ người ngoài. Tuổi đời 7 tháng. Đã đổi license một lần [MÃ].
- Bảo mật:
  - Mật khẩu admin mặc định `markus123` (in ngay trên trang đăng nhập) [CHẠY].
  - `POST /api/users` chỉ `requireAuth` và lấy `role` từ body, không thấy kiểm `authUser.role` trong handler. Có vẻ member bất kỳ có thể tạo user role `owner` [MÃ; chưa thử khai thác] — [api-server.ts#L6479-L6554](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/api-server.ts#L6479-L6554)
  - Tin Feishu của mọi người bị ghi vào phiên chính của owner [MÃ].
- Riêng tư: telemetry bật mặc định (`return { enabled: true }`) — [telemetry-service.ts#L65-L71](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/telemetry-service.ts#L65-L71). License heartbeat 4 giờ/lần tới Hub chỉ chạy khi có license key — [license-service.ts#L26-L105](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/org-manager/src/license-service.ts#L91-L105) [MÃ].
- Chi phí token: mỗi agent có heartbeat mặc định 30 phút (`heartbeat_interval_ms DEFAULT 1800000`) — [sqlite-storage.ts#L78](https://github.com/markus-global/markus/blob/bc6f1200a096/packages/storage/src/sqlite-storage.ts#L64-L85). Vòng tự thử lại khi quên `task_submit_review` cũng tốn token [MÃ].
- README/UI hứa hơn mã: PostgreSQL, Telegram/Slack/WhatsApp, trust levels, "agents will break them into tasks automatically" [MÃ][CHẠY].

### Inferences
- Nếu dùng, nên khóa mạng nội bộ, đổi mật khẩu mặc định, tắt telemetry, và vá `POST /api/users`.

### Gaps
- Chưa thử khai thác lỗ hổng `POST /api/users`.

---

## Clawith — thông tin chung: repo, license, sao, kích thước, bản phát hành, nhịp commit

### Takeaway
Clawith (github.com/dataelement/Clawith, công ty DataElem) dùng FastAPI + React, Apache-2.0, **~4,2k sao**. Bản mới nhất là v1.11.4-fix.1 (2026-08-24). Commit rất dày từ tháng 3 đến tháng 8, nhưng **không có commit nào trên mọi nhánh kể từ 2026-08-27**, tức đã im lặng khoảng 1 tháng tính đến 2026-09-27.

### Cited Findings
- Repo: https://github.com/dataelement/Clawith, mô tả "Your First AI Agents Company", website www.clawith.ai. Khi xem ngày 2026-09-27: **4.2k sao, 701 fork, 114 watcher, 265 issue mở, 74 PR mở** [DOC] — [GitHub repo page](https://github.com/dataelement/Clawith)
- License [MÃ]:
  - `LICENSE` là Apache 2.0, "Copyright 2025 DataElem Inc.". Chỉ có một file LICENSE, không có thư mục EE/commercial.
  - Lịch sử: "Add MIT License" (2026-03-03) rồi "license: change from MIT to Apache 2.0" (commit f66b20e, 2026-03-09) — [LICENSE](https://github.com/dataelement/Clawith/blob/45fc701c366c/LICENSE)
- Phát hành [MÃ][DOC]:
  - Tag gần nhất: `v1.11.4-fix.1` (2026-08-24 20:04 +0800, trang Releases ghi "Latest", nhãn "24 Aug"; năm suy từ git), `v1.11.4` (2026-08-24), `v1.11.3` (2026-07-28), `v1.11.2` (2026-07-23), `v1.11.1` (2026-07-18), `v1.11.0` "Group Collaboration, Shared Knowledge, Durable Agent Runtime" (2026-07-18), `v1.10.3` (2026-06-15)
  - Tổng 37 tag, có cả tag `ci-drone-smoke-*` — [Releases](https://github.com/dataelement/Clawith/releases)
- Nhịp commit [MÃ]:
  - main: 2026-03: 859 · 04: 603 · 05: 120 · 06: 53 · 07: 301 · 08: 170 · 09: 0
  - Mọi nhánh: 06: 68 · 07: 337 · 08: 281 · 09: 0
  - Commit cuối là nhánh `develop` 2026-08-27T10:54:15+08:00. Commit đầu 2026-03-03. 2.106 commit trên main.
- Người đóng góp từ 2026-06-01 [MÃ]: Y1fe1Zh0u 461 (+18 dưới tên "Yifei Zhou"), yaojin3616 77, 白里卿 41, 姚劲 40, yaojin 20, xiejiayu 15… Nhóm nhỏ của một công ty, một người chiếm phần lớn.
- Kích thước [MÃ]: ~16 MB. `backend/app` ~150 nghìn dòng Python, `backend/tests` ~85 nghìn dòng, frontend ~44 nghìn dòng TS/TSX. PostgreSQL + Redis, tùy chọn MinIO. Có Docker Compose và Helm.
- Không có issue nào chứa "telegram" (0 kết quả) [DOC] — [issues?q=telegram](https://github.com/dataelement/Clawith/issues?q=telegram)

### Inferences
- R8 vẫn Đạt vì bản phát hành 2026-08-24 nằm sau mốc 2026-06-27. Tuy vậy nhịp đang hạ về 0 trong tháng 9, và 265 issue / 74 PR đang mở. Cần theo dõi xem đây là nghỉ ngắn hay chậm lại lâu.

### Gaps
- Không truy cập được clawith.ai, ai-bot.cn, gitcode.csdn.net (proxy chặn), nên chưa đọc whitepaper/docs site.

---

## Clawith — kênh chat, cách thêm kênh, plugin

### Takeaway
Có 7 kênh dùng được: Slack, Discord, Microsoft Teams, Feishu/Lark, WeChat (iLink Bot), WeCom, DingTalk, cộng Atlassian là tích hợp công cụ. **Không có Telegram, không có Zalo.** Mã WhatsApp có nhưng **router không được mount**. Thêm kênh phải sửa core: enum PostgreSQL, router trong `main.py`, service khởi động, UI. **Không có hệ plugin.**

### Cited Findings
- Enum kênh trong DB [MÃ]: `channel_type_enum = ("feishu","wecom","wechat","whatsapp","dingtalk","slack","discord","atlassian","microsoft_teams","agentbay")` — [channel_config.py#L20-L22](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/channel_config.py#L20-L22)
- Đăng ký cứng [MÃ]:
  - `main.py` import từng router (`slack_router`, `discord_router`, `dingtalk_router`, `wecom_router`, `wechat_router`, `teams_router`, `feishu_router`, `atlassian_router`…) — [main.py#L381-L426](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/main.py#L381-L426)
  - Khởi động `feishu_ws`, `dingtalk_stream`, `wecom_stream`, `wechat_poll`, `discord_gw` — [main.py#L309-L318](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/main.py#L309-L318)
  - Không có router WhatsApp nào trong `main.py`.
- Kiểm trên bản chạy thử [CHẠY]:
  - OpenAPI của bản chạy (279 path) có route kênh cho dingtalk, discord, slack, teams, wechat, wecom, feishu, không có whatsapp/telegram/zalo.
  - UI Agent → Settings → Channel Config liệt kê Slack, Discord, Microsoft Teams, Feishu Bot, WeChat (iLink Bot), WeCom, DingTalk, Atlassian — [ảnh](screenshots/clawith_agent_channel_config.png)
- Grep "telegram|zalo" trong backend và frontend: 0 kết quả [MÃ].
- Không có plugin [MÃ]:
  - `builtin_tool_definitions.py` ghi rõ "This is deliberately data plus small conversion helpers. It is not a plugin…" — [builtin_tool_definitions.py#L7](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/builtin_tool_definitions.py#L1-L10)
  - Grep `entry_points`/`importlib.import_module` không ra cơ chế nạp nào.
  - Mở rộng không fork chỉ qua: MCP (tool `import_mcp_server`, `mcp_client.py`; README nói cài tool từ Smithery/ModelScope lúc chạy), Skills (`install_skill`, `search_clawhub`), trigger webhook — [webhooks.py#L1-L5](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/api/webhooks.py#L1-L5)
- README chỉ nêu "each agent gets its own Slack, Discord, or Feishu/Lark bot identity" [DOC] — [README.md#L57](https://github.com/dataelement/Clawith/blob/45fc701c366c/README.md#L57)

### Inferences
- Thêm Zalo/Telegram vào Clawith bắt buộc phải fork hoặc PR upstream. Việc cần làm: migration enum, `api/zalo.py`, gọi `channel_user_service.resolve_channel_user(…, "zalo", …)`, thêm case trong `channel_provider_delivery.py` và form trong UI. Khung mẫu thì rõ ràng.

### Gaps
- Chưa thử kết nối kênh thật nào (cần app ID/secret).

---

## Clawith — danh tính: OrgDepartment, OrgMember, quan hệ, `channel_user_service`, phân quyền, người yêu cầu khi ủy quyền

### Takeaway
Clawith có mô hình danh tính **phong phú nhất** trong hai ứng viên: phòng ban, thành viên có chức danh, đồng bộ danh bạ, quan hệ agent–người và agent–agent, và `origin_user_id` chạy xuyên các Run. Nhưng:
- `ChannelUserResolutionError` **chỉ** ném cho Feishu; các trường hợp khác **tự tạo user mới** (lazy registration).
- Trong runtime v2 (mặc định bật), prompt chat 1:1 **không** có tên người đang nói. Chỉ group chat mới có tên + chức danh + phòng ban.
- Không có mô hình "người này được yêu cầu agent làm gì".
- Agent nhận ủy quyền chỉ thấy tên agent nguồn, không thấy con người ban đầu.

### Cited Findings
- `OrgDepartment` [MÃ]: `__tenant_scoped__ = True`; các trường id, external_id, provider_id, name, parent_id, path, member_count, status, tenant_id, synced_at — [org.py#L13-L31](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/org.py#L13-L31)
- `OrgMember` [MÃ]: `__tenant_scoped__ = True`; các trường open_id, unionid, external_id, provider_id, name, name_translit_full/initial, email, avatar_url, **title**, **department_id**, **department_path**, phone, status, tenant_id, **user_id** (liên kết mềm tới User), synced_at — [org.py#L35-L63](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/org.py#L35-L63)
- `AgentRelationship(agent_id, member_id, relation='collaborator', description, created_by_user_id…)` và `AgentAgentRelationship(agent_id, target_agent_id, relation, description…)` [MÃ]. **Không** có `__tenant_scoped__`; hai bảng chỉ cách ly gián tiếp qua agent — [org.py#L66-L99](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/org.py#L66-L99)
- `User` [MÃ]: có `tenant_id`, `title`, `role Enum('platform_admin','org_admin','agent_admin','member')` — [user.py#L51-L80](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/user.py#L51-L80)
- `ChannelUserService.resolve_channel_user(db, agent, channel_type, external_user_id, extra_info) -> User` [MÃ] — [channel_user_service.py#L74-L207](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/channel_user_service.py#L74-L207)
  - Thứ tự xử lý:
    1. `_ensure_provider` tự tạo IdentityProvider theo kênh.
    2. Tìm OrgMember theo ID ngoài; nếu đã liên kết User thì trả về.
    3. Nếu chưa, khớp User theo **email** rồi **mobile** (`sso_service.match_user_by_email/mobile`) và liên kết OrgMember.
    4. **Chỉ với Feishu**, khi không có user_id/union_id ổn định, ném `ChannelUserResolutionError("…refusing to lazily create a duplicate user from open_id only.")`.
    5. Các trường hợp còn lại: `_create_channel_user` (**lazy registration**) và tạo OrgMember "shell".
  - Được gọi từ wechat, discord, wecom, dingtalk, teams, feishu, slack, whatsapp — grep [MÃ].
- Nhà cung cấp danh tính [MÃ]:
  - Lớp auth: Feishu, DingTalk, WeCom, Google Workspace, **Microsoft Teams (stub: mọi phương thức `raise NotImplementedError("Microsoft Teams OAuth not yet implemented")`)**, Google, GitHub — [auth_provider.py#L271-L841](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/auth_provider.py#L756-L770)
  - Đồng bộ danh bạ (org sync) chỉ có Feishu, DingTalk, WeCom, Google Workspace — [org_sync_adapter.py#L769-L1351](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/org_sync_adapter.py#L769)
  - UI Org Structure [CHẠY] hiện Feishu, WeCom, DingTalk, Google (Admin Directory Sync), OAuth2 (Generic OIDC Provider) — [ảnh](screenshots/clawith_enterprise_org_structure.png)
- Prompt 1:1 [MÃ]:
  - `build_agent_context(agent_id, agent_name, role_description="", current_user_name=None, *, allowed_tool_names=None)` chỉ thêm "## Current Conversation — Current human participant: {name}" (chỉ tên) khi có `current_user_name` — [agent_context.py#L433-L577](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_context.py#L433-L577)
  - Runtime v2 gọi hàm này **không** truyền `current_user_name` — [model_step_service.py#L1601-L1606](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/model_step_service.py#L1601-L1606), cùng tại #L2028 và #L2128
  - Chỉ đường cũ `call_llm` truyền `_user_name` — [caller.py#L504-L551](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/llm/caller.py#L504-L551)
  - Runtime v2 bật mặc định cho mọi nguồn: `AGENT_RUNTIME_V2_ENABLED: bool = True`, và `decide()` trả về cờ toàn cục — [config.py#L134-L137](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/config.py#L134-L137), [agent_runtime/config.py#L97-L132](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/config.py#L97-L132)
- Prompt group [MÃ]: `sender_profile` gồm tên hiển thị, `title` (OrgMember.title, nếu không có thì User.title) và `department` (OrgMember.department_path) — [group_context_builder.py#L261-L291](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/group_context_builder.py#L261-L291)
- Danh sách người có quan hệ [MÃ]: "Collaboration Background" liệt kê "- {member.name} — {member.title}" và ghi chú quan hệ, đưa vào mọi prompt của agent — [agent_context.py#L138-L177](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_context.py#L138-L177)
- Phân quyền [MÃ][CHẠY]:
  - `Agent.access_mode` (company/private/custom) và `AgentPermission(scope_type Enum('company','department','user'), access_level 'use'|'manage')` quyết định **ai được dùng/quản lý agent** — [agent.py#L120-L177](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/agent.py#L120-L177), [permissions.py#L47-L104](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/core/permissions.py#L47-L104)
  - Không có mô hình "được yêu cầu hành động gì".
  - `autonomy_policy` là L1/L2/L3 **theo agent và loại hành động**, không phụ thuộc người yêu cầu — [ảnh](screenshots/clawith_agent_autonomy_policy.png)
- Người yêu cầu khi ủy quyền [MÃ]:
  - A2A đặt `owner_user_id = source_run.origin_user_id or actor_user_id or source_agent.creator_id` và ghi `origin_user_id` vào Run đích — [a2a_runtime.py#L810-L813](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/a2a_runtime.py#L810-L813), [#L668-L669](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/a2a_runtime.py#L668-L669). `AgentRun` có `origin_user_id`, `origin_agent_id`, `parent_run_id` — [agent_run.py#L107-L119](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/agent_run.py#L107-L119)
  - Nhưng goal gửi cho agent đích chỉ là "…Source Agent: {source_agent.name}. Request: {message}", không có người — [a2a_runtime.py#L700-L707](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/a2a_runtime.py#L700-L707)
  - Khối `current_run` trong ngữ cảnh cũng không có origin_user — [context_builder.py#L240-L268](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/context_builder.py#L240-L268)

### Inferences
- 5b (một người nhiều kênh = 1 hồ sơ) chỉ đạt khi hai điều kiện cùng đúng:
  - Danh bạ doanh nghiệp đã được đồng bộ, hoặc kênh cung cấp email/số điện thoại.
  - Ở doanh nghiệp Việt Nam dùng Telegram/Zalo, cả hai đều không có sẵn, nên sẽ sinh user trùng.
- Nhận định cũ "ném ChannelUserResolutionError thay vì đoán" chỉ đúng cho Feishu.

### Gaps
- Chưa kiểm luồng WeChat/Discord truyền `extra_info` gì (email/mobile).
- Chưa chạy chat thật để xác nhận prompt 1:1 v2 thiếu tên. Kết luận dựa trên đọc mã, độ tin trung bình–cao.

---

## Clawith — tự phân rã yêu cầu (OKR, task_executor, Planning v2), review/duyệt, multi-tenant, sơ đồ tổ chức

### Takeaway
- **Không** có phân rã thành cây subtask kèm tiêu chí nghiệm thu:
  - OKR chỉ dùng để theo dõi và báo cáo.
  - `task_executor` chạy **một** task phẳng.
  - "Planning v2" chỉ phân công bước đầu cho **các agent được @ trong nhóm** (≥2 agent).
- Duyệt: L3 theo agent, người duyệt là người tạo agent. Trong runtime v2 chỉ thấy thực thi cho xóa file và xác nhận tạo phê duyệt Feishu.
- Multi-tenant **thật**: có bộ lọc ORM tự động.
- Không có sơ đồ tổ chức kéo-thả; chỉ có cây phòng ban dạng danh sách.

### Cited Findings
- `Task` [MÃ]: phẳng, gồm `agent_id` đơn, type todo|supervision, status pending|doing|done, `created_by`. Không có parent/subtask/acceptance — [task.py#L13-L60](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/task.py#L13-L60)
- `task_executor` [MÃ]: tạo goal **tiếng Trung cố định** "[任务执行] {title}\n任务描述: …\n\n请认真完成此任务，给出详细的执行结果。" rồi khởi chạy Run — [task_executor.py#L28-L40](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/task_executor.py#L28-L40)
- OKR [MÃ]:
  - `okr_agent_hook.py` chỉ tự gắn thành viên mới / agent công khai vào OKR Agent (`relation="okr_coordinator"`) — [okr_agent_hook.py#L1-L30](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/okr_agent_hook.py#L1-L30)
  - `okr_scheduler.py` đọc `focus.md` bằng regex, tạo báo cáo ngày/tuần — [okr_scheduler.py#L1-L14](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/okr_scheduler.py#L1-L14)
  - Tool `create_objective`/`create_key_result` do LLM gọi. OKR có `owner_type` company/user/agent — [okr.py#L35-L62](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/okr.py#L35-L62)
- Planning v2 [MÃ]:
  - System prompt yêu cầu trả JSON `{version, mode advisory|enforced, goal, plan_prompt, entry_steps[{agent_id, instruction}]}`, kèm các câu "Use only candidate agent_id values", "Do not invent analysis, synthesis, status reporting, **review**…", "Do not describe a DAG, step IDs, dependencies", "When wording is vague, make the smallest literal interpretation explicit" — [planning.py#L40-L100](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/planning.py#L40-L100)
  - Ứng viên lấy từ `candidate_agents`, bắt buộc ≥2 — [planning_scheduler.py#L81-L110](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/planning_scheduler.py#L81-L110)
- Duyệt [MÃ][CHẠY]:
  - `AutonomyService.check_and_enforce(db, agent, action_type, details)` với L1/L2/L3; L3 tạo `ApprovalRequest` gửi người tạo agent — [autonomy_service.py#L1-L110](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/autonomy_service.py#L51-L110)
  - Bảng ánh xạ tool của đường cũ có write_file, delete_file, send_feishu_message, send_message_to_agent, web_search, execute_code — [agent_tools.py#L2229-L2240](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_tools.py#L2229-L2240), thực thi tại [#L4697-L4720](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_tools.py#L4697-L4720)
  - Runtime v2 chỉ gọi `check_and_enforce` trong `_delete_autonomy_gate` (xóa file) — [tool_step_service.py#L1860-L1958](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/tool_step_service.py#L1860-L1958). Ngoài ra còn cổng xác nhận `feishu_approval_create` — [#L840-L870](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/tool_step_service.py#L840-L870). `execute_builtin_tool_outcome` không kiểm autonomy (đọc mã).
  - UI vẫn cho đặt L3 cho Write Files, Delete Files… — [ảnh](screenshots/clawith_agent_autonomy_policy.png). **UI có thể hứa nhiều hơn runtime v2 thực thi** (đọc mã, chưa thử).
  - Không có quy trình reviewer / trả lại làm lại.
- Multi-tenant [MÃ][CHẠY]:
  - Listener `do_orm_execute` gắn `with_loader_criteria(model, cls.tenant_id == tenant_id)` vào **mọi ORM SELECT**, áp cho model có `__tenant_scoped__` hoặc có `tenant_id NOT NULL`, khi context tenant được middleware đặt — [dao/base.py#L120-L175](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/dao/base.py#L120-L175)
  - Có 11 file model gắn `__tenant_scoped__`. Có trang AdminCompanies/PlatformDashboard. Bản chạy tạo công ty "Default", người đăng ký đầu tiên là "Platform Admin" — [ảnh](screenshots/clawith_dashboard.png)
  - Giới hạn: chỉ áp cho SELECT qua ORM, không cho UPDATE/DELETE hàng loạt hay SQL thô, và không áp khi context tenant là None.
- Sơ đồ tổ chức [MÃ][CHẠY]:
  - `OrgTab.tsx` có `DeptTree` (danh sách thụt lề, ký hiệu ▾/·), dữ liệu đồng bộ từ IdP — [OrgTab.tsx#L23-L63](https://github.com/dataelement/Clawith/blob/45fc701c366c/frontend/src/pages/enterprise-settings/tabs/OrgTab.tsx#L23-L63)
  - Frontend không có xyflow/reactflow, chỉ có `recharts`.
  - Tab "Directory" của agent liệt kê người/agent **được phép liên hệ** — [ảnh](screenshots/clawith_agent_directory.png)
- UI/docs [CHẠY][MÃ]:
  - UI chỉ có `en.json`, `zh.json`. README có bản en, zh-CN, ja, ko, es, ar.
  - Repo **không có ảnh chụp sản phẩm** (chỉ có slogan, QR, logo kênh). Các ảnh `clawith_*` trong thư mục screenshots do tôi tự chụp.
  - Múi giờ mặc định công ty là Asia/Shanghai.
- Cài đặt [CHẠY] (chạy native với Python 3.12 + PG16 + Redis, không dùng Docker):
  - `alembic upgrade head` trên DB trống **lỗi** tại `f065_feishu_group_target`: "column delivery_target_id of relation agent_schedules already exists".
  - Nguyên nhân: `001_initial_schema` dùng `Base.metadata.create_all` với model hiện tại — [001_initial_schema.py#L19-L22](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/alembic/versions/001_initial_schema.py#L19-L22)
  - `entrypoint.sh` thoát khi migration lỗi, trừ khi đặt `ALLOW_MIGRATION_FAILURE=true`.
  - Cách vượt qua: `upgrade f064_tool_call_tenants` rồi `stamp head`. Sau đó UI chạy được, hiển thị `v1.11.4-fix.1 (45fc701)`.

### Inferences
- R3 của Clawith yếu hơn Markus: Clawith không có khung task/subtask/review, chỉ có điều phối nhóm theo @mention.
- R10 là điểm cộng rõ nhất của Clawith.

### Gaps
- Chưa chạy vòng LLM thật, nên chưa kiểm Planning v2 hay luồng duyệt L3 lúc chạy.
- Chưa kiểm cài bằng Docker (daemon Docker không có trong môi trường).

---

## Clawith — bảng 12 tiêu chí

### Takeaway
Clawith mạnh ở danh tính doanh nghiệp (R5 một phần khá), multi-tenant (R10) và số kênh (R6 một phần). Clawith yếu ở phân rã/review (R3/R4), không có Telegram/Zalo, và ngôn ngữ/mặc định thiên về Trung Quốc.

### Cited Findings
| # | Điểm | Bằng chứng ngắn |
|---|---|---|
| R1 Backend riêng | **Đạt** [MÃ] | `PROVIDER_REGISTRY`: anthropic, openai, azure, deepseek, qwen, minimax, openrouter, zhipu, baidu, gemini, kimi, vllm, ollama, sglang, custom — [client.py#L2336-L2461](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/llm/client.py#L2336-L2461). Agent loại "openclaw" (bên ngoài) chỉ là tùy chọn. |
| R2 Nhiều agent, vai trò, team | **Một phần** [MÃ][CHẠY] | Nhiều agent (soul.md), A2A notify/consult/task_delegate, nhóm có Planning. Agent không được xếp vào phòng ban/team (phòng ban chỉ dành cho người; agent–agent chỉ là quan hệ). |
| R3 Tự phân rã yêu cầu mơ hồ | **Một phần (yếu)** [MÃ] | Planning v2 chỉ tạo entry_steps cho các agent được @, cấm DAG/review; Task phẳng; OKR chỉ theo dõi. |
| R4 Phê bình & duyệt | **Một phần (yếu)** [MÃ] | L3 approval theo agent, người duyệt là người tạo agent; runtime v2 chỉ thực thi cho xóa file + phê duyệt Feishu; không có reviewer/rework. |
| R5a | **Một phần** [MÃ] | Kênh → User; group có tên + chức danh + phòng ban; 1:1 v2 không có tên trong prompt. |
| R5b | **Một phần** [MÃ] | Hợp nhất theo OrgMember ID/email/mobile trong tenant; nếu không khớp thì lazy-create user trùng; không có Telegram/Zalo. |
| R5c | **Một phần** [MÃ] | Có chức danh + phòng ban (OrgMember), role nền tảng, quyền dùng agent theo phòng ban; không có quyền "được yêu cầu gì". |
| R5d | **Một phần** [MÃ] | `origin_user_id` truyền qua A2A và lưu DB, nhưng không vào prompt agent nhận. |
| R6 Kênh + mở rộng | **Một phần** [MÃ][CHẠY] | 7 kênh chạy thật (không có Telegram/Zalo; WhatsApp chưa mount); thêm kênh phải sửa core. |
| R7 Tự host + license | **Đạt** [MÃ] | Apache-2.0 (từ 2026-03-09, trước là MIT); Compose/Helm; không có phần EE. |
| R8 Còn sống | **Đạt (cảnh báo)** [MÃ] | v1.11.4-fix.1 ngày 2026-08-24; không có commit từ 2026-08-27. |
| R9 Sơ đồ tổ chức | **Không** [MÃ][CHẠY] | Chỉ có cây phòng ban dạng danh sách; không kéo-thả; không điều phối. |
| R10 Multi-tenant | **Đạt** [MÃ][CHẠY] | Bảng tenants + bộ lọc ORM tự động + Platform Admin. |
| R11 Plugin | **Một phần** [MÃ] | Không có plugin API (mã ghi rõ); chỉ có MCP (cài lúc chạy), Skills, webhook trigger. |
| R12 UI/docs/ảnh | **Một phần** [CHẠY][DOC] | UI EN/ZH khá gọn; README 6 thứ tiếng có English; không có ảnh sản phẩm trong repo; prompt/goal cứng bằng tiếng Trung; docs site không truy cập được. Đã tự chụp 11 ảnh `clawith_*`. |

### Inferences
- Với tiêu chí "nhớ ai là ai", Clawith là nền tảng tốt hơn để **sửa**: dữ liệu đã có sẵn, chỉ thiếu phần nối vào prompt và phần kênh VN.

### Gaps
- Xem các mục Gaps ở trên.

---

## Clawith — dựng lớp danh tính (R5) KHÔNG fork: điểm mở rộng cụ thể

### Takeaway
Dữ liệu (a) đã có sẵn, và (c) làm được ở mức thô bằng cấu hình UI. Còn (b) cho chat 1:1, (c) theo vai trò người yêu cầu, (d) vào prompt, và kênh Telegram/Zalo thì **đều cần sửa mã**. Hàm liên quan không có hook hay plugin; ví dụ `prompt_builder` chỉ là tham số hàm dựng trong Python.

### Cited Findings
- (a) Sổ đăng ký người + vai trò [MÃ]:
  - Có sẵn OrgDepartment/OrgMember (title, department_path, external_id/open_id/unionid) và `User.role`.
  - Đồng bộ từ Feishu/DingTalk/WeCom/Google Workspace, hoặc Generic OIDC (UI) — [org.py](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/org.py#L13-L63)
  - Điểm hợp nhất kênh: `ChannelUserService.resolve_channel_user(db, agent, channel_type: str, external_user_id: str|None, extra_info: dict|None) -> User` — [channel_user_service.py#L74-L81](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/channel_user_service.py#L74-L81). Chỉ gọi được từ mã kênh (không fork thì không thêm kênh được).
- (b) Chèn ai đang nói, vai trò, quyền [MÃ]:
  - Không fork, dùng được hai thứ:
    - Group chat: runtime tự chèn tên, chức danh, phòng ban — [group_context_builder.py#L261-L291](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/group_context_builder.py#L261-L291)
    - Mô tả `AgentRelationship.description` (sửa được qua UI/API "relationships") xuất hiện trong mọi prompt, ví dụ "Lan — Trưởng phòng Content; được duyệt ngân sách" — [agent_context.py#L138-L177](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_context.py#L138-L177)
  - Chat 1:1 cần sửa `model_step_service.py#L1601` để truyền `current_user_name`, hoặc sửa `build_agent_context(agent_id, agent_name, role_description="", current_user_name=None, *, allowed_tool_names=None)` — [agent_context.py#L433-L440](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_context.py#L433-L440). `ModelStepService(…, prompt_builder: PromptBuilder = build_agent_context)` cho tiêm builder khác, nhưng chỉ qua mã khởi tạo — [model_step_service.py#L1350-L1363](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/model_step_service.py#L1350-L1363)
- (c) Chặn/duyệt theo vai trò [MÃ][CHẠY]:
  - Không fork, có hai cách:
    - Dùng `AgentPermission(scope_type='department'|'user', access_level='use')` để chỉ phòng/nhóm người nhất định **dùng được** agent nhạy cảm (ví dụ agent "Chạy quảng cáo"), cấu hình qua UI — [agent.py#L163-L177](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/models/agent.py#L163-L177)
    - Đặt `autonomy_policy` L3 cho agent đó; người duyệt là người tạo agent — [autonomy_service.py#L51-L65](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/autonomy_service.py#L51-L65). Cần lưu ý runtime v2 hiện chỉ thực thi cổng này cho xóa file.
  - Chặn theo vai trò của **người yêu cầu** cần sửa `tool_step_service.py` (ví dụ mở rộng `_delete_autonomy_gate` thành cổng tổng quát có `origin_user_id`).
- (d) Mang người yêu cầu qua ủy quyền [MÃ]:
  - Dữ liệu đã chạy đúng (`origin_user_id` — [a2a_runtime.py#L810-L813](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/a2a_runtime.py#L810-L813)).
  - Chỉ cần sửa `_target_goal(source_agent, request)` để thêm tên/chức danh người gốc — [a2a_runtime.py#L700-L707](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/a2a_runtime.py#L700-L707). Việc này phải fork hoặc PR.
- Kênh Zalo/Telegram không fork [?]: chỉ có thể làm bằng bridge ngoài đăng nhập dưới tên từng user rồi gửi qua API chat/group. Chưa kiểm API group-message công khai.

### Inferences
- Với Clawith, fork cần ít dòng hơn Markus vì dữ liệu và luồng `origin_user_id` đã có. Nhưng codebase Python lớn (150 nghìn dòng) và thay đổi rất nhanh, nên chi phí rebase fork sẽ cao. Gửi PR upstream cho (b)/(d) là lựa chọn hợp lý hơn.

### Gaps
- Chưa kiểm API tạo relationship và API group message từ bên ngoài.

---

## Clawith — kiểm tra các nhận định của phiên trước

### Takeaway
Phần lớn nhận định đúng về dữ liệu, nhưng có ba chỗ cần sửa: cách xử lý lỗi của `channel_user_service`, danh sách kênh, và stub Microsoft Teams SSO. Mức tự phân rã nay đã kiểm được: yếu.

### Cited Findings
| Nhận định cũ | Kết quả | Bằng chứng |
|---|---|---|
| Apache-2.0, FastAPI + React, backend riêng | **Đúng** | LICENSE; `main.py` FastAPI; frontend React/Vite [MÃ][CHẠY]. Lưu ý: MIT→Apache ngày 2026-03-09 |
| OrgDepartment, OrgMember(name, title, department_id, department_path, email, phone, open_id/unionid/external_id), AgentRelationship, AgentAgentRelationship; bảng gắn `__tenant_scoped__` | **Đúng, có chỉnh** | Trường khớp (thêm user_id, provider_id, avatar_url, name_translit_*). Chỉ OrgDepartment/OrgMember có `__tenant_scoped__`, hai bảng quan hệ thì không [MÃ] |
| channel_user_service map người gửi → OrgMember, dùng lại SSO; ném ChannelUserResolutionError thay vì đoán | **Một phần / Sai ở vế sau** | Có map qua OrgMember và SSO email/mobile; nhưng **chỉ Feishu** mới ném lỗi, còn lại thì **tự tạo user mới** [MÃ] |
| IdP: Feishu, DingTalk, WeCom, Google Workspace, Microsoft Teams, Google, GitHub — sync danh bạ + SSO | **Một phần** | Lớp có đủ, nhưng **Teams OAuth là stub NotImplementedError**. Sync danh bạ chỉ Feishu/DingTalk/WeCom/Google Workspace (+OIDC chung). Google/GitHub chỉ để đăng nhập [MÃ][CHẠY] |
| Kênh: DingTalk, Feishu, WeChat, Discord, Slack; không Telegram, không Zalo | **Đã thay đổi (bổ sung)** | Thêm WeCom, Microsoft Teams (+Atlassian là công cụ). WhatsApp có mã nhưng chưa mount. Không Telegram/Zalo: **Đúng** [MÃ][CHẠY] |
| Không có hệ plugin — thêm kênh = sửa core | **Đúng** | builtin_tool_definitions.py#L7; main.py đăng ký cứng [MÃ] |
| Có OKR services và task_executor; mức tự phân rã chưa kiểm | **Đã kiểm: yếu** | OKR để theo dõi/báo cáo; task_executor chạy task phẳng; Planning v2 chỉ phân công bước đầu cho agent được @ [MÃ] |

### Inferences
- Không có.

### Gaps
- Không có.

---

## Clawith — rủi ro đáng chú ý

### Takeaway
Các rủi ro chính: nhịp phát triển đang chững lại, cài mới có lỗi migration, ngôn ngữ/mặc định Trung Quốc, và UI/runtime vênh nhau ở cổng duyệt.

### Cited Findings
- Bảo trì: không có commit mới trên mọi nhánh kể từ 2026-08-27. Còn 265 issue / 74 PR mở. Một người đóng góp (Y1fe1Zh0u/Yifei Zhou) chiếm ~70% commit từ 2026-06-01 (479/682) [MÃ][DOC].
- Cài đặt: `alembic upgrade head` trên DB trống lỗi ở commit 45fc701 (migration f065 thêm cột mà `create_all` ban đầu đã tạo) [CHẠY].
- Bản địa hóa:
  - Goal task cứng bằng tiếng Trung — [task_executor.py#L28-L40](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/task_executor.py#L28-L40)
  - Danh sách lời chào kiểm tra trong Planning phần lớn là tiếng Trung — [planning.py#L44-L66](https://github.com/dataelement/Clawith/blob/45fc701c366c/backend/app/services/agent_runtime/planning.py#L44-L66)
  - UI chỉ có EN/ZH, không có tiếng Việt; múi giờ mặc định Asia/Shanghai [CHẠY].
  - Hệ sinh thái tích hợp thiên về Trung Quốc: Feishu/DingTalk/WeCom/WeChat, Qwen/Zhipu/Baidu/Kimi.
- Bảo mật:
  - Runtime v2 dường như không thực thi L3 cho write/send/execute dù UI cho cấu hình [MÃ, chưa thử].
  - Log khởi động cảnh báo "bubblewrap (bwrap) is not installed… Local execute_code will use the reduced-isolation fallback" khi chạy ngoài Docker [CHẠY].
  - Lazy registration có thể tạo user "rác" cho người lạ nhắn vào bot [MÃ].
- Chi phí token: heartbeat mặc định 240 phút, khung 09:00–18:00, theo UI [CHẠY]; trigger tự tạo (Aware); OKR agent gom báo cáo hằng ngày [MÃ].

### Inferences
- Để dùng ở Việt Nam cần viết thêm kênh Zalo/Telegram, bổ sung bản dịch tiếng Việt, đổi múi giờ, và vá một số chỗ trong runtime. Như vậy thực chất là một fork có bảo trì.

### Gaps
- Chưa kiểm hiệu năng/chi phí thực tế khi chạy LLM.
