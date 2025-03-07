import streamlit as st

class Config:
    BASE_DIR = st.secrets["BASE_DIR"]
    LOGO_DIR = f"{BASE_DIR}/resource/ReceiPet.png"
    SQL_DIR = f"{BASE_DIR}/sql/INVITATION_CODE.db"
    FIRST_PAGE_DIR = f"{BASE_DIR}/src/read_receipt_page.py"
    SECOND_PAGE_DIR = f"{BASE_DIR}/src/edit_receipt_page.py"
    THIRD_PAGE_DIR = f"{BASE_DIR}/src/add_info_page.py" 
    FOURTH_PAGE_DIR = f"{BASE_DIR}/src/recommend_ recipe_page.py"

class GPT:
    GPT_URL = "https://api.openai.com/v1/chat/completions"
    GPT_MODEL_NAME = "gpt-4o"
    GPT_SYSTEM = "You are an ocr model."
    GPT_QUESTION = """Below is a list of items from the receipt: Extract only the name of each item and answer in comma-separated format.
    If the same item exists, print it only once.
    If it is not in receipt format, print the message, '이미지 분석 결과, 영수증이 아닌 것으로 보입니다. 영수증 이미지를 다시 한번 업로드해주세요.'"""
    
class PERPLEXITY:
    PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"
    PERPLEXITY_MODEL_NAME = "llama-3.1-sonar-small-128k-online"