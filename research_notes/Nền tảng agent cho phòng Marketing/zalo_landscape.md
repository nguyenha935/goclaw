# Bản đồ tích hợp Zalo cho nền tảng AI agent tự host (tính đến 27/09/2026)

> Ghi chú phương pháp (đọc trước):
> - Ngày làm việc: 27/09/2026 (đã xác nhận bằng `date` → `Sun Sep 27 03:41:53 UTC 2026`) [CHẠY].
> - **Tất cả domain chính thức của Zalo đều bị egress proxy của phiên này chặn (HTTP 403)**: `zalo.me`, `developers.zalo.me`, `oa.zalo.me`, `zalo.cloud`, `business.zalo.me`, `zalo.solutions`, `bot.zapps.me`, `docs.zaloplatforms.com`, `docs.openclaw.ai`; cả các báo/blog VN (`znews.vn`, `tienphong.vn`, `viblo.asia`, `miniai.vn`, `vihatsolutions.com`, `v9.com.vn`…) cũng bị chặn [CHẠY]. Vì vậy mọi thông tin "từ nguồn chính thức Zalo" dưới đây lấy từ **đoạn trích (snippet) của công cụ tìm kiếm** — được gắn nhãn **[DOC-snippet]** và ghi rõ là không mở được trang gốc. Những gì đọc được trực tiếp: GitHub (git clone), npm registry, PyPI JSON API.
> - Nhãn: [MÃ] = đã đọc mã nguồn; [CHẠY] = đã chạy lệnh (git/curl registry); [DOC] = chỉ tài liệu (đọc được trực tiếp, ví dụ file .md trong repo); [DOC-snippet] = tài liệu qua snippet tìm kiếm, không mở được trang; [?] = chưa kiểm chứng.
> - Nguồn chính thức Zalo (oa.zalo.me, zalo.solutions, developers.zalo.me, docs.zaloplatforms.com, zalo.me/blog, zalo.vn, help.zalo.me) được ghi "(CHÍNH THỨC)"; đại lý/reseller/blog ghi "(RESELLER/BLOG)".
> - Clone đã đặt tại scratchpad và đã xoá sau khi xong. Không động vào repo GoClaw (chỉ đọc).
> - Mốc thời gian npm là UTC; commit git ghi theo múi giờ của commit.

---

## 1. Zalo Bot API / Zalo Bot Platform chính thức — có gì, trạng thái, 1:1 vs nhóm, auth, giới hạn, chi phí, ToS

### Takeaway
Zalo Bot Platform (Bot Creator/Marketplace, API kiểu Telegram tại `bot-api.zaloplatforms.com/bot<TOKEN>/<method>`) là đường **chính thức**, tạo được từ tài khoản cá nhân, xác thực bằng bot token; nhắn 1:1 dùng được ngay, còn **tính năng bot trong nhóm được chính tài liệu Zalo ghi là "đang trong giai đoạn thử nghiệm nội bộ"** (bằng chứng mới nhất: 30/08/2026). Giới hạn tần suất, chi phí chính thức và điều khoản riêng cho bot AI: **không tìm được nguồn chính thức**.

