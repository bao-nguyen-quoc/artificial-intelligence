# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 6: Biểu diễn tri thức

### Mục lục

- [6.1 Khái niệm](#61-khái-niệm)
- [6.2 Các lược đồ biểu diễn tri thức](#62-các-lược-đồ-biểu-diễn-tri-thức)
- [6.3 Mạng ngữ nghĩa](#63-mạng-ngữ-nghĩa)
  - [6.3.1 Mở rộng mạng](#631-mở-rộng-mạng)
  - [6.3.2 Tính thừa kế và tính ngoại lệ](#632-tính-thừa-kế-và-tính-ngoại-lệ)
  - [6.3.3 Phép toán trên mạng ngữ nghĩa](#633-phép-toán-trên-mạng-ngữ-nghĩa)
- [6.4 Phụ thuộc khái niệm](#64-phụ-thuộc-khái-niệm)
- [6.5 Đồ thị khái niệm](#65-đồ-thị-khái-niệm)
- [6.6 Lược đồ cấu trúc Frame](#66-lược-đồ-cấu-trúc-frame)
- [6.7 Lược đồ cấu trúc Script](#67-lược-đồ-cấu-trúc-script)

**Vấn đề:** Máy tính không hiểu tri thức "thực", cần chuyển nó thành dạng tính toán được để xây dựng cơ sở tri thức cho hệ chuyên gia.
**Mục tiêu:** Nắm các lược đồ biểu diễn tri thức chính và biết khi nào dùng loại nào.

### 6.1 Khái niệm

> Biểu diễn tri thức là phương pháp mã hoá tri thức để thành lập cơ sở tri thức cho các hệ thống dựa trên tri thức (knowledge-based system). Công việc chính là chuyển **tri thức thực** của lĩnh vực thành **tri thức tính toán** bằng các lược đồ phù hợp.

| Tri thức thực của lĩnh vực | Ánh xạ sang | Tri thức tính toán |
|---|---|---|
| Đối tượng | → | Đối tượng tính toán |
| Quan hệ giữa các đối tượng | → | Quan hệ tính toán |

### 6.2 Các lược đồ biểu diễn tri thức

*Chú ý:* cần phân biệt **lược đồ biểu diễn** (scheme) và **môi trường hiện thực** (medium), giống như phân biệt cấu trúc dữ liệu và ngôn ngữ lập trình: cùng một kiểu bản ghi có thể hiện thực bằng Pascal, C, ... Một lược đồ cũng có thể hiện thực bằng nhiều ngôn ngữ lập trình.

| Lược đồ | Cách biểu diễn | Ví dụ |
|---|---|---|
| **Logic** | Biểu thức logic hình thức; luật suy diễn rất rõ ràng (chương 1). Dạng khai báo. | Logic mệnh đề, logic vị từ |
| **Thủ tục** | Tập chỉ thị lệnh cho biết **bằng cách nào** giải quyết vấn đề (ngược với dạng khai báo như logic và mạng). | Hệ luật sinh, luật trong CSTT của ES |
| **Mạng** | Đồ thị: đỉnh là đối tượng/khái niệm, cung là quan hệ. Dạng khai báo. | Mạng ngữ nghĩa, phụ thuộc khái niệm, đồ thị khái niệm |
| **Cấu trúc** | Mở rộng của lược đồ mạng: node là cấu trúc dữ liệu phức tạp gồm các **slot** có tên và trị, hoặc một thủ tục. Tích hợp cả khai báo lẫn thủ tục. | Frame, script, object |

**Các vấn đề cần chú ý khi xây dựng lược đồ:**

- Đối tượng và quan hệ biểu diễn được những gì trong lĩnh vực? Ví dụ `chieucao(nam, 170)` biểu diễn được "Nam cao 1m70", nhưng "An cao hơn Nam" thì không còn là một trị cụ thể.
- Phân biệt **nội hàm** và **ngoại diện** của khái niệm như thế nào?
- Biểu diễn **meta-knowledge** (tri thức về tri thức) như thế nào?
- Biểu diễn tính **phân cấp**: kế thừa, ngoại lệ, trị mặc định, đa thừa kế được đặc tả ra sao?
- Tích hợp **tri thức thủ tục** vào bản thân mô tả đối tượng như thế nào, và thủ tục chạy khi nào? (Frame ở mục 6.6 trả lời câu này.)

### 6.3 Mạng ngữ nghĩa

> Lược đồ mạng dùng đồ thị: **đỉnh** biểu diễn đối tượng, **cung** biểu diễn quan hệ giữa chúng.

#### 6.3.1 Mở rộng mạng

Chỉ cần thêm đỉnh và cung nối với các đỉnh có sẵn. Đỉnh mới biểu diễn đối tượng hoặc thuộc tính.

#### 6.3.2 Tính thừa kế và tính ngoại lệ

- **Thừa kế:** đặc điểm nổi bật của mạng ngữ nghĩa, thể hiện bằng cung đặc biệt **IS-A**. Đỉnh con thừa hưởng thuộc tính của đỉnh cha.
- **Ngoại lệ:** định nghĩa cung quan hệ mới đến một đỉnh có trị khác; thuộc tính riêng ở đỉnh con ghi đè thuộc tính thừa kế.

```
Chim cánh cụt --is-a--> Chim --has--> Cánh
                         Chim --can--> Bay
Chim cánh cụt --cannot--> Bay           (ngoại lệ ghi đè)
```

#### 6.3.3 Phép toán trên mạng ngữ nghĩa

| Phép toán | Nội dung |
|---|---|
| **Cập nhật** | Thêm, xoá, sửa nút và cung; hợp nhất hai mạng. |
| **Truy vấn** | Biểu diễn câu hỏi thành mạng con có nút biến, rồi so khớp với mạng lớn. Ví dụ `Chim cánh cụt --sống ở--> ?x` cho `?x = Nam Cực`. |
| **Kế thừa** | Tìm thuộc tính ở chính nút, không có thì đi lên theo cung IS-A. Gặp thuộc tính riêng ở nút con thì dùng nó. |
| **Suy diễn trên đồ thị** | Tìm đường đi (BFS, DFS) giữa hai khái niệm; bắc cầu `A is-a B`, `B is-a C` ⇒ `A is-a C`; tìm giao điểm bằng lan truyền kích hoạt từ hai nút (Quillian). |
| **Đo tương đồng** | Dựa vào độ dài đường đi ngắn nhất hoặc nút cha chung gần nhất (dùng nhiều trên WordNet). |

### 6.4 Phụ thuộc khái niệm

> Schank và Rieger đề xuất một tập phần tử cơ bản để biểu diễn **ngữ nghĩa** của câu ngôn ngữ tự nhiên một cách đồng nhất: hai câu khác chữ nhưng cùng nghĩa phải có cùng biểu diễn.

**4 khái niệm cơ bản:**

| Ký hiệu | Ý nghĩa | Tương ứng |
|---|---|---|
| **ACT** (Action) | Hành động | Động từ |
| **PP** (Picture Producers) | Đối tượng | Danh từ |
| **AA** (Action Adder) | Bổ nghĩa cho hành động | Trạng từ |
| **PA** (Picture Adder) | Bổ nghĩa cho đối tượng | Tính từ |

**12 hành động nguyên thủy:** mọi hành động đều được phân rã thành một hoặc nhiều hành động dưới đây.

| Nhóm | Hành động | Ý nghĩa |
|---|---|---|
| Chuyển đổi | `ATRANS` | Chuyển quan hệ (sở hữu): cho, tặng, bán, mua |
| | `PTRANS` | Chuyển vị trí vật lý: đi, chạy, mang đến |
| | `MTRANS` | Chuyển thông tin tinh thần: nói, kể, tiết lộ |
| Vật lý | `PROPEL` | Tác động lực vật lý lên đối tượng: đẩy, ném |
| | `MOVE` | Di chuyển một bộ phận cơ thể: giơ tay |
| | `GRASP` | Nắm lấy đối tượng |
| | `INGEST` | Đưa vào cơ thể: ăn, uống |
| | `EXPEL` | Tống ra khỏi cơ thể |
| Tinh thần | `MBUILD` | Tạo thông tin tinh thần mới: quyết định, suy ra |
| | `CONC` | Nghĩ về một ý kiến |
| Giác quan | `SPEAK` | Tạo ra âm thanh |
| | `ATTEND` | Tập trung giác quan: nhìn, nghe |

**Ví dụ:**

```
"An đưa quyển sách cho Bình"        "An ăn cơm"
  ACT:    ATRANS                       ACT:    INGEST
  Actor:  An                           Actor:  An
  Object: quyển sách                   Object: cơm
  From:   An
  To:     Bình
```

Các quan hệ phụ thuộc (mũi tên nối Actor, ACT, Object, Direction, ...) tạo thành văn phạm quan hệ ngữ nghĩa, dùng để biểu diễn bên trong cho câu; xem thêm ở tài liệu chuyên sâu.

### 6.5 Đồ thị khái niệm

> Đồ thị khái niệm (Sowa) là đồ thị hữu hạn, liên thông, có **hai loại đỉnh**: đỉnh khái niệm và đỉnh quan hệ.

- **Đỉnh khái niệm** (hình chữ nhật, viết `[ ]`): khái niệm cụ thể (cái bàn, điện thoại) hay trừu tượng (tình yêu, văn hoá).
- **Đỉnh quan hệ** (hình oval, viết `( )`): chỉ quan hệ giữa các khái niệm nối đến nó.
- Chỉ đỉnh **khác loại** mới nối được với nhau. Vì đã có đỉnh quan hệ nên các cung **không cần gán nhãn**.

```
"An đưa quyển sách cho Bình"

[ĐƯA] ─(Agnt)→ [NGƯỜI: An]
  ├──(Obj)──→ [SÁCH]
  └──(Rcpt)─→ [NGƯỜI: Bình]
```

(`Agnt` là tác nhân, `Obj` là đối tượng, `Rcpt` là người nhận.)

### 6.6 Lược đồ cấu trúc Frame

> Frame (Minsky, 1974) là cấu trúc dữ liệu biểu diễn một **đối tượng hoặc tình huống điển hình**, gồm các **slot** (khe) có tên. Mỗi slot chứa trị và có thể gắn thêm thủ tục.

**Các thuộc tính (facet) của một slot:**

| Facet | Ý nghĩa |
|---|---|
| `value` | Trị cụ thể |
| `default` | Trị mặc định khi chưa biết |
| `range` | Miền giá trị hợp lệ |
| `if-needed` | Thủ tục chạy khi **cần trị mà slot đang rỗng** (tính theo yêu cầu) |
| `if-added` | Thủ tục chạy khi slot **được gán trị** |
| `if-removed` | Thủ tục chạy khi trị bị xoá |

Các frame nối với nhau bằng quan hệ `is-a` / `instance-of` tạo thành hệ phân cấp: frame con **thừa kế** slot của frame cha, và trị mặc định ở frame con **ghi đè** trị của cha (ngoại lệ).

```
Frame: Nguoi
  so_chan:   default 2

Frame: Sinh_vien                 (is-a: Nguoi)
  tuoi:      range 15..60, default 20
  truong:    (chưa biết)

Frame: Lan                       (instance-of: Sinh_vien)
  truong:    ĐHBK
  nam_sinh:  2003
  tuoi:      if-needed → nam_hien_tai - nam_sinh
```

Hỏi `Lan.so_chan` → không có ở `Lan`, thừa kế lên `Nguoi` → `2`. Hỏi `Lan.tuoi` → slot rỗng nên chạy `if-needed`.

So với mạng ngữ nghĩa, frame **gom toàn bộ thuộc tính của một đối tượng vào một cấu trúc** và cho phép gắn thủ tục.

### 6.7 Lược đồ cấu trúc Script

> Script (Schank và Abelson, 1977) mô tả **chuỗi sự kiện điển hình** trong một tình huống quen thuộc (đi ăn quán, đi khám bệnh), dùng để hiểu câu chuyện và **suy ra các sự kiện không được nói rõ**. Frame mô tả đối tượng/tình huống tĩnh, còn script mô tả diễn tiến theo thời gian.

**Các thành phần:**

| Thành phần | Nội dung |
|---|---|
| Tên | Tên kịch bản |
| Điều kiện vào | Điều kiện để kịch bản xảy ra |
| Vai (roles) | Những người tham gia |
| Đạo cụ (props) | Các vật liên quan |
| Cảnh (scenes) | Chuỗi sự kiện, thường viết bằng các hành động nguyên thủy của phụ thuộc khái niệm |
| Kết quả | Trạng thái sau khi kịch bản kết thúc |

```
Script: QUÁN_ĂN
  Điều kiện vào: K đói, K có tiền
  Vai:     K (khách), N (nhân viên phục vụ)
  Đạo cụ:  bàn, thực đơn, món ăn, tiền
  Cảnh 1 - Vào quán:    K PTRANS K vào quán; K ATTEND tìm bàn; K PTRANS K đến bàn
  Cảnh 2 - Gọi món:     N ATRANS thực đơn cho K; K MBUILD chọn món; K MTRANS món cho N
  Cảnh 3 - Ăn:          N ATRANS món ăn cho K; K INGEST món ăn
  Cảnh 4 - Thanh toán:  K MTRANS "tính tiền"; K ATRANS tiền cho N; K PTRANS K ra khỏi quán
  Kết quả: K no, K hết tiền, quán có thêm tiền
```

**Ví dụ suy luận:** "An vào quán, gọi phở rồi trả tiền ra về." Câu chuyện không nói An có ăn không, nhưng cảnh *Ăn* nằm giữa *Gọi món* và *Thanh toán* trong script, nên ngầm hiểu **An đã ăn phở**.

*Hạn chế:* script khá cứng nhắc, tình huống lệch khỏi kịch bản (phở nguội nên An bỏ về) cần thêm nhánh rẽ hoặc ngoại lệ.