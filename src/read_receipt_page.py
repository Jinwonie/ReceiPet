import sqlite3
import streamlit as st
from conf import Config
from src import ticket_office, receipt_to_text, receipt_preprocessing

# api_key와 DB 연결을 위해 필요한 session을 가져옵니다.
if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = st.secrets["OPENAI_API_KEY"]
if "perplexity_api_key" not in st.session_state:
    st.session_state["perplexity_api_key"] = st.secrets["PERPLEXITY_API_KEY"]

# con & cursor는 하위 코드의 같은 thread에서 실행되어야 하기 때문에 실행 시마다 저장할 수 있도록 합니다.
st.session_state["con"] = sqlite3.connect(Config.SQL_DIR)
st.session_state["cursor"] = st.session_state.get("con", "").cursor()

# 제목에 이미지와 제목 명을 합치기 위해 st.columns 객체를 생성합니다.
col1, col2 = st.columns([1, 5]) # 1:5의 비율을 가집니다.(자유롭게 설정 가능)
with col1:
    st.image(Config.LOGO_DIR)
with col2:
    st.title("ReceiPet")

# 초대코드를 작성하는 사이드 바 폼입니다.
with st.sidebar.form(key="inv_code_ckecker"):
    st.session_state["invitation_code"] = st.text_input("Invitation Code", value=st.session_state.get("invitation_code", ""))
    inv_code_submit = st.form_submit_button("제출", icon="✔️")

# inv_code_submit 버튼을 활성화 했을 때 초대코드가 DB 내에 있는지 확인합니다.
if inv_code_submit and ("invitation_code" in st.session_state and st.session_state.invitation_code):
    st.session_state["authority_state"], st.session_state["print_state"], st.session_state["alert"] = ticket_office(st.session_state.get("con", ""), st.session_state.get("cursor", ""), st.session_state.get("invitation_code", ""))

# print_state와 invitation_code가 활성화 되어 있을 때 초대코드의 사용여부를 출력합니다.
if ("print_state" in st.session_state and st.session_state.print_state) and ("invitation_code" in st.session_state and st.session_state.invitation_code):
    st.sidebar.markdown(st.session_state.get("alert", ""), unsafe_allow_html=True)

# ReceiPet을 쉽게 이용할 수 있도록 markdown으로 설명서를 제공합니다.
st.subheader("ReceiPet 이용법")
st.markdown("""
            1. 영수증을 업로드합니다.<br>
            2. 수정할 내용이 있다면 수정합니다.<br>
            3. 추가 정보를 입력합니다.<br>
            4. 레시피를 추천받습니다.<br>
            """, unsafe_allow_html=True)
st.write("오늘도 즐거운 식사 되세요!👨🏼‍🍳🍳")

#################################################################내용 추출 코드#################################################################
# file_uploader로 바이트 스트림 파일을 받습니다.
st.session_state["receipt_img"] = st.file_uploader("영수증을 올려주세요", type=["png", "jpg", "jpeg"])

# 이미지가 들어오면 어떤 이미지인지 보여줍니다.
if "receipt_img" in st.session_state and st.session_state.receipt_img:
    st.image(st.session_state.get("receipt_img", ""))

# 영수증 읽기 버튼과 영수증 없이 진행 버튼을 생성합니다.
if st.button("영수증 읽기", key="receipt_submit_btn"):
    st.session_state["receipt_submit_state"] = True

# 영수증 없이 진행 버튼을 누르면 pass_submit_state 버튼이 활성화됩니다.
if st.button("영수증 없이 진행", key="pass_submit_btn"):
    st.session_state["pass_submit_state"] = True

# 초대코드를 입력하지 않으면 경고가 나오도록 설정합니다.
if not st.session_state["invitation_code"]:
    st.warning("초대코드를 입력해주세요", icon="⚠")
    
# 영수증 읽기 버튼을 클릭하면 이미지를 분석하고 OCR합니다.(초대코드가 활성화되어 있어야 함)
if ("receipt_submit_state" in st.session_state and st.session_state.receipt_submit_state) and ("authority_state" in st.session_state and st.session_state["authority_state"]):
    with st.spinner('영수증을 읽는 중입니다.'):
        # 이미지를 전처리하여 base64로 encoding 합니다.
        base64_image = receipt_preprocessing(st.session_state.get("receipt_img", ""))
        # LLM을 통해 OCR 된 항목 추출 결과를 st.session_state["receipt_text"]에 저장합니다.
        st.session_state["receipt_text"] = receipt_to_text(base64_image, st.session_state.get("openai_api_key", ""))
        # 만약 OCR 결과 영수증이 아닌 것으로 판단되면 하위 코드가 실행됩니다.
        if st.session_state.get("receipt_text", "") == "이미지 분석 결과, 영수증이 아닌 것으로 보입니다. 영수증 이미지를 다시 한번 업로드해주세요.":
            st.write(st.session_state.get("receipt_text", ""))
            st.session_state["receipt_submit_state"] = False
        # 분석이 완료되면 다음 페이지로 넘어갑니다.
        else:
            st.switch_page(Config.SECOND_PAGE_DIR)

# 영수증 없이 진행 버튼을 누르면 receipt_text 상태에 빈 문자열을 저장합니다.(초대코드가 활성화되어 있어야 함)
if ("pass_submit_state" in st.session_state and st.session_state.pass_submit_state) and ("authority_state" in st.session_state and st.session_state["authority_state"]):
    st.session_state["receipt_text"] = ""
    st.switch_page(Config.THIRD_PAGE_DIR)