### Cited Findings
- Tài liệu chính thức nằm ở "Zalo Platform Document Hub": trang tổng quan Zalo Bot, "Tạo Bot", "Sử dụng API", "Hướng dẫn sử dụng Zalo Bot tương tác với Nhóm Chat" (CHÍNH THỨC) [DOC-snippet] — [docs.zaloplatforms.com/docs/BOT](https://docs.zaloplatforms.com/docs/BOT), [create_bot](https://docs.zaloplatforms.com/docs/BOT/create_bot), [call_api](https://docs.zaloplatforms.com/docs/BOT/call_api). Domain cũ `bot.zapps.me/docs` vẫn được SDK cộng đồng và issue GoClaw trích dẫn — [GoClaw issue #1542](https://github.com/nextlevelbuilder/goclaw/issues/1542).
- Định dạng gọi API: `https://bot-api.zaloplatforms.com/bot<BOT_TOKEN>/<functionName>` (CHÍNH THỨC) [DOC-snippet] — [docs.zaloplatforms.com/docs/BOT/call_api](https://docs.zaloplatforms.com/docs/BOT/call_api). Được xác nhận trong mã của 3 hiện thực độc lập [MÃ]: OpenClaw `extensions/zalo/src/api.ts:15` (`ZALO_API_BASE = "https://bot-api.zaloplatforms.com"`), plugin chính thức Zalo `@zalo-platforms/openclaw-zaloclawbot` `dist/src/api/api.js:1`, GoClaw `internal/channels/zalo/zalo.go:37` + `:443` (`fmt.Sprintf("%s/bot%s/%s", apiBase, c.token, method)`).
- Các method dùng trong thực tế [MÃ]: `getMe`, `getUpdates`, `sendMessage`, `sendPhoto`, `sendChatAction`, `setWebhook`, `deleteWebhook`, `getWebhookInfo` — OpenClaw `extensions/zalo/src/api.ts:194-317` (clone openclaw/openclaw HEAD `96e4061`, 27/09/2026).
- Tạo bot: đăng nhập `bot.zaloplatforms.com`, tạo bot, token dạng `numeric_id:secret`; với Marketplace bot token có thể nằm trong tin nhắn chào mừng [DOC] — OpenClaw `docs/channels/zalo.md` (repo openclaw/openclaw). Bot được tạo qua Mini App "Zalo Bot Creator" (CHÍNH THỨC) [DOC-snippet] — [miniapp.zaloplatforms.com/apps/3082563950095582238](https://miniapp.zaloplatforms.com/apps/3082563950095582238/).
- Nhận tin: long-polling `getUpdates` hoặc webhook; **hai cơ chế loại trừ nhau**; webhook gửi header `X-Bot-Api-Secret-Token`, secret 8–256 ký tự, URL phải HTTPS [DOC] — OpenClaw `docs/channels/zalo.md`; xác nhận lại trong [GoClaw issue #1542](https://github.com/nextlevelbuilder/goclaw/issues/1542) (30/08/2026): "polling và webhook loại trừ nhau".
- Giới hạn văn bản: 2000 ký tự/tin (OpenClaw ghi "Zalo API limit") [DOC] — OpenClaw `docs/channels/zalo.md`; GoClaw `internal/channels/zalo/zalo.go` hằng `maxTextLength = 2000` [MÃ].
- **Nhóm**: trang chính thức "Hướng dẫn sử dụng Zalo Bot tương tác với Nhóm Chat" được snippet tóm tắt là "tính năng … đang trong giai đoạn thử nghiệm nội bộ và sẽ được phát hành trong tương lai", đồng thời mô tả cách mời bot vào nhóm, cách bot nhận tin trong nhóm và cách lấy group ID (CHÍNH THỨC) [DOC-snippet] — [docs.zaloplatforms.com/…/build-bot-interaction-with-group](https://docs.zaloplatforms.com/docs/BOT/best-practices/build-bot-interaction-with-group).
- GoClaw issue #1543 (mở 30/08/2026, tác giả maitanloi, trạng thái Open) trích nguyên văn tài liệu Zalo: "Tính năng đang trong giai đoạn thử nghiệm nội bộ"; bot trong nhóm chỉ được kích hoạt khi (1) người dùng reply/trích dẫn tin của bot, (2) @mention bot; giá trị `chat_type` cho nhóm **chưa được tài liệu hoá**; nguồn trích: `https://bot.zapps.me/docs/build-bot-interaction-with-group/` [DOC] — [GoClaw issue #1543](https://github.com/nextlevelbuilder/goclaw/issues/1543).
- Cơ chế mời vào nhóm (theo snippet): lấy link Bot từ Mini App Zalo Bot Creator, chia sẻ vào nhóm, trưởng nhóm bấm link và xác nhận thêm bot [DOC-snippet] — [docs.zaloplatforms.com/…/build-bot-interaction-with-group](https://docs.zaloplatforms.com/docs/BOT/best-practices/build-bot-interaction-with-group). Có một thread cộng đồng chính thức tên "Zalo BOT có thể hoạt động trong Group" nhưng không mở được — [developers.zalo.me/community/detail/c1e73a08064def13b65c](https://developers.zalo.me/community/detail/c1e73a08064def13b65c) [?].
- Mã OpenClaw nhận diện nhóm bằng `chat.chat_type === "GROUP"` (`extensions/zalo/src/monitor.ts:371`) [MÃ]; kiểu dữ liệu trong `@fased/zalo` khai báo `chat_type: "PRIVATE" | "GROUP"` (`src/api.ts:32`) [MÃ]. Tức cộng đồng *đoán* giá trị `GROUP`, khớp với cảnh báo trong issue #1543 rằng Zalo chưa công bố.
- Chi phí: một snippet tổng hợp từ các blog bên thứ ba nói "Zalo Bot cho phép tạo tối đa 3 bot miễn phí, mỗi bot tương tác với 50 người dùng và gửi tối đa 3000 tin/tháng" — **không xác định được trang nào nói vậy, không phải nguồn Zalo** [?] (RESELLER/BLOG, chưa kiểm chứng) — kết quả tìm kiếm gồm [vnrom.net](https://vnrom.net/2025/09/huong-dan-chi-tiet-cach-tao-zalo-bot-voi-n8n-hoan-toan-mien-phi/), [aizalo.com](https://aizalo.com/blog/huong-dan-cach-tao-chatbot-zalo-ca-nhan), [coderkiemcom.com](https://coderkiemcom.com/blog/portfolio/zalo-bot-tro-ly-ao-tu-dong-mien-phi).
- Rate limit của Bot API: snippet của tài liệu chính thức **không** chứa thông tin về giới hạn tần suất [DOC-snippet] — [docs.zaloplatforms.com/docs/BOT/call_api](https://docs.zaloplatforms.com/docs/BOT/call_api). (Con số "120 requests / 60s" trong OpenClaw là rate limit *của webhook endpoint phía OpenClaw*, không phải của Zalo [DOC] — OpenClaw `docs/channels/zalo.md`.)
- Bot Platform được mô tả (blog) là "tính năng Zalo Bot cá nhân — cho phép tài khoản Zalo thường tạo bot riêng, khác hoàn toàn OA" (RESELLER/BLOG) [DOC-snippet] — [tino.vn](https://tino.vn/blog/cach-tao-chatbot-zalo-ca-nhan-voi-n8n/), [vnrom.net](https://vnrom.net/2025/09/huong-dan-chi-tiet-cach-tao-zalo-bot-voi-n8n-hoan-toan-mien-phi/).

### Inferences
- Bot Platform phù hợp nhất cho **chat 1:1** (nội bộ hoặc khách), vì là đường chính thức, auth đơn giản (token), không có rủi ro khoá tài khoản như zca-js.
- Nhóm qua Bot Platform **chưa nên đưa vào vận hành**: tài liệu Zalo tự ghi "thử nghiệm nội bộ" (bằng chứng mới nhất 30/08/2026), và `chat_type` nhóm chưa được công bố.
- Việc Zalo phát hành plugin OpenClaw chạy trên Bot Platform (mục 5) cho thấy Zalo coi Bot Platform là con đường "chính thống" cho AI agent.

### Gaps
- Không đọc được trực tiếp trang tài liệu Bot (bị chặn) → không xác nhận được ngày cập nhật, tình trạng "thử nghiệm nội bộ" vào đúng ngày 27/09/2026 (chỉ có bằng chứng tới 30/08/2026).
- Không tìm được: rate limit chính thức, bảng giá/hạn mức chính thức của Zalo Bot, điều khoản sử dụng riêng cho Zalo Bot / cho bot dùng AI, quy tắc "bot có được nhắn trước cho người dùng chưa từng nhắn không".
- Ngày ra mắt chính thức Zalo Bot Platform: không tìm được nguồn chính thức (các blog n8n nói về nó từ 09/2025 — suy ra đã có ít nhất từ 2025).

---

## 2. Zalo Official Account (OA) API — gói dịch vụ từ 01/06/2026, gói nào cần cho API, loại tin nhắn & chi phí, OA trong nhóm (GMF)

### Takeaway
Nguồn **chính thức** (oa.zalo.me) xác nhận từ 01/06/2026 OA chuyển sang 4 gói Basic/Cơ bản – Standard/Tiêu chuẩn – Growth/Tăng trưởng – Comprehensive/Toàn diện; một snippet từ domain chính thức zalo.solutions nói **muốn liên kết ứng dụng với OA qua API phải dùng gói Tăng trưởng hoặc Toàn diện**. Giá cụ thể (Growth 2,5 triệu đ/năm…) hiện chỉ thấy qua snippet mà phần lớn là trang đại lý. OA **có** cơ chế nhóm chính thức (GMF, có API gửi tin/ webhook), gắn với gói Tăng trưởng/Toàn diện.

### Cited Findings
- Tin chính thức: "1/6/2026, Zalo Official Account triển khai 4 gói dịch vụ mới - tối ưu hiệu suất theo nhu cầu doanh nghiệp" và "[Chính thức] Quyền lợi và biểu phí các gói dịch vụ Zalo OA mới từ 1/6/2026" (CHÍNH THỨC) [DOC-snippet] — [oa.zalo.me/…_109742821673880689](https://oa.zalo.me/home/resources/news/162026-zalo-official-account-trien-khai-4-goi-dich-vu-moi-toi-uu-hieu-suat-theo-nhu-cau-doanh-nghiep-_109742821673880689), [oa.zalo.me/…_5100578039811031184](https://oa.zalo.me/home/resources/news/chinh-thuc-quyen-loi-va-bieu-phi-cac-goi-dich-vu-zalo-oa-moi-tu-162026-_5100578039811031184).
- Tên 4 gói: "Cơ bản - Tiêu chuẩn - Tăng trưởng - Toàn diện"; mua tại `zalo.solutions/oa/pricing` từ 12:00 ngày 01/06/2026 (CHÍNH THỨC) [DOC-snippet] — cùng 2 URL trên và [zalo.solutions/oa/pricing](https://zalo.solutions/oa/pricing).
- Từ 01/06/2026 dừng gia hạn gói cũ, mọi lần mua/gia hạn phải theo hệ 4 gói mới [DOC-snippet; không xác định được là trang chính thức hay đại lý] — kết quả gồm [oa.zalo.me news](https://oa.zalo.me/home/resources/news/162026-zalo-official-account-trien-khai-4-goi-dich-vu-moi-toi-uu-hieu-suat-theo-nhu-cau-doanh-nghiep-_109742821673880689), [v9.com.vn](https://v9.com.vn/bang-gia-zalo-oa-2026/) (RESELLER).
- **Điều kiện API** — snippet từ tìm kiếm *giới hạn domain zalo.solutions*: "Để liên kết ứng dụng với OA qua API, cần dùng gói Tăng trưởng (Growth) hoặc Toàn diện (Comprehensive)" (CHÍNH THỨC) [DOC-snippet] — trang liên quan: [zalo.solutions/business-message/guidelines/…/huong-dan-lien-ket-zalo-oa-vao-tai-khoan-zbs-va-uy-quyen-cho-ung-dung-appid](https://zalo.solutions/business-message/guidelines/en/huong-dan-lien-ket-zalo-oa-vao-tai-khoan-zbs-va-uy-quyen-cho-ung-dung-appid), [zalo.solutions/oa/pricing](https://zalo.solutions/oa/pricing). Không xác định được đoạn này nằm ở trang nào trong 2 trang.
- Định nghĩa trong bảng quyền lợi: "API Rate Limit = số request tối đa/phút một OA được gọi khi tích hợp Zalo OpenAPI (không gồm API gửi tin như ZBS Template Message)"; "Số App được ủy quyền = số ứng dụng tối đa một OA được ủy quyền" (CHÍNH THỨC) [DOC-snippet] — [zalo.solutions/oa/pricing](https://zalo.solutions/oa/pricing).
- Mâu thuẫn: một snippet (không lọc domain) nói gói Standard (1.000.000đ/12 tháng) có "tích hợp Zalo OpenAPI" [DOC-snippet, nguồn không xác định]; snippet khác (đại lý) nói "gói Basic và Standard không bật tính năng tích hợp Zalo Open API và không có API Rate Limit" (RESELLER) — [v9.com.vn/zalo-oa-trien-khai-4-goi-dich-vu-moi](https://v9.com.vn/zalo-oa-trien-khai-4-goi-dich-vu-moi/), [miniai.vn/so-sanh-goi-zalo-oa-cu-va-moi](https://miniai.vn/so-sanh-goi-zalo-oa-cu-va-moi/). Snippet từ domain chính thức (ở trên) nghiêng về "cần Growth trở lên".
- Giá (qua snippet, kết quả chủ yếu là đại lý): Basic miễn phí (mặc định cho OA đã xác thực); Standard 1.000.000đ/năm; Growth 2.500.000đ/12 tháng hoặc 1.400.000đ/6 tháng (gồm VAT); Comprehensive 6.000.000đ/năm (RESELLER/BLOG) [DOC-snippet] — [miniai.vn/bang-gia-zalo](https://miniai.vn/bang-gia-zalo/), [vihatsolutions.com/…/update-gia-goi-moi-zalo-oa](https://vihatsolutions.com/tin-cong-nghe/update-gia-goi-moi-zalo-oa/), [smsthuonghieu.com/goi-zalo-oa](https://www.smsthuonghieu.com/goi-zalo-oa/).
- Quyền lợi Growth (qua snippet, RESELLER): 500 tin tư vấn ngoài khung 48h/tháng, 10 kịch bản chatbot, 5 người trực MCC, ZCC không giới hạn, 15 tài khoản nhân viên, 1 nhóm GMF-100 miễn phí, tích hợp tối đa 3 ứng dụng qua API với rate limit 100 request/phút; vượt hạn mức tin tư vấn ngoài 48h: 55đ/tin [DOC-snippet] — [miniai.vn/so-sanh-goi-zalo-oa-cu-va-moi](https://miniai.vn/so-sanh-goi-zalo-oa-cu-va-moi/), [v9.com.vn/bang-gia-zalo-oa-2026](https://v9.com.vn/bang-gia-zalo-oa-2026/). **Chưa đối chiếu được với trang zalo.solutions.**
- Tin Tư vấn: gửi trong 48 giờ kể từ tương tác cuối của người dùng là miễn phí; ngoài 48 giờ tính phí theo bảng giá (CHÍNH THỨC) [DOC-snippet] — [oa.zalo.me/home/documents/guides/tin-tu-van](https://oa.zalo.me/home/documents/guides/tin-tu-van), [oa.zalo.me tổng quan các loại tin nhắn](https://oa.zalo.me/home/documents/guides/tong-quan-cac-loai-tin-nhan-tren-zalo-official-account-_3651713298729094511).
- "Công cụ OA OpenAPI có thể gửi tin Tư vấn đến người dùng trong vòng 07 ngày kể từ tương tác cuối của người dùng" (CHÍNH THỨC) [DOC-snippet] — cùng nhóm trang oa.zalo.me ở trên (không xác định chính xác trang).
- ZBS Template Message (tin theo mẫu) = hợp nhất tin UID Giao dịch, UID Truyền thông và ZNS, áp dụng từ 01/01/2026; có 2 loại chính Tin Giao dịch và Tin Hậu mãi; cấu trúc mới cho template tạo từ 27/02/2026, đơn giá mới cho template tạo từ 16/03/2026, áp dụng cho template cũ từ 24/03/2026 (dự kiến); gửi qua UID có giá thấp hơn gửi qua SĐT (CHÍNH THỨC) [DOC-snippet] — [zalo.solutions/business-message/pricing](https://zalo.solutions/business-message/pricing), [zalo.solutions thông báo cập nhật đơn giá ZBS](https://zalo.solutions/news/thong-bao-cap-nhat-cau-truc-va-don-gia-zbs-template-message/rb4ygyq8wdg7yvbue3qa7yli), [oa.zalo.me ZBS Template Message](https://oa.zalo.me/home/documents/guides/zbs-template-message).
- Số liệu cũ hơn (trước hệ gói 2026, RESELLER): 8 tin phản hồi miễn phí trong 48h; OA xác thực có 1000 tin miễn phí/tháng, từ tin 1001 giá 55đ/tin — [hotro.hana.ai](https://hotro.hana.ai/huong-dan-chinh-sach-gui-tin-va-quy-dinh-phi-gui-tin-cua-zalo-official-account/), [help.haravan.com](https://help.haravan.com/docs/social/integration/gioi-han-tin-nhan-duoc-gui-trong-harasocial-theo-cac-goi-dich-vu-tai-zalo-oa-ver-3/) [DOC-snippet] — **có thể đã lỗi thời sau 01/06/2026**.
- **GMF (nhóm chat của OA)**: "Tính năng Nhóm chat (GMF) là tính năng dành cho các OA đang sử dụng Gói Dịch vụ OA"; 4 loại GMF-10, GMF-50, GMF-100, GMF-1000 theo số thành viên; "Khi doanh nghiệp sử dụng Gói Dịch vụ Tăng trưởng/Toàn diện, mỗi gói sẽ có sẵn một số lượng nhóm"; với nhóm có sẵn theo gói, OA không phát sinh phí duy trì và phí tin nhắn từ OA vào nhóm trong thời hạn gói (CHÍNH THỨC) [DOC-snippet] — [oa.zalo.me/…/quan-ly-nhom-gmf](https://oa.zalo.me/home/documents/guides/quan-ly-nhom-gmf_1954166378348758227), [chính sách GMF](https://oa.zalo.me/home/documents/policy/tinh-nang-quan-ly-nhom).
- Chính sách GMF cũ (trước 2026): gói Advanced có 1 nhóm GMF-100, Premium có 3; mua thêm 25.000đ–300.000đ/tháng tuỳ loại [DOC-snippet] — cùng trang GMF trên (nội dung có thể đã cũ).
- **GMF có API chính thức**: tài liệu developers.zalo.me có mục "nhom-chat-gmf" gồm gửi tin nhóm dạng Text, Hình ảnh, Mention; quản lý nhóm (cập nhật dịch vụ cho nhóm); webhook "tin nhắn được gửi tới nhóm", "thành viên mới tham gia nhóm", "tạo nhóm OA" (CHÍNH THỨC) [DOC-snippet] — [tổng quan GMF](https://developers.zalo.me/docs/official-account/nhom-chat-gmf/general), [gửi text](https://developers.zalo.me/docs/official-account/nhom-chat-gmf/tin-nhan/text_message), [mention](https://developers.zalo.me/docs/official-account/nhom-chat-gmf/tin-nhan/mention_uid), [webhook tin nhóm](https://developers.zalo.me/docs/official-account/webhook/nhom-chat-gmf/messgae_webhook), bản mới trên Document Hub: [docs.zaloplatforms.com/…/nhom-chat-gmf/message_webhook](https://docs.zaloplatforms.com/docs/OA/webhook/nhom-chat-gmf/message_webhook).
- Mã cộng đồng dùng OA OpenAPI: `@elizaos/plugin-zalo` gọi `https://openapi.zalo.me/v2.0/oa` và OAuth `https://oauth.zaloapp.com/v4` [MÃ] (tarball npm 2.0.0-alpha); `zca-bridge` có module `src/zalo-oa/consultationWindow.ts`, `consultationTracker.ts` (quản lý cửa sổ tư vấn) [CHẠY: ls-tree] — [github.com/diendh/zca-bridge](https://github.com/diendh/zca-bridge).

### Inferences
- Với khách hàng, OA là kênh "đúng luật" duy nhất có cả chat tư vấn (miễn phí trong cửa sổ 48h), tin chủ động theo mẫu (ZBS Template/ZNS, trả phí) và nhóm cộng đồng (GMF) có API; nhưng để agent gọi API thì gần như chắc chắn cần gói **Growth (~2,5 triệu đ/năm)** trở lên.
- GMF là nhóm **do OA tạo/quản lý**, không phải cho OA chui vào nhóm Zalo thường có sẵn — suy luận từ mô tả "tạo nhóm OA", "GMF-10/50/100/1000" (chưa đọc được trang gốc để khẳng định).

### Gaps
- Không mở được `zalo.solutions/oa/pricing` và bài "[Chính thức] Quyền lợi và biểu phí…" → chưa đối chiếu trực tiếp bảng quyền lợi (rate limit từng gói, số app được ủy quyền, số nhóm GMF từng gói, hạn mức tin ngoài 48h).
- Đơn giá cụ thể ZBS Template Message 2026 (đ/tin) chưa lấy được.
- Chưa xác minh GMF API có yêu cầu gói nào (ngoài câu "Tăng trưởng/Toàn diện có sẵn một số nhóm").

---

## 3. Tài khoản cá nhân qua zca-js (không chính thức) — repo, license, bảo trì, bằng chứng bị khoá, điều khoản Zalo

### Takeaway
zca-js (MIT, RFS-ADRENO) vẫn được bảo trì tích cực (v2.2.0 ngày 09/09/2026) và tự cảnh báo có thể bị khoá/ban; điều khoản Zalo cấm đăng nhập bằng phần mềm bên thứ ba không được Zalo chấp thuận. Không tìm được báo cáo khoá tài khoản cụ thể nào có bằng chứng — rủi ro là **theo điều khoản và cảnh báo**, chưa có số liệu.

### Cited Findings
- Repo `github.com/RFS-ADRENO/zca-js`; `package.json`: `"name": "zca-js", "version": "2.2.0", "description": "Unofficial Zalo API for JavaScript"`; LICENSE: MIT, "Copyright (c) 2024 - 2025 RFS-ADRENO, truong9c2208, JustKemForFun" [MÃ] (clone HEAD `dadfef1`, 09/09/2026).
- README: "> [!NOTE] This is an unofficial Zalo API for personal account. It work by simulating the browser to interact with Zalo Web." và "> [!WARNING] Using this API could get your account locked or banned. We are not responsible for any issues that may happen. Use it at your own risk." [MÃ] (README.md dòng 3–7).
- Bảo trì: commit gần nhất 09/09/2026 "chore: bump to v2.2.0" và "feat(api): add new apis (#327)"; trước đó 17/03/2026 v2.1.2 [CHẠY: git log]. npm: tạo 15/07/2024, 63 phiên bản, bản mới nhất 2.2.0 ngày 09/09/2026 [CHẠY: registry.npmjs.org/zca-js].
- Issue vẫn hoạt động tháng 9/2026 (#379 ngày 22/09/2026, #376 ngày 19/09/2026 báo lỗi `ZcaApiError`) — [issues zca-js](https://github.com/RFS-ADRENO/zca-js/issues?q=is%3Aissue+ban+OR+locked+OR+kh%C3%B3a) [DOC]. Tìm "ban OR locked OR khóa" trong issues: **không có issue nào có tiêu đề báo bị khoá** [DOC].
- Discussion #335 "Đã có bác nào xài library này mà bị ban tài khoản chưa?" (aperture147, 26/04/2026): hỏi về việc dùng thay OA để gửi thông báo cho khách, lo bị ban; **0 trả lời** tại thời điểm xem — [discussion #335](https://github.com/RFS-ADRENO/zca-js/discussions/335) [DOC].
- Dự án zca-bridge (Zalo ↔ Chatwoot, Apache-2.0) cảnh báo: "Dùng API không chính thức có thể khiến tài khoản Zalo bị hạn chế, khóa hoặc cấm vĩnh viễn" — [github.com/diendh/zca-bridge](https://github.com/diendh/zca-bridge) [DOC]; hermes-zalo-plugin: "⚠️ zca-js is UNOFFICIAL. Use a secondary Zalo account." [MÃ: README.md, clone cuongdev/hermes-zalo-plugin].
- Điều khoản sử dụng Zalo: "cấm đăng nhập và sử dụng Dịch Vụ bằng một phần mềm tương thích của bên thứ ba hoặc hệ thống không được phát triển, cấp quyền hoặc chấp thuận bởi Zalo" (CHÍNH THỨC) [DOC-snippet] — [zalo.vn/dieukhoan](https://zalo.vn/dieukhoan/).
- Trang trợ giúp Zalo: lý do tài khoản bị tạm vô hiệu hoá gồm "sử dụng tài khoản bằng các công cụ, phần mềm bên thứ 3 không được phát hành bởi Zalo" (CHÍNH THỨC) [DOC-snippet] — [help.zalo.me — Tài khoản Zalo bị tạm thời vô hiệu hóa](https://help.zalo.me/huong-dan/chuyen-muc/quan-ly-tai-khoan-zalo/loi-thuong-gap/tai-khoan-zalo-bi-tam-thoi-vo-hieu-hoa/).
- Blog bán công cụ khuyên ngưỡng "an toàn" 20 tin/phút, 200–500 tin/ngày cho tài khoản cũ — (RESELLER/BLOG, không có cơ sở chính thức) [DOC-snippet] — [aizalo.com](https://aizalo.com/blog/cach-gui-tin-nhan-tu-dong-tren-zalo-khong-bi-khoa).
- Các bản port: Python `zca-py` 1.0.0 (19/09/2025, JustKemForFun, "Unofficial Zalo API for Python") [CHẠY: PyPI JSON]; Go `zcago` (github.com/amrakk/zcago, MIT theo ghi chú trong GoClaw) — GoClaw port từ đây (mục 7) [MÃ]; trạng thái bảo trì zcago chưa kiểm [?].

### Inferences
- Dùng zca-js cho kênh khách hàng/Marketing là vi phạm điều khoản Zalo (về mặt câu chữ) — rủi ro khoá tài khoản không đo được nhưng có thật; tài khoản cá nhân của nhân viên/số hotline kinh doanh **không nên** dùng.
- Việc thiếu báo cáo ban công khai có thể do người bị ban không báo lên GitHub (thiên lệch sống sót), không nên hiểu là an toàn.

### Gaps
- Không truy cập được Viblo/J2Team/Facebook groups → không có báo cáo ban cụ thể từ cộng đồng VN.
- Chưa đọc toàn văn điều khoản (zalo.vn/dieukhoan bị chặn) — chỉ có snippet.

---

## 4. OpenClaw: kênh `zalo` (Bot API) và `zalouser` (zca-js)

### Takeaway
Xác minh bằng mã: `zalo` = Zalo Bot Platform chính thức (`bot-api.zaloplatforms.com`), docs ghi "Status: experimental"; `zalouser` = tài khoản cá nhân qua zca-js 2.2.0, docs ghi "Status: experimental" + cảnh báo có thể bị khoá/ban. Tài liệu kênh `zalo` **đã đổi** ngày 05/07/2026: từ "chỉ DM, nhóm không dùng được thực tế" sang "DM và nhóm đều đã hiện thực (mention-gated)" kèm cảnh báo có nơi không thêm được bot vào nhóm.

### Cited Findings
- `extensions/zalo/package.json`: `"name": "@openclaw/zalo", "version": "2026.9.6", "description": "OpenClaw Zalo channel plugin for bot and webhook chats."` [MÃ] (openclaw HEAD `96e4061`, 27/09/2026 03:41 UTC).
- `extensions/zalo/src/api.ts:3` `@see https://bot.zaloplatforms.com/docs`; `:15` `const ZALO_API_BASE = "https://bot-api.zaloplatforms.com"` [MÃ].
- `docs/channels/zalo.md` (bản hiện tại): "Status: experimental. Direct messages and group chats are both implemented."; "Groups require an @mention to trigger the bot"; "Reported real-world caveat: on some Marketplace-bot setups the bot could not be added to a group at all… It is a platform-side constraint"; "This page covers Zalo Bot Creator / Marketplace bots. Zalo Official Account (OA) bots are a different product surface… This page does not cover them." [DOC].
- Bản trước (commit `00ad13b`, trước 01/07/2026): "Status: experimental. DMs are supported." và "For Zalo Bot Creator / Marketplace bots, group support was not available in practice because the bot could not be added to a group at all." [CHẠY: git show]. Doc được viết lại ở commit 05/07/2026 "docs: rewrite published docs grounded in current source (#100142)" [CHẠY: git log].
- `extensions/zalouser/package.json`: `"@openclaw/zalouser"` 2026.9.6, `"dependencies": {"zca-js": "2.2.0", …}`, mô tả "OpenClaw Zalo Personal Account plugin via native zca-js integration." [MÃ].
- `docs/channels/zalouser.md`: "Status: experimental. This integration automates a personal Zalo account via native zca-js…"; "<Warning> This is an unofficial integration and may result in account suspension or ban. Use at your own risk."; "Zalo Personal is an official external plugin, not bundled in core" (cài bằng `openclaw plugins install @openclaw/zalouser`); nhóm mặc định `groupPolicy = "allowlist"`; "Streaming is not supported"; "`zalo` is reserved for a potential future official Zalo API integration." [DOC].
- npm: `@openclaw/zalo` và `@openclaw/zalouser` bản 2026.9.6 phát hành 23/09/2026 [CHẠY: npm registry search].
- Hệ sinh thái OpenClaw còn nhiều plugin cộng đồng khác (npm): `openclaw-zalo-connect` 3.1.5 (07/09/2026, "via zca-js"), `zaloclaw` 2.5.11 (25/07/2026, zca-js), `zalo-personal` 2.4.2 (15/07/2026, zca-js), `openzca` 0.1.59 (CLI tương thích zca), `@mnemo-bot/zalo-oa` 0.1.0 (10/06/2026, "Zalo Official Account plugin (Open Platform v3.0) for OpenClaw"), `openclaw-zalo-mod` 2.31.2 (quản trị nhóm, dựa trên "Zalo Connect"/ZCA) [CHẠY: npm registry search; README openclaw-zalo-mod đọc qua git].

### Inferences
- Khẳng định "docs zalo ghi experimental" vẫn đúng ở 27/09/2026; nhưng mô tả nhóm của OpenClaw (hiện thực phía client) và mô tả của Zalo (tính năng nhóm thử nghiệm nội bộ) không mâu thuẫn: OpenClaw đã viết code sẵn cho nhóm, còn phía Zalo chưa mở rộng rãi.

### Gaps
- Không mở được docs.openclaw.ai (bị chặn) — đã đọc bản nguồn `docs/channels/*.md` trong repo thay thế.

---

## 5. Plugin "chính thức của Zalo" cho OpenClaw (Zalo ClawBot, kết nối bằng quét QR)

### Takeaway
**Tồn tại và xác minh được**: gói npm `@zalo-platforms/openclaw-zaloclawbot` (MIT, author "Zalo Platforms", v0.1.0 ngày 19/05/2026 → v0.1.4 ngày 17/06/2026), OpenClaw thêm trang docs ngày 19/06/2026, báo chí đưa tin Zalo công bố ngày 30/06/2026. Plugin dùng Bot Platform chính thức, đăng nhập bằng QR qua Zalo Mini App, **chỉ nhận chat riêng (PRIVATE) và chỉ nói chuyện với chủ bot** — không hỗ trợ nhóm.

### Cited Findings
- npm `@zalo-platforms/openclaw-zaloclawbot`: license MIT; `author: {"name": "Zalo Platforms"}`; maintainer npm `ken-kuro`; **không có trường repository/homepage**; các bản: 0.1.0 (19/05/2026), 0.1.1 (02/06/2026), 0.1.2 và 0.1.3 (17/06/2026), 0.1.4 (17/06/2026, `latest`); dependency duy nhất `qrcode-terminal` [CHẠY: registry.npmjs.org].
- README gói: "Official Zalo channel plugin for OpenClaw. Connect a personal Zalo bot to your OpenClaw agent with a QR-scan login — owner-bound, no webhook setup, no developer credentials."; "Owner-bound — the bot talks only to its owner; messages from others are dropped at the platform level."; "Ban-safe — it uses official Bot Platform APIs"; nhắc thêm gói `@zalo-platforms/openclaw-zaloclawbot-cli` [DOC] (README trong tarball npm).
- Mã (tarball 0.1.4) [MÃ]:
  - `dist/src/api/api.js:1` `DEFAULT_ZALO_API_BASE = "https://bot-api.zaloplatforms.com"` — dùng `getMe`, `sendMessage`, `sendChatAction`, `setWebhook`, `deleteWebhook`, `getWebhookInfo`, `getUpdates`.
  - `dist/src/auth/login-qr.js`: `DEFAULT_SESSION_SERVICE_URL = "https://bot.zaloplatforms.com"`, gọi `GET /agent/request-login` (trả `loginUrl`, `zbsk`) và poll `GET /agent/get-login-status?zbsk=…`; `ZBSK_TTL_MS = 5 * 60_000`; HTTP 498 = QR hết hạn.
  - `dist/src/channel.js:74` `chatTypes: ["direct"]`; `dist/src/messaging/inbound.js:12` `if (msg.chat?.chat_type !== "PRIVATE")` → bỏ qua mọi tin không phải chat riêng.
- OpenClaw `docs/channels/zaloclawbot.md`: "OpenClaw connects to Zalo ClawBot through the catalog-listed external `@zalo-platforms/openclaw-zaloclawbot` plugin. Login uses a Zalo Mini App QR code"; bảng tương thích "0.1.4 | >=2026.4.10 | latest | Active / Beta"; "the QR code resolves to a Zalo Mini App that binds a newly provisioned, private bot under a shared official OA directly to your Zalo user ID"; "the bot only communicates with its owner. Messages from other users are dropped at the platform level"; ghi chú "Behavior details on this page beyond install and config are as reported by the plugin's maintainers and are not verified against OpenClaw core source." [DOC]. Trang được thêm ngày 19/06/2026 ("feat(channels): add Zalo ClawBot external channel entry and documenta… (#89586)") [CHẠY: git log].
- Báo chí: "Ngày 30/06/2026, Zalo cho biết hãng phát triển plugin cho OpenClaw"; plugin "đã được công bố chính thức trên website của OpenClaw"; kết nối "bằng thao tác quét mã QR"; cho phép "ra lệnh cho AI Agent thực hiện việc soạn và gửi tin nhắn qua Zalo" [DOC-snippet] — [znews.vn](https://znews.vn/zalo-cap-nhat-phuong-thuc-ket-noi-den-openclaw-post1664688.html), [tienphong.vn](https://tienphong.vn/zalo-cap-nhat-phuong-thuc-ket-noi-den-openclaw-don-gian-hoa-trai-nghiem-voi-agentic-ai-post1855677.tpo), bài gốc trên blog chính thức Zalo (CHÍNH THỨC, không mở được): [zalo.me/vi/blog/…](https://zalo.me/vi/blog/zalo-cap-nhat-phuong-thuc-ket-noi-den-openclaw-don-gian-hoa-trai-nghiem-voi-agentic-ai). Quy trình 3 bước: cài plugin Zalo ClawBot → quét QR bằng Zalo để tạo "My ClawBot" → chat nhờ ClawBot hỗ trợ [DOC-snippet] — [baomoi.com](https://baomoi.com/zalo-cap-nhat-phuong-thuc-ket-noi-den-openclaw-c55512453.epi).

### Inferences
- "Chính thức của Zalo" được củng cố bởi 3 dấu hiệu độc lập: scope npm `@zalo-platforms` + author "Zalo Platforms", việc OpenClaw liệt kê trong catalog, và bài trên blog zalo.me. Không có chữ ký/repo công khai để kiểm chứng nguồn gốc mã; mã chỉ phát hành dạng `dist` (có `index.ts` gốc).
- Lọc "chỉ chủ bot" nằm **phía nền tảng Zalo** (theo tuyên bố); phía mã plugin chỉ lọc "PRIVATE". Kết hợp lại: không dùng được cho khách, không dùng được cho nhóm, mỗi nhân viên muốn dùng phải có bot riêng gắn với tài khoản mình → chỉ hợp "trợ lý cá nhân", không hợp gateway đa người dùng như GoClaw.
- Plugin chỉ chạy trong OpenClaw (phụ thuộc SDK plugin OpenClaw ≥ 2026.4.10); cơ chế "đăng nhập QR → cấp bot" dùng endpoint `bot.zaloplatforms.com/agent/*` chưa có tài liệu công khai — [?] liệu nền tảng khác (như GoClaw) có được phép dùng lại hay không.

### Gaps
- Ngày chính xác "30/06/2026" là ngày thông báo báo chí; bản npm đầu tiên có từ 19/05/2026 → "phát hành ngày 30/06/2026" là ngày công bố, không phải ngày phát hành mã.
- Không xác minh được maintainer `ken-kuro` có phải nhân viên VNG hay không.
- Điều khoản sử dụng hiện trong Mini App khi quét QR: không xem được.

---

## 6. Các nền tảng / framework agent khác đã có adapter Zalo

### Takeaway
Ngoài OpenClaw và GoClaw, **có** thêm nền tảng có connector Zalo được liệt kê chính thức trong repo của họ: **elizaOS** (catalog curated: `@elizaos/plugin-zalo` dùng OA OpenAPI, `@elizaos/plugin-zalouser` dùng CLI `zca`), **AgentOS** (framersai, kênh Zalo Bot API trong registry curated), **Vercel Chat SDK** (adapter cộng đồng dùng Bot Platform, được liệt kê trong docs). Hermes Agent, n8n, Chatwoot chỉ có qua plugin/bridge **bên thứ ba**. AstrBot, LangBot, Dify, Botpress, Rasa, Typebot, Flowise: **không thấy** adapter Zalo.

### Cited Findings
(Phương pháp: clone chỉ-cây (`--filter=blob:none --no-checkout`) rồi `git ls-tree -r HEAD --name-only | grep -i zalo` — chỉ bắt được *tên file*, không bắt được nhắc tên trong nội dung [CHẠY]; kết hợp npm registry search + tải tarball đọc mã.)

| Nền tảng | Có Zalo? | Gói / vị trí | Đường API | Bảo trì (mốc gần nhất) | Bằng chứng |
|---|---|---|---|---|---|
| **elizaOS** | Có (catalog curated, nguồn "store", `render.visible: false`) | `packages/core/src/catalog/curated/connectors/zalo.json` → `@elizaos/plugin-zalo`; `zalouser.json` → `@elizaos/plugin-zalouser` (catalog ghi 2.0.0-beta.0; npm latest 2.0.0-alpha) | plugin-zalo: **OA OpenAPI** `https://openapi.zalo.me/v2.0/oa` + `https://oauth.zaloapp.com/v4`; plugin-zalouser: `spawn("zca", …)` — cần `npm install -g zca-cli` (zca/tài khoản cá nhân, không chính thức) | repo eliza HEAD 26/09/2026; npm plugin sửa 16/06/2026 | [MÃ] catalog JSON + tarball npm (`dist/index.js:14,16,4208,4522,4890`) |
| **AgentOS (framersai)** | Có (registry curated) | `registry/curated/channels/zalo/*` trong framersai/agentos-extensions; npm `@framers/agentos-ext-channel-zalo` 0.1.0 (19/02/2026, MIT) | **Zalo Bot API** ("Zalo Bot API — text messaging with optional webhook or long-polling", secret `zalo.botToken`) | repo HEAD 05/08/2026 | [CHẠY] ls-tree; [MÃ] manifest.json |
| **Vercel Chat SDK** | Có — adapter **cộng đồng** được liệt kê trong docs chính thức | `apps/docs/content/adapters/community/zalo.mdx` trong vercel/chat → gói `chat-adapter-zalo` 0.1.0 (06/04/2026, MIT, buiducnhat) | **Zalo Bot Platform** (DM có, mentions có, streaming "Buffered") | adapter commit cuối 06/04/2026; vercel/chat HEAD 24/09/2026 | [DOC] zalo.mdx; [CHẠY] npm |
| **FasedAgent** | Có | npm `@fased/zalo` 0.1.76-rc.4 (13/08/2026, không ghi license/repo) | **Zalo Bot API** (`bot-api.zaloplatforms.com`, `chat_type: "PRIVATE" \| "GROUP"`) — cấu trúc mã giống OpenClaw | 13/08/2026 | [MÃ] tarball `src/api.ts:32`, `src/monitor.ts:314` |
| **Hermes Agent (NousResearch)** | Không có sẵn trong repo (ls-tree chỉ ra 1 file email không liên quan) | Plugin bên thứ ba: `hermes-zalo-plugin` (cuongdev, MIT, npm 1.0.9 04/07/2026, commit cuối 26/07/2026); fork `@ai.vn/hermes-zalo-gateway` (thodinh, 1.0.1, 30/08/2026); `abs-zalo-bot` (teddiesloco, MIT, 0.11.1 24/09/2026, có `hermes-plugin/platforms/zalo/adapter.py`, MCP) | hermes-zalo-plugin: **zca-js** (bridge Node + zca-js); abs-zalo-bot: **zca-js (QR cá nhân) + OA webhook** | hermes-agent HEAD 26/09/2026 | [CHẠY] ls-tree, npm; [MÃ] README |
| **n8n** | Không có node sẵn (n8n-io/n8n HEAD 27/09/2026) | Hàng chục community node: `n8n-nodes-zalo-platform` (hecigo, 2.0.1, 11/09/2026), `n8n-nodes-zalo-bot-official` (1.1.8, 31/07/2026), `n8n-nodes-zalo-gemazo` (0.10.64, 29/08/2026), `@bautran1911/n8n-nodes-zalo-oa` (1.0.19, 20/05/2026), `n8n-nodes-zalo-tokado` (0.2.7, 27/09/2026)… | Bot Platform (hecigo, bot-official); zca-js + Bot Platform (gemazo); OA ZBS Template (bautran1911); zca-js (tokado, nhiều gói khác) | xem cột trước | [CHẠY] ls-tree + npm |
| **Chatwoot** | Không có sẵn (chatwoot HEAD 25/09/2026); có issue #3372 "Adding Zalo as a messaging channel", discussion #8457 | Bridge bên thứ ba `zca-bridge` (diendh, Apache-2.0, commit cuối 23/09/2026; fork xzneozx96 19/06/2026) | **OA API + zca-js** | 23/09/2026 | [CHẠY] ls-tree; [DOC] [issue #3372](https://github.com/chatwoot/chatwoot/issues/3372), [zca-bridge](https://github.com/diendh/zca-bridge) |
| **AstrBot** | Không thấy (HEAD 27/09/2026; tìm web không thấy plugin) | — | — | — | [CHẠY] ls-tree; [DOC-snippet] |
| **LangBot** | Không thấy (HEAD 27/09/2026; danh sách nền tảng hỗ trợ không có Zalo) | — | — | — | [CHẠY] ls-tree; [DOC-snippet] [LangBot README](https://github.com/langbot-app/LangBot) |
| **Dify** | Không thấy trong `langgenius/dify-plugins` (HEAD 26/09/2026) | — | — | — | [CHẠY] ls-tree (marketplace.dify.ai bị chặn) |
| **Botpress** | Không thấy (HEAD 23/09/2026) | — | — | — | [CHẠY] ls-tree |
| **Rasa** | Không thấy; repo RasaHQ/rasa commit cuối 18/12/2025 | — | — | — | [CHẠY] ls-tree |
| **Typebot** | Không thấy (HEAD 24/09/2026) | — | — | — | [CHẠY] ls-tree |
| **Flowise** | Không thấy (HEAD 13/08/2026) | — | — | — | [CHẠY] ls-tree |

- Khác: MCP server `@gyga-browser/webmcp-zalo-notify` 0.1.0 (18/07/2026) gửi thông báo qua Zalo Bot (`sendMessage/sendPhoto/sendChatAction`) [CHẠY: npm]. PyPI: `PyZALO` 0.1.0 (17/08/2026, "Python library for Zalo OA Bot", tài liệu trỏ `bot.zaloplatforms.com/docs`), `python-zalo-bot` 0.1.9 (27/01/2026), `zlapi` 1.0.3 (23/11/2024, API cá nhân không chính thức), `zca-py` 1.0.0 [CHẠY: PyPI JSON API]. (Trang tìm kiếm pypi.org bị chặn bởi JS challenge → chỉ tra được theo tên đoán.)

### Inferences
- Nhận định "ngoài OpenClaw và GoClaw không có nền tảng nào có Zalo sẵn" là **sai** ở 27/09/2026: elizaOS và AgentOS có connector Zalo trong catalog/registry chính thức của họ; Chat SDK liệt kê adapter cộng đồng.
- Mẫu hình chung: gần như mọi adapter mới (2026) cho *chính thức* đều dùng Zalo Bot Platform; OA OpenAPI hiếm (elizaOS, `@mnemo-bot/zalo-oa`, zca-bridge, node n8n OA); nhóm thì hầu như chỉ đạt được qua zca-js.

### Gaps
- Kiểm tra theo tên file có thể bỏ sót adapter nằm trong file không chứa chữ "zalo" (ví dụ cấu hình chung). AstrBot/LangBot marketplace plugin (ngoài repo chính) chỉ tra qua web search.
- Chưa kiểm được Dify Marketplace trực tiếp (bị chặn).

---

## 7. GoClaw (repo cục bộ /home/user/goclaw) — hai hiện thực Zalo gọi API nào

### Takeaway
GoClaw có 2 kênh: `zalo_oa` ("Zalo OA") và `zalo_personal`. **Tên "Zalo OA" gây hiểu nhầm**: mã gọi **Zalo Bot API** (`bot-api.zaloplatforms.com`), không gọi OA OpenAPI (`openapi.zalo.me`), và chỉ DM. `zalo_personal` là port Go của giao thức Zalo Web (từ `zcago`, bản Go của hướng zca-js) — không chính thức, hỗ trợ nhóm, có cảnh báo khoá tài khoản.

### Cited Findings
- Hằng loại kênh: `internal/channels/channel.go:83` `TypeZaloOA = "zalo_oa"`, `:84` `TypeZaloPersonal = "zalo_personal"` [MÃ].
- `internal/channels/zalo/zalo.go:1-5`: "Package zalo implements the Zalo OA Bot channel. Ported from OpenClaw TS extensions/zalo/. Zalo Bot API: https://bot-api.zaloplatforms.com. DM only (no groups), text limit 2000 chars, polling + webhook modes." [MÃ].
- `zalo.go:37` `var apiBase = "https://bot-api.zaloplatforms.com"`; `:443` URL `"%s/bot%s/%s"`; method gọi: `getMe` (`:486`), `getUpdates` (`:506`), `sendMessage` (`:527`), `sendPhoto` (`:540`); `handleTextMessage` ghi "DM policy enforcement (Zalo is DM-only)" và luôn đẩy `"direct"` (`~:211-233`) [MÃ]. Không có lời gọi `setWebhook` → khớp với issue #1542 ("webhook_url/webhook_secret là config chết") [MÃ] + [DOC] [issue #1542](https://github.com/nextlevelbuilder/goclaw/issues/1542).
- `internal/channels/zalo/personal/channel.go:20-21`: "Channel connects to Zalo Personal Chat via the internal protocol port (from zcago, MIT). WARNING: Zalo Personal is an unofficial, reverse-engineered integration. Account may be locked/banned."; `:99-101` log `slog.Warn("security.unofficial_api", …)` khi khởi động [MÃ].
- `personal/protocol/crypto.go:2` "Ported from zcago (MIT license): https://github.com/amrakk/zcago"; `protocol/client.go:64,118` ghi port từ `zcago/internal/httpx` [MÃ].
- Endpoint của `zalo_personal` (grep) [MÃ]: `https://id.zalo.me/account/authen/qr/generate`, `…/qr/waiting-scan`, `…/qr/waiting-confirm`, `https://id.zalo.me/account/checksession`, `https://wpa.chat.zalo.me/api/login/getLoginInfo`, `…/getServerInfo`, `https://jr.chat.zalo.me/jr/userinfo`, `wss://ws1.zalo.me`, `wss://ws2.zalo.me`, `https://group1.zalo.me`, `https://file1.zalo.me`, `https://chat1.zalo.me` — tức giả lập Zalo Web (đăng nhập QR, WebSocket).
- Nhóm ở `zalo_personal`: `personal/policy.go:31-43` `checkGroupPolicy` (allowlist/pairing); `:71-72` chọn `protocol.ThreadTypeGroup` cho đích `group:` [MÃ].
- Tài liệu GoClaw `docs/05-channels-messaging.md:640-673`: "The Zalo OA (Official Account) channel connects to the Zalo OA Bot API… DM only: No group support"; bảng so sánh ghi Zalo OA "Protocol: Official Bot API… Risk: None", Zalo Personal "Reverse-engineered (zcago, MIT)… Group support: Yes… Account may be locked/banned" [DOC].
- Phiên bản: repo cục bộ HEAD `4d3c6bc` (04/07/2026); upstream `nextlevelbuilder/goclaw` HEAD `16ba6a5` (26/09/2026) — `zalo.go` upstream vẫn `apiBase = "https://bot-api.zaloplatforms.com"` và "DM only"; commit Zalo gần nhất upstream là 09/07/2026 (#1402, nhóm của kênh personal) [CHẠY: git clone + git log].
- Issue mở ngày 30/08/2026: #1542 (webhook không dùng), #1543 (hỗ trợ nhóm cho Zalo Bot — chờ Zalo ra mắt), #1544 (sai sót tài liệu về nguồn token và xác thực webhook) — [#1542](https://github.com/nextlevelbuilder/goclaw/issues/1542), [#1543](https://github.com/nextlevelbuilder/goclaw/issues/1543) [DOC].

### Inferences
- GoClaw hiện **không có** tích hợp OA OpenAPI thật (không tư vấn khách qua OA, không ZBS/ZNS, không GMF). Muốn dùng OA cho khách hàng phải viết adapter mới (tham khảo `@elizaos/plugin-zalo`, `@mnemo-bot/zalo-oa`, `zca-bridge/src/zalo-oa/*`).
- Kênh `zalo_oa` của GoClaw thực chất ngang tầm kênh `zalo` của OpenClaw trước 05/07/2026 (chỉ DM, chỉ polling).

### Gaps
- Chưa kiểm GoClaw web UI (`ui/web`) hiển thị tên "Zalo OA" thế nào và hướng dẫn nhập token gì (ngoài phạm vi; issue #1544 nói có sai sót tài liệu).

---

## 8. Kiểm lại các khẳng định của phiên trước

### Takeaway
3 khẳng định đúng (có sắc thái), 1 khẳng định đúng một phần (tên "Zalo OA" của GoClaw sai bản chất), 1 khẳng định sai (đã có nền tảng khác có Zalo), và 1 khẳng định "chưa kiểm" nay đã xác minh đúng bằng mã.

### Cited Findings
| # | Khẳng định phiên trước | Kết luận | Bằng chứng |
|---|---|---|---|
| 1 | OpenClaw có 3 đường: `zalo` (Zalo Bot API chính thức, docs ghi experimental), `zalouser` (zca-js không chính thức, docs cảnh báo khoá tài khoản), và plugin chính thức Zalo phát hành 30/6/2026 kết nối bằng quét QR | **Đúng** (bổ sung: plugin là gói ngoài `@zalo-platforms/openclaw-zaloclawbot`; bản npm đầu 19/05/2026, docs OpenClaw 19/06/2026, **30/06/2026 là ngày Zalo công bố**; ngoài ra còn nhiều plugin cộng đồng khác nên "3 đường" chưa đầy đủ) | [MÃ] `extensions/zalo/src/api.ts:15`, `extensions/zalouser/package.json`; [DOC] `docs/channels/zalo.md`, `zalouser.md`, `zaloclawbot.md`; [CHẠY] npm; [DOC-snippet] [znews](https://znews.vn/zalo-cap-nhat-phuong-thuc-ket-noi-den-openclaw-post1664688.html) |
| 2 | Plugin chính thức của Zalo chỉ chat riêng với chủ tài khoản (chưa kiểm) | **Đúng** (nay đã kiểm): mã bỏ mọi tin không phải `PRIVATE`, `chatTypes: ["direct"]`; README + docs OpenClaw: "the bot only communicates with its owner… dropped at the platform level" (phần "chỉ chủ" là tuyên bố của maintainer, lọc phía nền tảng) | [MÃ] `dist/src/messaging/inbound.js:12`, `dist/src/channel.js:74`; [DOC] README npm, `docs/channels/zaloclawbot.md` |
| 3 | Tài liệu Zalo mô tả bot vào nhóm nhưng ghi đang thử nghiệm nội bộ (chưa kiểm) | **Đúng** tới ít nhất 30/08/2026 (issue #1543 trích nguyên văn "Tính năng đang trong giai đoạn thử nghiệm nội bộ"; snippet trang docs.zaloplatforms.com cùng nội dung). Trạng thái đúng ngày 27/09/2026: chưa kiểm được trực tiếp. Lưu ý: docs **OpenClaw** đã đổi (05/07/2026) sang "groups supported (mention-gated)" | [DOC] [#1543](https://github.com/nextlevelbuilder/goclaw/issues/1543); [DOC-snippet] [docs.zaloplatforms.com](https://docs.zaloplatforms.com/docs/BOT/best-practices/build-bot-interaction-with-group); [CHẠY] git log OpenClaw |
| 4 | Gói Zalo OA đổi từ 1/6/2026; API cần gói Growth trở lên (nguồn là reseller) | **Đúng** — nay có nguồn Zalo chính thức (qua snippet): oa.zalo.me xác nhận 4 gói từ 01/06/2026; snippet domain zalo.solutions: "liên kết ứng dụng với OA qua API cần gói Tăng trưởng hoặc Toàn diện". Còn 1 snippet mâu thuẫn nói Standard có OpenAPI → cần đối chiếu trực tiếp bảng giá | [DOC-snippet] [oa.zalo.me news](https://oa.zalo.me/home/resources/news/162026-zalo-official-account-trien-khai-4-goi-dich-vu-moi-toi-uu-hieu-suat-theo-nhu-cau-doanh-nghiep-_109742821673880689), [zalo.solutions/oa/pricing](https://zalo.solutions/oa/pricing) |
| 5 | GoClaw có cả Zalo OA và Zalo Personal | **Đúng một phần / tên gây hiểu nhầm**: có 2 kênh `zalo_oa` và `zalo_personal`, nhưng `zalo_oa` gọi **Zalo Bot API** (`bot-api.zaloplatforms.com`), chỉ DM, **không** dùng OA OpenAPI | [MÃ] `internal/channels/zalo/zalo.go:1-5,37`; `internal/channels/channel.go:83-84` |
| 6 | Ngoài hệ OpenClaw và GoClaw, không tìm thấy nền tảng nào có Zalo sẵn | **Sai** (ở 27/09/2026): elizaOS (catalog curated `zalo`/`zalouser`), AgentOS (registry curated channel zalo), Vercel Chat SDK (adapter cộng đồng được liệt kê trong docs), FasedAgent (`@fased/zalo`); thêm Hermes/n8n/Chatwoot qua plugin bên thứ ba | [MÃ]/[CHẠY] — xem mục 6 |

### Inferences
- Điểm cần sửa nhiều nhất trong báo cáo trước: (5) và (6).

### Gaps
- Khẳng định (3) cần kiểm lại trực tiếp trên docs.zaloplatforms.com từ một mạng không bị chặn.

---

## 9. Khuyến nghị thực tế cho phòng Marketing online của một công ty VN: (a) nhân viên nội bộ chat với agent, (b) khách hàng, (c) nhóm Zalo

### Takeaway
(a) Nội bộ: dùng **Zalo Bot Platform (1:1)** — chính thức, rẻ, GoClaw đã hỗ trợ sẵn (kênh `zalo_oa`), chặn bằng allowlist/pairing. (b) Khách hàng: dùng **Zalo OA đã xác thực + OA OpenAPI (gói Growth trở lên)**, tôn trọng cửa sổ tư vấn 48h và dùng ZBS Template cho tin chủ động — GoClaw **chưa có** adapter này, cần xây. (c) Nhóm: nhóm khách/cộng đồng → **GMF của OA**; nhóm nội bộ → chờ Bot-in-group ra chính thức hoặc dùng kênh khác; zca-js chỉ nên là phương án chấp nhận rủi ro, bằng tài khoản phụ riêng.

### Cited Findings
- Bot Platform chính thức, auth bằng token, DM ổn định; nhóm "thử nghiệm nội bộ" — xem mục 1 ([#1543](https://github.com/nextlevelbuilder/goclaw/issues/1543), [docs.zaloplatforms.com](https://docs.zaloplatforms.com/docs/BOT/best-practices/build-bot-interaction-with-group)).
- GoClaw `zalo_oa` = Bot API, DM, mặc định `dmPolicy = "pairing"` (`internal/channels/zalo/zalo.go` hàm `New`) [MÃ].
- Zalo ClawBot chỉ nói chuyện với chủ, chỉ chạy trong OpenClaw — xem mục 5 [MÃ][DOC].
- OA: API cần Growth/Comprehensive; tin tư vấn miễn phí trong 48h; ZBS Template Message trả phí; GMF có API và gắn với gói Tăng trưởng/Toàn diện — xem mục 2 [DOC-snippet].
- zca-js: điều khoản Zalo cấm phần mềm bên thứ ba; chính tác giả cảnh báo khoá/ban — xem mục 3.

### Inferences
- **(a) Nhân viên nội bộ ↔ agent**:
  - Chọn: tạo 1 (hoặc vài) Zalo Bot qua Bot Creator; mỗi nhân viên nhắn 1:1 với bot; GoClaw kênh `zalo_oa` (thực ra là Bot API) + `dm_policy` pairing/allowlist theo Zalo user ID. Chi phí ≈ 0 (chưa kiểm chứng hạn mức chính thức).
  - Không chọn Zalo ClawBot cho mô hình "phòng ban dùng chung agent": nó owner-bound (1 bot ↔ 1 người) và chỉ cho OpenClaw.
  - Không dùng zca-js trên tài khoản cá nhân nhân viên.
  - Nếu cần thảo luận nhóm nội bộ với agent: tạm dùng kênh khác mà GoClaw đã hỗ trợ nhóm (Telegram/Slack/Discord/Feishu) cho tới khi Bot-in-group của Zalo ra chính thức.
- **(b) Khách hàng**:
  - Chọn: OA doanh nghiệp đã xác thực, mua gói **Growth (~2,5 triệu đ/năm, số liệu từ đại lý)** hoặc Comprehensive để được ủy quyền App/API; agent trả lời trong cửa sổ tư vấn (miễn phí trong 48h; OpenAPI cho gửi tin tư vấn tới 7 ngày — có thể phát sinh phí/hạn mức ngoài 48h); tin chủ động (khuyến mãi, nhắc hẹn) qua **ZBS Template Message** (phải duyệt mẫu, trả phí/tin).
  - Việc cần làm cho GoClaw: viết channel OA OpenAPI mới (OAuth v4 access/refresh token, webhook OA, gửi tin tư vấn, theo dõi cửa sổ 48h, ZBS template) — hiện không có trong mã. Tham khảo mã mở: `@elizaos/plugin-zalo`, `@mnemo-bot/zalo-oa`, `zca-bridge/src/zalo-oa/*`, node n8n OA.
  - Có thể dùng Zalo Bot cho khách như kênh phụ (khách quét QR/nhắn bot), nhưng không có nhận diện thương hiệu/xác thực doanh nghiệp như OA và hạn mức chưa rõ → không nên là kênh chính.
  - Tránh dùng số Zalo cá nhân (zca-js) để chăm sóc/nhắn khách hàng loạt: vi phạm điều khoản, rủi ro mất tài khoản kèm toàn bộ danh bạ khách.
- **(c) Nhóm Zalo**:
  - Nhóm khách hàng/cộng đồng do công ty lập: dùng **GMF của OA** (GMF-10/50/100/1000; gói Tăng trưởng/Toàn diện có sẵn một số nhóm; có API gửi text/ảnh/mention + webhook tin nhóm) → cần adapter OA có hỗ trợ GMF.
  - Nhóm Zalo thường đã có sẵn (không do OA tạo): đường chính thức duy nhất sẽ là Zalo Bot trong nhóm — **chưa phát hành chính thức** (tới 30/08/2026). Theo dõi docs.zaloplatforms.com; GoClaw issue #1543 đã ghi sẵn khoảng trống cần làm (`group_policy`, `require_mention`, `chat_type`).
  - zca-js (GoClaw `zalo_personal`, OpenClaw `zalouser`) vào nhóm được ngay nhưng là **phương án rủi ro**: chỉ dùng với SIM/tài khoản phụ riêng cho bot, `group_policy = allowlist`, lưu lượng thấp, không nhắn người lạ, sẵn sàng mất tài khoản; không dùng cho nhóm khách hàng quan trọng.

### Gaps
- Chưa xác minh được chi phí/hạn mức chính thức của Zalo Bot và bảng quyền lợi OA gốc (bị chặn) — trước khi chốt ngân sách cần ai đó mở trực tiếp `zalo.solutions/oa/pricing` và `docs.zaloplatforms.com/docs/BOT`.
- Chưa có điều khoản chính thức nào nói rõ Zalo cho phép/cấm dùng LLM trả lời khách qua OA hay Bot (không tìm thấy).
