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
  - Converted "last_review" column to datatime
- Added column "has_review" (bool) to show which entries have reviews
- Added "days_since_review" (int) to show how many days since the last review
