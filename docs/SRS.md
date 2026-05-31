# TÀI LIỆU YÊU CẦU PHẦN MỀM (SRS)

# HỆ THỐNG QUẢN TRÒ MA SÓI TỰ ĐỘNG REALTIME

## 1. Giới thiệu

### 1.1. Mục đích tài liệu

Tài liệu này mô tả yêu cầu phần mềm cho hệ thống **quản trò Ma Sói tự động realtime**. Mục tiêu là làm rõ nghiệp vụ, chức năng, logic game, yêu cầu âm thanh, yêu cầu realtime, yêu cầu kỹ thuật và tiêu chí nghiệm thu để lập trình viên hoặc AI coding assistant có thể dựa vào đây triển khai hệ thống.

Hệ thống được thiết kế cho các trận Ma Sói chơi trực tiếp ngoài đời. Người chơi ngồi cùng một địa điểm, mỗi người dùng điện thoại cá nhân để nhận vai trò và thực hiện hành động bí mật vào ban đêm. Một thiết bị Host dùng làm màn hình trung tâm và loa quản trò.

### 1.2. Mục tiêu hệ thống

Hệ thống cần thay thế vai trò của người quản trò bằng phần mềm, bao gồm:

- Tạo phòng chơi.
- Cho người chơi tham gia bằng mã phòng.
- Chia role ngẫu nhiên theo cấu hình Host chọn.
- Điều khiển vòng lặp ban đêm và ban ngày.
- Gọi từng role thức dậy bằng âm thanh.
- Cho đúng người chơi được thao tác bí mật khi tới lượt role của họ.
- Tự động xử lý logic chết, cứu, bảo vệ, soi, vote và điều kiện thắng.
- Đồng bộ màn hình Host và Client realtime.
- Hỗ trợ khoảng 10 người chơi cùng lúc trong một phòng.
- Có thể deploy lên web bằng nền tảng miễn phí hoặc chi phí thấp.

### 1.3. Phạm vi hệ thống

Hệ thống là một web app gồm:

- **Host App**: màn hình trung tâm dùng để tạo phòng, cấu hình role, bắt đầu game, chuyển phase, phát âm thanh thông báo và hiển thị kết quả.
- **Client App**: màn hình điện thoại của người chơi dùng để tham gia phòng, xem role, nhận trạng thái ngủ/thức, chọn mục tiêu, vote và xem kết quả.
- **Backend Server**: xử lý logic game, lưu trạng thái, điều phối realtime và phát event đến các client.
- **Database**: lưu phòng chơi, người chơi, role, trạng thái trận đấu, hành động ban đêm và vote.

Không ưu tiên làm hệ thống tài khoản đăng nhập trong phiên bản đầu. Người chơi chỉ cần nhập tên và mã phòng.

---

## 2. Công nghệ thống nhất sử dụng

### 2.1. Frontend

Sử dụng:

```txt
Vue 3 + Vite + TailwindCSS + Pinia
```

Mục đích:

- Vue 3 dùng để xây dựng giao diện Host và Client.
- Vite giúp chạy local và build nhanh.
- TailwindCSS dùng để thiết kế giao diện dark mode, responsive, dễ nhìn trên điện thoại.
- Pinia dùng để quản lý trạng thái phía client như thông tin player, room, role, phase, trạng thái sống/chết và trạng thái kết nối.

Deploy frontend lên:

```txt
Vercel
```

### 2.2. Backend

Sử dụng:

```txt
Python FastAPI
```

Mục đích:

- Cung cấp REST API cho tạo phòng, join phòng, lấy thông tin game.
- Cung cấp WebSocket để đồng bộ realtime.
- Xử lý toàn bộ logic game ở backend.
- Backend là nguồn dữ liệu chính xác duy nhất của trận đấu.

Deploy backend lên:

```txt
Render Web Service
```

### 2.3. Realtime Communication

Sử dụng:

```txt
FastAPI WebSocket
```

WebSocket dùng để:

- Cập nhật người chơi vào phòng realtime.
- Đồng bộ phase ngày/đêm.
- Gọi role thức dậy.
- Mở khóa màn hình đúng player/role.
- Gửi hành động ban đêm.
- Gửi vote ban ngày.
- Cập nhật kết quả chết, treo cổ, thắng thua.
- Cập nhật trạng thái kết nối của người chơi.

### 2.4. Database

Sử dụng:

```txt
Supabase PostgreSQL
```

Mục đích:

- Lưu thông tin phòng chơi.
- Lưu danh sách người chơi.
- Lưu role đã chọn và role đã chia.
- Lưu trạng thái game hiện tại.
- Lưu hành động ban đêm.
- Lưu vote ban ngày.
- Lưu các trạng thái đặc biệt như Cupid, tẩm dầu, sói nguyền, thuốc phù thủy.

### 2.5. ORM và migration

Sử dụng:

```txt
SQLAlchemy + Alembic
```

Mục đích:

- SQLAlchemy dùng để thao tác database bằng Python.
- Alembic dùng để quản lý thay đổi cấu trúc database.

---

## 3. Đối tượng sử dụng

### 3.1. Host

Host là người tạo phòng và điều khiển trận đấu. Host có thể là người không tham gia chơi hoặc là người điều phối bên ngoài.

Host có quyền:

- Tạo phòng.
- Chọn số lượng role.
- Xem danh sách người chơi đã vào phòng.
- Bắt đầu game.
- Điều khiển ban đêm, ban ngày và vote.
- Phát âm thanh thông báo.
- Xem kết quả xử lý ban đêm.
- Xem kết quả vote.
- Xem kết quả thắng thua.

