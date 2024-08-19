import streamlit as st
import time  # 추가된 부분

# from backend import process_rag, InputData
from predibase import Predibase

st.set_page_config(page_title="User/Company Multi-Page App", layout="wide")

# 로고와 타이틀을 두 개의 열로 나눔
col1, col2 = st.columns([1, 5])  # 첫 번째 열은 좁게, 두 번째 열은 넓게 설정

with col1:
    st.image("1.png", width=100)  # 로고의 크기를 적절하게 설정

with col2:
    st.title("RefundRangers💪 - your Tax Return Co-pilot")

# 사용자에게 입력받을 occupation 변수
occupation = st.text_input("What is your occupation?")

# 이메일 주소 입력 (옵셔널)
email = st.text_input(
    "What is your email address? (optional)", placeholder="example@example.com"
)

st.title("Your Occupation's Deduction Strategy")

# occupation이 입력되었고, 아직 response_rag가 세션 상태에 저장되지 않았다면 처리
if occupation and "response_rag_displayed" not in st.session_state:
    st.write("Processing your request. Please wait...")
    time.sleep(60)  # 60초 대기

    # 출력 내용을 session_state에 저장
    st.session_state.response_rag_text = """
    **🌟 Key Tax Deduction Guidelines for IT Professionals in Australia**<br>
    <br>
    **✅ Deductible Items:**<br>
    - **Car Expenses:** Only for work-related travel between jobs or to alternate workplaces, not for regular commuting.<br>
    - **Working from Home:** Expenses directly related to your work, following ATO guidelines.<br>
    - **Self-Education:** Courses that enhance skills for your current job or increase your income in your current role.<br>
    - **Tools and Equipment:** Work-related items; immediate deduction if under $300, or depreciation for more expensive items.<br>
    <br>
    **🚫 Non-Deductible Items:**<br>
    - **Personal Commutes:** Regular trips between home and work.<br>
    - **Employer-Provided Items:** Any expenses paid or reimbursed by your employer.<br>
    - **General Clothing:** Conventional clothing like business attire.<br>
    - **Personal Expenses:** Subscriptions, childcare, and fines.<br>
    <br>
    **📜 Summary**<br>
    Only claim expenses directly related to earning your income, keep records, and avoid claiming personal or employer-reimbursed costs. This ensures compliance and maximizes your deductions.
    """
    st.session_state.response_rag_displayed = True  # 이미 표시되었음을 기록

# 이전에 출력한 내용을 유지
if "response_rag_text" in st.session_state:
    st.write(st.session_state.response_rag_text, unsafe_allow_html=True)

# 챗봇 섹션을 텍스트박스 안에서 독립적으로 운영
with st.expander("Open Chatbot"):
    # 챗봇 메시지 관리
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": f"You are a helper for Australian Tax Refund, especially connecting occupations to deduction lists. The customer's job title is: {occupation}.",
            },
            {
                "role": "assistant",
                "content": "From your occupation, I can suggest some potential deductions. Would you like to know?",
            },
        ]

    # 이전 메시지 출력 (시스템 메시지는 제외)
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.chat_message(msg["role"]).write(msg["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # 챗봇 응답 처리
        pb = Predibase(api_token="pb_DxAFlDvTXviUE9BQ3iyPCw")

        # Predibase 모델 설정
        adapter_id = "Occup-deduc-guides-model/11"
        lorax_client = pb.deployments.client("solar-1-mini-chat-240612")

        response = lorax_client.generate(
            prompt,
            adapter_id=adapter_id,
            max_new_tokens=1000,
        ).generated_text

        # 모델 응답 처리 및 출력
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
