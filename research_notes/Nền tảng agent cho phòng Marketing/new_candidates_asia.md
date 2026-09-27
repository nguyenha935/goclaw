# Ứng viên mới từ cộng đồng Trung / Nhật / Hàn / Việt: nền tảng "công ty AI / nhân viên số" (kiểm chứng từ mã nguồn)

Ngày làm: 2026-09-27 (đã xác nhận bằng `date`: `Sun Sep 27 03:41:53 UTC 2026`). Mọi repo đều được `git clone --filter=blob:none` vào scratchpad, đọc mã thật, rồi xoá. Quy ước nhãn: [MÃ] đã đọc mã nguồn, [CHẠY] đã cài và chạy (lần này **không** có mục nào được cài/chạy), [DOC] chỉ đọc tài liệu/README/trang web, [?] chưa kiểm chứng. Số sao lấy từ trang GitHub qua WebFetch ngày 2026-09-27 (khoảng, có thể lệch). Ngày tháng lấy từ git (`git log -1 --format=%cI`, `git for-each-ref ... refs/tags`).

Giới hạn công cụ (ảnh hưởng độ phủ): proxy chặn zhuanlan.zhihu.com, qiita.com, news.hada.io, 80aj.com, gleamhub.net, openvort.com và **gitee.com** (git qua HTTPS bị `CONNECT tunnel failed, response 403`), nên với các trang này chỉ dùng được đoạn trích của kết quả tìm kiếm. PyPI thì vào được.

---

## Câu hỏi 1: Cộng đồng châu Á đang bàn về những dự án nào mà nguồn tiếng Anh bỏ sót? (khám phá + sàng lọc)

### Takeaway
Cộng đồng tiếng Trung sinh ra rất nhiều dự án "数字员工 / AI 员工 / 一人公司 (OPC)", nhưng phần lớn hoặc còn non (1–90 commit, 0–25 sao, không có LICENSE), hoặc dùng Claude Code/Codex/OpenClaw làm bộ thực thi. Ứng viên mới đáng chú ý nhất cho R5 là **OpenVort** (AGPL-3.0): mô hình danh bạ thật `Member` ↔ `PlatformIdentity` ↔ `Department` ↔ `ReportingRelation`, đồng bộ danh bạ WeCom/DingTalk/Feishu và gộp danh tính xuyên kênh. Nhưng bản phát hành cuối trên GitHub là 2026-04-27, nên trượt R8. Trong danh sách "đã liếc qua", **AgentTeams (HiClaw)** là mạnh nhất: có CRD `Human` với `PermissionLevel` và `AccessibleTeams`, có Team Leader làm rõ yêu cầu và viết tiêu chí nghiệm thu, và phát hành v1.2.4 ngày 2026-09-21. Cộng đồng Hàn và Nhật chủ yếu khuếch đại lại các dự án tiếng Anh đã bị loại (Paperclip, multica, OpenClaw). Ở cộng đồng Việt chỉ có thành phần kết nối Zalo, không có nền tảng tổ chức nào.

### Cited Findings

**A. Ứng viên MỚI (không nằm trong danh sách loại trừ hay danh sách "đã liếc qua"). Mỗi mục một đoạn sàng lọc.**

