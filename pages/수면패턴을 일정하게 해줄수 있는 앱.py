
import streamlit as st
from datetime import datetime, date, time, timedelta
import pandas as pd

st.set_page_config(
    page_title="수면 리듬",
    page_icon="🌙",
    layout="centered"
)

# ---------------- 디자인 ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #10172f 0%, #20284a 100%);
    color: #f8fafc;
}
h1, h2, h3, p, label {
    color: #f8fafc !important;
}
div[data-testid="stMetric"] {
    background: #293353;
    padding: 16px;
    border-radius: 16px;
    border: 1px solid #414d72;
}
div.stButton > button {
    border-radius: 12px;
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- 세션 데이터 ----------------
if "logs" not in st.session_state:
    st.session_state.logs = []

if "routine" not in st.session_state:
    st.session_state.routine = {}

# ---------------- 상단 화면 ----------------
st.title("🌙 수면 리듬")
st.write("고등학생을 위한 수면 습관 관리 도우미")
st.caption("조금씩 규칙적으로 자고 일어나는 습관을 만들어 봐요.")

home, record, routine, analysis = st.tabs([
    "🏠 오늘 계획",
    "📝 수면 기록",
    "🌜 취침 루틴",
    "📊 기록 분석"
])

# ================= 오늘 계획 =================
with home:
    st.header("오늘의 수면 계획")

    wake_time = st.time_input(
        "목표 기상 시간",
        value=time(7, 0),
        key="target_wake"
    )

    target_hours = st.select_slider(
        "목표 수면 시간",
        options=[8, 8.5, 9, 9.5, 10],
        value=8.5,
        format_func=lambda x: f"{x}시간"
    )

    wake_dt = datetime.combine(date.today(), wake_time)
    bed_dt = wake_dt - timedelta(hours=target_hours)

    st.markdown("### ✨ 나의 목표")
    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "추천 취침 시간",
            bed_dt.strftime("%p %I:%M")
            .replace("AM", "오전")
            .replace("PM", "오후")
        )

    with c2:
        st.metric("목표 수면 시간", f"{target_hours}시간")

    st.info(
        "잠들기 30분 전부터 준비해 봐요. "
        "청소년은 일반적으로 하루 8~10시간의 수면이 권장돼요."
    )

    st.subheader("오늘 수업 시간에 얼마나 졸렸나요?")

    sleepy = st.radio(
        "졸림 정도",
        [
            "거의 안 졸림",
            "조금 졸림",
            "많이 졸림",
            "집중하기 어려울 정도로 졸림"
        ],
        index=0
    )

    advice = {
        "거의 안 졸림":
            "좋아요! 지금의 수면 습관을 꾸준히 유지해 봐요.",
        "조금 졸림":
            "쉬는 시간에 가볍게 움직이고 낮에 햇빛을 쬐어 보세요.",
        "많이 졸림":
            "오늘은 취침 준비를 15분 일찍 시작해 보세요.",
        "집중하기 어려울 정도로 졸림":
            "충분히 잘 수 있도록 일정을 조정해 보세요. "
            "이런 졸림이 계속되면 보호자나 보건교사에게 이야기해 보세요."
    }

    st.success(advice[sleepy])

    st.subheader("수면 리듬을 위한 세 가지")
    st.write("🌅 주말에도 기상 시간을 크게 바꾸지 않기")
    st.write("📱 잠들기 전 30분은 화면 사용 줄이기")
    st.write("☕ 오후 늦게 카페인 음료 피하기")

