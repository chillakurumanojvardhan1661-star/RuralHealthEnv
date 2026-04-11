def normalize_score(score: float) -> float:
    """Clamps score strictly between 0 and 1 using EPS."""
    EPS = 1e-6
    return max(EPS, min(1.0 - EPS, score))