### 3.2. Player

Player là người chơi Ma Sói. Player sử dụng điện thoại cá nhân.

Player có thể:

- Nhập tên và mã phòng để tham gia.
- Xem role của mình sau khi game bắt đầu.
- Nhận màn hình ngủ vào ban đêm.
- Được mở khóa thao tác khi tới lượt role của mình.
- Chọn mục tiêu nếu role có kỹ năng.
- Vote treo cổ vào ban ngày.
- Xem trạng thái sống/chết của bản thân.
- Xem thông báo kết quả chung.

---

## 4. Quy trình tổng quan của game

### 4.1. Phase 1: Tạo phòng và setup role

Luồng xử lý:

1. Host mở website và chọn tạo phòng.
2. Backend tạo `room_id` và `room_code`.
3. Host chia sẻ `room_code` cho người chơi.
4. Player nhập tên và `room_code` để vào phòng.
5. Host chọn số lượng từng role trong giao diện giỏ role.
6. Hệ thống hiển thị:
   - Tổng số người chơi thực tế trong phòng: `N_players`.
   - Tổng số role Host đã chọn: `N_roles`.
7. Host chỉ được bắt đầu game khi `N_roles >= N_players`.
8. Khi Host bấm bắt đầu, backend chia role ngẫu nhiên cho người chơi.

### 4.2. Thuật toán chia role

Yêu cầu:

- Lấy ngẫu nhiên `N_players` role từ danh sách role Host đã chọn.
- Danh sách role được chia bắt buộc phải có ít nhất 1 `Ma Sói thường`.
- Nếu kết quả không có `Ma Sói thường`, backend phải random lại.
- Mỗi player nhận đúng 1 role.
- Client chỉ được biết role của chính mình.
- Host có thể xem toàn bộ role nếu cần chế độ debug, nhưng mặc định không hiển thị toàn bộ role để giữ tính công bằng.

Pseudo logic:

```txt
selected_roles = random_sample(role_cart, N_players)
while selected_roles does not contain NORMAL_WEREWOLF:
    selected_roles = random_sample(role_cart, N_players)
assign selected_roles to players randomly
```

### 4.3. Phase 2: Ban đêm

Ban đêm là phase quan trọng nhất của hệ thống.

Yêu cầu chính:

- Host phát âm thanh nền ban đêm.
- Host phát lời gọi từng role theo thứ tự cố định.
- Khi role được gọi, chỉ player thuộc role đó được mở màn hình thao tác.
- Người chơi khác giữ màn hình ngủ tối.
- Sau khi player thao tác xong, màn hình tự quay lại trạng thái ngủ.
- Backend lưu toàn bộ hành động ban đêm.
- Backend xử lý kết quả chết/cứu/bảo vệ/hiệu ứng đặc biệt khi kết thúc ban đêm.

### 4.4. Phase 3: Ban ngày

Ban ngày gồm:

1. Công bố người chết trong đêm.
2. Kiểm tra điều kiện thắng/thua đầu buổi sáng.
3. Nếu game chưa kết thúc, bắt đầu thời gian thảo luận.
4. Host hoặc hệ thống mở vote.
5. Player vote người muốn treo cổ.
6. Backend xử lý kết quả vote.
7. Người cao phiếu nhất bị loại.
8. Kiểm tra điều kiện thắng/thua sau vote.
9. Nếu chưa kết thúc, game quay lại ban đêm tiếp theo.

---

## 5. Yêu cầu âm thanh và quản trò ảo

### 5.1. Tầm quan trọng của âm thanh

Âm thanh là yêu cầu rất quan trọng của hệ thống vì Host cần thay thế người quản trò thật. Hệ thống không chỉ hiển thị chữ mà phải có khả năng đọc thông báo rõ ràng để người chơi nghe và làm theo.

Âm thanh có 4 vai trò chính:

- Hướng dẫn người chơi nhắm mắt, mở mắt, thức dậy, ngủ lại.
- Gọi từng role theo thứ tự trong ban đêm.
- Che tiếng thao tác bằng nhạc nền hoặc ambient noise.
- Công bố kết quả ban ngày và kết quả game.

### 5.2. Giải pháp âm thanh chính

Sử dụng:

```txt
Web Speech API / Text-To-Speech trên trình duyệt Host
```

Lý do:

- Không cần lưu nhiều file mp3.
- Không tốn băng thông backend.
- Dễ thay đổi nội dung lời đọc.
- Phù hợp deploy miễn phí.
- Host chỉ cần mở loa của thiết bị trung tâm.

### 5.3. Ambient noise ban đêm

Hệ thống cần có âm thanh nền ban đêm để tránh người chơi nghe được tiếng thao tác của nhau.

Yêu cầu:

- Khi bắt đầu ban đêm, Host phát ambient noise.
- Ambient noise lặp liên tục trong suốt ban đêm.
- Âm lượng ambient noise thấp hơn lời đọc quản trò.
- Khi quản trò ảo đọc thông báo, ambient noise vẫn chạy nhưng không được lấn át lời đọc.
- Khi chuyển sang ban ngày, ambient noise dừng.

Nguồn âm thanh:

- Có thể dùng 1 file `night-ambient.mp3` hoặc `night-ambient.ogg` dung lượng nhỏ.
- File có thể lưu trong frontend static assets hoặc Cloudinary.

### 5.4. Danh sách thông báo âm thanh bắt buộc

#### 5.4.1. Bắt đầu ban đêm

```txt
Trời tối rồi. Tất cả người chơi hãy nhắm mắt lại.
```

