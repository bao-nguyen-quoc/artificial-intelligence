# Artificial Intelligence Notebook

> Dựa trên tài liệu của khoá học tương ứng tại trường Đại học Bách Khoa - TP.Đà Nẵng

## Tổng quan

### 4 góc nhìn định nghĩa AI

- **Thinking humanly** (*Cognitive modeling*): Muốn máy suy nghĩ như người, trước hết phải hiểu con người suy nghĩ như thế nào. Dựa trên Khoa học nhận thức (Cognitive Science), General Problem Solver (GPS).
- **Thinking rationally** (*"Laws of thought"*): Tiếp cận bằng quy luật tư duy hình thức. Hai trở ngại lớn: khó biểu diễn vấn đề thực tế, chi phí tính toán lớn.
- **Acting humanly** (*Turing Test*, Alan Turing 1950): Máy được coi là có trí tuệ nếu giám khảo con người không phân biệt được câu trả lời là từ máy hay người, qua đối thoại văn bản gián tiếp. Cần năng lực ở: NLP, Knowledge representation, Automated reasoning, Computer vision, Robotics.
- **Acting rationally** (*Rational agent*): Agent nhận biết môi trường qua **sensors**, hành động qua **actuators**, và chọn hành động tối đa hoá khả năng đạt mục tiêu. Đây là hướng tiếp cận chủ đạo, hiện đại nhất của AI ngày nay.

### Ứng dụng

Game playing · Automated reasoning & Theorem proving · Expert systems · Planning & Robotics · Machine learning (supervised / unsupervised) · Natural language processing · Neural network

## Chapter 1: Suy luận logic

**Vấn đề:** Con người nhận thức thế giới qua giác quan, dùng tri thức tích luỹ để hành động hợp lý thông qua lập luận, suy diễn.
**Mục tiêu:** Khiến AI làm được điều tương tự.

> Ngôn ngữ biểu diễn tri thức = Cú pháp + Ngữ nghĩa + Luật suy diễn

### 1.1 Logic mệnh đề

> Máy tính không hiểu ngôn ngữ tự nhiên, nên cần một ngôn ngữ hình thức để biểu diễn tri thức và cho phép máy tự suy luận. Logic mệnh đề là ngôn ngữ đơn giản nhất để làm điều đó.

Gồm 4 thành phần: Cú pháp, Ngữ nghĩa, Dạng chuẩn tắc, Luật suy diễn.

**Ví dụ mở đầu:** "Nếu trời mưa thì trời có mây" → P = "Trời đang mưa", Q = "Trời có mây" → `P ⇒ Q`. Khi P đúng, Q chắc chắn đúng (Modus Ponens).

#### 1.1.1 Cú pháp

- Tập ký hiệu:
  - 2 hằng logic: `true` / `false`
  - Ký hiệu mệnh đề (biến mệnh đề): P, Q, ...
  - Kết nối logic: ¬, ∧, ∨, ⇒, ⟺
  - Ký hiệu `(`, `)`
- Luật xây dựng công thức:
  - Biến mệnh đề là công thức.
  - Với A, B là công thức thì `¬A`, `(A∧B)`, `(A∨B)`, `(A⇒B)`, `(A⟺B)` đều là công thức.

#### 1.1.2 Ngữ nghĩa

Ngữ nghĩa cho phép xác định ý nghĩa của công thức trong một mô hình cụ thể (một thế giới hiện thực cụ thể).

Nói cách khác: **Cú pháp** trả lời "viết thế nào", **Ngữ nghĩa** trả lời "công thức này đúng hay sai trong thực tế?".

#### 1.1.3 Các công thức tương đương

A và B tương đương (`A ≡ B`) nếu chúng luôn có cùng giá trị chân lý.

