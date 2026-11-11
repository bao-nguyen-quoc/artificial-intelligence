# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Chapter 4: Hệ luật sinh

### Mục lục

- [4.1 Nhắc lại tìm kiếm trên không gian trạng thái](#41-nhắc-lại-tìm-kiếm-trên-không-gian-trạng-thái)
- [4.2 Tìm kiếm đệ quy](#42-tìm-kiếm-đệ-quy)
  - [4.2.1 Đệ quy](#421-đệ-quy)
  - [4.2.2 Recursive search](#422-recursive-search)
  - [4.2.3 Pattern directed search](#423-pattern-directed-search)
- [4.3 Hệ luật sinh](#43-hệ-luật-sinh)
  - [4.3.1 Cấu trúc](#431-cấu-trúc)
  - [4.3.2 Chu trình Match - Resolve - Act](#432-chu-trình-match---resolve---act)
  - [4.3.3 Suy diễn tiến và suy diễn lùi](#433-suy-diễn-tiến-và-suy-diễn-lùi)
- [4.4 Điều khiển tìm kiếm trong hệ luật sinh](#44-điều-khiển-tìm-kiếm-trong-hệ-luật-sinh)
- [4.5 Ưu điểm của hệ luật sinh](#45-ưu-điểm-của-hệ-luật-sinh)

**Vấn đề:** Cần một khung làm việc tổng quát để biểu diễn tri thức dạng luật và dùng nó để tìm kiếm lời giải, mô phỏng cách con người giải quyết vấn đề.
**Mục tiêu:** Nắm kiến trúc hệ luật sinh, nền tảng của hệ chuyên gia (chương 5).

### 4.1 Nhắc lại tìm kiếm trên không gian trạng thái

> Lời giải là một **PATH** đi từ START đến GOAL. Tìm kiếm là kiểm tra có hệ thống các đường dẫn dẫn đến GOAL.

- **Backtracking:** cho phép giải thuật "phục hồi" khi đi vào nhánh không có đáp án.
- Hai danh sách giữ trạng thái:
  - `Open`: các trạng thái chưa xem xét, cho phép backtrack.
  - `Closed`: các trạng thái đã xem xét, dùng để phát hiện quay vòng, tránh lặp vô hạn.

| Giải thuật | Cấu trúc dữ liệu cho `Open` |
|---|---|
| DFS | Stack |
| BFS | Queue |
| Best-first | Priority Queue |

### 4.2 Tìm kiếm đệ quy

> Tìm kiếm đệ quy là giải thuật tìm kiếm trên không gian trạng thái, ngắn gọn, tự nhiên và hợp nhất với cách hiện thực của logic vị từ. Được dùng rộng rãi trong các shell của hệ chuyên gia.

Hai giải thuật chính: **Recursive search (RS)** và **Pattern directed search (PDS)**. PDS là nền tảng của PROLOG.

#### 4.2.1 Đệ quy

Một thủ tục đệ quy luôn có đủ 2 thành phần:

- **Thành phần đệ quy:** thủ tục gọi lại chính nó để lặp chuỗi thao tác.
- **Thành phần dừng:** chặn việc đệ quy vô tận.

Đệ quy là cấu trúc điều khiển tự nhiên cho các cấu trúc không xác định số phần tử như list, tree, đồ thị.

#### 4.2.2 Recursive search

Ví dụ kiểm tra một phần tử có thuộc list hay không:

```
function member(item, list);
begin
  if list rỗng then return (fail)               /* thành phần dừng */
  else if item = phần tử đầu của list then return (success)   /* thành phần dừng */
  else
    begin
      tail := list \ phần tử đầu;
      return member(item, tail);                /* thành phần đệ quy */
    end
end;
```

#### 4.2.3 Pattern directed search

> RS và các giải thuật search trước đó chưa nói cách biểu diễn một trạng thái cũng như cách **sinh trạng thái mới**. PDS giải quyết việc này bằng logic vị từ.

**Ý tưởng:** xuất phát từ goal `P`, dùng các luật dạng modus ponens `Q(x) ⇒ P(x)` (gọi là **luật sinh**) để chuyển trạng thái:

1. Tìm các rule có `P` ở vế phải (kết luận).
2. Xem vế trái `Q` (tiền đề) là **sub-goal**.
3. Đệ quy với `Q` cho đến khi `Q` là một fact trong kho tri thức.

**Ví dụ:**

```
Fact:  cho(D)
Rule:  cho(x) ⇒ dong_vat(x)
Goal:  dong_vat(D)

dong_vat(D) là vế phải của rule  →  sub-goal cho(D)
cho(D) trùng fact                →  success
```

**Đặc điểm:**

- Mỗi goal được tách thành các goal con (nhờ rule và phép hội).
- **Tách bạch điều khiển và dữ liệu:** giải thuật giữ nguyên, chỉ đổi database (fact + rule) là giải được bài toán khác. Đây là cơ sở của **expert system shell**: một bộ suy diễn, nhiều cơ sở tri thức.
- **Hạn chế về biến:** chỉ thay biến ở mức đơn giản (ví dụ `P(x) ∧ Q(x)` đúng khi cả hai thoả với cùng giá trị `x`), chưa đầy đủ như unification của Prolog.

Bản đầy đủ có xử lý thêm phủ định và phép tuyển:

```
function pattern_search(current_goal);
begin
  if current_goal có trong Closed then return fail
  else thêm current_goal vào Closed;

  while còn rule hay fact chưa xét do
  begin
    case
      current_goal trùng với fact:
        return (success);

      current_goal là negated(p):
        begin
          if pattern_search(p) then return fail
          else return success (không có thay thế)
        end;

      current_goal là phép hội (P1 ∧ ... ∧ Pn):
        begin
          for mỗi thành phần hội Pi do
            if not pattern_search(Pi) then return fail
            else thay các biến vừa gán vào các thành phần hội còn lại;
          return các thay thế
        end;

      current_goal là phép tuyển (V1 ∨ ... ∨ Vn):
        begin
          for mỗi thành phần tuyển Vi do
            if pattern_search(Vi) then return các thay thế;
          return fail
        end;

      current_goal là vế phải (kết luận) của một rule:
        begin
          áp dụng các phép thay thế vào vế trái Q (tiền đề);
          if pattern_search(Q)
            then return kết hợp của current_goal và các thay thế của Q
          else return fail
        end;
    end; /* case */
  end;
  return fail
end;
```

### 4.3 Hệ luật sinh

> Hệ luật sinh (Production System) là kiến trúc suy diễn dựa trên tri thức, xây dựng từ tập các luật dạng **điều kiện - hành động**. Nó cung cấp cơ chế điều khiển pattern-directed trong quá trình giải quyết vấn đề, và mô phỏng được cách con người giải quyết vấn đề.

#### 4.3.1 Cấu trúc

| Thành phần | Vai trò |
|---|---|
| **Working Memory** (bộ nhớ làm việc) | Chứa các mẫu mô tả **trạng thái hiện tại** của vấn đề; khởi tạo bằng trạng thái bắt đầu. Các mẫu này được so trùng với condition của rule, và action của rule tác động trực tiếp lên nó. |
| **Production Rules** (tập luật sinh) | `IF (CONDITION) THEN (ACTION)`. Condition là mẫu xác định khi nào rule áp dụng được; Action mô tả bước giải quyết, làm thay đổi hiện trạng. Tập luật là kho tri thức của bài toán. |
| **Recognize-action control** (bộ điều khiển) | Lặp chu trình Match - Resolve - Act (mục 4.3.2). |

#### 4.3.2 Chu trình Match - Resolve - Act

| Bước | Nội dung |
|---|---|
| **Match** (khớp mẫu) | So khớp dữ liệu trong Working Memory với condition của các luật. |
| **Resolve** (giải quyết xung đột) | Nhiều luật cùng thoả thì chọn một luật theo độ ưu tiên, tính cụ thể, hay độ mới (mục 4.4). |
| **Act** (thực thi) | Áp dụng luật đã chọn để cập nhật Working Memory. |

#### 4.3.3 Suy diễn tiến và suy diễn lùi

| | Suy diễn tiến (Forward / Data-driven) | Suy diễn lùi (Backward / Goal-driven) |
|---|---|---|
| Xuất phát | Các sự thật đã biết trong Working Memory | Goal cần chứng minh |
| Cách làm | Match condition → conflict → áp dụng action → thay đổi Working Memory | Match goal với kết luận của rule → condition thành sub-goal → đưa vào Working Memory |
| Dừng khi | Working Memory chứa goal state | Mọi sub-goal đều là fact |

**Ví dụ:** Luật `R1: A ∧ B ⇒ C` · `R2: C ⇒ D` · `R3: A ⇒ E`. Fact ban đầu `{A, B}`, goal là `D`.

```
Suy diễn tiến:
  Vòng 1: R1 và R3 cùng thoả → conflict → chọn R1 (cụ thể hơn: 2 điều kiện)
          WM = {A, B, C}
  Vòng 2: R2 thoả (và R3) → chọn R2 (recency: dùng C vừa thêm)
          WM = {A, B, C, D}  →  chứa goal, dừng

Suy diễn lùi:
  Goal D → R2 → sub-goal C → R1 → sub-goal A, B → đều là fact → success
  (R3 không bị đụng đến)
```

Suy diễn lùi chỉ khảo sát nhánh liên quan đến goal, còn suy diễn tiến có thể sinh ra các kết luận không cần thiết (như `E`).

### 4.4 Điều khiển tìm kiếm trong hệ luật sinh

Có 3 cách điều khiển:

1. **Chọn chiến lược:** data-driven hay goal-driven (mục 4.3.3).
2. **Điều khiển qua cấu trúc rule:** dùng các biến đổi tương đương của biểu thức trong rule để định hướng tìm kiếm.
3. **Điều khiển bằng phân tích conflict:** chọn luật nhờ heuristic và meta knowledge.

| Heuristic | Nội dung |
|---|---|
| **Refraction** | Rule đã áp dụng thì không dùng lại cho đến khi phần dữ liệu khớp với nó trong Working Memory thay đổi (tránh lặp vô hạn). |
| **Recency** | Ưu tiên rule có condition khớp với phần **mới thêm** vào Working Memory (theo đuổi một hướng triển khai). |
| **Specificity** | Rule càng đặc tả chi tiết (nhiều điều kiện hơn) càng được ưu tiên. |

### 4.5 Ưu điểm của hệ luật sinh

> Hệ luật sinh là khung làm việc tổng quát để thực thi các giải thuật tìm kiếm; đơn giản, dễ sửa đổi, linh động, nên là công cụ quan trọng để xây dựng hệ chuyên gia và các ứng dụng AI khác.

- **Tách bạch tri thức và điều khiển:** tri thức nằm trong các luật, điều khiển nằm trong chu trình Recognize-Action. Có thể cập nhật tri thức mà không sửa chương trình, và ngược lại.
- **Dễ áp dụng cho tìm kiếm trên không gian trạng thái:** state của Working Memory là node, rule là phép chuyển giữa các trạng thái.
- **Các luật độc lập** với nhau.
- **Áp dụng được heuristic** để điều khiển quá trình hoạt động.
- **Theo dõi và giải thích** được quá trình suy diễn.
- **Độc lập với ngôn ngữ** hiện thực, có thể dùng để mô phỏng cách giải quyết vấn đề của con người.