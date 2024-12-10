import streamlit as st
import pandas as pd
import plotly.express as px

st.title('投資計算器')

# 側邊欄：選擇計算類型
calc_type = st.sidebar.selectbox(
    '選擇計算類型',
    ['複利計算', '股票維持率計算', '定期定額試算']
)

if calc_type == '複利計算':
    col1, col2 = st.columns([2,1])
    
    with col1:
        principal = st.number_input('初始投資金額', min_value=0, value=10000)
        rate = st.number_input('年報酬率 (%)', min_value=0.0, value=5.0)
        years = st.number_input('投資年數', min_value=1, value=5)
    
    # 計算每年的投資金額
    yearly_values = []
    for year in range(years + 1):
        value = principal * (1 + rate/100) ** year
        yearly_values.append({'年份': year, '投資金額': value})
    
    df = pd.DataFrame(yearly_values)
    
    # 顯示結果
    future_value = yearly_values[-1]['投資金額']
    st.write(f'### 投資結果')
    st.write(f'經過 {years} 年後，你的投資將成長至: ${future_value:,.2f}')
    
    # 繪製成長曲線圖
    fig = px.line(df, x='年份', y='投資金額', 
                  title='投資成長曲線',
                  labels={'投資金額': '金額 ($)'})
    st.plotly_chart(fig)
    
    # 顯示詳細數據表
    with st.expander('查看詳細年度數據'):
        st.dataframe(df.style.format({'投資金額': '${:,.2f}'}))

        
elif calc_type == '股票維持率計算':
    stock_value = st.number_input('股票市值', min_value=0, value=10000)
    margin_req = st.number_input('維持率要求 (%)', min_value=0.0, value=25.0)
    
    maintenance_margin = stock_value * (margin_req/100)
    st.write(f'### 維持保證金')
    st.write(f'需要的維持保證金: ${maintenance_margin:,.2f}')

elif calc_type == '定期定額試算':
    monthly_invest = st.number_input('每月投資金額', min_value=0, value=1000)
    years = st.number_input('投資年數', min_value=1, value=10)
    rate = st.number_input('預期年報酬率 (%)', min_value=0.0, value=6.0)
    
    months = years * 12
    monthly_rate = rate/100/12
    future_value = monthly_invest * ((1 + monthly_rate)**(months) - 1) / monthly_rate
    
    st.write(f'### 定期定額結果')
    st.write(f'總投入金額: ${monthly_invest * months:,.2f}')
    st.write(f'預期最終金額: ${future_value:,.2f}')
    
