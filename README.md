# E-commerce Email Uplift: A/B, CIs, (CUPED next)

Hillstrom’s Email Marketing case. Цель: понять, **кому** и **какое** письмо слать, чтобы максимизировать инкрементальный доход.

## 🔎 Problem
Бизнес-вопрос: «Стоит ли слать промо-e-mail и какое письмо (Mens/Womens) приносит больше **покупок** и **выручки**?»

## 🧰 Stack
Python · numpy · pandas · matplotlib · seaborn · scikit-learn  
(без тяжёлых uplift-библиотек; статистика — руками)

## 📦 Data
**Hillstrom Email Marketing** (3 сегмента): `No E-Mail` (control), `Mens E-Mail`, `Womens E-Mail`.  
Ключевые поля: `visit` (0/1), `conversion` (0/1), `spend` (>=0), `history` (доэкспер. траты).

## ✅ Results so far (Day 1–2)
**Primary goal:** purchases & revenue → `CR_conv` и `ARPU`.

**ΔCR_conv vs Control (pp, 95% CI):**
- Mens: **+0.68**  \[+0.500; +0.861] — significant  
- Womens: **+0.31** \[+0.150; +0.472] — significant

**ΔARPU vs Control (currency, 95% CI):**
- Mens: **+0.770** \[0.485; 1.054] — significant  
- Womens: **+0.424** \[0.169; 0.680] — significant

**Interpretation.** Оба письма поднимают покупки и выручку; **Mens > Womens** «в среднем по популяции».

> ARPU = средняя выручка на пользователя (нули включены).  
> Быстрый расчёт выгоды: **Incremental revenue ≈ N × ΔARPU**.  
> Порог безубыточности: слать выгодно, если **cost_per_email < margin × ΔARPU**.

## 📊 Figures
- `reports/figures/cr_conv_by_segment.png` — CR (conversion) по сегментам  


## 🧪 Method (Day 1–2)
- **A/B**: базовые метрики — `CR_visit`, `CR_conv`, `ARPU`.  
- **Parametric CIs**:  
  - ΔCR — разница долей с SE = √(p₁(1−p₁)/n₁ + p₀(1−p₀)/n₀), 95% CI = Δ ± 1.96·SE  
  - ΔARPU — Welch для разницы средних: SE = √(s₁²/n₁ + s₀²/n₀), 95% CI = Δ ± 1.96·SE

---------------------------------------------------------------------
**"01_eda.ipynb — exploratory scratch (ручные шаги, заметки)."**
**"02_ab_test.ipynb — воспроизводимый A/B: CR/ARPU + 95% CI (ДОДЕЛАТЬ CUPED)."**

## ▶️ Reproduce
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Данные: data/raw/hillstrom.csv (см. ноутбук)
