# Agent chess

##  Cấu trúc dự án
Dự án `agent-chess` được thiết kế như sau:
- **`images/`**: Chứa ảnh các quân cờ
- **`my_chess/`**: Thư mục chứa logic xử lý trò chơi cờ.
- **`agents.py`**: Định nghĩa các agent chơi cờ như Alpha-Beta Agent, Minimax Agent, v.v.
- **`heuristics.py`**: chứa hàm đánh giá bàn cờ
- **`main.py`**: File chạy chính; bạn có thể import agent và khởi tạo game từ đây.
- **`test.py`**: Chứa các bài kiểm thử (unit tests) để đảm bảo module hoạt động chính xác.
- **`.gitignore`**: Các file hoặc thư mục (như `__pycache__`, `.vscode/`, `*.pyc`) không đưa lên Git.

## 🚀 Hướng dẫn sử dụng

1. **Cài đặt thư viện Pygame**  
   Mở terminal/cmd và chạy:
   ```bash
   pip install pygame
   
2. **Chạy hàm main.py**
   Mở terminal/cmd và chạy:
   ```bash
   python main.py