| Nhóm luật | Công thức |
|---|---|
| Luật thông dụng | `A ⇒ B ≡ ¬A ∨ B` · `A ⟺ B ≡ (A ⇒ B) ∧ (B ⇒ A)` · `¬(¬A) ≡ A` |
| De Morgan | `¬(A ∧ B) ≡ ¬A ∨ ¬B` · `¬(A ∨ B) ≡ ¬A ∧ ¬B` |
| Giao hoán | `A ∧ B ≡ B ∧ A` · `A ∨ B ≡ B ∨ A` |
| Kết hợp | `A ∧ (B ∧ C) ≡ (A ∧ B) ∧ C` · `A ∨ (B ∨ C) ≡ (A ∨ B) ∨ C` |
| Phân phối | `A ∧ (B ∨ C) ≡ (A ∧ B) ∨ (A ∧ C)` · `A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C)` |
| Loại trừ | `A ∨ ¬A ≡ true` |
| Mâu thuẫn | `A ∧ ¬A ≡ false` |

#### 1.1.4 Chuẩn hoá về CNF

Dạng chuẩn hội (CNF) = tích (∧) của các tổng (∨).
Ví dụ: `(P∨Q) ∧ (¬R∨S) ∧ (P∨¬Q∨R)`.

**Quy trình 3 bước**:

cho công thức `(P⇒Q) ∨ ¬(R∨¬S)`:

1. **Loại bỏ `⇒`, `⟺`** (dùng `A⇒B ≡ ¬A∨B`):
  `(¬P∨Q) ∨ ¬(R∨¬S)`
2. **Đưa phủ định vào trong** (De Morgan):
  `(¬P∨Q) ∨ (¬R∧S)`
3. **Phân phối `∨` vào `∧`**:
  `(¬P∨Q∨¬R) ∧ (¬P∨Q∨S)`

#### 1.1.5 Luật suy diễn

Từ giả thiết đã biết, máy áp dụng luật để rút ra kết luận mới.

| Luật | Dạng | Ví dụ |
|---|---|---|
| **Modus Ponens** | A ⇒ B, A ∴ B | Nếu mưa thì đường ướt; đang mưa ∴ đường ướt |
| **Modus Tollens** | A ⇒ B, ¬B ∴ ¬A | Nếu mưa thì đường ướt; đường không ướt ∴ trời không mưa |
| **Luật hội** (Conjunction) | A, B ∴ A ∧ B | Trời nắng; gió nhẹ ∴ trời nắng và gió nhẹ |
| **Luật đơn giản** (Simplification) | A ∧ B ∴ A, ∴ B | Nam vừa thông minh vừa chăm chỉ ∴ Nam thông minh, ∴ Nam chăm chỉ |
| **Luật cộng** (Addition) | A ∴ A ∨ B | Hôm nay thứ Hai ∴ hôm nay thứ Hai hoặc trời mưa (đúng bất kể trời mưa hay không) |
| **Tam đoạn luận tuyển** (Disjunctive Syllogism) | A ∨ B, ¬A ∴ B | Chìa khoá trong túi hoặc trên bàn; không ở trong túi ∴ ở trên bàn |
| **Tam đoạn luận giả thiết** (Hypothetical Syllogism) | A⇒B, B⇒C ∴ A⇒C | Học tốt→đậu tốt nghiệp; đậu tốt nghiệp→xin được việc ∴ học tốt→xin được việc |
| **Resolution** (phân giải) | A∨B, ¬B∨C ∴ A∨C | Trời mưa hoặc Nam ở nhà; Nam không ở nhà hoặc Nam mang ô ∴ trời mưa hoặc Nam mang ô |

#### 1.1.6 Phương pháp chứng minh bác bỏ (Refutation)

> Thường dùng trong chứng minh toán học. Để chứng minh **P** đúng: giả sử **¬P** (thêm vào giả thiết), rồi dùng luật phân giải để dẫn tới mâu thuẫn (sinh ra công thức rỗng `[]`).

#### 1.1.7 Bài tập vận dụng

> "Nam đẹp trai, giàu có. Do vậy, Nam hoặc là phung phí hoặc là (nhân từ và giúp người). Thực tế, Nam không phung phí và cũng không kiêu căng."
> Suy luận: "Do vậy, có thể nói Nam là người nhân từ"

**Kiểm chứng bằng luật phân giải.**

**1. Định nghĩa mệnh đề**

- A: Nam đẹp trai
- B: Nam giàu có
- C: Nam phung phí
- D: Nam nhân từ
- E: Nam giúp người
- F: Nam kiêu căng

