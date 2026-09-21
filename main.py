import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# -----------------------------
# 데이터 불러오기 & 전처리
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 열 이름을 코드에서 다루기 쉬운 영문명으로 매핑 (원본 CSV 열 순서 기준)
    df.columns = [
        "날짜", "순위", "영화코드", "영화명",
        "일관객", "누적관객", "스크린수", "상영횟수"
    ]

    # 날짜(하이픈 없는 여덟 자리 숫자) -> datetime 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

    return df


df = load_data()


# -----------------------------
# 구역 1. 영화별 일관객 변화 (시간에 따른 흐름)
# -----------------------------
st.header("구역 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list)

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 날짜별 일관객 수 변화",
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig1.update_layout(xaxis_title="날짜", yaxis_title="일관객 수(명)")

st.plotly_chart(fig1, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 한 문장으로 해석을 적어보세요)")


# -----------------------------
# 구역 2. (다음 그래프 추가 예정)
# -----------------------------
st.header("구역 2. (준비 중)")
st.caption("다음 그래프가 여기에 추가될 예정입니다.")


# -----------------------------
# 구역 3. (다음 그래프 추가 예정)
# -----------------------------
st.header("구역 3. (준비 중)")
st.caption("다음 그래프가 여기에 추가될 예정입니다.")
