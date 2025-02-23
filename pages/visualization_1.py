import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Monthly Netflix (Stock price with Hours Viewed)", layout="wide")
st.title("Monthly Netflix")

@st.cache_data
def load_monthly_data():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    df = pd.read_csv(os.path.join(base_path, "2-1_total.csv"))
    
    df['month_end'] = pd.to_datetime(df['month_end'], errors='coerce')
    df.dropna(subset=['month_end'], inplace=True)
    df['month_end'] = df['month_end'].dt.tz_localize(None)
    df.sort_values('month_end', inplace=True)
    
    df['title_initial'] = df['show_title'].apply(lambda x: str(x)[0] if pd.notna(x) else '?')
    if 'poster_url' not in df.columns:
        df['poster_url'] = 'n.a.n.'
    else:
        df['poster_url'].fillna('n.a.n.', inplace=True)

    df['Close_prev'] = df['Close'].shift(1)
    df['stock_diff'] = (df['Close'] - df['Close_prev']).fillna(0)

    df['view_rank'] = df['weekly_hours_viewed'].rank(method='dense', ascending=False).astype(int)
    df['bar_text'] = df.apply(lambda r: f"<b>{r['view_rank']}</b><br>{r['title_initial']}", axis=1)

    df['bar_color'] = "#d40d17"

    return df

df = load_monthly_data().reset_index(drop=True)

xvals = df['month_end'].values.astype('datetime64[ns]')
xvals = np.sort(xvals)
min_c = df['Close'].min()
max_c = df['Close'].max()

line_segments = []
for i in range(len(df)-1):
    xseg = [df.loc[i,'month_end'], df.loc[i+1,'month_end']]
    yseg = [df.loc[i,'Close'], df.loc[i+1,'Close']]
    seg_color = '#d40d17' if yseg[1]>=yseg[0] else '#fa4848'
    seg_trace = go.Scatter(
        x=xseg, y=yseg,
        mode='lines',
        line=dict(color=seg_color, width=4, shape='spline', smoothing=1.3),
        name=('Monthly Stock Price' if i==0 else None),
        legendgroup='stock',
        showlegend=(i==0),
        hoverinfo='skip'
    )
    line_segments.append(seg_trace)

marker_colors = []
for i in range(len(df)):
    if i == 0:
        marker_colors.append('#d40d17')
    else:
        marker_colors.append('#d40d17' if df.loc[i,'Close']>=df.loc[i,'Close_prev'] else '#fa4848')

df_pos = df[df['stock_diff']>0].copy()
df_pos['diff_rank'] = df_pos['stock_diff'].rank(method='dense', ascending=False).astype(int)
df_pos_top10 = df_pos[df_pos['diff_rank']<=10].sort_values('diff_rank')
df_pos_top10['star_y'] = df_pos_top10['weekly_hours_viewed'] + (df['weekly_hours_viewed'].max()*0.05)

fig = make_subplots(specs=[[{"secondary_y": True}]])  

fig.add_trace(
    go.Bar(
        x=df['month_end'],
        y=df['weekly_hours_viewed'],
        name='Monthly Hours Viewed',
        legendgroup='hours',
        showlegend=True,
        text=df['bar_text'],
        textposition='inside',
        marker_color=df['bar_color'],
        hovertemplate="%{x|%Y-%m}<br><b>%{customdata[0]}</b><br>시청시간: %{y:,.0f}시간<br><extra></extra>",
        customdata=list(zip(df['show_title']))
    ),
    secondary_y=True
)

area_x = np.concatenate([df['month_end'], df['month_end'][::-1]])
area_y = np.concatenate([df['Close'], np.zeros(len(df))[::-1]])
gradient_area = go.Scatter(
    x=area_x,
    y=area_y,
    fill='toself',
    fillcolor='rgba(245, 228, 228, 0.65)',
    line=dict(color='rgba(0,0,0,0)'),
    hoverinfo='skip',
    name='Monthly Stock Price',
    legendgroup='stock',
    showlegend=False
)
fig.add_trace(gradient_area, secondary_y=False)

