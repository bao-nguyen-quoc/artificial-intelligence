# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 2: Biểu diễn bài toán và tìm kiếm

### Mục lục

- [2.1 Tổng quan](#21-tổng-quan)
- [2.2 Biểu diễn trong không gian trạng thái](#22-biểu-diễn-trong-không-gian-trạng-thái)
  - [2.2.1 Trò chơi tám số](#221-trò-chơi-tám-số)
  - [2.2.2 Tìm đường trong mê cung](#222-tìm-đường-trong-mê-cung)
  - [2.2.3 Bài toán người và quỷ sang sông](#223-bài-toán-người-và-quỷ-sang-sông)
- [2.3 Một số bài toán khác](#23-một-số-bài-toán-khác)
- [2.4 Đồ thị tìm kiếm](#24-đồ-thị-tìm-kiếm)
- [2.5 Cây tìm kiếm](#25-cây-tìm-kiếm)

### 2.1 Tổng quan

**Vấn đề:** Nhiều bài toán AI không thể giải trực tiếp bằng một công thức hay phương trình đơn giản. Thay vào đó, ta cần biểu diễn bài toán dưới dạng không gian trạng thái, rồi tìm đường đi từ trạng thái ban đầu đến trạng thái đích.
**Mục tiêu:** Hiểu cách biểu diễn bài toán và phân loại các chiến lược tìm kiếm.

> Tìm kiếm là một thuật toán lấy đầu vào là một bài toán, và đầu ra là lời giải cho bài toán đó - thường là sau khi cân nhắc giữa một loạt các lời giải có thể có.

**Không gian trạng thái** trong tìm kiếm:
- Là tập các trạng thái có thể có của bài toán và các toán tử di chuyển trạng thái.
- Được biểu diễn bằng cây, đồ thị, ...

Nói cách khác: **Không gian trạng thái** trả lời "bài toán có thể ở những trạng thái nào?", **toán tử** trả lời "từ trạng thái này có thể chuyển sang trạng thái nào?", và **thuật toán tìm kiếm** trả lời "đi theo thứ tự nào để đến đích hiệu quả nhất?".

**Các phương pháp tìm kiếm:**

| Nhóm | Đặc điểm | Ví dụ |
|---|---|---|
| **Tìm kiếm không có thông tin** (blind search) | Thuật toán **không biết gì** về khoảng cách hay chi phí từ trạng thái hiện tại đến đích. Nó chỉ mở rộng các node theo một chiến lược cố định. | BFS, DFS, Uniform Cost Search, Iterative Deepening DFS |
| **Tìm kiếm có thông tin** (heuristic search) | Thuật toán sử dụng **hàm heuristic h(n)** để ước lượng chi phí từ node hiện tại đến đích, từ đó ưu tiên khám phá những hướng "hứa hẹn" hơn. | Greedy Best-First Search, A* |
| **Tìm kiếm đối kháng** (adversarial search) | Dùng trong môi trường có **nhiều tác nhân** cạnh tranh nhau (thường là 2 người chơi đối lập). Mục tiêu không chỉ là "đến đích" mà là **thắng** đối thủ, trong khi đối thủ cũng đang cố tối ưu hóa theo hướng ngược lại. | Minimax, Alpha-Beta Pruning |

### 2.2 Biểu diễn trong không gian trạng thái

> Để máy tính giải được bài toán, trước hết phải mô hình hoá bài toán đó: xác định trạng thái là gì, toán tử nào chuyển đổi trạng thái, đâu là trạng thái đầu và đâu là trạng thái đích. Dưới đây là một số bài toán kinh điển minh hoạ.

#### 2.2.1 Trò chơi tám số

**Bài toán:** Cho một lưới 3×3 với 8 ô số và một ô trống. Mục tiêu là di chuyển các số sao cho chúng xếp theo thứ tự từ 1 đến 8, với ô trống ở cuối.

**Trạng thái đầu**

```
| 1 |   | 4 |
| 6 | 3 | 2 |
| 7 | 8 | 5 |
```

```
{ 1, null, 4, 6, 3, 2, 7, 8, 5 }
```

**Trạng thái cuối**

```
| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 |   |
```

```
{ 1, 2, 3, 4, 5, 6, 7, 8, null }
```

**Toán tử** (mô tả theo hướng di chuyển của ô kề vào ô trống):

| Toán tử | Mô tả | Điều kiện |
|---|---|---|
| Up | Ô ở dưới ô trống di chuyển lên trên | Ô trống không nằm ở hàng cuối |
| Down | Ô ở trên ô trống di chuyển xuống dưới | Ô trống không nằm ở hàng đầu |
| Left | Ô ở bên phải ô trống di chuyển sang trái | Ô trống không nằm ở cột cuối |
| Right | Ô ở bên trái ô trống di chuyển sang phải | Ô trống không nằm ở cột đầu |

Trạng thái sẽ thay đổi phụ thuộc vào toán tử. Tuỳ thuộc vào vị trí ô trống mà một số toán tử sẽ không thực hiện được (ví dụ: ô trống ở góc trên-trái thì chỉ có 2 toán tử hợp lệ là Up và Left).

#### 2.2.2 Tìm đường trong mê cung

**Bài toán:** Cho mê cung trên lưới ô vuông 4×4, Robot bắt đầu từ ô (0,0) và cần di chuyển đến ô (3,3). Một số ô là tường, không đi qua được.

**Trạng thái đầu:** `(0, 0)`

**Trạng thái cuối:** `(3, 3)`

**Toán tử:**

| Toán tử | Mô tả | Điều kiện |
|---|---|---|
| Up | Di chuyển lên trên | Ô phía trên không phải tường, không ra ngoài lưới |
| Down | Di chuyển xuống dưới | Ô phía dưới không phải tường, không ra ngoài lưới |
| Left | Di chuyển sang trái | Ô bên trái không phải tường, không ra ngoài lưới |
| Right | Di chuyển sang phải | Ô bên phải không phải tường, không ra ngoài lưới |

Tương tự bài tám số: trạng thái thay đổi theo toán tử, và tuỳ vị trí hiện tại mà một số toán tử không thực hiện được.

#### 2.2.3 Bài toán người và quỷ sang sông

*to be defined*

### 2.3 Một số bài toán khác

Ngoài các bài toán minh hoạ ở trên, nhiều bài toán kinh điển khác cũng được biểu diễn và giải bằng tìm kiếm trong không gian trạng thái:

- **Tháp Hà Nội** - di chuyển n đĩa giữa 3 cọc, mỗi lần 1 đĩa, đĩa lớn không được nằm trên đĩa nhỏ.
- **8 hậu** - đặt 8 quân hậu trên bàn cờ 8×8 sao cho không quân nào tấn công quân nào.
- **Cờ vua / Cờ tướng** - bài toán đối kháng, không gian trạng thái cực lớn.
- **Tìm đường** (pathfinding) - ứng dụng trong bản đồ, game, robot tự hành.
- ...

### 2.4 Đồ thị tìm kiếm

> Khi không gian trạng thái có thể quay vòng (một trạng thái có thể đạt được từ nhiều đường đi khác nhau), ta biểu diễn bằng **đồ thị**. Mỗi đỉnh là một trạng thái, mỗi cạnh là một toán tử. Thuật toán tìm kiếm trên đồ thị cần ghi nhớ các trạng thái đã duyệt (tập `closed`) để tránh lặp vô hạn.

*Tìm hiểu thêm bên ngoài.*

### 2.5 Cây tìm kiếm

> Khi không gian trạng thái không có vòng lặp, hoặc ta chấp nhận mở rộng lại các trạng thái đã gặp, ta biểu diễn quá trình tìm kiếm bằng **cây**. Gốc cây là trạng thái ban đầu, mỗi nhánh tương ứng với một toán tử, và lá là trạng thái đích hoặc trạng thái không mở rộng được nữa.

*Tìm hiểu thêm bên ngoài.*
