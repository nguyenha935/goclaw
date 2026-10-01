# Brief nghiên cứu: cách dựng "công ty agent" phòng Marketing trên Hermes Agent + Honcho

> **Gửi phiên Claude mới.** Sau ba vòng nghiên cứu (kết thúc 27/9/2026), tôi đã chọn nền: **Hermes Agent + Honcho tự host**, còn OpenClaw là phương án dự phòng. Brief này yêu cầu **nghiên cứu cách làm**: thiết kế, prototype chạy được và bộ test. Chưa triển khai production.
>
> Phụ lục là dữ liệu của phiên trước, dùng để khởi động nhanh, **không được dùng làm kết luận**. Hermes đổi hàng trăm commit mỗi ngày, nên mọi điểm móc, số dòng và tên cấu hình trong phụ lục đều phải kiểm lại trên commit mới nhất.

---

## 1. Tôi cần gì

Một "công ty agent" tự host để vận hành **phòng Marketing online**. Về phòng ban và chia việc, hệ thống phải chạy giống bản thương mại của GoClaw (Dewee). Agent gọi model bằng API key của tôi. Kênh chat: Telegram và Zalo, có thể thêm web.

### Yêu cầu bắt buộc

1. **D1 – Vận hành phòng ban.**
   - Mỗi agent có chức danh và phòng ban (Leader, Content, Copywriter, Designer, Ads, SEO, Dev…).
   - Yêu cầu, kể cả yêu cầu mơ hồ, được làm rõ, chia việc và giao theo vai.
   - Có review và duyệt trước khi đăng bài hoặc tiêu tiền.
   - Cấu trúc tổ chức phải **thực sự quyết định** việc giao việc, không chỉ là chữ trong persona.
2. **K1 – Kho tri thức chung.** Brand guideline, bảng giá, SOP… mà mọi agent, hoặc agent cùng phòng, tra được.
   - Kho này tách khỏi bộ nhớ riêng của từng người dùng.
   - Admin là người nạp tài liệu.
   - Phân quyền được theo phòng ban.
3. **K2 – Biết ai là ai.**
   - (5a) Mỗi tin nhắn, agent thấy ID ổn định của người gửi, kèm kênh và nhóm.
   - (5b-in) Trong một kênh, người dùng A nói ở nhóm 1, nhóm 2 hay chat riêng đều được nhận là **một người**: điều agent biết về A ở đâu cũng dùng được ở chỗ khác, và bộ nhớ khoá theo người.
   - (5b-cross) Tốt nhất là A trên Telegram, Zalo và web quy về một người.
4. **K3 – Luật persona.** Quy tắc về tính cách, cách xưng hô và phong cách nói chuyện của từng agent, áp dụng ở mọi kênh và mọi nhóm.
5. **K4 – Bảo mật.**
   - Mặc định không bao giờ tiết lộ thông tin của người dùng này cho người dùng khác, trừ khi admin cho phép.
   - Điều A kể riêng trong DM không được nhắc lại trong nhóm có người khác.
6. **K5 – Gán admin qua kênh chat.**
   - Admin gán một tài khoản cụ thể trên một kênh cụ thể (ví dụ Telegram ID 9001) làm **admin hệ thống**.
   - Chỉ tài khoản đó có quyền admin qua chat.
   - Việc gán dựa trên ID nền tảng đã xác thực. Kẻ đặt tên hiển thị trùng không được qua mặt.
7. **5d – Giao việc mang theo người yêu cầu.** Agent 1 giao việc cho agent 2 thì agent 2 phải biết mình đang làm cho ai.

Người dùng **không có** chức danh. Tầng đặc quyền duy nhất là admin hệ thống.

### Ràng buộc

- **Không fork Hermes.** Chỉ dùng plugin (thư mục plugin hoặc pip entry point), cấu hình và dịch vụ chạy bên ngoài.
  - Sửa plugin Honcho nằm trong repo Hermes cũng tính là fork.
  - Nếu một việc bắt buộc phải sửa lõi, ghi rõ lý do và đề xuất phương án khác (PR upstream, hoặc plugin ngoài thay thế).
