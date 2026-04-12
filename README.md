# 📊 FitLater

## 🚀 Version 0.3.0

- ✅ Complete multi-layer pipeline:
  - Descriptive → Diagnostics → Advisory → Profile
- ✅ 100+ unit and integration tests
- ✅ Robust handling of edge cases (NaN, boolean, empty datasets)
- ✅ Stable CLI interface
- ✅ Deterministic and consistent outputs


## What is FitLater?

FitLater is a CLI-based data analysis tool that helps users understand their dataset before building machine learning models.

It provides structured insights and actionable recommendations through a multi-layer pipeline:
- Descriptive → Diagnostics → Advisory → Profile

The goal is not just to analyze data, but to guide better decisions during preprocessing and model development.

---

## ✨ Features

- 📊 Comprehensive data overview
- ⚠️ Automated issue detection (missing, outliers, skew, correlation)
- 💡 Actionable recommendations for preprocessing
- 🧠 Intelligent profiling of columns
- 🧪 100+ tests ensuring stability and correctness
- 💻 CLI-based interactive workflow

---

## 🏗️ Architecture

FitLater follows a layered design:

### 1. Descriptive Layer
Provides fundamental dataset insights:
- Shape, data types, distributions
- Missing values, duplicates

### 2. Diagnostics Layer
Identifies potential issues:
- Missing data severity
- Outliers
- Skewed distributions
- Feature correlations

### 3. Advisory Layer
Transforms issues into actionable recommendations:
- Data cleaning strategies
- Feature transformations
- Model-impact insights

### 4. Profile Layer
Builds column-level metadata:
- Skew, missing %, outliers
- Data type understanding

> This layered approach ensures clarity, consistency, and scalability.

---

## 🧪 Testing

FitLater includes 100+ unit and integration tests covering:

- Edge cases (NaN, boolean, empty data)
- Layer-wise validation
- Full pipeline consistency
- Deterministic outputs

Run tests:

```bash
pytest
```

---

## Quick start

**Requirements:** Python 3.10 or newer.

```bash
git clone https://github.com/jitesh2511/FitLater
cd FitLater
python -m venv .venv
```

Activate the virtual environment:

- **Windows:** `.venv\Scripts\activate`
- **macOS / Linux:** `source .venv/bin/activate`

Install dependencies and run the interactive CLI from the repository root:

```bash
pip install -r requirements.txt
python -m fitlater
```

Install as a package (editable) to get the `fitlater` command and run tests:

```bash
pip install -e ".[dev]"
pytest
fitlater
```

After loading a dataset:

- `overview` → Dataset summary  
- `correlation` → Correlation analysis  
- `outlier` → Outlier detection  
- `missing_diags` → Missing value diagnostics  
- `corr_diags` → Correlation diagnostics  
- `outlier_diags` → Outlier diagnostics  
- `dist_diags` → Distribution diagnostics  
- `diagnostics` → Full diagnostics report  
- `advisory_report` → Full advisory report [new in version 0.3.0]

Type `help` for commands. Use `exit` to quit.

---

## 🎯 Purpose

The goal of FitLater is simple:

> Help users **understand their data deeply before jumping into model building**

It ensures that important insights are not missed and that decisions are based on a clear understanding of the dataset.

---

## ⚠️ What FitLater is NOT

FitLater should not be confused with an AutoML tool.

It **does NOT**:
- Perform hyperparameter tuning  
- Suggest the best algorithm with least loss  
- Perform extensive cross-validations  

Instead, it focuses purely on:

> 📌 Exploratory Data Analysis (EDA)

---

## 🚀 Why Use FitLater?

- Gain clarity about your dataset  
- Avoid rushing into model building  
- Discover hidden patterns and insights  
- Make informed decisions for data preprocessing and modeling  

---

## 🧠 Philosophy

FitLater follows a simple philosophy:

> **“Understand first, model later.”**


---

## 🔮 Future Scope

- Web-based UI (Streamlit / React)
- Exportable reports (PDF/HTML)
- Integration with ML pipelines
- Advanced feature engineering suggestions


---

## 📌 Summary

FitLater is designed to act like a **thinking assistant for your data**, helping you slow down, analyze properly, and build better ML models with confidence.

---

## 📄 License

This project is licensed under a **proprietary license**.

All rights are reserved by the author.
You may not use, copy, modify, or distribute this software without explicit permission — see [LICENSE](LICENSE).

For licensing inquiries, please contact: jiteshkrishna6@gmail.com
