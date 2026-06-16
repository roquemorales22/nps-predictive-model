# NPS Promoter Classifier 🏦

A machine learning project developed as part of a real-world case study presented to **Santander Mexico**. The goal was to analyze NPS survey data from Mexican banking customers and build a model to identify what separates a **Passive customer from a Promoter** — and how the bank can act on it.

---

## 🔍 What It Does

- Exploratory analysis of NPS, CES, and CSAT metrics across customer segments
- Spearman correlation analysis to identify drivers of Promoter conversion
- VIF multicollinearity analysis for feature selection
- Binary classification model (Logistic Regression) to predict Passive → Promoter conversion
- Feature importance ranking with actionable levers for the bank
- Churn risk proxy metric built from survey signals
- SMOTE validation to test robustness under class imbalance
- Interactive Streamlit dashboard for hypothesis exploration

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| Recall (Promoters) | 0.79 |
| Precision (Promoters) | 0.85 |
| AUC-ROC | 0.808 |
| Accuracy | 0.76 |

**Top conversion drivers:** Digital Ease (24.9%), Digital Stability (21.4%), Transparency (18.6%), Speed (19%), Human Support (16%)

---

## 🗂 Project Structure

- `santander_case.ipynb` — Main analysis notebook
- `data_processing.py` — Data pipeline (run this first)
- `dashboards_hipotesis/dashboard_hip_1.py` — Streamlit dashboard
- `dashboards_hipotesis/data_processing_copy.py` — Dashboard data pipeline
- `data/NPS-Mexico-2026-v1.xlsx` — Anonymous survey dataset

---

## ⚙️ Tech Stack

Python · Pandas · NumPy · Scikit-learn · Imbalanced-learn · Plotly · Streamlit · Statsmodels

---

## ▶️ How to Run

```bash
pip install pandas numpy scikit-learn imbalanced-learn plotly streamlit statsmodels openpyxl
```

> **Note:** Download the entire `NPS-PROJECT` folder and open it in your editor of choice.

1. **Run `data_processing.py` first** — this cleans and standardizes the raw data.
2. Open `santander_case.ipynb` in Jupyter Notebook or VS Code and run all cells.
3. To launch the dashboard:

```bash
streamlit run dashboards_hipotesis/dashboard_hip_1.py
```
