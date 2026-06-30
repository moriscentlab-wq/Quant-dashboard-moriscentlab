"""
MQD Dashboard
Color Utility

Provides color and label mapping for MQD Score.
"""

from __future__ import annotations


def get_score_color(score: float) -> str:
    """
    Return a color based on the MQD Score.

    Parameters
    ----------
    score : float
        MQD Score (0~100)

    Returns
    -------
    str
        Hex color code.
    """

    if score >= 80:
        return "#2E7D32"  # Green

    if score >= 60:
        return "#66BB6A"  # Light Green

    if score >= 40:
        return "#FDD835"  # Yellow

    if score >= 20:
        return "#FB8C00"  # Orange

    return "#E53935"  # Red


def get_score_label(score: float) -> str:
    """
    Return a label based on the MQD Score.

    Parameters
    ----------
    score : float
        MQD Score (0~100)

    Returns
    -------
    str
        Score label.
    """

    if score >= 80:
        return "Strong Buy"

    if score >= 60:
        return "Buy"

    if score >= 40:
        return "Neutral"

    if score >= 20:
        return "Weak"

    return "Risk"
