import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Monthly Visualization (Stock vs Show)", layout="wide")
st.title("월간 넷플릭스 주가 & 월간 시청시간 1위 작품")

@st.cache_data
def load_monthly_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    return pd.read_csv(
        os.path.join(base_path, "2-1_total.csv"),
        parse_dates=['month_end', 'Date']
    ).sort_values('month_end')
df = load_monthly_data()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(
        x=df['month_end'],
        y=df['Close'],
        mode='lines+markers+text',
        text=[f"{val:.2f}" for val in df['Close']],
        textposition='top center',
        textfont=dict(color='blue', size=10),
        name='Monthly Stock Price',
        line=dict(color='blue'),
    ),
    secondary_y=False
)

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

min_c = df['Close'].min()
max_c = df['Close'].max()
fig.update_yaxes(
    title_text="Stock Price (USD)",
    range=[min_c-100, max_c+100],
    secondary_y=False
)
fig.update_yaxes(
    title_text="Monthly Hours Viewed",
    tickformat="~s",
    secondary_y=True
)

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

st.title("📈 주가 분석 (추가)")
st.write("이 페이지에서는 최종 전처리된 CSV('2-1_total.csv')를 직접 불러와 시각화합니다.")