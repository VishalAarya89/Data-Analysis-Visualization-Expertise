# 🏠 House Price Analysis — Report

---

## 1. Executive Summary
This report analyzes a dataset of **300 residential properties**
to identify the key factors driving house prices, compare value across
locations and property types, and provide actionable recommendations for
buyers, sellers, and investors.

The average property price in this dataset is **₹24,883,658**,
with **Area** emerging as the strongest price driver
(correlation = 0.80).
---
## 2. Dataset Overview
| Property | Value |
|---|---|
| Total Records | 300 |
| Features | Area, Bedrooms, Bathrooms, Age, Location, Property_Type, Price |
| Locations | Rural, Suburb, City Center |
| Property Types | House, Villa, Apartment |
| Price Range | ₹3,695,000 – ₹58,700,000 |
| Area Range | 520 – 4,999 sq.ft |
---
## 3. Data Cleaning Summary
- Checked for and removed duplicate records
- Verified no missing values across all columns
- Validated all Price and Area values are positive
- Standardized text fields (Location, Property_Type)
- Engineered new feature: **Price_per_sqft** for value comparison
---
## 4. Statistical Summary
|                |           Mean |        Median |          Mode |        Std Dev |      Variance |          Min |          Max |
|:---------------|---------------:|--------------:|--------------:|---------------:|--------------:|-------------:|-------------:|
| Area           | 2759.7         | 2738          |  623          | 1297.68        |   1.68398e+06 |  520         |  4999        |
| Bedrooms       |    3.03        |    3          |    4          |    1.47        |   2.15        |    1         |     5        |
| Bathrooms      |    2.03        |    2          |    2          |    0.79        |   0.63        |    1         |     3        |
| Age            |   25           |   25.5        |   34          |   14.33        | 205.42        |    0         |    49        |
| Price          |    2.48837e+07 |    2.2365e+07 |    1.7945e+07 |    1.26653e+07 |   1.60409e+14 |    3.695e+06 |     5.87e+07 |
| Price_per_sqft | 9542.84        | 9282.17       | 4555.56       | 3186.33        |   1.01527e+07 | 4555.56      | 21739.6      |
---
## 5. Correlation Analysis
|           |   Area |   Bedrooms |   Bathrooms |    Age |   Price |
|:----------|-------:|-----------:|------------:|-------:|--------:|
| Area      |  1     |     -0.004 |      -0.026 | -0.083 |   0.796 |
| Bedrooms  | -0.004 |      1     |      -0.044 | -0.032 |   0.202 |
| Bathrooms | -0.026 |     -0.044 |       1     |  0.118 |  -0.03  |
| Age       | -0.083 |     -0.032 |       0.118 |  1     |  -0.131 |
| Price     |  0.796 |      0.202 |      -0.03  | -0.131 |   1     |
**Correlation with Price (ranked):**
|           |   Price |
|:----------|--------:|
| Area      |   0.796 |
| Bedrooms  |   0.202 |
| Bathrooms |  -0.03  |
| Age       |  -0.131 |
---
## 6. Location-Based Analysis
| Location    |   Avg_Price |   Median_Price |   Avg_Area |   Avg_Price_per_sqft |   Property_Count |
|:------------|------------:|---------------:|-----------:|---------------------:|-----------------:|
| City Center | 3.31498e+07 |    3.497e+07   |    2777.87 |             12525.9  |               97 |
| Suburb      | 2.51081e+07 |    2.403e+07   |    2764.89 |              9681.16 |              105 |
| Rural       | 1.64614e+07 |    1.60525e+07 |    2736.16 |              6442.03 |               98 |
---
## 7. Property Type Analysis
| Property_Type   |   Avg_Price |   Median_Price |   Avg_Area |   Property_Count |
|:----------------|------------:|---------------:|-----------:|-----------------:|
| Apartment       | 2.71242e+07 |    2.56425e+07 |    3045.6  |               91 |
| Villa           | 2.49899e+07 |    2.181e+07   |    2720.56 |              102 |
| House           | 2.28769e+07 |    2.0575e+07  |    2553.86 |              107 |
---
## 8. Bedroom Impact Analysis
|   Bedrooms |   Avg_Price |   Avg_Area |   Count |
|-----------:|------------:|-----------:|--------:|
|          1 | 2.25146e+07 |    2845.8  |      70 |
|          2 | 2.31986e+07 |    2782.24 |      46 |
|          3 | 2.09123e+07 |    2555.35 |      49 |
|          4 | 2.70482e+07 |    2694.96 |      74 |
|          5 | 2.94373e+07 |    2886.59 |      61 |
---
## 9. Key Findings
1. **Area** has the strongest positive relationship
   with price (correlation = 0.80), making it
   the single most important factor in price determination.
2. **Age** shows the weakest relationship with price
   (correlation = -0.13), suggesting it plays a
   minor role compared to other features.
3. **City Center** is the most valuable location with
   an average price of ₹33,149,794, while
   **Rural** has the lowest average price.
4. **Apartment** properties command the highest average
   price at ₹27,124,203.
5. The average price per square foot across the dataset is
   ₹9,542.84, with **Rural**
   offering the best value per square foot.
---
## 10. Business Insights
- **Key Price Drivers:** Area is by far the dominant
  driver of price in this dataset, while features like Bathrooms and Age show
  little to no positive relationship with price.
- **Most Valuable Features:** Larger properties in premium locations
  (City Center) command significantly higher prices per square foot.
- **High-Demand Areas:** City Center properties have the highest average
  price, indicating strong demand and limited supply in central locations.
---
## 11. Recommendations
### For Investors
- Prioritize properties in **City Center** for
  long-term appreciation, but evaluate **Rural**
  for better entry price per square foot.
- Larger area properties show the most consistent price scaling — a safer
  bet for capital preservation.

### For Sellers (Pricing Strategy)
- Price properties based primarily on **Area**, the
  strongest value driver identified in this analysis — not on bedroom or
  bathroom count alone.
- Older properties should be priced competitively to offset the age-related
  depreciation trend observed in the data.
### For Buyers
- Compare **Price_per_sqft** across locations rather than absolute price
  alone — it provides a fairer basis for comparing value.
---
*Report generated automatically by analysis.py — Personal Finance & Data
Analytics Toolkit by Vishal Arya, Servana Tech.*
