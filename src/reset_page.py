import streamlit as st
from conf import Config

def reset_func():
    st.write("⚠️ 클릭 시 초대코드를 다시 입력해야하며, 다시 이용할 경우 이용횟수가 하나 차감됩니다. 그래도 진행하시겠습니까?")
    col1, col2 = st.columns([1, 13])
    with col1:
        yes_btn = st.button("예")
    with col2:
        no_btn = st.button("아니요")

    if yes_btn:
        st.session_state.clear()
        st.switch_page(Config.FIRST_PAGE_DIR)
    if no_btn:
        st.session_state["reset_state"] = False
        st.rerun()