**2. Biểu diễn giả thiết**

```
GT1: A ∧ B
GT2: (A ∧ B) ⇒ (C ∨ (D ∧ E))
GT3: ¬C ∧ ¬F
```

Kết luận cần kiểm chứng: **D**

**3. Chuẩn hoá về CNF**

```
Từ GT1: A, B

Từ GT2: (A ∧ B) ⇒ (C ∨ (D ∧ E))
  bỏ kéo theo:      ¬(A ∧ B) ∨ (C ∨ (D ∧ E))
  De Morgan:        ¬A ∨ ¬B ∨ C ∨ (D ∧ E)
  phân phối ∨/∧:     (¬A ∨ ¬B ∨ C ∨ D) ∧ (¬A ∨ ¬B ∨ C ∨ E)

Từ GT3: ¬C, ¬F
```

```
C1: A
C2: B
C3: ¬A ∨ ¬B ∨ C ∨ D
C4: ¬A ∨ ¬B ∨ C ∨ E
C5: ¬C
C6: ¬F
```

**4. Chứng minh bác bỏ**

Giả sử kết luận sai: `C7: ¬D`

```
Phân giải C3 và C1 (A):
  C8:  ¬B ∨ C ∨ D
Phân giải C8 và C2 (B):
  C9:  C ∨ D
Phân giải C9 và C5 (¬C):
  C10: D
Phân giải C10 và C7 (¬D):
  C11: []  (mâu thuẫn)
```

**Vậy kết luận "Nam là người nhân từ" là đúng.**

*Lưu ý:* C4 (liên quan đến E - "giúp người") và C6 (¬F - "không kiêu căng") không được dùng trong chứng minh - đây là giả thiết dư (redundant), không ảnh hưởng đến kết quả suy luận về D.

### 1.2 Logic vị từ

#### 1.2.1 Giới hạn của Logic mệnh đề

> "Mọi sinh viên trường ĐHBK đều có bằng tú tài. Lan không có bằng tú tài. Do vậy, Lan không là sinh viên trường ĐHBK."

Logic mệnh đề **không thể** biểu diễn câu này gọn gàng vì:

- "Lan" là một đối tượng cụ thể trong tập "sinh viên trường ĐHBK".
- Logic mệnh đề không có cách biểu diễn "với mọi X" hay "tồn tại một X".
- Phải liệt kê từng phần tử: "Nếu An là SV ĐHBK thì An có bằng tú tài", "Nếu Bình là SV ĐHBK thì Bình có bằng tú tài", ... - không khả thi.

Logic vị từ giải quyết bằng cách cho phép nói: `∀X (sv_bk(X) ⇒ tu_tai(X))` - "Với mọi X, nếu X là sinh viên ĐHBK, thì X có bằng tú tài".

#### 1.2.2 Định nghĩa

> Vị từ là phát biểu nói lên quan hệ giữa một đối tượng với thuộc tính của nó, hoặc quan hệ giữa các đối tượng với nhau. Được biểu diễn bởi tên vị từ và theo sau là danh sách thông số.

Ví dụ:

- `sv_bk(Lan)` - Lan là sinh viên ĐHBK.
- `khoang_cach(HN, HCM, 1500km)` - khoảng cách Hà Nội–TP.HCM là 1500km.

#### 1.2.3 Cú pháp

| Thành phần | Ký hiệu | Ví dụ |
|---|---|---|
| **Hằng** (constant) - đối tượng cụ thể | a, b, An, Ba, ... | `Lan`, `HN`, `HCM` |
| **Biến** (variable) - đại diện đối tượng bất kỳ | x, y, z, ... | `x`, `y` |
| **Vị từ** (predicate) - tên quan hệ/thuộc tính | P, Q, Like, ... | `sinh_vien_dhbk(x)`, `khoang_cach(x,y,z)` |
| **Hàm** (function) - chỉ đối tượng liên quan mà không cần đặt tên trực tiếp | f, g, mother, ... | `mother(x,y)` (y là mẹ của x) |
| **Kết nối logic** | ∧, ∨, ⇒, ⟺, ¬ | như logic mệnh đề |
| **Lượng từ** (quantifiers) | ∀ (với mọi), ∃ (tồn tại) | |
| **Ký hiệu ngăn cách** | `,` `(` `)` | |

