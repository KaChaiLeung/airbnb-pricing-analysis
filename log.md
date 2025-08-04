### Project Overview: London Airbnb Price Analysis & Prediction

**Objective:**  
Identify which listing features best explain and predict nightly prices for London Airbnb properties, and build a robust, interpretable regression pipeline.

---

#### 1. Data Ingestion & Initial Overview

- **Loaded** raw `listings.csv` from Inside Airbnb
- **Captured** dataset shape (rows × columns) and dtypes

---

#### 2. Data Cleaning & Transformation

- **Assessed** missingness per column; removed empty fields (`license`, `neighbourhood_group`)
- **Filtered** out listings missing a `price`
- **Imputed** missing `reviews_per_month` as 0
- **Converted** `last_review` to datetime; created:
  - `has_review` flag
  - `days_since_review` (days since last review)
- **Filled** missing `host_name` with `"Unknown"`
- **Saved** cleaned data to `data/listings_clean.csv`

---

#### 3. Exploratory Data Analysis & Visualization

- **Price summary** (count, mean, median, min/max, std, Q1/Q3, IQR)
- **Histograms**: price on linear vs. log scales; identified 6.7% outliers above 1.5×IQR
- **Box plots**: price by `room_type` and top-8 boroughs
- **Correlation heatmap** of numeric features (no strong linear trends)
- **Scatter + regression**: price vs. reviews/month, days_since_review, availability (log-scaled x)
- **Choropleth map** of median nightly price by borough

---

#### 4. Feature Engineering

- **Extracted** `bedroom_count` from listing `name` via regex
- **Log-transformed** skewed variables (`price`, `reviews_per_month`, `number_of_reviews_ltm`, `days_since_review`, `calculated_host_listings_count`)
- **Grouped** boroughs outside the top 8 into “Other”
- **One-hot encoded** `borough_grouped` & `room_type` (drop_first=True)
- **Converted** Boolean flags to integers
- **Dropped** raw identifiers & un-logged columns
- **Prepared** final modeling dataset (`ml_ready_listings.csv`)

---

#### 5. Modeling & Evaluation (No Geospatial)

- **Train/Test Split:** 80/20, seed=42
- **Baseline Models:**
  - Ridge Regression (α=1): RMSE=0.559 (~74.9% error), R²=0.522
  - Random Forest (200 trees): RMSE=0.476 (~60.6% error), R²=0.653
- **Hyperparameter Tuning:**
  - RidgeCV → α=0.1 (no change)
  - RF CV → RMSE=0.473, R²=0.657
  - HistGBR CV → RMSE=0.471, R²=0.661
- **Ensembles:**
  - Simple RF+GB avg → RMSE=0.466, R²=0.668
  - VotingRegressor → same
  - StackingRegressor (meta=Ridge) → RMSE=0.465, R²=0.669
- **10-Fold CV** on final stack → RMSE=0.481 ± 0.013, R²=0.639 ± 0.015

---

#### 6. Geospatial Feature & Extended Modeling

- **Fetched** Tube station data via TfL API
- **Computed** nearest-station distance (`dist_to_tube_km`) using a Haversine BallTree
- **Integrated** `dist_to_tube_km` into features; re-ran model pipelines

---

#### 7. Final Ensembles & Interpretability

- **Added** XGBoost to stacking with both Ridge and XGBoost meta-learners
- **Built** final stacked model (`passthrough=True`) for further gains
- **Explained** via permutation importance and SHAP (global feature impacts, base-model names removed)

---

### Skills & Tools Demonstrated

- **Libraries**: Pandas, NumPy, Matplotlib/Seaborn, GeoPandas, Folium, Scikit-Learn, XGBoost, SHAP
- **Techniques**: outlier detection, log transforms, regex parsing, geospatial analytics, hyperparameter search, k-fold CV, ensembling, permutation importance, SHAP explanations
- **Outcome**: an end-to-end, interpretable regression pipeline predicting log-price with ~0.46 RMSE (log-scale) and ~0.67 R².
