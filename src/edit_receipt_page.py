import streamlit as st
from conf import Config
from src import reset_func

################################################################영수증 내용 수정################################################################
# receipt_text가 st.session_state에 있고, st.session_state['receipt_text]에 데이터가 있는 경우 하위 코드를 실행합니다.
if 'receipt_text' in st.session_state and st.session_state['receipt_text']:
    st.title("🧾 영수증 내용 수정하기")
    # 버튼별 상태 관리 초기화(토글)
    if "toggle_state" not in st.session_state:
        st.session_state["toggle_state"] = {}
    if "delete_confirm" not in st.session_state:
        st.session_state["delete_confirm"] = None

    # 사용자가 어떻게 사용하면 되는지 설명서를 작성합니다.
    st.markdown(f'''
                영수증 내용 중 수정하고 싶은 항목이 있으신가요❓<br>
                품목에 해당하는 버튼을 클릭하고 수정해주세요❗<br>
                수정할 때는 "수정" 버튼을 눌러주세요❗<br>
                최종 수정이 완료되면 "수정완료" 버튼을 눌러주세요😊<hr>
                ''', unsafe_allow_html=True)

    st.header('🔍 영수증 항목 추출 결과')
    st.write(st.session_state.get("receipt_text", ""))
    st.subheader("아래 항목 중 수정하고 싶은 항목을 클릭하여 수정해주세요!")
    
    value_lst = st.session_state.get("receipt_text", "").strip().split(", ")

    for value in value_lst:
        # 버튼 생성
        if st.button(value, key=f"{value}_btn", icon="🛒"):
            # 버튼 클릭 시 해당 항목의 상태를 True로 설정
            st.session_state["toggle_state"][value] = not st.session_state["toggle_state"].get(value, False)

        # 클릭된 버튼 아래에 text_area 표시
        if st.session_state["toggle_state"].get(value, False):
            new_value = st.text_input(f"수정할 내용을 입력하세요.", key=f"text_input{value}")
            col1, col2 = st.columns([2, 9])
            with col1:
                if st.button("수정하기", key=f"save_{value}", icon="✔️"):
                    # 리스트에서 수정된 값 반영
                    index = value_lst.index(value)
                    value_lst[index] = new_value
                    # 상태 초기화 및 업데이트
                    st.session_state["receipt_text"] = ", ".join(value_lst)
                    st.session_state["toggle_state"][value] = False
                    st.rerun()
            with col2:
                if st.button("삭제하기", key=f"delete_{value}", icon="✖️"):
                    st.session_state["delete_confirm"] = value
                    
        # 삭제 확인 창
        if st.session_state["delete_confirm"] == value:
            st.write(f"⚠️ 삭제를 할 경우 해당 항목이 사라집니다. '{value}' 항목을 삭제하시겠습니까?")
            col1, col2 = st.columns([1, 15])
            with col1:
                if st.button("예", key=f"agree_del_{value}"):
                    index = value_lst.index(value)
                    del value_lst[index]
                    st.session_state["receipt_text"] = ", ".join(value_lst)
                    st.session_state["delete_confirm"] = None  # 상태 초기화
                    st.rerun()
            with col2:
                if st.button("아니요", key=f"disagree_del_{value}"):
                    st.session_state["delete_confirm"] = None  # 상태 초기화
                    st.rerun()

    st.markdown("---", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 8])
    with col1:
        if st.button("수정완료", key="complete_btn", icon="✔️"):
        # 수정완료 버튼을 누를 경우 최종 결과를 알려줍니다.
            st.session_state['finish_receipt'] = st.session_state.get('receipt_text', '')
            st.session_state["edit_state"] = True
        if "edit_state" in st.session_state and st.session_state.edit_state:
            st.switch_page(Config.THIRD_PAGE_DIR)
    with col2:
        if st.button("처음으로 돌아가기", key="reset_btn", icon="🔙"):
            st.session_state["reset_state"] = True
        if "reset_state" in st.session_state and st.session_state.reset_state:
            reset_func()
