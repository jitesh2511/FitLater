# ⚠️ Core Architecture Refactor

This branch represents a **major redesign of FitLater’s internal architecture**, focused on building a scalable and modular foundation for future development.

---

## 🎯 Objective

The goal of this refactor is to transition FitLater from a feature-driven prototype to a **layered, system-oriented design**.

Key improvements include:

* Clear separation of responsibilities across layers
* Improved modularity for easier extension and maintenance
* Consistent internal contracts between components
* Stronger testing and reliability guarantees

---

## 🧱 Architecture Overview

The system is structured into three primary layers:

### 1. Descriptive Layer

Responsible for generating structured summaries of the dataset:

* Data types and schema inference
* Statistical summaries
* Basic distributions and profiles

**Status:** ✅ Stabilized and fully tested

---

### 2. Diagnostics Layer

Identifies data quality issues based on descriptive insights:

* Missing values
* Outliers
* Distribution anomalies
* Correlation issues
* Type inconsistencies
* Duplicates and imbalance

**Status:** ✅ Stabilized and fully tested

---

### 3. Advisory Layer

Generates actionable recommendations based on detected issues:

* Data cleaning strategies
* Transformation suggestions
* Feature handling decisions

**Status:** ⏳ Under alignment with refactored architecture

---

## 🚧 Current State

* This branch is **under active development**
* Internal APIs and structures are still evolving
* Backward compatibility is **not guaranteed**

---

## ⚠️ Usage Notice

This branch is intended for:

* Development and experimentation
* Reviewing architectural changes

It is **not recommended for production use**.

---

## 📦 Stable Versions

For a stable and usable version of FitLater, refer to:

* `main` branch
* `dev` branch

---

## 🧠 Why This Refactor Matters

This redesign enables FitLater to evolve from a simple EDA tool into a:

> **modular data intelligence system**
> where data understanding, issue detection, and decision-making are clearly separated and extensible.

---

## 🚀 What’s Next

* Finalize Advisory Layer alignment
* Integrate layers into a unified pipeline
* Connect backend system with custom UI (v0.4)

---
