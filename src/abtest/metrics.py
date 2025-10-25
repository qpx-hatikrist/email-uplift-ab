import numpy as np
import pandas as pd

def cr(y: pd.Series) -> float:
    """
    Conversion rate: доля наблюдений > 0 (подходит и для bool/int {0,1}).
    """
    return float((np.asarray(y) > 0).mean())

def arpu(r: pd.Series) -> float:
    """
    Average revenue per user: среднее по всем (нули включены).
    """
    return float(np.asarray(r).mean())

# --- вспомогательное: квантиль нормраспределения для частых alpha ---

_Z = {
    0.10: 1.6448536269514722,  # 90%
    0.05: 1.959963984540054,   # 95%
    0.01: 2.5758293035489004,  # 99%
}


def _z_from_alpha(alpha: float) -> float:
    # двухсторонний интервал: z_{1 - alpha/2}
    return _Z.get(alpha, _Z[0.05])

# --- CI для разницы долей (ΔCR) ---


def ci_delta_proportion(n1: int, n0: int, p1: float, p0: float, alpha: float=0.05)->dict:
    """
    Доверительные интервалы для Δ = p1 - p0 (двухсторонний).
    Параметры:
        n1, n0 : размеры групп (treatment, control)
        p1, p0 : доли в [0,1] (не в процентах!)
        alpha  : 0.05 -> 95% CI; поддержаны {0.10, 0.05, 0.01}
    Возвращает:
        delta_pp, ci_lo_pp, ci_hi_pp, significant, delta, se
    Пример:
        mens = ci_delta_proportion(n["Mens E-Mail"], n["No E-Mail"], p["Mens E-Mail"], p["No E-Mail"])
        print(f"ΔCR = {mens['delta_pp']:.2f} п.п.; 95% CI [{mens['ci_lo_pp']:.2f}; {mens['ci_hi_pp']:.2f}] — "
              f"{'значимо' if mens['significant'] else 'не значимо'}")
    """
    if n1 <= 0 or n0 <= 0:
        raise ValueError("n1 and n0 must be positive")
    if not (0 <= p1 <= 1 and 0 <= p0 <= 1):
        raise ValueError("p1 and p0 must be in [0, 1]")
    z = _z_from_alpha(alpha)
    delta = p1 - p0
    se = ((p1*(1-p1)/n1) + (p0*(1-p0)/n0))**0.5
    lo, hi = delta - z*se, delta + z*se
    result = {
        "delta_pp": round(delta*100, 4),        # точечная оценка
        "ci_lo_pp": round(lo*100, 4),           # нижняя граница
        "ci_hi_pp": round(hi*100, 4),           # верхняя граница
        "significant": (lo > 0) or (hi < 0),    # интервал не пересекает 0
        "delta": delta,                         # точечная оценка в доле
        "se": se,                               # se
    }

    return result

# --- CI для разницы средних (ΔARPU), Welch ---

def ci_delta_mean_welch(n1:int, n0:int, m1:float, m0:float, v1:float, v0:float, alpha:float=0.05)->dict:
    """
    Доверительные интервалы для Δ = m1 - m0 (двухсторонний), Welch (неравные дисперсии).
    По умолчанию используем (z≈1.96 при 95%).
    Возвращает:
        delta, ci_lo, ci_hi, significant, se
    Пример:
        m = ci_delta_mean_welch(agg.loc["Mens E-Mail","n"], agg.loc["No E-Mail","n"],
                        agg.loc["Mens E-Mail","mean"], agg.loc["No E-Mail","mean"],
                        agg.loc["Mens E-Mail","var"],  agg.loc["No E-Mail","var"])
        print(f"ΔARPU = {m['delta']:.3f}; 95% CI [{m['ci_lo']:.3f}; {m['ci_hi']:.3f}] — "
              f"{'значимо' if m['significant'] else 'не значимо'}")

    """
    
    if n1 <= 1 or n0 <= 1:
        raise ValueError("n1 and n0 must be > 1")
    z = _z_from_alpha(alpha)
    delta = m1 - m0
    se = ((v1/n1) + (v0/n0))**0.5
    lo, hi = delta - z*se, delta + z*se
    result = {
        "delta": round(delta, 4),
        "ci_lo": round(lo, 4),
        "ci_hi": round(hi, 4),
        "significant": (lo > 0) or (hi < 0),
        "se": se,
    }
    return result