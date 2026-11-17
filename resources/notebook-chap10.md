# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 10: Phân cụm K-means (K-means clustering)

### Mục lục

- [Artificial Intelligence Notebook](#artificial-intelligence-notebook)
  - [Chapter 10: Phân cụm K-means (K-means clustering)](#chapter-10-phân-cụm-k-means-k-means-clustering)
    - [Mục lục](#mục-lục)
    - [10.1 Khái niệm](#101-khái-niệm)
      - [10.1.1 Phân cụm là gì](#1011-phân-cụm-là-gì)
      - [10.1.2 Phân cụm khác phân loại](#1012-phân-cụm-khác-phân-loại)
      - [10.1.3 Các họ thuật toán phân cụm](#1013-các-họ-thuật-toán-phân-cụm)
    - [10.2 Hàm mục tiêu J](#102-hàm-mục-tiêu-j)
    - [10.3 Thuật toán K-means Clustering](#103-thuật-toán-k-means-clustering)
      - [10.3.1 Các bước](#1031-các-bước)
      - [10.3.2 Vì sao thuật toán dừng](#1032-vì-sao-thuật-toán-dừng)
      - [10.3.3 Độ phức tạp](#1033-độ-phức-tạp)
    - [10.4 Ví dụ tính tay](#104-ví-dụ-tính-tay)
    - [10.5 Các vấn đề thực tế](#105-các-vấn-đề-thực-tế)
      - [10.5.1 Khởi tạo tâm cụm](#1051-khởi-tạo-tâm-cụm)
      - [10.5.2 Chọn số cụm K](#1052-chọn-số-cụm-k)
      - [10.5.3 Chuẩn hoá đặc trưng](#1053-chuẩn-hoá-đặc-trưng)
      - [10.5.4 Ngoại lệ, cụm rỗng và hình dạng cụm](#1054-ngoại-lệ-cụm-rỗng-và-hình-dạng-cụm)
      - [10.5.5 Các biến thể và thuật toán thay thế](#1055-các-biến-thể-và-thuật-toán-thay-thế)
    - [10.6 Các ứng dụng](#106-các-ứng-dụng)
    - [10.7 Tổng kết](#107-tổng-kết)
    - [10.8 Từ khoá để tự tìm hiểu thêm](#108-từ-khoá-để-tự-tìm-hiểu-thêm)

**Vấn đề:** Các phương pháp ở chương 9 học từ **ví dụ đã có nhãn** (email đã đánh dấu spam, ảnh đã biết là chó hay mèo). Nhưng hồ sơ khách hàng, tập văn bản hay các điểm ảnh thường **không có nhãn nào**, và ta muốn máy **tự tìm ra cấu trúc** của dữ liệu: những nhóm đối tượng giống nhau.

**Mục tiêu:** Định nghĩa được phân cụm và đặt nó vào bản đồ các loại học; phát biểu và **tính tay** được thuật toán K-means; giải thích hàm mục tiêu `J` và vì sao thuật toán luôn dừng; biết cách chọn `K`, khởi tạo tâm và chuẩn hoá đặc trưng.

### 10.1 Khái niệm

#### 10.1.1 Phân cụm là gì

> **Phân cụm** (Clustering, cluster analysis) là bài toán **chia một tập đối tượng thành các nhóm (cụm, cluster)** sao cho các đối tượng **trong cùng một cụm giống nhau nhiều** và các đối tượng **ở hai cụm khác nhau khác nhau nhiều**. Mức độ "giống nhau" thường được đo bằng **khoảng cách** giữa các vector đặc trưng.

Đây là bài toán điển hình của **học không giám sát** (mục 9.3.2): dữ liệu chỉ có các vector đặc trưng `x`, **không có nhãn** `y`, nên thuật toán không biết "đáp án đúng" mà phải tự tìm cấu trúc ẩn.

**K-means** (K-trung bình) là thuật toán phân cụm đơn giản và phổ biến nhất. Theo bài giảng, nó chia các đối tượng thành `K` phần dựa trên thuộc tính của chúng, với ba đặc điểm:

- Các thuộc tính của đối tượng tạo thành một **không gian vector** (có thể tính **trung bình** của một nhóm điểm).
- Mục tiêu là **cực tiểu hoá tổng phương sai trong cụm** (hàm `J`, mục 10.2).
- Số cụm `K` là **siêu tham số do người dùng chọn trước** (mục 9.2.1).

#### 10.1.2 Phân cụm khác phân loại

Phân cụm và phân loại (k-NN ở mục 9.5) cùng gán mỗi mẫu vào một nhóm, nhưng khác nhau ở chỗ nhóm đó từ đâu ra:

| | Phân loại (k-NN, mục 9.5) | Phân cụm (K-means) |
|---|---|---|
| Loại học | **Có giám sát** | **Không giám sát** |
| Dữ liệu huấn luyện | Cặp `(x, y)`, có nhãn | Chỉ có `x` |
| Các nhóm | **Đã biết trước** (do con người đặt tên) | **Do thuật toán tìm ra**, chỉ là số thứ tự 0, 1, 2... |
| Đánh giá | So dự đoán với nhãn thật (accuracy, F1...) | Không có đáp án: dùng `J`, silhouette hoặc đánh giá theo mục đích sử dụng |
| Siêu tham số chính | `k` láng giềng | `K` cụm |

*Chú ý:* hai chữ "k" **không liên quan**: `k` trong k-NN là số láng giềng được bỏ phiếu, còn `K` trong K-means là **số cụm** cần tìm. Hai thuật toán chỉ có chung ý tưởng "gần nhau thì giống nhau" và đều dựa trên khoảng cách Euclid, nên đều **cần chuẩn hoá đặc trưng** (mục 10.5.3).

#### 10.1.3 Các họ thuật toán phân cụm

| Họ | Ý tưởng | Cần chọn `K` trước? | Ví dụ |
|---|---|:---:|---|
| **Phân hoạch** (partitional) | Chia thẳng thành `K` phần rời nhau, tối ưu một hàm mục tiêu | Có | **K-means**, K-medoids |
| **Phân cấp** (hierarchical) | Gộp dần (hoặc tách dần) thành cây cụm (**dendrogram**) | Không (cắt cây ở mức bất kỳ) | Agglomerative clustering |
| **Dựa trên mật độ** (density-based) | Cụm là vùng có mật độ điểm cao, điểm lẻ loi là nhiễu | Không | **DBSCAN** |
| **Dựa trên mô hình** (model-based) | Giả định dữ liệu sinh từ hỗn hợp phân phối, ước lượng bằng EM (bảng mục 9.4) | Có | Gaussian Mixture Model (GMM) |

Ngoài ra còn phân biệt **phân cụm cứng** (*hard*: mỗi điểm thuộc đúng một cụm, như K-means) và **phân cụm mềm** (*soft*: mỗi điểm có xác suất thuộc từng cụm, như GMM).

### 10.2 Hàm mục tiêu J

Cho `n` điểm `x₁..xₙ` trong không gian `d` chiều, chia thành `K` cụm `C₁..C_K`. Mỗi cụm `Cⱼ` có **tâm** (centroid) `μⱼ` là **trung bình toạ độ** của các điểm trong cụm:

```
μⱼ = (1 / |Cⱼ|) · Σ_{x ∈ Cⱼ} x
```

K-means cực tiểu hoá **tổng bình phương khoảng cách từ mỗi điểm tới tâm cụm của nó**:

```
J = Σⱼ Σ_{x ∈ Cⱼ} ‖x − μⱼ‖²        với  ‖a − b‖² = Σᵢ (aᵢ − bᵢ)²
```

Đây chính là **hàm sai số bình phương** `E` (cũng gọi là **SSE**, *within-cluster sum of squares* - **WCSS**, hay **inertia** trong `scikit-learn`).

Liên hệ chương 9: `J` đóng vai trò **hàm mất mát** (mục 9.2.1) của bài toán, nhưng không cần nhãn nào.

**Hai tính chất giúp thuật toán đơn giản:**

1. **Với tâm cố định, gán mỗi điểm về tâm gần nhất là tốt nhất**: mỗi điểm đóng góp một số hạng `‖x − μⱼ‖²` vào `J`, chọn `j` làm số hạng này nhỏ nhất thì `J` nhỏ nhất.
2. **Với cách chia cụm cố định, tâm tốt nhất là trung bình**: với một cụm, cực tiểu hoá `f(μ) = Σ ‖x − μ‖²` bằng cách đặt đạo hàm bằng 0: `∂f/∂μ = −2 · Σ (x − μ) = 0`, suy ra `μ = (1/|C|) · Σ x`.

Nhờ hai tính chất này, ta **luân phiên** tối ưu theo từng nhóm biến (cụm của từng điểm, rồi vị trí các tâm), giống kiểu **tối ưu luân phiên từng nhóm biến**, mỗi bước đều không làm `J` tăng.

*Chú ý:* `J` **luôn giảm khi tăng `K`**: `K = 1` cho `J` bằng tổng phương sai của cả tập, `K = n` (mỗi điểm một cụm) cho `J = 0`. Vì vậy **không thể chọn `K` bằng cách cực tiểu hoá `J`**, cần cách khác (mục 10.5.2).

*Chú ý:* tâm `μⱼ` là **điểm trung bình**, thường **không trùng** với điểm dữ liệu nào. Đây là điều kiện bài giảng nêu: thuật toán chỉ áp dụng được khi **trung bình của cụm có định nghĩa**, tức đặc trưng phải là số. Với đặc trưng phân loại (giới tính, tỉnh thành) cần thuật toán khác (K-modes, K-medoids).

### 10.3 Thuật toán K-means Clustering

#### 10.3.1 Các bước

Thuật toán còn có tên **Lloyd's algorithm**.

```
Đầu vào : K (số cụm), D (tập n điểm)
Đầu ra  : K cụm

1. Chọn K điểm của D làm tâm ban đầu μ₁..μ_K          (khởi tạo)
2. Lặp:
   a. GÁN     : mỗi điểm về cụm có tâm gần nó nhất
   b. CẬP NHẬT: mỗi tâm = trung bình các điểm trong cụm
3. Đến khi không điểm nào đổi cụm (tâm không đổi)      (điều kiện dừng)
```

```
Khởi tạo K tâm
      │
      ▼
┌──▶ Bước GÁN: mỗi điểm → tâm gần nhất
│        │
│        ▼
│   Có điểm nào đổi cụm không? ── không ──▶ DỪNG
│        │ có
│        ▼
└─── Bước CẬP NHẬT: tâm = trung bình cụm
```

| Bước | Biến thay đổi | Tác dụng lên `J` |
|---|---|---|
| **Gán** | Cụm của từng điểm | `J` giảm hoặc giữ nguyên (tính chất 1, mục 10.2) |
| **Cập nhật** | Vị trí các tâm | `J` giảm hoặc giữ nguyên (tính chất 2, mục 10.2) |

#### 10.3.2 Vì sao thuật toán dừng

1. Mỗi bước **không làm `J` tăng**, và `J ≥ 0` nên bị chặn dưới.
2. Số cách chia `n` điểm thành `K` cụm là **hữu hạn** (tối đa `Kⁿ`).
3. Khi một lần lặp **đổi cụm** của ít nhất một điểm sang tâm gần hơn thì `J` **giảm thực sự** (khi khoảng cách bằng nhau, dùng một quy ước phá hoà cố định, ví dụ luôn chọn tâm có chỉ số nhỏ nhất, để không quay vòng). Do đó **không thể lặp lại một cách chia cụm đã gặp**, và vì chỉ có hữu hạn cách chia, thuật toán phải dừng sau hữu hạn bước.

*Chú ý:* "dừng" **không có nghĩa là tìm được cách chia tốt nhất**. K-means chỉ đảm bảo đạt một **cực tiểu địa phương** của `J` (giống leo đồi ở mục 7.9 và gradient descent ở mục 9.2.4). Kết quả **phụ thuộc vào tâm ban đầu** (mục 10.5.1). Việc tìm cách chia tối ưu toàn cục là bài toán **NP-khó**.

#### 10.3.3 Độ phức tạp

| Thành phần | Chi phí |
|---|---|
| Một lần **gán** (`n` điểm × `K` tâm × `d` chiều) | `O(n · K · d)` |
| Một lần **cập nhật** | `O(n · d)` |
| Cả thuật toán với `t` lần lặp | `O(t · n · K · d)` |
| Bộ nhớ | `O((n + K) · d)` |

Trong thực tế `t` thường nhỏ (vài chục lần), nên K-means **tuyến tính theo `n`** và chạy được trên dữ liệu rất lớn, một lý do khiến nó phổ biến hơn phân cụm phân cấp (thường `O(n²)` trở lên). Về lý thuyết, trường hợp xấu nhất `t` có thể rất lớn nhưng hiếm gặp.

### 10.4 Ví dụ tính tay

Số liệu nhỏ để tính tay được. Cho `n = 6` điểm hai chiều, cần chia thành `K = 2` cụm:

| Điểm | `(x₁, x₂)` |
|---|---|
| A | (1, 1) |
| B | (2, 1) |
| C | (4, 3) |
| D | (5, 4) |
| E | (5, 6) |
| F | (6, 5) |

Mắt thường thấy hai nhóm: `{A, B}` ở góc dưới trái và `{C, D, E, F}` ở trên phải. Ta cố ý chọn **tâm ban đầu xấu**: `μ₁ = A = (1, 1)`, `μ₂ = B = (2, 1)` (hai tâm nằm sát nhau) để xem thuật toán tự sửa như thế nào.

**Lần lặp 1.** Tâm: `μ₁ = (1, 1)`, `μ₂ = (2, 1)`.

*Bước gán:* tính khoảng cách Euclid tới từng tâm.

| Điểm | `d(·, μ₁)` | `d(·, μ₂)` | Cụm | `d²` tới tâm của cụm |
|---|---|---|---|---|
| A (1, 1) | 0 | 1.000 | 1 | 0 |
| B (2, 1) | 1.000 | 0 | 2 | 0 |
| C (4, 3) | `√13` = 3.606 | `√8` = 2.828 | 2 | 8 |
| D (5, 4) | `√25` = 5.000 | `√18` = 4.243 | 2 | 18 |
| E (5, 6) | `√41` = 6.403 | `√34` = 5.831 | 2 | 34 |
| F (6, 5) | `√41` = 6.403 | `√32` = 5.657 | 2 | 32 |

Cụm 1 = `{A}`, cụm 2 = `{B, C, D, E, F}`. Tổng cột cuối: `J = 0 + 0 + 8 + 18 + 34 + 32 = 92`.

*Bước cập nhật:*

```
μ₁ = (1, 1)
μ₂ = ((2+4+5+5+6)/5 , (1+3+4+6+5)/5) = (22/5 , 19/5) = (4.4 , 3.8)
```

Tính lại `J` với tâm mới: cụm 1 cho 0; cụm 2 cho `13.6 + 0.8 + 0.4 + 5.2 + 4.0 = 24.0` (lần lượt B, C, D, E, F), nên **`J = 24.0`**.

**Lần lặp 2.** Tâm: `μ₁ = (1, 1)`, `μ₂ = (4.4, 3.8)`.

| Điểm | `d(·, μ₁)` | `d(·, μ₂)` | Cụm | `d²` tới tâm của cụm |
|---|---|---|---|---|
| A (1, 1) | 0 | `√19.4` = 4.405 | 1 | 0 |
| B (2, 1) | 1.000 | `√13.6` = 3.688 | **1** (đổi) | 1 |
| C (4, 3) | 3.606 | `√0.8` = 0.894 | 2 | 0.8 |
| D (5, 4) | 5.000 | `√0.4` = 0.632 | 2 | 0.4 |
| E (5, 6) | 6.403 | `√5.2` = 2.280 | 2 | 5.2 |
| F (6, 5) | 6.403 | `√4` = 2.000 | 2 | 4.0 |

Điểm **B đổi từ cụm 2 sang cụm 1**. `J` (sau gán) `= 0 + 1 + 0.8 + 0.4 + 5.2 + 4.0 = 11.4`. Cập nhật:

```
μ₁ = ((1+2)/2 , (1+1)/2)             = (1.5 , 1.0)
μ₂ = ((4+5+5+6)/4 , (3+4+6+5)/4)     = (5.0 , 4.5)
```

Cách chia là `{A, B}` và `{C, D, E, F}`; `J` mới: cụm 1 cho `0.25 + 0.25 = 0.5`, cụm 2 cho `3.25 + 0.25 + 2.25 + 1.25 = 7.0`, nên **`J = 7.5`**.

**Lần lặp 3.** Tâm: `μ₁ = (1.5, 1)`, `μ₂ = (5, 4.5)`.

| Điểm | `d(·, μ₁)` | `d(·, μ₂)` | Cụm |
|---|---|---|---|
| A (1, 1) | 0.500 | `√24.5` = 4.950 | 1 |
| B (2, 1) | 0.500 | `√21.25` = 4.610 | 1 |
| C (4, 3) | `√10.25` = 3.202 | `√3.25` = 1.803 | 2 |
| D (5, 4) | `√21.25` = 4.610 | 0.500 | 2 |
| E (5, 6) | `√37.25` = 6.103 | 1.500 | 2 |
| F (6, 5) | `√36.25` = 6.021 | `√1.25` = 1.118 | 2 |

**Không điểm nào đổi cụm**, nên tâm không đổi: thuật toán **dừng** với `J = 7.5`.

**Diễn biến của `J`:**

| Thời điểm | `J` |
|---|---|
| Lần 1, sau gán (tâm ban đầu) | 92.0 |
| Lần 1, sau cập nhật | 24.0 |
| Lần 2, sau gán | 11.4 |
| Lần 2, sau cập nhật | 7.5 |
| Lần 3 (không đổi) | 7.5 |

**Nhận xét:**

- `J` **giảm sau mỗi bước** và không bao giờ tăng, đúng như mục 10.3.2.
- Dù tâm ban đầu xấu (hai tâm sát nhau), thuật toán vẫn tìm ra cách chia hợp lý nhờ vòng lặp gán - cập nhật. Nếu chọn tâm ban đầu là `A` và `F` (xa nhau), thuật toán chỉ cần **2 lần lặp** và ra **cùng kết quả**.
- **Không phải lần nào cũng may mắn như vậy**: ví dụ ở mục 10.5.1 cho thấy tâm ban đầu xấu có thể làm K-means kẹt ở cách chia tệ.

### 10.5 Các vấn đề thực tế

Bài giảng nêu bốn hạn chế của K-means; bảng dưới tóm tắt và chỉ ra mục xử lý:

| Hạn chế (theo bài giảng) | Hậu quả | Hướng xử lý |
|---|---|---|
| Chỉ áp dụng khi **trung bình** của cụm có định nghĩa | Không dùng được cho đặc trưng phân loại | K-modes, K-medoids (mục 10.5.5) |
| Phải **chỉ định trước số cụm `K`** | Chọn sai `K` cho cách chia vô nghĩa | Elbow, silhouette (mục 10.5.2) |
| Không phù hợp cụm có **hình dạng không lồi** | Cắt đôi cụm hình trăng khuyết, hình vòng | DBSCAN, GMM (mục 10.5.4, 10.5.5) |
| **Nhạy với nhiễu và ngoại lệ** | Một điểm xa kéo lệch cả tâm cụm | Loại ngoại lệ, K-medoids (mục 10.5.4) |

Ngoài ra còn hai vấn đề quan trọng khi dùng thật: **kết quả phụ thuộc khởi tạo** (mục 10.5.1) và **phụ thuộc thang đo đặc trưng** (mục 10.5.3).

#### 10.5.1 Khởi tạo tâm cụm

Vì K-means chỉ tìm cực tiểu địa phương, tâm ban đầu quyết định kết quả cuối cùng.

*Ví dụ tính tay (1 chiều):* 6 điểm `1, 2, 10, 11, 20, 21`, `K = 3`. Rõ ràng có ba cụm `{1, 2}`, `{10, 11}`, `{20, 21}` với `J = 3 × 0.5 = 1.5`. Nhưng nếu chọn tâm ban đầu `1, 2, 10` (hai tâm nằm trong cùng một nhóm):

| Lần | Gán | Tâm mới | `J` |
|---|---|---|---|
| 1 | `{1}`, `{2}`, `{10, 11, 20, 21}` | `1`, `2`, `15.5` | 222 → 101 |
| 2 | Không đổi | Dừng | **101** |

K-means dừng ở `J = 101`, **gấp hơn 60 lần** mức tốt nhất 1.5: cụm thứ ba gộp lẫn `{10, 11}` với `{20, 21}`. Đây là **cực tiểu địa phương**.

**Các cách khởi tạo:**

| Cách | Mô tả | Nhận xét |
|---|---|---|
| **Random / Forgy** | Chọn ngẫu nhiên `K` điểm dữ liệu làm tâm (cách của bài giảng) | Đơn giản, dễ gặp hai tâm trong cùng một nhóm |
| **Random partition** | Gán ngẫu nhiên mỗi điểm vào một cụm rồi tính tâm | Các tâm ban đầu thường nằm gần trung tâm dữ liệu |
| **k-means++** | Tâm đầu chọn ngẫu nhiên đều; mỗi tâm sau chọn với **xác suất tỉ lệ `D(x)²`**, `D(x)` là khoảng cách từ `x` tới tâm gần nhất đã chọn | Các tâm có xu hướng **rải xa nhau**; có bảo đảm lý thuyết về chất lượng; là **mặc định** của `scikit-learn` |
| **Chạy nhiều lần** (`n_init`) | Chạy cả thuật toán nhiều lần với khởi tạo khác nhau, **giữ lần có `J` nhỏ nhất** | Rẻ, hiệu quả, nên luôn dùng |

Kết quả đo trên đúng ví dụ 1 chiều này (1000 lần chạy với `seed` khác nhau; các con số có thể lệch đôi chút giữa các phiên bản Python): khởi tạo ngẫu nhiên kẹt khoảng **23%** số lần, `k-means++` chỉ kẹt khoảng **0.7%**, còn chạy ngẫu nhiên 10 lần rồi lấy lần tốt nhất thì **không lần nào kẹt**.

#### 10.5.2 Chọn số cụm K

Vì `J` luôn giảm khi `K` tăng (mục 10.2), ta không chọn `K` bằng cách cực tiểu `J`. Hai cách phổ biến:

**Phương pháp khuỷu tay (elbow):** vẽ `J` theo `K`; chọn `K` tại **"khuỷu tay"**, nơi `J` ngừng giảm nhanh (thêm cụm không còn đem lại lợi ích đáng kể).

**Hệ số silhouette:** với mỗi điểm `i`, gọi `a(i)` là khoảng cách trung bình tới các điểm **cùng cụm**, `b(i)` là khoảng cách trung bình tới các điểm của **cụm gần nhất khác**:

```
s(i) = (b(i) − a(i)) / max(a(i), b(i))        ∈ [−1, 1]
```

`s ≈ 1`: điểm nằm đúng cụm của nó và xa cụm khác; `s ≈ 0`: điểm nằm sát ranh giới hai cụm; `s < 0`: có thể đã bị gán nhầm cụm. **Silhouette trung bình** của mọi điểm càng lớn càng tốt; chọn `K` làm giá trị này lớn nhất. Ưu điểm so với `J`: silhouette **không tự động tốt hơn khi `K` tăng**.

*Kết quả đo trên dữ liệu 150 điểm sinh từ 3 đám (50 điểm quanh mỗi tâm `(2, 2)`, `(8, 3)`, `(5, 9)`, độ lệch chuẩn 0.8, sinh bằng `random.Random(42).gauss`):*

| `K` | `J` | Silhouette |
|---|---|---|
| 1 | 2526.51 | - |
| 2 | 1124.41 | 0.573 |
| **3** | **190.22** | **0.773** |
| 4 | 158.01 | 0.627 |
| 5 | 132.42 | 0.489 |
| 6 | 113.98 | 0.346 |

`J` tụt rất mạnh từ `K = 2` xuống `K = 3` (1124 → 190) rồi chỉ giảm chậm: **khuỷu tay ở `K = 3`**. Silhouette cũng đạt **cực đại ở `K = 3`**, khớp với số đám dùng để sinh dữ liệu.

*Chú ý:* với dữ liệu thật, khuỷu tay thường **không rõ ràng** và hai phương pháp có thể cho đáp án khác nhau. Nên kết hợp với **hiểu biết về bài toán** (ví dụ công ty chỉ có nguồn lực làm 4 chiến dịch thì chọn `K = 4`). Ngoài ra còn các cách khác: **gap statistic**, hoặc dùng GMM rồi chọn `K` bằng **BIC**.

#### 10.5.3 Chuẩn hoá đặc trưng

Giống k-NN (mục 9.5), K-means dùng khoảng cách Euclid nên **đặc trưng có giá trị lớn sẽ lấn át đặc trưng nhỏ**. Cách thông dụng là **chuẩn hoá z-score**:

```
z = (x − μ) / σ        (μ, σ: trung bình và độ lệch chuẩn của từng đặc trưng)
```

*Ví dụ:* 6 khách hàng gồm tuổi (năm) và thu nhập (đồng/tháng): `(22, 15 triệu)`, `(24, 38 triệu)`, `(26, 22 triệu)`, `(52, 41 triệu)`, `(55, 17 triệu)`, `(58, 30 triệu)`. Chênh lệch tuổi cỡ vài chục, chênh lệch thu nhập cỡ hàng chục triệu, nên **bình phương khoảng cách gần như chỉ do thu nhập quyết định**:

| Dữ liệu | Hai cụm tìm được |
|---|---|
| **Chưa chuẩn hoá** | Thu nhập thấp `{15, 22, 17 triệu}` và thu nhập cao `{38, 41, 30 triệu}` (**bỏ qua hoàn toàn tuổi**) |
| **Đã chuẩn hoá** | Nhóm trẻ `{22, 24, 26 tuổi}` và nhóm lớn tuổi `{52, 55, 58 tuổi}` |

Cách nào "đúng" tuỳ mục đích, nhưng **đơn vị đo (đồng hay triệu đồng) không nên là thứ quyết định kết quả**. Đổi thu nhập từ đồng sang triệu đồng sẽ làm kết quả thô đổi theo, còn dữ liệu đã chuẩn hoá thì không.

*Chú ý:* như đã nêu ở mục 9.1.5 và 9.2.3, tính `μ`, `σ` trên dữ liệu rồi mới chia tập huấn luyện/kiểm tra sẽ gây **rò rỉ dữ liệu**. Khi dùng K-means để gán cụm cho **điểm mới**, phải dùng **cùng `μ`, `σ`** đã tính lúc huấn luyện.

#### 10.5.4 Ngoại lệ, cụm rỗng và hình dạng cụm

**Ngoại lệ (outlier):** tâm là **trung bình** nên bị điểm xa kéo lệch. Ví dụ cụm `{10, 11, 12}` có tâm 11; thêm điểm `100` thì tâm thành `(10 + 11 + 12 + 100) / 4 = 33.25`, **xa mọi điểm bình thường**. Hướng xử lý: phát hiện và loại ngoại lệ trước, hoặc dùng **K-medoids** (tâm là một điểm dữ liệu thật, mục 10.5.5).

**Cụm rỗng:** có thể xảy ra (ví dụ khi hai tâm ban đầu trùng nhau, mọi điểm đều về tâm có chỉ số nhỏ hơn). Khi đó không thể tính trung bình (chia cho 0). Cách xử lý thường gặp: **giữ nguyên tâm cũ** hoặc chuyển tâm đó tới điểm đang **xa tâm của cụm nó nhất**.

**Hình dạng cụm:** do dùng khoảng cách tới tâm, K-means ngầm giả định cụm **lồi, gần hình cầu, kích thước và mật độ tương đương**. Về mặt lý thuyết, K-means chính là trường hợp giới hạn của GMM khi các cụm có **cùng phương sai hình cầu** và gán cứng (bài giảng phát biểu là "các cụm có phân phối Gauss").

| Dạng dữ liệu | K-means làm gì | Nên dùng |
|---|---|---|
| Hai nửa vành khuyên (`make_moons`), vòng tròn đồng tâm | **Cắt sai**: chia theo đường thẳng, không theo hình dạng | DBSCAN, spectral clustering |
| Các cụm kích thước hoặc mật độ khác nhau | Cụm lớn bị cắt, kéo điểm sang cụm nhỏ | GMM |
| Cụm hình elip nghiêng | Chia theo khoảng cách tới tâm nên không bám trục elip | GMM với ma trận hiệp phương sai đầy đủ |
| Số chiều rất lớn | Khoảng cách các điểm gần như bằng nhau (lời nguyền số chiều, mục 9.5) | Giảm chiều (PCA) trước khi phân cụm |

#### 10.5.5 Các biến thể và thuật toán thay thế

| Thuật toán | Khác K-means ở điểm nào | Dùng khi |
|---|---|---|
| **K-medoids** (PAM) | Tâm là **một điểm dữ liệu thật**; dùng được với khoảng cách bất kỳ | Có ngoại lệ, đặc trưng không phải số thuần tuý |
| **K-modes / K-prototypes** | Thay trung bình bằng **giá trị phổ biến nhất** (đặc trưng phân loại) hoặc trộn cả hai loại | Dữ liệu phân loại hoặc hỗn hợp |
| **Mini-batch K-means** | Mỗi bước cập nhật tâm chỉ trên **một lô nhỏ** (liên hệ SGD, mục 9.2.4) | Dữ liệu rất lớn |
| **Bisecting K-means** | Bắt đầu một cụm, lần lượt **tách đôi** cụm có `J` lớn nhất | Muốn cấu trúc phân cấp |
| **Fuzzy C-means** | **Phân cụm mềm**: mỗi điểm có độ thuộc về từng cụm | Cụm chồng lấn |
| **GMM + EM** (mục 9.4) | Cụm là phân phối Gauss, gán mềm, có ma trận hiệp phương sai | Cụm elip, cần xác suất |
| **DBSCAN** | Dựa trên **mật độ**, không cần `K`, nhận biết điểm nhiễu | Cụm hình dạng bất kỳ |

### 10.6 Các ứng dụng

| Ứng dụng | Tiếng Anh | Mô tả ngắn |
|---|---|---|
| **Phân khúc khách hàng** | Customer segmentation | Gom khách hàng theo hành vi mua (ví dụ gần đây, tần suất, giá trị: RFM) để thiết kế chiến dịch riêng cho từng nhóm |
| **Giảm số màu / nén ảnh** | Color quantization | Mỗi điểm ảnh là điểm 3 chiều `(R, G, B)`; `K` tâm cụm chính là **bảng màu** `K` màu |
| **Lượng tử hoá vector** | Vector quantization | Thay mỗi vector bằng tâm cụm gần nhất để nén dữ liệu (âm thanh, ảnh) |
| **Gom nhóm văn bản** | Document clustering | Biểu diễn mỗi văn bản thành vector (ví dụ TF-IDF) rồi gom theo chủ đề |
| **Chọn tâm cho mô hình khác** | Initialization for other models | Dùng K-means chọn tâm cho mạng hàm cơ sở xuyên tâm (RBF, bảng mục 9.4) hoặc khởi tạo cho GMM |
| **Phát hiện bất thường** | Anomaly detection | Điểm cách xa mọi tâm cụm là điểm đáng nghi |
| **Định vị cơ sở** | Facility location | Đặt `K` kho hàng gần các khách hàng nhất: gần với bài toán định vị ở mục 8.6.4 |

### 10.7 Tổng kết

| Nội dung | Ý chính |
|---|---|
| **Phân cụm** | Gom đối tượng giống nhau thành nhóm **không cần nhãn**; bài toán điển hình của học không giám sát |
| **Khác phân loại** | Phân loại có nhãn và nhóm biết trước (k-NN); phân cụm không nhãn, nhóm do thuật toán tìm, ý nghĩa do con người diễn giải |
| **K-means** | Chia dữ liệu thành `K` cụm, mỗi cụm đại diện bằng **tâm** là trung bình toạ độ |
| **Hàm mục tiêu** | `J = Σⱼ Σ_{x∈Cⱼ} ‖x − μⱼ‖²` (SSE, WCSS, inertia); luôn giảm khi `K` tăng nên không dùng để chọn `K` |
| **Thuật toán** | Khởi tạo `K` tâm, lặp **gán** (về tâm gần nhất) và **cập nhật** (tâm = trung bình) đến khi không điểm nào đổi cụm |
| **Vì sao dừng** | Mỗi bước không làm `J` tăng, số cách chia hữu hạn; nhưng chỉ đạt **cực tiểu địa phương** |
| **Độ phức tạp** | `O(t · n · K · d)`, tuyến tính theo số điểm |
| **Ví dụ tính tay** | 6 điểm, `K = 2`, tâm đầu `A`, `B`: `J` đi 92 → 24 → 11.4 → 7.5, dừng ở lần 3 |
| **Khởi tạo** | Kết quả phụ thuộc tâm đầu: dùng **k-means++** và **chạy nhiều lần** (`n_init`), giữ lần có `J` nhỏ nhất |
| **Chọn `K`** | Khuỷu tay của `J`, silhouette trung bình lớn nhất, kết hợp hiểu biết về bài toán |
| **Chuẩn hoá** | Bắt buộc khi các đặc trưng khác thang đo (z-score); dùng cùng `μ`, `σ` cho điểm mới |
| **Hạn chế** | Cần `K` trước, trung bình phải có nghĩa, cụm lồi dạng cầu, nhạy ngoại lệ |
| **Thay thế** | K-medoids, K-modes, mini-batch, GMM/EM, DBSCAN, phân cụm phân cấp |

### 10.8 Từ khoá để tự tìm hiểu thêm

Các từ khoá tiếng Anh nên dùng khi tra cứu sách, bài báo hoặc khoá học:

| Chủ đề | Từ khoá tìm kiếm |
|---|---|
| Nền tảng | `clustering unsupervised learning`, `k-means clustering`, `Lloyd's algorithm`, `within-cluster sum of squares`, `centroid`, `k-means convergence local minimum` |
| Khởi tạo | `k-means++ initialization`, `Forgy random partition`, `n_init multiple restarts` |
| Chọn số cụm | `elbow method`, `silhouette score`, `gap statistic`, `Davies-Bouldin index`, `Bayesian information criterion` |
| Tiền xử lý | `feature scaling standardization`, `z-score normalization`, `curse of dimensionality PCA` |
| Biến thể | `k-medoids PAM`, `k-modes k-prototypes`, `mini-batch k-means`, `bisecting k-means`, `fuzzy c-means` |
| Thuật toán khác | `hierarchical clustering dendrogram`, `DBSCAN`, `Gaussian mixture model EM`, `spectral clustering` |
| Đánh giá | `cluster purity`, `adjusted Rand index`, `normalized mutual information` |
| Ứng dụng | `customer segmentation RFM`, `color quantization k-means`, `vector quantization`, `document clustering TF-IDF` |
| Công cụ | `scikit-learn KMeans`, `MiniBatchKMeans`, `NumPy`, `Pillow` |
| Tài liệu tham khảo | Jiawei Han, *Data Mining: Concepts and Techniques* (2006); Arthur & Vassilvitskii, *k-means++: The Advantages of Careful Seeding* (2007); Russell & Norvig, *Artificial Intelligence: A Modern Approach* (phần Learning) |
