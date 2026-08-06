import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 앱 제목과 설명
st.title("🧪 세포/DNA 산화 스트레스 및 항산화 골든타임 예측기")
st.write("실험 데이터를 바탕으로 비타민 C 투여 시점 및 제제 종류에 따른 세포 복구 효율을 계산합니다.")

st.sidebar.header("⚙️ 실험 조건 설정")

# 2. 사용자 입력 (슬라이더 및 선택창)
condition = st.sidebar.selectbox(
    "처리 조건 선택",
    ["예방군 (선투여)", "동시처리군", "치료군 (20분 후 투여)", "염산치료군 (강산 손상)", "산화만 (치료X)", "대조군 (무처리)"]
)

exposure_time = st.sidebar.slider("산화제 노출 후 항산화제 투여까지 시간 (분)", 0, 60, 20)

# 3. 데이터 및 예측 로직
if condition == "대조군 (무처리)":
    survival_rate = 100.0
    dna_clarity = 100.0
    status = "🟢 정상 (손상 없음)"
elif condition == "예방군 (선투여)":
    survival_rate = 88.0
    dna_clarity = 90.0
    status = "🔵 최상 (사전 예방으로 세포 및 DNA 완벽 보호)"
elif condition == "동시처리군":
    survival_rate = 63.0
    dna_clarity = 70.0
    status = "🟡 양호 (일부 산화 방어 성공)"
elif condition == "치료군 (20분 후 투여)":
    # 노출 시간에 따라 생존율 감쇄 계산
    survival_rate = max(10.0, 40.0 - (exposure_time - 20) * 0.8)
    dna_clarity = max(10.0, 45.0 - (exposure_time - 20) * 0.8)
    status = "🟠 경고 (손상 진행 후 투여로 복구 한계 발생)"
elif condition == "염산치료군 (강산 손상)":
    survival_rate = 3.0
    dna_clarity = 4.0
    status = "🔴 위험 (강산으로 인한 비가역적 세포 파괴)"
else: # 산화만
    survival_rate = 15.0
    dna_clarity = 18.0
    status = "🔴 위험 (항산화제 미투여로 대량 사멸)"

# 4. 결과 출력
st.subheader("📊 분석 결과")
col1, col2 = st.columns(2)
col1.metric("예상 세포 생존율", f"{survival_rate:.1f} %")
col2.metric("DNA Band 선명도 (상대값)", f"{dna_clarity:.1f} %")

st.info(f"**판정 결과:** {status}")

# 5. 그래프 시각화
st.subheader("📈 그룹별 비교 그래프")
data = {
    '그룹': ['대조군', '예방군', '동시처리', '치료군', '산화만', '염산치료'],
    '생존율(%)': [100, 88, 63, survival_rate if condition == '치료군 (20분 후 투여)' else 40, 15, 3]
}
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(8, 4))
colors = ['gray', 'blue', 'green', 'orange', 'red', 'purple']
ax.bar(df['그룹'], df['생존율(%)'], color=colors)
ax.set_ylabel("Cell Survival Rate (%)")
st.pyplot(fig)

st.write("---")
st.caption("💡 본 프로그램은 효모 PDA 배지 콜로니 계측 및 전기영동 B값 정량 데이터를 기반으로 작동합니다.")
