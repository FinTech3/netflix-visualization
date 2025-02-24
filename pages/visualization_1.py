import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Monthly Netflix (Stock Price and Hours Viewed)",
    layout="wide"
)

col1, col2 = st.columns([0.1, 8.0])
with col1:
    st.markdown("""<div style="font-size:30px;font-weight:bold;"></div>""",
                unsafe_allow_html=True)
with col2:
    logo_path = os.path.join(os.path.dirname(__file__), "..", "data", "netflix_logo_w.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=250)

st.markdown("""
<div style="
  text-align:center;
  background-color:#CE0019;
  padding:15px;
  border-radius:90px;
  width:30%;
  margin:auto;">
  <h3 style="color:white;width : 100%; text-align : center; padding : 0; ">Stock Price and Hours Viewed</h3>
</div>
""", unsafe_allow_html=True)

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
    df['diff_rank'] = df.apply(
        lambda r: np.nan if r['stock_diff']<=0 else r['stock_diff'], axis=1
    )
    df['diff_rank'] = df['diff_rank'].rank(method='dense', ascending=False)
    df['diff_rank'] = df['diff_rank'].fillna(9999).astype(int)

    df['view_rank'] = df['weekly_hours_viewed'].rank(method='dense', ascending=False).astype(int)
    df['bar_text'] = df.apply(lambda r: f"{r['view_rank']}\n{r['title_initial']}", axis=1)
    df['bar_color'] = "#F15A24"

    return df.reset_index(drop=True)

df = load_monthly_data()

xvals = df['month_end'].values.astype('datetime64[ns]')
xvals = np.sort(xvals)
min_c = df['Close'].min()
max_c = df['Close'].max()

df_top5 = df[df['diff_rank']<=5].copy()
df_top5['star_y'] = df_top5['weekly_hours_viewed'] + df['weekly_hours_viewed'].max()*0.05

line_segments = []
for i in range(len(df)-1):
    xseg = [df.loc[i,'month_end'], df.loc[i+1,'month_end']]
    yseg = [df.loc[i,'Close'], df.loc[i+1,'Close']]
    seg_trace = go.Scatter(
        x=xseg, 
        y=yseg,
        mode='lines',
        line=dict(color='#CE0019', width=4, shape='spline', smoothing=1.3),
        name=('Monthly Stock Price' if i==0 else None),
        legendgroup='stock',
        showlegend=(i==0),
        hoverinfo='skip'
    )
    line_segments.append(seg_trace)

marker_trace = go.Scatter(
    x=df['month_end'],
    y=df['Close'],
    mode='markers',
    name='Monthly Stock Price',
    legendgroup='stock',
    showlegend=False,
    marker=dict(size=6, color='#CE0019'),
    customdata=df[['Close']],
    hovertemplate=(
        "%{x|%Y-%m}<br>"
        "<b>Netflix</b><br>"
        "주가: $%{customdata[0]:.2f}"
        "<extra></extra>"
    )
)

star_trace = go.Scatter(
    x=df_top5['month_end'],
    y=df_top5['star_y'],
    mode='markers',
    name='Monthly Hours Viewed',
    legendgroup='hours',
    showlegend=False,
    marker=dict(symbol='star', size=5, color='red', line=dict(width=1.5, color='red')),
    customdata=df_top5[['diff_rank','stock_diff', 'show_title']],
    hovertemplate=(
        "%{x|%Y-%m}<br>"
        "<b>%{customdata[2]}</b><br>"
        "상승폭: $%{customdata[1]:.2f}<br>"
        "주가상승폭 순위: %{customdata[0]}"
        "<extra></extra>"
    )
)

fig = make_subplots(specs=[[{"secondary_y": True}]])

bar_trace = go.Bar(
    x=df['month_end'],
    y=df['weekly_hours_viewed'],
    name='Monthly Hours Viewed',
    legendgroup='hours',
    showlegend=True,
    text=df['bar_text'],
    textposition='inside',
    textfont=dict(color='#F15A24', size=11),
    marker_color=df['bar_color'],
    customdata=df[['view_rank','show_title','poster_url']],
    hovertemplate=(
        "%{x|%Y-%m}<br>"
        "<b>%{customdata[1]}</b><br>"
        "누적시청순위: %{customdata[0]}<br>"
        "시청시간: %{y:,.0f}시간<br>"
        "<extra></extra>"   # <-- trace 이름 제거
    )
)
fig.add_trace(bar_trace, secondary_y=True)
fig.add_trace(star_trace, secondary_y=True)

area_x = np.concatenate([df['month_end'], df['month_end'][::-1]])
area_y = np.concatenate([df['Close'], np.zeros(len(df))[::-1]])
gradient_area = go.Scatter(
    x=area_x,
    y=area_y,
    fill='toself',
    fillcolor='rgba(249, 243, 239, 0.65)',
    line=dict(color='rgba(0,0,0,0)'),
    hoverinfo='skip',
    name='Monthly Stock Price',
    legendgroup='stock',
    showlegend=False
)
fig.add_trace(gradient_area, secondary_y=False)

for seg in line_segments:
    fig.add_trace(seg, secondary_y=False)
fig.add_trace(marker_trace, secondary_y=False)

# 레이아웃 / 스타일
fig.update_layout(
    hovermode='closest',
    height=800,
    paper_bgcolor='white',
    plot_bgcolor='white',
    font=dict(color='black'),
    legend=dict(
        font=dict(color='black', size=12),
        x=1.02, y=1,
        xanchor='left', yanchor='top',
        bgcolor='rgba(255,255,255,0.7)',
        bordercolor='white',
        borderwidth=1
    )
)

fig.update_yaxes(
    title_text="Stock Price (USD)",
    range=[0, max_c+50],
    color='black',
    secondary_y=False,
    showgrid=True,
    gridcolor='white',
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

tickvals = df['month_end']
ticktext = df['month_end'].dt.strftime('%Y-%m')
start_py = df['month_end'].iloc[0]
end_py = df['month_end'].iloc[-1]
fig.update_xaxes(
    type='date',
    range=[start_py, end_py],
    tickmode='array',
    tickvals=tickvals,
    ticktext=ticktext,
    tickangle=-45,
    color='black',
    rangeslider=dict(visible=True, bgcolor='#eee')
)

def shift_months_from_end(nmonths=6):
    if len(xvals) == 0:
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
range_all = [pd.to_datetime(xvals[0]).to_pydatetime(),
             pd.to_datetime(xvals[-1]).to_pydatetime()]

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.02, y=1.12,
            bgcolor='rgba(255, 253, 252,0.4)',
            font=dict(color='black'),
            showactive=False,
            buttons=[
                dict(label="6m", method="relayout", args=[{"xaxis.range": range_6m}]),
                dict(label="1y", method="relayout", args=[{"xaxis.range": range_1y}]),
                dict(label="All", method="relayout", args=[{"xaxis.range": range_all}]),
            ]
        )
    ]
)

st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})
