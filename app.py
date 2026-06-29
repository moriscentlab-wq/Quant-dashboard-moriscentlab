import streamlit as st

from charts.price_chart import draw_price_chart
from utils.colors import get_score_color, get_score_label

st.set_page_config(
    page_title="MQD v1.0",
    page_icon="📈",
    layout="wide"
)

st.title("📈 MQD v1.0")

st.success("프로젝트가 정상적으로 실행되었습니다.")

color = get_score_color(score)
label = get_score_label(score)

st.markdown(
    f"""
    <h2 style='color:{color};'>
    MQD Score : {score:.1f} ({label})
    </h2>
    """,
    unsafe_allow_html=True,
)
