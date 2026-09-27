# Các nền tảng agent mã nguồn mở nổi tiếng chưa được đánh giá (OpenClaw, elizaOS, Agent Zero, Eigent/CAMEL, Dify, Coze Studio, Letta, CrewAI) — ứng viên hoặc nền cho phòng Marketing đa agent tự host

Ghi chú phương pháp (áp dụng cho toàn bộ file):
- Ngày làm việc: 2026-09-27 (đã xác nhận bằng `date`: `Sun Sep 27 03:41:53 UTC 2026`). Mốc R8 = có release/tag từ 2026-06-27 trở đi.
- Mã đã đọc (clone `--depth 1` để đọc mã, clone `--bare --filter=tree:0` để lấy ngày tag bằng `git for-each-ref`):
  - OpenClaw `openclaw/openclaw` @ `96e4061553977c4434544b3f45059035d048fe3c` (2026-09-27T03:41:43Z)
  - elizaOS `elizaOS/eliza` @ `eb157cac4767dfc0268f6995e09de109d8468ff8` (2026-09-26T19:43:55-07:00)
  - Agent Zero `agent0ai/agent-zero` @ `e3051fb584b1a36be2b0a0c90606f1c2c2d356ec` (2026-09-23T19:39:16+02:00)
  - Eigent `eigent-ai/eigent` @ `3ec6f4c3c8794789fcf0abf5b572fa309a355b8a` (2026-09-26T11:46:39+08:00)
  - CAMEL `camel-ai/camel` @ `fc27907e31ea2074d6b65ceb121573c5fa1ab345` (2026-09-20T12:56:23+08:00)
  - Dify `langgenius/dify` @ `725611b2e9a425519e9fcb4dcc579bafea936d27` (2026-09-26T18:10:34Z)
  - Coze Studio `coze-dev/coze-studio` @ `fefb05ff27be1da939612fbf9faf5db62583b8ae` (2026-07-29T03:17:51Z)
  - Letta (repo cũ) `letta-ai/letta` @ `5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a` (2026-09-10) và Letta Code `letta-ai/letta-code` @ `44b154e45384d2e38a8c503b33dc1695e7fd91dd` (2026-09-26)
  - CrewAI `crewAIInc/crewAI` @ `4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec` (2026-09-25T18:00:20Z)
- Nhãn: [MÃ] = đã đọc mã nguồn; [DOC] = chỉ đọc tài liệu/README (kể cả docs nằm trong repo); [CHẠY] = đã cài và chạy (không có mục nào — không cài đặt nền tảng nào trong đợt này); [?] = chưa kiểm chứng.
- Không cài đặt/chạy nên KHÔNG chụp ảnh màn hình; thư mục `screenshots/` không được thêm file. Chỉ trích dẫn ảnh có sẵn trong repo.
- Số sao lấy từ trang GitHub qua WebFetch ngày 2026-09-27 (số làm tròn theo GitHub hiển thị).
- `docs.elizaos.ai` bị proxy chặn (EGRESS_BLOCKED) nên không đọc được tài liệu chính thức của elizaOS; mọi nhận định elizaOS dựa vào mã.

## 1. Triage nhanh cả 8 nền tảng: giấy phép và giới hạn dùng thương mại, R1 (backend riêng), R8 (release gần nhất), có hỗ trợ thật R3/R5 không

### Takeaway
Cả 8 đều tự host được và (trừ Dify) có giấy phép cho phép dùng thương mại không ràng buộc (MIT/Apache-2.0); Dify là "Apache 2.0 sửa đổi" cấm vận hành multi-tenant và cấm gỡ logo ở frontend. Coze Studio thất bại R8 (release cuối 2026-01-20); elizaOS chỉ còn tag beta (stable npm cuối 2026-01-19). Chỉ OpenClaw và elizaOS có hạ tầng định danh (R5) đáng kể trong mã; chỉ OpenClaw (Workboard) và CAMEL/Eigent (Workforce) có cơ chế phân rã việc (R3) thật trong mã — nhưng đều không có bước "làm rõ yêu cầu mơ hồ + viết tiêu chí nghiệm thu" bắt buộc.

### Cited Findings

Bảng triage (sao/fork thấy ngày 2026-09-27):

| Nền tảng | Giấy phép | R1 backend riêng | R8 release/tag gần nhất | R3 thật? | R5 thật? | Sao |
|---|---|---|---|---|---|---|
| OpenClaw | MIT, "© 2026 OpenClaw Foundation" [MÃ] | Đạt [MÃ] | `v2026.8.33` 2026-09-26, `v2026.9.6` 2026-09-23 (npm `latest`=2026.9.6) [MÃ git] | Một phần (Workboard `workboard_specify`/`workboard_decompose`) | Một phần–khá (5a đạt; 5b/5c/5d một phần) | ~391k sao / 82.2k fork |
| elizaOS | MIT [MÃ] | Đạt [MÃ] | tag `v2.0.3-beta.11` 2026-07-16; npm `@elizaos/core` latest=1.7.2 (2026-01-19), beta=2.0.3-beta.7 (2026-06-28) | Không thấy | Khá (5a đạt, 5b đạt theo từng agent, 5c một phần, 5d không) | 19.5k / 5.8k |
| Agent Zero | MIT, "© 2025 Agent Zero, s.r.o" [MÃ] | Đạt (LiteLLM) [MÃ] | `v2.13` 2026-09-23 (12 tag từ 2026-06-27) | Một phần (prompt) | Yếu | 19.3k / 3.8k |
| Eigent (dựa CAMEL) | Apache-2.0 [MÃ] | Đạt (CAMEL, BYO key/local model) [DOC/MÃ] | `v1.0.5` 2026-09-25 | Một phần (Workforce decompose) | Không | 15.4k / 1.8k |
| CAMEL (thư viện) | Apache-2.0 [MÃ] | Đạt [MÃ] | `v0.2.91a7` 2026-09-03 (chỉ bản alpha) | Một phần | Không | 17.8k / 2.1k |
| Dify | Apache-2.0 sửa đổi (cấm multi-tenant, cấm sửa logo frontend) [MÃ] | Đạt [DOC] | `1.17.1` 2026-09-10 | Không (workflow do người thiết kế) | Rất yếu (EndUser theo app) | 157.3k / 24.8k |
| Coze Studio | Apache-2.0 (`LICENSE-APACHE`) [MÃ] | Đạt [DOC] | `v0.5.1` 2026-01-20 → **trượt R8**; commit cuối 2026-07-29 | Không | Không | 21.6k / 3.1k |
| Letta (nay là Letta Code) | Apache-2.0 [MÃ] | Đạt (local backend dùng `@earendil-works/pi-ai`) [MÃ] | `letta-code` `v0.33.2` 2026-09-25 (116 tag từ 2026-06-27); repo `letta` cũ: `0.16.8` 2026-05-14 (đã dừng) | Không | Yếu (allowlist kênh) | letta 24.9k; letta-code 3.4k / 420 |
| CrewAI | MIT, "© 2025 crewAI, Inc." [MÃ] | Đạt [MÃ] | `1.15.22` 2026-09-16 (26 tag từ 2026-06-27) | Một phần (hierarchical/planning) | Không | 59.1k / 8.6k |

