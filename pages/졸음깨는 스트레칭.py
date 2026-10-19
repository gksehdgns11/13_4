
import streamlit as st

st.set_page_config(
    page_title="졸릴 땐, 스트레칭!",
    page_icon="🌙",
    layout="centered",
)

# 화면 디자인
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #f5f7ff 0%, #fff7fb 100%);
}
.main .block-container {
    max-width: 800px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}
.hero {
    padding: 1.5rem;
    border-radius: 24px;
    background: linear-gradient(125deg, #dfe8ff, #f3e7ff, #ffeaf4);
    border: 1px solid #e4e5fb;
    text-align: center;
    margin-bottom: 1rem;
}
.hero h1 {
    color: #283d86;
    font-size: 2.1rem;
    margin-bottom: .4rem;
}
.hero p {
    color: #4f587d;
    margin: 0;
}
.step-card {
    background: rgba(255,255,255,.9);
    border: 1px solid #e3e8f7;
    border-radius: 16px;
    padding: 1rem;
    margin: .55rem 0;
}
.step-card strong {
    color: #293e87;
    font-size: 1.04rem;
}
.muted {
    color: #66708d;
    font-size: .9rem;
}
</style>
""", unsafe_allow_html=True)

# 졸림 점수별 스트레칭
ROUTINES = {
    "low": {
        "title": "가벼운 리프레시",
        "description": "아직 많이 졸리지는 않아요. 눈과 어깨를 편안하게 풀어 봐요.",
        "moves": [
            (
                "먼 곳 바라보기",
                "20초",
                "화면에서 눈을 떼고 교실 끝이나 먼 곳을 편안하게 바라봐요."
            ),
            (
                "어깨 천천히 돌리기",
                "앞뒤 각 5회",
                "어깨를 천천히 뒤로, 다시 앞으로 돌려요."
            ),
            (
                "손가락 쫙 펴기",
                "8회",
                "손가락을 넓게 폈다가 힘을 빼고 편안하게 오므려요."
            ),
        ],
    },
    "medium": {
        "title": "몸을 깨우는 스트레칭",
        "description": "집중이 흐려지기 시작했어요. 상체와 다리를 부드럽게 움직여 봐요.",
        "moves": [
            (
                "목 옆 부드럽게 늘리기",
                "좌우 각 8초",
                "고개를 한쪽으로 살짝 기울여요. 손으로 세게 누르지 말고 반대쪽도 해요."
            ),
            (
                "등과 가슴 펴기",
                "10초 × 2회",
                "허리를 편안하게 세우고 어깨를 뒤로 보내 가슴을 열어요."
            ),
            (
                "발뒤꿈치 들기",
                "10회",
                "앉은 상태에서 발뒤꿈치를 천천히 들었다 내려요."
            ),
        ],
    },
    "high": {
        "title": "활기 충전 루틴",
        "description": "졸림이 많이 느껴져요. 무리하지 않는 범위에서 조금 더 크게 움직여요.",
        "moves": [
            (
                "자리에서 기지개 켜기",
                "10초 × 2회",
                "팔을 위로 뻗고 몸을 길게 늘려요. 어깨가 아프면 팔을 낮춰요."
            ),
            (
                "천천히 일어섰다 앉기",
                "5회",
                "주변 공간을 확인하고 천천히 움직여요. 어지러우면 생략해요."
            ),
            (
                "제자리 천천히 걷기",
                "30초",
                "주변의 책상과 가방을 피해 안전한 자리에서 가볍게 걸어요."
            ),
        ],
    },
}


def get_routine(score):
    """졸림 점수에 맞는 스트레칭을 반환합니다."""
    if score <= 3:
        return ROUTINES["low"]
    elif score <= 6:
        return ROUTINES["medium"]
    return ROUTINES["high"]


# 앱 첫 화면
st.markdown("""
<div class="hero">
    <h1>🌙 졸릴 땐, 스트레칭!</h1>
    <p>수업 중 졸음이 몰려올 때, 잠깐 몸을 움직이며 집중을 환기해요.</p>
</div>
""", unsafe_allow_html=True)

st.write(
    "현재 졸림 정도를 1부터 10까지 선택하면 "
    "지금 상태에 맞는 스트레칭을 추천해 줘요."
)

score = st.slider(
    "😴 지금 졸린 정도",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
)

st.caption("1점 = 거의 졸리지 않음 · 10점 = 매우 졸림")

feeling = st.text_input(
    "지금 어떤 상태인가요? (선택)",
    placeholder="예: 점심을 먹고 나니 졸려요",
    max_chars=120,
)

routine = get_routine(score)

st.markdown("---")
st.subheader(f"맞춤 루틴: {routine['title']} · {score}/10")
st.write(routine["description"])

if feeling.strip():
    st.info(f"입력한 상태: {feeling.strip()}")

# 스트레칭 동작과 완료 체크
st.markdown("### 오늘의 스트레칭")
st.write("각 동작을 마친 뒤 체크해 보세요.")

for index, (name, duration, instruction) in enumerate(
    routine["moves"]
):
    st.markdown(
        f"""
        <div class="step-card">
            <strong>{index + 1}. {name}</strong>
            <span class="muted"> · {duration}</span><br>
            {instruction}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.checkbox(
        "완료했어요",
        key=f"stretch_{score}_{index}",
    )

# 진행률 계산
done_count = sum(
    1
    for index in range(len(routine["moves"]))
    if st.session_state.get(f"stretch_{score}_{index}", False)
)

total_count = len(routine["moves"])

st.progress(done_count / total_count)
st.caption(f"완료 {done_count} / {total_count}개")

if done_count == total_count:
    st.success("완료! 잠깐 몸을 돌보는 시간을 가졌어요. 💙")
    st.balloons()
elif done_count > 0:
    st.info("좋아요! 남은 동작도 무리하지 않는 범위에서 이어 가 봐요.")

# 안전 안내
st.markdown("---")
st.markdown("#### 안전하게 이용하기")
st.markdown("""
- 목이나 허리를 세게 꺾거나 반동을 주지 마세요.
- 통증이나 어지러움이 느껴지면 즉시 멈추세요.
- 졸림이 심하면 가능할 때 충분히 쉬고 수면을 챙기세요.
- 수업 중에는 선생님의 안내와 교실 안전을 우선으로 해요.
""")

st.caption(
    "이 앱은 가벼운 움직임을 안내하는 학습용 앱이며, "
    "건강 문제를 진단하지 않습니다."
)
