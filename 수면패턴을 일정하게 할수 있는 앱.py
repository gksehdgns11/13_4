
import streamlit as st
import pandas as pd
from datetime import date, datetime, time, timedelta
from pathlib import Path

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="SleepMate | 수면 습관 관리",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path("sleep_records.csv")
COLUMNS = ["날짜", "취침", "기상", "수면시간"]

st.markdown("""
<style>
    .stApp {
        background-color: #F6F8FC;
    }
    [data-testid="stSidebar"] {
        background-color: #EDF2FA;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #263859;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #687792;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E3E9F3;
        padding: 16px;
        border-radius: 14px;
    }
    .tip {
        padding: 15px;
        border-radius: 12px;
        background: #EAF1FF;
        color: #263859;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 데이터 처리
# -----------------------------
def load_records():
    """CSV 기록을 불러오고 문제가 있으면 빈 데이터로 시작한다."""
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)

    try:
        df = pd.read_csv(DATA_FILE, dtype=str)

        if not set(COLUMNS).issubset(df.columns):
            st.warning("기록 파일의 형식이 올바르지 않아 새 기록으로 시작합니다.")
            return pd.DataFrame(columns=COLUMNS)

        df = df[COLUMNS].copy()
        df["날짜"] = pd.to_datetime(
            df["날짜"], errors="coerce"
        ).dt.date

        df["수면시간"] = pd.to_numeric(
            df["수면시간"], errors="coerce"
        )

        df = df.dropna(subset=["날짜", "수면시간"])
        df = df[df["수면시간"].between(0, 24)]
        return df.sort_values("날짜").reset_index(drop=True)

    except (OSError, ValueError, pd.errors.ParserError):
        st.warning("기록 파일을 읽지 못했습니다. 새 기록으로 시작합니다.")
        return pd.DataFrame(columns=COLUMNS)


def save_records(df):
    """기록을 CSV 파일로 저장한다."""
    try:
        df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
        return True
    except OSError:
        st.error("파일 저장에 실패했습니다. 저장 공간을 확인해 주세요.")
        return False


def calculate_sleep(bedtime, wake_time):
    """취침 시간부터 다음 기상 시간까지의 수면 시간을 계산한다."""
    start = datetime.combine(date.today(), bedtime)
    end = datetime.combine(date.today(), wake_time)

    if end <= start:
        end += timedelta(days=1)

    return round((end - start).total_seconds() / 3600, 2)


def format_hours(hours):
    """시간을 '7시간 30분' 형식으로 표시한다."""
    minutes = round(float(hours) * 60)
    return f"{minutes // 60}시간 {minutes % 60}분"


def upsert_record(df, selected_date, bedtime, wake_time):
    """같은 날짜의 기록이 있으면 수정하고, 없으면 추가한다."""
    hours = calculate_sleep(bedtime, wake_time)

    new_row = {
        "날짜": selected_date,
        "취침": bedtime.strftime("%H:%M"),
        "기상": wake_time.strftime("%H:%M"),
        "수면시간": hours,
    }

    df = df[df["날짜"] != selected_date].copy()
    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True,
    )
    return df.sort_values("날짜").reset_index(drop=True)


# -----------------------------
# 앱 시작
# -----------------------------
if "records" not in st.session_state:
    st.session_state.records = load_records()

if "checklist_date" not in st.session_state:
    st.session_state.checklist_date = date.today()

if st.session_state.checklist_date != date.today():
    st.session_state.checklist_date = date.today()
    st.session_state.checklist = [False, False, False, False]

if "checklist" not in st.session_state:
    st.session_state.checklist = [False, False, False, False]

if "bedtime_goal" not in st.session_state:
    st.session_state.bedtime_goal = time(23, 0)

if "wake_goal" not in st.session_state:
    st.session_state.wake_goal = time(7, 0)

df = st.session_state.records.copy()

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.markdown("## 🌙 SleepMate")
    st.caption("나만의 수면 습관 관리")

    page = st.radio(
        "메뉴",
        [
            "🏠 홈",
            "📝 수면 기록",
            "📊 패턴 분석",
            "🎯 목표와 체크리스트",
        ],
    )

    st.divider()
    st.caption("작은 습관부터 차근차근!")
    st.caption("기록은 현재 앱의 CSV 파일에 저장됩니다.")

# -----------------------------
# 홈
# -----------------------------
if page == "🏠 홈":
    st.markdown(
        '<div class="main-title">안녕! 오늘도 잘 자보자 🌙</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-title">'
        '규칙적인 수면으로 학교생활의 집중력을 관리해 봐요.'
        '</div>',
        unsafe_allow_html=True,
    )

    today = date.today()
    recent = df[df["날짜"] >= today - timedelta(days=6)]
    today_record = df[df["날짜"] == today]

    avg = recent["수면시간"].mean() if not recent.empty else 0
    latest = (
        float(today_record.iloc[-1]["수면시간"])
        if not today_record.empty else None
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "오늘 수면",
            format_hours(latest) if latest is not None else "기록 없음",
        )
    with c2:
        st.metric(
            "최근 7일 평균",
            format_hours(avg) if not recent.empty else "기록 없음",
        )
    with c3:
        st.metric(
            "오늘 체크리스트",
            f"{sum(st.session_state.checklist)}/4 완료",
        )

    st.subheader("🌟 오늘의 수면 목표")
    col1, col2 = st.columns(2)

    with col1:
        st.info(f"취침 목표: **{st.session_state.bedtime_goal.strftime('%H:%M')}**")
    with col2:
        st.info(f"기상 목표: **{st.session_state.wake_goal.strftime('%H:%M')}**")

    if latest is not None:
        if latest < 7:
            st.warning(
                "최근 기록한 수면이 짧아요. "
                "취침 시간을 조금 앞당길 수 있는지 살펴보세요."
            )
        elif latest < 8:
            st.info(
                "수면 시간을 조금 더 확보할 수 있을지 살펴보세요. "
                "청소년은 일반적으로 하루 8~10시간의 수면이 권장됩니다."
            )
        else:
            st.success(
                "좋아요! 오늘 수면 기록을 확인했어요. "
                "규칙적인 취침·기상 시간도 함께 유지해 봐요."
            )
    else:
        st.markdown(
            '<div class="tip">첫 번째 수면 기록을 추가하면 '
            '나의 수면 패턴을 확인할 수 있어요.</div>',
            unsafe_allow_html=True,
        )

    st.subheader("📌 오늘 실천하기")
    tasks = [
        "잠들기 30분 전 스마트폰 내려놓기",
        "가능하면 비슷한 시간에 잠자리에 들기",
        "기상 후 햇빛을 쬐며 몸 깨우기",
        "오후 늦은 시간의 카페인 음료 피하기",
    ]

    for i, task in enumerate(tasks):
        checked = st.checkbox(
            task,
            value=st.session_state.checklist[i],
            key=f"home_task_{i}",
        )
        st.session_state.checklist[i] = checked

    st.progress(sum(st.session_state.checklist) / len(tasks))
    st.caption(
        f"오늘 {sum(st.session_state.checklist)}개 / {len(tasks)}개 실천 완료"
    )

# -----------------------------
# 수면 기록
# -----------------------------
elif page == "📝 수면 기록":
    st.title("📝 수면 기록")
    st.write("잠든 시간과 일어난 시간을 입력해 주세요.")

    selected_date = st.date_input(
        "기록 날짜 (취침한 날짜)",
        value=date.today(),
        max_value=date.today(),
    )

    existing = df[df["날짜"] == selected_date]

    default_bed = time(23, 0)
    default_wake = time(7, 0)

    if not existing.empty:
        try:
            default_bed = time.fromisoformat(str(existing.iloc[-1]["취침"]))
            default_wake = time.fromisoformat(str(existing.iloc[-1]["기상"]))
        except ValueError:
            pass

    with st.form("sleep_form"):
        col1, col2 = st.columns(2)

        with col1:
            bedtime = st.time_input("취침 시간", value=default_bed)

        with col2:
            wake_time = st.time_input("기상 시간", value=default_wake)

        preview = calculate_sleep(bedtime, wake_time)
        st.info(f"예상 수면 시간: **{format_hours(preview)}**")

        submitted = st.form_submit_button(
            "💾 수면 기록 저장",
            use_container_width=True,
        )

        if submitted:
            if preview <= 0 or preview > 24:
                st.error("수면 시간을 확인해 주세요.")
            else:
                updated = upsert_record(
                    df, selected_date, bedtime, wake_time
                )
                if save_records(updated):
                    st.session_state.records = updated
                    st.success("수면 기록을 저장했습니다!")
                    st.rerun()

    st.divider()
    st.subheader("기록 삭제")

    if not df.empty:
        delete_date = st.selectbox(
            "삭제할 날짜",
            options=sorted(df["날짜"].tolist(), reverse=True),
            format_func=lambda d: d.strftime("%Y-%m-%d"),
        )

        if st.button("선택한 기록 삭제", type="secondary"):
            updated = df[df["날짜"] != delete_date].copy()
            if save_records(updated):
                st.session_state.records = updated
                st.success("선택한 기록을 삭제했습니다.")
                st.rerun()
    else:
        st.caption("아직 삭제할 기록이 없습니다.")

# -----------------------------
# 수면 패턴 분석
# -----------------------------
elif page == "📊 패턴 분석":
    st.title("📊 나의 수면 패턴")
    st.write("기록이 쌓일수록 생활 패턴을 이해하기 쉬워져요.")

    if df.empty:
        st.info("분석할 기록이 없어요. 먼저 수면 기록을 입력해 주세요.")
    else:
        today = date.today()
        last7 = df[
            (df["날짜"] >= today - timedelta(days=6))
            & (df["날짜"] <= today)
        ].copy()

        if last7.empty:
            st.info("최근 7일 기록이 없습니다. 수면 기록을 추가해 주세요.")
        else:
            average = last7["수면시간"].mean()
            target_rate = (
                last7["수면시간"].between(8, 10).mean() * 100
            )

            c1, c2, c3 = st.columns(3)
            c1.metric("기록 일수", f"{len(last7)}일")
            c2.metric("평균 수면", format_hours(average))
            c3.metric("8~10시간 수면 비율", f"{target_rate:.0f}%")

            chart_df = last7.copy()
            chart_df["날짜"] = pd.to_datetime(chart_df["날짜"])
            chart_df = chart_df.set_index("날짜")
            chart_df = chart_df[["수면시간"]]

            st.subheader("최근 7일 수면 시간")
            st.line_chart(chart_df, y="수면시간")
            st.caption(
                "그래프는 기록한 수면 시간 기준이며, "
                "수면의 질이나 수업 집중도를 직접 측정하지는 않습니다."
            )

            st.subheader("기록 상세")
            display_df = last7.copy()
            display_df["날짜"] = display_df["날짜"].astype(str)
            display_df["수면시간"] = display_df["수면시간"].apply(
                format_hours
            )
            st.dataframe(
                display_df.sort_values("날짜", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

            st.subheader("💡 나의 패턴 살펴보기")
            if average < 8:
                st.warning(
                    "최근 평균 수면이 청소년 권장 시간보다 짧아요. "
                    "일정한 취침 시간을 정하고 수면 기회를 늘려 보세요."
                )
            elif average <= 10:
                st.success(
                    "최근 평균 수면 시간이 청소년 권장 범위에 있어요. "
                    "수면 시간뿐 아니라 규칙성도 확인해 보세요."
                )
            else:
                st.info(
                    "평균 수면 시간이 긴 편이에요. "
                    "실제 수면 시간과 기록 입력이 정확한지 확인해 보세요."
                )

            if len(last7) >= 2:
                variation = last7["수면시간"].max() - last7["수면시간"].min()
                if variation >= 3:
                    st.info(
                        "날짜별 수면 시간 차이가 3시간 이상이에요. "
                        "취침·기상 시간을 조금 더 일정하게 유지해 보세요."
                    )

        st.divider()
        st.subheader("전체 기록 다운로드")
        csv_bytes = df.copy()
        csv_bytes["날짜"] = csv_bytes["날짜"].astype(str)
        st.download_button(
            "⬇️ 수면 기록 CSV 다운로드",
            data=csv_bytes.to_csv(
                index=False, encoding="utf-8-sig"
            ).encode("utf-8-sig"),
            file_name="sleep_records.csv",
            mime="text/csv",
            use_container_width=True,
        )

# -----------------------------
# 목표와 체크리스트
# -----------------------------
elif page == "🎯 목표와 체크리스트":
    st.title("🎯 나만의 수면 목표")
    st.write("무리한 목표보다 지킬 수 있는 목표를 정해 보세요.")

    with st.form("goal_form"):
        col1, col2 = st.columns(2)

        with col1:
            bedtime_goal = st.time_input(
                "목표 취침 시간",
                value=st.session_state.bedtime_goal,
            )

        with col2:
            wake_goal = st.time_input(
                "목표 기상 시간",
                value=st.session_state.wake_goal,
            )

        goal_hours = calculate_sleep(bedtime_goal, wake_goal)
        st.info(f"설정한 수면 시간: **{format_hours(goal_hours)}**")

        save_goal = st.form_submit_button(
            "목표 저장",
            use_container_width=True,
        )

        if save_goal:
            if goal_hours < 8:
                st.warning(
                    "청소년은 보통 8~10시간 수면이 권장돼요. "
                    "가능하다면 수면 시간을 더 확보하는 목표를 고려해 보세요."
                )
            st.session_state.bedtime_goal = bedtime_goal
            st.session_state.wake_goal = wake_goal
            st.success("수면 목표를 저장했습니다.")

    st.divider()
    st.subheader("☑️ 오늘의 실천 체크리스트")

    tasks = [
        "잠들기 30분 전 스마트폰 내려놓기",
        "비슷한 시간에 잠자리에 들기",
        "아침에 햇빛을 쬐며 몸 깨우기",
        "오후 늦은 시간의 카페인 음료 피하기",
    ]

    for i, task in enumerate(tasks):
        st.session_state.checklist[i] = st.checkbox(
            task,
            value=st.session_state.checklist[i],
            key=f"goal_task_{i}",
        )

    done = sum(st.session_state.checklist)
    st.progress(done / len(tasks))
    st.write(f"**오늘의 실천: {done}/{len(tasks)}개**")

    if done == len(tasks):
        st.success("오늘의 체크리스트를 모두 완료했어요! 🎉")

    st.caption(
        "체크리스트는 현재 실행 세션에 저장됩니다. "
        "앱이 재시작되면 체크 상태가 초기화될 수 있어요."
    )

# -----------------------------
# 공통 안내
# -----------------------------
st.divider()
st.caption(
    "SleepMate는 생활 습관 관리용 도구이며 의료 진단 도구가 아닙니다. "
    "충분히 자도 수업 시간 졸림이 계속되거나 일상생활에 큰 지장이 있다면 "
    "보호자와 상의하고 의료 전문가의 도움을 받아 보세요."
)
