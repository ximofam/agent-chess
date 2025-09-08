# Agent chess

---
## ♟️ Giới thiệu:
Thuật toán **Minimax** được dùng để mô phỏng trò chơi hai người (zero-sum) như cờ vua.  
AI giả định đối thủ luôn chơi tối ưu, từ đó chọn nước đi đem lại lợi ích tối đa cho mình.

Tuy nhiên, cây trạng thái cờ vua nở rất nhanh, nên cần hai kỹ thuật chính:

- **Giới hạn độ sâu (Depth Limit):** Thay vì duyệt đến hết ván, AI chỉ xét đến một độ sâu nhất định (ví dụ depth = 3 hoặc 4). Ở độ sâu đó, **hàm đánh giá** (evaluation function) ước lượng giá trị của vị trí hiện tại.
- **Alpha-Beta Pruning:** Kỹ thuật cắt tỉa nhánh không cần thiết, giúp giảm số lượng trạng thái phải xét nhưng vẫn giữ kết quả giống minimax đầy đủ.  
  - **Alpha**: giá trị tốt nhất hiện tại mà người chơi MAX có thể đảm bảo.  
  - **Beta**: giá trị tốt nhất hiện tại mà người chơi MIN có thể đảm bảo.  
  - Khi `alpha >= beta`, nhánh còn lại không ảnh hưởng đến kết quả ⇒ cắt bỏ.


## 🧮 Evaluation Function

AI đánh giá một vị trí cờ vua dựa trên nhiều yếu tố:

- **Material**: Giá trị các quân cờ (King, Queen, Rook, Bishop, Knight, Pawn).
- **King Safety**: Độ an toàn của vua.  
- **Center Control**: Kiểm soát trung tâm bàn cờ.  
- **PST (Piece-Square Tables)**: Điểm thưởng/phạt dựa trên vị trí quân cờ.  
- **Pawn Structure**: Đánh giá cấu trúc tốt, bao gồm:
  - **Isolated pawns**: tốt không có đồng minh ở cột liền kề ⇒ yếu, bị trừ điểm.
  - **Doubled pawns**: nhiều tốt chồng cùng một cột ⇒ kém hiệu quả, bị trừ điểm.

## Minimax Example Tree
![Minimax Example](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Minimax.svg/1920px-Minimax.svg.png)

## Alpha-beta pruning Example Tree
![Alpha-beta pruning Example](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/AB_pruning.svg/1920px-AB_pruning.svg.png)

## Demo
![Demo](https://github.com/user-attachments/assets/445ffd4d-193d-4167-90a4-346a34efd7df)


---

##  Cấu trúc project

- **`images/`**: Chứa ảnh các quân cờ
- **`my_chess/`**: Logic game (Board, Piece, Move).
- **`agents.py`**: Chess AI (**Minimax**, **Alpha-Beta pruning**, Random)
- **`heuristics.py`**: **evaluation function** được thực hiện trong file này
- **`main.py`**: File chạy chính; bạn có thể import agent và khởi tạo game từ đây.
- **`test.py`**: Chứa các bài kiểm thử (unit tests) để đảm bảo module hoạt động chính xác.

---


## 🚀 Hướng dẫn chạy project
1. Tải thư viện pygame
   ```bash
   pip install pygame
   ```
2. Chạy file main.py
   ```bash
   python main.py
   ```
   

---

## 📚 Tài liệu tham khảo
- [Wikipedia – Minimax algorithm](https://en.wikipedia.org/wiki/Minimax)  
- [Wikipedia – Alpha–beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)  
- [Piece-Square Tables (PST)](https://www.chessprogramming.org/Simplified_Evaluation_Function)  
- [python-chess GitHub](https://github.com/niklasf/python-chess) Logic chess game dựa trên thư viện này
- [https://github.com/leesamuel423/ai-chess](https://github.com/leesamuel423/ai-chess)

---

## Thành viên
- Phạm Đặng Quốc Viễn
- Vũ Mạnh Hùng