```txt
Đêm nay bắt đầu. Mọi người giữ im lặng và không nhìn màn hình của người khác.
```

#### 5.4.2. Gọi Ma Sói

```txt
Ma Sói thức dậy.
```

```txt
Ma Sói hãy nhìn nhau và chọn một người để cắn.
```

```txt
Ma Sói đã chọn xong. Ma Sói đi ngủ.
```

#### 5.4.3. Gọi Bảo vệ

```txt
Bảo vệ thức dậy.
```

```txt
Bảo vệ hãy chọn một người để bảo vệ trong đêm nay.
```

```txt
Bảo vệ đã chọn xong. Bảo vệ đi ngủ.
```

#### 5.4.4. Gọi Tiên tri

```txt
Tiên tri thức dậy.
```

```txt
Tiên tri hãy chọn một người để soi.
```

```txt
Tiên tri đã nhận kết quả. Tiên tri đi ngủ.
```

#### 5.4.5. Gọi Phù thủy

```txt
Phù thủy thức dậy.
```

```txt
Đêm qua có người bị Ma Sói cắn. Phù thủy có muốn cứu không?
```

```txt
Phù thủy có muốn dùng bình độc không?
```

```txt
Phù thủy đã chọn xong. Phù thủy đi ngủ.
```

Trường hợp không ai bị Sói cắn:

```txt
Đêm qua không có ai bị Ma Sói cắn. Phù thủy có muốn dùng bình độc không?
```

#### 5.4.6. Gọi Thợ săn

```txt
Thợ săn thức dậy.
```

```txt
Thợ săn hãy chọn một người để kéo theo nếu bản thân bị chết.
```

```txt
Thợ săn đã chọn xong. Thợ săn đi ngủ.
```

#### 5.4.7. Gọi Cupid đêm đầu tiên

```txt
Cupid thức dậy.
```

```txt
Cupid hãy chọn hai người để ghép đôi.
```

```txt
Cupid đã chọn xong. Cupid đi ngủ.
```

#### 5.4.8. Gọi Kẻ tẩm dầu

```txt
Kẻ tẩm dầu thức dậy.
```

```txt
Kẻ tẩm dầu hãy chọn hai người để tẩm dầu.
```

```txt
Kẻ tẩm dầu đã chọn xong. Kẻ tẩm dầu đi ngủ.
```

#### 5.4.9. Kết thúc ban đêm

```txt
Tất cả người chơi tiếp tục nhắm mắt. Hệ thống đang xử lý kết quả trong đêm.
```

```txt
Trời sáng rồi. Tất cả người chơi hãy mở mắt.
```

#### 5.4.10. Công bố kết quả ban ngày

Nếu không ai chết:

```txt
Đêm qua không có ai chết.
```

Nếu có người chết:

```txt
Đêm qua, người chơi sau đã chết: [Danh sách tên].
```

Không công bố nguyên nhân chết.

#### 5.4.11. Thảo luận và vote

```txt
Thời gian thảo luận bắt đầu.
```

```txt
Thời gian thảo luận đã kết thúc. Tất cả người chơi chuẩn bị bỏ phiếu.
```

```txt
Bắt đầu bỏ phiếu treo cổ.
```

```txt
Bỏ phiếu đã kết thúc. Hệ thống đang xử lý kết quả.
```

#### 5.4.12. Công bố kết quả vote

```txt
Người bị treo cổ là: [Tên người chơi].
```

Nếu hòa phiếu:

```txt
Kết quả bỏ phiếu hòa. Không ai bị treo cổ trong lượt này.
```

#### 5.4.13. Công bố thắng thua

```txt
Trò chơi kết thúc. Phe Ma Sói chiến thắng.
```

```txt
Trò chơi kết thúc. Phe Dân Làng chiến thắng.
```

```txt
Trò chơi kết thúc. Thằng Khờ chiến thắng.
```

```txt
Trò chơi kết thúc. Kẻ Tẩm Dầu chiến thắng.
```

```txt
Trò chơi kết thúc. Phe Người Yêu chiến thắng.
```

### 5.5. Yêu cầu điều khiển âm thanh trên Host

Host cần có bảng điều khiển âm thanh gồm:

- Nút bật/tắt giọng đọc.
- Nút bật/tắt ambient noise.
- Thanh chỉnh âm lượng giọng đọc.
- Thanh chỉnh âm lượng nhạc nền.
- Nút đọc lại câu hiện tại.
- Hiển thị câu đang được đọc.
- Trạng thái âm thanh: đang đọc, đã đọc xong, lỗi phát âm thanh.

### 5.6. Yêu cầu chống lỗi âm thanh

Do trình duyệt thường chặn autoplay âm thanh nếu người dùng chưa tương tác, hệ thống phải yêu cầu Host bấm nút kích hoạt âm thanh trước khi bắt đầu game.

Luồng đề xuất:

1. Host vào phòng.
2. Màn hình hiển thị nút `Kích hoạt âm thanh`.
3. Host bấm nút.
4. Hệ thống test đọc một câu ngắn:

```txt
Âm thanh đã sẵn sàng.
```

5. Sau đó mới cho phép Host bắt đầu ban đêm.

Nếu Text-To-Speech lỗi, hệ thống vẫn phải hiển thị câu thông báo dạng chữ lớn để Host có thể tự đọc.

---

## 6. Giao diện người dùng

## 6.1. Nguyên tắc UI chung

