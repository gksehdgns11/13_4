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
    st.session_state.sleep_records = [
        {"date": "2026-10-16", "bedtime": "2026-10-15 23:00", "waketime": "2026-10-16 07:00", "duration": 8.0, "quality": "좋음"},
        {"date": "2026-10-17", "bedtime": "2026-10-16 23:30", "waketime": "2026-10-17 07:00", "duration": 7.5, "quality": "보통"},
        {"date": "2026-10-18", "bedtime": "2026-10-17 22:30", "waketime": "2026-10-18 06:30", "duration": 8.0, "quality": "매우 좋음"},
    ]

if "target_bedtime" not in st.session_state:
    st.session_state.target_bedtime = time(23, 0)

if "target_waketime" not in st.session_state:
    st.session_state.target_waketime = time(7, 0)

if "reminder_time" not in st.session_state:
    st.session_state.reminder_time = time(22, 30)

# --- 유틸리티 함수 ---
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
    """최근 7회 수면 규칙성 점수 계산 (100점 만점)"""
    if not records:
        return 0
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

# 대시보드 핵심 지표
streak_count = calculate_streak(st.session_state.sleep_records)
regularity_score = calculate_regularity_score(st.session_state.sleep_records)

if st.session_state.sleep
