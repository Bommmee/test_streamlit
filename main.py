import streamlit as st
import os
from predibase import Predibase, FinetuningConfig, DeploymentConfig

st.set_page_config(page_title="User/Company Multi-Page App", layout="wide")

# 멀티페이지 구성
# page = st.sidebar.selectbox("Select a page:", ["User", "Company"])

# if page == "User":
st.title("Personalise your 2023-24 return")
# 사용자 이름 입력
name = st.text_input("Enter your Name", key="name")

# TFN 입력
tfn = st.text_input("Enter your Tax File Number (TFN)", key="tfn")

# 질문 1: Australian resident for tax purposes
st.markdown(
    "### 1. Were you an Australian resident for tax purposes from 1 July 2023 to 30 June 2024? [learn more](https://www.ato.gov.au/single-page-applications/calculatorsandtools#AreYouAResident/questions)"
)
resident_status = st.radio("", ["Yes", "No"], key="resident_status")

# 질문 2: Spouse status
st.markdown(
    "### 2. Did you have a spouse at any time between 1 July 2023 and 30 June 2024?"
)
spouse_status = st.radio("", ["Yes", "No"], key="spouse_status")

st.markdown(
    "### Self Assessment [more information](https://www.ato.gov.au/individuals-and-families/your-tax-return/instructions-to-complete-your-tax-return/mytax-instructions/supporting-documents-for-my-tax/before-you-begin#Selfassessment)"
)

st.info(
    "We use data from a range of sources to pre-fill your tax return. Based on available pre-fill information, we may have made some selections for you. Make other selections that may apply to include them in your tax return."
)
st.markdown("[Video Tutorials](https://ato.publish.viostream.com/mytax)")

# 수입 및 소득 체크리스트
st.markdown(
    "### 3. You received salary, wages or other income on an income statement/payment summary, Australian Government payments, or First home super saver (FHSS) scheme payment",
)

# 소항목 체크박스
salary_wages = st.checkbox(
    "Salary, wages, allowances, tips, bonuses etc. (including lump sum A, B, D or E payments)",
    key="salary_wages",
)
government_payments = st.checkbox(
    "Australian Government payments such as JobSeeker, Youth Allowance, Austudy, pensions etc.",
    key="government_payments",
)
etp = st.checkbox("Employment termination payments (ETP)", key="etp")
foreign_income = st.checkbox(
    "Foreign employment income (on an income statement/payment summary)",
    key="foreign_income",
)
attributed_income = st.checkbox(
    "Attributed personal services income (on a payment summary)",
    key="attributed_income",
)
fhss = st.checkbox("First home super saver (FHSS) scheme", key="fhss")

# 수퍼애뉴에이션 및 투자 소득
st.markdown(
    "### 4. You had income from Australian superannuation or annuity funds",
)
super_income = st.checkbox(
    "Check if you had income from Australian superannuation or annuity funds",
    key="super_income",
)

st.markdown(
    "### 5. You had Australian interest, or other Australian income or losses from investments or property",
)

# 소항목 체크박스
interest = st.checkbox("Interest", key="interest")
dividends = st.checkbox("Dividends", key="dividends")
rent_income = st.checkbox("Rent (Australian properties)", key="rent_income")
capital_gains = st.checkbox(
    "Capital gains or losses that are not from a managed fund or trust distribution",
    key="capital_gains",
)
capital_losses = st.checkbox(
    "Unapplied net capital losses from earlier years to carry forward but no CGT event this year",
    key="capital_losses",
)

st.markdown(
    "### 6. You had managed fund or trust distributions (including where distribution has capital gains and foreign income)",
)
managed_fund = st.checkbox(
    "Check if you had managed fund or trust distributions", key="managed_fund"
)

st.markdown(
    "### 7. You were a sole trader or had business income or losses or partnership distributions",
)
sole_trader = st.checkbox(
    "Check if you were a sole trader or had business income or losses or partnership distributions",
    key="sole_trader",
)

st.markdown("### 8. You had foreign income")
foreign_income_checkbox = st.checkbox(
    "Check if you had foreign income", key="foreign_income_checkbox"
)

