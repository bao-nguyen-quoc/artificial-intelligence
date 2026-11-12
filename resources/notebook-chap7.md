# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 7: Tính toán tiến hoá

### Mục lục

- [7.1 Khái niệm](#71-khái-niệm)
- [7.2 Bài toán tối ưu và vì sao cần tính toán tiến hoá](#72-bài-toán-tối-ưu-và-vì-sao-cần-tính-toán-tiến-hoá)
- [7.3 Khung chung của thuật toán tiến hoá](#73-khung-chung-của-thuật-toán-tiến-hoá)
- [7.4 Phân loại các kỹ thuật tính toán tiến hoá](#74-phân-loại-các-kỹ-thuật-tính-toán-tiến-hoá)
- [7.5 Thuật toán tiến hoá](#75-thuật-toán-tiến-hoá)
  - [7.5.1 Thuật toán di truyền](#751-thuật-toán-di-truyền-genetic-algorithm---ga)
  - [7.5.2 Lập trình tiến hoá](#752-lập-trình-tiến-hoá-evolutionary-programming---ep)
  - [7.5.3 Chiến lược tiến hoá](#753-chiến-lược-tiến-hoá-evolution-strategies---es)
  - [7.5.4 Lập trình di truyền](#754-lập-trình-di-truyền-genetic-programming---gp)
- [7.6 Trí tuệ bầy đàn](#76-trí-tuệ-bầy-đàn-swarm-intelligence)
  - [7.6.1 Thuật toán đàn kiến](#761-thuật-toán-đàn-kiến-ant-colony-optimization---aco)
  - [7.6.2 Tối ưu bầy đàn](#762-tối-ưu-bầy-đàn-particle-swarm-optimization---pso)
  - [7.6.3 Thuật toán đàn ong](#763-thuật-toán-đàn-ong-bees-algorithm)
- [7.7 Các kỹ thuật khác](#77-các-kỹ-thuật-khác)
- [7.8 Ứng dụng](#78-ứng-dụng)
- [7.9 Ưu nhược điểm và khi nào dùng](#79-ưu-nhược-điểm-và-khi-nào-dùng)
- [7.10 Hướng tiếp theo: thuật toán di truyền](#710-hướng-tiếp-theo-thuật-toán-di-truyền)

**Vấn đề:** Nhiều bài toán thực tế có không gian lời giải khổng lồ, không thể duyệt hết và cũng khó giải bằng phương pháp giải tích. Trong khi đó, tự nhiên đã "giải" những bài toán thích nghi cực kỳ phức tạp qua hàng tỷ năm tiến hoá.
**Mục tiêu:** Nắm bức tranh tổng quan của tính toán tiến hoá: ý tưởng chung, các nhóm kỹ thuật chính và vị trí của thuật toán di truyền trong đó.

### 7.1 Khái niệm

> **Tính toán tiến hoá** (Evolutionary Computation - EC) là một lĩnh vực của trí tuệ nhân tạo, gồm các thuật toán tối ưu **lấy cảm hứng từ cơ chế tiến hoá của sinh vật**, dùng để giải các bài toán tối ưu, đặc biệt là **tối ưu tổ hợp**.

Điểm chung của các kỹ thuật này:

- Làm việc với **một tập (quần thể)** lời giải cùng lúc, không chỉ một lời giải.
- Cải thiện dần chất lượng qua **nhiều thế hệ** bằng cơ chế **chọn lọc** và **biến đổi**.
- Dựa trên **ngẫu nhiên có định hướng**, không cần đạo hàm hay tri thức sâu về cấu trúc bài toán.

| Cơ chế tự nhiên | Ánh xạ sang tính toán |
|---|---|
| Cá thể | Một lời giải ứng viên |
| Quần thể | Tập các lời giải ứng viên |
| Độ thích nghi (fitness) | Giá trị hàm mục tiêu của lời giải |
| Chọn lọc tự nhiên | Ưu tiên giữ lại lời giải tốt |
| Lai ghép, đột biến | Toán tử sinh lời giải mới từ lời giải cũ |
| Thế hệ | Một vòng lặp của thuật toán |

*Chú ý:* tính toán tiến hoá là **nhóm phương pháp** thuộc về *metaheuristic*, không phải một thuật toán cụ thể. Nó nằm cạnh các hướng khác như học máy, suy luận logic (chương 1) hay biểu diễn tri thức (chương 6).

### 7.2 Bài toán tối ưu và vì sao cần tính toán tiến hoá

**Bài toán tối ưu:** tìm lời giải `x*` trong không gian tìm kiếm `S` sao cho hàm mục tiêu `f` đạt cực trị:

```
x* = argmax f(x),   x ∈ S        (hoặc argmin)
```

**Tối ưu tổ hợp:** `S` là tập rời rạc hữu hạn nhưng rất lớn, lời giải là một cách sắp xếp/chọn lựa các thành phần.

*Ví dụ - bài toán người du lịch (TSP):* đi qua `n` thành phố, mỗi thành phố đúng một lần, quay về điểm xuất phát, tổng quãng đường ngắn nhất. Số hành trình khác nhau là `(n-1)!/2`:

| n | Số hành trình (xấp xỉ) |
|---|---|
| 10 | 181 440 |
| 20 | 6.1 × 10¹⁶ |
| 50 | 3 × 10⁶² |

Duyệt toàn bộ (vét cạn) là bất khả thi: đây là hiện tượng **bùng nổ tổ hợp**. Ở các chương trước, ta đã gặp các phương pháp tìm kiếm (BFS, DFS, A*) cũng đối mặt với vấn đề này khi không gian trạng thái quá lớn.

**Hướng của tính toán tiến hoá:** không đảm bảo tìm ra lời giải **tối ưu tuyệt đối**, nhưng tìm được lời giải **đủ tốt** trong thời gian chấp nhận được.

### 7.3 Khung chung của thuật toán tiến hoá

```
1. Khởi tạo quần thể P(0) gồm N cá thể (thường ngẫu nhiên)
2. Đánh giá độ thích nghi f của từng cá thể trong P(0)
3. t = 0
4. Lặp cho đến khi thoả điều kiện dừng:
     a. Chọn lọc:   chọn các cá thể "cha mẹ" từ P(t), ưu tiên cá thể có f tốt
     b. Biến đổi:   lai ghép + đột biến trên cha mẹ để sinh cá thể con
     c. Đánh giá:   tính f cho cá thể con
     d. Thay thế:   chọn N cá thể từ cha mẹ + con để tạo P(t+1)
     e. t = t + 1
5. Trả về cá thể tốt nhất tìm được
```

| Thành phần | Vai trò | Lưu ý khi thiết kế |
|---|---|---|
| **Biểu diễn** (encoding) | Mã hoá lời giải thành cá thể | Quyết định không gian tìm kiếm và toán tử dùng được |
| **Hàm thích nghi** | Đo chất lượng lời giải | Thường chính là hàm mục tiêu |
| **Chọn lọc** | Tạo áp lực hướng đến lời giải tốt | Quá mạnh thì hội tụ sớm, quá yếu thì tìm kiếm lan man |
| **Toán tử biến đổi** | Sinh lời giải mới | Lai ghép khai thác, đột biến khám phá |
| **Điều kiện dừng** | Quyết định khi nào kết thúc | Số thế hệ tối đa, đạt ngưỡng fitness, không cải thiện sau k thế hệ |

*Nguyên tắc cân bằng:* **khám phá** (exploration: tìm vùng mới) và **khai thác** (exploitation: tinh chỉnh quanh lời giải tốt). Đây là vấn đề trung tâm của mọi thuật toán trong chương này.

### 7.4 Phân loại các kỹ thuật tính toán tiến hoá

| Nhóm | Kỹ thuật | Cảm hứng |
|---|---|---|
| **Thuật toán tiến hoá** | Thuật toán di truyền (GA) | Di truyền học, chọn lọc tự nhiên |
| | Lập trình tiến hoá (EP) | Tiến hoá của hành vi |
| | Chiến lược tiến hoá (ES) | Tiến hoá, tối ưu tham số thực |
| | Lập trình di truyền (GP) | Tiến hoá của chương trình |
| **Trí tuệ bầy đàn** (Swarm Intelligence) | Thuật toán đàn kiến (ACO) | Đàn kiến tìm đường |
| | Tối ưu bầy đàn (PSO) | Đàn chim, đàn cá |
| | Thuật toán đàn ong (Bees algorithm) | Đàn ong tìm mật |
| **Các kỹ thuật khác** | Bản đồ tự tổ chức (SOM) | Vỏ não, mạng nơ-ron |
| | Sự sống nhân tạo (Artificial Life) | Hệ sinh học mô phỏng |
| | Hệ miễn dịch nhân tạo (AIS) | Hệ miễn dịch |
| | Mô hình tiến hoá khả học (LEM) | Tiến hoá có học máy dẫn dắt |

*Chú ý:* ranh giới giữa các nhóm không tuyệt đối. Thuật toán tiến hoá mô phỏng **quá trình tiến hoá qua thế hệ** (chọn lọc, lai ghép, đột biến). Trí tuệ bầy đàn mô phỏng **hành vi tập thể** của các cá thể đơn giản tương tác với nhau và với môi trường.

### 7.5 Thuật toán tiến hoá

#### 7.5.1 Thuật toán di truyền (Genetic Algorithm - GA)

- Đề xuất bởi **John Holland** (thập niên 1970).
- Cá thể là **nhiễm sắc thể** thường mã hoá bằng chuỗi bit, số nguyên hoặc hoán vị.
- Dùng đủ 3 toán tử: **chọn lọc**, **lai ghép** (crossover), **đột biến** (mutation). Lai ghép là toán tử chủ đạo.
- Là đại diện tiêu biểu nhất của tính toán tiến hoá, sẽ được trình bày chi tiết ở chương sau.

```
Cha:  1 0 1 1 | 0 0 1        Lai ghép 1 điểm cắt
Mẹ:   0 1 0 0 | 1 1 0   →   Con 1:  1 0 1 1 1 1 0
                             Con 2:  0 1 0 0 0 0 1
```

#### 7.5.2 Lập trình tiến hoá (Evolutionary Programming - EP)

- Đề xuất bởi **Lawrence Fogel** (thập niên 1960), ban đầu tiến hoá các **máy trạng thái hữu hạn** để dự đoán chuỗi ký hiệu.
- Tập trung vào **hành vi** của cá thể, không mô phỏng di truyền.
- **Không dùng lai ghép**, chỉ dùng **đột biến**; mỗi cha mẹ sinh con bằng đột biến, sau đó chọn lọc.

#### 7.5.3 Chiến lược tiến hoá (Evolution Strategies - ES)

- Đề xuất bởi **Ingo Rechenberg** và **Hans-Paul Schwefel** (Đức, thập niên 1960).
- Cá thể là **vector số thực**, phù hợp tối ưu tham số liên tục.
- Đột biến theo phân phối Gauss, và **bước đột biến được tiến hoá cùng cá thể** (tự thích nghi).
- Hai kiểu thay thế kinh điển:

| Ký hiệu | Ý nghĩa |
|---|---|
| `(μ + λ)` | μ cha mẹ sinh λ con, chọn μ cá thể tốt nhất từ **cả cha mẹ và con** |
| `(μ, λ)` | Chỉ chọn μ cá thể tốt nhất từ **tập con** (cha mẹ bị loại) |

#### 7.5.4 Lập trình di truyền (Genetic Programming - GP)

- Phổ biến bởi **John Koza** (1992).
- Cá thể không phải chuỗi giá trị mà là **chương trình**, thường biểu diễn bằng **cây cú pháp** (nút trong là hàm/toán tử, lá là biến/hằng).
- Lai ghép bằng cách **hoán đổi cây con** giữa hai chương trình; đột biến thay một cây con bằng cây con sinh ngẫu nhiên.
- Ứng dụng: hồi quy biểu tượng (tìm công thức khớp dữ liệu), thiết kế mạch, sinh luật.

```
Cây biểu diễn  (x + 3) * y

        *
       / \
      +   y
     / \
    x   3
```

| | GA | EP | ES | GP |
|---|---|---|---|---|
| **Biểu diễn** | Chuỗi bit / số / hoán vị | Tuỳ bài toán (ban đầu: máy trạng thái) | Vector số thực | Cây chương trình |
| **Lai ghép** | Có (chủ đạo) | Không | Có thể có | Có (hoán đổi cây con) |
| **Đột biến** | Có (thứ yếu) | Có (chủ đạo) | Có (chủ đạo, tự thích nghi) | Có |
| **Thường dùng cho** | Tối ưu tổ hợp, tổng quát | Dự đoán, điều khiển | Tối ưu tham số liên tục | Sinh chương trình, công thức |

### 7.6 Trí tuệ bầy đàn (Swarm Intelligence)

> Hành vi thông minh **xuất hiện (emergent)** từ sự tương tác của nhiều cá thể đơn giản, mỗi cá thể chỉ tuân theo luật cục bộ và không có bộ điều khiển trung tâm.

#### 7.6.1 Thuật toán đàn kiến (Ant Colony Optimization - ACO)

- Đề xuất bởi **Marco Dorigo** (1992), cho bài toán tìm đường đi ngắn nhất (điển hình là TSP).
- Cảm hứng: kiến để lại **pheromone** trên đường đi; đường ngắn được đi nhiều lần hơn nên pheromone dày hơn, thu hút thêm kiến (phản hồi dương). Pheromone **bay hơi** theo thời gian nên đường kém dần bị bỏ.

```
Xác suất kiến ở đỉnh i chọn đi đến đỉnh j:
   p(i,j) = [τ(i,j)]^α · [η(i,j)]^β / Σ_k [τ(i,k)]^α · [η(i,k)]^β

Cập nhật pheromone:
   τ(i,j) ← (1 − ρ) · τ(i,j) + Σ_kiến Δτ_k(i,j)
```

| Ký hiệu | Ý nghĩa |
|---|---|
| `τ` | Lượng pheromone trên cạnh (i,j) |
| `η` | Thông tin heuristic, ví dụ `1/khoảng cách` |
| `α, β` | Trọng số của pheromone và heuristic |
| `ρ` | Tốc độ bay hơi |
| `Δτ_k` | Pheromone kiến k để lại, tỉ lệ nghịch với độ dài hành trình |

#### 7.6.2 Tối ưu bầy đàn (Particle Swarm Optimization - PSO)

- Đề xuất bởi **Kennedy và Eberhart** (1995), mô phỏng đàn chim/cá tìm thức ăn.
- Mỗi **hạt** có vị trí `x` và vận tốc `v` trong không gian tìm kiếm. Mỗi hạt nhớ vị trí tốt nhất của bản thân (`pbest`) và biết vị trí tốt nhất của cả bầy (`gbest`).
- Phù hợp tối ưu hàm **liên tục**.

```
v ← w·v + c1·r1·(pbest − x) + c2·r2·(gbest − x)
x ← x + v
```

| Ký hiệu | Ý nghĩa |
|---|---|
| `w` | Hệ số quán tính (giữ hướng đang đi) |
| `c1` | Hệ số nhận thức (kéo về kinh nghiệm bản thân) |
| `c2` | Hệ số xã hội (kéo về kinh nghiệm của bầy) |
| `r1, r2` | Số ngẫu nhiên trong [0,1] |

*So với GA:* PSO không có lai ghép hay chọn lọc, mà các hạt **cùng tồn tại** và học lẫn nhau qua `gbest`.

#### 7.6.3 Thuật toán đàn ong (Bees algorithm)

- Đề xuất bởi **Pham và cộng sự** (2005), mô phỏng cách ong mật đi tìm nguồn hoa.
- Ong trinh sát tìm ngẫu nhiên các vùng; vùng nào có "chất lượng hoa" tốt thì được **huy động thêm ong** đến khai thác kỹ hơn ở lân cận, các vùng kém được bỏ.
- Kết hợp **tìm kiếm toàn cục** (trinh sát ngẫu nhiên) và **tìm kiếm cục bộ** (khai thác lân cận vùng tốt).

| | ACO | PSO | Bees |
|---|---|---|---|
| **Giao tiếp** | Gián tiếp qua pheromone | Chia sẻ `gbest` | Huy động theo chất lượng vùng |
| **Không gian** | Rời rạc, đồ thị | Liên tục | Liên tục và rời rạc |
| **Ứng dụng điển hình** | TSP, định tuyến | Tối ưu hàm, huấn luyện mạng | Tối ưu hàm, lập lịch |

### 7.7 Các kỹ thuật khác

Các kỹ thuật này có chung tinh thần "học từ sinh học" nhưng không hoàn toàn theo khung tiến hoá ở mục 7.3.

| Kỹ thuật | Ý tưởng chính |
|---|---|
| **Bản đồ tự tổ chức** (Self-organizing map - SOM, Kohonen) | Mạng nơ-ron học **không giám sát**, ánh xạ dữ liệu nhiều chiều lên lưới 2 chiều sao cho dữ liệu gần nhau trong không gian gốc nằm gần nhau trên lưới. Học bằng cạnh tranh: nơ-ron thắng và các nơ-ron lân cận được điều chỉnh về phía mẫu. |
| **Sự sống nhân tạo** (Artificial Life) | Mô phỏng các hệ có đặc tính của sự sống (sinh sản, thích nghi, tiến hoá) trong máy tính để nghiên cứu hiện tượng sinh học. Ví dụ: *Game of Life* của Conway, các hệ như Tierra, Avida. |
| **Hệ miễn dịch nhân tạo** (Artificial Immune System - AIS) | Mô phỏng hệ miễn dịch: *chọn lọc âm* (loại bỏ bộ phát hiện khớp với dữ liệu "bình thường" để nhận ra bất thường), *chọn lọc vô tính* (nhân bản và đột biến các kháng thể khớp tốt). Dùng cho phát hiện bất thường, an ninh mạng. |
| **Mô hình tiến hoá khả học** (Learnable Evolution Model - LEM, Michalski) | Thay vì chỉ dựa vào toán tử ngẫu nhiên, dùng **học máy** trên nhóm cá thể tốt và xấu để rút ra quy tắc mô tả vùng tốt, rồi dùng quy tắc đó **dẫn dắt** việc sinh cá thể mới. |

### 7.8 Ứng dụng

| Lĩnh vực | Ví dụ |
|---|---|
| Tối ưu tổ hợp | TSP, định tuyến xe, lập lịch sản xuất, lập thời khoá biểu, bài toán cái túi |
| Tối ưu tham số | Chỉnh siêu tham số mô hình học máy, thiết kế kỹ thuật (hình dạng cánh, anten) |
| Học máy | Chọn đặc trưng, huấn luyện/tiến hoá cấu trúc mạng nơ-ron |
| Thiết kế tự động | Sinh chương trình, mạch điện (GP), thiết kế hệ thống |
| Mạng và an ninh | Định tuyến mạng, phát hiện xâm nhập (AIS) |
| Trò chơi và robot | Tiến hoá chiến lược chơi, bộ điều khiển robot |
| Phân tích dữ liệu | Phân cụm, trực quan hoá dữ liệu nhiều chiều (SOM) |

### 7.9 Ưu nhược điểm và khi nào dùng

| Ưu điểm | Nhược điểm |
|---|---|
| Không cần đạo hàm, hàm mục tiêu có thể không liên tục, nhiễu | **Không đảm bảo** tìm được tối ưu toàn cục |
| Tìm kiếm song song trên cả quần thể, ít kẹt cực trị địa phương hơn leo đồi đơn giản | Tốn nhiều lần đánh giá hàm thích nghi |
| Linh hoạt, áp dụng cho nhiều loại bài toán | Nhiều tham số cần chỉnh (kích thước quần thể, xác suất lai ghép/đột biến, ...) |
| Dễ cài đặt, dễ kết hợp tri thức riêng của bài toán | Kết quả mang tính ngẫu nhiên, cần chạy nhiều lần để đánh giá |

**Nên dùng khi:** không gian tìm kiếm lớn, hàm mục tiêu phức tạp hoặc "hộp đen", chấp nhận lời giải gần tối ưu.
**Không nên dùng khi:** bài toán có thuật toán chính xác hiệu quả (ví dụ quy hoạch tuyến tính) hoặc đòi hỏi bảo đảm tối ưu tuyệt đối.

### 7.10 Hướng tiếp theo: thuật toán di truyền

Trong các kỹ thuật ở trên, **thuật toán di truyền** là đại diện tiêu biểu nhất:

- Khung của GA chính là khung chung ở mục 7.3, với đầy đủ chọn lọc, lai ghép và đột biến.
- Nhiều khái niệm của các kỹ thuật khác (quần thể, fitness, đột biến, thế hệ) đều được trình bày rõ nhất qua GA.

Chương tiếp theo sẽ đi sâu vào: mã hoá nhiễm sắc thể, các phương pháp chọn lọc (bánh xe roulette, giải đấu, ...), các toán tử lai ghép/đột biến và ví dụ giải bài toán cụ thể.