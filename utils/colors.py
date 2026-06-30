"""
MQD Dashboard
Color Utilities
"""


def get_score_color(score: float) -> str:
    """
    MQD Score에 따른 색상 반환
    """

    if score >= 80:
        return "#00C853"      # Strong Green

    elif score >= 60:
        return "#64DD17"      # Green

    elif score >= 40:
        return "#FFD600"      # Yellow

    elif score >= 20:
        return "#FF9100"      # Orange

    return "#D50000"          # Red


def get_score_label(score: float) -> str:
    """
    MQD Score Label
    """

    if score >= 80:
        return "🟢 Strong Buy"

    elif score >= 60:
        return "🟢 Buy"

    elif score >= 40:
        return "🟡 Neutral"

    elif score >= 20:
        return "🟠 Weak"

    return "🔴 Risk"
