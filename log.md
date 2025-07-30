# Airbnb Data Analysis

### Which property features best explain and predict nightly price for London Airbnb listings?

## Fetching Data

- Downloading listings.csv for London from https://insideairbnb.com/get-the-data/
- Initialised GitHub repo with .gitignore and LICENSE

## Cleaning Data

- Printed out shape of dataframe
- Calculated percentage of data missing in each column
- Removed columns "license" and "neighbourhood_group" as they had no data
- Filtered out entries with no price
- Replaced all NaN in "reviews_per_month" column with 0
  - They had no revies