- **Honcho server dùng AGPL-3.0:** không sửa mã server. Mọi tuỳ biến phải nằm phía Hermes.
- **Zalo chỉ dùng đường chính thức:** Zalo Bot Platform cho chat 1:1 nội bộ, Zalo OA cho khách hàng. Loại các đường dùng tài khoản cá nhân (zca-js…) vì có rủi ro khoá tài khoản.
- **Tôi viết được Python** và sẵn sàng tự viết plugin, adapter. Tôi không muốn gánh một bản fork.
- **Tài liệu và báo cáo bằng tiếng Việt.** Định danh trong mã giữ nguyên.
- **Không ghi secret** (API key, bot token) vào repo hay vào ghi chú.

---

## 2. Câu hỏi phải trả lời

### A. Kiến trúc và vận hành

1. **Topology:** mỗi agent là một profile; một gateway multiplex hay mỗi profile một tiến trình?
   - Trên Telegram/Zalo, nên dùng mỗi agent một bot, hay một bot định tuyến tới nhiều profile (`profile_routes` / Bot Mode)?
   - Yêu cầu phải thoả: "agent 1 có mặt ở nhiều nhóm".
2. **Triển khai Honcho:**
   - Thành phần: Postgres + pgvector, API, deriver, Redis có cần không.
   - Tài nguyên cần thiết.
   - Chọn model cho từng việc: chat, deriver (cần structured output), dialectic (cần tool calling), embedding.
   - Chất lượng trích dữ kiện tiếng Việt.
3. **Chi phí:** token và số lời gọi LLM cho mỗi tin nhắn, gồm cả phần Honcho.
4. **Nâng cấp:** chiến lược ghim phiên bản, xử lý API plugin không ổn định (`COMPAT_MANIFEST.md`), và bộ test hồi quy chạy lại mỗi lần nâng cấp.
5. **Vận hành:** sao lưu và khôi phục, log, audit, giám sát.

### B. Thiết kế từng mảnh

Với mỗi mảnh, nêu đủ:
- hook/API với chữ ký chính xác tại commit đã ghim (`file:line`);
- schema dữ liệu và nơi lưu;
- cấu hình đi kèm và lệnh admin;
- các tình huống lỗi;
- test tự động tương ứng.

Các mảnh:

1. **Danh tính và admin (5a, K5).**
   - `/claim_admin <mã một lần>`, bảng admin khoá theo cặp (platform, user_id), đồng bộ với `allow_admin_from`.
   - Trả lời người dùng từ hook mà **không** dùng API nội bộ như `gateway._delivery_adapter_for`.
   - Nút duyệt inline trên Telegram phải kiểm tầng admin.
2. **Chính sách riêng tư (K4).**
   - Cấu hình cứng hoá.
   - Lọc (thay vì chặn hẳn) kết quả `session_search` theo chủ phiên.
   - Kiểm tham số `peer` của các tool `honcho_*`; chặn tool `memory` ghi dữ kiện của người khác.
   - Lệnh `/grant` và `/revoke` có audit.
   - **"Điều kể trong DM chỉ dùng trong DM":** dùng nguồn gốc quan sát của Honcho (`session_name` trong bảng `documents`) có làm được không?
   - Chuyện dữ liệu đã rò nằm lại trong phiên cũ (system prompt bị đóng băng).
3. **Hành vi trong nhóm.**
   - `group_sessions_per_user: true` thì kín, nhưng agent có thể không thấy tin của người khác trong cùng nhóm (phiên trước suy ra, **chưa kiểm**). `false` thì rò `<memory-context>`.
   - Tìm cách để agent thấy toàn bộ cuộc trò chuyện nhóm mà không lộ bộ nhớ riêng của từng người.
4. **Memory provider.**
   - Có thể **thay plugin Honcho trong repo bằng một memory provider ngoài** (gói riêng, đăng ký qua `register_memory_provider`, bọc Honcho SDK) không?
   - Nếu được, provider ngoài này phải giải quyết: peer id kèm tên nền tảng; Honcho chạy trong worker kanban dưới danh nghĩa người yêu cầu; lọc DM→nhóm.
   - Kiểm điều kiện và giấy phép: plugin Honcho của Hermes theo MIT, SDK theo Apache-2.0.
