import streamlit as st
from src import reset_func

if "recommend_recipe" in st.session_state and st.session_state.recommend_recipe:
    st.write('다음은 추천 레시피입니다.')
    st.write(st.session_state.get("recommend_recipe", ""))
    
    if st.button("처음으로 돌아가기", key="reset_btn", icon="🔙"):
        st.session_state["reset_state"] = True
    if "reset_state" in st.session_state and st.session_state.reset_state:
        reset_func()