- OpenClaw LICENSE: "MIT License Copyright (c) 2026 OpenClaw Foundation" [MÃ] — [LICENSE](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/LICENSE)
- elizaOS LICENSE: "MIT License Copyright (c) 2026 Shaw Walters and elizaOS Contributors" [MÃ] — [LICENSE](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/LICENSE)
- Agent Zero LICENSE: "MIT License Copyright (c) 2025 Agent Zero, s.r.o" [MÃ] — [LICENSE](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/LICENSE)
- Eigent: README "This repository is licensed under the Apache License 2.0" và file LICENSE là Apache 2.0 nguyên bản [MÃ]; tuy nhiên README quảng cáo "Enterprise Features - SSO, access control" là tính năng thương mại riêng ("Exclusive Features (like SSO & custom development)") [DOC] — [README](https://github.com/eigent-ai/eigent/blob/3ec6f4c3c8794789fcf0abf5b572fa309a355b8a/README.md)
- Dify LICENSE — trích nguyên văn [MÃ] — [LICENSE](https://github.com/langgenius/dify/blob/725611b2e9a425519e9fcb4dcc579bafea936d27/LICENSE):
  > "Dify is licensed under a modified version of the Apache License 2.0, with the following additional conditions:
  > 1. Dify may be utilized commercially, including as a backend service for other applications or as an application development platform for enterprises. Should the conditions below be met, a commercial license must be obtained from the producer:
  > a. Multi-tenant service: Unless explicitly authorized by Dify in writing, you may not use the Dify source code to operate a multi-tenant environment.
  >     - Tenant Definition: Within the context of Dify, one tenant corresponds to one workspace. The workspace provides a separated area for each tenant's data and configurations.
  > b. LOGO and copyright information: In the process of using Dify's frontend, you may not remove or modify the LOGO or copyright information in the Dify console or applications. This restriction is inapplicable to uses of Dify that do not involve its frontend.
  >     - Frontend Definition: For the purposes of this license, the "frontend" of Dify includes all components located in the `web/` directory when running Dify from the raw source code, or the "web" image when running Dify with Docker.
  > 2. As a contributor, you should agree that:
  > a. The producer can adjust the open-source agreement to be more strict or relaxed as deemed necessary.
  > b. Your contributed code may be used for commercial purposes, including but not limited to its cloud business operations.
  > Apart from the specific conditions mentioned above, all other rights and restrictions follow the Apache License 2.0. [...]
  > The interactive design of this product is protected by appearance patent.
  > © 2025 LangGenius, Inc."
- Coze Studio chỉ có `LICENSE-APACHE` (Apache 2.0) [MÃ]; tag cuối `v0.5.1` 2026-01-20, 0 tag từ 2026-06-27, chỉ 1 commit từ 2026-06-27 (2026-07-29 "fix(infra): align statefulset servicename...") [MÃ git] — [repo](https://github.com/coze-dev/coze-studio/tree/fefb05ff27be1da939612fbf9faf5db62583b8ae)
- Letta: README repo `letta-ai/letta` nói "The current source code lives in `letta-ai/letta-code`" và "The `archive` branch contains the retired Letta V1 API server" [DOC] — [README](https://github.com/letta-ai/letta/blob/5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a/README.md); tag cuối của repo cũ `0.16.8` 2026-05-14 [MÃ git]
- CrewAI LICENSE MIT "Copyright (c) 2025 crewAI, Inc."; README nhắc bản thương mại "CrewAI AMP Suite ... managed deployment, observability, governance" [MÃ/DOC] — [README](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/README.md)
- Ngày tag lấy bằng `git for-each-ref --sort=-creatordate` trên clone treeless; trang tag tương ứng: [OpenClaw tags](https://github.com/openclaw/openclaw/tags), [eliza tags](https://github.com/elizaOS/eliza/tags), [agent-zero tags](https://github.com/agent0ai/agent-zero/tags), [eigent tags](https://github.com/eigent-ai/eigent/tags), [camel tags](https://github.com/camel-ai/camel/tags), [dify tags](https://github.com/langgenius/dify/tags), [coze-studio tags](https://github.com/coze-dev/coze-studio/tags), [letta-code tags](https://github.com/letta-ai/letta-code/tags), [crewAI tags](https://github.com/crewAIInc/crewAI/tags)
- npm: `@elizaos/core` dist-tags `latest: '1.7.2'`, `beta: '2.0.3-beta.7'`; 1.7.2 publish 2026-01-19T20:50:18Z; 2.0.3-beta.7 publish 2026-06-28T08:09:52Z; `openclaw` dist-tags `latest: '2026.9.6'`, `extended-stable: '2026.7.35'` (lấy bằng `npm view`) — [npm @elizaos/core](https://www.npmjs.com/package/@elizaos/core), [npm openclaw](https://www.npmjs.com/package/openclaw)
- Trang Releases GitHub của elizaOS chỉ hiển thị các "release" chứa asset CI (`pr-evidence-14` 2026-09-26, `pr-evidence-11` đánh dấu "Latest" 2026-08-23), không phải bản phát hành sản phẩm [DOC] — [eliza releases](https://github.com/elizaOS/eliza/releases)
- Số sao/fork (2026-09-27): [OpenClaw](https://github.com/openclaw/openclaw) 391k/82.2k; [eliza](https://github.com/elizaOS/eliza/releases) 19.5k/5.8k; [agent-zero](https://github.com/agent0ai/agent-zero) 19.3k/3.8k; [eigent](https://github.com/eigent-ai/eigent) 15.4k/1.8k; [camel](https://github.com/camel-ai/camel) 17.8k/2.1k; [dify](https://github.com/langgenius/dify) 157.3k/24.8k; [coze-studio](https://github.com/coze-dev/coze-studio) 21.6k/3.1k; [letta](https://github.com/letta-ai/letta) 24.9k/2.6k; [letta-code](https://github.com/letta-ai/letta-code) 3.4k/420; [crewAI](https://github.com/crewAIInc/crewAI) 59.1k/8.6k.
- Mức độ hoạt động (số commit trên HEAD từ 2026-06-27, tính bằng `git rev-list --count --since`): OpenClaw 38,463; eliza 21,286; dify 2,296; letta-code 942; agent-zero 534; crewAI 315; eigent 141; camel 64; letta (cũ) 8; coze-studio 1 [MÃ git].

### Inferences
- Chọn 3 nền tảng để kiểm sâu: OpenClaw (mạnh nhất về kênh + định danh + plugin + Zalo), elizaOS (mô hình entity/world/role + Principal identity), Agent Zero (backend riêng, phân cấp agent, Telegram/WhatsApp, MIT). Eigent/CAMEL đáng giá ở R3 nhưng không có kênh chat và không có định danh → chỉ triage.
- Dify loại cho kịch bản "một cài đặt phục vụ nhiều công ty" (R10) vì giấy phép; dùng nội bộ một workspace thì được, nhưng phải giữ logo/copyright ở giao diện `web/`.
- Coze Studio loại do R8 (không release trong 8 tháng) và tài liệu hướng về coze.cn tiếng Trung.
- Tốc độ commit cực lớn của OpenClaw (~38k commit/3 tháng) và eliza (~21k) là rủi ro "churn": API/config thay đổi liên tục, nhiều commit do agent AI tạo (nhánh/tag `codex/...`, `checkpoint/...` trong eliza).

### Gaps
- Không kiểm chứng số sao bằng nguồn thứ hai; 391k sao của OpenClaw là con số GitHub hiển thị qua WebFetch, không đối chiếu được.
- Không cài đặt bản nào nên không có đánh giá [CHẠY] và không có ảnh chụp màn hình mới.

## 2. OpenClaw — kiểm chứng mã: định tuyến đa agent, sub-agent, identityLinks, quyền, Zalo, plugin SDK, phân rã/duyệt, release, giấy phép

### Takeaway
OpenClaw là nền mạnh nhất trong nhóm: backend gọi API model trực tiếp, nhiều agent với bindings theo kênh/tài khoản/peer/guild/role, team preset (coordinator/researcher/writer/reviewer), Workboard có `specify`/`decompose`/trạng thái `review`, 27 plugin kênh gồm `zalo` (Bot API chính thức) và `zalouser` (zca-js, không chính thức), và plugin SDK rất rộng (thêm kênh, chèn ngữ cảnh mỗi lượt, chặn/đòi duyệt tool, kho lưu riêng). Điểm yếu nằm đúng ở R5: `session.identityLinks` chỉ gộp *khóa phiên DM*, không tạo hồ sơ; `users.linkChannelIdentity` (mới, v2026.9.6) chỉ dùng cho quyền owner/admin; không có chức danh/phòng ban; sub-agent chỉ biết "requester session" + kênh, không biết người thật là ai.

### Cited Findings

**Định tuyến đa agent / bindings**
- Schema binding có `match` gồm `accountId` (rỗng = tài khoản mặc định, `"*"` = mọi tài khoản), `peer`, `guildId`, `teamId`, `roles`, và override `dmScope` theo binding [MÃ] — [zod-schema.agents.ts#L96-L120](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/config/zod-schema.agents.ts#L96-L120)
- Thứ tự ưu tiên binding: "exact peer, parent peer, peer wildcard, guild+roles, guild, team, account, channel, default agent"; nhiều trường trong một binding là AND [DOC] — [multi-agent.md#L307-L315](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/concepts/multi-agent.md#L307-L315)
- Team preset: `openclaw agents team create` tạo `coordinator` (chief of staff), researcher, writer, reviewer, mỗi agent có workspace riêng; `subagents.allowAgents` + `delegationMode: "prefer"`; tài liệu nói rõ `"prefer"` "is prompt guidance, not a scheduler"; "Role instructions require human approval before external sends, publication, purchases, deletion, or production changes" [DOC] — [multi-agent.md#L112-L175](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/concepts/multi-agent.md#L112-L175)

**Sub-agent và việc con có biết người yêu cầu gốc**
- System prompt của sub-agent chỉ gồm "Requester session: <requesterSessionKey>" và "Requester channel: <channel>" trong mục "## Session Context" [MÃ] — [subagent-system-prompt.ts#L118-L128](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/agents/subagents/spawn/subagent-system-prompt.ts#L118-L128)
- Metadata spawn lưu `spawnedBy`, `groupId`, `groupChannel`, `groupSpace`, `workspaceDir`, danh sách allow/deny tool kế thừa [MÃ] — [spawned-context.ts#L14-L35](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/agents/spawned-context.ts#L14-L35)
- Chính sách tool theo người yêu cầu được giải một lần ở cổng vào tin cậy, con cháu dùng "persisted effective parent projection" thay vì đoán danh tính: "Sender-dependent policy resolves once at trusted ingress; verified descendants consume the persisted effective parent projection instead of guessing identity." [MÃ] — [requester-tool-policy.ts#L1-L5](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/agents/requester-tool-policy.ts#L1-L5)
- Tài liệu: "Internal events and delegated tasks do not automatically inherit a personal profile. Subagent bootstrap still contains only its existing allowed project instructions." [DOC] — [user-model.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/concepts/user-model.md)
- Tác vụ ủy quyền giữ "snapshot" danh sách profile người góp công của phiên nguồn (tối đa 32) nhưng chỉ phục vụ ghi công Git co-author, "does not ... grant access" [DOC] — [user-model.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/concepts/user-model.md)

**`session.identityLinks` — liên kết gì, áp dụng ở đâu**
- Kiểu cấu hình: `identityLinks: z.record(z.string(), z.array(z.string()))` (tên chuẩn → danh sách ID có tiền tố kênh) [MÃ] — [zod-schema.session-config.ts#L44](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/config/zod-schema.session-config.ts#L44)
- Help text: "Maps canonical identities to provider-prefixed peer IDs so equivalent users resolve to one DM thread (example: telegram:123456)." [MÃ] — [schema.help.automation.ts#L13-L14](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/config/schema.help.automation.ts#L13-L14)
- `resolveLinkedDirectPeerId` so khớp `peerId` hoặc `channel:peerId` với danh sách, trả về *tên canonical* (chuỗi) — không có dữ liệu hồ sơ [MÃ] — [session-key.ts#L265-L301](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/routing/session-key.ts#L265-L301)
- Trong `buildAgentPeerSessionKey`, link chỉ áp dụng khi `peerKind === "direct"` và `dmScope !== "main"`; mặc định `dmScope ?? "main"` → với cấu hình mặc định identityLinks KHÔNG có tác dụng; nhóm (group) không dùng identityLinks [MÃ] — [session-key.ts#L206-L263](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/routing/session-key.ts#L206-L263)
- Các nơi dùng khác: `resolve-route.ts`, `history.ts` (lọc lịch sử DM theo peer logic), `runtime-policy-session-key.ts` (khóa chính sách per-peer), `security/audit-channel.ts` (audit), và các kênh telegram/whatsapp/synology-chat/clickclack/zalouser [MÃ] — [history.ts#L144-L152](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/agents/embedded-agent-runner/history.ts#L144-L152), [runtime-policy-session-key.ts#L131-L142](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/auto-reply/reply/runtime-policy-session-key.ts#L131-L142)
- Tài liệu khẳng định identityLinks KHÔNG xác lập danh tính người: "Display names, usernames, and `session.identityLinks` do not establish this association." [DOC] — [user-model.md (Channel identity links)](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/concepts/user-model.md)

**Định danh người dùng (Gateway profile) và liên kết kênh**
- Có "Gateway profiles" cho người đăng nhập Control UI, với `gateway.roles` (định nghĩa vai trò: quyền xem phiên người khác `none/view/suggest/write`, danh sách agent được dùng, `modelPolicy`, `scopes`, `accessPolicyPlugin`) [MÃ] — [schema.help.core.ts#L145-L172](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/config/schema.help.core.ts#L145-L172)
- Phương thức Gateway `users.linkChannelIdentity` / `users.listChannelIdentities` / `users.unlinkChannelIdentity` (cần `operator.admin`), `identity = {channelId, accountId, senderId}` [MÃ] — [users-channel-identities.ts#L33-L60](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/gateway/server-methods/users-channel-identities.ts#L33-L60), [user-profiles.types.ts#L45-L49](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/state/user-profiles.types.ts#L45-L49)
- Nơi tiêu thụ liên kết này duy nhất là `resolveUserChannelIdentity` trong `channel-operator-authority.ts`, được gọi từ `auto-reply/command-auth.ts` (quyền lệnh owner); hàm trả về sớm nếu không cấu hình `gateway.roles` hoặc `gateway.auth.identityScopes` [MÃ] — [channel-operator-authority.ts#L49-L75](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/gateway/channel-operator-authority.ts#L49-L75)
- Release note 2026.9.6: "Recognize explicitly linked Team administrators in channels (#153508)"; "Links do not expand conversation visibility or give a group the administrator's authority." [DOC] — [releases/2026.9.6.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/releases/2026.9.6.md)
- USER.md cá nhân theo profile (`users/<canonical-profile-id>/USER.md`) chỉ cho người đăng nhập Gateway; "Display labels, channel sender IDs, unknown-source creator IDs, and agent owners cannot select a personal file." [DOC] — [user-model.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/concepts/user-model.md)
- Multi-user mode: "Session ownership, visibility in the sidebar, and presence indicators are usability features, not security boundaries." [DOC] — [multi-user.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/concepts/multi-user.md)

**Ngữ cảnh người gửi mỗi lượt (5a)**
- `buildInboundUserContextPrefix` chèn khối "Conversation info:" gồm `chat_id`, `message_id`, `sender{id,name,username,e164,is_bot}`, `conversation_label`, `group_subject`, `group_channel`, `group_space`, `group_members`, `topic_name`... (sender chỉ đưa vào khi không phải DM qua webchat) [MÃ] — [inbound-meta.ts#L574-L660](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/auto-reply/reply/inbound-meta.ts#L574-L660)
- System prompt có khối JSON `openclaw.inbound_meta.v2` gồm `account_id`, `channel`, `provider`, `surface`, `chat_type`, kèm cảnh báo "Treat human names, group subjects ... as untrusted content" [MÃ] — [inbound-meta.ts#L540-L571](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/auto-reply/reply/inbound-meta.ts#L540-L571)

**Quyền hạn (owner allowlist, allowFrom, group policy, elevated/exec approvals)**
- `commands.ownerAllowFrom` ("Explicit owner allowlist for owner-scoped commands"), `commands.allowFrom`, `tools.elevated.allowFrom` [MÃ] — [schema.help.agents.ts#L220-L223](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/config/schema.help.agents.ts#L220-L223), [schema.help.runtime.ts#L171-L178](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/config/schema.help.runtime.ts#L171-L178)
- Kênh có `dmPolicy` (`pairing|allowlist|open|disabled`, mặc định `pairing`), `allowFrom`, `groupPolicy` (`open|disabled|allowlist`) [MÃ] — (schema sinh tự động) [bundled-channel-config-metadata.generated.ts](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/config/bundled-channel-config-metadata.generated.ts)
- `tools.toolsBySender`: khóa `channel:<channelId>:<senderId>`, `id:`, `e164:`, `username:`, `name:`, `"*"` → allow/deny tool theo người gửi; per-agent override [DOC+MÃ] — [tool-policy.md#L225-L243](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/gateway/config-tools/tool-policy.md#L225-L243), [sender-tool-policy.ts#L25-L60](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/agents/sender-tool-policy.ts#L25-L60)
- Pipeline chính sách tool xếp lớp: profile, provider, global, agent, group, sender, sandbox, subagent, inherited, và `ownerOnlyCoreToolPolicy` (deny các tool lõi owner-only nếu `!senderIsOwner`) [MÃ] — [tool-dispatch.ts#L126-L150](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/skills/runtime/tool-dispatch.ts#L126-L150)
- Exec approvals: "Commands run only when policy + allowlist + (optional) user approval all agree" [DOC] — [exec-approvals.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/tools/exec-approvals.md)

**Kênh Zalo (`zalo`, `zalouser`)**
- Có 27 extension kênh có file `channel-plugin-api.ts`: a2a, buzz, clickclack, discord, feishu, googlechat, imessage, irc, line, matrix, mattermost, msteams, nextcloud-talk, nostr, qa-channel, raft, reef, signal, slack, sms, synology-chat, telegram, tlon, twitch, whatsapp, zalo, zalouser [MÃ] — [extensions/](https://github.com/openclaw/openclaw/tree/96e4061553977c4434544b3f45059035d048fe3c/extensions)
- `extensions/zalo` (`@openclaw/zalo` 2026.9.6, "Zalo channel plugin for bot and webhook chats"), gọi `https://bot-api.zaloplatforms.com` (Zalo Bot Platform) [MÃ] — [zalo/src/api.ts#L3-L15](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/extensions/zalo/src/api.ts#L3-L15)
- Tài liệu: "Status: experimental. Direct messages and group chats are both implemented"; token lấy ở bot.zaloplatforms.com; mặc định DM policy là pairing [DOC] — [docs/channels/zalo.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/channels/zalo.md)
- `extensions/zalouser` (`@openclaw/zalouser`, "Zalo Personal Account plugin via native zca-js integration", phụ thuộc `zca-js` 2.2.0); README cảnh báo "Using Zalo automation may result in account suspension or ban ... This is an unofficial integration." [MÃ] — [zalouser/package.json](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/extensions/zalouser/package.json), [zalouser/README.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/extensions/zalouser/README.md)
- Plugin ngoài `@zalo-platforms/openclaw-zaloclawbot` (id `openclaw-zaloclawbot`, đăng nhập QR Zalo Mini App); OpenClaw ghi rõ hành vi "not verified against OpenClaw core source"; npm version 0.1.4 (npm `time.modified` 2026-06-17) [DOC] — [docs/channels/zaloclawbot.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/channels/zaloclawbot.md)

**Plugin SDK**
- `OpenClawPluginApi` có `registerChannel`, `registerTool`, `registerHook`, `on<K extends PluginHookName>`, `registerGatewayMethod`, `registerHttpRoute`, `registerService`, `registerTrustedToolPolicy`, `registerGatewayAccessPolicy`, `registerContextEngine`, `registerProvider`, `registerCommand`, `registerControlUiDescriptor`… [MÃ] — [plugin-api.types.ts#L183-L383](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/plugin-api.types.ts#L183-L383), `on` tại [#L472](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/plugin-api.types.ts#L472)
- 42 hook: `before_model_resolve`, `agent_turn_prepare`, `before_prompt_build`, `before_agent_reply`, `llm_input`, `message_received`, `before_tool_call`, `after_tool_call`, `subagent_spawned`, `subagent_ended`, `before_dispatch`, `before_agent_run`, … (không còn `before_agent_start` trong danh sách hook hiện hành) [MÃ] — [hook-types.ts#L107-L150](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-types.ts#L107-L150)
- Hook chèn prompt (`agent_turn_prepare`, `before_prompt_build`, `heartbeat_prompt_contribution`) bị chặn nếu cấu hình `allowPromptInjection: false`; hook hội thoại cần `plugins.entries.<id>.hooks.allowConversationAccess: true` [MÃ/DOC] — [hook-types.ts#L178-L199](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-types.ts#L178-L199), [docs/plugins/hooks.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/plugins/hooks.md)
- Ngữ cảnh hook `PluginHookAgentContext` có `agentId`, `sessionKey`, `channel`, `accountId`, `chatId`, `senderId`, `channelContext`, `inputProvenance`, `toolAuthority` [MÃ] — [hook-types.ts#L274-L316](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-types.ts#L274-L316)
- Kết quả `before_prompt_build`: `systemPrompt`, `prependContext`, `appendContext`, `toolsAllow` (thu hẹp tool trong lượt), `prependSystemContext`, `appendSystemContext` [MÃ] — [hook-before-agent-start.types.ts#L22-L51](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-before-agent-start.types.ts#L22-L51)
- Kết quả `before_tool_call`: `params`, `block`, `blockReason`, `requireApproval{title, description, severity, timeoutMs, allowedDecisions: allow-once|allow-always|deny, onResolution}` [MÃ] — [hook-before-tool-call-result.ts#L14-L35](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-before-tool-call-result.ts#L14-L35)
- Kho lưu riêng của plugin: `api.runtime.state.openKeyedStore<T>(options)` (SQLite-backed) và `openBlobStore` [MÃ] — [runtime/types-core.ts#L516-L530](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/runtime/types-core.ts#L516-L530)
- Hook `subagent_spawned` nhận ctx `{runId, childSessionKey, requesterSessionKey}` và event có `requester{channel, accountId, to, threadId, messageId}` [MÃ] — [hook-types.ts#L769-L831](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-types.ts#L769-L831)

**Phân rã việc và duyệt (R3/R4)**
- Plugin Workboard (bundled): trạng thái `triage, backlog, todo, scheduled, ready, running, review, blocked, done`; tool `workboard_specify` ("Turn a rough triage/backlog card into a clarified `todo` card; records the spec summary"), `workboard_decompose` ("Fan a parent orchestration card into linked children"), `workboard_link` (phụ thuộc cha-con), `workboard_claim`, `workboard_complete/block`, `workboard_proof`, `workboard_reassign` [DOC] — [docs/plugins/workboard.md#L86-L189](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/plugins/workboard.md#L86-L189)
- "Board metadata can set `autoDecompose`... OpenClaw records this intent and exposes it in worker context. Actual specification/decomposition still runs through the normal Workboard tools." [DOC] — [workboard.md#L299-L302](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/plugins/workboard.md#L299-L302)
- Lifecycle sync chuyển run thành công sang `review` (`succeeded: { card: "review", execution: "review" }`); "Manual review states win" [MÃ/DOC] — [lifecycle-sync.ts#L108](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/extensions/workboard/src/lifecycle-sync.ts#L108)
- "Proof statuses are worker-reported outcomes, not independent verification." [DOC] — [workboard.md#L191](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/plugins/workboard.md#L191)

**R1, R10, R12, bảo mật**
- Runtime mặc định `openclaw` là embedded harness; Claude CLI chỉ là "CLI backend" tùy chọn theo model; Codex/Copilot là plugin harness tùy chọn [DOC] — [agent-runtimes.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/concepts/agent-runtimes.md); transport gọi API trực tiếp (`@anthropic-ai/sdk` 0.126.0, `openai` 7.17.0 trong package.json) [MÃ] — [anthropic-transport-stream.ts](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/packages/ai/src/transports/anthropic-transport-stream.ts)
- Multi-tenant: "OpenClaw's default security model is one trusted operator boundary per Gateway ... running a separate complete OpenClaw instance for each tenant"; `openclaw fleet` "cell" mỗi tenant, "Fleet is experimental" [DOC] — [multi-tenant-hosting.md](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/gateway/multi-tenant-hosting.md)
- Docs chỉ có tiếng Anh (`docs.json` languages = `['en']`); Control UI có locale `vi.ts` [MÃ] — [ui/src/i18n/locales](https://github.com/openclaw/openclaw/tree/96e4061553977c4434544b3f45059035d048fe3c/ui/src/i18n/locales)
- Ảnh có sẵn trong repo: `docs/assets/macos-onboarding/*.png|jpeg`, `docs/whatsapp-openclaw.jpg`, `docs/images/feishu-get-group-id.png`, banner/hero; không thấy ảnh chụp Control UI/Workboard trong repo [MÃ] — [docs/assets](https://github.com/openclaw/openclaw/tree/96e4061553977c4434544b3f45059035d048fe3c/docs/assets)
- Không tìm thấy "org chart" trong docs (`grep -rli "org chart|orgchart|organization chart" docs` rỗng) [MÃ].
- Bảo mật: CVE-2026-25253 (đánh cắp token qua tham số `gatewayUrl` của Control UI → RCE, CVSS 8.8, sửa từ 2026.1.29); chiến dịch "ClawHavoc" với hơn 800 skill độc hại trên ClawHub — [SonicWall](https://www.sonicwall.com/blog/openclaw-auth-token-theft-leading-to-rce-cve-2026-25253), [The Hacker News](https://thehackernews.com/2026/05/four-openclaw-flaws-enable-data-theft.html)

**Chấm 12 tiêu chí — OpenClaw (commit 96e40615)**

| Tiêu chí | Điểm | Bằng chứng ngắn |
|---|---|---|
| R1 | Đạt [MÃ] | runtime `openclaw` gọi API bằng `@anthropic-ai/sdk`/`openai`; CLI backend chỉ tùy chọn |
| R2 | Đạt [MÃ/DOC] | `agents.entries` + bindings (channel/account/peer/guild/team/roles); team preset coordinator/researcher/writer/reviewer; `subagents.allowAgents`. Không có khái niệm "phòng ban" hạng nhất |
| R3 | Một phần [DOC/MÃ] | Workboard `workboard_specify`, `workboard_decompose`, phụ thuộc cha-con; nhưng do LLM tự gọi tool, không có bước làm rõ/tiêu chí nghiệm thu bắt buộc |
| R4 | Một phần [MÃ/DOC] | cột `review`, vai trò reviewer, `before_tool_call.requireApproval`, exec approvals; không có vòng "trả về làm lại" bắt buộc bằng mã; duyệt trước khi đăng chỉ là chỉ dẫn trong vai trò |
| R5a | Đạt [MÃ] | khối `Conversation info` (sender id/name/username, group_subject…) + `inbound_meta.v2` (channel, account, chat_type) mỗi lượt |
| R5b | Một phần [MÃ] | `session.identityLinks` chỉ gộp khóa phiên DM khi `dmScope != main`; `users.linkChannelIdentity` gắn sender kênh → Gateway profile nhưng chỉ dùng cho quyền owner/admin |
| R5c | Một phần [MÃ/DOC] | `gateway.roles` (cho người đăng nhập UI), `toolsBySender`, `ownerAllowFrom`, `elevated.allowFrom`; không có chức danh/phòng ban; profile không được đưa vào prompt cho người gửi qua kênh |
| R5d | Một phần [MÃ] | con biết `requesterSessionKey` + kênh; kế thừa chính sách tool của người yêu cầu; không biết tên/vai trò người thật |
| R6 | Đạt [MÃ] | 27 extension có `channel-plugin-api.ts` (telegram, discord, slack, whatsapp, feishu, line, zalo, zalouser, msteams, matrix, signal, googlechat…) qua `api.registerChannel` |
| R7 | Đạt [MÃ] | MIT, không điều khoản bổ sung |
| R8 | Đạt [MÃ git] | `v2026.9.6` 2026-09-23, `v2026.8.33` 2026-09-26; 37 tag `v*` từ 2026-06-27 |
| R9 | Không [MÃ] | không thấy org chart |
| R10 | Một phần [DOC] | 1 Gateway = 1 vùng tin cậy; Fleet (thử nghiệm) = 1 cell/tenant |
| R11 | Đạt [MÃ] | plugin SDK rất rộng (kênh, tool, hook, gateway method, http route, policy, storage) |
| R12 | Một phần [DOC/MÃ] | docs tiếng Anh rất nhiều; UI có tiếng Việt; ít ảnh UI trong repo; cấu hình phức tạp |

### Inferences
- OpenClaw là "nền" khả thi nhất cho phòng Marketing tự host ở Việt Nam: có Zalo Bot (API chính thức bot-api.zaloplatforms.com) và Zalo cá nhân (rủi ro khóa tài khoản), team preset gần với cấu trúc "trưởng nhóm + chuyên viên + reviewer", và plugin SDK đủ để xây lớp định danh mà không fork (xem mục 9).
- Hạn chế cốt lõi: mô hình tin cậy là "một nhóm tin nhau trên một Gateway"; phân biệt sếp/nhân viên/khách qua kênh chat phải tự xây bằng plugin; phân quyền tool theo người gửi có sẵn (`toolsBySender`) nhưng khóa theo ID kênh, không theo hồ sơ hợp nhất.
- Churn rất lớn (38k commit/3 tháng, nhiều tuyến release `2026.6.x/2026.7.x/2026.8.x/2026.9.x` song song, trường deprecated có ngày gỡ như "Removal: after 2026-09-08") → plugin bên ngoài cần theo sát SDK.

### Gaps
- Chưa đọc mã `workboard_specify` để biết có trường tiêu chí nghiệm thu (acceptance criteria) có cấu trúc không [?].
- Chưa kiểm thứ tự thời gian giữa hook `subagent_spawned` và lượt `before_prompt_build` đầu tiên của con (quan trọng cho 5d bằng plugin) [?].
- Plugin `@zalo-platforms/openclaw-zaloclawbot` là mã ngoài, chưa đọc [?].
- Không chạy thử nên chưa xác nhận UI Workboard/Control UI thực tế.

## 3. elizaOS — kiểm chứng mã: entities/components/worlds/rooms, vai trò, liên kết đa nền tảng, nhiều agent, plugin API, phân rã/duyệt, release, giấy phép

### Takeaway
elizaOS (nhánh v2 trên `main`, `package.json` version 2.0.4) có mô hình dữ liệu định danh giàu nhất trong nhóm: Entity/Component/World/Room, vai trò OWNER/ADMIN/MEMBER/GUEST/NONE theo World được thực thi ở action gate, và một "identity authority" (PrincipalService + IdentityClaim + merge/split có nhật ký) để gộp cùng một người trên nhiều kênh. Nhưng: định danh bị phạm vi theo từng agent (UUID = hash(platformId:agentId)), host độc lập hiện chỉ chạy `agents.list[0]`, không có ủy quyền giữa các agent eliza (orchestrator chỉ điều khiển coding CLI qua ACP), không có phân rã việc, không có kênh Zalo, và sản phẩm đã chuyển hướng sang "agentic OS" cá nhân. Release ổn định cuối trên npm là 1.7.2 (2026-01-19).

### Cited Findings
- Kiểu dữ liệu: `Component{id, entityId, agentId, roomId, worldId, sourceEntityId, type, data}`, `Entity{id, names[], metadata, agentId, components}`, `Role = {OWNER, ADMIN, MEMBER, GUEST, NONE}`, `WorldMetadata{ownership{ownerId}, roles: Record<string, Role>, ...}`, `World`, `Room{source, type, channelId, worldId, serverId}`, `Relationship{sourceEntityId, targetEntityId, tags}` [MÃ] — [types/environment.ts#L12-L110](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/environment.ts#L12-L110)
- Entity UUID phụ thuộc agent: `createUniqueUuid(runtime, baseUserId)` = `stringToUuid(\`${baseUserId}:${runtime.agentId}\`)` [MÃ] — [entities.ts#L90-L100](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/entities.ts#L90-L100); plugin Telegram dùng hàm này cho world/room/entity [MÃ] — [plugin-telegram/src/service.ts#L1683-L1690](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-telegram/src/service.ts#L1683-L1690)
- Thứ hạng vai trò `CANONICAL_ROLE_RANK = {NONE:0, GUEST:1, USER:2, MEMBER:2, ADMIN:3, OWNER:4}`, `RoleGate{roles, anyOf, allOf, noneOf, minRole}` [MÃ] — [access-control/role-primitives.ts#L1-L80](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/access-control/role-primitives.ts#L1-L80)
- Nơi thực thi: `runtime/action-gate.ts` kiểm `contextGate.roleGate ?? action.roleGate` và `action.roleGate` [MÃ] — [action-gate.ts#L110-L140](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/runtime/action-gate.ts#L110-L140); `execute-planned-tool-call.ts` gọi `checkSenderRole` [MÃ] — [execute-planned-tool-call.ts#L1126](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/runtime/execute-planned-tool-call.ts#L1126); provider cũng có `roleGate` (vd. ROLES provider `roleGate: { minRole: "ADMIN" }`) [MÃ]
- `checkSenderRole` → `resolveWorldForMessage` → `resolveEntityRole(world.metadata, entityId)`; OWNER lưu trong world chỉ được công nhận nếu nguồn cấp là `"manual"` (sửa lỗi #14707: chủ guild Discord từng tự thành OWNER); vai trò có thể lấy từ entity đã liên kết (`getConfirmedLinkedEntityIds`) khi không có PrincipalService [MÃ] — [roles.ts#L738-L926](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/roles.ts#L738-L926), [roles.ts#L1110-L1129](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/roles.ts#L1110-L1129)
- Connector admin whitelist (`setConnectorAdminWhitelist`, `matchEntityToConnectorAdminWhitelist`) cấp ADMIN theo metadata kênh [MÃ] — [roles.ts#L663-L725](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/roles.ts#L663-L725)
- Identity authority: `Principal{id, agentId, kind: person|agent|service|organization|unknown, displayName}`, `IdentityClaim{principalEntityId, namespace, connectorId, connectorAccountId, externalSubjectId, handle, verification: unverified|observed|verified|owner_bound, status, confidence, ownerBindingId, provenance}`, thao tác merge/split có trạng thái `planned|committed|completed|reverted|failed` [MÃ] — [types/identity.ts#L1-L80](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/identity.ts#L1-L80), `abstract class PrincipalService` [#L434](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/identity.ts#L434)
- Triển khai SQL: `attestPersonLink`, `verifyPersonLink`, `proposeMerge`, `confirmMerge`, `commitMerge`, `split`, `resolveCanonicalPrincipal`, `getCluster`, nhật ký merge và redirect có phiên bản ("Attestation evidence is append-only") [MÃ] — [plugin-sql/src/services/sql-principal.ts#L1-L6](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-sql/src/services/sql-principal.ts#L1-L6), [#L558-L1300](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-sql/src/services/sql-principal.ts#L558)
- RelationshipsService (plugin-assistant): danh bạ theo agent, "strengthened identity records (`entity_identities`) with confidence-based auto-merge candidates (`entity_merge_candidates`), and identity-cluster resolution via union-find"; `ContactInfo{categories, tags, preferences, customFields}` [MÃ] — [plugin-assistant/src/services/relationships.ts#L1-L10](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/services/relationships.ts#L1-L10), [#L182-L187](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/services/relationships.ts#L182-L187)
- Ngữ cảnh người gửi: provider `ENTITIES` chèn "# People in the Room" + `senderName` (roleGate GUEST) [MÃ] — [providers/entities.ts#L1-L60](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/basic-capabilities/providers/entities.ts); provider `ROLES` chỉ cho ADMIN, chỉ trong GROUP ("No access to role information in DMs") [MÃ] — [providers/roles.ts#L80-L140](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-assistant/src/features/advanced-capabilities/providers/roles.ts#L80-L140)
- Lưu ý kỹ thuật: text của provider chỉ tới planner nếu khai báo `contexts`/`contextGate` hoặc `alwaysInResponseState` [MÃ] — [types/components.ts#L858-L912](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/components.ts#L858)
- Plugin API: `Plugin{name, init, services, componentTypes, actions, providers, chatPreHandlers, evaluators, responseHandlerEvaluators, adapter, models, events, connectorSources, routes?, views, widgets, contexts, autoEnable, dependencies, priority, schema}` [MÃ] — [types/plugin.ts#L1119-L1322](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/plugin.ts#L1119); `ComponentTypeDefinition{name, schema, validator}` [#L65-L69](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/plugin.ts#L65-L69); runtime `createComponent(component)`, `getComponents(...)`, `updateWorld(world)` [MÃ] — [types/runtime.ts#L1396-L1456](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/runtime.ts#L1396)
- Nhiều agent: kiểu `Project{agents: ProjectAgent[]}` vẫn tồn tại [MÃ] — [types/plugin.ts#L1324-L1333](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/plugin.ts#L1324-L1333); nhưng host độc lập `packages/agent` chỉ đọc `config.agents?.list?.[0]` (build-character-config, plugin-collector, first-time-setup) [MÃ] — [build-character-config.ts#L40](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/runtime/build-character-config.ts#L40); đa agent có trong dịch vụ cloud `packages/cloud/services/agent-server/src/agent-manager.ts` ("hosted agent-server manager boundary for cloud runtime containers") [MÃ] — [agent-manager.ts#L1](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/cloud/services/agent-server/src/agent-manager.ts#L1)
- Config `packages/agent` có `agents.list`, `bindings`, `broadcast` (hình dạng rất giống OpenClaw) [MÃ] — [config/zod-schema.ts#L586](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/agent/src/config/zod-schema.ts#L586)
- `plugin-agent-orchestrator`: "spawning and orchestrating coding sub-agents via the Agent Client Protocol (ACP)... Configure the chosen coding-agent executable and credentials" (tức điều khiển CLI coding bên ngoài, không phải agent eliza khác) [DOC] — [plugin-agent-orchestrator/README.md](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-agent-orchestrator/README.md)
- Tài liệu/bài viết (qua kết quả tìm kiếm, không đọc được docs gốc) mô tả "Add Multiple Agents" với nhiều `ProjectAgent` và "inter-agent signaling for delegation" — [docs.elizaos.ai guide (tiêu đề qua search)](https://docs.elizaos.ai/guides/add-multiple-agents), [Starlog](https://starlog.is/articles/ai-agents/elizaos-eliza/). Repo `elizaOS/the-org` ("Agents for organizations") hiện trả về 404 — [github.com/elizaOS/the-org](https://github.com/elizaOS/the-org)
- Duyệt/xác nhận: `ServiceType.APPROVAL`, kiểu `PendingUserAction` hợp nhất "task-based approvals (`ApprovalService`), the LifeOps approval queue, pending planner prompts" [MÃ] — [types/pending-user-action.ts#L1-L30](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/pending-user-action.ts), [types/service.ts#L34](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/service.ts#L34)
- Kênh: plugins `plugin-telegram`, `plugin-discord`, `plugin-slack`, `plugin-x`, `plugin-imessage`, `plugin-google-workspace`… Không có plugin Zalo; UI chỉ liệt kê id connector `zalo`/`zalouser` trong registry giao diện [MÃ] — [plugins/](https://github.com/elizaOS/eliza/tree/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins), [connector-mode-registry.ts#L530-L541](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/ui/src/components/connectors/connector-mode-registry.ts#L530-L541)
- R1: `plugin-openai` dùng `@ai-sdk/openai`, `plugin-anthropic` dùng `@ai-sdk/anthropic` [MÃ] — [plugin-openai/package.json](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-openai/package.json)
- Chất lượng: `plugins/plugin-slack/LICENSE` chứa JSON lỗi GitHub `{"message":"Not Found",...}` thay vì văn bản giấy phép [MÃ] — [plugin-slack/LICENSE](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/plugins/plugin-slack/LICENSE)
- README định vị: "elizaOS is an open-source TypeScript framework and product stack for autonomous AI agents... the Eliza app, the CLI, cloud services, native bridges" và phân phối Linux/Android trong `packages/os` [DOC] — [README.md](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/README.md)

**Chấm 12 tiêu chí — elizaOS (commit eb157cac, nhánh v2)**

| Tiêu chí | Điểm | Bằng chứng ngắn |
|---|---|---|
| R1 | Đạt [MÃ] | model plugin qua `@ai-sdk/*`; orchestrator ACP chỉ tùy chọn |
| R2 | Một phần [MÃ] | kiểu `Project{agents[]}` có; host v2 chạy `agents.list[0]`; đa agent ở cloud agent-server; không thấy cơ chế team/ủy quyền giữa agent eliza |
| R3 | Không [MÃ, tìm chưa thấy] | có planner gọi tool, plugin goals/todos; không có phân rã từ yêu cầu mơ hồ |
| R4 | Một phần [MÃ] | ApprovalService / PendingUserAction / `requiresConfirmation`; không có luồng review–làm lại |
| R5a | Đạt [MÃ] | ENTITIES provider (người trong phòng + sender), Room/World theo kênh |
| R5b | Đạt, nhưng theo từng agent [MÃ] | PrincipalService + IdentityClaim + merge/split; RelationshipsService union-find; entity UUID gắn `agentId` |
| R5c | Một phần [MÃ] | vai trò OWNER/ADMIN/MEMBER/GUEST theo World, thực thi ở action gate; chức danh/phòng ban chỉ có thể nhét vào `ContactInfo.customFields`/Component |
| R5d | Không [MÃ] | không có ủy quyền agent-agent mang người yêu cầu |
| R6 | Một phần [MÃ] | nhiều plugin kênh, thêm adapter bằng plugin (services/connectorSources); không có Zalo |
| R7 | Đạt [MÃ] | MIT |
| R8 | Đạt (chỉ beta) [MÃ git + npm] | tag `v2.0.3-beta.11` 2026-07-16; stable npm cuối 1.7.2 (2026-01-19) |
| R9 | Không [?] | không thấy |
| R10 | Không [?] | multi-tenant chỉ thấy trong Eliza Cloud (hosted) |
| R11 | Đạt [MÃ] | Plugin interface đầy đủ |
| R12 | Một phần [DOC/?] | docs site bị chặn, không kiểm được; sản phẩm đổi hướng liên tục |

### Inferences
- Mô hình định danh của elizaOS là tham chiếu tốt nhất để *thiết kế* lớp R5 (claim có mức xác minh, merge/split có nhật ký, vai trò theo world), nhưng không phải nền tốt cho "phòng ban nhiều agent": mỗi agent có không gian entity riêng nên một nhân viên nhắn cho 5 agent sẽ thành 5 entity khác nhau cần gộp lại.
- README/bài viết nói "runtime handles coordination" cho multi-agent, nhưng mã host v2 hiện tại chạy một agent; đây là độ vênh README-vs-code cần ghi nhận.
- Rủi ro lớn: stable npm dừng ở 1.7.2 (2026-01-19) trong khi `main` v2 thay đổi ~21k commit/3 tháng, định hướng "personal assistant / LifeOps / OS" chứ không phải doanh nghiệp.

### Gaps
- Không đọc được docs.elizaos.ai (proxy chặn) nên không xác nhận cách chạy nhiều agent trong một server ở bản 1.7.x.
- Chưa kiểm cơ chế liên lạc giữa agent (nếu có) trong cloud agent-server [?].
- Chưa kiểm plugin ngoài (registry) có Zalo hay không [?].

## 4. Agent Zero — ủy quyền phân cấp superior/subordinate, có phân rã việc mơ hồ không, đa người dùng, kênh chat, giấy phép, release

### Takeaway
Agent Zero (MIT, `v2.13` 2026-09-23) gọi model trực tiếp qua LiteLLM, có cây agent phân cấp thật (`call_subordinate` tạo `Agent(parent.number + 1)` trong context con riêng) và kênh Telegram/WhatsApp/email dạng plugin. Nhưng phân rã việc chỉ là chỉ dẫn prompt, không có đội/phòng ban, không có quy trình review, đăng nhập web là một cặp `AUTH_LOGIN/AUTH_PASSWORD` (đơn người dùng), và định danh người gửi chỉ là chuỗi "[Telegram message from {{sender}}]".

### Cited Findings
- R1: `models.py` import `litellm` [MÃ] — [models.py#L19-L30](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/models.py#L19-L30); plugin `_orchestrator` chỉ là skill hướng dẫn điều khiển CLI ngoài (Codex, Claude Code, Gemini CLI, Hermes…) — "There is intentionally no `terminal_agent` tool" [DOC] — [plugins/_orchestrator/README.md](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_orchestrator/README.md)
- Ủy quyền: class `Delegation(Tool)` [MÃ] — [tools/call_subordinate.py#L220](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/tools/call_subordinate.py#L220); "Every fresh child is `Agent(parent.number + 1, ...)` in its own persisted child-chat context"; profile được kiểm theo danh sách có sẵn [DOC trong repo] — [call_subordinate.py.dox.md](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/tools/call_subordinate.py.dox.md)
- Prompt: "always use specialized subordinate agents for specialized tasks matching their prompt profile"; "when a request calls for independent perspectives, challenges, or workstreams, delegate them to separate subordinates" [MÃ] — [prompts/agent.system.tool.call_sub.md#L1-L14](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/prompts/agent.system.tool.call_sub.md)
- Profile agent có sẵn: `agent0`, `default`, `developer`, `hacker`, `researcher`, `tiny-local` [MÃ] — [agents/](https://github.com/agent0ai/agent-zero/tree/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/agents)
- Plugin `_goal`: trạng thái goal `active|paused|complete|blocked`; `/goal auto` để agent tự tạo goal [DOC trong repo] — [plugins/_goal/AGENTS.md](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_goal/AGENTS.md)
- Telegram: "Each Telegram user gets a dedicated `AgentContext`"; ACL theo bot; nhóm có chế độ `mention|all|off` [DOC] — [plugins/_telegram_integration/README.md](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_telegram_integration/README.md); `_is_allowed(bot_cfg, user_id, username)` [MÃ] — [handler.py#L99-L133](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_telegram_integration/helpers/handler.py#L99); tin nhắn gói dạng `[Telegram message from {{sender}}] {{body}} [End Telegram message]` [MÃ] — [fw.telegram.user_message.md](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_telegram_integration/prompts/fw.telegram.user_message.md)
- Plugin khác: `_whatsapp_integration`, `_email_integration`, `_tool_access` (chính sách Allow/Block tool theo profile/project, "keeps delegated agents bound to their own effective scope") [MÃ/DOC] — [plugins/](https://github.com/agent0ai/agent-zero/tree/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins), [_tool_access/README.md](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_tool_access/README.md)
- Điểm mở rộng: thư mục `extensions/python/` có các hook `agent_init`, `system_prompt`, `message_loop_prompts_before/after`, `before_main_llm_call`, `tool_execute_before/after`, `monologue_start/end`, `util_model_call_before`… [MÃ] — [extensions/python](https://github.com/agent0ai/agent-zero/tree/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/extensions/python)
- Đăng nhập: `helpers/login.py` đọc một cặp `AUTH_LOGIN`/`AUTH_PASSWORD` từ dotenv [MÃ] — [helpers/login.py#L6-L14](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/helpers/login.py)
- Ảnh UI có sẵn: `docs/res/ui_screen2.png`, `docs/res/time-travel.png`, `docs/res/codex-screenshot.png` [MÃ] — [docs/res](https://github.com/agent0ai/agent-zero/tree/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/docs/res)
- Release: `v2.13` 2026-09-23, `v2.12` 2026-09-09, `v2.11` 2026-08-27, `v2.10` 2026-08-19 (git) [MÃ git] — [tags](https://github.com/agent0ai/agent-zero/tags)

**Chấm 12 tiêu chí — Agent Zero (commit e3051fb5)**

| Tiêu chí | Điểm | Bằng chứng ngắn |
|---|---|---|
| R1 | Đạt [MÃ] | LiteLLM; CLI ngoài chỉ qua skill tùy chọn |
| R2 | Một phần [MÃ] | profile + cây subordinate; không có team/phòng ban |
| R3 | Một phần [MÃ] | chỉ dẫn prompt "delegate… workstreams"; `_goal`; không có làm rõ/tiêu chí nghiệm thu |
| R4 | Không [MÃ, chưa thấy] | chỉ Allow/Block tool, `/steer` can thiệp; không có cổng duyệt/review |
| R5a | Một phần [MÃ] | chuỗi "Telegram message from <sender>"; không có khối ngữ cảnh chuẩn đa kênh |
| R5b | Không [MÃ] | context theo `(bot_name, tg_user_id)` |
| R5c | Không [MÃ] | chỉ allowlist; web một tài khoản |
| R5d | Không [?] | subordinate nhận message từ cha; chưa thấy metadata người yêu cầu |
| R6 | Một phần [MÃ] | Telegram, WhatsApp, email dạng plugin; thêm kênh bằng plugin khả thi; không có Zalo |
| R7 | Đạt [MÃ] | MIT |
| R8 | Đạt [MÃ git] | v2.13 2026-09-23 |
| R9 | Không | — |
| R10 | Không [MÃ] | một login |
| R11 | Đạt [MÃ] | plugins + extension hooks |
| R12 | Một phần [DOC] | docs tiếng Anh, có ảnh UI |

### Inferences
- Agent Zero hợp với "một người vận hành, một trợ lý mạnh có trợ lý con", không hợp với "phòng Marketing nhiều người, nhiều vai trò"; muốn dùng cần tự xây đa người dùng, định danh, review.
- Agent chạy trong Docker có quyền thực thi mã/terminal rộng → cần cô lập kỹ khi mở cho nhân viên/khách qua Telegram.

### Gaps
- Chưa kiểm cách context con truy ngược tới context gốc (để lấy `telegram_user_id`) — mới thấy `_is_child_context(...)` dựa trên "persisted parent context" [?].
- Chưa đọc `a2a_chat.py` (A2A giữa các instance) [?].

## 5. Eigent / CAMEL Workforce — phân rã việc + coordinator + gán worker trong mã; tự host với key riêng; kênh chat; giấy phép; release

### Takeaway
CAMEL Workforce có đủ vòng "task agent phân rã → coordinator gán worker → đánh giá chất lượng → retry/replan/decompose/reassign" trong mã, và có chế độ human-intervention; nhưng prompt phân rã yêu cầu "created without asking any questions" (không làm rõ). Eigent là app desktop Electron + backend FastAPI bọc Workforce, tự host được với model riêng; KHÔNG có kênh chat (chỉ có interface `IChannelAdapter`, "Concrete adapters (Slack/WhatsApp/etc.) are out of scope"), không có định danh người dùng; SSO/access control là tính năng Enterprise trả phí.

### Cited Findings
- `TASK_DECOMPOSE_PROMPT`: "As a Task Decomposer with the role of {role_name}, your objective is to divide the given task into subtasks... Ensure that the task plan is created without asking any questions." [MÃ] — [camel/tasks/task_prompt.py#L17-L33](https://github.com/camel-ai/camel/blob/fc27907e31ea2074d6b65ceb121573c5fa1ab345/camel/tasks/task_prompt.py#L17-L33)
- Workforce có `coordinator_agent` và `task_agent` tùy biến; `_decompose_task`, `_call_coordinator_for_assignment`, `_validate_assignments`, `_update_task_dependencies_from_assignments`, `_process_task_with_intervention` ("human intervention support") [MÃ] — [workforce.py#L193-L200](https://github.com/camel-ai/camel/blob/fc27907e31ea2074d6b65ceb121573c5fa1ab345/camel/societies/workforce/workforce.py#L193-L200), [#L1549](https://github.com/camel-ai/camel/blob/fc27907e31ea2074d6b65ceb121573c5fa1ab345/camel/societies/workforce/workforce.py#L1549), [#L2903](https://github.com/camel-ai/camel/blob/fc27907e31ea2074d6b65ceb121573c5fa1ab345/camel/societies/workforce/workforce.py#L2903), [#L3768-L4011](https://github.com/camel-ai/camel/blob/fc27907e31ea2074d6b65ceb121573c5fa1ab345/camel/societies/workforce/workforce.py#L3768)
- `TASK_ANALYSIS_PROMPT` chấm điểm chất lượng 0-100, "quality_score < 60 means quality is insufficient", chọn chiến lược khôi phục; `RecoveryStrategy` gồm `REPLAN`, `DECOMPOSE`, `REASSIGN` (và retry) [MÃ] — [workforce/prompts.py#L311-L360](https://github.com/camel-ai/camel/blob/fc27907e31ea2074d6b65ceb121573c5fa1ab345/camel/societies/workforce/prompts.py#L311), [workforce/utils.py#L211-L218](https://github.com/camel-ai/camel/blob/fc27907e31ea2074d6b65ceb121573c5fa1ab345/camel/societies/workforce/utils.py#L211)
- Eigent backend dùng `Workforce`/`ManagedWorkforce(options, execution, coordinator, planner, workers)` [MÃ] — [backend/app/utils/workforce.py#L178](https://github.com/eigent-ai/eigent/blob/3ec6f4c3c8794789fcf0abf5b572fa309a355b8a/backend/app/utils/workforce.py#L178), [managed_workforce.py#L80](https://github.com/eigent-ai/eigent/blob/3ec6f4c3c8794789fcf0abf5b572fa309a355b8a/backend/app/agent/factory/managed_workforce.py#L80)
- Kênh: `IChannelAdapter` chỉ là hợp đồng mở rộng: "This round defines the extension contract only. Concrete adapters (Slack/WhatsApp/etc.) are out of scope." [MÃ] — [backend/app/channels/interface.py#L17-L45](https://github.com/eigent-ai/eigent/blob/3ec6f4c3c8794789fcf0abf5b572fa309a355b8a/backend/app/channels/interface.py#L17-L45); Slack/Lark chỉ là toolkit (tool gọi ra) [MÃ] — [slack_toolkit.py](https://github.com/eigent-ai/eigent/blob/3ec6f4c3c8794789fcf0abf5b572fa309a355b8a/backend/app/agent/toolkit/slack_toolkit.py)
- README: "Local Deployment (Recommended)" với hướng dẫn `server/README_EN.md`; "Quick Start (Cloud-Connected)... requires account registration"; "Model Agnostic — Connect the models you already use—cloud APIs, enterprise gateways, or local inference"; Enterprise: "Exclusive Features (like SSO & custom development)" [DOC] — [README.md#L94-L186](https://github.com/eigent-ai/eigent/blob/3ec6f4c3c8794789fcf0abf5b572fa309a355b8a/README.md#L94)
- Release: Eigent `v1.0.5` 2026-09-25, `v1.0.4` 2026-09-05, `v1.0.0` 2026-06-17; CAMEL chỉ có alpha `v0.2.91a7` 2026-09-03, `v0.2.91a5` 2026-07-13 [MÃ git] — [eigent tags](https://github.com/eigent-ai/eigent/tags), [camel tags](https://github.com/camel-ai/camel/tags)
- Ảnh: README Eigent dùng ảnh host ngoài (`https://eigent-ai.github.io/.github/assets/head.png`, `opensource.png`) [DOC] — [README.md](https://github.com/eigent-ai/eigent/blob/3ec6f4c3c8794789fcf0abf5b572fa309a355b8a/README.md)

### Inferences
- CAMEL Workforce là "thư viện phân rã + đánh giá chất lượng" tốt nhất trong nhóm để *mượn ý tưởng/mã* cho R3/R4 (ví dụ nhúng vào một nền có kênh + định danh), nhưng không tự thân là nền tảng phòng ban: không có kênh chat, không có người dùng, không có vai trò.
- R3 vẫn chỉ "Một phần": thiếu bước làm rõ yêu cầu mơ hồ và tiêu chí nghiệm thu; quality check là LLM tự chấm.

### Gaps
- Chưa đọc `server/` của Eigent để xác nhận chế độ local không cần tài khoản cloud [?].
- Chưa kiểm Eigent có luồng duyệt của người (human approval) trong UI hay chỉ human-intervention của CAMEL [?].

## 6. Dify và Coze Studio — đa agent, tích hợp kênh chat, định danh end-user, giới hạn giấy phép, release

### Takeaway
Dify (1.17.1, 2026-09-10) là nền low-code workflow/agent rất sống động với node `agent_v2` và `human_input` (HITL), nhưng định danh chỉ là `EndUser` theo app (`external_user_id`, `name`, `session_id`), kênh chat nằm ở plugin marketplace/LangBot chứ không trong lõi, và giấy phép cấm vận hành multi-tenant + cấm sửa logo frontend. Coze Studio (open-source của ByteDance) đã chững: release cuối `v0.5.1` 2026-01-20; bản mở không có multi-agent/kênh (IDL có kiểu MultiAgent dùng chung với bản thương mại), docs trỏ về coze.cn.

### Cited Findings
- Dify `EndUser{tenant_id, app_id, type, external_user_id, name, is_anonymous, session_id}`; `EndUserType` = `app-deploy|browser|mcp|openapi|service-api|trigger` [MÃ] — [api/models/model.py#L2083-L2112](https://github.com/langgenius/dify/blob/725611b2e9a425519e9fcb4dcc579bafea936d27/api/models/model.py#L2083-L2112), [api/models/enums.py#L208-L219](https://github.com/langgenius/dify/blob/725611b2e9a425519e9fcb4dcc579bafea936d27/api/models/enums.py#L208)
- Node workflow gồm `agent`, `agent_v2` (có `ask_human_hitl.py`, `ask_human_resume.py`), `human_input`, `knowledge_retrieval`, `trigger_*` [MÃ] — [api/core/workflow/nodes](https://github.com/langgenius/dify/tree/725611b2e9a425519e9fcb4dcc579bafea936d27/api/core/workflow/nodes)
- Thư mục mới `dify-agent` ("Dify Agent hosts Agenton-composed Pydantic AI runs behind a FastAPI API") và `dify-agent-runtime` (Go, shellctl/PTY job runner) [DOC] — [dify-agent/docs/dify-agent/index.md](https://github.com/langgenius/dify/blob/725611b2e9a425519e9fcb4dcc579bafea936d27/dify-agent/docs/dify-agent/index.md), [dify-agent-runtime/README.md](https://github.com/langgenius/dify/blob/725611b2e9a425519e9fcb4dcc579bafea936d27/dify-agent-runtime/README.md)
- Kênh: plugin extension chính thức `slack_bot` (endpoint) trong `dify-official-plugins`; docs Dify hướng dẫn nối Slack/Lark/Discord/Telegram… qua LangBot [DOC] — [slack_bot README](https://github.com/langgenius/dify-official-plugins/blob/main/extensions/slack_bot/README.md), [docs.dify.ai LangBot](https://docs.dify.ai/en/learn-more/use-cases/connect-dify-to-various-im-platforms-by-using-langbot)
- Giấy phép Dify: xem trích nguyên văn ở mục 1 (cấm multi-tenant trừ khi có văn bản cho phép; cấm gỡ/sửa LOGO và copyright trong console/app khi dùng frontend `web/`; "appearance patent") [MÃ] — [LICENSE](https://github.com/langgenius/dify/blob/725611b2e9a425519e9fcb4dcc579bafea936d27/LICENSE)
- Coze Studio README "Feature list": Model service, Build agent, Build apps, Build a workflow, Develop resources, API and SDK; "certain features, such as tone customization, are limited to the commercial version" [DOC] — [README.md#L28-L36](https://github.com/coze-dev/coze-studio/blob/fefb05ff27be1da939612fbf9faf5db62583b8ae/README.md#L28-L36), [README.md#L86](https://github.com/coze-dev/coze-studio/blob/fefb05ff27be1da939612fbf9faf5db62583b8ae/README.md#L86)
- Coze Studio IDL có `MultiAgentSessionType_Flow/Host`, `ModelFuncConfigType_MultiAgentRecognize` (mã sinh từ IDL dùng chung) [MÃ] — [bot_common.go#L1199-L1203](https://github.com/coze-dev/coze-studio/blob/fefb05ff27be1da939612fbf9faf5db62583b8ae/backend/api/model/app/bot_common/bot_common.go#L1199-L1203)
- Coze Studio commit gần nhất: 2026-07-29 (infra), 2026-04-20 ("fix(plugin): oauth phishing"), 2026-04-09 (nonce OAuth) [MÃ git] — [commits](https://github.com/coze-dev/coze-studio/commits/main)
- Ảnh Dify trong repo: `images/describe.png`, `images/models.png`, `images/GitHub_README_if.png` [MÃ] — [dify/images](https://github.com/langgenius/dify/tree/725611b2e9a425519e9fcb4dcc579bafea936d27/images)

### Inferences
- Dify: R1 Đạt, R2 Một phần (nhiều app/agent nối bằng workflow, không có tổ chức agent), R3 Không (người thiết kế workflow), R4 Một phần (node human_input/HITL), R5 gần như Không (EndUser theo app, không vai trò), R6 Một phần (qua plugin/LangBot), R7 Đạt có điều kiện (nội bộ 1 workspace OK; multi-tenant và white-label cần giấy phép thương mại), R8 Đạt, R10 bị giấy phép chặn.
- Coze Studio: loại (R8 trượt, thiếu kênh/multi-agent ở bản mở, docs tiếng Trung là chính).

### Gaps
- Chưa kiểm Dify marketplace có plugin Zalo hay không [?].
- Chưa đọc sâu `agent_v2` để biết có gọi agent con/đa agent hay không [?].

## 7. Letta — định danh theo người dùng (identities API?), nhóm đa agent, kênh, giấy phép, release

### Takeaway
Repo `letta-ai/letta` (server V1 có Identities API và multi-agent groups) đã bị "nghỉ hưu" — mã đang phát triển chuyển sang `letta-ai/letta-code` (Apache-2.0, `v0.33.2` 2026-09-25), một "stateful agent harness" hướng cá nhân/coding với kênh Telegram/Slack/Discord/WhatsApp/Signal và plugin kênh tự viết tại `~/.letta/channels/<id>/`. Định danh trong letta-code chỉ là allowlist/admin tier theo biến môi trường; "acting user" chỉ có ý nghĩa với Letta Cloud.

### Cited Findings
- README repo cũ: "The current source code lives in `letta-ai/letta-code`... The `archive` branch contains the retired Letta V1 API server." [DOC] — [letta/README.md](https://github.com/letta-ai/letta/blob/5bcdd177d70fa2b31a754cfcd801e77b2e1ab16a/README.md)
- Letta Code README: "Letta Code is a stateful agent harness..."; bảng tính năng: Subagents & Multi-agent ("Agents can call any other agent (including themselves) as subagents"), Messaging Integrations (Slack, Telegram, browser, custom channels), Hooks, Permissions, Crons [DOC] — [letta-code/README.md](https://github.com/letta-ai/letta-code/blob/44b154e45384d2e38a8c503b33dc1695e7fd91dd/README.md)
- Kênh có sẵn trong mã: `src/channels/{telegram,slack,discord,whatsapp,signal,custom}`; plugin người dùng nạp từ `~/.letta/channels/<channel-id>/` với `channel.json` + `plugin.mjs` [MÃ/DOC] — [src/channels/README.md](https://github.com/letta-ai/letta-code/blob/44b154e45384d2e38a8c503b33dc1695e7fd91dd/src/channels/README.md)
- Kiểm soát truy cập: `LETTA_CHANNELS_ALLOWED_USERS`, `LETTA_CHANNELS_ADMIN_USERS`, `LETTA_CHANNELS_ALLOW_ALL_USERS`; "Modeled on the Hermes gateway's authorization layer" [MÃ] — [src/channels/access-control.ts#L1-L40](https://github.com/letta-ai/letta-code/blob/44b154e45384d2e38a8c503b33dc1695e7fd91dd/src/channels/access-control.ts)
- `X-Letta-Acting-User-Id`: cloud-api dùng để "re-attribute requests to the human who actually initiated them"; không có acting user ở "self-hosted / direct flows" [MÃ] — [src/agent/acting-user.ts#L1-L35](https://github.com/letta-ai/letta-code/blob/44b154e45384d2e38a8c503b33dc1695e7fd91dd/src/agent/acting-user.ts)
- R1: phụ thuộc `@earendil-works/pi-ai` ^0.87.1 và `openai` ^6.48.0; backend local `src/backend/local` [MÃ] — [package.json](https://github.com/letta-ai/letta-code/blob/44b154e45384d2e38a8c503b33dc1695e7fd91dd/package.json)
- Ảnh: `assets/letta-code-demo.gif`, `assets/tutor-profile.png` [MÃ] — [letta-code/assets](https://github.com/letta-ai/letta-code/tree/44b154e45384d2e38a8c503b33dc1695e7fd91dd/assets)

### Inferences
- Letta Code: R1 Đạt, R2 Một phần (subagent), R3 Không, R4 Một phần (permissions/approval cho tool), R5 yếu (5a có thể có qua channel adapter, 5b/5c/5d không), R6 Đạt (plugin kênh không sửa lõi — thêm Zalo khả thi), R7 Đạt, R8 Đạt. Hướng "một agent có bộ nhớ" hơn là "phòng ban".
- Identities API của Letta V1 (nếu cần) nằm trong mã đã nghỉ hưu → không nên xây mới trên đó.

### Gaps
- Chưa đọc mã adapter để xác nhận khối ngữ cảnh người gửi đưa vào prompt [?].
- Chưa kiểm nhánh `archive` của letta để trích Identities API [?].

## 8. CrewAI — hierarchical process / manager agent / planning; kênh; giấy phép; release

### Takeaway
CrewAI (MIT, `1.15.22` 2026-09-16) là thư viện Python, không phải nền tảng vận hành: có `Process.hierarchical` với `manager_llm`/`manager_agent`, `planning=True` (CrewPlanner), `human_input` trên Task và `@human_feedback` trong Flows; không có kênh chat, không có định danh người dùng; UI/giám sát nằm ở CrewAI AMP thương mại.

### Cited Findings
- `Process.sequential`, `Process.hierarchical` [MÃ] — [process.py#L9-L10](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/lib/crewai/src/crewai/process.py#L9-L10)
- `Crew`: "manager_llm: The language model that will run manager agent", "manager_agent: Custom agent that will be used as manager", "planning: Plan the crew execution and add the plan to the crew", `planning_llm` [MÃ] — [crew.py#L172-L199](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/lib/crewai/src/crewai/crew.py#L172-L199), [#L347-L351](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/lib/crewai/src/crewai/crew.py#L347-L351); `utilities/planning_handler.py` [MÃ]
- Ủy quyền giữa agent qua `DelegateWorkTool` [MÃ] — [agent_tools.py#L7-L28](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/lib/crewai/src/crewai/tools/agent_tools/agent_tools.py#L7-L28)
- Human-in-the-loop: `Task.human_input` [MÃ] — [task.py#L233](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/lib/crewai/src/crewai/task.py#L233); `def human_feedback(` trong Flows [MÃ] — [flow/human_feedback.py#L402](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/lib/crewai/src/crewai/flow/human_feedback.py#L402)
- Telemetry có cơ chế tắt `_is_telemetry_disabled()` [MÃ] — [telemetry.py#L100-L139](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/lib/crewai/src/crewai/telemetry/telemetry.py#L100-L139)
- README: "CrewAI AMP Suite adds managed deployment, observability, governance, security, and enterprise support" [DOC] — [README.md#L69](https://github.com/crewAIInc/crewAI/blob/4ed2abc7bbf504a634d3b733f2a97e0fbe8d44ec/README.md#L69)

### Inferences
- CrewAI: R1 Đạt, R2 Đạt ở mức thư viện (crew = đội), R3 Một phần (manager phân việc cho các Task đã định nghĩa trước; planning chỉ lập kế hoạch từng bước, không tự làm rõ yêu cầu mơ hồ), R4 Một phần (human_input/human_feedback), R5 Không, R6 Không, R7 Đạt, R8 Đạt, R9–R12 Không/không áp dụng (không có UI mở). Chỉ hợp làm "động cơ" bên trong một nền khác.

### Gaps
- Chưa đọc `planning_handler.py` chi tiết [?].

## 9. Lớp định danh (R5 5a–5d) không cần fork — phần có sẵn và điểm mở rộng cho từng nền tảng đã kiểm sâu

### Takeaway
OpenClaw là nơi dựng lớp định danh "không fork" khả thi nhất: plugin có thể đọc `senderId/channel/accountId` mỗi lượt, tra hồ sơ trong kho riêng (`openKeyedStore`), chèn "người này là ai, chức danh, được phép gì" qua `before_prompt_build` (kèm `toolsAllow`), chặn/đòi duyệt tool qua `before_tool_call`, và theo dõi quan hệ cha-con qua `subagent_spawned` để truyền "làm thay ai" cho agent con. elizaOS có sẵn nhiều hơn ở tầng dữ liệu (Principal/claim/merge, role theo world) nhưng định danh bị cắt theo từng agent và thiếu ủy quyền agent-agent. Agent Zero thiếu gần hết, chỉ có hook Python chung.

### Cited Findings

**OpenClaw — có sẵn**
- 5a: khối `Conversation info` + `inbound_meta.v2` [MÃ] — [inbound-meta.ts#L540-L660](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/auto-reply/reply/inbound-meta.ts#L540-L660)
- 5b (một phần): `session.identityLinks` (gộp khóa phiên DM) [MÃ] — [session-key.ts#L206-L301](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/routing/session-key.ts#L206-L301); `users.linkChannelIdentity` (gắn `{channelId, accountId, senderId}` → Gateway profile, chỉ dùng cho quyền owner) [MÃ] — [users-channel-identities.ts#L33](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/gateway/server-methods/users-channel-identities.ts#L33)
- 5c (một phần): `toolsBySender`, `commands.ownerAllowFrom`, `tools.elevated.allowFrom`, `gateway.roles` [MÃ] — [sender-tool-policy.ts#L25](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/agents/sender-tool-policy.ts#L25), [schema.help.core.ts#L145](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/config/schema.help.core.ts#L145)
- 5d (một phần): con có "Requester session"/"Requester channel"; chính sách tool của người yêu cầu được kế thừa [MÃ] — [subagent-system-prompt.ts#L118-L128](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/agents/subagents/spawn/subagent-system-prompt.ts#L118-L128), [requester-tool-policy.ts#L1-L5](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/agents/requester-tool-policy.ts#L1-L5)

**OpenClaw — điểm mở rộng (chữ ký thật)**
- `api.on<K extends PluginHookName>(hookName, handler, opts?)` [MÃ] — [plugin-api.types.ts#L472](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/plugin-api.types.ts#L472)
- `before_prompt_build(event: {prompt, currentUserMessage?, currentUserMessageId?, messages}, ctx: PluginHookAgentContext{agentId, sessionKey, channel, accountId, chatId, senderId, channelContext, inputProvenance,...}) → {systemPrompt?, prependContext?, appendContext?, toolsAllow?, prependSystemContext?, appendSystemContext?}` [MÃ] — [hook-before-agent-start.types.ts#L22-L51](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-before-agent-start.types.ts#L22-L51), [hook-types.ts#L274-L316](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-types.ts#L274-L316)
- `before_tool_call → {params?, block?, blockReason?, requireApproval?{title, description, severity, timeoutMs, allowedDecisions, onResolution}}` [MÃ] — [hook-before-tool-call-result.ts#L14-L35](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-before-tool-call-result.ts#L14-L35)
- `subagent_spawned(event: {childSessionKey, agentId, label?, mode, requester?{channel, accountId, to, threadId, channelId, messageId}, runId, ...}, ctx: {runId?, childSessionKey?, requesterSessionKey?})` [MÃ] — [hook-types.ts#L769-L831](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/hook-types.ts#L769-L831)
- `api.runtime.state.openKeyedStore<T>(options: OpenAsyncKeyedStoreOptions): PluginStateKeyedStore<T>` [MÃ] — [runtime/types-core.ts#L520-L522](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/runtime/types-core.ts#L520-L522)
- `api.registerTool(tool | factory, opts?)`, `api.registerGatewayMethod(...)`, `api.registerHttpRoute(params)`, `api.registerTrustedToolPolicy(policy)` (plugin cài đặt phải khai báo id trong `contracts.trustedToolPolicies`), `api.registerChannel(registration | ChannelPlugin)`, `api.registerControlUiDescriptor(...)` [MÃ] — [plugin-api.types.ts#L214-L383](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/src/plugins/plugin-api.types.ts#L214-L383)
- Điều kiện cấu hình: `plugins.entries.<id>.hooks.allowConversationAccess: true` và không đặt `allowPromptInjection: false` [DOC] — [docs/plugins/hooks.md#L131-L182](https://github.com/openclaw/openclaw/blob/96e4061553977c4434544b3f45059035d048fe3c/docs/plugins/hooks.md#L131)

**elizaOS — có sẵn và điểm mở rộng**
- Có sẵn: 5a (ENTITIES provider), 5b (PrincipalService/IdentityClaim/merge; RelationshipsService cluster), 5c một phần (Role theo World + `roleGate` ở action/provider/context), 5d không [MÃ] — xem mục 3.
- Điểm mở rộng: `Plugin.providers: Provider[]` (provider động mỗi lượt, cần `contexts`/`contextGate` hoặc `alwaysInResponseState` để lên planner) [MÃ] — [types/components.ts#L858-L912](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/components.ts#L858); `Plugin.componentTypes: ComponentTypeDefinition[]` + `runtime.createComponent(component)` để gắn "hồ sơ công việc" vào Entity [MÃ] — [types/plugin.ts#L65-L69](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/plugin.ts#L65-L69), [types/runtime.ts#L1456](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/runtime.ts#L1456); `Action.roleGate`/`contextGate` [MÃ] — [types/plugin.ts#L648](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/plugin.ts#L648); `PrincipalService.resolveCanonicalPrincipal(...)` [MÃ] — [types/identity.ts#L434-L440](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/identity.ts#L434); `runtime.updateWorld(world)` để ghi `metadata.roles` [MÃ] — [types/runtime.ts#L1396](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/runtime.ts#L1396); `Plugin.services`, `Plugin.events`, `Plugin.evaluators` [MÃ] — [types/plugin.ts#L1195-L1260](https://github.com/elizaOS/eliza/blob/eb157cac4767dfc0268f6995e09de109d8468ff8/packages/core/src/types/plugin.ts#L1195)

**Agent Zero — có sẵn và điểm mở rộng**
- Có sẵn: 5a một phần (tên người gửi Telegram trong message) [MÃ] — [fw.telegram.user_message.md](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_telegram_integration/prompts/fw.telegram.user_message.md); plugin Telegram lưu `telegram_user_id` trong `context.data` (`CTX_TG_USER_ID`) [MÃ] — [constants.py#L10](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_telegram_integration/helpers/constants.py#L10)
- Điểm mở rộng: class `Extension.execute(system_prompt: list[str], loop_data: LoopData, **kwargs)` trong `extensions/python/system_prompt/` (ví dụ plugin Telegram tự chèn prompt) [MÃ] — [_20_telegram_context.py](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_telegram_integration/extensions/python/system_prompt/_20_telegram_context.py); hook `tool_execute_before` (plugin `_tool_access` dùng để thực thi chính sách) [MÃ] — [_tool_access/extensions/python/tool_execute_before/_10_enforce_tool_policy.py](https://github.com/agent0ai/agent-zero/blob/e3051fb584b1a36be2b0a0c90606f1c2c2d356ec/plugins/_tool_access/extensions/python/tool_execute_before/_10_enforce_tool_policy.py)

### Inferences
- **OpenClaw — thiết kế plugin "org-identity" không fork (khả thi, cần kiểm thử):**
  1. Kho hồ sơ: `openKeyedStore` với khóa `person:<id>` → `{tên, chức danh, phòng ban, vai trò (boss/staff/customer), quyền yêu cầu, danh sách claim kênh}` và khóa `claim:<channel>:<accountId>:<senderId>` → `person:<id>`. Quản trị qua `registerGatewayMethod`/`registerHttpRoute` (+ `registerControlUiDescriptor` nếu cần UI). Có thể đồng bộ thêm với `users.linkChannelIdentity` để người admin được quyền owner trong kênh.
  2. 5a/5b/5c mỗi lượt: `api.on("before_prompt_build")` đọc `ctx.channel/accountId/senderId` → tra claim → trả `prependContext` ("Người đang nhắn: Nguyễn A — Trưởng phòng Marketing — vai trò: boss — được yêu cầu: ngân sách ≤ X") và `toolsAllow` thu hẹp tool theo vai trò. Người lạ → "customer" mặc định.
  3. 5c cưỡng chế: `api.on("before_tool_call")` → `block` hoặc `requireApproval` (ví dụ nhân viên yêu cầu chi tiền/đăng bài → cần boss duyệt); hoặc `registerTrustedToolPolicy`. Bổ sung `toolsBySender` trong config cho lớp phòng thủ tĩnh.
  4. 5d: `api.on("subagent_spawned")` ghi `childSessionKey → person` (lấy từ bản ghi của `requesterSessionKey`, đã lưu ở bước 2) → trong `before_prompt_build` của con, tra `ctx.sessionKey` để chèn "đang làm thay mặt: …". Rủi ro: thứ tự hook (xem Gaps mục 2) và các đường spawn ACP/Codex có thể không đi qua cùng hook.
  5. Hạn chế còn lại: hồ sơ không hiện ở UI "People" gốc; phiên nhóm vẫn chung khóa phiên theo nhóm (đúng mong muốn), còn DM đa kênh nên bật `dmScope: "per-peer"` + `identityLinks` để lịch sử hội thoại cũng hợp nhất.
- **elizaOS — không fork nhưng tốn công hơn:** dùng provider + componentTypes + roleGate + PrincipalService là đủ cho 5a–5c trong phạm vi một agent; để nhiều agent chia sẻ một hồ sơ phải tự viết service đồng bộ Principal giữa các agent (vì `agentId` nằm trong khóa), và 5d phải tự dựng cơ chế ủy quyền agent-agent (hiện không có).
- **Agent Zero — gần như phải tự xây từ đầu:** extension `system_prompt` có thể đọc `context.data["telegram_user_id"]` để chèn hồ sơ; `tool_execute_before` để chặn; nhưng không có kho hồ sơ, không có đa người dùng web, không có hợp nhất kênh, và việc truyền người yêu cầu cho subordinate phải tự dò context cha.

### Gaps
- Chưa có thử nghiệm [CHẠY] nào chứng minh plugin OpenClaw nói trên hoạt động (đặc biệt `allowPromptInjection`, thứ tự `subagent_spawned` so với lượt đầu của con, và đường spawn ACP).
- Chưa kiểm elizaOS có hook nào tương đương `before_tool_call` với trạng thái "chờ duyệt" gắn với vai trò hay không, ngoài `requiresConfirmation`/ApprovalService [?].
- Chưa kiểm plugin kênh Zalo nào tồn tại cho elizaOS/Agent Zero/Letta ngoài OpenClaw [?].