- Giao diện ưu tiên mobile-first.
- Ban đêm dùng nền tối để tránh lộ mặt người chơi.
- Nút bấm phải to, dễ bấm trên điện thoại.
- Không hiển thị thông tin bí mật của người khác.
- Mỗi phase cần có trạng thái rõ ràng.
- Khi mất kết nối, client phải hiển thị cảnh báo.

## 6.2. Giao diện Host

Host cần các màn hình sau:

### 6.2.1. Màn hình tạo phòng

Hiển thị:

- Nút tạo phòng.
- Mã phòng sau khi tạo.
- Link tham gia phòng.
- QR code tham gia phòng nếu có thể.

### 6.2.2. Màn hình lobby

Hiển thị:

- Room code.
- Danh sách người chơi đã tham gia.
- Trạng thái kết nối của từng người.
- Giỏ chọn role.
- Tổng số người chơi.
- Tổng số role đã chọn.
- Cảnh báo nếu số role chưa đủ.
- Nút bắt đầu game.

### 6.2.3. Màn hình điều khiển game

Hiển thị:

- Phase hiện tại: Đêm / Ngày / Vote / Kết thúc.
- Đêm thứ mấy hoặc ngày thứ mấy.
- Role hiện đang được gọi.
- Câu âm thanh đang đọc.
- Trạng thái đã submit hành động của role hiện tại.
- Nút chuyển bước tiếp theo.
- Nút đọc lại câu hiện tại.
- Nút tạm dừng / tiếp tục âm thanh.
- Nút dừng game khẩn cấp.

### 6.2.4. Màn hình kết quả ban đêm

Hiển thị:

- Danh sách người chết trong đêm.
- Không hiển thị nguyên nhân chết cho player.
- Host có thể xem chi tiết debug nếu bật chế độ debug.

### 6.2.5. Màn hình vote

Hiển thị:

- Danh sách player còn sống.
- Ai đã vote, ai chưa vote.
- Bảng xếp hạng số phiếu realtime.
- Người đang có phiếu cao nhất đưa lên trên.
- Nút kết thúc vote.

### 6.2.6. Màn hình kết thúc game

Hiển thị:

- Phe thắng.
- Danh sách role thật của toàn bộ player.
- Timeline tóm tắt các đêm/ngày nếu có.
- Nút tạo ván mới.

## 6.3. Giao diện Client

Client cần các màn hình sau:

### 6.3.1. Màn hình vào phòng

Hiển thị:

- Ô nhập tên người chơi.
- Ô nhập mã phòng.
- Nút tham gia.

### 6.3.2. Màn hình chờ

Hiển thị:

- Tên player.
- Room code.
- Danh sách người chơi trong phòng.
- Trạng thái chờ Host bắt đầu.

### 6.3.3. Màn hình xem role

Sau khi game bắt đầu, player được xem:

- Tên role của mình.
- Phe của mình.
- Mô tả ngắn kỹ năng.
- Nút xác nhận đã hiểu.

### 6.3.4. Màn hình ngủ ban đêm

Yêu cầu:

- Nền đen gần như hoàn toàn.
- Chỉ có hiệu ứng pulse rất mờ để biết máy vẫn hoạt động.
- Không hiển thị role hoặc thông tin nhạy cảm.
- Không có nút thao tác.

### 6.3.5. Màn hình thức theo role

Khi tới lượt role của player:

- Màn hình đổi màu nhẹ theo phe:
  - Dân: xanh lá.
  - Sói: đỏ.
  - Phe thứ ba: tím.
- Hiển thị hướng dẫn ngắn.
- Hiển thị danh sách mục tiêu hợp lệ.
- Sau khi chọn xong, hiển thị trạng thái đã gửi.
- Sau đó tự quay lại màn hình ngủ.

### 6.3.6. Màn hình ban ngày

Hiển thị:

- Ai đã chết đêm qua.
- Trạng thái sống/chết của bản thân.
- Đồng hồ thảo luận.
- Khi đến vote, hiển thị danh sách player còn sống để vote.

### 6.3.7. Màn hình player đã chết

Nếu player chết:

- Hiển thị trạng thái đã chết.
- Không được vote.
- Không được dùng kỹ năng.
- Vẫn có thể xem thông báo chung.

---

## 7. Role và logic chức năng

## 7.1. Danh sách role phiên bản đầu

### 7.1.1. Dân làng

Phe: Dân.

Logic:

- Không có kỹ năng ban đêm.
- Ban đêm luôn ở màn hình ngủ.
- Thắng khi toàn bộ Sói chết.

### 7.1.2. Bảo vệ

Phe: Dân.

Logic:

- Mỗi đêm chọn 1 người để bảo vệ.
- Không được bảo vệ cùng một người trong 2 đêm liên tiếp.
- Nếu người được bảo vệ bị Sói cắn, người đó không chết vì Sói cắn.

Client ban đêm:

- Hiển thị danh sách player còn sống.
- Disable người đã bảo vệ ở đêm trước.

### 7.1.3. Thợ săn

Phe: Dân.

Logic:

- Mỗi đêm chọn 1 người làm mục tiêu kéo theo.
- Nếu Thợ săn chết, mục tiêu đã chọn cũng chết.
- Cần lưu mục tiêu mới nhất của Thợ săn.

Client ban đêm:

- Hiển thị danh sách player còn sống trừ bản thân.
- Cho chọn 1 mục tiêu.

### 7.1.4. Tiên tri

Phe: Dân.

Logic:

- Mỗi đêm chọn 1 người để soi.
- Backend trả về kết quả: `Sói` hoặc `Không phải Sói`.
- Sói nguyền chưa bị nguyền tính là không phải Sói.
- Sói nguyền đã hóa Sói tính là Sói.