1. **OpenVort**, repo `openvort/openvort` (TQ). Tìm thấy qua tìm kiếm "github AI 员工 平台 开源 企业微信 钉钉 飞书 部门 权限" ([GitHub](https://github.com/openvort/openvort), [bản mirror trên AtomGit](https://gitcode.com/gh_mirrors/op/openvort)). Đây là "nền tảng AI 员工 mã nguồn mở": nhân viên AI là `Member.is_virtual` gắn với `post` (vị trí) và skills, làm việc cùng người thật trong WeCom/DingTalk/Feishu. Backend Python/FastAPI, UI Vue 3. Tự gọi API Anthropic, OpenAI-compatible và OpenAI Responses [MÃ]. Có sẵn mô hình danh bạ, phòng ban, quan hệ báo cáo và đồng bộ danh bạ IM [MÃ]. Giấy phép AGPL-3.0. Khoảng 436★, 73 fork (2026-09-27). Rủi ro:
   - Bản cuối v0.13.0 ngày 2026-04-27, commit `7beee90`. Cả 22 commit trên GitHub đều là snapshot "release: vX", tức GitHub chỉ là nơi đẩy bản phát hành, còn nơi phát triển thật không thấy được. Không truy cập được Gitee.
   - README ghi `pip install openvort`, nhưng PyPI trả 404 cho `openvort`. README và thực tế lệch nhau.
   - Tài liệu gần như chỉ có tiếng Trung.
   - Hướng tới đội phần mềm (Gitee, Jenkins, Zentao).

   **Chấm sâu ở Câu hỏi 2.**
2. **Agency Orchestrator**, repo `jnMetaCode/agency-orchestrator` (TQ). Tìm thấy qua [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh) ("277 vai chuyên gia, 20 bộ phận") và đoạn trích Zhihu "180名AI员工，分布于 17 个部门" ([Zhihu](https://zhuanlan.zhihu.com/p/2018323825935262516), bị chặn nên không đọc được, chưa xác định bài nói về repo nào [?]).
   - Từ một câu yêu cầu, hệ thống tự lập nhóm vai và sinh DAG YAML. Có tiêu chí nghiệm thu được kiểm tự động kèm một vòng làm lại, và có bước `approval` do người ký.
   - Gọi API trực tiếp qua 20+ nhà cung cấp; CLI như Claude Code/Codex chỉ là tuỳ chọn [MÃ].
   - Công cụ một người dùng, không có kênh chat vào.
   - Apache-2.0, khoảng 2.3k★, 305 fork. Tag v0.19.2 ngày 2026-09-06, commit cuối 2026-09-25 [MÃ].

   **Chấm sâu.**
3. **opc-web**, repo `wenbuer/opc-web` (TQ, chủ đề OPC 一人公司). Tìm thấy qua tìm kiếm "一人公司 OPC 智能体 开源 github" ([GitHub](https://github.com/wenbuer/opc-web)).
   - Bàn điều khiển cục bộ: R0 là người, R1 là trợ lý tách việc và gom báo cáo, RX là các vai thực thi. Có bàn duyệt (批阅台) để duyệt, bác, hoặc sửa rồi làm lại.
   - Gọi `/chat/completions` bằng urllib, không cần CLI; DeepSeek Harness chỉ là tuỳ chọn [MÃ].
   - Chỉ nghe 127.0.0.1, không có kênh chat.
   - MIT, khoảng 6★. Tag v1.18.0 ngày 2026-09-20, nhưng lịch sử git chỉ bắt đầu từ 2026-09-14 (18 commit).

   **Chấm sâu.**
4. **zalo-agent**, repo `vuhai2002/zalo-agent` (VN). Tìm thấy qua tìm kiếm "nền tảng AI agent mã nguồn mở zalo tự host" và [kết quả Viblo](https://viblo.asia/p/vuot-xa-openclaw-5-giai-phap-thay-the-ai-agent-ma-nguon-mo-an-toan-va-hieu-qua-ZjJYWoN6VOE).
   - Agent tự host sống trong Zalo cá nhân (thư viện zca-js không chính thức) và Zalo Bot API chính thức. Hỗ trợ nhiều tài khoản, mỗi tài khoản một "não" riêng; có dashboard, 15 tool và MCP.
   - Tài liệu tiếng Việt là chính.
   - MIT, khoảng 5★. Tag v0.3.1 ngày 2026-08-30, commit cuối cũng 2026-08-30 [MÃ].
   - Mã nguồn có chú thích nhắc tới goclaw và Hermes (`src/agent/user-message-line.ts`) [MÃ].
   - Không phải nền tảng tổ chức.

   **Chấm sâu, như một thành phần Zalo.**
5. **UMI**, repo `huang1119/UMI` (TQ, "多agent电商数字员工平台"). Tìm thấy qua tìm kiếm "数字员工 开源 钉钉 企业微信 通讯录 同步" ([GitHub](https://github.com/huang1119/UMI)).
   - Nền tảng nhân viên số cho thương mại điện tử (CSKH, vận hành, marketing, chọn hàng). Hỗ trợ Feishu, Telegram, QQ, DingTalk, WeChat, Discord, WhatsApp. Có ma trận quyền (`docs/ACL-MATRIX.md`: admin, owner workspace, `owner_im_id`) [MÃ].
   - Bộ thực thi là SDK `@earendil-works/pi-coding-agent` (Pi coding agent) nhúng trong container `container/agent-runner/src/runtime/pi/pi-runtime.ts` [MÃ]. Nó gọi mô hình bằng key của người dùng, nhưng vẫn là một coding-agent của bên thứ ba.
   - Chỉ có **1 commit** (2026-09-23), `package.json` tên "miniclaw". Upstream `helsome/miniclaw` riêng tư hoặc không tồn tại (git đòi đăng nhập). 0★.

   Rủi ro rất cao. Chỉ sàng lọc, không chấm sâu.
6. **GuSheng107/digital-employee** (TQ). Tìm thấy cùng tìm kiếm với UMI ([GitHub](https://github.com/GuSheng107/digital-employee)).
   - Gateway Feishu/WeCom, `backend-auth` (người dùng, vai trò, menu, quyền), `backend-agent` gọi mô hình qua LiteLLM [MÃ].
   - Gateway **chưa nối với agent**: `backend-gateway/src/core/hub.py:82,180` gọi `_mock_agent_process` [MÃ]. Danh tính trong hệ chỉ là tài khoản quản trị, không ánh xạ người gửi IM thành nhân viên.
   - Đổi giấy phép từ MIT sang AGPL-3.0 ngày 2026-08-27 (commit `856ca02`). Khoảng 22★. Commit cuối 2026-09-23.

   Còn quá sớm.
7. **Lianjifu/digital-employee-platform** (TQ, "数字工作伙伴平台"). Backend Go, có `internal/feishu`, `dingtalk`, `wecom`, `weixin`, `policy`, `deworkflow` [MÃ].
   - **Không có tệp LICENSE** ở gốc repo (chỉ có LICENSE của các skill bên thứ ba) [MÃ]. Trang GitHub cũng hiện "License: None", 0★ ([GitHub](https://github.com/Lianjifu/digital-employee-platform)). Như vậy mặc định là "giữ mọi quyền", **trượt R7**.
   - Commit cuối 2026-09-19, tag `20260817`.
8. **KDevSec/digital-employees** (TQ, "数字员工套件2.0"). Tìm thấy qua tìm kiếm "数字员工 开源 飞书 组织架构".
   - Gồm Keycloak, nền tảng quản lý và workbench. Engine gọi một "底座 CLI" để thực thi (`workbench/workbench-engine/src/r1/ledger.ts:122`) và mang skill/hook kiểu Claude Code (`templates/*/skills/*`) [MÃ].
   - **Không có LICENSE**. Commit cuối 2026-08-28, đang ở giai đoạn V0.1.

   Trượt R1 (có thể) và R7.
9. **lp7915/digital-workforce** (TQ). Nhân viên số làm việc trong nhóm Feishu với "bộ nhớ dự án", có kịch bản marketing ADA (phân tích nghệ sĩ, độ hợp thương hiệu, tổng kết chiến dịch).
   - Vòng lặp agent chạy trên **Volcengine Ark Managed Agents** (`https://ark.cn-beijing.volces.com/api/v3`) [MÃ], tức là nằm trên cloud của ByteDance chứ không phải trên máy mình. Vì vậy R1 chỉ đạt một phần và việc tự host không trọn vẹn.
   - Chỉ chạy trên 127.0.0.1, không có LICENSE. Lịch sử bắt đầu từ 2026-09-20.
10. **OpenOcta**, repo `openocta/openocta` (TQ). Được giới thiệu là "OpenClaw 替代" trên CSDN và NetEase ([CSDN](https://blog.csdn.net/Databuff/article/details/162868352), [163.com](https://www.163.com/dy/article/KR9KGP630556L3O4.html)).
    - Ở phiên bản hiện tại đây là **agent AIOps trên desktop**, một tệp Go duy nhất. Có WeCom/DingTalk/Feishu, hàng đợi phê duyệt và nhật ký kiểm toán. Không phải nền tảng tổ chức.
    - **Giấy phép không nhất quán**: README ghi Apache-2.0 (dòng 17 và 458), nhưng tệp `LICENSE` là **GPLv3**, được thay ngày 2026-09-16 (commit `0c7dac2` "Add LICENSE file") [MÃ].
    - Khoảng 3.2k★. Tag v1.0.9 ngày 2026-09-09.
11. **Easy Agent Team**, repo `othorizon/easy-agent-team` (TQ, được nhắc trên V2EX và 80aj). Phân phối skill, cấu hình MCP, biến môi trường và quyền theo vai cho Claude Code và các client cục bộ. Nền tảng tự nó **không chạy agent**, nên trượt R1. Khoảng 10★ [DOC] ([GitHub](https://github.com/othorizon/easy-agent-team)).
12. **Golutra**, repo `golutra/golutra` (TQ, từng livestream "24 小时运行 AI 公司" trên V2EX). Biến Codex/Claude Code/OpenClaw thành "hệ thống agent thống nhất", nên trượt R1 [DOC] ([V2EX](https://v2ex.com/t/1201156), [GitHub](https://github.com/golutra/golutra)).
13. **OpenCrew**, repo `AlexAnys/opencrew` (TQ, được báo Nhật GH Media đưa tin). Là lớp cấu hình trên OpenClaw theo mô hình kênh Slack = vai, thread = việc. Phụ thuộc OpenClaw, không có backend riêng, khoảng 495★ [DOC] ([GitHub](https://github.com/AlexAnys/opencrew)).
14. **multi-agent-shogun**, repo `yohey-w/multi-agent-shogun` (Nhật, Zenn). Điều khiển 10 coding CLI (Claude Code, Codex, ...) qua tmux theo cấp bậc "shogun/karo". **Trượt R1** (`shutsujin_departure.sh:8-10,98-99`) [MÃ]. Tag v5.2.0 ngày 2026-06-06, commit cuối 2026-08-06. README cho biết chính tác giả đã giải tán "đội 10 agent" để chuyển sang dự án kagemusha ([Zenn](https://zenn.dev/ai_jidoka_lab/articles/zenn_intro_overview)).
15. **OpenCarrier**, repo `yinnho/opencarrier` (TQ, Rust, "AI 分身"). Là trợ lý cá nhân quét mã để dùng qua WeChat/WeCom/Feishu/DingTalk, không phải nền tảng tổ chức. README ghi MIT nhưng repo **không có tệp LICENSE** [MÃ]. Khoảng 5★. Tag v0.3.0 ngày 2026-05-06, commit cuối 2026-08-25.
16. **abs-zalo-bot**, repo `teddiesloco/abs-zalo-bot` (VN). **Bộ chuyển tiếp Zalo** (Zalo cá nhân qua QR và Zalo OA qua webhook có HMAC) được đóng gói thành **MCP server** cho Hermes/Claude Code/Codex; có `hermes-plugin/`. MIT, khoảng 23★. Tag git cuối v0.8.1 ngày 2026-09-13, CHANGELOG ghi v0.9.2 ngày 2026-09-22 [MÃ]. Là một thành phần, không phải nền tảng.
17. Chỉ thấy trong kết quả tìm kiếm, chưa clone [?]:
    - **Rovai AI**: cấu hình Claude/Codex làm "đồng đội", nên có thể trượt R1 ([V2EX](https://www.v2ex.com/t/1238939)).
    - **Agents Chat** và **Agents Anywhere**: xoay quanh các coding agent ACP ([V2EX](https://www.v2ex.com/t/1229617)).
    - **ClawTeam** (HKUDS): leader sinh ra các worker ([GeekNews](https://news.hada.io/topic?id=27609)).
    - **OCMS**, repo `Salt05/OCMS`: CRM Zalo nhiều tài khoản ([GitHub](https://github.com/Salt05/OCMS)).

**B. Sàng lọc lại các dự án gốc Trung Quốc từng "liếc qua" (mỗi dự án một dòng: repo · giấy phép · backend riêng? · bản phát hành cuối · tín hiệu R3/R5)**

- **EDICT**, repo `cft0808/edict` · MIT · **Không** có backend riêng: `edict/backend/app/workers/dispatch_worker.py:429,542` gọi CLI `openclaw agent` [MÃ] · không có tag, commit cuối **2026-05-06** nên trượt R8 · R3/R4 có bậc "Môn hạ tỉnh" duyệt bắt buộc [DOC], R5 không có · khoảng 16.9k★.
- **AgentTeams (HiClaw)**, repo `agentscope-ai/AgentTeams` (URL cũ `alibaba/hiclaw` tự chuyển hướng) · Apache-2.0 · Có backend: worker chạy runtime QwenPaw/OpenClaw/Hermes/CoPaw/DeepSeek-Harness và gọi mô hình qua Higress bằng key của mình · tag **v1.2.4 ngày 2026-09-21** · R3 mạnh (Leader phải làm rõ yêu cầu và viết tiêu chí nghiệm thu), R5 một phần (CRD `Human` có `permissionLevel`) · khoảng 5.7k★. **Đã kiểm sâu, xem Câu hỏi 2.**
- **QwenPaw** (trước là CoPaw), repo `agentscope-ai/QwenPaw` · Apache-2.0 · Có backend · tag v2.2.2-beta.3 ngày 2026-09-20, bản ổn định v2.2.1 ngày 2026-09-11 · là **trợ lý cá nhân**. R5 chỉ có ACL theo kênh (`app/channels/access_control.py:74 UserInfo(remark, username)`). R6 tốt: kênh do plugin đăng ký (`app/channels/registry.py`, `_get_plugin_channels`) [MÃ] · khoảng 35.3k★.
- **CowAgent**, repo `zhayujie/CowAgent` (trước là chatgpt-on-wechat) · MIT · Có backend · bản 2.1.9 ngày 2026-09-14 · có đội multi-agent trong một hội thoại chung (`agent/team.py`, `agent/multiagent/`), nhưng hướng một người dùng (một tệp `USER.md`) nên R5 yếu · khoảng 47.1k★.
- **JiuwenSwarm**, repo `openJiuwen-ai/jiuwenswarm` (Huawei openJiuwen) · Apache-2.0 · Có backend (OpenAI-compatible, Huawei MaaS) · tag **v0.2.7.beta1 ngày 2026-09-22** (trang GitHub lại hiện v0.2.4.beta3 là "latest release", không khớp) · R3 có Leader tách việc, nhưng logic nằm trong `openjiuwen` agent-core lấy từ gitcode [?]. R5 yếu (tên người gửi Feishu lấy qua contact API) · khoảng 6k★. Đã kiểm vừa phải.
- **UniEmployee**, repo `zj-unicom-ai/UniEmployee` (China Unicom Chiết Giang) · MIT · Có backend · tag **v0.20.0 ngày 2026-09-24** · R4 tốt (HITL ở mức tool). R5 một phần: OIDC ánh xạ department thành org, người gửi IM thành `im:{channel}:{sender}`. R6 hiện chỉ có webhook chung; README nói adapter WeCom/Feishu/DingTalk riêng "đang trong lộ trình" · khoảng 277★. Đã kiểm vừa phải.
- **Wegent**, repo `wecode-ai/Wegent` · Apache-2.0 · Một phần: có đường native `chat_shell/` (Python), còn desktop và executor Rust dựa trên **Codex** · tag v2.0.21 ngày 2026-09-17, nhánh wework-v0.5.6-beta.3 ngày 2026-09-27 · R5 có tín hiệu: `backend/app/services/channels/handler.py:111 UserMappingConfig` với chế độ `select_user` / `staff_id` / `email`; `dingtalk/user_resolver.py:64` ghép người gửi DingTalk với người dùng Wegent qua email hoặc staff_id [MÃ] · khoảng 862★. Hướng tới công việc lập trình.
- **OPC-Nexus**, repo `h4dex/opc-nexus` · MIT · Một phần: lõi điều phối là **Hermes Runtime** (bản fork của Hermes Agent, dự án đã bị loại); worker là Codex/Claude Code/Pi/Hermes · tag v2.0.1 ngày 2026-08-24, commit cuối 2026-09-04 · R3/R4 mạnh theo README (làm rõ yêu cầu, lên kế hoạch, duyệt, giao việc, nghiệm thu) [DOC]. Chỉ có bản desktop Electron (Windows/Ubuntu), không có server · khoảng 240★.
- **Clawith Cloud** là bản SaaS có host của Clawith (dự án đã loại) tại cloud.clawith.ai. Không tự host được, không có gì mới ([search](https://clawith.ai/)) [DOC].

**C. Cộng đồng Nhật, Hàn, Việt**
- GeekNews (Hàn) chủ yếu đăng lại OpenClaw, multica, ClawTeam, Paperclip ([GeekNews OpenClaw](https://news.hada.io/topic?id=26914), [multica](https://news.hada.io/topic?id=28399), [ClawTeam](https://news.hada.io/topic?id=27609)); dev.to tiếng Hàn và SOTAAZ viết về Paperclip ([dev.to](https://dev.to/_53fb7c03dd741a6124e4e/ai-eijeonteu-20gaereul-hoesaceoreom-gulrineun-opeunsoseu-paperclip-2j1m)). Không tìm thấy dự án gốc Hàn nào có backend riêng.
- Zenn và Qiita (Nhật) chủ yếu viết về "AI社員" dựng trên OpenClaw + Slack, cùng multi-agent-shogun (Claude Code) ([Zenn OpenClaw AI社員](https://zenn.dev/quick119/articles/5ca9177fe04044), [Zenn NTT Data](https://zenn.dev/nttdata_tech/articles/bf6b694144e55a)). Không tìm thấy nền tảng gốc Nhật nào đạt R1.
- Việt Nam: Znews/Baomoi đưa tin Zalo đổi cách kết nối với OpenClaw ([Znews](https://znews.vn/zalo-cap-nhat-phuong-thuc-ket-noi-den-openclaw-post1664688.html)). Mã nguồn mở của VN chủ yếu là thành phần Zalo (zalo-agent, abs-zalo-bot, zalo-bot-template, OCMS) ([GitHub topic zalo-bot](https://github.com/topics/zalo-bot)).

### Inferences
- "AI 员工 / 数字员工" ở TQ thường đi theo hướng HR/doanh nghiệp: SOP, phê duyệt, kiểm toán, danh bạ. Tuy vậy chỉ OpenVort thực sự mô hình hoá **người thật** trong danh bạ (phòng ban, chức vụ, quan hệ báo cáo, danh tính trên nhiều nền tảng). Các dự án còn lại chủ yếu mô hình hoá "nhân viên AI".
- Nhiều dự án mới ở TQ không có LICENSE, hoặc README và LICENSE mâu thuẫn (Lianjifu, KDevSec, lp7915, OpenCarrier, OpenOcta). Với khách hàng doanh nghiệp, phải kiểm tệp LICENSE thật chứ không tin huy hiệu trên README.
- Không có ứng viên nào có sẵn kết nối Zalo *và* mô hình tổ chức. Đường khả thi là ghép một nền tảng có R5 tốt với một bộ chuyển tiếp Zalo (zalo-agent hoặc abs-zalo-bot làm tham chiếu).

### Gaps
- Không đọc được Zhihu, Qiita, GeekNews, 80aj, gleamhub và Gitee (proxy chặn). Có thể còn dự án chỉ công bố trên Gitee mà tôi không thấy được.
- Không có số sao cho KDevSec, lp7915, golutra; số sao của OpenCrew (495) chỉ lấy từ đoạn trích tìm kiếm.
- Chưa xác định được bài Zhihu "180名AI员工/17个部门" nói về repo nào.

---

## Câu hỏi 2: Kiểm sâu từ mã nguồn (chấm đủ 12 tiêu chí)

### Takeaway
Trong các ứng viên mới, **OpenVort** là dự án duy nhất đạt gần trọn R5 (5a, 5b, 5c) từ mã. Nhưng nó trượt R8 (bản cuối 2026-04-27) và không đa tenant. **Agency Orchestrator** và **opc-web** mạnh về R3/R4 (tách việc, tiêu chí nghiệm thu, làm lại, cổng người duyệt) nhưng không có danh tính và kênh chat. **zalo-agent** là thành phần Zalo tốt, không phải nền tảng tổ chức. Ở danh sách cũ, **AgentTeams** nổi bật nhất nếu chấp nhận hạ tầng nặng (Matrix, Higress, K8s/Docker).

### Cited Findings

#### 2.1 OpenVort, `openvort/openvort` @ `7beee903f1f8558c1a5d590d33cb6fbfd4cc1438` (2026-04-27)
- **Nơi gọi model API** [MÃ]: `src/openvort/core/engine/llm.py`, gồm `AnthropicProvider` (L119), `OpenAICompatibleProvider` (L251), `OpenAIResponsesProvider` (L556). README gọi đây là "vòng agentic dựa trên Claude tool use, failover nhiều mô hình" ([llm.py](https://github.com/openvort/openvort/blob/7beee90/src/openvort/core/engine/llm.py)).
- **Mô hình người, vai trò, phòng ban** [MÃ], trong `src/openvort/contacts/models.py`:
  - `Member` (L21): tên, email, SĐT, `position`, `is_account`; các trường nhân viên AI (`is_virtual`, `post`, `virtual_system_prompt`, `skills`, `auto_report`).
  - `PlatformIdentity` (L60), ràng buộc `UniqueConstraint(platform, platform_user_id)`: `platform_position`, `platform_department`, `raw_data`.
  - `MatchSuggestion` (L89): khớp theo email/phone/name, có `confidence`, trạng thái pending/accepted/rejected.
  - `Department` (L112, dạng cây qua `parent_id`), `MemberDepartment` (L134, có `is_primary`), `ReportingRelation` (L155, kiểu direct/dotted/functional).

  ([models.py](https://github.com/openvort/openvort/blob/7beee90/src/openvort/contacts/models.py))
- **Phân giải danh tính người gửi** [MÃ]:
  - `contacts/resolver.py:17 IdentityResolver.resolve(platform, platform_user_id) -> Member | None`, có cache.
  - `cli/service.py:340-400 build_context()`: kênh web lấy thẳng `member_id`; kênh IM gọi `resolver.resolve(channel_name, user_id)`, rồi nạp `roles`, `permissions`, `position` và **toàn bộ tài khoản của người đó trên các nền tảng** (`ctx.platform_accounts`).
  - `core/engine/context.py:47 get_sender_prompt()` chèn "# 当前对话者" vào prompt (tên, chức vụ, email, vai trò), kèm prompt riêng theo vai (`auth/prompts/{admin,manager,member,guest}.md`).
  - `core/messaging/group_context.py` gắn nhóm chat với dự án.

  ([service.py](https://github.com/openvort/openvort/blob/7beee90/src/openvort/cli/service.py), [context.py](https://github.com/openvort/openvort/blob/7beee90/src/openvort/core/engine/context.py))
- **Đồng bộ danh bạ** [MÃ]: lớp trừu tượng `contacts/sync.py:38 ContactSyncProvider` với `fetch_members()` và `fetch_departments()`; được hiện thực trong `channels/{wecom,dingtalk,feishu}/sync.py` và `plugins/zentao/sync.py`. `contacts/matcher.py:21 IdentityMatcher` tạo gợi ý gộp danh tính.
- **Tách việc, duyệt, phê duyệt** [MÃ]:
  - `plugins/vortflow/engine.py:14` có `StoryState`: submitted → intake → review → rejected / pm_refine → design → breakdown → dev_assign → in_progress → testing → bugfix → done.
  - Các tool `vortflow_intake_story`, `create_task`, `assign`, ... (`plugins/vortflow/tools/`).
  - Test plan có trạng thái approved/rejected (`router/test_plans.py:143-145`).
  - Đây là quy trình agile phần mềm, không phải bước tự làm rõ một yêu cầu mơ hồ.
- **Kênh và cách nạp plugin** [MÃ]:
  - `plugin/base.py:20 Message(content, sender_id, sender_name, channel, msg_type, images, voice_media_ids, raw)`.
  - `plugin/base.py:40 BaseChannel` với `start()`, `stop()`, `send(target, message)`, `on_message(handler)`, `is_configured()`, `get_sync_provider()`.
  - `plugin/loader.py:306-321 _load_channels()` nạp từ entry_points nhóm **`openvort.channels`**; plugin nạp từ nhóm `openvort.plugins`.
  - Kênh có sẵn: wecom, dingtalk, feishu, openclaw.

  ([loader.py](https://github.com/openvort/openvort/blob/7beee90/src/openvort/plugin/loader.py))
- **Phát hành** [MÃ]: tag v0.13.0 (2026-04-27), v0.12.0 (2026-04-09), v0.11.0 (2026-04-08). Tổng 22 commit, commit đầu 2026-03-22. PyPI `openvort` trả 404 (đã kiểm ngày 2026-09-27).
- **Tài liệu và ảnh chụp** [DOC]: README tiếng Trung, có tagline tiếng Anh. Ảnh chụp thật nằm trên CDN của dự án (ví dụ `https://cdn.openvort.com/uploads/86f4d6e6-3872-48cc-91db-026afc47c096.png`, màn "AI 聊天"). Có demo trực tuyến tại demo.openvort.com (không truy cập được).

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 | **Đạt** | [MÃ] `core/engine/llm.py` L119/251/556, dùng key của người dùng |
| R2 | Một phần | [MÃ] Có nhiều nhân viên AI (`Member.is_virtual` + `post`) và phòng ban. Chưa thấy cơ chế để các nhân viên AI phối hợp hay giao việc cho nhau (chưa kiểm chứng) |
| R3 | Một phần | [MÃ] StoryState có intake/review/pm_refine/breakdown/dev_assign, nhưng AI chỉ chuyển trạng thái qua tool. Không thấy bước tự hỏi lại và tự viết tiêu chí nghiệm thu |
| R4 | Một phần | [MÃ] Có trạng thái review/rejected cho story và approved/rejected cho test plan. Không có cổng người duyệt chung trước khi đăng bài hay chi tiền |
| R5a | **Đạt** | [MÃ] `get_sender_prompt` (tên, chức vụ, vai trò), biết kênh, `group_context` |
| R5b | **Đạt** | [MÃ] Một `Member` có nhiều `PlatformIdentity`, cộng `IdentityMatcher` và `MatchSuggestion` |
| R5c | **Đạt (gần trọn)** | [MÃ] Có `position`, `Department`, `ReportingRelation`; 4 vai admin/manager(部门管理者)/member/guest kèm quyền (`auth/service.py:16-30`); tool bị lọc theo quyền. Riêng phòng ban **không** được chèn vào prompt |
| R5d | Một phần | [MÃ] Mỗi lần gọi tool đều được gắn `tool_input["_member_id"] = ctx.member.id` (`core/engine/agent.py:300`). Chưa thấy chuỗi giao việc giữa các agent |
| R6 | **Đạt** | [MÃ] Có 4 kênh và cơ chế entry_points `openvort.channels`. Không có Telegram hay Zalo sẵn |
| R7 | Một phần (AGPL-3.0) | Dùng nội bộ được. Nếu **sửa** rồi cho người dùng truy cập qua mạng (kể cả nhân viên) thì phải cung cấp mã nguồn bản sửa cho họ (§13). Plugin chạy cùng tiến trình nên được coi như tác phẩm kết hợp, tức nên phát hành cùng AGPL |
| R8 | **Không** | Bản cuối 2026-04-27, trước ngưỡng 2026-06-27 |
| R9 | Không / chưa kiểm | Có cây phòng ban, nhưng chưa thấy sơ đồ kéo-thả dùng để điều phối việc |
| R10 | Không | [MÃ] Không có mô hình tenant (grep `tenant` chỉ ra kết quả trong API Feishu) |
| R11 | **Đạt** | [MÃ] entry_points `openvort.plugins`, 10 plugin có sẵn, có "扩展市场" |
| R12 | Một phần | Có ảnh chụp thật (CDN) và demo, nhưng tài liệu chỉ tiếng Trung |

#### 2.2 Agency Orchestrator, `jnMetaCode/agency-orchestrator` @ `bed6613` (2026-09-25)
- **Model API** [MÃ]: `src/connectors/openai-compatible.ts:76 OpenAICompatibleConnector`, `api-providers.ts`, `ollama.ts`. CLI là tuỳ chọn: `claude-code.ts`, `codex-cli.ts`, `gemini-cli.ts`, `openclaw-cli.ts`, `hermes-cli.ts`, ... README nói "đã đăng nhập Claude Code thì tự dùng" ([connectors](https://github.com/jnMetaCode/agency-orchestrator/tree/bed6613/src/connectors)).
- **Từ yêu cầu mơ hồ đến kế hoạch** [MÃ]: `src/cli/compose.ts:249-289` là prompt cho LLM tự chọn vai trong thư viện 276 vai và viết DAG YAML. Prompt này ép:
  - bước cuối phải có `acceptance:` gồm 2–5 điều kiện kiểm được;
  - dùng bước `type: human_input` khi cần hỏi lại người dùng;
  - dùng bước `type: approval` cho việc rủi ro hoặc tốn tiền.
- **Engine thực thi** [MÃ]: `src/core/executor.ts:559` (approval), `:564` (human_input), `:1104-1142` (`verifyAcceptance` rồi làm lại đúng một vòng). `src/core/verify.ts:74 verifyAcceptance`. `handleApproval` (khoảng L1194-1207) chờ duyệt qua web Studio hoặc stdin.
- **Danh tính** [MÃ]: `web/server.js:129-130` ghi rõ "Local single-user tool — bind to loopback by default", `HOST` mặc định 127.0.0.1.
- **Kênh** [MÃ]: chỉ đẩy kết quả ra ngoài (`src/notify.ts:44-61`, webhook DingTalk/Feishu/WeCom/Slack). Có MCP server (`src/mcp/server.ts`).
- **Ảnh chụp thật** [MÃ]: `docs/screenshots/studio-roles-en.png`, `docs/screenshots/studio-workflows-en.png`, `demo-studio-en.gif`.

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 | **Đạt** | [MÃ] Có đường gọi API native; CLI chỉ là tuỳ chọn |
| R2 | Một phần | Có thư viện vai theo "bộ phận" [DOC agency-agents-zh], nhưng đội hình chỉ sống trong một lần chạy, không có agent thường trực |
| R3 | **Đạt** | [MÃ] compose tự lập đội, sinh DAG kèm acceptance; executor kiểm và làm lại. Chỉ hỏi lại người dùng khi LLM tự chèn `human_input` |
| R4 | **Đạt / Một phần** | [MÃ] Có cổng `approval`, nghiệm thu tự động với một vòng làm lại, và `--feedback`. Review chỉ bắt buộc ở bước có ghi `acceptance` |
| R5a–d | **Không** | [MÃ] Công cụ một người dùng |
| R6 | Không | [MÃ] Chỉ có webhook ra, không có kênh chat vào |
| R7 | **Đạt** | Apache-2.0, có Dockerfile |
| R8 | **Đạt** | Tag v0.19.2 ngày 2026-09-06; 455 commit từ sau 2026-06-27 |
| R9 | Một phần | Canvas kéo node và nối cạnh *điều khiển DAG* (`src/canvas/graph.ts`) [MÃ/DOC], nhưng đó là sơ đồ quy trình, không phải sơ đồ tổ chức |
| R10 | Không | — |
| R11 | Một phần | Thư viện vai dạng npm (`agency-agents-ko`, ...), `ao-skills`, connector factory |
| R12 | **Đạt** | README EN/ZH, có ảnh và GIF thật; khoảng 2.3k★ |

#### 2.3 opc-web, `wenbuer/opc-web` @ `2cd3dc4` (2026-09-20)
- **Model API** [MÃ]: `src/opc_web/engines/api.py:169-187` dùng urllib POST tới `{baseUrl}/chat/completions` (mặc định DeepSeek). Engine DSH (DeepSeek Harness headless, một agent CLI) là tuỳ chọn (`engines/dsh.py`).
- **Tách việc** [MÃ]: `src/opc_web/chain.py:99-143 decompose()`:
  - LLM tách việc thành tối đa `maxSubtasks` dòng `| số | mô tả | R_x | 期望产出 | 待派 |`.
  - Việc được giao theo bảng vai và chức trách (`roles.role_digest`). Nếu không ra được vai hợp lệ thì trả rỗng và việc bị chặn.
  - Không có bước hỏi lại người dùng; "期望产出" chỉ là tiêu chí sơ lược.
- **Duyệt và làm lại** [MÃ]:
  - `src/opc_web/review.py:10-64`: R0 duyệt, bác hoặc sửa, ghi vào `批阅台.md`.
  - `server.py:661-684`: sau khi R0 duyệt, R1 phát lại việc. Duyệt thì thực thi. Chọn "sửa" thì tạo việc "按批阅修改…后重报" và lặp **cho tới khi được duyệt**. Bác thì dừng.
- **Phạm vi truy cập** [MÃ]: `config.py:140`, `HOST` mặc định 127.0.0.1.
- **Ảnh chụp thật**: `images/opc-command-center-01..08.png` (bàn chỉ huy, bàn duyệt, workbench, nhật ký, token).

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 | **Đạt** | [MÃ] engines/api.py |
| R2 | Một phần | [MÃ] Vai R1..R7 (`agents-seed/*.role.md`), không có phòng ban |
| R3 | Một phần | [MÃ] Tách thành nhiều việc con và giao theo chức trách, nhưng không hỏi lại và không có tiêu chí nghiệm thu thật |
| R4 | **Đạt / Một phần** | [MÃ] Có cổng người duyệt, gửi lại để làm lại cho tới khi duyệt. Không có agent phản biện bắt buộc |
| R5a–d | **Không** | Chỉ có một người (R0), chạy cục bộ |
| R6 | Không | Không có kênh chat |
| R7 | **Đạt** | MIT |
| R8 | **Đạt** (còn non) | v1.18.0 ngày 2026-09-20. Lịch sử git chỉ từ 2026-09-14 (18 commit), khoảng 6★ |
| R9 / R10 | Không | — |
| R11 | Một phần | Có registry engine (`engines/registry.py`) và thư mục skill |
| R12 | Một phần | README ZH/EN, có ảnh thật |

#### 2.4 zalo-agent, `vuhai2002/zalo-agent` @ `bf154de` (2026-08-30)
- **Model API** [MÃ]: `src/agent/agent-loop.ts:1` dùng `streamText` của Vercel AI SDK; `llm-provider.ts` hỗ trợ OpenAI-compatible, Anthropic và Google.
- **Mô hình dữ liệu** [MÃ], trong `src/conversation/database.ts`:
  - `contacts(account_id, user_id, display_name, first_seen, last_seen, message_count)` (L62);
  - `agents` là "não": persona cộng model (L80);
  - `accounts` là kênh: `allowlist_mode`, `allowlist_user_ids`, `group_require_mention`, ... (L93);
  - `memories(account_id, subject_id, learned_in_thread_id, learned_in_group)` (L108). Ký ức học trong chat riêng thì không đưa ra nhóm.
- **Người gửi** [MÃ]: `src/agent/user-message-line.ts` hiển thị mỗi tin dạng `[dd/mm hh:mm] Tên: nội dung`, và gắn nhãn "chưa xác minh" cho người ngoài allowlist.
- **Kênh** [MÃ]: `src/zalo/kenh-luot.ts:23 KenhLuot` là lớp trừu tượng năng lực kênh, chỉ phục vụ 2 loại Zalo (cá nhân qua zca-js, Bot API). README cảnh báo Zalo cá nhân có **nguy cơ bị khoá tài khoản** [DOC].
- **Ảnh chụp**: trong repo không có ảnh chụp dashboard thật, chỉ có logo và nền (`web/public/*`).

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 | **Đạt** | [MÃ] |
| R2 | Không | [MÃ] Mỗi tài khoản gắn một não, không có phối hợp |
| R3 | Không | Chỉ có một vòng lặp agent kèm tool |
| R4 | Không | Chỉ có allowlist và giới hạn chủ động gửi |
| R5a | Một phần | [MÃ] Có tên người gửi, biết thread nhóm hay riêng, có allowlist |
| R5b | Không | Chỉ có Zalo, định danh theo từng tài khoản |
| R5c | Không | Không có chức danh, phòng ban hay quyền |
| R5d | N/A | — |
| R6 | Một phần | Chỉ có Zalo (2 loại); thêm kênh khác phải sửa lõi |
| R7 | **Đạt** | MIT. Lưu ý rủi ro của zca-js không chính thức |
| R8 | Đạt (sát ngưỡng) | v0.3.1 ngày 2026-08-30; tháng 9/2026 không có commit |
| R9 / R10 | Không | — |
| R11 | Một phần | MCP server bên ngoài (`src/mcp`) |
| R12 | Một phần | Tài liệu VN là chính, có README.en; không có ảnh chụp thật |

#### 2.5 AgentTeams (HiClaw), `agentscope-ai/AgentTeams` @ `89562fb` (2026-09-23). Kiểm sâu lại vì mạnh.
- **Model API**: [MÃ] `agentteams-controller/api/v1beta1/types.go:186-196`, `Model`/`ModelProvider` ("APIG Model API") và `Runtime` thuộc `openclaw | copaw | hermes | qwenpaw | deepseek-harness` (mặc định openclaw). [DOC] v1.2.3 khuyến nghị QwenPaw ([README](https://github.com/agentscope-ai/AgentTeams)).
- **Mô hình người và đội** [MÃ], trong `types.go`:
  - `HumanSpec` (L620-645): `DisplayName`, `Email`, `PermissionLevel` (1 Admin, 2 Team, 3 Worker), `AccessibleTeams`, `AccessibleWorkers`, `IdentitySource{Issuer, Subject}` (OIDC), `Capabilities`, `Note`.
  - `TeamSpec` (L453): `Admin`, `HumanMembers`, `WorkerMembers`, `ChannelPolicy`.
  - `TeamWorkerRef.Role` (L484) nhận `team_leader` hoặc `worker`.
  - `TeamMemberSpec.Role` (L505) mặc định là coordinator.
- **Phân giải người gửi**:
  - [MÃ/prompt] `manager/agent/skills/channel-management/references/identity-and-contacts.md`: người gửi trên Matrix được xếp vào Admin, Team Leader, Worker, Human L1/L2/L3, Trusted Contact hoặc Unknown (Unknown thì im lặng). Ở kênh ngoài Matrix chỉ có admin (qua `primary-channel.json`) và `trusted-contacts.json {channel, sender_id}`.
  - [MÃ] Controller tự thực thi quyền qua `internal/auth/matrix_authenticator.go:121` (theo `PermissionLevel`).
- **Làm rõ, tách việc, duyệt** [MÃ]:
  - `plugins/teamharness/skills/team/team-coordination/SKILL.md:18-29,85`: trước khi giao việc phải làm rõ mục tiêu, tiêu chuẩn nghiệm thu và người phụ trách; mơ hồ thì hỏi lại người yêu cầu; chọn giữa DAG và Loop.
  - `task-delegation/SKILL.md:75`: spec việc có "Acceptance Criteria".
  - `plugins/teamharness/mcp/server.py:3137,4441`: `accept_task_result` có `REVISION_NEEDED` dẫn tới trạng thái `revision`; chuyển trạng thái submitted → completed/revision/blocked/cancelled.
- **Việc thay mặt ai** [MÃ]: `server.py:217,253-257,443-448` lưu "requester route": kênh nguồn, phòng hoặc hội thoại gốc, và `sender_staff_id` của DingTalk để báo lại đúng người yêu cầu.
- **Kênh** [MÃ]: Matrix (Tuwunel + Element) là kênh chính. `ChannelsSpec` của Worker chỉ có `DingTalk` (`types.go:374-380`). Kênh khác phải đi qua plugin của runtime OpenClaw/QwenPaw [DOC].
- **Ảnh chụp thật**: `docs/zh-cn/images/windows-deploy/element-web-home.png`, `element-web-login.png`.

| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 | **Đạt** (gián tiếp) | Runtime native gọi qua gateway Higress bằng key của mình; Claude Code chỉ là tài sản tuỳ chọn ở `teamharness/remote` |
| R2 | **Đạt** | [MÃ] CRD Team có Leader và Worker, kiến trúc Manager-Workers |
| R3 | **Đạt** (qua prompt skill và state machine DAG) | [MÃ] team-coordination bắt làm rõ, viết tiêu chí nghiệm thu, hỏi lại |
| R4 | Một phần | [MÃ] Có trạng thái revision; con người can thiệp trong phòng chat (có kiểm toán, [DOC] v1.2.3). Không thấy cổng duyệt bắt buộc trước khi đăng hay chi tiền |
| R5a | **Đạt** | [MÃ] Bảng phân loại người gửi và controller thực thi quyền |
| R5b | Không | Human gắn với một user Matrix hoặc OIDC; kênh ngoài Matrix chỉ có danh sách `trusted-contacts` riêng, không gộp |
| R5c | Một phần | Có mức quyền, phạm vi đội và capabilities, nhưng **không có chức danh hay phòng ban** |
| R5d | Một phần | [MÃ] Có requester route trong TeamHarness |
| R6 | Một phần | Có Matrix và DingTalk; Zalo không có |
| R7 | **Đạt** | Apache-2.0. Hạ tầng nặng: Matrix, Higress, MinIO, controller (Docker, Helm, K8s) |
| R8 | **Đạt** | Tag v1.2.4 ngày 2026-09-21; 172 commit từ sau 2026-06-27 |
| R9 | Không / chưa kiểm | Khai báo bằng YAML/CRD; không thấy sơ đồ tổ chức kéo-thả |
| R10 | Chưa kiểm | Controller theo namespace (`types.go` L19), có thể cô lập được nhưng chưa kiểm chứng |
| R11 | **Đạt** | `plugins/README.md`, `agentteams plugin install`, skills trên Nacos |
| R12 | **Đạt** | README EN/zh-CN/ja-JP, docs EN+ZH, có ảnh thật; khoảng 5.7k★ |

#### 2.6 Kiểm vừa phải: JiuwenSwarm @ `52abe68db` và UniEmployee @ `7d5edf5`

**JiuwenSwarm**
- **Kênh** [MÃ]: `jiuwenswarm/gateway/channel_manager/im_platforms/` có feishu, dingtalk, wecom, wechat, telegram, slack, discord, whatsapp, xiaoyi.
  - `BaseChannel` (`channel_manager/base.py:119`) có `start`, `stop`, `send`, và `is_allowed(sender_id)` (allow_from, L170).
  - Các kênh được **khởi tạo cứng** trong `gateway/app_gateway.py` (L2365-2763), nên thêm Zalo phải sửa lõi. Có `register_external_channel()` (`channel_manager.py:266`) và `ApplicationPluginExtension.bind_web_channel()` (`extensions/sdk/application_plugin.py:79`); đường đi cho kênh ngoài qua hai hàm này chưa kiểm chứng.
- **Danh tính** [MÃ]: Feishu chỉ lấy *tên* qua `contact.v3.user.get` (`feishu_im_adapter.py:45-80`); DingTalk dùng `sender_nick`. Đây là trợ lý có "principal user", nên R5 yếu.
- **HITL** [MÃ]: `human` / `human_session` trong Swarmflow (`agents/harness/team/handlers/workflow_state.py:57-59`) và luồng duyệt skill-evolution (`team_manager.py:382,1807`).
- **Tách việc**: logic Leader nằm trong `openjiuwen` (`pyproject.toml:20`, lấy từ gitcode), chưa kiểm [?].
- **Điểm**: R1 Đạt · R2 Đạt · R3 Một phần [?] · R4 Một phần · R5 5a Một phần, 5b/5c/5d Không · R6 Một phần (nhiều kênh nhưng khởi tạo cứng) · R7 Đạt (Apache-2.0) · R8 Đạt · R11 Một phần · R12 Đạt (EN/CN, ảnh `docs/assets/images/`).

**UniEmployee**
- **Kênh** [MÃ]: `backend/app/routes/im.py:1-6` mô tả kênh gồm provider web / wecom / feishu / dingtalk / generic, với webhook chung `POST /api/im/channels/{id}/incoming` (`ImIncomingMessage{sender_id, message, employee_id, secret}`, `models.py:95`) và `outbound_webhook`. Người gửi được đặt tên `im:{channel_id}:{sender_id}` (`im.py:61`).
- **Danh tính** [MÃ]: `auth.py:194-205 oidc_role_and_org` ánh xạ group thành vai, claim `department` thành org.
- **Phê duyệt** [MÃ]: HITL theo tool (`catalog/employees.py:9 _build_interrupt_on`), `approvals.py` có tự bác khi hết hạn.
- **Điểm**: R1 Đạt · R2 Một phần (subagents trong từng nhân viên) · R3 Một phần (SOP/StateGraph cố định) · R4 **Đạt** (theo tool) · R5 5a Một phần, 5b Không, 5c Một phần (OIDC dept), 5d Không · R6 Một phần (webhook chung) · R7 Đạt · R8 Đạt · R10 Một phần (cột `tenant_id` nhưng chỉ một `ENTERPRISE_TENANT_ID`) · R12 Đạt (ZH/EN, `assets/screenshots/00-chat-main.png`, ...).

### Inferences
- Nếu R5 là tiêu chí quan trọng nhất, mô hình dữ liệu của OpenVort là **khuôn mẫu tham chiếu tốt nhất** tìm được: Member, PlatformIdentity, MatchSuggestion, Department, ReportingRelation, cộng ContactSyncProvider. Đáng *sao chép thiết kế* ngay cả khi không dùng chính OpenVort (vì R8 và AGPL).
- AgentTeams là lựa chọn "đang sống, Apache-2.0, có đội và có Human" nhưng thiếu chức danh/phòng ban và thiếu gộp danh tính xuyên kênh. Muốn bổ sung phải làm ở tầng skill/MCP, hoặc sửa CRD.
- Agency Orchestrator và opc-web phù hợp làm "động cơ quy trình" (R3/R4) đặt sau một cổng nhận diện danh tính, không phải nền tảng hoàn chỉnh.

### Gaps
- Không cài và chạy bất kỳ dự án nào ([CHẠY] = 0); điểm UI dựa trên ảnh trong repo.
- OpenVort: chưa kiểm chứng việc giao việc giữa các nhân viên AI và mức độ trọn vẹn của các `sync.py` (có phân trang, có xử lý chức vụ không).
- AgentTeams: chưa kiểm R10 (đa namespace) và dashboard.
- JiuwenSwarm: logic Leader nằm trong repo `openjiuwen` agent-core trên gitcode, chưa đọc.

---

## Câu hỏi 3: Nếu phải tự xây tầng danh tính (R5), có làm được mà KHÔNG fork không? (điểm mở rộng cụ thể)

### Takeaway
Chỉ **OpenVort** và **UniEmployee** có điểm mở rộng thật để gắn kênh mới (Zalo) và danh bạ mà không sửa lõi. **QwenPaw** mở cho kênh nhưng không có mô hình người. **AgentTeams** chỉ mở rộng được danh tính ở tầng skill/MCP (phải sửa CRD nếu muốn thêm trường). **JiuwenSwarm, zalo-agent, opc-web và Agency Orchestrator** cần fork, hoặc phải bọc bên ngoài.

### Cited Findings
- **OpenVort**, không cần fork [MÃ]:
  - (1) Kênh Zalo là một gói pip riêng khai báo entry point `[project.entry-points."openvort.channels"] zalo = "pkg:ZaloChannel"`. Lớp này kế thừa `BaseChannel` (`src/openvort/plugin/base.py:40`, gồm `async start()`, `async stop()`, `async send(target: str, message: Message)`, `on_message(handler: MessageHandler)`, `is_configured() -> bool`, `get_sync_provider() -> ContactSyncProvider | None`). Loader tự nạp nó (`plugin/loader.py:306-321`).
  - (2) Danh bạ: hiện thực `ContactSyncProvider.fetch_members() -> list[PlatformContact]` và `fetch_departments() -> list[PlatformDepartment]` (`contacts/sync.py:13-65`). Khi đó `IdentityMatcher.find_matches(contact)` (`contacts/matcher.py:28`) sinh `MatchSuggestion` để gộp danh tính với người đã có trên WeCom/Feishu.
  - (3) Phân giải người gửi dùng khoá `(channel_name, sender_id)` qua `IdentityResolver.resolve` (`contacts/resolver.py:32`), không phải sửa gì.
  - (4) Tool mới dùng gói `openvort.plugins` với `BaseTool.required_permission` (ví dụ `plugins/vortflow/tools/intake.py`, `required_permission = "vortflow.story"`).
  - Chỗ thiếu duy nhất là muốn chèn *phòng ban* vào prompt. `RequestContext.get_sender_prompt()` (`core/engine/context.py:47`) không có hook, nên phải sửa lõi. Cách không fork: đặt `platform_position` giàu thông tin, hoặc dùng prompt của vai trò (`auth/prompts/*.md`).
  - ([base.py](https://github.com/openvort/openvort/blob/7beee90/src/openvort/plugin/base.py), [sync.py](https://github.com/openvort/openvort/blob/7beee90/src/openvort/contacts/sync.py))
- **UniEmployee**, không cần fork cho phần kênh [MÃ]:
  - Một cầu nối Zalo bên ngoài POST tới `/api/im/channels/{id}/incoming` với `{sender_id, message, employee_id, secret}` (`backend/app/routes/im.py`, `models.py:95`), rồi nhận trả lời qua `outbound_webhook` của kênh.
  - Tuy nhiên danh tính sẽ là `im:{channel_id}:{sender_id}` (`im.py:61`), tức **mỗi kênh một người**. Muốn gộp xuyên kênh (5b) thì cầu nối phải tự quy đổi về một `sender_id` chuẩn *trước khi* gửi vào. Hệ không có trường chức danh cho người gửi IM.
- **QwenPaw**, không cần fork cho kênh [MÃ]:
  - `src/qwenpaw/app/channels/registry.py` gộp các kênh có sẵn (`_BUILTIN_SPECS`) với kênh từ plugin (`_get_plugin_channels()` qua `PluginRegistry().get_registered_channels()`).
  - Danh tính chỉ có `ChannelACL` và `UserInfo(remark, username)` theo từng kênh (`access_control.py:74,101`). Muốn có R5 thì phải tự xây một tool hoặc MCP tra danh bạ bên ngoài.
- **AgentTeams**, mở rộng một phần:
  - Các trường của `HumanSpec` là cố định (`types.go:620-645`). Thêm chức danh hay phòng ban phải **sửa CRD** (fork), hoặc tạm nhét vào `Note`.
  - Cách không fork: viết skill Manager hoặc Worker mới (thư mục `manager/agent/skills/*`) gọi một MCP server tra danh bạ (có skill `mcp-server-management`), khớp theo `matrixUserID` hoặc `sender_staff_id`.
  - Kênh mới cho Worker phải đi qua plugin kênh của runtime (ví dụ registry plugin của QwenPaw) vì `ChannelsSpec` chỉ có DingTalk (`types.go:374`).
- **JiuwenSwarm**, phải sửa lõi để thêm kênh:
  - Kênh được khởi tạo trong `gateway/app_gateway.py` (L2365-2763). Có thể thử `ChannelManager.register_external_channel(channel_id, channel)` (`channel_manager.py:266`) từ một `ApplicationPluginExtension` (`extensions/sdk/application_plugin.py:69-91`), nhưng chưa kiểm chứng có dùng được như vậy không.
  - Danh tính không có mô hình người.
- **zalo-agent / opc-web / Agency Orchestrator**: không có điểm mở rộng danh tính.
  - zalo-agent: `contacts` và `memories` gắn chặt với `account_id` (`database.ts:62,108`), nên phải fork.
  - opc-web: chỉ một người (R0), nên phải fork.
  - Agency Orchestrator: chỉ có thể *bọc* bên ngoài. Cổng nhận diện truyền hồ sơ người yêu cầu vào `inputs` / `{{variables}}` của workflow YAML khi gọi `ao run`, hoặc gọi qua MCP server (`src/mcp/server.ts`).

### Inferences
- Nếu giữ nền tảng hiện có (ví dụ GoClaw) và chỉ "mượn" ý tưởng, đáng mượn nhất là thiết kế **PlatformIdentity + MatchSuggestion + ContactSyncProvider** của OpenVort. Thiết kế này giải được 5b (một người nhiều kênh) và 5c (phòng ban, chức vụ, quan hệ báo cáo) theo cách có người xác nhận gộp.
- Với Zalo, không ứng viên châu Á nào có adapter sẵn trong nền tảng tổ chức. zalo-agent (`src/zalo/*`, lớp `KenhLuot`) và abs-zalo-bot (MCP, cả OA lẫn cá nhân) là mã tham chiếu tốt để viết một adapter `BaseChannel` riêng.

### Gaps
- Chưa thử dựng plugin kênh cho OpenVort hay QwenPaw để xác nhận nạp được thật ([CHẠY] chưa làm).
- Chưa đánh giá pháp lý chi tiết về việc plugin chạy cùng tiến trình với lõi AGPL (OpenVort, GuSheng107) có bị coi là tác phẩm phái sinh hay không. Nên hỏi luật sư nếu định phân phối ra ngoài.
