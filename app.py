import streamlit as st
from conf import Config

if __name__ == "__main__":
    # 홈페이지 제목과 아이콘 설정
    st.set_page_config(page_title="ReceiPet", page_icon="🍴")
    
    # 1~3번 페이지의 경로 및 제목+아이콘 설정
    first_page = st.Page(Config.FIRST_PAGE_DIR, title="Read Reciept", icon="🧾")
    second_page = st.Page(Config.SECOND_PAGE_DIR, title="Edit Receipt", icon="📝")
    third_page = st.Page(Config.THIRD_PAGE_DIR, title="Add Information", icon="➕")
    fourth_page = st.Page(Config.FOURTH_PAGE_DIR, title="Recommend Recipe", icon="🍽️")
    
    # 페이지를 스위칭할 수 있도록 navigation에 페이지 저장, position을 "hidden"으로 설정하여 side navigation 제거
    pg = st.navigation([first_page, second_page, third_page, fourth_page], position="hidden")
    pg.run()
