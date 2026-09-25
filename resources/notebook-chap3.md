# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 3: Các thuật toán tìm kiếm

### Mục lục

- [3.1 Tìm kiếm không thông tin (blind search)](#31-tìm-kiếm-không-thông-tin-blind-search)
  - [3.1.1 Tìm kiếm theo chiều rộng (BFS)](#311-tìm-kiếm-theo-chiều-rộng-bfs)
  - [3.1.2 Tìm kiếm theo chiều sâu (DFS)](#312-tìm-kiếm-theo-chiều-sâu-dfs)
  - [3.1.3 Tìm kiếm sâu dần (IDS)](#313-tìm-kiếm-sâu-dần-ids)
  - [3.1.4 Tìm kiếm chi phí cực tiểu (Uniform Cost Search)](#314-tìm-kiếm-chi-phí-cực-tiểu-uniform-cost-search)
- [3.2 Tìm kiếm có thông tin (informed search)](#32-tìm-kiếm-có-thông-tin-informed-search)
  - [3.2.1 Tìm kiếm Heuristic](#321-tìm-kiếm-heuristic)
  - [3.2.2 Tìm kiếm ước lượng (Best-First Search)](#322-tìm-kiếm-ước-lượng-best-first-search)
  - [3.2.3 Thuật toán A*](#323-thuật-toán-a)
- [3.3 Tìm kiếm trên cây trò chơi (Game Tree Search)](#33-tìm-kiếm-trên-cây-trò-chơi-game-tree-search)
  - [3.3.1 Tìm kiếm Minimax](#331-tìm-kiếm-minimax)
  - [3.3.2 Cắt tỉa Alpha-Beta](#332-cắt-tỉa-alpha-beta)
- [3.4 Các vấn đề khác](#34-các-vấn-đề-khác)

### 3.1 Tìm kiếm không thông tin (blind search)

> Nhóm thuật toán này không biết gì về "đích ở đâu" - chúng chỉ mở rộng các node theo một chiến lược cố định (FIFO, LIFO, chi phí tăng dần, ...). Đơn giản nhưng đảm bảo tính đầy đủ trong nhiều trường hợp.

#### 3.1.1 Tìm kiếm theo chiều rộng (BFS)

> Ý tưởng: duyệt cây theo từng lớp, ưu tiên các đỉnh **gần đỉnh xuất phát nhất** trước. Đảm bảo tìm được lời giải nông nhất (ít bước nhất).

**Thuật toán:**

1. Cho đỉnh xuất phát vào `open` (hoạt động theo quy tắc **FIFO**).
2. Nếu `open` rỗng → tìm kiếm thất bại, kết thúc.
3. Lấy đỉnh đầu trong `open` ra, gọi là `O`. Cho `O` vào `closed`.
4. Nếu `O` là đỉnh đích → tìm kiếm thành công, kết thúc.
5. Tìm tất cả các đỉnh con của `O` **không thuộc `open` và `closed`**, **thêm vào cuối** `open`.
6. Quay lại bước 2.

**Độ phức tạp:**

| | Giá trị | Giải thích |
|---|---|---|
| Thời gian | $O(b^d)$ | Phải duyệt toàn bộ các node ở mỗi lớp |
| Không gian | $O(b^d)$ | Phải lưu toàn bộ biên (frontier) trong bộ nhớ |

Trong đó: `b` = branching factor (số nhánh tối đa), `d` = depth (độ sâu của lời giải).

#### 3.1.2 Tìm kiếm theo chiều sâu (DFS)

> Ý tưởng: ngược lại với BFS - ưu tiên đi **sâu nhất có thể** trước, rồi quay lui khi gặp ngõ cụt. Tiết kiệm bộ nhớ hơn BFS nhưng không đảm bảo tìm lời giải ngắn nhất.

**Thuật toán:**

1. Cho đỉnh xuất phát vào `open` (hoạt động theo quy tắc **LIFO**).
2. Nếu `open` rỗng → tìm kiếm thất bại, kết thúc.
3. Lấy đỉnh đầu trong `open` ra, gọi là `O`. Cho `O` vào `closed`.
4. Nếu `O` là đỉnh đích → tìm kiếm thành công, kết thúc.
5. Tìm tất cả các đỉnh con của `O` **không thuộc `open` và `closed`**, **thêm vào đầu** `open`.
6. Quay lại bước 2.

**Độ phức tạp:**

| | Giá trị | Giải thích |
|---|---|---|
| Thời gian | $O(b^d)$ | Trường hợp xấu nhất vẫn phải duyệt hết |
| Không gian | $O(b \cdot d)$ | Chỉ cần lưu đường đi hiện tại + các anh em chưa duyệt ở mỗi lớp |

*Lưu ý:* DFS có thể rơi vào vòng lặp vô hạn nếu không kiểm tra trạng thái đã duyệt (tập `closed`), đặc biệt trên đồ thị có chu trình.

#### 3.1.3 Tìm kiếm sâu dần (IDS)

*to be defined*

#### 3.1.4 Tìm kiếm chi phí cực tiểu (Uniform Cost Search)

> Khi các cạnh có chi phí khác nhau, BFS không còn đảm bảo tìm lời giải tối ưu. Uniform Cost Search giải quyết bằng cách luôn mở rộng node có **tổng chi phí từ gốc thấp nhất**.

**Đặt vấn đề:** Khi một bài toán có nhiều nghiệm, ta thường muốn chọn phương án có "chi phí thấp nhất".

Ví dụ: Đi từ TP.A đến TP.B, sao cho nhanh nhất, rẻ nhất. BFS và DFS không đảm bảo tối ưu cho bài toán này.

**Thuật toán:**

1. Cho đỉnh xuất phát vào `open`.
2. Nếu `open` rỗng → tìm kiếm thất bại, kết thúc.
3. Lấy đỉnh đầu trong `open` ra, gọi là `O`. Cho `O` vào `closed`.
4. Nếu `O` là đỉnh đích → tìm kiếm thành công, kết thúc.
5. Tìm tất cả các đỉnh con của `O` **không thuộc `open` và `closed`**, cho vào `open` theo thứ tự tăng dần về **tổng chi phí g(n) từ đỉnh xuất phát**.
6. Quay lại bước 2.

**Tính chất:**

- Lời giải được phát hiện đầu tiên cũng là nghiệm có "chi phí thấp nhất" (optimal).
- Nếu bài toán có lời giải, đảm bảo thuật toán sẽ dừng (complete).
- Nếu mọi cạnh đều có chi phí bằng 1, UCS trở thành BFS.

### 3.2 Tìm kiếm có thông tin (informed search)

> Thay vì "mù quáng" duyệt theo thứ tự cố định, các thuật toán nhóm này sử dụng **tri thức bổ sung** (hàm heuristic) để ước lượng hướng đi triển vọng, giúp tìm lời giải nhanh hơn đáng kể.

#### 3.2.1 Tìm kiếm Heuristic

**Heuristic là gì?**

> Heuristic = theo kinh nghiệm, phán đoán. Là cách ước lượng "còn bao xa nữa" mà không cần biết chính xác.

**Ví dụ thực tế:** Khi không rõ đường đi, mọi người thường nhắm về hướng cần tới để đi - ưu tiên đường đi có khoảng cách đường chim bay ngắn nhất tới đích. Đó chính là tư duy heuristic.

> Tìm kiếm Heuristic là tìm kiếm sử dụng kiến thức phỏng đoán chi phí từ đỉnh đang xét đến đích, nhằm ưu tiên các hướng "hứa hẹn" hơn.

#### 3.2.2 Tìm kiếm ước lượng (Best-First Search)

> Ý tưởng: tại mỗi bước, mở rộng node có **giá trị heuristic h(n) nhỏ nhất** - tức node được "phỏng đoán" là gần đích nhất.

**Thuật toán:**

1. Cho đỉnh xuất phát vào `open`.
2. Nếu `open` rỗng → tìm kiếm thất bại, kết thúc.
3. Lấy đỉnh đầu trong `open` ra, gọi là `O`. Cho `O` vào `closed`.
4. Nếu `O` là đỉnh đích → tìm kiếm thành công, kết thúc.
5. Tìm tất cả các đỉnh con của `O` **không thuộc `open` và `closed`**, cho vào `open` theo thứ tự tăng dần về **khoảng cách ước lượng h(n) đến đích**.
6. Quay lại bước 2.

**Tính chất:**

- Lời giải được phát hiện đầu tiên **không đảm bảo** là nghiệm có "chi phí thấp nhất" (not optimal).
- Khá giống UCS về cấu trúc, nhưng thường tiết kiệm hơn về mặt không gian vì hướng về đích nhanh hơn.

#### 3.2.3 Thuật toán A*

> A* kết hợp ưu điểm của cả hai: **chi phí thực tế** (từ UCS) + **ước lượng** (từ Best-First Search), tạo ra thuật toán vừa hiệu quả vừa đảm bảo tối ưu khi heuristic thỏa điều kiện.

Sử dụng hàm đánh giá:

```
f(n) = g(n) + h'(n)
```

| Thành phần | Ý nghĩa |
|---|---|
| `g(n)` | Chi phí thực tế từ đỉnh xuất phát tới đỉnh đang xét |
| `h'(n)` | Chi phí ước lượng từ đỉnh đang xét tới đích |
| `f(n)` | Tổng chi phí ước lượng của toàn bộ đường đi qua n |

**Thuật toán:**

1. Cho đỉnh xuất phát vào `open`.
2. Nếu `open` rỗng → tìm kiếm thất bại, kết thúc.
3. Lấy đỉnh đầu trong `open` ra, gọi là `O`. Cho `O` vào `closed`.
4. Nếu `O` là đỉnh đích → tìm kiếm thành công, kết thúc.
5. Tìm tất cả các đỉnh con của `O` **không thuộc `open` và `closed`**, cho vào `open` theo thứ tự tăng dần về **hàm đánh giá f(n) = g(n) + h'(n)**.
6. Quay lại bước 2.

**Tính chất:**

- Lời giải được phát hiện đầu tiên **đảm bảo** "chi phí thấp nhất" (optimal) - với điều kiện heuristic là **admissible**: `h'(n) ≤ h(n)` (ước lượng luôn ≤ chi phí thực).
- So với UCS thì tiết kiệm hơn về mặt không gian nhờ heuristic hướng dẫn.
- Theo thực nghiệm, A* thường nhanh hơn đáng kể so với các thuật toán blind search.

### 3.3 Tìm kiếm trên cây trò chơi (Game Tree Search)

> Thuật toán A* chỉ thích hợp với các bài toán **không có tính đối kháng** (dò đường mê cung, puzzle, 8 con hậu, ...). Các bài toán đối kháng (cờ vua, cờ tướng, tic-tac-toe) đòi hỏi tư duy khác: mình muốn đến đích, đồng thời đối thủ cũng đang cố cản phá. Cần thuật toán chuyên biệt.

#### 3.3.1 Tìm kiếm Minimax

> Ý tưởng: trong trò chơi 2 người, lượt MAX cố **tối đa hoá** lợi ích, lượt MIN cố **tối thiểu hoá** lợi ích của MAX. Cả hai đều chơi tối ưu.

Minimax được xây dựng dựa trên giả thiết:
- Cả 2 đối thủ có cùng kiến thức và không gian trạng thái của trò chơi (ví dụ cờ vua: 2 người chơi cùng chia sẻ luật chơi và trạng thái bàn cờ).
- Cả 2 đối thủ có cùng mức cố gắng như nhau.

```
          [MAX]
        /       \
    [MIN]        [MIN]
    /   \        /   \
   3     5      2     9
  / \   / \    / \   / \
 0   1 2   3  4   5 6   7
```

**Thứ tự thực thi:** DFS từ trên xuống, trả giá trị từ dưới lên.

> Minimax dùng DFS (Depth-First Search): đi sâu xuống tận lá trước, rồi mới "bubble up" giá trị lên từng lớp.

**Minimax với độ sâu giới hạn**

Trong thực tế, không gian trạng thái thường quá lớn để mở rộng toàn bộ (ví dụ: cờ vua có ~10^120 trạng thái). Minimax thuần tuý đòi hỏi phải có toàn bộ cây trò chơi để gán giá trị cho lá rồi tính ngược lên - điều này không khả thi.

Hướng giải quyết: **Giới hạn** không gian trạng thái theo **độ sâu** và/hoặc **số node con**.

**Giới hạn theo độ sâu**

Thay vì đào sâu đến tận cuối game, chỉ nhìn trước `d` bước rồi dừng:

```
Minimax thuần túy:
ROOT -> ... -> ... LEAF (kết thúc game) - lúc này mới evaluate được

Minimax depth-limited:
ROOT -> lớp 1 -> lớp 2 -> lớp 3 - dừng tại đây và evaluate luôn dù game chưa kết thúc
```

**Giới hạn theo node con**

Không duyệt tất cả nước đi có thể, mà chỉ giữ lại những nước đi **có triển vọng** theo một quy tắc nào đó:

```
Các node con có thể duyệt: [A, B, C, D, E, F, G]
            |
            V
(Lọc dựa trên hàm heuristic nào đó)
            |
            V
Các node con đáng giá để duyệt: [C, E, G]
```

Ví dụ: trong cờ vua - "Chỉ xét các nước đi mang tính tấn công/phòng thủ, lược bỏ các nước đi trung lập hơn."

**Đánh đổi:** mất tính chính xác tuyệt đối (không còn guaranteed optimal) nhưng chạy được trong thực tế.

**Thuật toán (pseudocode):**

```
function minimax(node, depth, maximizingPlayer)
  if node is "end node" or depth = 0
    return value(node)
  if maximizingPlayer
    MAX := -∞
    foreach child of node
      MAX := max(MAX, minimax(child, depth - 1, false))
    return MAX
  else
    MIN := +∞
    foreach child of node
      MIN := min(MIN, minimax(child, depth - 1, true))
    return MIN
```

**Vấn đề:** kể cả khi giới hạn độ sâu, số đỉnh con của một đỉnh bất kỳ vẫn rất lớn.

Ví dụ: Cờ vua trung bình có branching factor ≈ 35. Với độ sâu giới hạn = 4, cần ít nhất ~$35^4$ ≈ 1.5 triệu phép đánh giá. Vì vậy cần phương pháp **giảm số nhánh** phải duyệt.

#### 3.3.2 Cắt tỉa Alpha-Beta

> Cắt tỉa Alpha-Beta cho phép loại bỏ các nhánh **chắc chắn không ảnh hưởng** đến kết quả cuối cùng - giảm đáng kể số node phải đánh giá mà **không thay đổi** kết quả so với Minimax đầy đủ.

**Mục đích:** Làm giảm số nhánh trong cây tìm kiếm mà không ảnh hưởng đến sự đánh giá của đỉnh gốc.

**Ý tưởng cốt lõi:**
- `α` (alpha): giá trị tốt nhất mà MAX đã đảm bảo được (cận dưới).
- `β` (beta): giá trị tốt nhất mà MIN đã đảm bảo được (cận trên).
- Khi `α ≥ β` → nhánh hiện tại không thể cải thiện kết quả → **cắt bỏ** (prune).

**Thuật toán (pseudocode):**

```
function minimax(node, depth, maximizingPlayer)
  return alphaBeta(node, depth, -∞, +∞, true)
// -----------------------------------------------------------
function alphaBeta(node, depth, alpha, beta, maximizingPlayer)
  if node is "end node" or depth = 0
    return value(node)
  if maximizingPlayer
    foreach child of node
      alpha := max(alpha, alphaBeta(child, depth - 1, alpha, beta, false))
      if alpha >= beta
        break
    return alpha
  else
    foreach child of node
      beta := min(beta, alphaBeta(child, depth - 1, alpha, beta, true))
      if alpha >= beta
        break
    return beta
// -----------------------------------------------------------
function alphaBeta(node, depth, alpha, beta)
  if node is "end node" or depth = 0
    return value(node)
  foreach child of node
    alpha := max(alpha, -alphaBeta(child, depth - 1, -beta, -alpha))
    if alpha >= beta
      break
  return alpha
```

*Lưu ý:* Phiên bản cuối cùng (Negamax) gộp logic MAX/MIN vào cùng một hàm bằng cách đảo dấu - gọn hơn nhưng tương đương về kết quả.

### 3.4 Các vấn đề khác

**Độ phức tạp thời gian vs Không gian**

| Loại | Đo lường | Câu hỏi |
|---|---|---|
| **Thời gian** (Time Complexity) | Số lượng **thao tác/bước** mà thuật toán thực hiện | "Thuật toán cần thực hiện bao nhiêu phép tính?" |
| **Không gian** (Space Complexity) | Lượng **bộ nhớ** mà thuật toán cần dùng trong quá trình chạy | "Thuật toán cần lưu trữ bao nhiêu dữ liệu cùng lúc?" |