**Công thức phân tử:** `tên_vị_từ(term1, ..., termn)`, trong đó term là hằng, biến hoặc hàm. Công thức không chứa biến gọi là công thức cụ thể.

```
∀X (sv_bk(X) ⇒ tu_tai(X))
¬tu_tai("Lan")
Do vậy, ¬sv_bk("Lan")
```

```
∃X (sv_cntt(X) ∧ lap_trinh_tot(X))
```

#### 1.2.4 Công thức tương đương

```
Đặt lại tên biến:
  ∀X G(X) ≡ ∀Y G(Y)
  ∃X G(X) ≡ ∃Y G(Y)
Phủ định:
  ¬∀X G(X) ≡ ∃X ¬G(X)
  ¬∃X G(X) ≡ ∀X ¬G(X)
Phân giải:
  ∀X (G(X)∧H(X)) ≡ ∀X G(X) ∧ ∀X H(X)
  ∃X (G(X)∧H(X)) ≡ ∃X G(X) ∧ ∃X H(X)
```

#### 1.2.5 Chuẩn hoá công thức vị từ về CNF

1. **Loại bỏ `⇒`, `⟺`**: `A⇒B ≡ ¬A∨B` · `A⟺B ≡ (A⇒B)∧(B⇒A)`
2. **Đưa phủ định vào sát phần tử** (công thức phủ định của vị từ, De Morgan)
3. **Loại bỏ `∃` (Skolem hoá)**: `∃y G(y) ≡ G(Y)` - đặt tên cụ thể (hằng Skolem) cho y.
  Nếu y phụ thuộc vào biến x đang bị `∀` bao ngoài, thay y bằng hàm Skolem của x: `∀x (∃y P(x,y)) ≡ ∀x P(x,f(x))`
4. **Xoá lượng tử `∀`**: sau bước 3 chỉ còn `∀`, có thể xoá vì mọi biến còn lại đều là `∀`. `∀x P(x,f(x)) ≡ P(x,f(x))`
5. **Chuyển về CNF**: áp dụng như logic mệnh đề (mục 1.1.4).

### 1.3 Ví dụ tổng hợp: "Ai giết mèo Bibi?"

Cho biết:

- Ba nuôi một con chó (tên D)
- Ba hoặc Am đã giết con mèo Bibi
- Mọi người nuôi chó đều yêu quý động vật
- Ai yêu quý động vật cũng không giết động vật
- Chó mèo là động vật

Hỏi: Ai giết mèo Bibi?

**1. Định nghĩa hằng và vị từ**

- Hằng: Ba, Am, Bibi, D
- Vị từ:
  - `nuoi(x,y)`: x nuôi y
  - `yeu_dong_vat(x)`: x yêu động vật
  - `giet(x,y)`: x giết y
  - `dong_vat(x)`: x là động vật
  - `cho(x)`: x là chó
  - `meo(x)`: x là mèo

**2. Biểu diễn giả thiết**

```
(1) cho(D) ∧ nuoi(Ba, D)
(2) meo(Bibi) ∧ (giet(Ba, Bibi) ∨ giet(Am, Bibi))
(3) ∀x (∃y cho(y) ∧ nuoi(x, y) ⇒ yeu_dong_vat(x))
(4) ∀x ∀y ((yeu_dong_vat(x) ∧ dong_vat(y)) ⇒ ¬giet(x, y))
(5) ∀x (cho(x) ⇒ dong_vat(x)) ∧ ∀y (meo(y) ⇒ dong_vat(y))
```

**3. Chuẩn hoá về CNF**

