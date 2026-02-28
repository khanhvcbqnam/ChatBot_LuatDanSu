# ⚖️ Trợ lý Luật Dân sự (Streamlit ChatBot)

Chào sếp Canhnho! Đây là dự án ChatBot hỗ trợ tra cứu Luật Dân sự được tối ưu hóa cho Streamlit.

## 📂 Cấu trúc thư mục
- `LuatDanSu.py`: File chạy chính của ứng dụng.
- `01.system_trainning.txt`: Huấn luyện phong cách trả lời cho "Em".
- `requirements.txt`: Danh sách các thư viện cần thiết.
- `.streamlit/config.toml`: Cấu hình giao diện Premium.

## 🔐 Bảo mật API Key
Để đảm bảo an toàn, sếp có 2 cách để cung cấp API Key:
1.  **Cách 1 (Tạm thời)**: Nhập trực tiếp vào ô "Gemini API Key" ở thanh Sidebar khi chạy ứng dụng.
2.  **Cách 2 (Khuyên dùng)**: Tạo file `.streamlit/secrets.toml` trong thư mục dự án và thêm dòng sau:
    ```toml
    GEMINI_API_KEY = "Khóa_của_sếp_ở_đây"
    ```
    Khi đó, "Em" sẽ tự động nhận diện mà sếp không cần nhập lại mỗi lần chạy.

## 💡 Cách dùng
- Sếp có thể nhập số Điều (vd: "Điều 1") hoặc từ khóa (vd: "Vay tài sản") vào ô chat.
- "Em" sẽ tự động tìm kiếm và hiển thị nội dung cho sếp ngay lập tức.

Chúc sếp làm việc hiệu quả!
