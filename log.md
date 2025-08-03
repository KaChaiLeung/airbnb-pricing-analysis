# Airbnb Data Analysis

### Which property features best explain and predict nightly price for London Airbnb listings?

## Fetching Data

- Downloading listings.csv for London from https://insideairbnb.com/get-the-data/
- Initialised GitHub repo with .gitignore and LICENSE

## Cleaning Data

- Printed out shape of dataframe
- Calculated percentage of data missing in each column
- Cleaned data
  - Removed columns "license" and "neighbourhood_group" as they had no data
  - Removed any entries with no price data
  - Filled NaNs in "reviews_per_month" with 0 indicating no reviews
  - Converted "last_review" column to datetime
- Added column "has_review" (bool) to show which entries have reviews
- Added "days_since_review" (int) to show how many days since the last review
- Filled NaNs in "host_name" with "Unknown"
- Saved filtered data to "data/listings_clean.csv"

## Exploratory Data Analysis and Visualisations

- Calculated price statistics from listings_clean.csv
  - Count
  - Mean
  - Median
  - Min Price
  - Max Price
  - Standard Deviation
  - First Quartile
  - Third Quartile
  - Interquartile Range
- Plotted histogram of price vs. count
  - Set log_scale=True as price was heavily skewed to the lower end
- Identified and removed outliers
  - Found upper and lower bounds for outliers
    - 1.5 x IQR
  - Calculated percentage of outliers above/below bounds
  - Total percentage outliers = 6.69% (6.69% above and 0% below)
- Plotted new count vs. price with both linear scale and log scale
- Plotted box plots of room types vs. price
  - Entire home/apt - Highest median ~£180
  - Private room - contained many outliers above tail
  - Hotel room - Largest IQR
  - Shared room - lowest median ~£35 and IQR
- Found boroughs with the most amount of properties
  - Plotted box plots for each of the top 8 boroughs vs. price
- Calculated correlation matrix for relevant columns
  - price, reviews_per_month, days_since_review, availability_365, minimum_nights, number_of_reviews, calculated_host_listings_count
  - No obvious correlation between columns - Need to rely on calculated data

## Model Building and Evaluation

- Extracted number of rooms from "name" column
- Calculated log of certain columns
  - "price", "reviews_per_month", "number_of_reviews_ltm", "days_since_review", "calculated_host_listings_count"
- Grouped boroughs not in the top 8 as "Other"
- Dropped irrelevant columns
  - "Unnamed: 0", "id", "name", "host_id", "host_name", "price", "number_of_reviews", "last_review", "reviews_per_month", "calculated_host_listings_count", "number_of_reviews_ltm", "days_since_review", "neighbourhood"
- Filled NaNs from log step with 0
- Created dummy data for "neighbourhood" and "room_type"
- Changed all boolean values to integer
  - True = 1 and False = 0
- Initialised a random seed = 42
- Set target data as data["log_price"]
- Set domain data as all columns other than "log_price"
- Separated into train and test datasets
  - 20% of data is test data

### Ridge

- Positive coefficients indicate features that raise price relative to baseline
- Negative coefficients indicate features that lower price relative to baseline

- Baseline model:
  - alpha=1.0, random_state=42
  - RMSE: 0.559
  - R²: 0.522
  - Percentage Error: 74.85%
  - Top 10 features that influenced prediction:
    - "room_Shared room" = -1.525
    - "room_Private room" = -0.9296
    - "has_review" = -0.5517
    - "boro_Other" = -0.3506
    - "room_Hotel room" = -0.3440
    - "boro_Hackney" = -0.2499
    - "boro_Westminster" = 0.2276
    - "latitude" = 0.2179
    - "boro_Tower Hamlets" = -0.2128
    - "boro_Kensington and Chelsea" = 0.2104
