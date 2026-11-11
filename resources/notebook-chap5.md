# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 5: Hệ chuyên gia (Expert system)

### Mục lục

- [5.1 Giới thiệu](#51-giới-thiệu)
- [5.2 Cấu trúc](#52-cấu-trúc)
  - [5.2.1 Cơ sở tri thức](#521-cơ-sở-tri-thức)
  - [5.2.2 Bộ nhớ làm việc](#522-bộ-nhớ-làm-việc)
  - [5.2.3 Động cơ suy luận](#523-động-cơ-suy-luận)
  - [5.2.4 Các thành phần khác](#524-các-thành-phần-khác)
- [5.3 Đặc trưng cơ bản của ES](#53-đặc-trưng-cơ-bản-của-es)
- [5.4 Các kỹ thuật suy luận](#54-các-kỹ-thuật-suy-luận)
  - [5.4.1 Các hình thức suy luận](#541-các-hình-thức-suy-luận)
  - [5.4.2 Suy luận tiến và suy luận lùi](#542-suy-luận-tiến-và-suy-luận-lùi)

**Vấn đề:** Tri thức của chuyên gia con người khan hiếm, đắt đỏ và khó nhân rộng.
**Mục tiêu:** Xây dựng chương trình mô phỏng khả năng giải quyết vấn đề của chuyên gia, trong một lĩnh vực hẹp.

> Hệ chuyên gia (Expert System, ES) = **Cơ sở tri thức** + **Động cơ suy luận**. ES là ứng dụng điển hình của hệ luật sinh (chương 4).

### 5.1 Giới thiệu

ES là chương trình được thiết kế theo mô hình giải quyết vấn đề của chuyên gia con người, gồm 2 khối cơ bản:

| Khối | Nội dung |
|---|---|
| **Cơ sở tri thức** (CSTT) | Chứa tri thức của một lĩnh vực do chuyên gia con người chuyển giao: khái niệm cơ bản, sự kiện, luật và quan hệ giữa chúng. |
| **Động cơ suy luận** | Bộ xử lý tri thức, mô phỏng cách suy luận của chuyên gia. Kết hợp thông tin người dùng mô tả với CSTT để đưa ra kết luận hay đề nghị. |

### 5.2 Cấu trúc

#### 5.2.1 Cơ sở tri thức

> **Kỹ sư tri thức** thu thập tri thức từ chuyên gia rồi mã hoá vào CSTT. Cách mã hoá được trình bày ở chương 6 (biểu diễn tri thức).

Cách biểu diễn tiêu biểu là dùng **luật**. Ví dụ chẩn đoán xe:

```
RULE 1:
    IF   "Xe không thể khởi động được"
    THEN "Vấn đề trong hệ thống điện"

RULE 2:
    IF   "Vấn đề trong hệ thống điện"
    AND  "Điện thế ắc-quy nhỏ hơn 10 Volt"
    THEN "Lỗi tại bộ ắc-quy"
```

#### 5.2.2 Bộ nhớ làm việc

Chứa các **sự kiện của vấn đề**, do người dùng nhập vào lúc đầu hoặc do ES sinh ra trong quá trình suy luận.

- ES dùng chung cho nhiều người (từ xa): bộ nhớ làm việc được phân nhóm theo **phiên làm việc** (session) của từng người dùng.
- ES có thể nạp thêm thông tin từ nguồn ngoài (CSDL, bảng tính, sensor, ...) vào đầu session hoặc khi cần.

#### 5.2.3 Động cơ suy luận

So trùng các sự kiện trong bộ nhớ làm việc với tri thức trong CSTT để dẫn ra kết luận. Với CSTT dạng luật, cách hoạt động giống hệ luật sinh:

1. Tìm luật có tiền đề trùng với các sự kiện trong bộ nhớ làm việc.
2. Thêm kết luận của luật đó vào bộ nhớ làm việc.
3. Tiếp tục tìm sự so trùng khác cho đến khi có kết luận.

#### 5.2.4 Các thành phần khác

- **Tiện ích giải thích:** cho biết ES đã suy luận ra kết luận như thế nào, vì sao hỏi một câu hỏi.
- **Giao diện người dùng:** nhập sự kiện và nhận kết luận.

### 5.3 Đặc trưng cơ bản của ES

| # | Đặc trưng | Ý chính |
|---|---|---|
| 1 | Phân tách tri thức và điều khiển | Đặc điểm phân biệt ES với chương trình truyền thống (xem chương 4). |
| 2 | Sở hữu tri thức chuyên gia | Tri thức trong CSTT chính là giá trị của ES; có thể nhân bản và cập nhật khi hệ thống đang chạy. |
| 3 | Chuyên gia trong lĩnh vực hẹp | Lĩnh vực hẹp thì lượng tri thức nhỏ, dễ quản lý và dễ thử nghiệm chiến lược điều khiển. Tri thức thường được chia thành từng mảng. |
| 4 | Suy luận trên ký hiệu | Tri thức biểu diễn bằng ký hiệu nên tận dụng được các giải thuật xử lý ký hiệu (như phép toán vị từ ở chương 1). |
| 5 | Suy luận có heuristic | Dùng kinh nghiệm để giải quyết hiệu quả hơn. Ví dụ: chẩn đoán xe thì kiểm tra hệ thống điện trước; nghi ung thư thì kiểm tra tiền sử gia đình trước. Cần cách đánh giá thứ tự ưu tiên của các luật. |
| 6 | Cho phép suy luận không chính xác | Làm việc được với thông tin thiếu hoặc mơ hồ, như bác sĩ cấp cứu không kịp làm đủ xét nghiệm. Hiện thực bằng các luật dành riêng cho tình huống thiếu thông tin. |
| 7 | Bị giới hạn vào vấn đề giải quyết | Không phải vấn đề nào cũng làm ES được; nếu lĩnh vực chưa cần đến chuyên gia con người thì khó xây dựng ES thành công. |
| 8 | Độ phức tạp vừa phải | Vấn đề quá khó (chuyên gia mất vài giờ) nên chia thành nhiều bài toán con, mỗi bài toán một ES. |
| 9 | Có khả năng bị lỗi | Giống chuyên gia con người. ES cần **lưu vết suy luận** để khi người dùng báo kết luận sai thì ghi nhận và theo hướng suy luận khác. Chương trình truyền thống không có đặc điểm này, nhưng không có nghĩa là tốt hơn; mỗi loại có đặc điểm riêng. |

### 5.4 Các kỹ thuật suy luận

> Suy luận là quá trình làm việc với tri thức, sự kiện và chiến lược giải toán để dẫn tới kết luận.

#### 5.4.1 Các hình thức suy luận

| Hình thức | Ý chính |
|---|---|
| Diễn dịch | Từ tiền đề suy ra kết luận chắc chắn (ví dụ Modus Ponens). |
| Quy nạp | Từ nhiều trường hợp cụ thể rút ra kết luận tổng quát. |
| Tương tự | Dựa vào trường hợp tương tự đã biết để suy ra trường hợp mới. |
| Khả sai | Kết luận hợp lý nhưng có thể sai (ví dụ chẩn đoán từ triệu chứng). |
| Common-sense | Dùng tri thức thường thức của đời sống hằng ngày. |
| Đơn điệu | Thêm tri thức mới không làm mất các kết luận đã có. |
| Không đơn điệu | Thêm thông tin mới có thể làm **rút lại** kết luận cũ (chim bay được, nhưng chim cánh cụt thì không). |

#### 5.4.2 Suy luận tiến và suy luận lùi

| | Suy luận tiến | Suy luận lùi |
|---|---|---|
| Bản chất bài toán | Có thông tin, tìm xem suy ra được gì | Lập giả thiết, tìm xem chứng minh được không |
| Ưu điểm | Từ ít sự kiện ban đầu dẫn ra được nhiều thông tin | Hướng đến một GOAL cụ thể nên câu hỏi liên quan nhau; chỉ khảo sát nhánh tri thức đang quan tâm |
| Nhược điểm | Không biết sự kiện nào quan trọng, nên có thể hỏi nhiều câu thừa hoặc không liên quan | Bám theo dòng suy luận định trước, khó rẽ sang goal khác |
| Phù hợp | Hoạch định, giám sát, điều khiển, diễn dịch | Chẩn đoán, kê toa, gỡ rối |

**Meta-rule:** luật dùng để hướng không gian tri thức đang khảo sát sang một vùng khác; là cách khắc phục nhược điểm bám theo goal cũ của suy luận lùi.

**Ví dụ** (dùng 2 luật chẩn đoán xe ở mục 5.2.1):

```
Suy luận tiến:
  Sự kiện: "Xe không khởi động được", "Điện thế ắc-quy = 9V"
  → RULE 1 thoả → thêm "Vấn đề trong hệ thống điện"
  → RULE 2 thoả → kết luận "Lỗi tại bộ ắc-quy"

Suy luận lùi:
  Giả thuyết: "Lỗi tại bộ ắc-quy"
  → RULE 2 → cần "Vấn đề trong hệ thống điện" và "Điện thế < 10V"
  → "Vấn đề trong hệ thống điện" → RULE 1 → cần "Xe không khởi động được"
  → hỏi người dùng 2 sự kiện còn thiếu, đối chiếu → chứng minh được hay không
```