5. **Kho tri thức chung (K1).**
   - Hermes chỉ cho **một** external memory provider, nên kho này phải là plugin riêng có kho lưu của nó (pgvector dùng chung Postgres, SQLite FTS5…).
   - Thiết kế nạp tài liệu: đồng bộ thư mục, admin upload qua chat/dashboard, URL.
   - Phân quyền theo phòng ban.
   - Tự tiêm top-k vào prompt, kèm tool `kb_search`.
   - Không bao giờ nạp hội thoại vào kho.
6. **Persona (K3).**
   - SOUL.md theo profile, `channel_prompts`.
   - Subagent tạo bằng `delegate_task` hiện chạy không có SOUL.
   - Thông báo hệ thống của gateway có emoji.
   - Chặn người thường sửa persona (`/personality`, tool file).
7. **Phòng ban và giao việc (D1).**
   - File `org.yaml` gồm `title`, `department`, `reports_to`, `can_assign`.
   - Tiêm roster vào prompt.
   - Cưỡng chế bằng `pre_tool_call` trên `kanban_create`/`kanban_complete`: assignee phải đúng phòng, reviewer là `reports_to`, chưa review thì không được hoàn tất.
   - **Cầu nối chat → Triage**, để yêu cầu mơ hồ trong chat tự đi qua Specify/Decompose.
   - Vòng review: `kanban_request_review` / `kanban_request_changes`.
8. **Người yêu cầu đi theo việc (5d).**
   - Kanban: `post_tool_call(kanban_create)` cộng `pre_llm_call` trong worker.
   - `delegate_task`: tra ngược qua `parent_session_id`.
9. **Liên kết xuyên kênh (5b-cross).** Lệnh `/link <mã>` sinh ở kênh 1, xác nhận ở kênh 2, rồi ghi `userPeerAliases` an toàn; mọi ID đều có tiền tố nền tảng.
10. **Adapter Zalo.**
    - `register_platform` cho Zalo Bot Platform (chat 1:1). Kiểm trạng thái bot trong nhóm hiện nay.
    - Zalo OA OpenAPI cho khách hàng: để pha sau, nhưng ước lượng luôn.
    - Hai plugin của tinovn không có file LICENSE: liên hệ tác giả hay tự viết (tham khảo `extensions/zalo` MIT của OpenClaw)?

### C. Bảo mật

1. **Mô hình mối đe doạ:**
   - kẻ giả mạo tên hiển thị;
   - prompt injection từ khách nhắn qua OA;
   - người dùng thường lạm dụng tool file, shell, web hay terminal;
   - lộ tài khoản admin;
   - lộ dữ liệu qua nhóm.
2. **Danh sách mặc định cần khoá**, kèm cấu hình cụ thể.

### D. Spike với LLM thật và bot thật

- Lập kế hoạch đo, kèm ngưỡng đạt/trượt cho từng mục:
  - chất lượng deriver tiếng Việt;
  - model có giữ persona không;
  - model có tự gọi `kb_search` / `honcho_search` không;
  - lọc @mention trong nhóm;
  - hệ quả của việc tách phiên nhóm theo người;
  - decomposer có chọn đúng người không;
  - chi phí cho mỗi tin nhắn.
- **Chỉ chạy khi tôi cung cấp API key và bot token.** Hỏi tôi trước. Không tự tạo tài khoản.

---

## 3. Cách làm bắt buộc

1. **Clone `NousResearch/hermes-agent` và `plastic-labs/honcho` bản mới nhất.**
   - Ghi commit hash và ngày.
   - Kiểm lại mọi điểm móc ở phụ lục. Chỗ nào đã đổi thì ghi rõ "đã đổi".
2. **Đọc mã, không tin README.** Mọi khẳng định kèm `file:line` tại commit đã ghim, hoặc URL, và gắn nhãn:
   - **[MÃ]** đã đọc mã;
   - **[CHẠY]** đã chạy thật;
   - **[DOC]** chỉ đọc tài liệu;
   - **[?]** chưa kiểm chứng.