# 기타 소득
st.markdown(
    "### 9. You had other income not listed above (including employee share schemes) [all other income](https://www.ato.gov.au/individuals-and-families/your-tax-return/instructions-to-complete-your-tax-return/mytax-instructions/2024/income/other-income)"
)
other_income = st.checkbox(
    "Check if you had other income not listed above", key="other_income"
)

# 공제 항목
st.markdown("### 10. You had deductions you want to claim")

# 소항목 체크박스
work_related_expenses = st.checkbox(
    "Work-related expenses - You must have salary or wages income",
    key="work_related_expenses",
)
working_from_home = st.checkbox(
    "This includes working from home expenses", key="working_from_home"
)
donations = st.checkbox(
    "Gifts, donations, interest, dividends, and the cost of managing your tax affairs",
    key="donations",
)
income_protection = st.checkbox(
    "Income protection, sickness and accident insurance premiums",
    key="income_protection",
)
other_deductions = st.checkbox("Other deductions", key="other_deductions")

# 이전 소득 연도의 손실
st.markdown(
    "### 12. You had tax losses of earlier income years [tax loses of earlier income years](https://www.ato.gov.au/individuals-and-families/your-tax-return/instructions-to-complete-your-tax-return/mytax-instructions/2024/tax-losses-of-earlier-income-years)"
)
tax_losses = st.checkbox(
    "Check if you had tax losses of earlier income years", key="tax_losses"
)

# 세액 공제 및 조정
st.markdown("### 13. You are claiming tax offsets or adjustments")
claiming_tax_offsets = st.checkbox(
    "Check if you are claiming tax offsets or adjustments",
    key="claiming_tax_offsets",
)

# Income statements and payment summaries
st.markdown("### 14. Income statements and payment summaries")
occupation = st.selectbox(
    "Occupation where you earned most income",
    [
        "Software Engineer",
        "Data Scientist",
        "System Administrator",
        "Network Engineer",
        "IT Support Specialist",
        "DevOps Engineer",
        "Cybersecurity Analyst",
        "Database Administrator",
        "Web Developer",
        "Cloud Solutions Architect",
        "IT Project Manager",
    ],
    key="occupation",
)
# Interest
st.markdown("### 15. Interest")
interest_banks = st.multiselect(
    "Select the banks where you received interest:",
    [
        "ANZ Bank",
        "Commonwealth Bank of Australia",
        "National Australia Bank",
        "Westpac Banking Corporation",
        "Macquarie Bank",
        "Bank of Queensland",
        "Bendigo and Adelaide Bank",
        "Suncorp Bank",
        "ASB Bank (New Zealand)",
        "BNZ (Bank of New Zealand)",
    ],
    key="interest_banks",
)

# Dividends
st.markdown("### 16. Dividends")
dividend_sources = st.multiselect(
    "Select the companies from which you received dividends:",
    [
        "Commonwealth Bank of Australia",
        "Westpac Banking Corporation",
        "National Australia Bank",
        "ANZ Bank",
        "Telstra",
        "Woolworths Group",
        "Coles Group",
        "BHP",
        "Rio Tinto",
        "Fortescue Metals Group",
    ],
    key="dividend_sources",
)

# Other income
st.markdown("### 17. Other income")
other_income_sources = st.multiselect(
    "Select other sources of income:",
    [
        "CBA (Commonwealth Bank of Australia)",
        "Westpac",
        "ANZ",
        "NAB",
        "AMP Limited",
        "Suncorp",
        "Medibank",
        "Insurance Australia Group (IAG)",
        "Macquarie Group",
        "QBE Insurance",
    ],
    key="other_income_sources",
)

# Income tests
st.markdown("### 18. Income tests")
num_dependent_children = st.number_input(
    "Number of dependent children", min_value=0, key="num_dependent_children"
)

# Medicare and private health insurance
st.markdown("### 19. Medicare and private health insurance")
medicare_exemption = st.selectbox(
    "Medicare levy exemption or reduction",
    ["None", "Full exemption", "Partial exemption"],
    key="medicare_exemption",
)
medicare_surcharge = st.selectbox(
    "Medicare levy surcharge",
    ["Liable for Medicare levy surcharge", "Not liable"],
    key="medicare_surcharge",
)
private_health_insurance = st.selectbox(
    "Private health insurance policies",
    ["Not provided", "Provided"],
    key="private_health_insurance",
)

