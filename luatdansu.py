import streamlit as st
import pandas as pd
import google.generativeai as genai

# Cấu hình giao diện
st.set_page_config(page_title="Trợ lý Luật Dân sự AI", page_icon="⚖️", layout="centered")

# --- QUẢN LÝ API KEY (BẢO MẬT) ---
# Cách 1: Lấy từ Streamlit Secrets (Nếu chạy trên Cloud/Local có file secrets.toml)
# Cách 2: Cho phép sếp nhập trực tiếp ở Sidebar nếu chưa có trong Secrets
try:
    api_key = st.secrets.get("GEMINI_API_KEY") 
except Exception:
    api_key = None

with st.sidebar:
    st.header("🔑 Cấu hình bảo mật")
    if not api_key:
        api_key = st.text_input("Sếp nhập Gemini API Key vào đây nhé:", type="password")
        if api_key:
            st.success("Đã nhận khóa API! ✅")
        else:
            st.warning("Sếp vui lòng nhập API Key để kích hoạt trí tuệ Gemini ạ.")
    else:
        st.success("Đã kết nối API từ hệ thống! ✅")

# 1. Cấu hình Gemini AI (Chỉ chạy khi có Key)
if api_key:
    genai.configure(api_key=api_key)

    # 2. Đọc hướng dẫn hệ thống (Persona)
    try:
        with open("01.system_trainning.txt", "r", encoding="utf-8") as f:
            system_instruction = f.read()
    except FileNotFoundError:
        system_instruction = "Bạn là trợ lý ảo Luật Dân sự, xưng 'Em' gọi 'Sếp'."

    # 3. Khởi tạo Model Gemini với cơ chế thử lại nhiều phiên bản
    # Vì mỗi tài khoản/khu vực có quota khác nhau, em sẽ thử lần lượt ạ
    if "model_name" not in st.session_state:
        models_to_try = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-pro"]
        selected_model = "gemini-pro" # Default fallback
        for m_name in models_to_try:
            try:
                # Thử tạo model để kiểm tra tính khả dụng
                genai.GenerativeModel(model_name=m_name)
                selected_model = m_name
                break
            except Exception:
                continue
        st.session_state.model_name = selected_model

    # Tạo đối tượng model từ tên đã chọn
    try:
        model = genai.GenerativeModel(
            model_name=st.session_state.model_name, 
            system_instruction=system_instruction
        )
    except Exception:
        # Nếu model không hỗ trợ system_instruction (bản cũ)
        model = genai.GenerativeModel(model_name=st.session_state.model_name)

    # 4. Khởi tạo session state cho lịch sử chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        initial_msg = f"Em chào sếp Canhnho! 👋 Em đã sẵn sàng hỗ trợ sếp với trí tuệ {st.session_state.model_name}. Sếp cần em tư vấn hay tra cứu vấn đề gì không ạ?"
        st.session_state.messages.append({"role": "assistant", "content": initial_msg})

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # 5. Giao diện chính
    st.title("⚖️ Trợ lý Luật Dân sự (Gemini AI)")
    st.caption(f"Đang dùng: {st.session_state.model_name} - Bảo mật & Tận tâm")
    st.markdown("---")

    # Hiển thị lịch sử chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Xử lý nhập liệu từ Sếp
    if prompt := st.chat_input("Sếp muốn em hỗ trợ gì ạ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Em đang suy nghĩ, sếp đợi em xíu nhé..."):
                try:
                    response = st.session_state.chat_session.send_message(prompt)
                    full_response = response.text
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str:
                        error_msg = "Dạ sếp, hiện tại yêu cầu đang hơi quá tải (lỗi Quota 429). Sếp vui lòng đợi khoảng **1 phút** rồi hỏi lại em nhé! ☕"
                    else:
                        error_msg = f"Dạ sếp, em gặp chút trục trặc: {error_str}. Sếp thử lại câu hỏi khác nhé ạ!"
                    
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # Sidebar bổ sung
    with st.sidebar:
        st.markdown("---")
        st.header("🏢 Phòng làm việc")
        if st.button("🧹 Xóa lịch sử Chat"):
            st.session_state.messages = []
            st.session_state.chat_session = model.start_chat(history=[])
            st.rerun()

        if st.button("🚀 Khám phá Antigravity"):
            st.balloons()
            st.success("Python làm mọi thứ nhẹ nhàng!")
        st.write("Phiên bản AI Inside 3.1 - Security Edition")
else:
    st.title("⚖️ Trợ lý Luật Dân sự AI")
    st.info("👋 Chào sếp! Để bắt đầu dùng trí tuệ AI, sếp vui lòng nhập **Gemini API Key** ở thanh bên trái (Sidebar) nhé ạ.")
    st.image("https://raw.githubusercontent.com/streamlit/docs/main/public/images/tutorials/secrets_management.png", caption="Sếp có thể cấu hình Secrets để không phải nhập lại nhiều lần.")