for seg in line_segments:
    fig.add_trace(seg, secondary_y=False)

fig.add_trace(
    go.Scatter(
        x=df['month_end'],
        y=df['Close'],
        mode='markers',
        name='Monthly Stock Price',
        legendgroup='stock',
        showlegend=False,
        marker=dict(size=6, color=marker_colors),
        hovertemplate="%{x|%Y-%m}<br>주가: $%{y:.2f}<extra></extra>"
    ),
    secondary_y=False
)

fig.add_trace(
    go.Scatter(
        x=df_pos_top10['month_end'],
        y=df_pos_top10['star_y'],
        mode='markers+text',
        name='Monthly Hours Viewed',
        legendgroup='hours',
        showlegend=False,
        marker=dict(symbol='star', size=14, color='#d40d17',
                    line=dict(width=1, color='#d40d17')),
        text=df_pos_top10['diff_rank'].astype(str),
        textposition='middle center',
        textfont=dict(color='white', size=9),
        hovertemplate=(
            "상승폭 순위: %{text}<br>"
            "상승폭: $%{customdata:.2f}<extra></extra>"
        ),
        customdata=df_pos_top10['stock_diff'],
    ),
    secondary_y=True
)

fig.update_layout(
    hovermode='closest',
    height=800,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(color='black'),
    title=dict(
        text="Stock price with Hours Viewed",
        font=dict(color='black', size=28),
        x=0.5, xanchor='center'
    ),
    legend=dict(
        font=dict(color='black', size=12),
        x=1.02, y=1,
        xanchor='left', yanchor='top',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='white',
        borderwidth=1
    )
)

min_c = df['Close'].min()
max_c = df['Close'].max()
fig.update_yaxes(
    title_text="Stock Price (USD)",
    range=[0, max_c+50],
    color='black',
    secondary_y=False,
    showgrid=True, gridcolor='white',
    zeroline=False
)
fig.update_yaxes(
    title_text="Monthly Hours Viewed",
    tickformat="~s",
    color='black',
    secondary_y=True,
    showgrid=False,
    zeroline=False
)

start_py = df['month_end'].iloc[0]
end_py   = df['month_end'].iloc[-1]
fig.update_xaxes(
    type='date',
    range=[start_py, end_py],
    tickformat='%Y-%m',
    tickangle=-45,
    color='black',
    rangeslider=dict(visible=True, bgcolor='#eee')
)

def shift_months_from_end(nmonths=6):
    if len(xvals)==0:
        return [datetime(2021,1,1), datetime(2021,7,1)]
    end_pd = pd.to_datetime(xvals[-1])
    start_pd = end_pd - pd.DateOffset(months=nmonths)
    start_pd_np = np.datetime64(start_pd)
    if start_pd_np < xvals[0]:
        start_pd_np = xvals[0]
    idx = np.searchsorted(xvals, start_pd_np, side='left')
    idx = max(0, idx)
    return [pd.to_datetime(xvals[idx]).to_pydatetime(),
            pd.to_datetime(xvals[-1]).to_pydatetime()]

range_6m = shift_months_from_end(6)
range_1y = shift_months_from_end(12)
range_all = [
    pd.to_datetime(xvals[0]).to_pydatetime(),
    pd.to_datetime(xvals[-1]).to_pydatetime()
]

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.02, y=1.12,
            bgcolor='rgba(200,200,200,0.4)',
            font=dict(color='black'),
            showactive=False,
            buttons=[
                dict(label="6m", method="relayout", args=[{"xaxis.range": range_6m}]),
                dict(label="1y", method="relayout", args=[{"xaxis.range": range_1y}]),
                dict(label="All",method="relayout", args=[{"xaxis.range": range_all}]),
            ]
        )
    ]
)

st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
