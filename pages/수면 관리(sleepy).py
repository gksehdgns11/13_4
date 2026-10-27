import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta, time

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="Sleepy - 규칙적인 수면 관리",
    page_icon="🌙",
    layout="wide"
)

# --- 세션 상태 초기화 ---
if "sleep_records" not in st.session_state:
    st.session_state.sleep_records = []

if "target_bedtime" not in st.session_state:
    st.session_state.target_bedtime = time(23, 0)

if "target_waketime" not in st.session_state:
    st.session_state.target_waketime = time(7, 0)

if "reminder_time" not in st.session_state:
    st.session_state.reminder_time = time(22, 30)

# --- 유틸리티 함수 ---
def get_age_recommended_sleep(age):
    """나이에 따른 권장 수면 시간 가이드라인 (National Sleep Foundation 기준)"""
    if age <= 1:
        return "영아 (1~2세)", "11~14시간", 12.0
    elif age <= 5:
        return "유아 (3~5세)", "10~13시간", 11.0
    elif age <= 13:
        return "학령기 아동 (6~13세)", "9~11시간", 10.0
    elif age <= 17:
        return "청소년 (14~17세)", "8~10시간", 9.0
    elif age <= 64:
        return "성인 (18~64세)", "7~9시간", 8.0
    else:
        return "노년층 (65세 이상)", "7~8시간", 7.5

def calculate_streak(records):
    """연속 기록 일수 계산"""
    if not records:
        return 0
    
    dates = sorted(list(set([r["date"] for r in records])))
    dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
    
    streak = 1
    today = datetime.now().date()
    
    if dates[-1] < today - timedelta(days=1):
        return 0
        
    for i in range(len(dates) - 1, 0, -1):
        if (dates[i] - dates[i-1]).days == 1:
            streak += 1
        else:
            break
    return streak

def calculate_regularity_score(records):
    """최근 7회 수면 규칙성 점수 계산 (기록이 없을 경우 None 반환)"""
    if not records:
        return None
    recent_records = records[-7:]
    durations = [r["duration"] for r in recent_records]
    avg_duration = sum(durations) / len(durations)
    
    variance = sum((x - avg_duration) ** 2 for x in durations) / len(durations)
    std_dev = variance ** 0.5
    
    score = max(0, min(100, int(100 - (std_dev * 15))))
    return score

# --- 사이드바: 목표 설정, 알림 및 백업 ---
with st.sidebar:
    st.header("🌙 수면 목표 설정")
    set_bedtime = st.time_input("목표 취침 시간", value=st.session_state.target_bedtime)
    set_waketime = st.time_input("목표 기상 시간", value=st.session_state.target_waketime)
    st.session_state.target_bedtime = set_bedtime
    st.session_state.target_waketime = set_waketime
    
    dummy_date = datetime.today().date()
    dt_bed = datetime.combine(dummy_date, set_bedtime)
    dt_wake = datetime.combine(dummy_date, set_waketime)
    if dt_wake <= dt_bed:
        dt_wake += timedelta(days=1)
    target_duration = (dt_wake - dt_bed).total_seconds() / 3600
    
    st.info(f"🎯 **목표 수면 시간:** {target_duration:.1f}시간")
    st.divider()
    
    st.header("⏰ 취침 알림 시간 설정")
    rem_time = st.time_input("알림 희망 시간", value=st.session_state.reminder_time)
    if st.button("알림 시간 저장", use_container_width=True):
        st.session_state.reminder_time = rem_time
        st.success(f"{rem_time.strftime('%H:%M')} 알림이 설정되었습니다.")
        st.caption("※ 현재 버전은 실제 알림을 전송하지 않습니다.")
        
    st.divider()
    st.header("💾 데이터 관리 및 백업")
    
    json_data = json.dumps(st.session_state.sleep_records, ensure_ascii=False, indent=2)
    st.download_button(
        label="📥 수면 기록 백업 (JSON 다운로드)",
        data=json_data,
        file_name="sleepy_records.json",
        mime="application/json",
        use_container_width=True
    )
    
    if st.button("🗑️ 전체 수면 기록 삭제", use_container_width=True):
        st.session_state.sleep_records = []
        st.rerun()

# --- 메인 헤더 ---
st.title("🌙 Sleepy - 건강한 수면 습관 관리")
st.markdown("개인의 생활 패턴에 맞춰 최적의 수면 시간을 찾고 수면 습관을 기록해 보세요.")

# 데이터 유무에 따른 수치 예외 처리
streak_count = calculate_streak(st.session_state.sleep_records)
regularity_score = calculate_regularity_score(st.session_state.sleep_records)

if st.session_state.sleep_records:
    recent_7 = st.session_state.sleep_records[-7:]
    avg_sleep = sum([r["duration"] for r in recent_7]) / len(recent_7)
    avg_sleep_str = f"{avg_sleep:.1f}시간"
    regularity_score_str = f"{regularity_score}점"
else:
    avg_sleep = 0.0
    avg_sleep_str = "- (기록 없음)"
    regularity_score_str = "- (기록 없음)"

# 대시보드 핵심 지표 출력
c1, c2, c3, c4 = st.columns(4)
c1.metric("🔥 연속 기록", f"{streak_count}일째")
c2.metric("📊 최근 7회 평균 수면", avg_sleep_str)
c3.metric("✨ 수면 규칙성 점수", regularity_score_str)
c4.metric("🎯 목표 수면 시간", f"{target_duration:.1f}시간")

st.divider()

# 메인 탭
tab1, tab2, tab3 = st.tabs(["✍️ 수면 기록 & 계산기", "📈 수면 패턴 분석", "📜 수면 일지"])