3. **Kiểm đường ống trước bằng LLM giả.**
   - Dùng server LLM giả có sẵn: `research_notes/tools/stub_llm.py` trong repo `nguyenha935/goclaw`, nhánh `claude/dreamy-johnson-snk1l3`. Nó ghi lại mọi request gửi tới model và trả lời theo kịch bản. Đọc docstring trước khi dùng. Nếu không truy cập được repo này thì tự viết một bản tương đương.
   - Bơm tin nhắn bằng plugin nền tảng giả, theo mẫu `tests/e2e/core/chaos/_gateway_fake_platform.py` của Hermes.
   - Chỉ dùng LLM và bot thật khi tôi cho phép.
4. **Mọi khẳng định về riêng tư phải có test tự động chứng minh.** Mỗi đường rò trong phụ lục mục C phải có một test báo đỏ khi cấu hình sai.
5. **Không fork.** Gặp chỗ bắt buộc sửa lõi thì dừng lại, ghi rõ, rồi đề xuất phương án khác.
6. **Tự xác định ngày hôm nay** và ghi thời điểm kiểm. GitHub ẩn năm với các ngày trong năm hiện tại; chỗ nào phải suy năm thì ghi rõ.
7. **Trang bị chặn mạng** (proxy chặn Zalo, một số trang tài liệu…) thì ghi rõ, và gắn nhãn "chưa kiểm chứng" cho thông tin lấy gián tiếp.
8. **Hỏi tôi trước khi:** tạo tài khoản thật, gửi tin vào kênh thật, tiêu tiền, hoặc đẩy mã lên nơi công khai.

---

## 4. Kịch bản kiểm chuẩn (dùng lại cho mọi test)

- **Agent:** agent 1 "Content Lead – Phòng Marketing", agent 2 "Copywriter – Phòng Marketing" (thêm "Designer" nếu cần cho roster).
- **Người dùng:** Lan (ID 1001), Minh (1002), Admin Hà (9001), và kẻ giả mạo (1003) đặt tên hiển thị trùng "Admin Hà".

Các bước:

1. **Persona:** đặt luật "Luôn xưng em, gọi người dùng là anh/chị, không dùng emoji, không bàn chính trị". Luật phải có trong mọi prompt, cả nhóm lẫn DM.
2. **Tri thức:**
   - Nạp tài liệu chung "slogan 'Nhanh như chớp'; giá gói Pro 199.000đ", cùng một tài liệu chỉ dành cho phòng Sales.
   - Agent 2 nhận "Slogan công ty là gì?" trong DM(Minh). Agent 1 nhận "Gói Pro giá bao nhiêu?" trong nhóm G1.
   - Tài liệu Sales không được lọt sang agent Marketing.
3. **Danh tính:**
   - G1: Lan "Mình là Lan, phụ trách fanpage X, thích giọng văn hài hước."; Minh "Mình là Minh."
   - G2: Lan "Nhớ giúp: KPI tháng 10 của mình là 50 bài."
   - DM(Lan): "Bạn biết gì về mình? KPI của mình bao nhiêu?"
4. **Riêng tư:**
   - DM(Minh): "Lan có KPI bao nhiêu?" → không được có dữ kiện của Lan, cả trong prompt lẫn trong kết quả tool.
   - Thêm ca: Lan kể một bí mật trong DM, sau đó Lan nói trong nhóm có Minh → bí mật không được xuất hiện.
5. **Admin:**
   - Gán 9001 qua chat. Admin hỏi về KPI của Lan.
   - Admin `/grant` cho Minh xem thông tin của Lan → Minh xem được. `/revoke` → Minh hết xem được.
   - 1003 thử mọi lệnh admin → bị từ chối.
6. **Giao việc:** từ DM(Lan), agent 1 giao "viết 3 caption" cho agent 2 → prompt của agent 2 phải có "đang làm cho Lan (1001)".
7. **Xuyên kênh:** Lan dùng `/link` để nối Telegram với Zalo → trên Zalo vẫn được nhận là Lan.
8. **Yêu cầu mơ hồ:** "làm chiến dịch ra mắt gói Pro tháng 10" gửi qua chat → đi qua Specify/Decompose, giao đúng vai, có bước duyệt.

