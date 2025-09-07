# Agent chess

---

## 🧮 Evaluation Function

AI đánh giá một vị trí cờ vua dựa trên nhiều yếu tố:

- **Material**: Giá trị các quân cờ (King, Queen, Rook, Bishop, Knight, Pawn).  
- **Mobility**: Số lượng nước đi hợp lệ.  
- **King Safety**: Độ an toàn của vua.  
- **Center Control**: Kiểm soát trung tâm bàn cờ.  
- **PST (Piece-Square Tables)**: Điểm thưởng/phạt dựa trên vị trí quân cờ.



##  Cấu trúc project

- **`images/`**: Chứa ảnh các quân cờ
- **`my_chess/`**: Logic game (Board, Piece, Move).
- **`agents.py`**: Chess AI (Minimax, Alpha-Beta pruning, Random)
- **`heuristics.py`**: Hàm đánh giá bàn cờ dựa trên PST
- **`main.py`**: File chạy chính; bạn có thể import agent và khởi tạo game từ đây.
- **`test.py`**: Chứa các bài kiểm thử (unit tests) để đảm bảo module hoạt động chính xác.
- **`.gitignore`**: Chặn các file hoặc thư mục (như `__pycache__`, `.vscode/`, `*.pyc`) không đưa lên Git.

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

## 📚 References
- [Wikipedia – Minimax algorithm](https://en.wikipedia.org/wiki/Minimax)  
- [Wikipedia – Alpha–beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)  
- [Piece-Square Tables (PST)](https://www.chessprogramming.org/Simplified_Evaluation_Function) – Chess Programming Wiki  
- Norvig, P. (1992). *Artificial Intelligence: A Modern Approach* – Chương về Game Playing  
- [The Chess Programming Wiki](https://www.chessprogramming.org/) – Tài nguyên toàn diện về lập trình AI cờ vua

---

## Thành viên
- Phạm Đặng Quốc Viễn
- Vũ Mạnh Hùng