import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 앱 제목 및 설명
st.title("🧪 산화 스트레스 처리시점에 따른 항산화 효력 변화 예측기")
st.write("자주탐 실험 데이터(효모 콜로니 수 & DNA Band B값)를 기반으로 조건처리 시점별 세포 생존율을 예측합니다.")

st.sidebar.header("⚙️ 실험 조건 설정")

# ⭐ 핵심: 사용자가 조정한 시간(슬라이더 값)을 컴퓨터에 기억시키는 메모리(Session State) 설정
if 'saved_time' not in st.session_state:
    st.session_state.saved_time = 15

# 2. 사용자 입력 (조건 선택)
condition = st.sidebar.selectbox(
    "처리 조건 선택",
    ["치료군 (15분 손상 후 비타민C 사후처리)", "예방군 (15분 비타민C 선처리)", "동시처리군", "염산치료군 (더 강한 손상)", "산화처리군 (산화만)", "대조군 (무처리)"]
)

# 3. 조건별 슬라이더 제목 자동 변경
if "예방군" in condition:
    slider_label = "비타민 C 선처리 후 산화제 투여까지 시간 (분)"
elif "치료군" in condition or "염산" in condition:
    slider_label = "산화제(또는 염산) 노출 후 비타민 C 투여까지 시간 (분)"
else:
    slider_label = "반응 유지 시간 (분)"

# 4. 메모리(saved_time)와 연결된 슬라이더 생성 (카테고리를 바꿔도 숫자가 리셋되지 않음)
exposure_time = st.sidebar.slider(
    slider_label, 
    min_value=0, 
    max_value=60, 
    value=st.session_state.saved_time,
    key="time_slider"
)

# 슬라이더가 움직일 때마다 현재 수치를 메모리에 실시간 업데이트
st.session_state.saved_time = exposure_time

# 5. 실측 데이터 기준(대조군 250개 = 100%) 및 반응 모델 연산
if condition == "대조군 (무처리)":
    colony_count = 250
    b_value = 159.0
    status = "🟢 정상 (손상 없음)"

elif "예방군" in condition:
    if exposure_time <= 15:
        survival_pct = 75.0 + (exposure_time * 0.6)
    else:
        survival_pct = max(50.0, 84.0 - ((exposure_time - 15) * 0.4))
    
    colony_count = int(250 * (survival_pct / 100.0))
    b_value = 161.0
    status = "🔵 최상 (사전 예방으로 세포 및 DNA 완벽 보호)"

elif "동시처리군" in condition:
    survival_pct = max(30.0, 58.0 - ((exposure_time - 15) * 0.3))
    colony_count = int(250 * (survival_pct / 100.0))
    b_value = 162.0
    status = "🟡 양호 (산화와 항산화 반응 동시 진행)"

elif "치료군 (15분" in condition:
    base_pct = 30.0 - ((exposure_time - 15) * 1.0) if exposure_time >= 15 else 30.0 + ((15 - exposure_time) * 1.5)
    survival_pct = max(0.0, base_pct)
    colony_count = int(250 * (survival_pct / 100.0))
    b_value = 155.7
    
    if exposure_time <= 10:
        status = "🟡 골든타임 이내 (빠른 사후 조치로 높은 복구율)"
    elif exposure_time <= 20:
        status = "🟠 경고 (손상 진행으로 세포 복구 한계 발생)"
    else:
        status = "🔴 골든타임 초과 (비가역적 세포 손상 진행)"

elif "염산" in condition:
    colony_count = 0
    b_value = 169.3
    status = "🔴 위험 (강산으로 인한 세포 완숙 파괴)"

else: # 산화처리군
    colony_count = 0
    b_value = 156.7
    status = "🔴 치명적 (항산화제 미투여로 대량 사멸)"

# 백분율 계산
survival_rate_pct = (colony_count / 250.0) * 100.0
dna_relative_pct = (b_value / 159.0) * 100.0

# 6. 결과 출력
st.subheader("📊 실제 데이터 기반 분석 결과")
col1, col2, col3 = st.columns(3)
col1.metric("예상 콜로니 개수", f"{colony_count} 개")
col2.metric("세포 생존율", f"{survival_rate_pct:.1f} %")
col3.metric("상대 DNA B값 비율", f"{dna_relative_pct:.1f} %")

st.info(f"**판정 결과:** {status}")

# 7. 실측치 기반 그래프 시각화
st.subheader("📈 그룹별 콜로니 수 비교 (실측치 연동)")

prev_cnt = colony_count if "예방군" in condition else 210
treat_cnt = colony_count if "치료군" in condition else 75

data = {
    'Group': ['Control', 'Prevent', 'Simultaneous', 'Treat', 'Oxidized', 'Acid-Treat'],
    'Colony Count': [250, prev_cnt, 145, treat_cnt, 0, 0]
}
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(8, 4))
colors = ['gray', 'blue', 'green', 'orange', 'red', 'purple']
ax.bar(df['Group'], df['Colony Count'], color=colors)
ax.set_ylabel("Yeast Colony Count")
ax.set_ylim(0, 280)

for i, v in enumerate(df['Colony Count']):
    ax.text(i, v + 5, str(v), ha='center', fontweight='bold')

st.pyplot(fig)

st.write("---")
st.caption("💡 대조군(250개) 기준 실측치 수치를 100%로 두고 산출된 데이터입니다.")
