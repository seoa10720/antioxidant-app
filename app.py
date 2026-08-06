import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. 앱 제목과 설명
st.title("🧪 세포/DNA 산화 스트레스 및 항산화 골든타임 예측기")
st.write("실험 데이터를 바탕으로 비타민 C 투여 시점 및 제제 종류에 따른 세포 복구 효율을 계산합니다.")

st.sidebar.header("⚙️ 실험 조건 설정")

# 2. 사용자 입력 (조건 선택)
condition = st.sidebar.selectbox(
    "처리 조건 선택",
    ["치료군 (산화제 노출 후 비타민C 처리)", "예방군 (비타민C 선처리 후 산화제)", "동시처리군", "염산치료군 (강산 손상 후 치료)", "산화만 (치료X)", "대조군 (무처리)"]
)

# 3. 조건에 따른 슬라이더 제목 자동 변경
if "예방군" in condition:
    slider_label = "비타민 C 선처리 후 산화제 투여까지 시간 (분)"
elif "치료군" in condition or "염산" in condition:
    slider_label = "산화제(또는 염산) 노출 후 비타민 C 투여까지 시간 (분)"
else:
    slider_label = "반응 유지 시간 (분)"

exposure_time = st.sidebar.slider(slider_label, 0, 60, 20)

# 4. 조건별 데이터 및 수학적 모델 계산
if condition == "대조군 (무처리)":
    survival_rate = 100.0
    dna_clarity = 100.0
    status = "🟢 정상 (손상 없음)"

elif "예방군" in condition:
    # 예방군: 선처리 후 산화제 투여까지의 시간에 따른 변화
    if exposure_time < 5:
        survival_rate = 75.0 + (exposure_time * 2.0)
        dna_clarity = 80.0 + (exposure_time * 1.5)
        status = "🔵 양호 (선처리 시간이 짧아 항산화 보호막 형성 진행 중)"
    elif exposure_time <= 25:
        survival_rate = 92.0
        dna_clarity = 90.0
        status = "🔵 최상 (사전 예방으로 세포 및 DNA 완벽 방어)"
    else:
        survival_rate = max(60.0, 92.0 - ((exposure_time - 25) * 0.5))
        dna_clarity = max(65.0, 90.0 - ((exposure_time - 25) * 0.5))
        status = "🟡 보통 (선처리 후 시간이 오래 경과하여 예방 효과 소폭 감소)"

elif "동시처리군" in condition:
    survival_rate = max(40.0, 70.0 - (exposure_time * 0.2))
    dna_clarity = max(45.0, 75.0 - (exposure_time * 0.2))
    status = "🟡 양호 (산화와 항산화 반응이 동시 진행됨)"

elif "치료군 (산화제" in condition:
    # 치료군: 노출 시간이 길어질수록 생존율 급격히 감소
    base_survival = 80.0 - (exposure_time * 1.2)
    base_dna = 85.0 - (exposure_time * 1.3)
    
    survival_rate = max(5.0, base_survival)
    dna_clarity = max(5.0, base_dna)
    
    if exposure_time <= 10:
        status = "🟡 골든타임 이내! (빠른 치료로 높은 복구율 보임)"
    elif exposure_time <= 25:
        status = "🟠 경고 (손상이 진행되어 복구 효율이 떨어짐)"
    else:
        status = "🔴 골든타임 초과! (세포 손상 심화로 항산화 복구 한계)"

elif "염산" in condition:
    survival_rate = max(1.0, 25.0 - (exposure_time * 0.8))
    dna_clarity = max(1.0, 20.0 - (exposure_time * 0.7))
    status = "🔴 위험 (강산성 조건으로 인한 비가역적 단백질/DNA 변성)"

else: # 산화만
    survival_rate = max(2.0, 30.0 - (exposure_time * 0.5))
    dna_clarity = max(2.0, 35.0 - (exposure_time * 0.5))
    status = "🔴 치명적 (항산화 방어 없이 지속적인 산화 손상 누적)"

# 5. 결과 출력
st.subheader("📊 분석 결과")
col1, col2 = st.columns(2)
col1.metric("예상 세포 생존율", f"{survival_rate:.1f} %")
col2.metric("DNA Band 선명도 (상대값)", f"{dna_clarity:.1f} %")

st.info(f"**판정 결과:** {status}")

# 6. 그래프 시각화 (폰트 깨짐 방지를 위한 영문 라벨 설정 및 실시간 연동)
st.subheader("📈 그룹별 생존율 비교")

prev_val = survival_rate if "예방군" in condition else 88.0
treat_val = survival_rate if "치료군 (산화제" in condition else 40.0
acid_val = survival_rate if "염산" in condition else 3.0

data = {
    'Group': ['Control', 'Prevent', 'Simultaneous', 'Treat', 'Oxidized', 'Acid-Treat'],
    'Survival Rate (%)': [100.0, prev_val, 63.0, treat_val, 15.0, acid_val]
}
df = pd.DataFrame(data)

fig, ax = plt.subplots(figsize=(8, 4))
colors = ['gray', 'blue', 'green', 'orange', 'red', 'purple']
ax.bar(df['Group'], df['Survival Rate (%)'], color=colors)
ax.set_ylabel("Cell Survival Rate (%)")
ax.set_ylim(0, 110)
st.pyplot(fig)

st.write("---")
st.caption("💡 본 프로그램은 효모 PDA 배지 콜로니 계측 및 전기영동 B값 정량 데이터를 기반으로 작동합니다.")