# ================= 수면 기록 =================
with record:
    st.header("어젯밤 수면 기록")

    with st.form("sleep_form"):
        day = st.date_input("기상한 날짜", value=date.today())

        c1, c2 = st.columns(2)

        with c1:
            sleep_at = st.time_input(
                "잠든 시간",
                value=time(23, 0),
                key="sleep_at"
            )

        with c2:
            wake_at = st.time_input(
                "기상 시간",
                value=time(7, 0),
                key="wake_at"
            )

        quality = st.slider(
            "일어난 뒤 개운함",
            min_value=1,
            max_value=5,
            value=3
        )

        note = st.text_input(
            "메모 (선택)",
            placeholder="예: 시험 공부 때문에 늦게 잠"
        )

        save = st.form_submit_button(
            "기록 저장",
            type="primary",
            use_container_width=True
        )

    if save:
        start = datetime.combine(day, sleep_at)
        end = datetime.combine(day, wake_at)

        # 기상 시간이 취침 시간보다 이르면 다음 날 기상으로 계산
        if end <= start:
            end += timedelta(days=1)

        hours = (end - start).total_seconds() / 3600

        if hours <= 0 or hours > 18:
            st.error("시간을 다시 확인해 주세요.")
        else:
            new_log = {
                "날짜": str(day),
                "취침": sleep_at.strftime("%H:%M"),
                "기상": wake_at.strftime("%H:%M"),
                "수면 시간": round(hours, 2),
                "개운함": quality,
                "메모": note
            }

            # 같은 날짜 기록은 새 기록으로 교체
            st.session_state.logs = [
                x for x in st.session_state.logs
                if x["날짜"] != str(day)
            ]
            st.session_state.logs.append(new_log)
            st.session_state.logs.sort(key=lambda x: x["날짜"])

            st.success(f"저장 완료! 수면 시간은 {hours:.1f}시간이에요.")

            if hours < 8:
                st.warning(
                    "수면 시간이 청소년 권장 범위보다 짧아요. "
                    "오늘은 충분히 잘 수 있도록 계획해 보세요."
                )
            elif hours <= 10:
                st.success("일반적인 청소년 권장 수면 범위에 들어요.")

# ================= 취침 루틴 =================
with routine:
    st.header("🌜 잠들기 전 30분")

    st.write("오늘 실천할 수 있는 항목을 체크해 봐요.")

    tasks = [
        "휴대폰을 내려놓거나 화면 밝기 줄이기",
        "내일 입을 교복과 가방 준비하기",
        "양치와 세안 마치기",
        "조명을 낮추고 조용하게 쉬기",
        "알람을 맞추고 취침 준비 끝내기"
    ]

    today = str(date.today())

    if today not in st.session_state.routine:
        st.session_state.routine[today] = []

    done = st.session_state.routine[today]

    for i, task in enumerate(tasks):
        checked = st.checkbox(
            task,
            value=task in done,
            key=f"task_{today}_{i}"
        )

        if checked and task not in done:
            done.append(task)
        elif not checked and task in done:
            done.remove(task)

    progress = len(done) / len(tasks)

    st.progress(progress, text=f"{len(done)} / {len(tasks)} 완료")

    if len(done) == len(tasks):
        st.balloons()
        st.success("오늘의 취침 루틴을 모두 완료했어요! 🌙")

# ================= 기록 분석 =================
with analysis:
    st.header("📊 나의 수면 분석")

    logs = st.session_state.logs

    if not logs:
        st.info("아직 기록이 없어요. 수면 기록 탭에서 기록을 추가해 주세요.")
    else:
        df = pd.DataFrame(logs).sort_values("날짜")
        recent = df.tail(7)

        avg_sleep = recent["수면 시간"].mean()
        avg_quality = recent["개운함"].mean()

        c1, c2 = st.columns(2)

        c1.metric("평균 수면 시간", f"{avg_sleep:.1f}시간")
        c2.metric("평균 개운함", f"{avg_quality:.1f} / 5")

        st.subheader("최근 수면 시간")
        chart_df = recent.set_index("날짜")[["수면 시간"]]
        st.bar_chart(chart_df)

        st.subheader("기록 목록")
        st.dataframe(
            df.sort_values("날짜", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "📥 수면 기록 다운로드",
            data=csv_data,
            file_name="sleep_records.csv",
            mime="text/csv",
            use_container_width=True
        )

        if st.button("모든 기록 삭제"):
            st.session_state.logs = []
            st.rerun()

st.divider()
st.caption(
    "이 앱은 수면 습관을 관리하기 위한 도구이며 의료 진단을 제공하지 않습니다. "
    "충분히 자도 졸림이 계속되면 보호자나 의료 전문가와 상담해 보세요. "
    "기록은 앱 세션에 저장되며 영구 보관되지 않을 수 있습니다."
)