# 탭 1: 수면 기록 및 추천 취침 시간 계산기
with tab1:
    st.subheader("💡 나이별 추천 수면 시간 & 취침 계산기")
    with st.expander("개인 맞춤 추천 취침 시간 확인하기", expanded=True):
        col_calc1, col_calc2, col_calc3 = st.columns(3)
        with col_calc1:
            age = st.number_input("나이 (세)", min_value=1, max_value=100, value=25)
        with col_calc2:
            desired_wake = st.time_input("희망 기상 시간", value=time(7, 0))
        with col_calc3:
            pattern = st.selectbox("수면 타입 선택", ["기본 권장 수면시간 적용", "짧은 수면 선호", "충분한 수면 선호"])
        
        group_name, rec_range_str, base_rec_hours = get_age_recommended_sleep(age)
        
        if pattern == "짧은 수면 선호":
            selected_hours = base_rec_hours - 0.5
        elif pattern == "충분한 수면 선호":
            selected_hours = base_rec_hours + 0.5
        else:
            selected_hours = base_rec_hours
            
        dummy_today = datetime.today().date()
        wake_dt = datetime.combine(dummy_today, desired_wake)
        rec_bed_dt = wake_dt - timedelta(hours=selected_hours)
        
        # 📌 세로선(|) 제거 및 구분을 더 명확하게 수정된 파란색 박스
        st.info(f"👶/👨 **연령별 분류:** {group_name}  ,  **의학적 권장 수면시간:** {rec_range_str}")
        
        st.markdown(f"""
        > 💡 **맞춤 추천 취침 시간:** **오후 {rec_bed_dt.strftime('%I:%M')}**  
        > (적용 수면 시간: **{selected_hours:.1f}시간** | 희망 기상 시간: **{desired_wake.strftime('%H:%M')}**)
        """)

    st.divider()
    st.subheader("✍️ 수면 기록 작성")
    
    col_d, col_q = st.columns(2)
    with col_d:
        record_date = st.date_input("기록 날짜", value=datetime.now().date())
    with col_q:
        quality = st.selectbox("수면 만족도", ["매우 좋음", "좋음", "보통", "나쁨", "매우 나쁨"])
        
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        bed_d = st.date_input("잠든 날짜", value=record_date - timedelta(days=1))
        bed_t = st.time_input("잠든 시간", value=time(23, 0))
    with col_in2:
        wake_d = st.date_input("일어난 날짜", value=record_date)
        wake_t = st.time_input("일어난 시간", value=time(7, 0))
        
    bed_datetime = datetime.combine(bed_d, bed_t)
    wake_datetime = datetime.combine(wake_d, wake_t)
    
    if wake_datetime <= bed_datetime:
        st.error("⚠️ 기상 시간은 잠든 시간보다 나중이어야 합니다.")
    else:
        calc_duration = (wake_datetime - bed_datetime).total_seconds() / 3600
        st.info(f"⏱️ 계산된 총 수면 시간: **{calc_duration:.1f} 시간**")
        
        if st.button("수면 기록 저장", type="primary", use_container_width=True):
            new_record = {
                "date": str(record_date),
                "bedtime": bed_datetime.strftime("%Y-%m-%d %H:%M"),
                "waketime": wake_datetime.strftime("%Y-%m-%d %H:%M"),
                "duration": round(calc_duration, 1),
                "quality": quality
            }
            st.session_state.sleep_records.append(new_record)
            st.success("수면 기록이 저장되었습니다.")
            st.rerun()

# 탭 2: 수면 패턴 분석
with tab2:
    st.subheader("📊 최근 수면 시간 변화")
    if not st.session_state.sleep_records:
        st.info("저장된 수면 기록이 없습니다. 먼저 첫 수면 기록을 등록해 보세요!")
    else:
        df = pd.DataFrame(st.session_state.sleep_records)
        df_chart = df.tail(14).copy()
        
        df_chart["실제 수면 시간"] = df_chart["duration"]
        df_chart["목표 수면 시간"] = target_duration
        chart_data = df_chart.set_index("date")[["실제 수면 시간", "목표 수면 시간"]]
        
        st.bar_chart(chart_data, use_container_width=True)
        
        st.subheader("💬 수면 피드백")
        if avg_sleep >= target_duration - 0.5 and avg_sleep <= target_duration + 0.5:
            st.success("🎉 목표 수면 시간을 잘 유지하고 있습니다. 계속해서 일정한 패턴을 유지해 보세요!")
        elif avg_sleep < target_duration - 0.5:
            st.warning("⚠️ 목표 수면 시간보다 모자랍니다. 취침 시간을 조금 앞당겨 건강을 챙겨보세요.")
        else:
            st.info("ℹ️ 목표 수면 시간보다 더 많이 취침 중입니다. 규칙적인 일과 형성을 권장합니다.")

# 탭 3: 수면 일지 및 삭제
with tab3:
    st.subheader("📜 저장된 수면 기록 목록")
    if not st.session_state.sleep_records:
        st.info("등록된 수면 기록이 없습니다.")
    else:
        df_display = pd.DataFrame(st.session_state.sleep_records)
        df_display.columns = ["날짜", "취침 일시", "기상 일시", "수면 시간(h)", "만족도"]
        st.dataframe(df_display, use_container_width=True)
        
        st.caption("특정 날짜의 수면 기록을 선택하여 삭제할 수 있습니다.")
        del_date = st.selectbox("삭제할 기록 선택", [r["date"] for r in st.session_state.sleep_records])
        if st.button("선택한 기록 삭제"):
            st.session_state.sleep_records = [r for r in st.session_state.sleep_records if r["date"] != del_date]
            st.success(f"{del_date} 날짜 기록이 삭제되었습니다.")
            st.rerun()
