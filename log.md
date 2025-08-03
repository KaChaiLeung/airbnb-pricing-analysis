### Airbnb Data Analysis

**Which property features best explain and predict nightly price for London Airbnb listings?**

---

## Fetching Data

- Downloaded **listings.csv** for London from [Inside Airbnb](https://insideairbnb.com/get-the-data/)
- Initialized GitHub repo with `.gitignore` and `LICENSE`

---

## Cleaning Data

- Inspected DataFrame shape and missing-value percentages
- **Removed** columns with no data: `license`, `neighbourhood_group`
- **Dropped** listings with missing `price`
- **Filled** NaNs in `reviews_per_month` with 0
- **Converted** `last_review` → `datetime`
- **Added**
  - `has_review` (bool) = whether a listing has any reviews
  - `days_since_review` (int) = days since last review
- **Filled** NaNs in `host_name` with `"Unknown"`
- **Saved** cleaned data to `data/listings_clean.csv`

---

## Exploratory Data Analysis & Visualisation

- **Price statistics**: count, mean, median, min, max, std, Q1, Q3, IQR
- **Histogram** of price (log scale to handle skew)
- **Outlier analysis** using 1.5×IQR — 6.69% of listings above upper bound, 0% below
- **Box plots** of price by room type and by top-8 boroughs
- **Correlation matrix** among numeric features (little linear correlation)

---

## Feature Engineering

- **Extracted** `bedroom_count` from `name` via regex
- **Log-transformed** skewed numerics with `log1p`:
  - `price` → `log_price`
  - `reviews_per_month` → `log_reviews_per_month`
  - `number_of_reviews_ltm` → `log_reviews_ltm`
  - `days_since_review` → `log_days_since_review`
  - `calculated_host_listings_count` → `log_host_listings`
- **Renamed** `neighbourhood` → `borough` and grouped all but the top 8 into `"Other"`
- **One-hot encoded** `borough_grouped` and `room_type` (with `drop_first=True`)
- **Converted** all Boolean columns to 0/1 integers
- **Dropped** leftover identifiers and raw columns, leaving 23–27 numeric predictors + dummies

---

## Train/Test Split

- **Target:** `y = data["log_price"]`
- **Features:** `X = data.drop(columns="log_price")`
- **Split:** 80% train / 20% test, `random_state=42`

---

## Model Building & Evaluation

### 1. Ridge Regression

- **Parameters:** `alpha=1.0`, `random_state=42`
- **Test performance:**
  - **RMSE (log-price):** 0.559 → ~74.9% raw-price error
  - **R²:** 0.522
- **Top 10 coefficients** (effect on log-price):
  1. `room_Shared room` = −1.525
  2. `room_Private room` = −0.930
  3. `has_review` = −0.552
  4. `boro_Other` = −0.351
  5. `room_Hotel room` = −0.344
  6. `boro_Hackney` = −0.250
  7. `boro_Westminster` = +0.228
  8. `latitude` = +0.218
  9. `boro_Tower Hamlets` = −0.213
  10. `boro_Kensington and Chelsea` = +0.210

### 2. RidgeCV

- **Grid:** α ∈ [0.001, 0.01, 0.1, 1, 10, 100], 5-fold CV on RMSE
- **Best α:** 0.1
- **Performance:** same as Ridge baseline (RMSE 0.559, R² 0.522)

### 3. Random Forest Regressor

- **Baseline** (`n_estimators=200`, `max_depth=None`, `min_samples_leaf=5`)

  - **RMSE:** 0.476 (≈61.1% error)
  - **R²:** 0.653
  - **Top 10 importances:**
    1. `room_Private room` = 0.440
    2. `longitude` = 0.101
    3. `latitude` = 0.096
    4. `bedroom_count` = 0.060
    5. `availability_365` = 0.057
    6. `log_host_listings` = 0.048
    7. `boro_Westminster` = 0.037
    8. `log_reviews_per_month` = 0.034
    9. `log_days_since_review` = 0.031
    10. `boro_Kensington and Chelsea` = 0.028

- **Tuned** via `RandomizedSearchCV`
  - **Best params:** `n_estimators=143`, `min_samples_leaf=4`, `max_features=0.8`, `max_depth=40`
  - **RMSE:** 0.473 (≈60.6% error)
  - **R²:** 0.657

### 4. Gradient Boosting Regressor

- **Baseline** (`HistGradientBoostingRegressor` default)

  - **RMSE:** 0.476 (≈61.1% error)
  - **R²:** 0.653

- **Tuned** via `RandomizedSearchCV`
  - **RMSE:** 0.471 (≈60.1% error)
  - **R²:** 0.661

### 5. Ensembles

- **Simple average (RF + GB):**
  - **RMSE:** 0.466 (≈59.3% error)
  - **R²:** 0.668
- **VotingRegressor:**
  - **RMSE:** 0.466
  - **R²:** 0.668
- **StackingRegressor** (meta-learner = Ridge):
  - **RMSE:** 0.465 (≈59.2% error)
  - **R²:** 0.669

---

## Cross-Validation

- **10-Fold CV** on final StackingRegressor:
  - **Average RMSE:** 0.481 ± 0.013
  - **Average R²:** 0.639 ± 0.015