Client ban đêm:

- Hiển thị danh sách player còn sống.
- Sau khi chọn, hiện popup kết quả bí mật.

### 7.1.5. Phù thủy

Phe: Dân.

Logic:

- Có 2 bình:
  - `healing_potion_available = true`.
  - `poison_potion_available = true`.
- Mỗi bình chỉ được dùng 1 lần trong cả game.
- Ban đêm, Phù thủy biết ai bị Sói cắn.
- Nếu còn bình cứu, có thể cứu người bị Sói cắn.
- Nếu còn bình độc, có thể chọn 1 người để giết.
- Sau khi dùng bình, flag chuyển thành false.

Client ban đêm:

- Nếu có người bị Sói cắn và còn bình cứu: hiện nút cứu.
- Nếu còn bình độc: hiện danh sách người để độc.
- Có thể bỏ qua không dùng bình.

### 7.1.6. Ma Sói thường

Phe: Sói.

Logic:

- Các Sói biết nhau.
- Ban đêm cùng vote chọn 1 người để cắn.
- Backend lấy mục tiêu có nhiều phiếu Sói nhất.
- Nếu hòa phiếu Sói, có thể chọn ngẫu nhiên trong các mục tiêu cao phiếu hoặc yêu cầu Sói vote lại. Phiên bản đầu nên chọn ngẫu nhiên để đơn giản.

Client ban đêm:

- Hiển thị danh sách Sói cùng phe.
- Hiển thị danh sách player còn sống không phải Sói để chọn cắn.
- Cho vote mục tiêu cắn.

### 7.1.7. Sói nguyền

Phe ban đầu: Dân.

Phe sau khi bị Sói cắn: Sói.

Logic:

- Ban đầu được tính là Dân.
- Nếu bị Sói cắn, không chết ngay mà chuyển phe từ Dân sang Sói.
- Sau khi hóa Sói, được tính là Sói trong điều kiện thắng.
- Sau khi hóa Sói, giao diện ban đêm đổi sang giao diện Sói.

Client:

- Trước khi hóa Sói: giống Dân thường.
- Sau khi hóa Sói: thấy danh sách Sói và được vote cắn cùng Sói.

### 7.1.8. Cupid

Phe: Thứ ba hoặc độc lập tùy luật.

Logic phiên bản đầu:

- Chỉ được gọi ở đêm đầu tiên.
- Chọn 2 player để ghép đôi.
- Nếu một người trong cặp đôi chết, người còn lại cũng chết theo.
- Nếu cặp đôi gồm 1 Sói và 1 Dân, tạo phe đặc biệt `Phe Người Yêu`.
- Phe Người Yêu thắng khi cặp đôi là những người duy nhất còn sống, hoặc sống cùng Cupid nếu chọn luật cho phép Cupid sống cùng cặp đôi.

Client ban đêm:

- Đêm đầu tiên hiển thị danh sách player.
- Chọn đúng 2 người.

### 7.1.9. Kẻ tẩm dầu

Phe: Thứ ba.

Logic:

- Mỗi đêm chọn tối đa 2 player còn sống chưa bị tẩm dầu.
- Player được chọn có flag `is_oiled = true`.
- Kẻ tẩm dầu thắng ngay khi toàn bộ player còn sống đều có `is_oiled = true`.

Client ban đêm:

- Hiển thị danh sách player còn sống chưa bị tẩm dầu.
- Cho chọn tối đa 2 người.

### 7.1.10. Thằng Khờ

Phe: Thứ ba.

Logic:

- Không có kỹ năng ban đêm.
- Nếu bị treo cổ bằng vote ban ngày, game kết thúc ngay.
- Kết quả: Thằng Khờ thắng.

Client:

- Ban đêm ngủ.
- Ban ngày vote như người chơi bình thường nếu còn sống.

---

## 8. Thứ tự gọi role ban đêm

Thứ tự gọi role đề xuất:

Đêm đầu tiên:

```txt
1. Cupid
2. Kẻ tẩm dầu
3. Bảo vệ
4. Thợ săn
5. Ma Sói
6. Phù thủy
7. Tiên tri
```

Từ đêm thứ hai trở đi:

```txt
1. Kẻ tẩm dầu
2. Bảo vệ
3. Thợ săn
4. Ma Sói
5. Phù thủy
6. Tiên tri
```

Ghi chú:

- Cupid chỉ gọi đêm đầu tiên.
- Dân làng và Thằng Khờ không cần gọi vì không có kỹ năng ban đêm.
- Role không tồn tại trong phòng thì bỏ qua.
- Role đã chết thì không được gọi, trừ khi luật riêng yêu cầu.

---

## 9. Xử lý kết quả ban đêm

Backend cần gom tất cả hành động ban đêm rồi xử lý theo thứ tự hợp lý.

### 9.1. Dữ liệu hành động ban đêm

Mỗi action gồm:

```txt
action_id
room_id
night_number
actor_player_id
actor_role
action_type
target_player_id
target_player_ids
created_at
```

Ví dụ action type:

```txt
CUPID_LINK
OIL_MARK
PROTECT
HUNTER_MARK
WEREWOLF_BITE
WITCH_HEAL
WITCH_POISON
SEER_CHECK
```

### 9.2. Resolve ban đêm

Thứ tự xử lý đề xuất:

