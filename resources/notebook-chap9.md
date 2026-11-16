# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 9: Học máy (Machine learning)

### Mục lục

- [Artificial Intelligence Notebook](#artificial-intelligence-notebook)
  - [Chapter 9: Học máy (Machine learning)](#chapter-9-học-máy-machine-learning)
    - [Mục lục](#mục-lục)
    - [9.1 Khái niệm](#91-khái-niệm)
      - [9.1.1 Định nghĩa](#911-định-nghĩa)
      - [9.1.2 Học máy khác lập trình truyền thống](#912-học-máy-khác-lập-trình-truyền-thống)
      - [9.1.3 Học máy, suy diễn thống kê và khai phá dữ liệu](#913-học-máy-suy-diễn-thống-kê-và-khai-phá-dữ-liệu)
      - [9.1.4 Vai trò của con người](#914-vai-trò-của-con-người)
      - [9.1.5 Quy trình một dự án học máy](#915-quy-trình-một-dự-án-học-máy)
      - [9.1.6 Đạo đức và thiên lệch dữ liệu](#916-đạo-đức-và-thiên-lệch-dữ-liệu)
    - [9.2 Các khái niệm nền tảng](#92-các-khái-niệm-nền-tảng)
      - [9.2.1 Dữ liệu và mô hình](#921-dữ-liệu-và-mô-hình)
      - [9.2.2 Khái quát hoá, overfitting và underfitting](#922-khái-quát-hoá-overfitting-và-underfitting)
      - [9.2.3 Chia dữ liệu và đánh giá mô hình](#923-chia-dữ-liệu-và-đánh-giá-mô-hình)
      - [9.2.4 Gradient descent](#924-gradient-descent)
    - [9.3 Các loại giải thuật học](#93-các-loại-giải-thuật-học)
      - [9.3.1 Học có giám sát](#931-học-có-giám-sát)
      - [9.3.2 Học không giám sát](#932-học-không-giám-sát)
      - [9.3.3 Học bán giám sát](#933-học-bán-giám-sát)
      - [9.3.4 Học tăng cường](#934-học-tăng-cường)
      - [9.3.5 Học chuyển đổi](#935-học-chuyển-đổi)
      - [9.3.6 Học cách học](#936-học-cách-học)
    - [9.4 Các chủ đề và kỹ thuật học máy](#94-các-chủ-đề-và-kỹ-thuật-học-máy)
    - [9.5 Ví dụ minh hoạ: phân loại bằng k láng giềng gần nhất](#95-ví-dụ-minh-hoạ-phân-loại-bằng-k-láng-giềng-gần-nhất)
    - [9.6 Các ứng dụng](#96-các-ứng-dụng)
    - [9.7 Tổng kết](#97-tổng-kết)
    - [9.8 Từ khoá để tự tìm hiểu thêm](#98-từ-khoá-để-tự-tìm-hiểu-thêm)

**Vấn đề:** Các chương trước giải bài toán bằng cách con người **tự viết ra quy tắc** (luật suy diễn, hàm heuristic, hàm thích nghi...). Với những bài toán như nhận dạng chữ viết, lọc thư rác hay dịch ngôn ngữ, không ai viết nổi đầy đủ các quy tắc đó bằng tay, nhưng lại có rất nhiều **dữ liệu ví dụ**.

**Mục tiêu:** Hiểu học máy là gì, phân biệt được các loại học (có giám sát, không giám sát, tăng cường...), nắm các khái niệm nền tảng (dữ liệu huấn luyện, overfitting, đánh giá mô hình), biết tên tiếng Anh của các kỹ thuật chính để tự tra cứu, và cài đặt được một thuật toán học đơn giản (`K-Nearest Neighbors` - `k-NN`).

### 9.1 Khái niệm

#### 9.1.1 Định nghĩa

> **Học máy** (Machine Learning - ML, có tài liệu gọi là *máy học*) là một lĩnh vực của trí tuệ nhân tạo, nghiên cứu và xây dựng các kỹ thuật cho phép hệ thống **"học" tự động từ dữ liệu** để giải quyết những vấn đề cụ thể.

Hai định nghĩa kinh điển:

- **Arthur Samuel (1959):** học máy là lĩnh vực nghiên cứu cung cấp cho máy tính **khả năng học hỏi mà không cần được lập trình một cách rõ ràng** (*"...without being explicitly programmed"*). Samuel là người viết chương trình chơi cờ đam (checkers) tự cải thiện qua các ván đấu.
- **Tom M. Mitchell (1997):** định nghĩa theo dạng **hình thức**, có thể kiểm chứng được:

> *"A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E."*

Nghĩa là một chương trình "học" khi **hiệu năng P** trên **nhiệm vụ T** tăng lên nhờ **kinh nghiệm E**. Khi gặp một bài toán học máy, hãy xác định ba thành phần **(T, P, E)** trước:

| Bài toán | Nhiệm vụ T | Độ đo P | Kinh nghiệm E |
|---|---|---|---|
| Lọc thư rác (spam filter) | Phân loại email là spam hay không | Tỉ lệ email phân loại đúng | Tập email đã được người dùng gắn nhãn spam/không spam |
| Chơi cờ đam (Samuel) | Chơi cờ đam | Tỉ lệ thắng | Các ván tự chơi với chính mình |
| Nhận dạng chữ viết tay | Đọc ra chữ từ ảnh | Tỉ lệ ký tự đọc đúng | Tập ảnh chữ viết tay kèm đáp án |
| Dự đoán giá nhà | Ước lượng giá một căn nhà | Sai số trung bình | Dữ liệu các giao dịch đã diễn ra |

**Mục tiêu cốt lõi: khái quát hoá** (generalization). Một "người học" (người hay máy) cần **khái quát hoá từ kinh nghiệm đã có** để xử lý thành công các nhiệm vụ **chưa từng gặp**. Vì vậy, một máy học tốt phải thực hiện **chính xác trên dữ liệu mới** sau khi đã được huấn luyện trên một tập dữ liệu, chứ không phải chỉ "thuộc lòng" tập huấn luyện (xem mục 9.2.2).

#### 9.1.2 Học máy khác lập trình truyền thống

```
Lập trình truyền thống:   Dữ liệu  +  Chương trình (quy tắc do người viết)  →  Kết quả
Học máy:                  Dữ liệu  +  Kết quả mong muốn (nhãn)              →  Chương trình (mô hình)
```

| | Lập trình truyền thống | Học máy |
|---|---|---|
| Quy tắc xuất phát từ | Con người viết tay | Thuật toán **rút ra từ dữ liệu** |
| Khi bài toán thay đổi | Sửa code | Huấn luyện lại với dữ liệu mới |
| Phù hợp khi | Quy tắc rõ ràng, ít (ví dụ: tính thuế) | Quy tắc khó diễn đạt, quá nhiều hoặc thay đổi theo thời gian (ví dụ: nhận dạng khuôn mặt) |
| Điểm yếu | Không mở rộng được với bài toán phức tạp | Cần nhiều dữ liệu chất lượng; mô hình có thể khó giải thích |

*Chú ý:* học máy **không** phải lúc nào cũng tốt hơn. Nếu có thuật toán chính xác, đơn giản và hiệu quả cho bài toán (ví dụ sắp xếp, tìm đường đi ngắn nhất ở chương 3) thì không cần học máy.

#### 9.1.3 Học máy, suy diễn thống kê và khai phá dữ liệu

- **Suy diễn thống kê** (statistical inference): học máy **rất gần** với lĩnh vực này, nhiều phương pháp dùng chung, chủ yếu khác nhau về **thuật ngữ** và trọng tâm (thống kê thiên về giải thích mối quan hệ và suy ra tham số, học máy thiên về **dự đoán** chính xác).

| Thuật ngữ thống kê | Thuật ngữ học máy |
|---|---|
| Biến độc lập (independent variable) | **Đặc trưng** (feature) |
| Biến phụ thuộc (dependent variable) | **Nhãn** (label), đầu ra (target) |
| Ước lượng tham số (estimation) | **Huấn luyện** (training) |
| Hồi quy / phân loại (regression / classification) | Giữ nguyên tên |

- **Khai phá dữ liệu** (Data Mining) và học máy hay bị **nhầm lẫn**. Hai lĩnh vực khá gần nhau, đôi khi dùng chung nhiều phương pháp và công cụ, nhưng khác nhau chủ yếu ở **mục tiêu**:

| | Khai phá dữ liệu (Data Mining) | Học máy (Machine Learning) |
|---|---|---|
| Mục tiêu | Tìm **thông tin, tri thức hoàn toàn mới**, tiềm năng có ích trong nguồn dữ liệu (*discover*) | **Dự đoán** một số thông tin của dữ liệu dựa trên các **đặc tính đã biết** (*predict*) |
| Ví dụ | Phát hiện nhóm khách hàng hay mua hai mặt hàng cùng nhau (luật kết hợp, *association rules*) | Dự đoán khách hàng mới có mua hàng hay không |

Hai lĩnh vực thường kết hợp: khai phá dữ liệu có thể dùng thuật toán học máy làm công cụ, và học máy cần dữ liệu đã được làm sạch, trích xuất qua các bước khai phá dữ liệu.

*Chú ý:* ranh giới "khám phá" và "dự đoán" chỉ mang tính tương đối. Trong thực tế hai lĩnh vực dùng chung nhiều phương pháp và công cụ (ví dụ phân cụm hay cây quyết định có thể dùng để khám phá nhóm khách hàng, cũng có thể dùng để dự đoán), nên cùng một kỹ thuật thuộc về lĩnh vực nào thường tuỳ vào mục đích sử dụng.

#### 9.1.4 Vai trò của con người

- Một số hệ thống học máy cố gắng **loại bỏ nhu cầu trực giác của con người** trong việc phân tích dữ liệu.
- Tuy nhiên **không thể loại bỏ hoàn toàn tác động của con người**: con người vẫn chọn bài toán, thu thập và gắn nhãn dữ liệu, chọn đặc trưng (feature engineering), chọn mô hình, chỉnh siêu tham số (hyperparameter) và diễn giải kết quả.
- Học máy có thể xem là nỗ lực **tự động hoá một phần** của quy trình khoa học: thay vì con người quan sát dữ liệu rồi tự nghĩ ra quy luật, máy làm một phần việc đó.

#### 9.1.5 Quy trình một dự án học máy

Một dự án học máy thực tế không chỉ là "chạy một thuật toán". Các bước điển hình:

| Bước | Việc cần làm | Liên hệ trong chương |
|---|---|---|
| 1. Xác định bài toán | Xác định **(T, P, E)**; cân nhắc có thực sự cần học máy không | Mục 9.1.1, 9.1.2 |
| 2. Thu thập dữ liệu | Lấy dữ liệu đại diện cho tình huống thật; gắn nhãn nếu cần | Mục 9.1.4, 9.3 |
| 3. Làm sạch dữ liệu | Xử lý giá trị thiếu, mẫu trùng lặp, ngoại lệ, nhãn sai | Mục 9.5 (mẫu nhiễu) |
| 4. Kỹ thuật đặc trưng | Chọn, tạo, biến đổi, chuẩn hoá đặc trưng (**feature engineering**) | Mục 9.5 (chuẩn hoá) |
| 5. Huấn luyện | Học tham số trên **tập huấn luyện** | Mục 9.2.1, 9.2.4 |
| 6. Kiểm định | Chọn siêu tham số, so sánh mô hình trên **tập kiểm định** (validation) | Mục 9.2.3 |
| 7. Kiểm tra | Đánh giá cuối cùng **một lần** trên **tập kiểm tra** (test) | Mục 9.2.3 |
| 8. Triển khai và giám sát | Đưa vào sử dụng, theo dõi hiệu năng; dữ liệu thực tế có thể đổi theo thời gian (**data drift**) nên cần huấn luyện lại | Mục 9.1.2 |

*Chú ý:* quy trình này **lặp đi lặp lại**, không đi một chiều: kết quả kiểm định kém thường buộc quay lại bước 3-4 hoặc thu thập thêm dữ liệu. Nên **chia dữ liệu train/validation/test từ sớm**, trước khi chuẩn hoá hay chọn đặc trưng dựa trên thống kê của dữ liệu, nếu không dễ gây rò rỉ dữ liệu (mục 9.2.3).

#### 9.1.6 Đạo đức và thiên lệch dữ liệu

Vì mô hình **học từ dữ liệu**, nó cũng học luôn cả những thiên lệch có trong dữ liệu đó:

- **Thiên lệch dữ liệu** (data bias): dữ liệu thu thập không đại diện cho mọi nhóm người hoặc phản ánh định kiến trong quá khứ. Ví dụ: mô hình sàng lọc hồ sơ học từ dữ liệu tuyển dụng cũ vốn thiên về một nhóm, sẽ lặp lại và có thể khuếch đại thiên lệch đó.
- **Công bằng** (fairness): nên đo hiệu năng **riêng cho từng nhóm** (theo giới tính, độ tuổi, vùng miền...), vì độ chính xác trung bình cao có thể che giấu việc mô hình sai nhiều hơn ở một nhóm thiểu số.
- **Quyền riêng tư** (privacy): dữ liệu huấn luyện thường chứa thông tin cá nhân; cần xin phép, ẩn danh hoá, chỉ thu thập phần cần thiết và tuân thủ quy định về bảo vệ dữ liệu.
- **Giải thích được và trách nhiệm**: với các quyết định ảnh hưởng đến con người (cho vay, chẩn đoán, tuyển dụng), cần có khả năng giải thích mô hình và xác định ai chịu trách nhiệm khi mô hình sai.

*Chú ý:* "bias" ở đây (thiên lệch về mặt xã hội/dữ liệu) **khác** với "bias" trong *bias-variance tradeoff* (độ chệch của mô hình, mục 9.2.2).

### 9.2 Các khái niệm nền tảng

#### 9.2.1 Dữ liệu và mô hình

| Thuật ngữ | Tiếng Anh | Ý nghĩa | Ví dụ (dự đoán giá nhà) |
|---|---|---|---|
| **Mẫu** (ví dụ, quan sát) | sample / example / instance | Một đối tượng trong dữ liệu | Một căn nhà |
| **Đặc trưng** | feature (attribute) | Một thuộc tính mô tả mẫu; các đặc trưng ghép thành **vector đặc trưng** `x` | Diện tích, số phòng, khu vực |
| **Nhãn** | label / target | Đáp án cần dự đoán `y` | Giá nhà |
| **Tập huấn luyện** | training set | Các cặp `(x, y)` dùng để học | Hàng nghìn căn nhà đã bán |
| **Mô hình** | model | Hàm `f` ánh xạ `x → y` do thuật toán học ra | Công thức ước lượng giá |
| **Tham số** | parameter | Giá trị mô hình **tự học** từ dữ liệu | Các hệ số trong công thức |
| **Siêu tham số** | hyperparameter | Giá trị **người dùng chọn trước** khi học | Số láng giềng `k` trong k-NN |
| **Hàm mất mát** | loss function | Đo mô hình dự đoán **sai bao nhiêu**; quá trình học là **cực tiểu hoá** hàm này | Bình phương sai số |
| **Huấn luyện** | training (fitting) | Tìm tham số làm hàm mất mát nhỏ | |
| **Suy luận** | inference (prediction) | Dùng mô hình đã học để dự đoán mẫu mới | |

Có thể nhìn học máy như một bài toán **tối ưu** (liên hệ chương 7 và 8): không gian tìm kiếm là các mô hình khả dĩ, hàm mục tiêu là hàm mất mát trên dữ liệu. Thuật toán di truyền cũng có thể dùng để huấn luyện mô hình (ví dụ lập trình di truyền ở mục 7.5.4). Với các mô hình có hàm mất mát khả vi, cách huấn luyện phổ biến nhất là **gradient descent** (mục 9.2.4).

#### 9.2.2 Khái quát hoá, overfitting và underfitting

| Hiện tượng | Biểu hiện | Nguyên nhân thường gặp | Hướng khắc phục |
|---|---|---|---|
| **Overfitting** (học vẹt, quá khớp) | Sai số trên **tập huấn luyện thấp** nhưng trên **tập kiểm tra (test) / dữ liệu mới cao** | Mô hình quá phức tạp, quá ít dữ liệu, dữ liệu nhiễu bị học theo | Thêm dữ liệu, đơn giản hoá mô hình, **regularization** (xem bên dưới), dừng sớm (early stopping) |
| **Underfitting** (quá đơn giản) | Sai số cao **cả** trên tập huấn luyện lẫn tập kiểm tra (test) | Mô hình quá đơn giản, đặc trưng không đủ thông tin | Dùng mô hình mạnh hơn, thêm đặc trưng, huấn luyện lâu hơn |

```
Sai số
  │ x
  │ ox
  │  ox
  │    xx                                   xxxx  ← sai số trên tập kiểm tra (test): hình chữ U
  │     oxx                             xxxx
  │       oxxx                     xxxxx
  │         ooxxxxxxx      xxxxxxxx
  │            oooo  xxXxxx
  │                oooooo
  │                    ¦ oooooooooooooooooo
  │                    ¦                   ooooo  ← sai số trên tập huấn luyện (train): giảm đều
  └─────────────────────────────────────────────→ độ phức tạp của mô hình
    underfitting       ↑            overfitting
                 điểm cân bằng
```

Chú giải: `o` là sai số trên **tập huấn luyện** (giảm đều khi mô hình phức tạp hơn); `x` là sai số trên **tập kiểm tra (test)** (giảm rồi tăng lại, có dạng chữ U); `X` là **điểm cực tiểu** của đường test, gọi là **điểm cân bằng**: bên trái là underfitting, bên phải là overfitting (đường train vẫn đi xuống nhưng đường test đã đi lên, khoảng cách giữa hai đường ngày càng lớn).

Đây là biểu hiện của sự đánh đổi **bias-variance** (*bias-variance tradeoff*):

- **Bias** (độ chệch) cao: mô hình giả định quá đơn giản, bỏ sót quy luật thật. Gây underfitting.
- **Variance** (phương sai) cao: mô hình quá nhạy với từng chi tiết của tập huấn luyện. Gây overfitting.
- Tăng độ phức tạp của mô hình làm bias giảm nhưng variance tăng. Mục tiêu là điểm cân bằng cho sai số trên dữ liệu mới nhỏ nhất.

*Chú ý:* sai số trên tập huấn luyện **không** phản ánh chất lượng thật của mô hình. Phải đo trên dữ liệu mô hình **chưa từng thấy** (tập kiểm tra).

**Regularization (chính quy hoá):** là kỹ thuật chống overfitting bằng cách **cộng thêm một số hạng phạt vào hàm mất mát** theo độ lớn của các trọng số `w`, để mô hình không dùng các trọng số quá lớn nhằm bám theo từng chi tiết của dữ liệu huấn luyện:

```
Loss_mới = Loss_dữ_liệu + λ · R(w)
```

| Loại | `R(w)` | Tác dụng |
|---|---|---|
| **L2** (Ridge, weight decay) | `Σ wᵢ²` | **Co nhỏ** các trọng số về gần 0 nhưng hiếm khi bằng đúng 0 |
| **L1** (Lasso) | `Σ │wᵢ│` | Có thể đưa nhiều trọng số về **đúng 0**, tức loại bỏ đặc trưng (chọn đặc trưng tự động) |

`λ` (≥ 0) là **siêu tham số** điều chỉnh độ mạnh của hình phạt: `λ = 0` là không chính quy hoá (dễ overfitting), `λ` quá lớn ép mô hình quá đơn giản (underfitting). Giống `k` trong k-NN, `λ` được chọn trên **tập kiểm định**.

#### 9.2.3 Chia dữ liệu và đánh giá mô hình

**Chia dữ liệu:**

| Tập | Vai trò | Tỉ lệ tham khảo |
|---|---|---|
| **Huấn luyện** (train) | Học tham số của mô hình | ~60-80% |
| **Kiểm định** (validation) | Chọn siêu tham số, so sánh mô hình | ~10-20% |
| **Kiểm tra** (test) | Đánh giá cuối cùng, chỉ dùng **một lần** khi đã chọn xong mô hình | ~10-20% |

Các khoảng trên chỉ là tham khảo và **ba tỉ lệ phải cộng lại đúng 100%**. Hai cách chia thường gặp: **70% / 15% / 15%** (ví dụ 1000 mẫu → 700 train, 150 validation, 150 test) hoặc **80% / 10% / 10%** (1000 mẫu → 800 train, 100 validation, 100 test).

*Chú ý:* đừng nhầm **tập kiểm định (validation)** với **tập kiểm tra (test)**. Tập kiểm định được dùng **nhiều lần** trong lúc phát triển (để chỉnh `k`, `λ`, so sánh mô hình), còn tập kiểm tra **chỉ dùng một lần** ở cuối để báo cáo chất lượng cuối cùng.

- Nếu dữ liệu ít, dùng **kiểm định chéo** (**k-fold cross-validation**): chia dữ liệu thành `k` phần, lần lượt dùng mỗi phần làm tập kiểm định, các phần còn lại để huấn luyện, rồi lấy trung bình kết quả.
- **Rò rỉ dữ liệu** (data leakage): thông tin từ tập kiểm tra (test) lọt vào quá trình huấn luyện hay chọn mô hình làm kết quả đẹp một cách giả tạo. Lỗi thường gặp nhất là chỉnh siêu tham số trực tiếp trên tập kiểm tra (test) thay vì trên tập kiểm định (validation).

**Bốn loại kết quả của bài toán phân loại hai lớp:**

Quy ước: **"dương" (positive) là lớp mà ta quan tâm cần phát hiện** (ví dụ: email *là spam*, bệnh nhân *có bệnh*); lớp còn lại là "âm" (negative). Chữ cái sau (P/N) là **dự đoán** của mô hình, chữ cái đầu (T/F) cho biết dự đoán đó **đúng hay sai**.

Lấy ví dụ bộ lọc spam thử trên 100 email (60 email thật sự là spam, 40 email hợp lệ):

| Ký hiệu | Tên | Thực tế | Dự đoán | Ý nghĩa | Số email trong ví dụ |
|---|---|---|---|---|---|
| **TP** | True positive | Dương (spam) | Dương (spam) | Spam được **bắt đúng** | 40 |
| **FN** | False negative | Dương (spam) | Âm (không spam) | Spam bị **bỏ sót** | 20 |
| **FP** | False positive | Âm (hợp lệ) | Dương (spam) | **Báo động nhầm**: email hợp lệ bị đánh dấu là spam | 10 |
| **TN** | True negative | Âm (hợp lệ) | Âm (không spam) | Email hợp lệ được **cho qua đúng** | 30 |

Bảng nhầm lẫn (**confusion matrix**) tổng hợp bốn giá trị này, dùng đúng các định nghĩa ở trên:

|  | Dự đoán dương | Dự đoán âm |
|---|---|---|
| **Thật sự dương** | TP (true positive) = 40 | FN (false negative) = 20 |
| **Thật sự âm** | FP (false positive) = 10 | TN (true negative) = 30 |

**Hai loại lỗi có cái giá khác nhau tuỳ bài toán:**

- **Lọc spam:** **FP** (email hợp lệ bị đưa vào hộp thư rác) thường tệ hơn **FN**, vì người dùng có thể **mất một email quan trọng**, còn bỏ sót vài thư rác chỉ gây phiền. Ta ưu tiên **precision** cao.
- **Sàng lọc bệnh** (dương = có bệnh): **FN** (bỏ sót bệnh nhân) thường tệ hơn **FP**, vì người bệnh **không được điều trị kịp thời**, còn báo nhầm chỉ dẫn đến xét nghiệm thêm. Ta ưu tiên **recall** cao.

Đây chính là lý do cần cả **precision** (phạt FP) lẫn **recall** (phạt FN), thay vì chỉ dùng accuracy.

**Độ đo đánh giá** (TP, FP, FN, TN theo định nghĩa trên):

| Loại bài toán | Độ đo | Công thức / ý nghĩa |
|---|---|---|
| Hồi quy | **MSE** (Mean Squared Error) | `MSE = (1/n) · Σ (yᵢ − ŷᵢ)²` |
| Phân loại | **Accuracy** (độ chính xác) | `(TP + TN) / (TP + TN + FP + FN)`: tỉ lệ dự đoán đúng trên tổng số mẫu |
| Phân loại | **Precision** | `TP / (TP + FP)`: trong số dự đoán "dương", bao nhiêu đúng |
| Phân loại | **Recall** (sensitivity) | `TP / (TP + FN)`: trong số thật sự "dương", bắt được bao nhiêu |
| Phân loại | **F1-score** | `2 · P · R / (P + R)`: trung bình điều hoà của precision và recall |

*Ví dụ tính tay:* bộ lọc spam ở trên có `TP = 40`, `FP = 10`, `FN = 20`, `TN = 30`.

```
Accuracy  = (40 + 30) / 100 = 0.70
Precision = 40 / (40 + 10)   = 0.80    (cảnh báo spam thì 80% đúng)
Recall    = 40 / (40 + 20)   ≈ 0.667   (chỉ bắt được 2/3 số spam thật)
F1        = 2 · 0.8 · 0.667 / (0.8 + 0.667) ≈ 0.727
```

*Chú ý:* **accuracy có thể gây hiểu nhầm** khi dữ liệu mất cân bằng (imbalanced). Nếu 99% email là không spam, mô hình luôn đoán "không spam" đạt accuracy 99% nhưng recall bằng 0. Khi đó cần xét precision, recall, F1.

#### 9.2.4 Gradient descent

Ở mục 9.2.1 ta nói "học là cực tiểu hoá hàm mất mát". **Gradient descent** (hạ gradient) là cách phổ biến nhất để làm việc đó, khi hàm mất mát `L(θ)` là hàm khả vi của các tham số `θ`:

- **Gradient** `∇L(θ)` là vector đạo hàm riêng của `L` theo từng tham số, chỉ hướng làm `L` **tăng nhanh nhất**. Vì vậy ta đi **ngược** hướng đó.
- Bắt đầu từ `θ` khởi tạo (thường ngẫu nhiên), lặp lại quy tắc cập nhật:

```
θ ← θ − η · ∇L(θ)
```

- `η` (eta) là **tốc độ học** (learning rate), một **siêu tham số**: quá nhỏ thì hội tụ rất chậm, quá lớn thì bước nhảy vượt qua điểm cực tiểu và **phân kỳ**.
- Thực tế thường dùng **mini-batch / stochastic gradient descent (SGD)**: mỗi bước chỉ tính gradient trên một phần nhỏ của dữ liệu huấn luyện để nhanh hơn.

*Ví dụ tính tay:* cực tiểu hoá `L(θ) = (θ − 3)²` (cực tiểu tại `θ = 3`), có `∇L(θ) = 2(θ − 3)`, khởi tạo `θ₀ = 0`.

| Bước | `η = 0.1`: `θ` | `η = 0.1`: `L(θ)` | `η = 1.1`: `θ` | `η = 1.1`: `L(θ)` |
|---|---|---|---|---|
| 0 | 0.000 | 9.000 | 0.000 | 9.000 |
| 1 | 0.600 | 5.760 | 6.600 | 12.960 |
| 2 | 1.080 | 3.686 | −1.320 | 18.662 |
| 3 | 1.464 | 2.359 | 8.184 | 26.874 |
| 4 | 1.771 | 1.510 | −3.221 | 38.698 |

Với `η = 0.1`, `θ` tiến dần về 3 và `L` giảm đều (mỗi bước `θ` cách 3 một khoảng bằng 0.8 lần bước trước). Với `η = 1.1`, `θ` nhảy qua lại quanh 3 với biên độ tăng dần, `L` tăng: đây là phân kỳ do tốc độ học quá lớn.

*Chú ý:* với hàm mất mát nhiều cực tiểu địa phương (như mạng nơ-ron), gradient descent chỉ đảm bảo tìm cực tiểu **địa phương**, giống vấn đề kẹt cực trị địa phương của leo đồi đã nhắc ở mục 7.9. Mạng nơ-ron tính gradient bằng **lan truyền ngược** (chương 11).

### 9.3 Các loại giải thuật học

Các loại học phân biệt chủ yếu theo **loại tín hiệu / phản hồi** mà thuật toán nhận được trong lúc học.

| Loại học | Tiếng Anh | Dữ liệu / phản hồi | Bài toán điển hình |
|---|---|---|---|
| **Có giám sát** | Supervised learning | Có **nhãn** cho mọi mẫu | Phân loại, hồi quy |
| **Không giám sát** | Unsupervised learning | **Không** có nhãn | Phân cụm, giảm chiều |
| **Bán giám sát** | Semi-supervised learning | **Ít** mẫu có nhãn + **nhiều** mẫu không nhãn | Phân loại khi gắn nhãn tốn kém |
| **Tăng cường** | Reinforcement learning (RL) | Phần thưởng/phạt từ **môi trường** sau mỗi hành động | Chơi game, điều khiển robot |
| **Chuyển đổi** | Transductive learning | Dữ liệu huấn luyện + dữ liệu kiểm tra (test, không nhãn) có sẵn | Dự đoán trực tiếp cho tập kiểm tra cho trước |
| **Học cách học** | Meta-learning (learning to learn) | Kinh nghiệm từ **nhiều bài toán học** | Thích nghi nhanh với bài toán mới |

*Chú ý:* ngoài các loại trên còn có **học tự giám sát** (self-supervised learning): nhãn được **tạo tự động từ chính dữ liệu** (ví dụ che một từ trong câu rồi bắt mô hình đoán lại), nên không cần người gắn nhãn. Nó thường dùng để huấn luyện trước các mô hình lớn, xem mục 9.6.

#### 9.3.1 Học có giám sát

- Thuật toán tạo ra **một hàm ánh xạ dữ liệu vào tới kết quả mong muốn** (`f: x → y`) từ các cặp `(x, y)` đã có.
- **Phát biểu chuẩn** là bài toán **phân loại** (classification): chương trình học (cách xấp xỉ biểu hiện của) một hàm ánh xạ một **vector** tới một vài **lớp** bằng cách xem xét một số mẫu dữ liệu - kết quả của hàm đó.

Hai dạng chính, phân biệt theo kiểu của nhãn `y`:

| | Phân loại (Classification) | Hồi quy (Regression) |
|---|---|---|
| Nhãn `y` | **Rời rạc** (tập lớp hữu hạn) | **Liên tục** (số thực) |
| Ví dụ | Email là spam hay không; ảnh là chó hay mèo | Dự đoán giá nhà, nhiệt độ ngày mai |
| Độ đo thường dùng | Accuracy, precision, recall, F1 | MSE, MAE |

#### 9.3.2 Học không giám sát

- **Mô hình hoá một tập dữ liệu**, **không có sẵn** các ví dụ đã được gắn nhãn: thuật toán tự tìm cấu trúc ẩn trong dữ liệu.
- Các bài toán chính:
  - **Phân cụm** (clustering): gom các mẫu giống nhau thành nhóm, ví dụ **K-means** (chương 10).
  - **Giảm chiều** (dimensionality reduction): biểu diễn dữ liệu bằng ít đặc trưng hơn, ví dụ **PCA** (Principal Component Analysis).
  - **Phát hiện bất thường** (anomaly detection): tìm mẫu khác thường.
  - **Luật kết hợp** (association rule learning): tìm các mục hay xuất hiện cùng nhau.

#### 9.3.3 Học bán giám sát

- **Kết hợp** các ví dụ có gắn nhãn và không gắn nhãn để sinh một hàm hoặc một bộ phân loại thích hợp.
- Động cơ: **gắn nhãn thường tốn kém** (cần chuyên gia), còn dữ liệu không nhãn thì rẻ và nhiều. Ví dụ: có hàng triệu ảnh y khoa nhưng chỉ vài trăm ảnh được bác sĩ chẩn đoán.

#### 9.3.4 Học tăng cường

- Thuật toán học **cách hành động** tuỳ theo các **quan sát về thế giới**.
- Mỗi hành động đều **có tác động tới môi trường**, và môi trường cung cấp **thông tin phản hồi** (phần thưởng hoặc phạt) để **hướng dẫn** thuật toán của quá trình học.

```
        hành động (action)
   ┌───────────────────────→
Tác nhân (agent)         Môi trường (environment)
   ←───────────────────────┘
   trạng thái (state) + phần thưởng (reward)
```

- Khác học có giám sát ở chỗ **không có đáp án đúng cho từng bước**, chỉ có phần thưởng (thường đến muộn) cho cả chuỗi hành động. Do đó phải cân bằng **khám phá** (exploration) và **khai thác** (exploitation), giống vấn đề đã gặp ở chương 7 (mục 7.3).
- Thuật toán tiêu biểu: **Q-learning**, **Policy Gradient**, **Deep Q-Network (DQN)**. Ứng dụng: AlphaGo, robot, xe tự lái, huấn luyện chatbot qua phản hồi của người dùng (RLHF).
- Liên hệ mục 3.3 (tìm kiếm trên cây trò chơi: minimax, alpha-beta): ở đó máy chơi cờ dựa trên **hàm đánh giá do người thiết kế**, còn học tăng cường cho phép máy **tự học** chiến lược qua các ván chơi.

#### 9.3.5 Học chuyển đổi

- **Tương tự học có giám sát** nhưng **không xây dựng hàm một cách rõ ràng**.
- Thay vì thế, cố gắng **đoán kết quả mới** dựa vào các dữ liệu huấn luyện, kết quả huấn luyện, và **dữ liệu thử nghiệm có sẵn** trong quá trình huấn luyện.
- Khác biệt với học quy nạp (inductive learning, tức học có giám sát thông thường: học hàm tổng quát `f` rồi áp dụng cho mọi dữ liệu): học chuyển đổi chỉ quan tâm dự đoán cho **đúng tập mẫu kiểm tra (test) cụ thể đã biết**, không cần mô hình tổng quát.

*Chú ý:* đừng nhầm **học chuyển đổi** (*transductive learning*) với **học chuyển giao** (*transfer learning*). Học chuyển giao là **dùng lại mô hình đã huấn luyện cho bài toán A làm điểm xuất phát cho bài toán B** (ví dụ lấy mạng nhận dạng ảnh đã học trên hàng triệu ảnh rồi tinh chỉnh bằng vài trăm ảnh y khoa), giúp học nhanh hơn với ít dữ liệu hơn. Hai khái niệm có tên dịch gần giống nhau nhưng **khác hẳn nhau**: một bên nói về *cách suy luận trên tập kiểm tra (test)*, bên kia nói về *tái sử dụng tri thức giữa hai bài toán*. Học chuyển giao là kỹ thuật rất phổ biến với mạng nơ-ron (chương 11) và các mô hình ngôn ngữ lớn (mục 9.6).

#### 9.3.6 Học cách học

- Thuật toán **học thiên kiến quy nạp** (inductive bias) **của chính mình**, dựa theo các **kinh nghiệm đã gặp**.
- **Inductive bias** là những giả định mà thuật toán dùng để suy ra kết quả cho dữ liệu chưa thấy (ví dụ k-NN giả định "các mẫu gần nhau thì cùng lớp"). Meta-learning cố gắng tự chọn hay điều chỉnh các giả định này sao cho học bài toán mới nhanh hơn, với ít dữ liệu hơn (liên quan **few-shot learning** và **AutoML**).

### 9.4 Các chủ đề và kỹ thuật học máy

Phân loại theo nội dung bài giảng, gồm ba nhóm: **(1)** hồi quy và phân loại, tức mô hình hoá **hàm mật độ xác suất có điều kiện** `P(y | x)` (dự đoán `y` khi biết `x`); **(2)** các **mô hình phát sinh** (mô hình hoá cách dữ liệu được sinh ra); **(3)** các **kỹ thuật suy luận xấp xỉ**. Cột đầu của mỗi bảng ghi theo dạng **`Tiếng Việt - Tiếng Anh`** (tên tiếng Anh dùng để tra cứu).

**Nhóm 1: Hồi quy và phân loại (mô hình hoá `P(y | x)`)**

*Chú ý:* tiêu đề "mô hình hoá `P(y | x)`" theo cách phân nhóm của bài giảng và được hiểu theo **nghĩa rộng**. Không phải kỹ thuật nào trong nhóm cũng xuất ra xác suất: SVM và perceptron học một **hàm quyết định / ranh giới phân lớp** `x → y` (cho nhãn hoặc điểm số), k-NN cho nhãn bằng bỏ phiếu; trong khi hồi quy logistic hay mạng nơ-ron với đầu ra softmax cho xác suất thật sự.

| Kỹ thuật (Tiếng Việt - Tiếng Anh) | Ý tưởng chính | Liên hệ |
|---|---|---|
| **Hồi quy tuyến tính - Linear Regression** | Dự đoán giá trị liên tục bằng một hàm tuyến tính `ŷ = w·x + b`; chọn `w`, `b` làm **MSE** nhỏ nhất | Mô hình cơ bản nhất cho **hồi quy**; huấn luyện bằng gradient descent (mục 9.2.4); thêm phạt L2/L1 thành Ridge/Lasso (mục 9.2.2) |
| **Hồi quy logistic - Logistic Regression** | Dù tên là "hồi quy", đây là phương pháp **phân loại**: `P(y = 1 \| x) = σ(w·x + b)` với `σ(z) = 1 / (1 + e⁻ᶻ)`, dự đoán lớp 1 khi xác suất > 0.5 | Cho **xác suất** thật sự; ranh giới tuyến tính; gần với một nơ-ron dùng hàm sigmoid (chương 11) |
| **Mạng nơ-ron - Artificial Neural Network (ANN)** | Nhiều nơ-ron nối thành lớp, học trọng số bằng lan truyền ngược (backpropagation) | Chương 11; nền tảng của **Deep Learning** |
| **Cây quyết định - Decision Tree** | Chuỗi câu hỏi "đặc trưng nào, ngưỡng nào" tạo thành cây; mỗi lá là một lớp/giá trị | Thuật toán **ID3**, **C4.5**, **CART**; đo bằng **entropy / information gain**, **Gini** |
| **Lập trình biểu thức gen - Gene Expression Programming (GEP)** | Tiến hoá chương trình biểu diễn bằng chuỗi gen độ dài cố định, giải mã thành cây biểu thức | Biến thể của GP (chương 7) |
| **Lập trình di truyền - Genetic Programming (GP)** | Tiến hoá chính **chương trình/biểu thức** (biểu diễn bằng cây) bằng chọn lọc, lai ghép, đột biến | Mục 7.5.4 |
| **Hồi quy quá trình Gauss - Gaussian Process Regression (GPR)** | Coi hàm cần học là một **quá trình ngẫu nhiên Gauss**, cho cả dự đoán lẫn **độ bất định** | Dùng nhiều trong tối ưu Bayes (Bayesian optimization) |
| **Phân tích biệt thức tuyến tính - Linear Discriminant Analysis (LDA)** | Tìm hướng chiếu tuyến tính làm các lớp tách nhau nhất. Khi dùng để phân loại, LDA là **mô hình phát sinh**: giả định mỗi lớp có phân phối Gauss với **cùng ma trận hiệp phương sai**, rồi dùng quy tắc Bayes, kết quả là ranh giới quyết định tuyến tính | Vừa phân loại vừa giảm chiều; **không phải** phương pháp phân biệt thuần tuý dù có ranh giới tuyến tính (đừng nhầm với LDA = Latent Dirichlet Allocation) |
| **k láng giềng gần nhất - k-Nearest Neighbors (k-NN)** | Lớp của mẫu mới = lớp **đa số** trong `k` mẫu huấn luyện **gần nhất** | Mục 9.5 |
| **Độ dài thông điệp tối thiểu - Minimum Message Length (MML)** | Mô hình tốt là mô hình cho **tổng độ dài mã hoá (mô hình + dữ liệu) ngắn nhất** | Gần với **MDL** (Minimum Description Length); hiện thực hoá **dao cạo Occam** |
| **Cảm tri nguyên - Perceptron** | Một nơ-ron đơn: tổng có trọng số của đầu vào rồi qua hàm ngưỡng, **phân loại tuyến tính** | "Viên gạch" của mạng nơ-ron (chương 11) |
| **Hàm cơ sở xuyên tâm - Radial Basis Function (RBF) network** | Tổ hợp tuyến tính các hàm phụ thuộc **khoảng cách tới các tâm** (thường dạng Gauss) | Mạng nơ-ron một lớp ẩn dùng RBF |
| **Máy vector hỗ trợ - Support Vector Machine (SVM)** | Tìm **siêu phẳng** phân chia hai lớp với **lề (margin) lớn nhất**; dùng **kernel trick** để xử lý dữ liệu không tách tuyến tính | Rất mạnh với dữ liệu vừa và nhỏ |

**Nhóm 2: Mô hình hoá hàm mật độ xác suất qua mô hình phát sinh** (generative models, mô hình hoá cách dữ liệu được **sinh ra**, tức `P(x)` hoặc `P(x, y)`)

| Kỹ thuật (Tiếng Việt - Tiếng Anh) | Ý tưởng chính |
|---|---|
| **Thuật toán cực đại kỳ vọng - Expectation-Maximization (EM)** | Ước lượng tham số khi có **biến ẩn**: lặp bước **E** (ước lượng biến ẩn) và bước **M** (cực đại hoá tham số). Dùng trong **Gaussian Mixture Model** (phân cụm mềm) |
| **Các mô hình đồ hoạ: mạng Bayes - Bayesian network (Bayes net)** | Đồ thị có hướng không chu trình; mỗi nút là biến ngẫu nhiên, cạnh biểu diễn **phụ thuộc có điều kiện** |
| **Các mô hình đồ hoạ: mạng Markov - Markov network / Markov Random Field (MRF)** | Đồ thị **vô hướng** biểu diễn phụ thuộc giữa các biến |

> Ghi nhớ: **mô hình phân biệt** (discriminative) học trực tiếp **hàm quyết định** `x → y` hoặc `P(y | x)`, **không** mô hình hoá cách `x` được sinh ra (ví dụ: SVM và perceptron học ranh giới/hàm quyết định; hồi quy logistic, mạng nơ-ron softmax học `P(y | x)`). **Mô hình phát sinh** (generative) học `P(x, y)` (hay `P(x | y)` và `P(y)`) rồi dùng quy tắc Bayes để suy ra `P(y | x)` (ví dụ: LDA, naive Bayes). Mô hình phát sinh còn có thể **sinh dữ liệu mới**, nền tảng của AI tạo sinh (generative AI).

**Nhóm 3: Các kỹ thuật suy luận xấp xỉ đúng** (approximate inference, dùng khi tính xác suất chính xác quá tốn kém)

| Kỹ thuật (Tiếng Việt - Tiếng Anh) | Ý tưởng chính |
|---|---|
| **Chuỗi Markov phương pháp Monte Carlo - Markov Chain Monte Carlo (MCMC)** | **Lấy mẫu** từ phân phối phức tạp bằng cách chạy một chuỗi Markov hội tụ về phân phối đó (ví dụ **Metropolis-Hastings**, **Gibbs sampling**) |
| **Phương pháp biến thiên - Variational methods (Variational Inference)** | Xấp xỉ phân phối phức tạp bằng một phân phối **đơn giản hơn**, biến bài toán suy luận thành bài toán **tối ưu** |

**Bản đồ tổng hợp: kỹ thuật nào thuộc loại học nào**

| Kỹ thuật | Học có giám sát | Học không giám sát | Ghi chú |
|---|:---:|:---:|---|
| Hồi quy tuyến tính, hồi quy logistic | ✔ | | Hồi quy / phân loại cơ bản |
| Mạng nơ-ron, Cây quyết định, SVM, k-NN, Perceptron, RBF, LDA | ✔ | | Mạng nơ-ron còn dùng cho học không giám sát (autoencoder) và học tăng cường |
| Hồi quy quá trình Gauss (GPR) | ✔ | | Hồi quy có kèm độ bất định |
| Lập trình di truyền (GP), GEP | ✔ | | Thường dùng cho hồi quy/phân loại bằng tiến hoá |
| K-means | | ✔ | Chương 10 |
| EM (Gaussian Mixture) | | ✔ | Phân cụm mềm |
| Mạng Bayes, mạng Markov | ✔ | ✔ | Cả **cấu trúc** lẫn **tham số** đều có thể học **có nhãn** (ví dụ naive Bayes) hoặc **không nhãn** (ví dụ dùng EM với biến ẩn), tuỳ cách dùng |

*Chú ý:* ba kỹ thuật **cố ý không có mặt** trong bản đồ vì chúng không phải một "loại học":

- **MCMC** và **phương pháp biến thiên** là **công cụ suy luận xấp xỉ** (Nhóm 3), được dùng *bên trong* nhiều mô hình xác suất, bất kể mô hình đó học có hay không có giám sát.
- **MML** là một **nguyên lý chọn mô hình** (mô hình nào mô tả dữ liệu ngắn gọn nhất), áp dụng được cho cả hai loại học.

### 9.5 Ví dụ minh hoạ: phân loại bằng k láng giềng gần nhất

Phần này minh hoạ khái niệm **học có giám sát**, **siêu tham số** và **overfitting** bằng thuật toán đơn giản nhất: k-NN. Số liệu nhỏ để tính tay được.

**Ý tưởng:** k-NN không "huấn luyện" gì cả (còn gọi là **lazy learning**, học lười): chỉ **lưu** tập huấn luyện. Khi có mẫu mới `x`:

1. Tính **khoảng cách** từ `x` tới mọi mẫu huấn luyện (thường dùng khoảng cách **Euclid**: `d(a, b) = √( Σ (aᵢ − bᵢ)² )`).
2. Lấy `k` mẫu **gần nhất**.
3. **Bỏ phiếu đa số**: lớp xuất hiện nhiều nhất trong `k` mẫu đó là lớp dự đoán.

*Chú ý:* vì không huấn luyện nên **toàn bộ chi phí chuyển sang lúc suy luận**: mỗi truy vấn phải tính khoảng cách tới cả `n` mẫu có `d` đặc trưng, tức **O(n·d)** (cộng thêm chi phí sắp xếp hoặc chọn `k` nhỏ nhất), chậm khi `n` lớn. Ngoài ra, k-NN chịu **lời nguyền số chiều** (*curse of dimensionality*): khi số đặc trưng `d` rất lớn, khoảng cách giữa các điểm trở nên **gần như bằng nhau** nên khái niệm "gần nhất" mất ý nghĩa và k-NN dự đoán kém đi; khi đó cần giảm chiều (ví dụ PCA, mục 9.3.2) hoặc chọn bớt đặc trưng.

**Dữ liệu huấn luyện** (2 đặc trưng, 2 lớp):

| Mẫu | Đặc trưng `(x₁, x₂)` | Lớp |
|---|---|---|
| A | (1, 1) | đỏ |
| B | (2, 1) | đỏ |
| C | (1, 2) | đỏ |
| D | (5, 5) | xanh |
| E | (6, 5) | xanh |
| F | (5, 6) | xanh |
| N | (2, 2) | xanh |

Mẫu `N` nằm giữa vùng "đỏ" nhưng mang nhãn xanh: đây là **mẫu nhiễu** (có thể do gắn nhãn sai). Cần dự đoán lớp của điểm mới `q = (3, 2)`.

**Bước 1: khoảng cách từ `q` tới từng mẫu**

| Mẫu | Phép tính | Khoảng cách | Hạng |
|---|---|---|---|
| N (2, 2) | `√((3−2)² + (2−2)²) = √1` | 1.000 | 1 |
| B (2, 1) | `√(1 + 1) = √2` | 1.414 | 2 |
| C (1, 2) | `√(4 + 0) = √4` | 2.000 | 3 |
| A (1, 1) | `√(4 + 1) = √5` | 2.236 | 4 |
| D (5, 5) | `√(4 + 9) = √13` | 3.606 | 5 |
| E (6, 5) | `√(9 + 9) = √18` | 4.243 | 6 |
| F (5, 6) | `√(4 + 16) = √20` | 4.472 | 7 |

**Bước 2: bỏ phiếu với các giá trị `k` khác nhau**

| `k` | `k` láng giềng gần nhất | Phiếu | Dự đoán |
|---|---|---|---|
| 1 | N | xanh: 1 | **xanh** |
| 3 | N, B, C | xanh: 1, đỏ: 2 | **đỏ** |
| 5 | N, B, C, A, D | xanh: 2, đỏ: 3 | **đỏ** |
| 7 | N, B, C, A, D, E, F (cả tập huấn luyện) | xanh: 4 (D, E, F, N), đỏ: 3 (A, B, C) | **xanh** |

**Nhận xét:**

- Với `k = 1`, mô hình bị **mẫu nhiễu N** kéo lệch: dự đoán "xanh" dù `q` rõ ràng nằm trong vùng đỏ. Đây là dạng **overfitting** (mô hình bám theo cả nhiễu, **variance cao**).
- Tăng `k` giúp "làm mịn" ranh giới quyết định, chống nhiễu tốt hơn. Nhưng `k` quá lớn thì mô hình **underfitting**: với `k = 7` (bằng cả tập huấn luyện, `n = 7`), bỏ phiếu cho **xanh 4 : đỏ 3** dù `q = (3, 2)` nằm ngay sát vùng đỏ. Dự đoán lúc này chỉ phản ánh **lớp đa số của toàn tập** và **bỏ qua vị trí** của `q`: đúng là biểu hiện của bias cao (mô hình quá đơn giản). Như vậy `k = 1` sai vì variance cao, `k = 7` sai vì bias cao, còn `k = 3` hoặc `5` cho kết quả hợp lý.
- `k` là **siêu tham số**: chọn bằng **tập kiểm định (validation)** hoặc **cross-validation**, không chọn bằng tập kiểm tra (test).
- Khi hai lớp có số phiếu bằng nhau, cần quy tắc phá hoà (chọn `k` lẻ cho bài toán hai lớp, hoặc chọn lớp có láng giềng gần nhất).
- Vì dựa trên khoảng cách, các đặc trưng cần được **chuẩn hoá** (scaling) về cùng thang đo, nếu không đặc trưng có đơn vị lớn sẽ lấn át các đặc trưng khác.

**Cài đặt Python** (chỉ dùng thư viện chuẩn; cần **Python 3.8 trở lên** vì dùng `math.dist`):

```python
import math
from collections import Counter

TRAIN = [
    ((1, 1), "đỏ"),
    ((2, 1), "đỏ"),
    ((1, 2), "đỏ"),
    ((5, 5), "xanh"),
    ((6, 5), "xanh"),
    ((5, 6), "xanh"),
    ((2, 2), "xanh"),  # mẫu nhiễu
]


def knn_predict(x, train, k):
    # sắp xếp các mẫu huấn luyện theo khoảng cách Euclid tới x
    ranked = sorted(train, key=lambda s: math.dist(x, s[0]))
    # bỏ phiếu đa số trong k mẫu gần nhất
    votes = Counter(label for _, label in ranked[:k])
    return votes.most_common(1)[0][0], ranked[:k]


if __name__ == "__main__":
    q = (3, 2)
    for k in (1, 3, 5, 7):
        label, neighbors = knn_predict(q, TRAIN, k)
        print(k, label, [(p, round(math.dist(q, p), 3)) for p, _ in neighbors])
```

Kết quả khi chạy (khớp với bảng tính tay ở trên):

```
1 xanh [((2, 2), 1.0)]
3 đỏ [((2, 2), 1.0), ((2, 1), 1.414), ((1, 2), 2.0)]
5 đỏ [((2, 2), 1.0), ((2, 1), 1.414), ((1, 2), 2.0), ((1, 1), 2.236), ((5, 5), 3.606)]
7 xanh [((2, 2), 1.0), ((2, 1), 1.414), ((1, 2), 2.0), ((1, 1), 2.236), ((5, 5), 3.606), ((6, 5), 4.243), ((5, 6), 4.472)]
```

*Chú ý về cách phá hoà:* hàm `sorted` của Python là **ổn định** (*stable*): hai mẫu có khoảng cách **bằng nhau** giữ nguyên thứ tự xuất hiện trong `TRAIN`, nên mẫu đứng trước trong `TRAIN` được xếp gần hơn. Tương tự, khi hai lớp hoà phiếu, `Counter.most_common` trả về lớp **được gặp đầu tiên**, tức lớp của láng giềng gần nhất. Kết quả vì vậy **phụ thuộc thứ tự dữ liệu** khi có hoà.

*Chú ý:* nếu chạy trên Windows và gặp lỗi `UnicodeEncodeError` khi in tiếng Việt, đặt biến môi trường `PYTHONIOENCODING=utf-8` trước khi chạy.

**Thử thay đổi để hiểu thêm:**

| Thử | Quan sát cần kiểm tra |
|---|---|
| Xoá mẫu nhiễu `N` khỏi `TRAIN` | `k = 1` có còn dự đoán sai không? |
| Dự đoán điểm `(4, 4)` với `k = 1, 3, 5` | Điểm nằm giữa hai vùng, kết quả thay đổi thế nào theo `k`? |
| Nhân đặc trưng `x₂` lên 100 lần | Khoảng cách bị đặc trưng nào chi phối? Vì sao cần chuẩn hoá? |
| Dùng thư viện `scikit-learn` (`KNeighborsClassifier`) | So sánh kết quả với bản tự cài đặt |

### 9.6 Các ứng dụng

| Ứng dụng | Tiếng Anh | Mô tả ngắn | Kỹ thuật thường dùng |
|---|---|---|---|
| **Máy cảm giác** | Machine perception | Máy thu nhận, diễn giải dữ liệu từ cảm biến (hình ảnh, âm thanh, xúc giác) | Mạng nơ-ron, xử lý tín hiệu |
| **Thị giác máy tính** | Computer Vision | Hiểu ảnh/video: phân loại ảnh, nhận diện khuôn mặt, phát hiện vật thể | Mạng nơ-ron tích chập (CNN) |
| **Xử lý ngôn ngữ tự nhiên** | Natural Language Processing (NLP) | Hiểu và sinh ngôn ngữ: dịch máy, phân tích cảm xúc, tóm tắt | Transformer, mô hình ngôn ngữ |
| **Máy tìm kiếm** | Search engine | Xếp hạng kết quả, gợi ý truy vấn, hiểu ý định người dùng | Learning to rank |
| **Tin sinh học** | Bioinformatics | Phân tích chuỗi DNA/protein, dự đoán cấu trúc protein, tìm thuốc | Mô hình xác suất, mạng nơ-ron |
| **Phân tích thị trường chứng khoán** | Stock market analysis | Dự đoán xu hướng giá, phát hiện giao dịch bất thường | Hồi quy, chuỗi thời gian |
| **Nhận dạng tiếng nói, chữ viết** | Speech / Handwriting recognition | Chuyển giọng nói thành văn bản, ảnh chữ viết tay thành văn bản | Mạng nơ-ron, mô hình Markov ẩn (HMM) |
| **Nhận dạng vật thể** | Object recognition | Xác định vật thể nào có trong ảnh và ở đâu | CNN |
| **Mô hình ngôn ngữ lớn** (ChatGPT) | Large Language Model (LLM) | Mạng nơ-ron rất lớn học từ lượng văn bản khổng lồ để sinh ngôn ngữ | Transformer, học tự giám sát (self-supervised), RLHF |

*Chú ý:* mô hình ngôn ngữ lớn thường được huấn luyện trước bằng **học tự giám sát** (self-supervised learning: nhãn được tạo tự động từ chính dữ liệu, ví dụ đoán từ tiếp theo), sau đó tinh chỉnh bằng học có giám sát và học tăng cường. Các loại học ở mục 9.3 vì vậy thường được **kết hợp** trong một hệ thống thực tế.

### 9.7 Tổng kết

| Nội dung | Ý chính |
|---|---|
| **Học máy là gì** | Cho máy **học từ dữ liệu** thay vì lập trình quy tắc rõ ràng (Samuel); hiệu năng P trên nhiệm vụ T tăng theo kinh nghiệm E (Mitchell) |
| **Mục tiêu cốt lõi** | **Khái quát hoá**: làm tốt trên dữ liệu **chưa từng thấy**, không chỉ thuộc lòng tập huấn luyện |
| **Phân biệt lĩnh vực** | Gần với suy diễn thống kê; khác khai phá dữ liệu ở mục tiêu (dự đoán và khám phá tri thức mới) |
| **Các loại học** | Có giám sát, không giám sát, bán giám sát, tăng cường, chuyển đổi, học cách học (cùng học tự giám sát; đừng nhầm học chuyển đổi với học chuyển giao) |
| **Có giám sát** | Học hàm `x → y`; **phân loại** (nhãn rời rạc) và **hồi quy** (nhãn liên tục) |
| **Rủi ro chính** | **Overfitting** / **underfitting**; đánh giá trên tập kiểm tra (test) tách biệt, chọn siêu tham số trên tập kiểm định (validation), dùng cross-validation; chống overfitting bằng regularization (L1/L2) |
| **Cách học** | Cực tiểu hoá hàm mất mát, thường bằng **gradient descent** `θ ← θ − η·∇L(θ)` với tốc độ học `η` là siêu tham số |
| **Kỹ thuật chính** | Hồi quy tuyến tính/logistic, mạng nơ-ron, cây quyết định, SVM, k-NN, perceptron, LDA, GP/GEP, Gaussian process, EM, mạng Bayes/Markov, MCMC, variational |
| **Quy trình** | Xác định bài toán → thu thập và làm sạch dữ liệu → đặc trưng → huấn luyện → kiểm định → kiểm tra → triển khai và giám sát (lặp lại nhiều vòng) |
| **Con người và đạo đức** | Không thể loại bỏ hoàn toàn: chọn dữ liệu, đặc trưng, mô hình, siêu tham số; cần cảnh giác với thiên lệch dữ liệu, công bằng và quyền riêng tư |
| **Hướng tiếp theo** | Chương 10 (K-means: học không giám sát), chương 11 (Mạng nơ-ron nhân tạo) |

### 9.8 Từ khoá để tự tìm hiểu thêm

Các từ khoá tiếng Anh nên dùng khi tra cứu sách, bài báo hoặc khoá học:

| Chủ đề | Từ khoá tìm kiếm |
|---|---|
| Nền tảng | `machine learning basics`, `supervised vs unsupervised learning`, `bias-variance tradeoff`, `overfitting regularization`, `train validation test split`, `k-fold cross-validation`, `confusion matrix precision recall F1`, `gradient descent learning rate`, `L1 L2 regularization lasso ridge`, `machine learning workflow`, `data drift`, `algorithmic bias fairness` |
| Phân loại / hồi quy | `linear regression`, `logistic regression`, `decision tree ID3 entropy information gain`, `k-nearest neighbors`, `support vector machine kernel trick`, `perceptron learning rule`, `naive Bayes classifier` |
| Mô hình xác suất | `Bayesian network`, `expectation maximization Gaussian mixture`, `Markov chain Monte Carlo`, `variational inference`, `Gaussian process regression` |
| Tiến hoá | `genetic programming symbolic regression`, `gene expression programming` |
| Học tăng cường | `reinforcement learning Q-learning`, `Markov decision process`, `exploration vs exploitation` |
| Hiện đại | `deep learning`, `convolutional neural network`, `transformer attention`, `large language model`, `self-supervised learning`, `transfer learning` |
| Công cụ | `scikit-learn`, `NumPy`, `pandas`, `PyTorch`, `TensorFlow` |
| Tài liệu tham khảo | Tom Mitchell, *Machine Learning* (1997); Russell & Norvig, *Artificial Intelligence: A Modern Approach* (phần Learning); khoá *Machine Learning* của Andrew Ng (Coursera) |
