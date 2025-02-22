import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Monthly Visualization (Stock vs Show)", layout="wide")
st.title("월간 넷플릭스 주가 & 월간 시청시간 1위 작품")

@st.cache_data
def load_monthly_data():
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data")
    )
    df = pd.read_csv(
        os.path.join(base_path, "2-1_total.csv")
    )
    df['month_end'] = pd.to_datetime(df['month_end'], errors='coerce')
    df.dropna(subset=['month_end'], inplace=True)
    
    df.sort_values('month_end', inplace=True)
    
    df['title_initial'] = df['show_title'].apply(lambda x: str(x)[0] if pd.notna(x) else '?')

    if 'poster_url' not in df.columns:
        df['poster_url'] = 'n.a.n.'
    else:
        df['poster_url'].fillna('n.a.n.', inplace=True)

    df['Close_prev'] = df['Close'].shift(1)
    df['stock_diff'] = (df['Close'] - df['Close_prev']).fillna(0)
    max_abs_diff = df['stock_diff'].abs().max() or 1

    def get_bar_color(diff):
        ratio = abs(diff)/max_abs_diff
        if diff >= 0:
            r = 255
            g = int(255 - 255*ratio)
            b = int(255 - 255*ratio)
        else:
            r = int(255 - 255*ratio)
            g = int(255 - 255*ratio)
            b = 255
        return f"rgba({r},{g},{b},0.8)"
    
    df['bar_color'] = df['stock_diff'].apply(get_bar_color)
    return df

df = load_monthly_data()

xvals = df['month_end'].dropna().values.astype('datetime64[ns]')
xvals = np.sort(xvals)
if len(xvals) == 0:
    xvals = np.array([np.datetime64('2021-01-01')])

min_c = df['Close'].min()
max_c = df['Close'].max()

def shift_months_from_end(nmonths=6):
    """최근 nmonths 달 범위를 [start, end]로 반환, 데이터 범위 안에서만."""
    if len(xvals) == 0:
        return [np.datetime64('2021-01-01'), np.datetime64('2021-07-01')]
    end_dt64 = xvals[-1]
    end_pd = pd.to_datetime(end_dt64)
    start_pd = end_pd - pd.DateOffset(months=nmonths)
    start_dt64 = np.datetime64(start_pd)
    if start_dt64 < xvals[0]:
        start_dt64 = xvals[0]
    idx = np.searchsorted(xvals, start_dt64, side='left')
    idx = max(0, idx)
    return [xvals[idx], xvals[-1]]

range_6m = shift_months_from_end(6)
range_1y = shift_months_from_end(12)
range_all = [xvals[0], xvals[-1]]

fig = make_subplots(specs=[[{"secondary_y": True}]])  

fig.add_trace(
    go.Scatter(
        x=df['month_end'],
        y=df['Close'],
        mode='lines+markers',
        name='Monthly Stock Price',
        line=dict(color='red', width=3),
        marker=dict(size=6, color='red'),
        hovertemplate=(
            "%{x|%Y-%m}<br>"
            "주가: $%{y:.2f}"
            "<extra></extra>"
        ),
    ),
    secondary_y=False
)

fig.add_trace(
    go.Bar(
        x=df['month_end'],
        y=df['weekly_hours_viewed'],
        name='Monthly Hours Viewed',
        text=df['title_initial'],
        textposition='inside',
        marker_color=df['bar_color'],
        hovertemplate=(
            "%{x|%Y-%m}<br>"
            "<b>%{customdata[0]}</b><br>"
            "시청시간: %{y:,.0f}시간<br>"
            "포스터: <img src='%{customdata[1]}' width='100' onerror=\"this.src='';this.alt='n.a.n.';\"/><br>"
            "<extra></extra>"
        ),
        customdata=list(zip(df['show_title'], df['poster_url'])),
        selected=dict(marker=dict(opacity=1)),
        unselected=dict(marker=dict(opacity=0.8)),
    ),
    secondary_y=True
)

fig.update_layout(
    hovermode='closest',
    height=800,
    paper_bgcolor='#222222',
    plot_bgcolor='#333333',
    font=dict(color='#FFFFFF'),
    title=dict(
        text="Monthly Stock vs Monthly #1 Show (Hours)",
        font=dict(color='#e50914', size=28),
        x=0.5,
        xanchor='center'
    ),
    legend=dict(
        font=dict(color='#FFFFFF', size=12),
        x=1.02, y=1,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(70,70,70,0.7)',
        bordercolor='gray',
        borderwidth=1
    ),
)

fig.update_yaxes(
    title_text="Stock Price (USD)",
    range=[0, max_c+50],
    color='white',
    secondary_y=False,
    showspikes=True,
    spikemode='toaxis',
    spikecolor='grey',
    spikethickness=1,
    spikedash='dash'
)

fig.update_yaxes(
    title_text="Monthly Hours Viewed",
    tickformat="~s",
    color='white',
    secondary_y=True,
    showspikes=True,
    spikemode='toaxis',
    spikecolor='grey',
    spikethickness=1,
    spikedash='dash'
)

xtexts = [pd.to_datetime(d).strftime('%Y-%m') for d in xvals]

fig.update_xaxes(
    tickmode='array',
    tickvals=xvals,
    ticktext=xtexts,
    tickangle=-45,
    color='white',
    range=[xvals[0], xvals[-1]],
    rangeslider=dict(
        visible=True,
        autorange=True,
        bgcolor='#444444'
    ),
    type='date'
)

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.02,
            y=1.12,
            bgcolor='rgba(100,100,100,0.4)',
            font=dict(color='white'),
            showactive=False,
            buttons=[
                dict(
                    label="6m",
                    method="relayout",
                    args=[{"xaxis.range": range_6m}],
                ),
                dict(
                    label="1y",
                    method="relayout",
                    args=[{"xaxis.range": range_1y}],
                ),
                dict(
                    label="All",
                    method="relayout",
                    args=[{"xaxis.range": range_all}],
                ),
            ]
        )
    ]
)

st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})

st.title("📈 주가 분석 (추가)")
st.write("이 페이지에서는 최종 전처리된 CSV('2-1_total.csv')를 직접 불러와 시각화합니다.")