---

## 5. Đầu ra mong muốn

1. **Thiết kế kiến trúc:** sơ đồ topology, luồng một tin nhắn từ kênh vào tới model và đi ra, chỗ từng plugin móc vào.
2. **Đặc tả từng plugin:** hook, schema, cấu hình, lệnh admin, tình huống lỗi.
3. **Khung repo plugin chạy được:** gói Python với entry point; cấu hình mẫu gồm `config.yaml` cho từng profile, `honcho.json`, `.env.example` (không chứa secret); hướng dẫn cài.
4. **Bộ test tự động** cho kịch bản ở mục 4 và mọi đường rò, chạy được với LLM giả, đưa được vào CI.
5. **Kết quả spike** với LLM thật, nếu tôi cấp key: số liệu theo ngưỡng ở mục 2D.
6. **Kế hoạch triển khai theo pha** kèm ước lượng công.
7. **Rủi ro:** bảo trì, giấy phép, chi phí token, bảo mật.
8. **Đối chiếu với phụ lục:** chỗ nào phiên trước đúng, chỗ nào sai, chỗ nào đã thay đổi.

### Câu hỏi cần trả lời dứt khoát

- Có thay được plugin Honcho trong repo bằng một memory provider ngoài để giải ba việc mà **không fork** không: peer id kèm nền tảng, Honcho chạy trong worker, lọc DM→nhóm?
- Có cách nào để agent trong nhóm thấy toàn bộ cuộc trò chuyện mà không lộ bộ nhớ riêng của từng người?
- Kho tri thức chung đặt ở đâu khi Hermes chỉ cho một memory provider ngoài?
- Gán admin qua chat có làm trọn được chỉ bằng API công khai không?
- Trên Telegram và Zalo, nên dùng mỗi agent một bot hay một bot cho nhiều agent?
- Tổng công thực tế còn bao nhiêu, và những phần nào sẽ phải viết lại mỗi khi Hermes nâng cấp?

---

# Phụ lục — dữ liệu phiên trước (27/9/2026), chỉ để đối chiếu

Nhãn: **[MÃ]** đọc mã · **[CHẠY]** chạy thật với LLM giả và nền tảng giả · **[DOC]** tài liệu · **[?]** chưa kiểm chứng.

Phiên bản đã kiểm:
- Hermes `9fa23760bcf5a8288c3ba2f0bea898d54652c317` (2026-09-27). Một số kết quả lấy từ `516535b5` và `42d70d29`.
- Honcho server `2eb27b6c` (v3.2.1, 2026-09-22), SDK `honcho-ai` 2.2.0.

Toàn bộ báo cáo và bằng chứng nằm trong repo `nguyenha935/goclaw`, nhánh `claude/dreamy-johnson-snk1l3`:
- `reports/Ứng viên mới và elizaOS develop.md` (báo cáo cuối);
- `reports/Nền tảng agent nhận diện người dùng.md`;
- `research_notes/Ứng viên mới và elizaOS develop/hermes_final_criteria.md`;
- `research_notes/Nền tảng agent nhận diện người dùng/hermes_honcho.md`;
- mã nguồn plugin prototype `lab-org` nằm trong `research_notes/Ứng viên mới và elizaOS develop/evidence/hermes_final_criteria_evidence.txt`, mục "Prototype source".

## A. Điểm móc plugin (đường dẫn tại `9fa23760`, phải kiểm lại)

- **`register_platform`** — `hermes_cli/plugins.py:807`. Plugin nền tảng giả `labgram` bơm tin qua `build_source → MessageEvent → handle_message` [CHẠY].
- **`pre_llm_call`** — điểm gọi ở `agent/turn_context.py:749-800`.
  - Nhận `session_id, task_id, user_message, conversation_history, is_first_turn, model, platform, parent_session_id, sender_id`.
  - Trả `{"context": ...}`; nội dung được nối vào **tin nhắn người dùng** của lượt đó [CHẠY].
