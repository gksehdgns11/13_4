


import streamlit as st

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="잠깨움 스트레칭",
    page_icon="🌙",
    layout="centered"
)

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef3ff 0%, #f5efff 55%, #fff0f7 100%);
}
.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid #e5e4ff;
    border-radius: 24px;
    padding: 28px 24px;
    text-align: center;
    box-shadow: 0 8px 28px rgba(103, 92, 170, 0.08);
}
.hero h1 {
    color: #5c57a8;
    font-size: 2.25rem;
    margin-bottom: 8px;
}
.hero p {
    color: #686783;
    font-size: 1.02rem;
}
.info-card {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid #e7e3ff;
    border-radius: 18px;
    padding: 18px;
    margin: 12px 0;
}
.stButton > button {
    border-radius: 12px;
    border: 0;
    background: #766ce0;
    color: white;
    font-weight: 600;
}
.stButton > button:hover {
    background: #6258c7;
    color: white;
}
h2, h3 {
    color: #57529b;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 점수별 스트레칭 데이터
# -----------------------------
ROUTINES = {
    1: {
        "title": "가벼운 몸풀기 🌱",
        "message": "아직 많이 졸리지 않아요. 가볍게 몸을 풀어 봐요!",
        "items": [
            ("손가락 쫙 펴기", "10초", "손가락을 펼쳤다가 편안하게 힘을 빼요."),
            ("손목 돌리기", "좌우 5회", "손목으로 작은 원을 그리듯 천천히 돌려요."),
            ("어깨 으쓱하기", "5회", "어깨를 올렸다가 천천히 내려요."),
        ],
    },
    2: {
        "title": "손과 어깨 깨우기 ✋",
        "message": "조금 졸리네요. 손과 어깨를 움직여 봐요!",
        "items": [
            ("목 옆으로 기울이기", "좌우 5초", "고개를 좌우로 부드럽게 기울여요."),
            ("어깨 으쓱하기", "5회", "어깨를 귀 쪽으로 올렸다가 내려요."),
            ("손바닥 밀기", "10초", "양손바닥을 맞대고 가볍게 밀어요."),
        ],
    },
    3: {
        "title": "상체 스트레칭 🌿",
        "message": "졸음이 조금씩 오네요. 상체를 펴 봐요!",
        "items": [
            ("팔 위로 뻗기", "10초", "두 팔을 위로 올려 기지개를 켜요."),
            ("등 둥글게 펴기", "5회", "양팔을 앞으로 뻗으며 등을 부드럽게 펴요."),
            ("손목 스트레칭", "좌우 5초", "반대 손으로 손을 부드럽게 당겨요."),
        ],
    },
    4: {
        "title": "굳은 어깨 풀기 💫",
        "message": "목과 어깨를 천천히 풀어 봐요!",
        "items": [
            ("어깨 뒤로 돌리기", "10회", "어깨를 뒤쪽으로 천천히 돌려요."),
            ("가슴 펴기", "10초", "허리를 편하게 세우고 가슴을 열어요."),
            ("목 옆 근육 늘리기", "좌우 5초", "고개를 좌우로 부드럽게 기울여요."),
        ],
    },
    5: {
        "title": "기지개 스트레칭 ☀️",
        "message": "상체와 발목을 움직여 몸을 환기해 봐요!",
        "items": [
            ("양팔 기지개", "10초", "팔을 위로 뻗으며 기지개를 켜요."),
            ("앉아서 상체 돌리기", "좌우 5회", "허리에 무리가 가지 않게 좌우로 돌려요."),
            ("발목 돌리기", "좌우 5회", "발끝으로 작은 원을 그려요."),
        ],
    },
    6: {
        "title": "하체까지 깨우기 🌼",
        "message": "다리도 가볍게 움직여 봐요!",
        "items": [
            ("무릎 번갈아 들기", "좌우 8회", "앉은 상태에서 무릎을 하나씩 들어요."),
            ("발뒤꿈치 들기", "10회", "발끝을 바닥에 두고 뒤꿈치를 올렸다 내려요."),
            ("등과 어깨 펴기", "10초", "허리를 편하게 세우고 어깨를 펴요."),
        ],
    },
    7: {
        "title": "다리와 전신 풀기 🌈",
        "message": "졸음이 강하네요. 무리하지 않고 움직여 봐요!",
        "items": [
            ("앉아서 다리 펴기", "좌우 5초", "한쪽 다리를 편하게 펴고 잠시 유지해요."),
            ("발끝 당기기", "좌우 5회", "발끝을 몸 쪽으로 당겼다가 편하게 놓아요."),
            ("팔 길게 뻗기", "10초", "팔을 위로 뻗으며 상체를 늘려요."),
        ],
    },
    8: {
        "title": "가볍게 움직이기 🚶",
        "message": "졸음이 많이 와요. 안전한 공간에서 움직여 봐요!",
        "items": [
            ("제자리 천천히 걷기", "20초", "주변을 확인하고 천천히 걸어요."),
            ("종아리 늘리기", "좌우 10초", "안정적인 곳을 짚고 종아리를 부드럽게 늘려요."),
            ("어깨 돌리기", "앞뒤 5회", "어깨를 앞뒤로 천천히 돌려요."),
        ],
    },
    9: {
        "title": "전신 리프레시 🌟",
        "message": "매우 졸리네요. 안전하게 자세를 바꾸고 몸을 풀어요!",
        "items": [
            ("천천히 일어나기", "1회", "안전한 공간에서 천천히 일어났다가 편하게 앉아요."),
            ("제자리 걷기", "20초", "주변에 방해물이 없는 곳에서 천천히 걸어요."),
            ("전신 기지개", "10초", "편안한 자세로 팔을 위로 뻗어요."),
        ],
    },
    10: {
        "title": "천천히 쉬어 가기 🌙",
        "message": "졸음이 아주 심해요. 스트레칭보다 휴식이 더 필요할 수 있어요.",
        "items": [
            ("편안한 자세 잡기", "10초", "의자에 등을 기대고 편안하게 앉아요."),
            ("어깨 힘 빼기", "5회", "어깨를 가볍게 올렸다가 힘을 빼고 내려요."),
            ("천천히 호흡하기", "5회", "편안하게 숨을 들이쉬고 천천히 내쉬어요."),
        ],
    },
}

# -----------------------------
# 제목
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>🌙 잠깨움 스트레칭</h1>
    <p>졸린 순간, 내 상태에 맞는 스트레칭으로 잠깐 몸을 깨워 봐요.</p>
    <p>오늘의 나에게 맞는 작은 리프레시 시간 💜</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------
# 졸림 정도 입력
# -----------------------------
st.subheader("💤 지금 얼마나 졸린가요?")

score = st.slider(
    "졸림 정도를 선택하세요.",
    min_value=1,
    max_value=10,
    value=5,
    step=1,
    help="1점은 거의 졸리지 않는 상태, 10점은 매우 졸린 상태예요."
)

if score <= 3:
    level = "가벼운 졸음"
    emoji = "🙂"
elif score <= 6:
    level = "보통 졸음"
    emoji = "😪"
elif score <= 8:
    level = "심한 졸음"
    emoji = "🥱"
else:
    level = "매우 심한 졸음"
    emoji = "😴"

st.markdown(
    f"""
    <div class="info-card" style="text-align:center;">
        <div style="font-size:2.2rem;">{emoji}</div>
        <h3 style="margin:5px 0;">현재 점수: {score} / 10</h3>
        <p style="margin:0;">졸림 상태: <b>{level}</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

feeling = st.text_input(
    "지금 기분이나 졸린 이유를 적어 보세요. (선택)",
    placeholder="예: 점심을 먹고 나니 졸려요."
)

if feeling.strip():
    st.caption(f"오늘의 한마디: {feeling.strip()}")

# -----------------------------
# 점수에 맞는 루틴 표시
# -----------------------------
routine = ROUTINES[score]

st.divider()
st.subheader(f"✨ 추천 스트레칭: {routine['title']}")
st.write(routine["message"])
st.caption("아래 동작을 편안한 범위에서 천천히 따라 해 보세요.")

# 점수가 바뀌어도 완료 체크가 점수별로 구분되도록 설정
done_count = 0

for index, item in enumerate(routine["items"]):
    name, duration, description = item
    key = f"done_{score}_{index}"

    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    completed = st.checkbox(
        f"{name}  ·  {duration}",
        key=key
    )
    st.write(description)
    st.markdown("</div>", unsafe_allow_html=True)

    if completed:
        done_count += 1

# -----------------------------
# 진행률
# -----------------------------
st.subheader("📈 나의 진행 상황")

progress = done_count / len(routine["items"])
st.progress(progress)
st.write(f"완료한 스트레칭: **{done_count} / {len(routine['items'])}개**")

if done_count == len(routine["items"]):
    st.success("🎉 모든 동작을 완료했어요! 잠깐 몸을 움직인 나를 칭찬해 주세요.")
    st.balloons()
elif done_count > 0:
    st.info("좋아요! 남은 동작도 무리하지 말고 천천히 해 봐요.")
else:
    st.caption("스트레칭을 하나씩 완료할 때마다 체크해 보세요.")

# -----------------------------
# 안전 안내
# -----------------------------
st.divider()
st.subheader("💜 안전하게 이용하기")

st.markdown("""
- 목이나 허리를 세게 돌리지 말고, 통증이 느껴지면 바로 멈춰요.
- 교실에서는 주변 친구와 책상에 부딪히지 않도록 조심해요.
- 졸음이 심할 때는 스트레칭만으로 해결하려 하지 말고, 선생님께 알리고 휴식을 취해요.
- 스트레칭은 잠을 대신할 수 없어요. 충분한 수면이 중요해요.
""")

st.caption("잠깨움 스트레칭 · 오늘도 무리하지 말고 천천히 💜")
