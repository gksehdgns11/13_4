
import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(
    page_title="졸림 레이더",
    page_icon="🌙",
    layout="wide"
)

SUBJECTS = [
    "국어", "영어", "수학", "사회", "과학",
    "한국사", "정보", "체육", "음악", "미술", "기타"
]

SLEEP_LABELS = {
    0: "😎 아주 맑음",
    1: "🙂 거의 안 졸림",
    2: "😐 조금 졸림",
    3: "🥱 꽤 졸림",
    4: "😴 많이 졸림",
    5: "🫠 눈을 뜨기 힘듦"
}

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(120deg, #e8f3ff, #f2edff);
    border: 1px solid #dce7fa;
}
.hero h1 {
    color: #1f3155;
}
</style>
""", unsafe_allow_html=True)

if "records" not in st.session_state:
    st.session_state.records = []


def recommend(sleep, focus):
    if sleep <= 1 and focus >= 4:
        return (
            "🟢 도전 모드",
            "심화 문제, 발표, 토론 활동을 추천합니다."
        )
    elif sleep <= 2:
        return (
            "🟢 기본 수업",
            "핵심 개념을 정리하고 확인 문제를 풀어보세요."
        )
    elif sleep == 3:
        return (
            "🟡 참여형 수업",
            "미니 퀴즈, 짝 설명, 예시 문제 풀이를 추천합니다."
        )
    elif sleep == 4:
        return (
            "🟠 활동 전환",
            "설명을 줄이고 질문이나 참여형 활동을 넣어보세요."
        )
    else:
        return (
            "🔴 부담 낮추기",
            "핵심 내용을 나누어 설명하고 짧은 휴식을 고려하세요."
        )


st.markdown("""
<div class="hero">
    <h1>🌙 졸림 레이더</h1>
    <p>과목별 졸림을 기록하고 수업에 맞는 집중 전략을 찾아보세요!</p>
</div>
""", unsafe_allow_html=True)

st.write("")

record_tab, dashboard_tab, guide_tab = st.tabs([
    "✍️ 졸림 기록",
    "📊 분석 대시보드",
    "💡 사용 안내"
])

# -----------------------------
# 1. 졸림 기록 화면
# -----------------------------
with record_tab:
    left, right = st.columns(2)

    with left:
        st.subheader("오늘의 졸림 기록")

        with st.form("sleep_form"):
            subject = st.selectbox("과목 선택", SUBJECTS)
            record_date = st.date_input("날짜", value=date.today())

            sleep = st.slider(
                "졸림 정도",
                min_value=0,
                max_value=5,
                value=2
            )

            st.write("현재 상태:", SLEEP_LABELS[sleep])

            focus = st.slider(
                "집중도",
                min_value=1,
                max_value=5,
                value=3
            )

            memo = st.text_input(
                "메모 (선택)",
                placeholder="예: 점심시간 직후"
            )

            submitted = st.form_submit_button(
                "기록 저장하기",
                type="primary",
                use_container_width=True
            )

        if submitted:
            try:
                record = {
                    "날짜": record_date.isoformat(),
                    "시간": datetime.now().strftime("%H:%M:%S"),
                    "과목": subject,
                    "졸림 점수": int(sleep),
                    "졸림 상태": SLEEP_LABELS[sleep],
                    "집중도": int(focus),
                    "메모": memo.strip()
                }

                st.session_state.records.append(record)
                st.success("기록이 저장되었습니다!")

            except (ValueError, TypeError):
                st.error("기록 저장 중 오류가 발생했습니다.")

    with right:
        st.subheader("📌 추천 수업 방식")

        plan, action = recommend(sleep, focus)

        st.markdown(f"### {plan}")
        st.write(action)

        st.info(
            "졸림이 높을 때는 수업을 무조건 어렵게 하기보다 "
            "설명 시간과 활동 방식을 조절하는 것이 좋습니다."
        )

# -----------------------------
# 2. 분석 대시보드
# -----------------------------
with dashboard_tab:
    st.subheader("📊 과목별 졸림 분석")

    if not st.session_state.records:
        st.info(
            "아직 기록이 없습니다. "
            "졸림 기록 탭에서 첫 기록을 추가해 보세요."
        )

    else:
        df = pd.DataFrame(st.session_state.records)

        average = df["졸림 점수"].mean()

        subject_average = (
            df.groupby("과목")["졸림 점수"]
            .mean()
            .sort_values(ascending=False)
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("평균 졸림", f"{average:.1f} / 5")
        col2.metric("가장 졸린 과목", subject_average.index[0])
        col3.metric("총 기록 수", f"{len(df)}회")

        st.write("### 과목별 평균 졸림 점수")
        st.bar_chart(subject_average)

        st.write("### 기록 목록")
        st.dataframe(
            df.sort_values(
                ["날짜", "시간"],
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📥 기록 CSV 다운로드",
            data=csv_data,
            file_name="sleep_class_records.csv",
            mime="text/csv"
        )

        if st.button("🗑️ 모든 기록 삭제"):
            st.session_state.records = []
            st.rerun()

        st.caption(
            "기록은 현재 세션에 저장됩니다. "
            "필요한 자료는 CSV로 다운로드하세요."
        )

# -----------------------------
# 3. 사용 안내
# -----------------------------
with guide_tab:
    st.subheader("💡 졸림 점수 안내")

    guide = pd.DataFrame([
        {"점수": 0, "상태": SLEEP_LABELS[0], "추천": "심화 문제와 토론"},
        {"점수": 1, "상태": SLEEP_LABELS[1], "추천": "평소 수업 진행"},
        {"점수": 2, "상태": SLEEP_LABELS[2], "추천": "핵심 개념 정리"},
        {"점수": 3, "상태": SLEEP_LABELS[3], "추천": "미니 퀴즈와 질문"},
        {"점수": 4, "상태": SLEEP_LABELS[4], "추천": "참여형 활동"},
        {"점수": 5, "상태": SLEEP_LABELS[5], "추천": "핵심 내용 분할, 휴식 고려"}
    ])

    st.dataframe(
        guide,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    ### 사용 방법

    1. 수업 중 과목과 졸림 정도를 입력합니다.
    2. 집중도까지 입력하면 추천 수업 방식을 확인할 수 있습니다.
    3. 여러 번 기록한 뒤 과목별 평균 졸림을 비교합니다.
    4. 결과를 참고해 수업 진행 방식을 조절합니다.
    """)

    st.warning(
        "이 앱은 의료적 진단 도구가 아닙니다. "
        "졸림이 지속되면 충분한 수면과 휴식을 챙기세요."
    )

st.divider()
st.caption("졸림 레이더 | 과목별 집중 관리 도우미")