- **`register_system_prompt_section`** — `hermes_cli/plugins.py:954-977`. Bị **đóng băng theo phiên** và không thấy người gửi, nên chỉ hợp với nội dung tĩnh như roster phòng ban [CHẠY].
- **`pre_tool_call`** — `hermes_cli/plugins.py:1945-2051`.
  - Trả `block`, `approve` hoặc `modify`. Nhận tool thật kể cả khi model gọi qua `tool_call`.
  - Người gửi lấy qua `get_session_env("HERMES_SESSION_PLATFORM"/"_USER_ID"/"_USER_NAME")` (`gateway/session_context.py:36-47, 173-179`) [CHẠY].
  - Riêng kết quả `approve` (bắt người duyệt) bị bỏ qua khi bật yolo hoặc `approvals.mode: off`, và trong worker kanban mặc định bị từ chối [MÃ].
- **`post_tool_call`** — dùng trên `kanban_create` để ghi bảng "task → người yêu cầu" (PoC cho 5d) [CHẠY].
- **`pre_gateway_dispatch`** — `gateway/run_inbound.py:67-100`.
  - Chạy **trước** bước xác thực. Có `event.source.user_id`. Trả `{"action":"skip"}` để bỏ tin.
  - Prototype phải trả lời qua `gateway._delivery_adapter_for(src).send(...)`, là **API nội bộ** [CHẠY].
- **`register_command`** — handler chỉ nhận `raw_args`, không biết ai gửi (`hermes_cli/plugins.py:677-702`) [MÃ].
- **`register_tool`, `register_hook`** — `hermes_cli/plugins.py:456, 930` [CHẠY].
- **`register_telegram_handler`** — `hermes_cli/plugins.py:874-877`. Có thể dùng để vá nút duyệt inline [?].
- **`register_memory_provider`:**
  - Hermes chỉ cho builtin cộng **tối đa một** provider ngoài (`agent/memory_manager.py:337, 378-388`) [MÃ].
  - `CONTRIBUTING.md` đóng danh sách provider **trong repo**; plugin ngoài vẫn được đăng ký [MÃ].
  - Việc thay hẳn plugin `honcho` trong repo bằng provider ngoài **chưa kiểm**.
- **Độ ổn định API:** `COMPAT_MANIFEST.md` ghi "Internal import paths are not a stable API". Plugin import sai đường đã bị tắt từ 2026-09-14. Trong `slash_access.py` có khối "PLUGIN-COMPAT (revert-scheduled)". Riêng ngày 2026-09-27 có 372 commit trong khoảng 8 giờ [MÃ].

## B. Khoá cấu hình liên quan

- `memory.memory_enabled` và `memory.user_profile_enabled` là hai công tắc riêng (`tools/memory_tool.py:258-261`) [MÃ].
- `memory.provider: honcho`.
- Honcho:
  - `recallMode`: `context` ẩn mọi tool `honcho_*`; `hybrid` thì có tool.
  - `userPeerAliases`: ánh xạ nhiều ID về một peer.
  - `pinUserPeer`: gộp mọi người về một peer — không dùng.
  - `runtimePeerPrefix`, `observationMode`.
  - Đặt trong `$HERMES_HOME/honcho.json`; đọc lại khi khởi tạo phiên, đổi alias có hiệu lực sau `/new` [CHẠY].
- `group_sessions_per_user`: mặc định `true`; thêm participant ID vào khoá phiên nhóm (`gateway/session.py:673-714`) [MÃ].
- `platforms.<p>.extra.allow_admin_from` / `group_allow_admin_from` / `user_allowed_commands` (`gateway/slash_access.py`):
  - khớp theo `user_id`; chỉ chặn **slash command**, không chặn tool hay câu hỏi thường;
  - chỉ đặt được qua file cấu hình [CHẠY].
- `kanban.auto_decompose: true` (chỉ áp cho cột Triage), `review_dispatch: true` (`hermes_cli/config_defaults.py:1874, 1916`) [MÃ].
- `skills.external_dirs`, `channel_prompts`, `display.tool_progress`, `approvals.destructive_slash_confirm` [MÃ].

## C. Đường rò đã thấy khi chạy thật, và cách đã đóng

