# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

*đây là các chương còn lại*

## Chapter 7: Tính toán tiến hoá (Evolutionary computing)

## Chapter 8: Thuật toán di truyền (Genetic algorithm)

- [ ] Cần cài đặt code

### Bài tập: giải TSP bằng GA

**Đề bài.** Cài đặt GA bằng **Python** (file `.py` hoặc notebook `.ipynb`) để giải bài toán người bán hàng với **10 thành phố** cho trước, dùng **mã hoá hoán vị**.

Tọa độ các thành phố (khoảng cách là khoảng cách Euclid, hành trình là chu trình khép kín):

| Thành phố | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| `x` | 60 | 180 | 80 | 140 | 20 | 100 | 200 | 140 | 40 | 100 |
| `y` | 200 | 200 | 180 | 180 | 160 | 160 | 160 | 140 | 120 | 120 |

**Mã khung** (hoàn thành các hàm có `NotImplementedError`):

```python
import math
import random

CITIES = [
    (60, 200),
    (180, 200),
    (80, 180),
    (140, 180),
    (20, 160),
    (100, 160),
    (200, 160),
    (140, 140),
    (40, 120),
    (100, 120),
]
N = len(CITIES)

POP, GENS, PC, PM, K, ELITE = 100, 300, 0.9, 0.2, 3, 2
OPTIMUM = 459.99


def dist(a, b):
    return math.dist(CITIES[a], CITIES[b])


def tour_length(tour):
    """Độ dài chu trình khép kín (đã cho sẵn)."""
    return sum(dist(tour[i], tour[(i + 1) % N]) for i in range(N))


def init_population():
    """Trả về POP hoán vị ngẫu nhiên của 0..N-1."""
    raise NotImplementedError


def tournament_select(pop):
    """Chọn giải đấu kích thước K: trả về cá thể có tour_length NHỎ nhất trong K cá thể ngẫu nhiên."""
    raise NotImplementedError


def order_crossover(p1, p2):
    """OX (mục 8.4.5): trả về MỘT con là hoán vị hợp lệ."""
    raise NotImplementedError


def swap_mutation(tour):
    """Với xác suất PM, hoán đổi 2 vị trí ngẫu nhiên. Không sửa tour gốc, trả về tour mới."""
    raise NotImplementedError


def run_ga(seed):
    """Chạy GA, bắt đầu bằng random.seed(seed). Trả về (độ dài tốt nhất, hoán vị tốt nhất)."""
    raise NotImplementedError


def main():
    lengths = [run_ga(seed)[0] for seed in range(20)]
    hits = sum(abs(L - OPTIMUM) < 0.01 for L in lengths)
    print("độ dài tốt nhất mỗi lần chạy:", [round(L, 2) for L in lengths])
    print(f"đạt tối ưu {hits}/20 lần")


if __name__ == "__main__":
    main()
```

**Yêu cầu bắt buộc:**

1. Cài đặt đủ 5 hàm trong mã khung, đúng chữ ký hàm.
2. **Mọi cá thể** ở mọi thế hệ phải là hoán vị hợp lệ của `0..N-1`. Hãy viết `assert sorted(t) == list(range(N))` để kiểm tra khi gỡ lỗi.
3. Dùng **elitism** với `ELITE` cá thể tốt nhất mỗi thế hệ.
4. Với cấu hình trong mã khung (`POP=100`, `GENS=300`, `PC=0.9`, `PM=0.2`, `K=3`, `ELITE=2`), chạy `main()` phải đạt tối ưu **ít nhất 15/20 lần**.
5. Vẽ **đường cong hội tụ** (độ dài tốt nhất theo từng thế hệ, một lần chạy) và viết nhận xét ngắn (3 đến 5 câu): GA hội tụ nhanh hay chậm, từ thế hệ nào gần như không cải thiện thêm.

**Mốc tham khảo để tự kiểm tra:** cố định thành phố 0 rồi vét cạn `9! = 362 880` hoán vị cho hành trình ngắn nhất dài **459.99**, ví dụ `0 → 2 → 5 → 3 → 1 → 6 → 7 → 9 → 8 → 4 → 0` (đảo chiều hoặc xoay vòng vẫn cùng độ dài). Nếu GA của bạn cho kết quả **ngắn hơn** 459.99, hàm tính độ dài hoặc tính hợp lệ của hoán vị đang có lỗi.

**Gợi ý:**

- Khởi tạo bằng `random.shuffle` trên `list(range(N))`.
- Với `order_crossover`, chọn hai điểm cắt `a < b` bằng `sorted(random.sample(range(N), 2))`; copy đoạn `p1[a:b+1]`, rồi lấy các phần tử của `p2` chưa có trong đoạn đó, điền vào các vị trí trống từ trái sang phải. Tham khảo ví dụ ở mục 8.4.5.
- Không dùng lai ghép cắt-ghép thông thường cho hoán vị.
- Kết quả của GA mang tính **ngẫu nhiên**: luôn so sánh trên nhiều `seed`.

**Câu hỏi lý thuyết (trả lời ngắn):**

1. Vì sao lai ghép một điểm cắt thông thường trên hoán vị có thể sinh lời giải không hợp lệ? Cho ví dụ với `[1,2,3,4]` và `[3,4,1,2]`.
2. Điều gì xảy ra với quần thể nếu `PM = 0`? Nếu `PM = 1`?
3. TSP là bài toán cực tiểu hoá nhưng GA ở chương này tối đa hoá fitness. Nêu hai cách chuyển đổi.

**Mở rộng (không bắt buộc):**

- So sánh chọn lọc giải đấu với roulette (`f = 1/L`), báo cáo số lần đạt tối ưu trên 20 `seed`.
- Quét `PM ∈ {0, 0.05, 0.2, 0.5}` và nhận xét.
- Thay đột biến hoán đổi bằng **đảo đoạn** và so sánh.
- Cài đặt **tìm kiếm ngẫu nhiên** (sinh hoán vị ngẫu nhiên, giữ tốt nhất) với **cùng số lần đánh giá** hàm độ dài như GA, rồi so sánh để thấy GA hơn ở đâu.
- Sinh 30 thành phố ngẫu nhiên (vét cạn không khả thi) và so sánh GA với thuật toán tham lam láng giềng gần nhất.

## Chapter 9: Học máy (Machine learning)

## Chapter 10: K-means clustering

- [ ] Cần cài đặt code

## Chapter 11: Mạng neuron nhân tạo (Neuron network)

- [ ] Cần cài đặt code (một lớp mạng vừa hoặc cực kỳ nhỏ, chỉ cần mang tính tìm hiểu thôi)