1. Xác định mục tiêu Sói cắn.
2. Kiểm tra Sói nguyền nếu bị cắn.
3. Kiểm tra Bảo vệ có bảo vệ đúng mục tiêu không.
4. Kiểm tra Phù thủy có cứu không.
5. Kiểm tra Phù thủy có độc ai không.
6. Xác định danh sách chết chính thức.
7. Xử lý Thợ săn kéo chết nếu Thợ săn chết.
8. Xử lý Cupid kéo chết nếu một người trong cặp đôi chết.
9. Cập nhật trạng thái alive/dead.
10. Kiểm tra Kẻ tẩm dầu có thắng không.
11. Chuyển sang ban ngày.

### 9.3. Không công bố nguyên nhân chết

Ban ngày chỉ công bố danh sách người chết.

Không công bố:

- Ai bị Sói cắn.
- Ai bị Phù thủy độc.
- Ai chết vì Cupid.
- Ai chết vì Thợ săn.

---

## 10. Vote ban ngày

### 10.1. Điều kiện vote

- Chỉ player còn sống được vote.
- Mỗi player còn sống được vote 1 lần.
- Có thể đổi vote trước khi Host kết thúc vote nếu hệ thống cho phép.
- Phiên bản đầu nên cho phép đổi vote để dễ dùng.

### 10.2. Xử lý kết quả vote

Backend đếm số phiếu.

- Người có phiếu cao nhất bị treo cổ.
- Nếu hòa phiếu cao nhất, phiên bản đầu xử lý là không ai bị treo cổ.
- Nếu người bị treo cổ là Thằng Khờ, game kết thúc ngay và Thằng Khờ thắng.
- Nếu người bị treo cổ thuộc cặp đôi Cupid, người còn lại cũng chết theo.
- Sau khi xử lý chết do vote, backend kiểm tra điều kiện thắng thua.

---

## 11. Điều kiện thắng thua

Backend chạy hàm:

```txt
check_game_over(room_id)
```

Hàm này được gọi ở các thời điểm:

- Sau khi xử lý kết quả ban đêm.
- Sau khi xử lý kết quả vote.
- Sau khi có hiệu ứng chết dây chuyền.
- Sau khi Kẻ tẩm dầu đánh dấu người chơi.

### 11.1. Thứ tự ưu tiên kiểm tra

Thứ tự kiểm tra đề xuất:

```txt
1. Thằng Khờ thắng nếu vừa bị treo cổ.
2. Kẻ tẩm dầu thắng nếu tất cả người sống đều đã bị tẩm dầu.
3. Phe Người Yêu thắng nếu thỏa điều kiện.
4. Phe Dân thắng nếu không còn Sói sống.
5. Phe Sói thắng nếu số Sói sống >= số Dân sống.
6. Nếu chưa có điều kiện nào đúng, game tiếp tục.
```

### 11.2. Phe Sói thắng

Điều kiện:

```txt
Số Sói còn sống >= Số Dân còn sống
```

Và không có phe thứ ba nào đạt điều kiện thắng đặc biệt.

Sói nguyền đã hóa Sói được tính vào phe Sói.

### 11.3. Phe Dân thắng

Điều kiện:

```txt
Số Sói còn sống = 0
```

Tất cả Ma Sói thường và Sói nguyền đã hóa Sói đều phải chết.

### 11.4. Thằng Khờ thắng

Điều kiện:

```txt
Người bị treo cổ bằng vote ban ngày có role = Thằng Khờ
```

Game kết thúc ngay.

### 11.5. Kẻ tẩm dầu thắng

Điều kiện:

```txt
Tất cả player còn sống đều có is_oiled = true
```

Game kết thúc ngay.

### 11.6. Phe Người Yêu thắng

Điều kiện:

- Cupid đã ghép đôi 1 Sói và 1 Dân.
- Hai người yêu còn sống.
- Những người còn sống chỉ còn cặp đôi, hoặc cặp đôi cùng Cupid nếu luật cho phép Cupid sống cùng phe Người Yêu.

### 11.7. Hoãn kết thúc game

Một số trường hợp không nên kết thúc game ngay dù điều kiện số lượng có vẻ đã đủ.

Ví dụ:

- Sói bằng số Dân nhưng Phù thủy còn sống và còn bình độc.
- Phù thủy có khả năng giết Sói ở đêm sau.

Logic:

```txt
Nếu Sói >= Dân
và Phù thủy còn sống
và poison_potion_available = true
thì có thể cho game tiếp tục thêm một đêm.
```

Phiên bản đầu có thể triển khai đơn giản:

- Có bật option `enable_delayed_game_over`.
- Nếu option tắt, dùng luật thắng cơ bản.
- Nếu option bật, áp dụng logic hoãn game.

---

## 12. Realtime events

Backend và frontend giao tiếp qua WebSocket bằng event JSON.

### 12.1. Format event chung

```json
{
  "type": "EVENT_NAME",
  "room_id": "ABC123",
  "payload": {},
  "timestamp": "2026-05-31T12:00:00Z"
}
```

### 12.2. Event từ server gửi xuống client

```txt
ROOM_CREATED
PLAYER_JOINED
PLAYER_LEFT
PLAYER_CONNECTION_CHANGED
ROLE_CART_UPDATED
GAME_STARTED
YOUR_ROLE_ASSIGNED
PHASE_CHANGED
NIGHT_STARTED
ROLE_CALLED
PLAYER_WAKE_ALLOWED
PLAYER_SLEEP
ACTION_RECEIVED
NIGHT_RESOLVED
DAY_STARTED
DISCUSSION_STARTED
VOTE_STARTED
VOTE_UPDATED
VOTE_ENDED
PLAYER_ELIMINATED
GAME_OVER
ERROR_MESSAGE
```