# How did you complete this tax return?
st.markdown("### 20. How did you complete this tax return?")
tax_return_completion = st.radio(
    "How did you complete this tax return?",
    ["Prepared myself", "Tax Help volunteer"],
    key="tax_return_completion",
)

# Will you need to lodge an Australian tax return in future years?
st.markdown("### 21. Will you need to lodge an Australian tax return in future years?")
future_tax_return = st.radio(
    "Will you need to lodge an Australian tax return in future years?",
    ["Yes (or I’m unsure)", "No (this is my final return)"],
    key="future_tax_return",
)

# 영수증 이미지 업로드 섹션
st.title("Upload Your Receipts")
uploaded_files = st.file_uploader(
    "Choose receipt images",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg"],
    key="uploaded_files",
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption=uploaded_file.name)

# Tax estimate (this would typically be calculated and displayed, but we'll just leave a placeholder here)
st.markdown("## Tax estimate")
st.write(
    "Your tax estimate will be calculated and displayed here once all information is provided."
)

# # 챗봇 섹션
# st.title("Chatbot")
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [
#         {"role": "assistant", "content": "How can I help you?"}
#     ]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo", messages=st.session_state.messages
#     )
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)
pb = Predibase(api_token="pb_DxAFlDvTXviUE9BQ3iyPCw")  # "pb_DxAFlDvTXviUE9BQ3iyPCw")

# Predibase 모델 설정
adapter_id = "Occup-deduc-guides-model/11"  # 실제 사용 중인 모델의 어댑터 ID로 교체
lorax_client = pb.deployments.client(
    "solar-1-mini-chat-240612"
)  # 실제 클라이언트 설정으로 교체

# 챗봇 섹션
st.title("Refund Ranger Chatbot")

# 사용자에게 입력받을 occupation 변수
occupation = "Software Engineer"  # 예시로 occupation 변수를 설정

# 시스템 메시지 추가
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": f"You are a helper for Australian Tax Refund, especially connecting occupations to deduction lists. The customer's job title is: {occupation}.",
        },
        {
            "role": "system",
            "content": (
                f"According to the Australian Tax Office (ATO), the job title '{occupation}' must be classified into one of the following ATO occupation categories: "
                "Adult industry workers, Agricultural workers, Apprentices and trainees, Australian Defence Force members, "
                "Building and construction employees, Bus drivers, Call centre operators, Cleaners, Community support workers and direct carers, "
                "Doctor, specialist or other medical professionals, Factory workers, Fire fighters, Fitness and sporting industry employees, "
                "Flight crew, Gaming attendants, Guards and security employees, Hairdressers and beauty professionals, "
                "Hospitality industry employees, Lawyers, Meat workers, Media professionals, Mining site employees, Nurses and midwives, "
                "Paramedics, Performing artists, Pilots, Police officers, Professional sportspersons, Real estate employees, Recruitment consultants, "
                "Retail industry workers, Sales and marketing managers, Teachers and education professionals, Tradespersons, Train drivers, "
                "Travel agent employees, Truck drivers, IT Professionals, Office workers, Engineers. "
                "Please provide occupation category descriptions using full text labels and avoid numerical codes unless specifically requested."
            ),
        },
        {
            "role": "system",
            "content": (
                "When providing responses, base all answers strictly on the ATO's official individual tax refund guidelines. "
                "Do not reference any information that is not directly derived from the ATO's official documentation."
            ),
        },
        {
            "role": "assistant",
            "content": "How can I help you with your Occupation and Deduction?",
        },
    ]

# 이전 메시지 출력 (시스템 메시지는 제외)
for msg in st.session_state.messages:
    if msg["role"] != "system":  # 시스템 메시지를 출력하지 않음
        st.chat_message(msg["role"]).write(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Predibase 모델 호출
    response = lorax_client.generate(
        prompt,
        adapter_id=adapter_id,
        max_new_tokens=1000,  # 필요에 따라 조정 가능
    ).generated_text

    # 모델 응답 처리 및 출력
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