| Đường rò | Bằng chứng | Đã đóng bằng |
|---|---|---|
| `USER.md` và `MEMORY.md` dùng chung cả profile | "Lan (1001): KPI tháng 10 là 50 bài." nằm trong system prompt của DM(Minh) | `memory_enabled: false` + `user_profile_enabled: false` |
| `session_search` không lọc theo người (`tools/session_search_tool.py:23`) | Minh tìm ra phiên G2 của Lan | Plugin `pre_tool_call` chặn với người thường; lọc theo chủ phiên chưa làm |
| `honcho_search`/`profile`/`context`/`reasoning` nhận `peer` tuỳ ý (`plugins/memory/honcho/tool_schemas.py:49-50`) | Minh đọc được tin gốc của Lan | `recallMode: context`, hoặc plugin kiểm `peer` |
| Phiên nhóm dùng chung phát lại `<memory-context>` của người nói trước (`agent/turn_context.py:93-103`) | Lượt của B thấy KPI của A | Giữ `group_sessions_per_user: true` |
| Peer ID là ID thô, không có tiền tố nền tảng (`plugins/memory/honcho/session_peers.py:81-106`) | Người khác có ID 1001 trên nền tảng khác sẽ nhận hồ sơ của Lan | Chưa đóng: cần tiền tố trong adapter tự viết, hoặc provider ngoài |
| Phiên cũ giữ nguyên system prompt đã đóng băng | Dữ liệu rò còn nguyên cho tới `/new` | Thủ tục reset phiên sau mỗi lần đổi chính sách |

Với bộ `memory_enabled: false` + `user_profile_enabled: false` + `group_sessions_per_user: true` + plugin `pre_tool_call`, test của phiên trước **không thấy rò**. Admin 9001 xem được thông tin. `/grant 1002 1001` cho Minh xem, `/revoke` thu lại [CHẠY].

## D. Những gì đã chạy được

- **5b-in:** Honcho lưu quan sát theo cặp (observer=agent, observed=người). DM(Lan) ngay lượt đầu đã được tiêm tự động dữ kiện từ G1 và G2; DM(Minh) chỉ thấy dữ kiện của Minh [CHẠY].
- **5b-cross:** thêm `userPeerAliases {"zl-777":"1001"}` rồi `/new` là A trên nền tảng thứ hai có đủ dữ kiện. Hiện phải sửa tay, không có bước xác minh [CHẠY].
- **K3:** SOUL.md có trong 19/19 system prompt của agent 1.
  - Chỗ hở: `delegate_task` tạo con với `skip_context_files=True, skip_memory=True` (`tools/delegate_tool.py:241`); thông báo gateway có emoji; `/personality` đổi persona cho cả profile [CHẠY][MÃ].
- **K1:** plugin `lab-org` dùng `pre_llm_call` cộng tool `kb_search` trên thư mục `kb/<scope>/*.md`, phân quyền theo profile/phòng. Agent 1 và agent 2 nhận đúng tài liệu; tài liệu Sales không lọt sang.
  - Truy xuất đang dùng từ khoá nên kết quả nhiễu; production cần embedding [CHẠY].
  - OpenViking (AGPL) và Supermemory có ingest tài liệu nhưng chiếm slot memory duy nhất; Supermemory còn ghi cả hội thoại vào kho [MÃ].
- **K5:** `allow_admin_from: ["9001"]` → 1003 "Admin Hà" có `/whoami` = Tier user và bị từ chối `/personality`.
  - Plugin `/claim_admin HA-7Q2X`: mã chỉ dùng được một lần; 1003 bị từ chối `/grant`.
  - Nút duyệt inline Telegram chỉ kiểm allowlist, không kiểm tầng admin (`plugins/platforms/telegram/adapter.py:4693-4701, 4738-4752`) [MÃ].
  - Tên hiển thị không được dùng để xác thực (`gateway/authz_mixin.py:172-174`) [MÃ].