### 12.3. Event từ client gửi lên server

```txt
JOIN_ROOM
UPDATE_ROLE_CART
START_GAME
START_NIGHT
CALL_NEXT_ROLE
SUBMIT_NIGHT_ACTION
START_DAY
START_VOTE
SUBMIT_VOTE
END_VOTE
REQUEST_AUDIO_REPLAY
END_GAME
```

### 12.4. Nguyên tắc bảo mật realtime

Backend không được gửi role bí mật của người này cho người khác.

Ví dụ:

- Player A chỉ nhận role của Player A.
- Sói chỉ thấy danh sách Sói nếu player đó là Sói.
- Tiên tri chỉ nhận kết quả soi của chính mình.
- Phù thủy chỉ nhận thông tin người bị Sói cắn nếu tới lượt Phù thủy.

---

## 13. REST API đề xuất

REST API dùng cho các thao tác không cần realtime hoặc cần khởi tạo.

### 13.1. Room API

```txt
POST /api/rooms
GET /api/rooms/{room_code}
POST /api/rooms/{room_code}/join
POST /api/rooms/{room_id}/start
POST /api/rooms/{room_id}/end
```

### 13.2. Player API

```txt
GET /api/rooms/{room_id}/players
GET /api/players/{player_id}
PATCH /api/players/{player_id}/ready
```

### 13.3. Role API

```txt
GET /api/roles
PUT /api/rooms/{room_id}/role-cart
GET /api/rooms/{room_id}/role-cart
```

### 13.4. Game API

```txt
GET /api/rooms/{room_id}/state
POST /api/rooms/{room_id}/night/start
POST /api/rooms/{room_id}/night/action
POST /api/rooms/{room_id}/night/resolve
POST /api/rooms/{room_id}/day/start
POST /api/rooms/{room_id}/vote/start
POST /api/rooms/{room_id}/vote
POST /api/rooms/{room_id}/vote/end
```

---

## 14. Database schema đề xuất

### 14.1. rooms

```txt
id
room_code
host_token
status
current_phase
current_day
current_night
current_role_turn
created_at
updated_at
```

### 14.2. players

```txt
id
room_id
name
session_token
role_code
side
is_alive
is_connected
is_host
joined_at
updated_at
```

### 14.3. roles

```txt
id
code
name
side
description
night_order
is_active
```

### 14.4. room_role_cart

```txt
id
room_id
role_code
quantity
```

### 14.5. game_states

```txt
id
room_id
phase
night_number
day_number
current_role_code
enable_delayed_game_over
winner
is_game_over
updated_at
```

### 14.6. night_actions

```txt
id
room_id
night_number
actor_player_id
actor_role_code
action_type
target_player_id
target_player_ids
created_at
```

### 14.7. votes

```txt
id
room_id
day_number
voter_player_id
target_player_id
created_at
updated_at
```

### 14.8. cupid_links

```txt
id
room_id
player_1_id
player_2_id
is_mixed_side
created_at
```

### 14.9. player_status_effects

```txt
id
room_id
player_id
is_oiled
is_cursed_wolf_activated
protected_last_night_by
hunter_target_id
updated_at
```

### 14.10. witch_states

```txt
id
room_id
player_id
healing_potion_available
poison_potion_available
updated_at
```

---

## 15. Bảo mật và chống gian lận

### 15.1. Session token

Mỗi player khi join phòng được cấp `session_token`.

Token dùng để:

- Xác định player khi reconnect.
- Ngăn người khác gửi action thay player.
- Lưu trong localStorage của trình duyệt.

### 15.2. Host token

Host có `host_token` riêng.

Chỉ Host được:

- Bắt đầu game.
- Chuyển phase.
- Gọi role tiếp theo.
- Bắt đầu vote.
- Kết thúc vote.
- Kết thúc game.

### 15.3. Validate action

Backend phải kiểm tra:

- Player có tồn tại trong room không.
- Player còn sống không.
- Player có đúng role đang được gọi không.
- Phase hiện tại có cho phép action này không.
- Target có hợp lệ không.
- Player đã submit action chưa.
- Role có còn kỹ năng không.

Client không được tự quyết định logic game.

---

## 16. Khả năng chịu lỗi

### 16.1. Player reload trang

Nếu player reload:

- Client đọc `session_token` từ localStorage.
- Gửi reconnect đến backend.
- Backend trả lại trạng thái hiện tại của player.
- Player tiếp tục ở đúng màn hình hiện tại.

### 16.2. Player mất kết nối

Nếu player mất kết nối:

- Host thấy trạng thái player là disconnected.
- Game không tự dừng.
- Nếu tới lượt player bị mất kết nối, Host có thể chờ hoặc bỏ qua.

### 16.3. Host reload trang

Nếu Host reload:

- Host dùng `host_token` để reconnect.
- Backend trả lại trạng thái room hiện tại.
- Host tiếp tục điều khiển game.

### 16.4. Lỗi âm thanh

Nếu Text-To-Speech không hoạt động:

- Host vẫn thấy câu cần đọc bằng chữ lớn.
- Có nút đọc lại.
- Có cảnh báo âm thanh lỗi.

---

## 17. Yêu cầu hiệu năng

Hệ thống cần hỗ trợ tối thiểu:

```txt
1 phòng chơi
1 Host
10 Player
11 WebSocket connections
```

Yêu cầu:

- Chuyển phase dưới 1 giây trong điều kiện mạng ổn định.
- Vote cập nhật realtime dưới 1 giây.
- Action ban đêm được lưu chính xác.
- Không mất trạng thái khi player reload.
- Backend xử lý game logic tập trung, không phụ thuộc vào client.

