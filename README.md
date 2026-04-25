# FitLater

## Version 0.4.0

- Introduced frontend UI (HTML, CSS, JavaScript)
- Added backend API layer (FastAPI)
- Integrated UI with FitLater pipeline
- Improved diagnostics formatting and consistency
- UI currently under active development

---

## Philosophy

FitLater follows a simple principle:

> Understand first, model later.

---

## What is FitLater?

FitLater is a data analysis system designed to help users understand their dataset before building machine learning models.

It follows a structured pipeline:

- Descriptive → Diagnostics → Advisory → Profile

By enforcing a data-first approach, FitLater identifies issues early and provides actionable recommendations for preprocessing.

---

## Screenshots

### Dashboard (Empty State)
![Empty Dashboard](assets/screenshots/dash_empty.png)

### Dashboard (After Upload)
![Dashboard Results 1](assets/screenshots/dash_result_1.png)

![Dashboard Results 2](assets/screenshots/dash_result_2.png)

### Advisory Panel (High Priority)
![Advisory 1](assets/screenshots/advise_1.png)

### Advisory Panel (Mixed Priorities)
![Advisory 2](assets/screenshots/advise_2.png)

---

## What FitLater is NOT

FitLater is not an AutoML tool.

It does not:
- Perform hyperparameter tuning  
- Recommend models  
- Run training or evaluation pipelines  

It focuses strictly on exploratory data analysis (EDA) and data understanding.

---

## Features

- Comprehensive data overview
- Automated issue detection (missing values, outliers, skew, correlation)
- Actionable preprocessing recommendations
- Column-level profiling
- 360+ unit and integration tests
- CLI-based workflow
- Web-based UI (in development)

---

## Frontend (v0.4.0)

FitLater includes a custom-built UI for interactive data analysis.

- Upload datasets directly from the browser
- View diagnostics and advisory outputs visually
- Sidebar-based navigation
- Modular panel design (Upload, Advisory, Diagnostics)

Note: UI is under active development. Additional pages such as Analytics, Reports, and Settings are planned.

---

## API Layer (v0.4.0)

A FastAPI-based backend connects the frontend with the FitLater engine.

- Handles dataset upload and processing
- Executes diagnostics and advisory pipeline
- Returns structured JSON responses for UI rendering

Designed for future deployment and scalability.

---

## Architecture

FitLater follows a layered design:

### Descriptive Layer
Provides fundamental dataset insights:
- Shape, data types, distributions
- Missing values, duplicates

### Diagnostics Layer
Identifies potential issues:
- Missing data severity
- Outliers
- Skewed distributions
- Feature correlations

### Advisory Layer
Transforms detected issues into actionable recommendations:
- Data cleaning strategies
- Feature transformations
- Model-impact insights

### Profile Layer
Builds column-level metadata:
- Skew, missing percentage, outliers
- Data type understanding

This layered approach ensures clarity, consistency, and scalability.

---

## Testing

FitLater includes 360+ unit and integration tests covering:

- Edge cases (NaN, boolean, empty datasets)
- Layer-wise validation
- Full pipeline consistency
- Deterministic outputs

Run tests:

```bash
pytest
```

---

## Quick Start

**Requirements:** Python 3.10 or newer

### Setup

```bash
git clone https://github.com/jitesh2511/FitLater
cd FitLater
python -m venv .venv
```

Activate the virtual environment:

- Windows: `.venv\Scripts\activate`  
- macOS / Linux: `source .venv/bin/activate`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## CLI Usage

Run FitLater from terminal:

```bash
python -m fitlater
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
- `advisory_report` → Full advisory report  

Type `help` for commands. Use `exit` to quit.

---

## UI Usage (v0.4.0)

### Start Backend API

```bash
uvicorn backend.app:app --reload
```

### Open Frontend

Open `index.html` in your browser  
(or use Live Server in VS Code)

### Workflow

1. Upload a CSV file  
2. Backend processes the dataset  
3. View diagnostics and advisory results in the dashboard  

---

## Summary

FitLater is a structured system for exploratory data analysis that helps users make informed preprocessing decisions before model development.

---

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software, provided that the original copyright notice and license are included.

See the [LICENSE](LICENSE) file for details.

## Attribution

If you use FitLater in your work, consider citing or linking back to this repository:

https://github.com/jitesh2511/FitLater