import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 앱 제목 및 설명
st.title("🧪 세포/DNA 산화 스트레스 및 항산화 골든타임 예측기")
st.write("실측 실험 데이터(효모 콜로니 수 & DNA Band B값)를 바탕으로 비타민 C 처리 시점별 세포 생존율을 예측합니다.")

st.sidebar.header("⚙️ 실험 조건 설정")

# 2. 사용자 입력 (조건 선택 및 공통 시간 설정)
condition = st.sidebar.selectbox(
    "상세 분석할 조건 선택",
    ["치료군 (15분 손상 후 비타민C 사후처리)", "예방군 (15분 비타민C 선처리)", "동시처리군", "염산치료군 (강산 손상)", "산화처리군 (산화만)", "대조군 (무처리)"]
)

# 슬라이더: 이 시간이 '모든 집단'의 그래프 수치에 동시에 반영됩니다.
exposure_time = st.sidebar.slider(
    "처리 및 반응 유지 시간 (분)", 
    min_value=0, 
    max_value=60, 
    value=15,
    key="global_time_slider"
)

# 3. 모든 집단에 대해 설정된 시간(exposure_time)을 적용하여 콜로니 수 한꺼번에 연산

# [1] 대조군 (시간 영향 없음)
cnt_control = 250

# [2] 예방군 (시간에 따른 연산)
if exposure_time <= 15:
    pct_prev = 75.0 + (exposure_time * 0.6)
else:
    pct_prev = max(50.0, 84.0 - ((exposure_time - 15) * 0.4))
cnt_prevent = int(250 * (pct_prev / 100.0))

# [3] 동시처리군 (시간에 따른 연산)
pct_simul = max(30.0, 58.0 - ((exposure_time - 15) * 0.3))
cnt_simul = int(250 * (pct_simul / 100.0))

# [4] 치료군 (시간에 따른 연산 - 15분 이후 급격히 감소)
base_pct_treat = 30.0 - ((exposure_time - 15) * 1.0) if exposure_time >= 15 else 30.0 + ((15 - exposure_time) * 1.5)
pct_treat = max(0.0, base_pct_treat)
cnt_treat = int(250 * (pct_treat / 100.0))

# [5] 산화처리군 & 염산치료군 (0개 고정)
cnt_oxidized = 0
cnt_acid = 0


# 4. 상단 카드에는 선택한 카테고리의 '상세 정보' 출력
if condition == "대조군 (무처리)":
    selected_count = cnt_control
    b_value = 159.0
    status = "🟢 정상 (손상 없음)"

elif "예방군" in condition:
    selected_count = cnt_prevent
    b_value = 161.0
    status = "🔵 최상 (사전 예방으로 세포 및 DNA 완벽 보호)"

elif "동시처리군" in condition:
    selected_count = cnt_simul
    b_value = 162.0
    status = "🟡 양호 (산화와 항산화 반응 동시 진행)"

elif "치료군 (15분" in condition:
    selected_count = cnt_treat
    b_value = 155.7
    if exposure_time <= 10:
        status = "🟡 골든타임 이내 (빠른 사후 조치로 높은 복구율)"
    elif exposure_time <= 20:
        status = "🟠 경고 (손상 진행으로 세포 복구 한계 발생)"
    else:
        status = "🔴 골든타임 초과 (비가역적 세포 손상 진행)"

elif "염산" in condition:
    selected_count = cnt_acid
    b_value = 169.3
    status = "🔴 위험 (강산으로 인한 세포 완숙 파괴)"

else: # 산화처리군
    selected_count = cnt_oxidized
    b_value = 156.7
    status = "🔴 치명적 (항산화제 미투여로 대량 사멸)"

# 백분율 계산
survival_rate_pct = (selected_count / 250.0) * 100.0
dna_relative_pct = (b_value / 159.0) * 100.0

# 5. 선택 집단 상세 결과 출력
st.subheader("📊 선택 조건 상세 분석 결과")
col1, col2, col3 = st.columns(3)
col1.metric("예상 콜로니 개수", f"{selected_count} 개")
col2.metric("세포 생존율", f"{survival_rate_pct:.1f} %")
col3.metric("상대 DNA B값 비율", f"{dna_relative_pct:.1f} %")

st.info(f"**판정 결과:** {status}")


# 6. ⭐ 핵심: 슬라이더 시간(exposure_time)이 전치되어 연산된 '모든 집단' 그래프 시각화
st.subheader(f"📈 전체 그룹별 콜로니 수 비교 ({exposure_time}분 기준 연산 결과)")

data = {
    'Group': ['Control', 'Prevent', 'Simultaneous', 'Treat', 'Oxidized', 'Acid-Treat'],
    'Colony Count': [cnt_control, cnt_prevent, cnt_simul, cnt_treat, cnt_oxidized, cnt_acid]
}
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(8, 4))
colors = ['gray', 'blue', 'green', 'orange', 'red', 'purple']
ax.bar(df['Group'], df['Colony Count'], color=colors)
ax.set_ylabel("Yeast Colony Count")
ax.set_ylim(0, 280)

# 막대 상단 수치 표시
for i, v in enumerate(df['Colony Count']):
    ax.text(i, v + 5, str(v), ha='center', fontweight='bold')

st.pyplot(fig)

st.write("---")
st.caption("💡 슬라이더로 조절한 시간이 모든 집단의 예상 수치에 동시에 연동되어 시각화됩니다.")