---

## 18. Tiêu chí nghiệm thu

### 18.1. Tạo phòng

- Host tạo được phòng.
- Hệ thống sinh room code.
- Player join bằng room code.
- Host thấy danh sách player realtime.

### 18.2. Setup role

- Host tăng/giảm số lượng role.
- Hệ thống tính tổng role.
- Không cho bắt đầu nếu role ít hơn player.
- Chia role ngẫu nhiên.
- Đảm bảo có ít nhất 1 Ma Sói thường.

### 18.3. Ban đêm

- Host phát được âm thanh bắt đầu đêm.
- Ambient noise chạy trong đêm.
- Hệ thống gọi role theo đúng thứ tự.
- Chỉ player đúng role được mở màn hình thao tác.
- Player khác vẫn ở màn hình ngủ.
- Action được gửi và lưu thành công.
- Sau khi submit, player quay lại màn hình ngủ.

### 18.4. Ban ngày

- Hệ thống công bố đúng danh sách người chết.
- Không công bố nguyên nhân chết.
- Có đồng hồ thảo luận.
- Vote hoạt động realtime.
- Người cao phiếu nhất bị loại.
- Hòa phiếu thì không ai bị loại.

### 18.5. Điều kiện thắng

- Dân thắng khi không còn Sói.
- Sói thắng khi số Sói sống >= số Dân sống.
- Thằng Khờ thắng khi bị treo cổ.
- Kẻ tẩm dầu thắng khi toàn bộ người sống đã bị tẩm dầu.
- Cặp đôi Cupid thắng nếu thỏa điều kiện.

### 18.6. Âm thanh Host

- Host kích hoạt được âm thanh trước game.
- Hệ thống đọc được câu thông báo bằng Text-To-Speech.
- Có nút đọc lại câu hiện tại.
- Có thể bật/tắt ambient noise.
- Có thể chỉnh âm lượng.
- Nếu âm thanh lỗi, câu thông báo vẫn hiển thị rõ để Host đọc thủ công.

### 18.7. Deploy

- Frontend deploy được lên Vercel.
- Backend deploy được lên Render.
- Database dùng Supabase PostgreSQL.
- Người chơi có thể truy cập bằng link public.
- Tối thiểu 10 player và 1 Host có thể vào cùng 1 phòng để chơi.

---

## 19. Phạm vi phiên bản MVP

Phiên bản MVP nên làm trước các chức năng sau:

```txt
1. Tạo phòng và join phòng.
2. Setup role bằng giỏ role.
3. Chia role ngẫu nhiên có ít nhất 1 Sói.
4. WebSocket realtime cho Host và Client.
5. Màn hình ngủ/thức ban đêm.
6. Gọi role bằng Text-To-Speech.
7. Ambient noise ban đêm.
8. Logic cơ bản: Sói, Dân, Bảo vệ, Tiên tri, Phù thủy.
9. Công bố người chết ban ngày.
10. Vote treo cổ.
11. Điều kiện thắng Dân/Sói.
12. Deploy Vercel + Render + Supabase.
```

Các role nâng cao nên làm sau:

```txt
1. Cupid.
2. Kẻ tẩm dầu.
3. Thằng Khờ.
4. Sói nguyền.
5. Thợ săn.
6. Hoãn kết thúc game.
7. Timeline lịch sử game.
8. QR code join phòng.
9. Debug mode cho Host.
```

---

## 20. Gợi ý cấu trúc source code

### 20.1. Frontend

```txt
frontend/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── host/
│   │   ├── player/
│   │   └── common/
│   ├── pages/
│   │   ├── HostRoom.vue
│   │   ├── PlayerJoin.vue
│   │   └── PlayerGame.vue
│   ├── stores/
│   │   ├── roomStore.ts
│   │   ├── playerStore.ts
│   │   └── gameStore.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── websocket.ts
│   │   └── audioService.ts
│   └── main.ts
```

### 20.2. Backend

```txt
backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   ├── websocket/
│   ├── game_engine/
│   │   ├── role_assignment.py
│   │   ├── night_resolver.py
│   │   ├── vote_resolver.py
│   │   ├── win_condition.py
│   │   └── role_rules.py
│   └── utils/
├── alembic/
├── requirements.txt
└── Dockerfile
```

---

## 21. Nguyên tắc quan trọng khi AI hỗ trợ code

Khi yêu cầu AI viết code cho project này, cần nhấn mạnh:

```txt
Backend là nguồn sự thật duy nhất.
Client chỉ gửi yêu cầu/hành động.
Backend phải validate mọi hành động.
Không gửi thông tin role bí mật cho sai người.
Mọi thay đổi phase phải broadcast qua WebSocket.
Âm thanh Host là chức năng quan trọng, không được bỏ qua.
Ưu tiên MVP trước, role nâng cao làm sau.
```

Prompt mẫu để đưa cho AI coding assistant:

```txt
Dựa trên tài liệu SRS này, hãy triển khai từng phần theo MVP. Không tự ý đổi stack công nghệ. Frontend dùng Vue 3 + Vite + TailwindCSS + Pinia, backend dùng FastAPI + WebSocket, database dùng Supabase PostgreSQL. Backend phải là nguồn sự thật duy nhất. Đặc biệt chú ý hệ thống âm thanh Host gồm Text-To-Speech, ambient noise, nút đọc lại câu hiện tại và fallback hiển thị câu đọc nếu âm thanh lỗi.
```

