import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def wrap_text(txt, max_len=12):
    if pd.isna(txt):
        return ''
    txt = str(txt)
    lines = []
    while len(txt) > max_len:
        lines.append(txt[:max_len])
        txt = txt[max_len:]
    lines.append(txt)
    return "<br>".join(lines)

st.set_page_config(page_title="Monthly Visualization (Stock vs Show)", layout="wide")
st.title("월간 넷플릭스 주가 & 월간 시청시간 1위 작품")

@st.cache_data
def load_monthly_data():
    # (A) 넷플릭스 주가 CSV
    df_stock = pd.read_csv("data/nflx_stock_daily.csv", parse_dates=['Date'])
    df_stock.sort_values('Date', inplace=True)
    df_stock['year_month'] = df_stock['Date'].dt.to_period('M')
    
    # 마지막 거래일
    df_monthly_stock = df_stock.groupby('year_month').tail(1).copy()
    
    # (B) 넷플릭스 TSV
    df_nf = pd.read_csv("data/netflix_top10.tsv", sep='\t', parse_dates=['week'])
    df_nf.dropna(subset=['week','weekly_hours_viewed'], inplace=True)
    
    # 주간 1위
    df_top = df_nf.loc[df_nf.groupby('week')['weekly_hours_viewed'].idxmax()].copy()
    df_top.sort_values('week', inplace=True)
    df_top.reset_index(drop=True, inplace=True)
    
    # 월간 변환
    df_top['year_month'] = df_top['week'].dt.to_period('M')
    df_sum = df_top.groupby(['year_month','show_title'], as_index=False)['weekly_hours_viewed'].sum()
    idx = df_sum.groupby('year_month')['weekly_hours_viewed'].idxmax()
    df_monthly = df_sum.loc[idx].copy()
    
    # 달 말일 (Timestamp)
    # asfreq + to_timestamp
    df_monthly['month_end'] = df_monthly['year_month'].apply(
        lambda p: p.asfreq('D','end').to_timestamp()
    )
    
    # Merge
    df_monthly_merge = pd.merge(df_monthly, df_monthly_stock, on='year_month', how='inner')
    
    # 부분 월(2025-02 등) 제거
    df_monthly_merge = df_monthly_merge[df_monthly_merge['month_end'] <= pd.to_datetime('2025-01-31')]
    df_monthly_merge.reset_index(drop=True, inplace=True)
    
    # 래핑
    df_monthly_merge['title_wrapped'] = df_monthly_merge['show_title'].apply(lambda x: wrap_text(x, 12))
    
    return df_monthly_merge

df = load_monthly_data()

# (C) 그래프 생성
fig = make_subplots(specs=[[{"secondary_y": True}]])

# 왼쪽축: 주가
fig.add_trace(
    go.Scatter(
        x=df['month_end'],
        y=df['Close'],
        mode='lines+markers+text',
        text=[f"{val:.2f}" for val in df['Close']],
        textposition='top center',
        textfont=dict(color='blue', size=10),
        name='Monthly Stock Price',
        line=dict(color='blue')
    ),
    secondary_y=False
)

# 오른쪽축: 시청시간
fig.add_trace(
    go.Bar(
        x=df['month_end'],
        y=df['weekly_hours_viewed'],
        text=df['title_wrapped'],
        textposition='inside',
        textfont=dict(color='black', size=9),
        marker_color='rgba(255,165,0,0.6)',
        name='Monthly Hours Viewed'
    ),
    secondary_y=True
)

fig.update_layout(
    template='plotly_white',
    title="Monthly Stock vs Monthly #1 Show (Hours)",
    xaxis_title="Month End"
)

# Y축 범위
min_c = df['Close'].min()
max_c = df['Close'].max()
fig.update_yaxes(title_text="Stock Price (USD)",
                 range=[min_c-50, max_c+50],
                 secondary_y=False)

fig.update_yaxes(title_text="Monthly Hours Viewed",
                 tickformat="~s",
                 secondary_y=True)

# X축 Tickmode='array'
xvals = sorted(df['month_end'].unique())
xtexts = [f"{d.year}-{d.month:02d}" for d in xvals]
fig.update_xaxes(
    tickmode='array',
    tickvals=xvals,
    ticktext=xtexts,
    tickangle=-45,
    rangeslider=dict(visible=True),
    range=[xvals[0], xvals[-1]]
)

st.plotly_chart(fig, use_container_width=True)

st.set_page_config(page_title="주가 분석", layout="wide")

st.title("📈 주가 분석")
st.write("이 페이지에서는 주가 데이터를 시각화합니다.")