- **D1:** `hermes kanban decompose` gửi cho model roster gồm mô tả từng profile (`hermes_cli/kanban_decompose.py:37-94, 156-190`). DAG trả về: copywriter và designer chạy song song, bước duyệt giao cho default. Ở đây stub quyết định assignee.
  - `PROFILE_ROLES` chỉ có `setup`; không có trường phòng ban.
  - Review là tuỳ chọn.
  - Tin chat không tự vào cột Triage.
  - Lõi cố ý không lấy `created_by` từ tham số tool (`tools/kanban_tools.py:139-150`) [CHẠY][MÃ].
- **5d:** worker kanban chỉ thấy tiêu đề và mô tả task. PoC `post_tool_call(kanban_create)` + `pre_llm_call` đọc `HERMES_KANBAN_TASK` tiêm được "làm THAY MẶT Lan (user_id=1001)" [CHẠY].
  - Worker bật Honcho báo "no user peer" [CHẠY].
  - Đường `delegate_task` qua `parent_session_id` chưa chạy [?].
- **Honcho tự host (không Docker):**
  - Hạ tầng: PG16 + pgvector 0.6.0 cài từ apt, `alembic upgrade head`, `fastapi run src/main.py` và `python -m src.deriver`.
  - Không cần Redis (`CACHE_ENABLED=false`).
  - LLM và embedding trỏ qua `LLM_OPENAI_BASE_URL` / `LLM_OPENAI_API_KEY` (`src/config.py:774-787`).
  - Cần sẵn file `o200k_base.tiktoken` khi mạng kín.
  - Python ≥3.13; Hermes phải cài trên Python 3.14 [CHẠY].
  - Một kịch bản tốn 68 lời gọi embedding, 24 dialectic và 13 deriver.
- **Kanban** được thiết kế "single-host by design" [MÃ].

## E. Zalo (nhiều nguồn chính thức bị chặn, chỉ có snippet tìm kiếm)

- **Zalo Bot Platform:** `bot-api.zaloplatforms.com/bot<TOKEN>/<method>`.
  - Chat 1:1 chạy ổn định.
  - Bot trong nhóm "thử nghiệm nội bộ", theo bằng chứng mới nhất ngày 30/8/2026.
  - Mỗi tin tối đa 2.000 ký tự; polling và webhook loại trừ nhau.
- **Zalo OA:** từ 1/6/2026 có 4 gói Cơ bản / Tiêu chuẩn / Tăng trưởng / Toàn diện.
  - Gọi API cần gói Tăng trưởng trở lên; có nguồn mâu thuẫn.
  - Tin tư vấn miễn phí trong 48 giờ, OpenAPI gửi được tới 7 ngày; tin chủ động qua ZBS Template thì trả phí.
  - GMF là nhóm chat của OA.
- **Plugin Zalo cho Hermes:** `tinovn/hermes-zalo-oa-plugin` (OA, commit cuối 2026-09-11) và `tinovn/hermes-zalo-plugin` (tài khoản cá nhân, 2026-09-14). Cả hai **không có file LICENSE**.
- **Mã tham khảo cho Bot API:** `extensions/zalo` của OpenClaw (MIT).

## F. Ước lượng của phiên trước (chưa kiểm chứng)

- Riêng các plugin (KB, admin/riêng tư, phòng ban, 5d, `/link`): 3–4 người-tuần.
- Tổng gồm spike, dựng Honcho, adapter Zalo Bot và test hồi quy: 28–44 ngày công.
- Bảo trì: 0,5–1 ngày mỗi tuần.

## G. Việc phiên trước chưa kiểm

- Chưa có lần chạy nào với LLM thật hay bot Telegram/Zalo thật.
- Chưa kiểm hệ quả của việc tách phiên nhóm theo người.
- Chưa kiểm `transform_tool_result` để lọc kết quả `session_search`.
- Chưa kiểm `honcho_reasoning`, `honcho_context`, `honcho_profile` riêng lẻ; chưa kiểm peer card và dream.
- Chưa kiểm background review khi `memory_enabled: false`.
- Chưa kiểm đường `delegate_task` cho 5d.
- Chưa có lệnh `/link`.
- Chưa có cách trả lời từ hook bằng API công khai.
- Chưa chạy với nhiều người dùng đồng thời.
