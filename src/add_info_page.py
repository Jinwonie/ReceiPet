import streamlit as st
from conf import Config
from src import reset_func, generate_perplexity_question, question_to_answer

# 이 코드는 receipt_submit_state또는 pass_submit_state의 영향을 받습니다.
if ("receipt_submit_state" in st.session_state and st.session_state.receipt_submit_state) or ("pass_submit_state" in st.session_state and st.session_state.pass_submit_state):
    with st.form('add_information_form'):
        st.title("➕ 추가 정보 입력하기")
        st.markdown("""추가로 입력하고 싶은 재료가 있나요❓<br>
                    이곳에서 자유롭게 추가하고 싶은 재료를 입력해주세요❗<br>
                    또한, 알레르기가 있어서 먹지 못하는 재료나 넣고 싶지 않은 재료가 있다면 입력해주세요❗""", unsafe_allow_html=True)
        
        if "finish_receipt" in st.session_state and st.session_state.finish_receipt:
            st.header("🔍 영수증 최종 수정 결과")
            st.write(f"{st.session_state.get('finish_receipt', '')}")

            st.write("")

            st.subheader('📝 추가 재료 입력')
            # 추가 재료를 입력할 수 있는 공간을 생성합니다.
            st.session_state['add_ingredients'] = st.text_area('여기에 재료를 추가해주세요.')

        else:
            st.write("")

            st.subheader('재료를 입력해주세요.')

            st.write("")

            st.subheader('재료 입력')
            # 추가 재료를 입력할 수 있는 공간을 생성합니다.
            st.session_state['add_ingredients'] = st.text_area('여기에 재료를 입력해주세요.')

        st.subheader('알레르기 및 금지 재료 정보 입력')
        # 알레르기 유발 재료 및 레시피에서 제외할 재료를 입력할 수 있는 공간을 생성합니다.
        st.session_state['sub_ingredients'] = st.text_area('알레르기를 유발하는 재료 혹은 넣고 싶지 않은 재료를 입력하세요.')

        finish_write = st.form_submit_button('작성완료')
        if finish_write:
            st.session_state["finish_write_state"] = True
            st.session_state['add_information_state'] = False
            st.rerun()
###############################################################################################################################################

##############################################################추가 내용 확인 코드###############################################################
# 추가 내용이 잘 작성되었는지 확인할 수 있는 폼을 생성합니다.(이 코드는 finish_write_state의 영향을 받음)
if 'finish_write_state' in st.session_state and st.session_state.finish_write_state:
    with st.form('add_information_confirm'):
        st.subheader("추가 정보 확인")

        st.write("")

        st.markdown(f'''
                    추가 재료: {st.session_state.get('add_ingredients', '없음')}<br><br>
                    알레르기 및 금지 재료: {st.session_state.get('sub_ingredients', '없음')}<br><br>
                    선택하신 정보가 맞습니까?<br>
                    ''', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 15])
        with col1:
            ans_yes = st.form_submit_button('예')
        with col2:
            ans_no = st.form_submit_button('아니요')

        # 예를 누르면 add_information_state 상태를 True로, 아니요를 누르면 add_information_state 상태를 False로 설정합니다.
        # 이 코드에 나오는 항목들을 지우고 다음 항목을 보여주게 하기 위함
        if ans_yes:
            st.session_state['add_information_state'] = True
            st.session_state['finish_write_state'] = False
            st.rerun()
        if ans_no:
            st.session_state['add_information_state'] = False
            st.session_state['finish_write_state'] = False
            st.rerun()
###############################################################################################################################################

##############################################################최종 내용 확인 코드###############################################################
# 최종 작성된 내용을 확인할 수 있는 폼을 생성합니다.
if 'add_information_state' in st.session_state and st.session_state.add_information_state:
    with st.form('final_confirm'):
        st.write("선택하신 최종 정보입니다.")
        st.write("")
        st.markdown(f"1. 영수증 내 물품 목록: {st.session_state.get('finish_receipt', '없음')}", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"2. 추가 재료: {st.session_state.get('add_ingredients', '없음')}", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"3. 알레르기 및 금지 재료: {st.session_state.get('sub_ingredients', '없음')}", unsafe_allow_html=True)
        st.markdown("내용이 일치한다면 '레시피 추천 받기' 버튼을 눌러 레시피 추천을 받으세요!<br>내용이 일치하지 않는다면 내용을 수정하세요.<br>", unsafe_allow_html=True)

###############################################################레시피 추천 코드################################################################
# 내용이 일치한다면 recommend_recipe 버튼을 눌러서 레시피 추천을 받을 수 있게 됩니다.
        recommend_recipe = st.form_submit_button('레시피 추천 받기')
        if recommend_recipe:
            st.session_state["recommend_recipe_state"] = True

        if "recommend_recipe_state" in st.session_state and st.session_state.recommend_recipe_state:
                with st.spinner('레시피 추천 중...'):
                    question = generate_perplexity_question(st.session_state.get('finish_receipt', ''), st.session_state.get('add_ingredients', ''),\
                        st.session_state.get('sub_ingredients', ''))
                    st.session_state["recommend_recipe"] = question_to_answer(question, st.session_state.get("perplexity_api_key", ""))
                    st.switch_page(Config.FOURTH_PAGE_DIR)
###############################################################################################################################################

if "receipt_submit_state" in st.session_state and st.session_state.receipt_submit_state:
    col1, col2 = st.columns([3, 8]) # 3:8의 비율을 가집니다.(자유롭게 설정 가능)
    with col1:
        if st.button("영수증 재수정하기", key="reset_edit_btn", icon="🧾"):
            st.session_state["finish_write_state"] = False
            st.session_state["edit_state"] = False
            st.switch_page(Config.SECOND_PAGE_DIR)
    with col2:
        if st.button("처음으로 돌아가기", key="reset_btn", icon="🔙"):
            st.session_state["reset_state"] = True
        if "reset_state" in st.session_state and st.session_state.reset_state:
            reset_func()
else:
    if st.button("처음으로 돌아가기", key="reset_btn", icon="🔙"):
        st.session_state["reset_state"] = True
    if "reset_state" in st.session_state and st.session_state.reset_state:
        reset_func()