```
Từ (1): cho(D)                      nuoi(Ba, D)
Từ (2): meo(Bibi)                   giet(Ba, Bibi) ∨ giet(Am, Bibi)

Từ (3): ∀x (∃y cho(y) ∧ nuoi(x, y) ⇒ yeu_dong_vat(x))
  bỏ kéo theo:        ∀x (¬(∃y cho(y) ∧ nuoi(x, y)) ∨ yeu_dong_vat(x))
  De Morgan:          ∀x (¬∃y cho(y) ∨ ¬nuoi(x, y) ∨ yeu_dong_vat(x))
  phủ định lượng từ y: ∀x (∀y ¬cho(y) ∨ ¬nuoi(x, y) ∨ yeu_dong_vat(x))
  xoá ∀:               ¬cho(y) ∨ ¬nuoi(x, y) ∨ yeu_dong_vat(x)

Từ (4): ∀x ∀y ((yeu_dong_vat(x) ∧ dong_vat(y)) ⇒ ¬giet(x, y))
  bỏ kéo theo:  ∀x ∀y (¬(yeu_dong_vat(x) ∧ dong_vat(y)) ∨ ¬giet(x, y))
  De Morgan:    ∀x ∀y (¬yeu_dong_vat(x) ∨ ¬dong_vat(y) ∨ ¬giet(x, y))
  xoá ∀:         ¬yeu_dong_vat(x) ∨ ¬dong_vat(y) ∨ ¬giet(x, y)

Từ (5): ∀x (cho(x) ⇒ dong_vat(x)) ∧ ∀y (meo(y) ⇒ dong_vat(y))
  bỏ kéo theo + xoá ∀ + đơn giản hoá:
    ¬cho(x) ∨ dong_vat(x)
    ¬meo(y) ∨ dong_vat(y)
```

```
C1: cho(D)
C2: nuoi(Ba, D)
C3: meo(Bibi)
C4: giet(Ba, Bibi) ∨ giet(Am, Bibi)
C5: ¬cho(y) ∨ ¬nuoi(x, y) ∨ yeu_dong_vat(x)
C6: ¬yeu_dong_vat(x) ∨ ¬dong_vat(y) ∨ ¬giet(x, y)
C7: ¬cho(x) ∨ dong_vat(x)
C8: ¬meo(y) ∨ dong_vat(y)
```

**4. Giải**

*Cách giải 1 - chứng minh bác bỏ (giả sử Am không giết Bibi):*

```
Giả sử:
  C9:  ¬giet(Am, Bibi)
Phân giải C4, C9:
  C10: giet(Ba, Bibi)
Phân giải C10, C6 (x=Ba, y=Bibi):
  C11: ¬yeu_dong_vat(Ba) ∨ ¬dong_vat(Bibi)
Phân giải C3, C8 (y=Bibi):
  C12: dong_vat(Bibi)
Phân giải C11, C12:
  C13: ¬yeu_dong_vat(Ba)
Phân giải C13, C5 (x=Ba):
  C14: ¬cho(y) ∨ ¬nuoi(Ba, y)
Phân giải C14, C1 (y=D):
  C15: ¬nuoi(Ba, D)
Phân giải C15, C2:
  C16: []  (mâu thuẫn)
```

Vậy **Am giết Bibi.**

*Cách giải 2 - phân giải thuận, không cần giả sử phản chứng:*

```
Phân giải C5, C1 (y=D):
  C9:  ¬nuoi(x, D) ∨ yeu_dong_vat(x)
Phân giải C9, C2 (x=Ba):
  C10: yeu_dong_vat(Ba)
Phân giải C10, C6 (x=Ba):
  C11: ¬dong_vat(y) ∨ ¬giet(Ba, y)
Phân giải C3, C8 (y=Bibi):
  C12: dong_vat(Bibi)
Phân giải C11, C12 (y=Bibi):
  C13: ¬giet(Ba, Bibi)
Phân giải C4, C13:
  C14: giet(Am, Bibi)
```

→ **Am giết Bibi.**

*So sánh:* Cách 2 đi thẳng bằng phân giải thuận (forward resolution), không cần giả thiết phản chứng ban đầu - suy luận có ý nghĩa ngữ nghĩa rõ ràng hơn ở từng bước (Ba nuôi chó → Ba yêu động vật → Ba không giết động vật → vậy phải là Am). Tuy nhiên, Cách 1 với tư duy phản chứng cũng là 1 phương án thông dụng trong nhiều suy luận toán học.