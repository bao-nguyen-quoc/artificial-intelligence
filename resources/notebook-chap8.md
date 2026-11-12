# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 8: Thuật toán di truyền (Genetic algorithm)

### Mục lục

- [8.1 Khái niệm](#81-khái-niệm)
- [8.2 Thuật ngữ](#82-thuật-ngữ)
- [8.3 Sơ đồ thuật toán](#83-sơ-đồ-thuật-toán)
- [8.4 Các thành phần của GA](#84-các-thành-phần-của-ga)
  - [8.4.1 Mã hoá](#841-mã-hoá)
  - [8.4.2 Khởi tạo quần thể](#842-khởi-tạo-quần-thể)
  - [8.4.3 Hàm thích nghi và xử lý ràng buộc](#843-hàm-thích-nghi-và-xử-lý-ràng-buộc)
  - [8.4.4 Chọn lọc](#844-chọn-lọc)
  - [8.4.5 Lai ghép](#845-lai-ghép)
  - [8.4.6 Đột biến](#846-đột-biến)
  - [8.4.7 Thay thế và điều kiện dừng](#847-thay-thế-và-điều-kiện-dừng)
  - [8.4.8 Tham số](#848-tham-số)
- [8.5 Cơ sở lý thuyết](#85-cơ-sở-lý-thuyết)
- [8.6 Các bài toán ứng dụng](#86-các-bài-toán-ứng-dụng)
  - [8.6.1 Bài toán cái túi (Knapsack)](#861-bài-toán-cái-túi-knapsack)
  - [8.6.2 Bài toán đường đi Hamilton (Hamiltonian path)](#862-bài-toán-đường-đi-hamilton-hamiltonian-path)
  - [8.6.3 Bài toán người bán hàng (TSP)](#863-bài-toán-người-bán-hàng-tsp)
  - [8.6.4 Bài toán định vị cơ sở (Facility location)](#864-bài-toán-định-vị-cơ-sở-facility-location)
  - [8.6.5 Bài toán ghép cặp (Matching)](#865-bài-toán-ghép-cặp-matching)
  - [8.6.6 Bài toán xếp thùng (Bin packing)](#866-bài-toán-xếp-thùng-bin-packing)
  - [8.6.7 Bài toán phân công tổng quát (GAP)](#867-bài-toán-phân-công-tổng-quát-gap)
- [8.7 Ví dụ minh hoạ: giải bài toán cái túi bằng GA](#87-ví-dụ-minh-hoạ-giải-bài-toán-cái-túi-bằng-ga)
- [8.8 Tổng kết](#88-tổng-kết)

**Vấn đề:** Chương 7 cho thấy tính toán tiến hoá giải bài toán tối ưu bằng cách "tiến hoá" một quần thể lời giải. Cần một thuật toán cụ thể, đủ tổng quát để áp dụng cho nhiều bài toán tổ hợp khác nhau.
**Mục tiêu:** Hiểu các thành phần của thuật toán di truyền, biết chọn mã hoá và toán tử phù hợp với từng loại bài toán, và tự cài đặt được một bản GA hoàn chỉnh.

### 8.1 Khái niệm

> **Thuật toán di truyền** (Genetic Algorithm - GA) là thuật toán tìm kiếm tối ưu dựa trên quần thể, mô phỏng **chọn lọc tự nhiên** và **di truyền**: cá thể thích nghi tốt có nhiều cơ hội sinh sản hơn, con cái thừa hưởng (và pha trộn) đặc điểm của cha mẹ, thỉnh thoảng xuất hiện đột biến ngẫu nhiên.

- Do **John Holland** đề xuất (đặt nền móng trong cuốn *Adaptation in Natural and Artificial Systems*, 1975), được phổ biến rộng rãi sau đó (Goldberg và nhiều tác giả khác).
- Là đại diện tiêu biểu của họ thuật toán tiến hoá ở chương 7: dùng **cả ba** cơ chế chọn lọc, lai ghép, đột biến; cá thể thường là chuỗi gen mã hoá lời giải.

**Điểm khác với các phương pháp tìm kiếm ở các chương trước:**

| | BFS / DFS / A* | Thuật toán di truyền |
|---|---|---|
| Đơn vị làm việc | Một **đường đi / trạng thái** được xây dựng từng bước | Một **quần thể lời giải hoàn chỉnh** (có thể chưa tốt, thậm chí chưa hợp lệ) |
| Cách tiến triển | Mở rộng nút theo cấu trúc không gian trạng thái | Chọn lọc + biến đổi ngẫu nhiên có định hướng |
| Cần gì từ bài toán | Hàm kế tiếp, (heuristic) | Cách mã hoá và **hàm thích nghi** |
| Bảo đảm | Có thể bảo đảm tối ưu (A* với heuristic chấp nhận được) | Không bảo đảm tối ưu, cho lời giải tốt trong thời gian chấp nhận được |

### 8.2 Thuật ngữ

| Thuật ngữ GA | Ý nghĩa | Ví dụ (bài toán cái túi, 6 vật) |
|---|---|---|
| **Nhiễm sắc thể** (chromosome) / cá thể | Một lời giải ứng viên đã mã hoá | `110101` |
| **Gen** | Một thành phần của nhiễm sắc thể | Bit thứ 3 |
| **Alen** (allele) | Giá trị của gen | `0` hoặc `1` |
| **Locus** | Vị trí của gen trong nhiễm sắc thể | Vị trí 3 |
| **Kiểu gen** (genotype) | Dạng **mã hoá** của lời giải | Chuỗi bit `110101` |
| **Kiểu hình** (phenotype) | Lời giải **thực** sau khi giải mã | Chọn các vật 1, 2, 4, 6 |
| **Quần thể** (population) | Tập các cá thể ở một thời điểm | 20 chuỗi bit |
| **Độ thích nghi** (fitness) | Số đo chất lượng của cá thể | Tổng giá trị các vật được chọn |
| **Thế hệ** (generation) | Một vòng lặp của thuật toán | |

*Chú ý:* GA tìm kiếm trên **kiểu gen**, còn hàm thích nghi đánh giá **kiểu hình**. Việc giải mã kiểu gen thành kiểu hình là một phần của hàm thích nghi.

### 8.3 Sơ đồ thuật toán

```
Đầu vào: kích thước quần thể N, xác suất lai ghép Pc, xác suất đột biến Pm
1. Khởi tạo quần thể P(0) gồm N nhiễm sắc thể ngẫu nhiên
2. Tính fitness cho mọi cá thể của P(0)
3. t = 0
4. Lặp cho đến khi thoả điều kiện dừng:
     a. Giữ lại một số cá thể tốt nhất (elitism)
     b. Lặp cho đến khi đủ N cá thể mới:
          - Chọn lọc:  chọn 2 cha mẹ từ P(t) theo fitness
          - Lai ghép:  với xác suất Pc, trao đổi gen của cha mẹ để sinh 2 con
                       (ngược lại con = bản sao của cha mẹ)
          - Đột biến:  mỗi gen của con bị thay đổi với xác suất Pm
     c. P(t+1) = các cá thể mới;  tính fitness;  t = t + 1
5. Trả về cá thể tốt nhất tìm được
```

Đây chính là khung chung ở mục 7.3, cụ thể hoá bằng ba toán tử di truyền. Dạng trên gọi là GA **thế hệ** (generational: thay gần như toàn bộ quần thể mỗi vòng). Dạng **trạng thái ổn định** (steady-state) mỗi vòng chỉ sinh một vài con rồi thay vào những cá thể kém nhất.

### 8.4 Các thành phần của GA

Để áp dụng GA cho một bài toán mới, cần quyết định 5 việc: **mã hoá**, **hàm thích nghi**, **chọn lọc**, **lai ghép/đột biến**, **tham số**. Trong đó mã hoá và toán tử là những chỗ "mang tri thức của bài toán" nhiều nhất.

#### 8.4.1 Mã hoá

| Kiểu mã hoá | Nhiễm sắc thể | Bài toán điển hình |
|---|---|---|
| **Nhị phân** | Chuỗi bit | Cái túi (chọn/không chọn), định vị cơ sở (mở/đóng) |
| **Hoán vị** | Một cách sắp xếp các phần tử `1..n` | TSP, đường đi Hamilton, xếp thùng (qua bộ giải mã) |
| **Số nguyên / nhãn** | Vector, mỗi gen thuộc một tập giá trị rời rạc | Phân công (gen j = tác nhân làm việc j), tô màu đồ thị |
| **Số thực** | Vector số thực | Tối ưu tham số liên tục |
| **Nhóm** (grouping) | Danh sách các nhóm | Xếp thùng, phân cụm |
| **Cây** | Cây cú pháp | Lập trình di truyền (mục 7.5.4) |

**Nguyên tắc chọn mã hoá:**

- Mỗi lời giải phải có ít nhất một nhiễm sắc thể tương ứng, và tốt nhất mọi nhiễm sắc thể đều giải mã được thành lời giải **hợp lệ**.
- Phép lai ghép/đột biến nên cho ra nhiễm sắc thể còn **hợp lệ** (hoặc sửa lại được rẻ). Ví dụ hoán vị cần toán tử riêng (mục 8.4.5).
- Phép biến đổi nhỏ trên nhiễm sắc thể nên gây thay đổi **nhỏ** trên lời giải, để tìm kiếm cục bộ có ý nghĩa.

#### 8.4.2 Khởi tạo quần thể

- **Ngẫu nhiên:** mặc định, bảo đảm đa dạng. Với mã hoá hoán vị, dùng xáo trộn (shuffle) để luôn hợp lệ.
- **Gieo bằng heuristic:** đưa vào vài cá thể tạo từ thuật toán tham lam (ví dụ láng giềng gần nhất cho TSP). Hội tụ nhanh hơn nhưng dễ giảm đa dạng nếu gieo quá nhiều.

#### 8.4.3 Hàm thích nghi và xử lý ràng buộc

Hàm thích nghi `f(x)` đo chất lượng lời giải; GA **chỉ cần** giá trị này, không cần đạo hàm hay cấu trúc bài toán.

- **Bài toán cực tiểu hoá** (TSP: độ dài `L`) cần đổi thành **cực đại hoá**: `f = 1/L` hoặc `f = C_max − L`.
- Chọn lọc roulette (mục 8.4.4) yêu cầu `f ≥ 0`.

**Xử lý ràng buộc** khi nhiễm sắc thể giải mã ra lời giải vi phạm điều kiện:

| Cách | Nội dung | Ưu / nhược |
|---|---|---|
| **Loại bỏ** (death penalty) | Cho fitness = 0 (hoặc loại hẳn) | Đơn giản; lãng phí khi nhiều cá thể vi phạm, và mọi cá thể vi phạm có fitness bằng nhau nên không biết cái nào "gần hợp lệ hơn" |
| **Phạt** (penalty) | `f = giá trị − λ · mức vi phạm` | Phân biệt được mức độ vi phạm; cần chỉnh `λ` |
| **Sửa chữa** (repair) | Biến lời giải vi phạm thành hợp lệ (ví dụ bỏ bớt vật) | Quần thể luôn hợp lệ; cần viết thủ tục sửa cho từng bài toán |
| **Bộ giải mã** (decoder) | Mã hoá gián tiếp, giải mã luôn cho lời giải hợp lệ (ví dụ hoán vị → xếp First-Fit) | Không bao giờ vi phạm; có thể thu hẹp không gian tìm kiếm |

#### 8.4.4 Chọn lọc

Mục đích: chọn cha mẹ, **ưu tiên** cá thể tốt nhưng vẫn cho cá thể kém một cơ hội nhỏ (để giữ đa dạng).

**Bánh xe roulette** (tỉ lệ theo fitness): xác suất chọn cá thể `i` là

```
P_i = f_i / Σ_j f_j
```

Hình dung: chia một bánh xe thành các cung có độ dài tỉ lệ với fitness, quay một lần được một cá thể. Nhược điểm: một cá thể vượt trội có thể chiếm gần hết bánh xe (hội tụ sớm), còn khi fitness của các cá thể gần bằng nhau thì chọn lọc gần như ngẫu nhiên.

**Giải đấu** (tournament): chọn ngẫu nhiên `k` cá thể, lấy cá thể tốt nhất trong nhóm. `k` càng lớn áp lực chọn lọc càng mạnh. Không cần fitness dương, không bị ảnh hưởng bởi thang đo của fitness.

```python
def tournament(pop, fits, k=3):
    idx = random.sample(range(len(pop)), k)
    return pop[max(idx, key=lambda i: fits[i])]
```

**Chọn theo hạng** (rank): xếp hạng cá thể rồi chọn theo xác suất phụ thuộc hạng thay vì giá trị fitness, giảm hiện tượng một cá thể thống trị.

**Elitism:** sao chép thẳng một hoặc vài cá thể tốt nhất sang thế hệ sau. Bảo đảm fitness tốt nhất **không bao giờ giảm** giữa các thế hệ.

**Áp lực chọn lọc** (selection pressure) là khái niệm cần cân bằng: quá mạnh thì quần thể đồng nhất sớm (kẹt cực trị địa phương), quá yếu thì tiến triển chậm, gần với tìm kiếm ngẫu nhiên.

#### 8.4.5 Lai ghép

Trao đổi gen giữa hai cha mẹ để tạo con, **khai thác** các phần tốt đã có.

**Mã hoá nhị phân / vector:**

```
Một điểm cắt (cắt sau vị trí 3):
  Cha:  1 0 1 | 1 0 0          Con 1:  1 0 1 | 1 0 1
  Mẹ:   1 1 0 | 1 0 1    →     Con 2:  1 1 0 | 1 0 0

Hai điểm cắt: hoán đổi đoạn giữa hai điểm cắt.

Đồng nhất (uniform): với mỗi gen, tung đồng xu để quyết định lấy từ cha hay mẹ.
```

**Mã hoá hoán vị:** cắt-ghép thông thường sẽ tạo thành phố bị **lặp** hoặc **thiếu**, nên cần toán tử riêng:

- **OX (Order Crossover):** giữ nguyên một đoạn của cha, các vị trí còn lại điền bằng các phần tử còn thiếu **theo thứ tự xuất hiện trong mẹ**.
- Các toán tử khác: PMX (partially mapped), CX (cycle), ER (edge recombination)...

```
Ví dụ OX (đoạn giữ lại: vị trí 4..6, đếm từ 1; các vị trí trống điền từ trái sang phải)

  Cha:  1 2 3 [4 5 6] 7 8
  Mẹ:   3 7 5  1 6 8  2 4

  Bước 1: copy đoạn của cha          →  _ _ _ 4 5 6 _ _
  Bước 2: lấy mẹ theo thứ tự, bỏ các số đã có (4, 5, 6):  3 7 1 8 2
  Bước 3: điền vào chỗ trống         →  3 7 1 4 5 6 8 2     (là hoán vị hợp lệ)

  Con thứ hai: đổi vai trò cha/mẹ     →  2 3 4 1 6 8 5 7
```

*Chú ý:* bản OX gốc điền các chỗ trống bắt đầu **sau** điểm cắt thứ hai rồi quay vòng. Bản điền từ trái sang phải ở trên đơn giản hơn để cài đặt và vẫn luôn cho hoán vị hợp lệ.

#### 8.4.6 Đột biến

Thay đổi ngẫu nhiên nhỏ trên nhiễm sắc thể, đóng vai trò **khám phá** và **duy trì đa dạng** (khôi phục gen đã mất khỏi quần thể).

| Mã hoá | Toán tử đột biến |
|---|---|
| Nhị phân | **Lật bit:** mỗi bit đổi `0↔1` với xác suất `Pm` |
| Hoán vị | **Hoán đổi** (swap) hai vị trí; **đảo đoạn** (inversion); **chèn** (insertion); **xáo trộn** một đoạn (scramble) |
| Số nguyên / nhãn | Thay gen bằng một giá trị ngẫu nhiên khác trong miền cho phép |
| Số thực | Cộng nhiễu Gauss |

```
Lật bit (vị trí 6):       1 1 0 1 0 0   →   1 1 0 1 0 1
Hoán đổi (vị trí 2 và 5): 1 2 3 4 5 6   →   1 5 3 4 2 6
Đảo đoạn (vị trí 2..5):   1 2 3 4 5 6   →   1 5 4 3 2 6
```

Đột biến quá nhỏ: quần thể mất đa dạng, dễ kẹt. Đột biến quá lớn: GA trở thành tìm kiếm ngẫu nhiên.

#### 8.4.7 Thay thế và điều kiện dừng

- **Thay thế:** thế hệ mới thay hoàn toàn (có thể kèm elitism), hoặc chọn `N` cá thể tốt nhất từ cha mẹ + con, hoặc kiểu steady-state.
- **Điều kiện dừng thông dụng:**
  - Đạt số thế hệ tối đa.
  - Đạt ngưỡng fitness mong muốn.
  - Fitness tốt nhất không cải thiện sau `k` thế hệ liên tiếp.
  - Hết ngân sách (thời gian, số lần đánh giá fitness).

#### 8.4.8 Tham số

| Tham số | Giá trị thường dùng (kinh nghiệm) | Ảnh hưởng |
|---|---|---|
| Kích thước quần thể `N` | Vài chục đến vài trăm | Lớn: đa dạng hơn, mỗi thế hệ tốn hơn |
| Xác suất lai ghép `Pc` | Khoảng 0.6 đến 0.95 | Thấp: con giống cha mẹ, tiến triển chậm |
| Xác suất đột biến `Pm` | Mỗi gen khoảng `1/độ dài` nhiễm sắc thể (hoặc nhỏ hơn) | Cân bằng khám phá/khai thác |
| Kích thước giải đấu `k` | 2 đến 5 | Áp lực chọn lọc |
| Số cá thể elitism | 1 đến vài cá thể | Giữ lời giải tốt nhất |
| Số thế hệ | Tuỳ bài toán và ngân sách | |

Đây là giá trị khởi điểm theo kinh nghiệm, không có bộ tham số tốt nhất cho mọi bài toán. Cần thử nghiệm và chạy **nhiều lần với seed khác nhau** (GA là thuật toán ngẫu nhiên).

### 8.5 Cơ sở lý thuyết

Vì sao GA hoạt động? Holland giải thích bằng khái niệm **lược đồ** (schema) trên chuỗi nhị phân.

**Lược đồ:** mẫu chuỗi dùng ký tự `*` (đúng với `0` hoặc `1`).

```
H = 1 * 0 * * 1      (độ dài L = 6)
   khớp với: 100001, 100011, 100101, 100111, 110001, 110011, 110101, 110111  (8 chuỗi)
```

- **Bậc** `o(H)`: số vị trí đã xác định (không phải `*`). Ở trên `o(H) = 3`.
- **Độ dài định nghĩa** `δ(H)`: khoảng cách giữa vị trí xác định đầu tiên và cuối cùng. Ở trên `δ(H) = 6 − 1 = 5`.

**Định lý lược đồ** (Holland): với chọn lọc tỉ lệ theo fitness, lai ghép một điểm và đột biến lật bit, số cá thể khớp lược đồ `H` kỳ vọng thoả

```
E[ m(H, t+1) ]  ≥  m(H, t) · ( f(H) / f_tb ) · [ 1 − Pc · δ(H)/(L−1) − o(H) · Pm ]
```

với `m(H,t)` là số cá thể khớp `H` ở thế hệ `t`, `f(H)` là fitness trung bình của chúng, `f_tb` là fitness trung bình quần thể.

**Cách hiểu:** lược đồ **ngắn** (δ nhỏ), **bậc thấp** (o nhỏ) và có fitness **trên trung bình** sẽ có số lượng tăng dần qua các thế hệ (xấp xỉ theo cấp số nhân). Lai ghép và đột biến ít khi phá vỡ các lược đồ như vậy.

**Giả thuyết khối xây dựng** (building block hypothesis): GA hoạt động bằng cách tìm và **ghép nối** các khối ngắn, bậc thấp, fitness cao thành lời giải tốt hơn.

*Lưu ý:* định lý lược đồ chỉ là **bất đẳng thức về xu hướng kỳ vọng**, không bảo đảm GA hội tụ về tối ưu toàn cục, và giả thuyết khối xây dựng vẫn có những phê bình trong giới nghiên cứu. Ngoài ra, theo định lý **No Free Lunch**, không có thuật toán tìm kiếm nào tốt nhất cho mọi bài toán, vì vậy việc thiết kế mã hoá và toán tử phù hợp bài toán là quan trọng hơn bản thân khung GA.

**Hai hiện tượng cần theo dõi khi chạy GA:**

| Hiện tượng | Biểu hiện | Hướng khắc phục |
|---|---|---|
| **Hội tụ sớm** (premature convergence) | Quần thể đồng nhất quá sớm, kẹt ở cực trị địa phương | Giảm áp lực chọn lọc, tăng `Pm`, tăng `N` |
| **Tiến triển chậm** | Fitness trung bình gần như không tăng | Tăng áp lực chọn lọc, giảm `Pm`, kiểm tra lại hàm thích nghi |

### 8.6 Các bài toán ứng dụng

Các bài toán dưới đây đều là bài toán **tối ưu tổ hợp**: lời giải là một cách chọn, sắp xếp hoặc phân nhóm các phần tử. Điểm đáng chú ý là mỗi bài toán gợi ý một kiểu **mã hoá** khác nhau.

| Bài toán | Phải quyết định | Mã hoá gợi ý | Hàm thích nghi |
|---|---|---|---|
| Cái túi | Chọn vật nào | Chuỗi bit | Tổng giá trị (phạt nếu quá tải) |
| Đường đi Hamilton | Thứ tự đi qua các đỉnh | Hoán vị đỉnh | Số cạnh hợp lệ liên tiếp |
| Người bán hàng (TSP) | Thứ tự thăm các thành phố | Hoán vị thành phố | `1 / độ dài hành trình` |
| Định vị cơ sở | Mở cơ sở nào | Chuỗi bit (hoặc danh sách `p` chỉ số) | `−(chi phí mở + chi phí phục vụ)` |
| Ghép cặp | Ghép phần tử nào với phần tử nào | Hoán vị (hai phía) hoặc chuỗi bit theo cạnh | Tổng trọng số cặp ghép (phạt nếu cặp trùng đỉnh) |
| Xếp thùng | Vật nào vào thùng nào | Hoán vị + bộ giải mã, hoặc mã hoá nhóm | Ít thùng, mức lấp đầy cao |
| Phân công tổng quát | Tác nhân nào làm việc nào | Vector nhãn | `−(tổng chi phí + phạt vượt dung lượng)` |

#### 8.6.1 Bài toán cái túi (Knapsack)

- **Bài toán (0/1):** có `n` vật, vật `i` nặng `w_i` và giá trị `v_i`; túi chịu tối đa `W`. Chọn tập vật có **tổng giá trị lớn nhất** sao cho tổng khối lượng không vượt `W`.
- **Mã hoá:** chuỗi `n` bit, bit `i = 1` nghĩa là chọn vật `i`.
- **Ràng buộc:** tổng khối lượng `≤ W`. Xử lý bằng phạt, loại bỏ, hoặc sửa chữa (bỏ bớt vật khỏi túi cho đến khi hợp lệ).
- **Toán tử:** lai ghép một điểm/đồng nhất, đột biến lật bit.
- **Lưu ý:** bài toán NP-khó nhưng có thuật toán quy hoạch động `O(n·W)` (giả đa thức); GA hữu ích khi `W` rất lớn hoặc có thêm ràng buộc phức tạp. Chọn làm ví dụ ở mục 8.7.

#### 8.6.2 Bài toán đường đi Hamilton (Hamiltonian path)

- **Bài toán:** cho đồ thị `G = (V, E)`, tìm đường đi qua **mỗi đỉnh đúng một lần**. Đây là bài toán **quyết định** (NP-đầy đủ): đường đi có tồn tại hay không.
- **Mã hoá:** hoán vị của các đỉnh.
- **Hàm thích nghi:** đếm số cặp đỉnh liên tiếp `(π_i, π_{i+1})` là một cạnh của `G`. Đạt `n − 1` nghĩa là hoán vị đó **là** một đường đi Hamilton. Cách này biến bài toán quyết định thành bài toán tối ưu.
- **Toán tử:** OX/PMX, đột biến hoán đổi hoặc đảo đoạn.
- **Lưu ý:** nếu GA không tìm thấy hoán vị đạt `n − 1`, **không** thể kết luận đường đi không tồn tại.

#### 8.6.3 Bài toán người bán hàng (TSP)

- **Bài toán:** thăm `n` thành phố, mỗi thành phố đúng một lần, quay về nơi xuất phát, tổng quãng đường ngắn nhất (xem mục 7.2).
- **Mã hoá:** hoán vị `n` thành phố.
- **Hàm thích nghi:** `f = 1 / L` với `L` là độ dài hành trình.
- **Toán tử:** OX/PMX/ER cho lai ghép; hoán đổi hoặc đảo đoạn cho đột biến (đảo đoạn tương ứng với bước 2-opt trong tìm kiếm cục bộ).
- **Lưu ý:** cùng một hành trình có nhiều biểu diễn (xoay vòng, đảo chiều), nên cố định thành phố đầu hoặc chấp nhận sự dư thừa này. Chọn làm **bài tập** ở mục 8.8.

#### 8.6.4 Bài toán định vị cơ sở (Facility location)

- **Bài toán:** có `m` vị trí ứng viên để đặt cơ sở (kho, trạm...) và tập khách hàng. Chọn vị trí mở cơ sở, gán mỗi khách hàng cho một cơ sở đã mở, sao cho **tổng chi phí** (chi phí mở cơ sở cộng chi phí phục vụ/vận chuyển) nhỏ nhất. Biến thể **p-median** yêu cầu mở đúng `p` cơ sở; biến thể **có giới hạn dung lượng** (capacitated) mỗi cơ sở phục vụ tối đa một lượng nhu cầu.
- **Mã hoá:** chuỗi `m` bit (bit `j = 1` nghĩa là mở cơ sở `j`), hoặc danh sách `p` chỉ số.
- **Bộ giải mã:** với tập cơ sở đã mở, gán mỗi khách hàng cho cơ sở **gần nhất** (khi không có giới hạn dung lượng), rồi tính tổng chi phí.
- **Ràng buộc:** số bit `1` phải bằng `p` (p-median): sửa chữa bằng cách bật/tắt ngẫu nhiên bit cho đủ; với dung lượng thì dùng phạt.

#### 8.6.5 Bài toán ghép cặp (Matching)

- **Bài toán (dạng tổng quát):** cho đồ thị có trọng số, chọn tập cạnh **không chung đỉnh** sao cho tổng trọng số lớn nhất. Trường hợp hai phía `n × n` chính là bài toán phân công (assignment): ghép mỗi phần tử của tập A với đúng một phần tử của tập B.
- **Mã hoá:** hoán vị `π` (hai phía): `π(i) = j` nghĩa là ghép `i` với `j`, luôn hợp lệ; hoặc chuỗi bit theo cạnh (cần xử lý ràng buộc chung đỉnh).
- **Hàm thích nghi:** tổng trọng số các cặp, trừ phạt nếu có đỉnh được ghép hai lần.
- **Lưu ý:** dạng cơ bản này có thuật toán **chính xác đa thức** (Hungarian cho hai phía, Edmonds cho đồ thị tổng quát), nên theo mục 7.9, GA không phải lựa chọn tốt ở đây. GA có ý nghĩa khi bài toán có **thêm ràng buộc** làm mất tính dễ giải (ví dụ ghép ba tập, ràng buộc tương thích phức tạp), hoặc để minh hoạ.

#### 8.6.6 Bài toán xếp thùng (Bin packing)

- **Bài toán:** có `n` vật kích thước `s_i`, thùng sức chứa `C`. Xếp tất cả vật vào **ít thùng nhất**. Cận dưới hiển nhiên: `⌈Σ s_i / C⌉`.
- **Mã hoá:**
  - **Hoán vị + bộ giải mã:** hoán vị xác định thứ tự xếp, giải mã bằng First-Fit (cho mỗi vật vào thùng đầu tiên còn chỗ). Luôn hợp lệ.
  - **Mã hoá nhóm** (grouping GA): nhiễm sắc thể là danh sách các thùng, toán tử thao tác trên **nhóm** thay vì từng vật.
  - **Vector nhãn:** gen `i` là thùng chứa vật `i` (cần xử lý thùng quá tải).
- **Hàm thích nghi:** chỉ dùng "số thùng" thì quá thô (nhiều cá thể bằng nhau). Thường thêm thành phần thưởng cho thùng đầy, ví dụ `Σ (độ đầy thùng / C)² / số thùng`, khuyến khích có thùng gần đầy và thùng gần trống thay vì mọi thùng đầy vừa phải.

#### 8.6.7 Bài toán phân công tổng quát (GAP)

- **Bài toán:** gán `n` công việc cho `m` tác nhân; mỗi công việc **đúng một** tác nhân; gán việc `j` cho tác nhân `i` tốn chi phí `c_ij` và chiếm tài nguyên `r_ij`; tác nhân `i` có dung lượng `b_i`. Cực tiểu tổng chi phí.
- **Mã hoá:** vector độ dài `n`, gen `j ∈ {1..m}` là tác nhân được giao việc `j`. Ràng buộc "mỗi việc đúng một tác nhân" **được bảo đảm sẵn** bởi mã hoá.
- **Ràng buộc còn lại:** `Σ r_ij ≤ b_i` cho mỗi tác nhân: xử lý bằng phạt (`f = −(tổng chi phí + λ · tổng vượt dung lượng)`) hoặc sửa chữa (chuyển việc từ tác nhân quá tải sang tác nhân còn chỗ).
- **Toán tử:** lai ghép đồng nhất; đột biến thay tác nhân của một việc bằng tác nhân khác.

### 8.7 Ví dụ minh hoạ: giải bài toán cái túi bằng GA

Phần này đi **song song** giữa khái niệm, số liệu tính tay và code Python. Các đoạn code ở mục này ghép lại thành một chương trình hoàn chỉnh.

#### 8.7.1 Bài toán

Có 6 vật, túi chịu tối đa `W = 15`:

| Vật | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Khối lượng `w` | 5 | 4 | 6 | 3 | 7 | 2 |
| Giá trị `v` | 10 | 40 | 30 | 50 | 35 | 25 |

Chỉ có `2⁶ = 64` tổ hợp nên có thể kiểm tra hết để biết đáp án: **tối ưu là chọn vật 2, 3, 4, 6** (nặng `4+6+3+2 = 15`, giá trị `40+30+50+25 = 145`). Bài toán nhỏ là chủ ý, để so được kết quả GA với đáp án đúng. Với `n` lớn, vét cạn không còn khả thi.

```python
import random

WEIGHTS = [5, 4, 6, 3, 7, 2]
VALUES = [10, 40, 30, 50, 35, 25]
CAPACITY = 15
N = len(WEIGHTS)

POP_SIZE = 20
GENERATIONS = 30
P_CROSSOVER = 0.8
P_MUTATION = 0.05  # xác suất đột biến cho MỖI gen
ELITE = 1
```

#### 8.7.2 Bước 1: mã hoá

Nhiễm sắc thể là chuỗi 6 bit, bit `i = 1` nghĩa là bỏ vật `i` vào túi.

```
110101  →  chọn vật 1, 2, 4, 6
           khối lượng = 5 + 4 + 3 + 2  = 14   (≤ 15, hợp lệ)
           giá trị    = 10 + 40 + 50 + 25 = 125
```

#### 8.7.3 Bước 2: hàm thích nghi

Giá trị tổng nếu không vượt tải, ngược lại bằng 0 (cách "loại bỏ" ở mục 8.4.3).

```python
def fitness(chrom):
    weight = sum(c * w for c, w in zip(chrom, WEIGHTS))
    value = sum(c * v for c, v in zip(chrom, VALUES))
    return value if weight <= CAPACITY else 0
```

Tính tay cho một quần thể mẫu gồm 4 cá thể:

| Cá thể | Nhiễm sắc thể | Vật được chọn | Khối lượng | Giá trị | Fitness |
|---|---|---|---|---|---|
| A | `101100` | 1, 3, 4 | 14 | 90 | **90** |
| B | `011010` | 2, 3, 5 | 17 (> 15) | 105 | **0** |
| C | `110101` | 1, 2, 4, 6 | 14 | 125 | **125** |
| D | `010101` | 2, 4, 6 | 9 | 115 | **115** |

Cá thể B có giá trị cao nhưng vượt tải nên bị loại (fitness 0).

#### 8.7.4 Bước 3: khởi tạo quần thể

Mỗi gen là bit ngẫu nhiên. (Bản mẫu dùng 20 cá thể; ví dụ tính tay ở đây dùng 4 cho gọn.)

```python
def init_population():
    return [[random.randint(0, 1) for _ in range(N)] for _ in range(POP_SIZE)]
```

#### 8.7.5 Bước 4: chọn lọc (roulette)

Tổng fitness của quần thể mẫu: `90 + 0 + 125 + 115 = 330`.

| Cá thể | Fitness | Xác suất `P = f / 330` | Cung trên bánh xe |
|---|---|---|---|
| A | 90 | 0.273 | `[0, 90)` |
| B | 0 | 0.000 | (rỗng) |
| C | 125 | 0.379 | `[90, 215)` |
| D | 115 | 0.348 | `[215, 330]` |

Quay số `r` trong `[0, 330]`: ví dụ `r = 150` rơi vào cung của C, `r = 250` rơi vào cung của D. Cá thể B không bao giờ được chọn.

```python
def roulette(pop, fits):
    total = sum(fits)
    if total == 0:
        return random.choice(pop)
    r = random.uniform(0, total)
    acc = 0
    for chrom, f in zip(pop, fits):
        acc += f
        if acc >= r:
            return chrom
    return pop[-1]
```

Dòng `if total == 0` phòng trường hợp mọi cá thể đều vượt tải. (Có thể thay bằng giải đấu ở mục 8.4.4.)

#### 8.7.6 Bước 5: lai ghép một điểm

Giả sử chọn được cha mẹ A và C, điểm cắt sau vị trí 3:

```
  A:  1 0 1 | 1 0 0          Con 1:  1 0 1 | 1 0 1   = 101101
  C:  1 1 0 | 1 0 1    →     Con 2:  1 1 0 | 1 0 0   = 110100
```

Đánh giá hai con:

- Con 1 `101101`: chọn vật 1, 3, 4, 6, nặng `5+6+3+2 = 16 > 15`, vượt tải nên fitness `0`.
- Con 2 `110100`: chọn vật 1, 2, 4, nặng `12`, giá trị `100`, fitness `100`.

Lai ghép **không** bảo đảm con tốt hơn cha mẹ, có thể sinh cá thể vi phạm ràng buộc. GA dựa vào việc sinh nhiều con và chọn lọc giữ lại những con tốt.

```python
def crossover(p1, p2):
    if random.random() < P_CROSSOVER:
        cut = random.randint(1, N - 1)
        return p1[:cut] + p2[cut:], p2[:cut] + p1[cut:]
    return p1[:], p2[:]
```

#### 8.7.7 Bước 6: đột biến

Lật mỗi bit với xác suất nhỏ. Ví dụ lật bit thứ 6 của Con 2:

```
110100  →  110101      fitness từ 100 tăng lên 125
```

Đột biến có thể giúp (như trên) hoặc làm hại (lật bit thứ 3 cho `111100`, nặng 18, vượt tải). Chọn lọc ở các thế hệ sau sẽ loại bỏ các đột biến có hại.

```python
def mutate(chrom):
    return [1 - g if random.random() < P_MUTATION else g for g in chrom]
```

#### 8.7.8 Bước 7: ghép thành vòng lặp tiến hoá

Mỗi thế hệ: giữ `ELITE` cá thể tốt nhất, rồi lặp chọn lọc, lai ghép, đột biến cho đến khi đủ `POP_SIZE` cá thể.

```python
def run(seed=None, verbose=False):
    if seed is not None:
        random.seed(seed)
    pop = init_population()
    best = max(pop, key=fitness)
    for gen in range(GENERATIONS + 1):
        fits = [fitness(c) for c in pop]
        gen_best = max(pop, key=fitness)
        if fitness(gen_best) > fitness(best):
            best = gen_best
        if verbose:
            print(f"gen {gen:2d} best={max(fits):3d} avg={sum(fits) / len(fits):6.1f}")
        # thế hệ mới
        ranked = sorted(pop, key=fitness, reverse=True)
        new_pop = [c[:] for c in ranked[:ELITE]]
        while len(new_pop) < POP_SIZE:
            p1, p2 = roulette(pop, fits), roulette(pop, fits)
            c1, c2 = crossover(p1, p2)
            new_pop += [mutate(c1), mutate(c2)]
        pop = new_pop[:POP_SIZE]
    return best, fitness(best)


if __name__ == "__main__":
    best, f = run(seed=42, verbose=True)
    print("best:", best, "fitness:", f)
    hits = sum(run(seed=s)[1] == 145 for s in range(100))
    print("hit optimum in", hits, "/ 100 runs")
```

#### 8.7.9 Kết quả và nhận xét

Chạy với `seed=42` (trích):

```
gen  0 best=125 avg=  34.0
gen  1 best=125 avg=  50.5
gen  2 best=145 avg=  62.2
...
gen 10 best=145 avg= 129.8
...
gen 30 best=145 avg= 102.2
best: [0, 1, 1, 1, 0, 1] fitness: 145
```

Chạy 100 lần với `seed` từ 0 đến 99: **97/100 lần** tìm được đáp án tối ưu 145.

**Quan sát:**

- **Fitness tốt nhất** đạt 145 từ thế hệ 2 và không giảm nữa nhờ **elitism**.
- **Fitness trung bình** tăng mạnh (từ 34.0 ở thế hệ 0 lên khoảng 100 đến 136 ở các thế hệ sau) nhưng **dao động** chứ không tăng đều: lai ghép và đột biến liên tục sinh ra con vượt tải (fitness 0) kéo trung bình xuống.
- Còn 3/100 lần không tìm ra tối ưu: GA **không bảo đảm** tối ưu. Kết quả cụ thể phụ thuộc `seed`, nên cần chạy nhiều lần mới đánh giá được thuật toán.

**Thử thay đổi để thấy ảnh hưởng của từng thành phần:**

| Thử | Quan sát cần kiểm tra |
|---|---|
| `P_MUTATION = 0` | Quần thể có kẹt không? Tỉ lệ chạm tối ưu thay đổi ra sao? |
| `ELITE = 0` | Fitness tốt nhất có còn không giảm giữa các thế hệ? |
| Thay roulette bằng `tournament` | Tốc độ hội tụ và tỉ lệ chạm tối ưu |
| Thay "fitness 0" bằng phạt `giá trị − λ · phần vượt tải` | Có giảm số cá thể "chết" không? Cần chỉnh `λ` thế nào? |
| Tăng lên 30 vật ngẫu nhiên | Vét cạn `2³⁰` đã rất chậm; GA còn hiệu quả không? |

### 8.8 Tổng kết

| Nội dung | Ý chính |
|---|---|
| **Bản chất GA** | Tìm kiếm trên quần thể bằng chọn lọc, lai ghép, đột biến |
| **Việc cần thiết kế** | Mã hoá, hàm thích nghi, chọn lọc, toán tử, tham số |
| **Mã hoá theo bài toán** | Bit (cái túi, định vị), hoán vị (TSP, Hamilton), nhãn (phân công), nhóm (xếp thùng) |
| **Ràng buộc** | Loại bỏ, phạt, sửa chữa, bộ giải mã |
| **Lý thuyết** | Định lý lược đồ mô tả xu hướng, không bảo đảm tối ưu |
| **Thực hành** | GA ngẫu nhiên: chạy nhiều `seed`, theo dõi hội tụ sớm và đa dạng quần thể |
| **Khi nào dùng** | Không gian tìm kiếm lớn, hàm mục tiêu phức tạp; ít hợp khi đã có thuật toán chính xác hiệu quả |