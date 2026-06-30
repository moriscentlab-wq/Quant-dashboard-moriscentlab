MQD(Mori Quant Dashboard) 프로젝트의

charts/price_chart.py

파일을 작성해주세요.

===================================

Python 3.12

Streamlit

Plotly

PEP8

Type Hint

Docstring

===================================

필수 함수

def draw_price_chart(
    data: pd.DataFrame,
) -> None

===================================

기능

Plotly 사용

종가(Close)

MA20

MA60

MA120

4개 라인 출력

-----------------------------------

차트 옵션

template="plotly_white"

height=600

hovermode="x unified"

use_container_width=True

-----------------------------------

legend 표시

-----------------------------------

Close는 굵게 표시

-----------------------------------

MA20

MA60

MA120

컬럼이 없으면 표시하지 말 것

-----------------------------------

Streamlit

st.plotly_chart()

사용

===================================

실행 가능한 전체 코드 작성

생략 금지

복사 후 바로 실행 가능해야 함
