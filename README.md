# MQD (Mori Quant Dashboard)

**Version:** **v1.0.0**

MQD (Mori Quant Dashboard)는 **Python**과 **Streamlit** 기반의 퀀트 투자 분석 대시보드입니다. Yahoo Finance 데이터를 이용하여 기술적 지표를 계산하고, MQD Score를 통해 투자 판단에 필요한 정보를 직관적으로 제공합니다.

---

## Features

* Yahoo Finance 데이터 다운로드
* 이동평균선 (MA20, MA60, MA120)
* RSI (Relative Strength Index)
* Momentum
* ROC (Rate of Change)
* MQD Score 계산
* Confidence Score 계산
* Plotly 기반 인터랙티브 차트
* Streamlit Dashboard

---

## Project Structure

```text
MQD/
│
├── config/
│   ├── __init__.py
│   └── tickers.py
│
├── collectors/
│   ├── __init__.py
│   └── yahoo.py
│
├── indicators/
│   ├── __init__.py
│   ├── moving_average.py
│   ├── rsi.py
│   └── momentum.py
│
├── scoring/
│   ├── __init__.py
│   └── mqd_score.py
│
├── charts/
│   ├── __init__.py
│   └── price_chart.py
│
├── utils/
│   ├── __init__.py
│   └── colors.py
│
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

## Requirements

* Python 3.12
* Streamlit
* pandas
* numpy
* yfinance
* plotly

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd MQD
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

Start the Streamlit dashboard.

```bash
streamlit run streamlit_app.py
```

---

## Dashboard Workflow

1. Select Market
2. Select Ticker
3. Download Market Data
4. Calculate Moving Averages
5. Calculate RSI
6. Calculate Momentum
7. Calculate ROC
8. Calculate MQD Score
9. Calculate Confidence Score
10. Display Price Chart
11. Display Key Metrics
12. Display Last Update

---

## MQD Score

| Component    |  Weight |
| ------------ | ------: |
| MA Trend     |      25 |
| Close > MA20 |      15 |
| RSI          |      20 |
| MA20 Rising  |      20 |
| Momentum     |      10 |
| ROC          |      10 |
| **Total**    | **100** |

> **Confidence Score**는 MQD Score와 독립적으로 계산됩니다.

---

## Changelog

### v1.0.0

#### Added

* Yahoo Finance Collector
* Moving Average Indicator
* RSI Indicator
* Momentum Indicator
* ROC Indicator
* MQD Score Engine
* Confidence Score
* Plotly Price Chart
* Streamlit Dashboard

#### Improved

* Logging
* Type Hints
* Docstrings
* Error Handling
* PEP 8 Compliance

#### Fixed

* Import issues
* Duplicate code
* MultiIndex handling
* Data validation
* Exception handling

---

## Release Notes

MQD v1.0은 첫 번째 정식 릴리스입니다.

주요 개선 사항

* 종목 선택 후 필요한 데이터만 다운로드
* Streamlit Cache를 통한 성능 향상
* Plotly 기반 인터랙티브 차트
* 자동 기술적 지표 계산
* MQD Score 및 Confidence Score 제공
* 모듈화된 프로젝트 구조
* Python 3.12 호환
* 최신 yfinance API 기반 설계
* PEP 8 스타일 적용
* 예외 처리 및 로깅 강화

---

## License

본 프로젝트의 공개 배포 전에는 적절한 라이선스(예: MIT License, Apache License 2.0)를 선택하여 추가하시기 바랍니다.

---

## Disclaimer

MQD는 투자 분석을 지원하기 위한 도구이며, 투자 자문이나 매매 추천을 제공하지 않습니다. 모든 투자 결정과 그에 따른 책임은 사용자 본인에게 있습니다.
