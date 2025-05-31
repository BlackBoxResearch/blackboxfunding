import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# --- Synthetic data generator ---
def generate_path(S0, num_points, r, t_step, V, rand, rand_trend, mean, mean_reversion):
    S = S0 * np.ones(num_points)
    trend = 0
    for i in range(1, num_points):
        trend += rand_trend[i-1] * S[i-1] / 2000 - trend / 10
        S[i] = mean_reversion * (mean - S[i-1]) + S[i-1] * np.exp(
            (r - 0.5 * V**2) * t_step + np.sqrt(t_step) * V * rand[i-1]
        ) + 0.7 * trend
    return S

# --- Chart config ---
def generate_chart_data(seed, num_points=50000):
    rs = np.random.RandomState(seed)
    rand = rs.standard_normal(num_points - 1)
    rand_trend = rs.standard_normal(num_points - 1)

    prices = generate_path(
        S0=1,
        num_points=num_points,
        r=0,
        t_step=1/365,
        V=0.1,
        rand=rand,
        rand_trend=rand_trend,
        mean=1,
        mean_reversion=0.004
    )

    start_date = datetime.strptime("2018-12-22", "%Y-%m-%d")
    return [
        {
            "time": (start_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "value": round(price, 5)
        }
        for i, price in enumerate(prices)
    ]

# --- Session state to hold seeds ---
if "seed1" not in st.session_state:
    st.session_state.seed1 = 123
if "seed2" not in st.session_state:
    st.session_state.seed2 = 456

# --- Regenerate button ---
if st.button("Regenerate Data"):
    st.session_state.seed1 = np.random.randint(1, 100000)
    st.session_state.seed2 = np.random.randint(1, 100000)

# --- Generate two datasets ---
data1 = generate_chart_data(st.session_state.seed1)
data2 = generate_chart_data(st.session_state.seed2)

# --- Chart visual config ---
chartOptions = {
    "layout": {
        "textColor": 'white',
        "background": {
            "type": 'solid',
            "color": 'rgb(16,12,12)'
        }
    },
    "grid": {
        "vertLines": { "visible": False },
        "horzLines": { "visible": False }
    },
    "timeScale": { "borderColor": "white" },
    "rightPriceScale": { "borderColor": "white" },
    "height": 300,
}

def create_series(data):
    return [{
        "type": 'Baseline',
        "data": data,
        # "options": {
        #     "lineColor": "#e0dcdc",
        #     "lineWidth": 1,
        #     "topColor": "rgba(192, 188, 188, 0.3)",
        #     "bottomColor": "rgba(192, 188, 188, 0.0)"
        # }
        "options": {
            "baseValue": {"type": "price", "price": 1},
            "topLineColor": 'rgba( 38, 166, 154, 1)',
            "topFillColor1": 'rgba( 38, 166, 154, 0.28)',
            "topFillColor2": 'rgba( 38, 166, 154, 0.05)',
            "bottomLineColor": 'rgba( 239, 83, 80, 1)',
            "bottomFillColor1": 'rgba( 239, 83, 80, 0.05)',
            "bottomFillColor2": 'rgba( 239, 83, 80, 0.28)',
            "lineWidth": 1,
        }
    }]

# --- UI ---
st.title("Welcome, Ben", anchor=False)
st.caption("Last login 10/05/25 00:31")
st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.container(border=False):
        st.markdown("**Chart 1 – Synthetic Feed A**")
        renderLightweightCharts([
            {
                "chart": chartOptions,
                "series": create_series(data1),
            }
        ], 'area1')

with col2:
    with st.container(border=False):
        st.markdown("**Chart 2 – Synthetic Feed B**")
        renderLightweightCharts([
            {
                "chart": chartOptions,
                "series": create_series(data2),
            }
        ], 'area2')
