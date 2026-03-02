import streamlit as st
import pandas as pd
from openai import OpenAI

# Cấu hình giao diện
st.set_page_config(page_title="Trợ lý Luật Dân sự AI", page_icon="⚖️", layout="centered")

# --- QUẢN LÝ API KEY (BẢO MẬT) ---
# Cách 1: Lấy từ Streamlit Secrets (Nếu chạy trên Cloud/Local có file secrets.toml)
# Cách 2: Cho phép sếp nhập trực tiếp ở Sidebar nếu chưa có trong Secrets
try:
    api_key = st.secrets.get("OPENAI_API_KEY") 
except Exception:
    api_key = None

with st.sidebar:
    st.header("🔑 Cấu hình bảo mật")
    if not api_key or api_key == "your_openai_api_key_here":
        api_key = st.text_input("Sếp nhập OpenAI API Key vào đây nhé:", type="password")
        if api_key:
            st.success("Đã nhận khóa API! ✅")
        else:
            st.warning("Sếp vui lòng nhập API Key để kích hoạt trí tuệ OpenAI ạ.")
    else:
        st.success("Đã kết nối API từ hệ thống! ✅")

# 1. Cấu hình OpenAI (Chỉ chạy khi có Key hợp lệ)
if api_key and api_key != "your_openai_api_key_here":
    client = OpenAI(api_key=api_key)

    # 2. Đọc hướng dẫn hệ thống (Persona)
    try:
        with open("01.system_trainning.txt", "r", encoding="utf-8") as f:
            system_instruction = f.read()
    except FileNotFoundError:
        system_instruction = "Bạn là trợ lý ảo Luật Dân sự, xưng 'Em' gọi 'Sếp'."

    # 3. Cấu hình Model OpenAI
    if "model_name" not in st.session_state:
        st.session_state.model_name = "gpt-4o-mini"

    # 4. Khởi tạo session state cho lịch sử chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        initial_msg = f"Em chào sếp Canhnho! 👋 Em đã sẵn sàng hỗ trợ sếp với trí tuệ {st.session_state.model_name}. Sếp cần em tư vấn hay tra cứu vấn đề gì không ạ?"
        st.session_state.messages.append({"role": "assistant", "content": initial_msg})


    # 5. Giao diện chính
    st.title("⚖️ Trợ lý Luật Dân sự (OpenAI)")
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
                    # Chuẩn bị tin nhắn cho OpenAI
                    messages_for_api = [{"role": "system", "content": system_instruction}]
                    for m in st.session_state.messages:
                        messages_for_api.append({"role": m["role"], "content": m["content"]})
                    
                    response = client.chat.completions.create(
                        model=st.session_state.model_name,
                        messages=messages_for_api,
                    )
                    full_response = response.choices[0].message.content
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    error_str = str(e)
                    if "insufficient_quota" in error_str:
                        error_msg = "Dạ sếp, có vẻ như tài khoản OpenAI đang hết hạn mức (Quota). Sếp kiểm tra lại giúp em nhé! ☕"
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
            st.rerun()

        if st.button("🚀 Khám phá Antigravity"):
            st.balloons()
            st.success("Python làm mọi thứ nhẹ nhàng!")
        st.write("Phiên bản AI Inside 3.1 - Security Edition")
else:
    st.title("⚖️ Trợ lý Luật Dân sự AI")
    st.info("👋 Chào sếp! Để bắt đầu dùng trí tuệ AI, sếp vui lòng nhập **OpenAI API Key** ở thanh bên trái (Sidebar) nhé ạ.")
    st.image("https://raw.githubusercontent.com/streamlit/docs/main/public/images/tutorials/secrets_management.png", caption="Sếp có thể cấu hình Secrets để không phải nhập lại nhiều lần.")
