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
# 구역 2. 일관객 합계 상위 5편의 날짜별 일관객 비교
# -----------------------------
st.header("구역 2. 일관객 합계 상위 5편 비교")

# 영화별 일관객 합계 계산 후 상위 5편 선정
top5_movies = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index.tolist()
)

top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 수",
)
fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화명 (클릭해서 켜고 끄기)",
)

st.plotly_chart(fig2, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 한 문장으로 해석을 적어보세요)")


# -----------------------------
# 구역 3. 날짜별 10위권 일관객 합계 (영역 그래프)
# -----------------------------
st.header("구역 3. 날짜별 10위권 일관객 합계")

daily_total = df.groupby("날짜")["일관객"].sum().reset_index()

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 영화 일관객 합계",
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 일관객: %{y:,}명<extra></extra>"
)
fig3.update_layout(xaxis_title="날짜", yaxis_title="합계 일관객 수(명)")

# 합계가 가장 컸던 날 3일 찾기
top3_days = daily_total.sort_values("일관객", ascending=False).head(3)

for _, row in top3_days.iterrows():
    fig3.add_scatter(
        x=[row["날짜"]],
        y=[row["일관객"]],
        mode="markers+text",
        marker=dict(size=10, color="red"),
        text=[row["날짜"].strftime("%Y-%m-%d")],
        textposition="top center",
        showlegend=False,
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 일관객: %{y:,}명<extra></extra>",
    )

st.plotly_chart(fig3, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 한 문장으로 해석을 적어보세요)")


# -----------------------------
# 구역 4. 일관객 합계 TOP 10 (가로 막대그래프)
# -----------------------------
st.header("구역 4. 일관객 합계 TOP 10")

movie_stats = (
    df.groupby("영화명")
    .agg(합계일관객=("일관객", "sum"), 순위권진입일수=("날짜", "count"))
    .reset_index()
    .sort_values("합계일관객", ascending=False)
    .head(10)
)

# 가로 막대그래프에서 위쪽에 큰 값이 오도록 정렬 순서 지정
movie_stats = movie_stats.sort_values("합계일관객", ascending=True)

fig4 = px.bar(
    movie_stats,
    x="합계일관객",
    y="영화명",
    orientation="h",
    custom_data=["순위권진입일수"],
    title="일관객 합계 TOP 10",
)
fig4.update_traces(
    hovertemplate=(
        "영화: %{y}<br>"
        "합계 일관객: %{x:,}명<br>"
        "10위권 진입 일수: %{customdata[0]}일<extra></extra>"
    )
)
fig4.update_layout(
    xaxis_title="합계 일관객 수(명)",
    yaxis_title="영화명",
    yaxis=dict(categoryorder="total ascending"),
)

st.plotly_chart(fig4, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 한 문장으로 해석을 적어보세요)")


# -----------------------------
# 구역 5. 월×요일별 일관객 합계 히트맵
# -----------------------------
st.header("구역 5. 월×요일별 일관객 합계")

heatmap_df = df.copy()
heatmap_df["월"] = heatmap_df["날짜"].dt.month
heatmap_df["요일번호"] = heatmap_df["날짜"].dt.dayofweek  # 월요일=0, 일요일=6

요일_이름 = ["월", "화", "수", "목", "금", "토", "일"]
heatmap_df["요일"] = heatmap_df["요일번호"].map(dict(enumerate(요일_이름)))

pivot = (
    heatmap_df.groupby(["월", "요일"])["일관객"]
    .sum()
    .reset_index()
    .pivot(index="요일", columns="월", values="일관객")
    .reindex(요일_이름)  # 월요일부터 일요일 순서로 정렬
)

fig5 = px.imshow(
    pivot,
    color_continuous_scale="Reds",
    aspect="auto",
    labels=dict(x="월", y="요일", color="일관객 합계"),
    title="월×요일별 일관객 합계 히트맵",
)
fig5.update_traces(
    hovertemplate="월: %{x}월<br>요일: %{y}요일<br>합계 일관객: %{z:,}명<extra></extra>"
)
fig5.update_xaxes(dtick=1, title="월")
fig5.update_yaxes(title="요일")

st.plotly_chart(fig5, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 한 문장으로 해석을 적어보세요)")
