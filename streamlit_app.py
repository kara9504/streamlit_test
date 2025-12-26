import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 페이지 설정 (웹사이트 제목)
st.set_page_config(page_title="우리들의 공유 달력", layout="centered")

st.title("📅 전시회 공유 달력 & 방명록")
st.write("원하는 날짜에 일정을 남겨보세요. 모든 사람과 공유됩니다!")

# 2. 구글 스프레드시트 연결 설정
# (나중에 Streamlit Cloud 설정에서 시트 주소를 넣을 거예요)
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 데이터 불러오기 함수
def load_data():
    # 구글 시트의 데이터를 읽어옵니다. (기본적으로 첫 번째 시트)
    return conn.read()

# 4. 데이터 저장하기 함수
def save_data(date, content):
    existing_data = load_data()
    # 새 일정을 데이터프레임으로 만들기
    new_row = pd.DataFrame([{"날짜": str(date), "일정": content}])
    # 기존 데이터에 합치기
    updated_data = pd.concat([existing_data, new_row], ignore_index=True)
    # 구글 시트에 다시 업데이트하기
    conn.update(data=updated_data)

# --- 화면 구성 시작 ---

# 5. 일정 입력창 (노션처럼 깔끔하게 접어두기)
with st.expander("➕ 여기에 새로운 일정을 추가하세요!"):
    with st.form("input_form"):
        new_date = st.date_input("날짜를 선택하세요")
        new_content = st.text_input("일정 내용을 적어주세요 (예: 지민이 다녀감!)")
        submit_button = st.form_submit_button("일정 등록하기")

        if submit_button:
            if new_content:
                save_data(new_date, new_content)
                st.success("성공적으로 등록되었습니다! 화면을 새로고침해보세요.")
                st.balloons() # 축하 효과
            else:
                st.warning("내용을 입력해주세요!")

# 6. 등록된 일정 보여주기
st.subheader("📌 친구들이 남긴 일정 목록")
data = load_data()

if not data.empty:
    # 날짜순으로 정렬해서 보여주기
    data = data.sort_values(by="날짜", ascending=True)
    st.table(data) # 표 형태로 예쁘게 출력
else:
    st.info("아직 등록된 일정이 없어요. 첫 번째 주인공이 되어보세요!")

# 7. 간단한 달력 모양 (참고용)
import calendar
from datetime import datetime
yy, mm = datetime.now().year, datetime.now().month
st.sidebar.text(calendar.month(yy, mm))
