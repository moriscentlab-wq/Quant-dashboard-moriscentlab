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

st.write(
    """
    MQD 투자 시스템

    좌측 메뉴에서 기능을 선택하세요.
    """
)
