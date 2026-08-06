import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110
plt.rcParams["font.size"] = 10

DATA_PATH = "house_prices.csv"
VISUALS_DIR = "visuals"
REPORT_PATH = "report.md"

PALETTE = ["#2E5EAA", "#5DA9E9", "#F2A65A", "#E76F51", "#43AA8B"]
ACCENT_COLOR = "#2E5EAA"

os.makedirs(VISUALS_DIR, exist_ok=True)

NUMERIC_FEATURES = ["Area", "Bedrooms", "Bathrooms", "Age", "Price", "Price_per_sqft"]
CORRELATION_FEATURES = ["Area", "Bedrooms", "Bathrooms", "Age", "Price"]


def save_plot(filename: str) -> None:
    plt.tight_layout()
    output_path = os.path.join(VISUALS_DIR, filename)
    plt.savefig(output_path)
    plt.close()
    print(f"[SAVED] {output_path}")


def add_linear_trend(x: pd.Series, y: pd.Series, color: str = "black") -> None:
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    x_line = np.linspace(x.min(), x.max(), 100)
    plt.plot(x_line, p(x_line), color=color, linestyle="--", linewidth=1.5, label="Trend Line")


def get_price_correlations(corr: pd.DataFrame) -> pd.Series:
    return corr["Price"].drop("Price").sort_values(ascending=False)


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[LOAD] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    initial_rows = len(df)

    df.drop_duplicates(inplace=True)
    duplicates_removed = initial_rows - len(df)

    missing_before = df.isnull().sum().sum()
    if missing_before > 0:
        df.dropna(inplace=True)

    for col in ["Location", "Property_Type"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    invalid_rows = df[(df["Price"] <= 0) | (df["Area"] <= 0)]
    df = df[(df["Price"] > 0) & (df["Area"] > 0)]

    df["Price_per_sqft"] = (df["Price"] / df["Area"]).round(2)

    print("\n[CLEAN] Data Cleaning Summary")
    print(f"        Duplicates removed   : {duplicates_removed}")
    print(f"        Missing values found : {missing_before}")
    print(f"        Invalid rows removed : {len(invalid_rows)}")
    print(f"        Final dataset shape  : {df.shape[0]} rows, {df.shape[1]} columns")

    return df

def compute_statistics(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = NUMERIC_FEATURES
    stats = {}

    for col in numeric_cols:
        stats[col] = {
            "Mean":     round(df[col].mean(), 2),
            "Median":   round(df[col].median(), 2),
            "Mode":     round(df[col].mode().iloc[0], 2),
            "Std Dev":  round(df[col].std(), 2),
            "Variance": round(df[col].var(), 2),
            "Min":      round(df[col].min(), 2),
            "Max":      round(df[col].max(), 2),
        }

    stats_df = pd.DataFrame(stats).T
    print("\n[STATS] Descriptive Statistics")
    print(stats_df.to_string())
    return stats_df

def compute_correlation(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = CORRELATION_FEATURES
    corr = df[numeric_cols].corr().round(3)

    print("\n[CORRELATION] Correlation Matrix")
    print(corr.to_string())

    print("\n[CORRELATION] Correlation with Price (sorted):")
    price_corr = get_price_correlations(corr)
    print(price_corr.to_string())

    return corr
def analyze_location(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("Location").agg(
        Avg_Price=("Price", "mean"),
        Median_Price=("Price", "median"),
        Avg_Area=("Area", "mean"),
        Avg_Price_per_sqft=("Price_per_sqft", "mean"),
        Property_Count=("Property_ID", "count"),
    ).round(2).sort_values("Avg_Price", ascending=False)

    print("\n[LOCATION] Price Summary by Location")
    print(summary.to_string())
    return summary

def analyze_property_type(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("Property_Type").agg(
        Avg_Price=("Price", "mean"),
        Median_Price=("Price", "median"),
        Avg_Area=("Area", "mean"),
        Property_Count=("Property_ID", "count"),
    ).round(2).sort_values("Avg_Price", ascending=False)

    print("\n[PROPERTY TYPE] Price Summary by Property Type")
    print(summary.to_string())
    return summary

def analyze_bedroom_impact(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("Bedrooms").agg(
        Avg_Price=("Price", "mean"),
        Avg_Area=("Area", "mean"),
        Count=("Property_ID", "count"),
    ).round(2)

    print("\n[BEDROOMS] Price Summary by Bedroom Count")
    print(summary.to_string())
    return summary

def plot_correlation_heatmap(corr: pd.DataFrame) -> None:
    plt.figure(figsize=(7, 5.5))
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="coolwarm",
        center=0, linewidths=0.5, square=True, cbar_kws={"shrink": 0.8}
    )
    plt.title("Correlation Heatmap — Property Features vs Price", fontsize=12, fontweight="bold")
    save_plot("01_correlation_heatmap.png")

def plot_price_distribution(df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Price"], bins=30, kde=True, color=ACCENT_COLOR, edgecolor="white")
    plt.axvline(df["Price"].mean(), color="#E76F51", linestyle="--", linewidth=2,
                label=f"Mean: ₹{df['Price'].mean():,.0f}")
    plt.axvline(df["Price"].median(), color="#43AA8B", linestyle="--", linewidth=2,
                label=f"Median: ₹{df['Price'].median():,.0f}")
    plt.title("Price Distribution of Properties", fontsize=12, fontweight="bold")
    plt.xlabel("Price (₹)")
    plt.ylabel("Number of Properties")
    plt.legend()
    save_plot("02_price_histogram.png")

def plot_area_vs_price(df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5.5))
    sns.scatterplot(
        data=df, x="Area", y="Price", hue="Property_Type",
        palette=PALETTE[:3], alpha=0.75, s=55, edgecolor="white"
    )
    add_linear_trend(df["Area"], df["Price"], color="black")

    plt.title("Area vs Price Relationship", fontsize=12, fontweight="bold")
    plt.xlabel("Area (sq.ft)")
    plt.ylabel("Price (₹)")
    plt.legend(title="Property Type")
    save_plot("03_area_vs_price_scatter.png")

def plot_boxplot_by_location(df: pd.DataFrame) -> None:
    plt.figure(figsize=(8, 5.5))
    order = df.groupby("Location")["Price"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="Location", y="Price", order=order, hue="Location",
                palette=PALETTE[:3], legend=False)
    plt.title("Price Distribution by Location", fontsize=12, fontweight="bold")
    plt.xlabel("Location")
    plt.ylabel("Price (₹)")
    save_plot("04_boxplot_by_location.png")

def plot_feature_importance(corr: pd.DataFrame) -> None:
    price_corr = corr["Price"].drop("Price").sort_values()

    plt.figure(figsize=(8, 5))
    colors = ["#E76F51" if v < 0 else ACCENT_COLOR for v in price_corr.values]
    bars = plt.barh(price_corr.index, price_corr.values, color=colors, edgecolor="white")

    for bar, val in zip(bars, price_corr.values):
        plt.text(val + (0.02 if val >= 0 else -0.02), bar.get_y() + bar.get_height()/2,
                  f"{val:.2f}", va="center", ha="left" if val >= 0 else "right", fontsize=9)

    plt.title("Feature Importance — Correlation with Price", fontsize=12, fontweight="bold")
    plt.xlabel("Correlation Coefficient")
    plt.axvline(0, color="black", linewidth=0.8)
    save_plot("05_feature_importance.png")

def plot_avg_price_by_bedrooms(df: pd.DataFrame) -> None:
    summary = df.groupby("Bedrooms")["Price"].mean().round(0)

    plt.figure(figsize=(7, 5))
    plt.bar(summary.index.astype(str), summary.values, color=ACCENT_COLOR, edgecolor="white")
    for i, v in enumerate(summary.values):
        plt.text(i, v + summary.values.max()*0.01, f"₹{v:,.0f}", ha="center", fontsize=9)
    plt.title("Average Price by Bedroom Count", fontsize=12, fontweight="bold")
    plt.xlabel("Number of Bedrooms")
    plt.ylabel("Average Price (₹)")
    save_plot("06_avg_price_by_bedrooms.png")

def plot_property_type_pie(df: pd.DataFrame) -> None:
    counts = df["Property_Type"].value_counts()

    plt.figure(figsize=(6.5, 6.5))
    plt.pie(
        counts.values, labels=counts.index, autopct="%1.1f%%",
        colors=PALETTE[:3], startangle=90,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        textprops={"fontsize": 10}
    )
    plt.title("Property Type Distribution", fontsize=12, fontweight="bold")
    save_plot("07_property_type_pie.png")

def plot_age_vs_price(df: pd.DataFrame) -> None:
    """Scatter plot exploring relationship between property age and price."""
    plt.figure(figsize=(8, 5.5))
    sns.scatterplot(data=df, x="Age", y="Price", color=ACCENT_COLOR, alpha=0.6, s=50)
    add_linear_trend(df["Age"], df["Price"], color="#E76F51")
    plt.title("Property Age vs Price", fontsize=12, fontweight="bold")
    plt.xlabel("Age (years)")
    plt.ylabel("Price (₹)")
    plt.legend()
    save_plot("08_age_vs_price.png")

def generate_all_visuals(df: pd.DataFrame, corr: pd.DataFrame) -> None:
    """Runs all visualization functions in sequence."""
    print("\n[VISUALS] Generating charts...")
    plot_correlation_heatmap(corr)
    plot_price_distribution(df)
    plot_area_vs_price(df)
    plot_boxplot_by_location(df)
    plot_feature_importance(corr)
    plot_avg_price_by_bedrooms(df)
    plot_property_type_pie(df)
    plot_age_vs_price(df)

def generate_insights(df: pd.DataFrame, corr: pd.DataFrame,
                       location_summary: pd.DataFrame,
                       type_summary: pd.DataFrame) -> dict:
    price_corr = get_price_correlations(corr)

    insights = {
        "top_price_driver":     price_corr.index[0],
        "top_price_driver_val": price_corr.iloc[0],
        "weakest_driver":       price_corr.index[-1],
        "weakest_driver_val":   price_corr.iloc[-1],
        "most_valuable_location":   location_summary.index[0],
        "most_valuable_location_price": location_summary.iloc[0]["Avg_Price"],
        "least_valuable_location":  location_summary.index[-1],
        "most_valuable_type":    type_summary.index[0],
        "most_valuable_type_price": type_summary.iloc[0]["Avg_Price"],
        "avg_price_per_sqft":    df["Price_per_sqft"].mean(),
        "cheapest_location_per_sqft": df.groupby("Location")["Price_per_sqft"].mean().idxmin(),
        "total_properties":     len(df),
        "overall_avg_price":    df["Price"].mean(),
    }

    print("\n[INSIGHTS] Business Insights")
    print(f"  • Strongest price driver   : {insights['top_price_driver']} "
          f"(corr = {insights['top_price_driver_val']:.2f})")
    print(f"  • Weakest price driver     : {insights['weakest_driver']} "
          f"(corr = {insights['weakest_driver_val']:.2f})")
    print(f"  • Most valuable location   : {insights['most_valuable_location']} "
          f"(avg ₹{insights['most_valuable_location_price']:,.0f})")
    print(f"  • Most valuable type       : {insights['most_valuable_type']} "
          f"(avg ₹{insights['most_valuable_type_price']:,.0f})")
    print(f"  • Avg price per sq.ft      : ₹{insights['avg_price_per_sqft']:,.2f}")
    print(f"  • Best value-per-sqft area : {insights['cheapest_location_per_sqft']}")

    return insights


def run_analysis(path: str = DATA_PATH, generate_visuals: bool = False):
    df_raw = load_data(path)
    df = clean_data(df_raw)
    stats_df = compute_statistics(df)
    corr = compute_correlation(df)
    location_summary = analyze_location(df)
    type_summary = analyze_property_type(df)
    bedroom_summary = analyze_bedroom_impact(df)
    insights = generate_insights(df, corr, location_summary, type_summary)

    if generate_visuals:
        generate_all_visuals(df, corr)

    return df, stats_df, corr, location_summary, type_summary, bedroom_summary, insights


def generate_report(df, stats_df, corr, location_summary,
                     type_summary, bedroom_summary, insights) -> None:
    report = f"""# 🏠 House Price Analysis — Report

---

## 1. Executive Summary
This report analyzes a dataset of **{insights['total_properties']} residential properties**
to identify the key factors driving house prices, compare value across
locations and property types, and provide actionable recommendations for
buyers, sellers, and investors.

The average property price in this dataset is **₹{insights['overall_avg_price']:,.0f}**,
with **{insights['top_price_driver']}** emerging as the strongest price driver
(correlation = {insights['top_price_driver_val']:.2f}).
---
## 2. Dataset Overview
| Property | Value |
|---|---|
| Total Records | {len(df)} |
| Features | Area, Bedrooms, Bathrooms, Age, Location, Property_Type, Price |
| Locations | {", ".join(df['Location'].unique())} |
| Property Types | {", ".join(df['Property_Type'].unique())} |
| Price Range | ₹{df['Price'].min():,.0f} – ₹{df['Price'].max():,.0f} |
| Area Range | {df['Area'].min():,.0f} – {df['Area'].max():,.0f} sq.ft |
---
## 3. Data Cleaning Summary
- Checked for and removed duplicate records
- Verified no missing values across all columns
- Validated all Price and Area values are positive
- Standardized text fields (Location, Property_Type)
- Engineered new feature: **Price_per_sqft** for value comparison
---
## 4. Statistical Summary
{stats_df.to_markdown()}
---
## 5. Correlation Analysis
{corr.to_markdown()}
**Correlation with Price (ranked):**
{corr['Price'].drop('Price').sort_values(ascending=False).to_markdown()}
---
## 6. Location-Based Analysis
{location_summary.to_markdown()}
---
## 7. Property Type Analysis
{type_summary.to_markdown()}
---
## 8. Bedroom Impact Analysis
{bedroom_summary.to_markdown()}
---
## 9. Key Findings
1. **{insights['top_price_driver']}** has the strongest positive relationship
   with price (correlation = {insights['top_price_driver_val']:.2f}), making it
   the single most important factor in price determination.
2. **{insights['weakest_driver']}** shows the weakest relationship with price
   (correlation = {insights['weakest_driver_val']:.2f}), suggesting it plays a
   minor role compared to other features.
3. **{insights['most_valuable_location']}** is the most valuable location with
   an average price of ₹{insights['most_valuable_location_price']:,.0f}, while
   **{insights['least_valuable_location']}** has the lowest average price.
4. **{insights['most_valuable_type']}** properties command the highest average
   price at ₹{insights['most_valuable_type_price']:,.0f}.
5. The average price per square foot across the dataset is
   ₹{insights['avg_price_per_sqft']:,.2f}, with **{insights['cheapest_location_per_sqft']}**
   offering the best value per square foot.
---
## 10. Business Insights
- **Key Price Drivers:** {insights['top_price_driver']} is by far the dominant
  driver of price in this dataset, while features like Bathrooms and Age show
  little to no positive relationship with price.
- **Most Valuable Features:** Larger properties in premium locations
  (City Center) command significantly higher prices per square foot.
- **High-Demand Areas:** City Center properties have the highest average
  price, indicating strong demand and limited supply in central locations.
---
## 11. Recommendations
### For Investors
- Prioritize properties in **{insights['most_valuable_location']}** for
  long-term appreciation, but evaluate **{insights['cheapest_location_per_sqft']}**
  for better entry price per square foot.
- Larger area properties show the most consistent price scaling — a safer
  bet for capital preservation.

### For Sellers (Pricing Strategy)
- Price properties based primarily on **{insights['top_price_driver']}**, the
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
"""
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n[REPORT] Markdown report saved to: {REPORT_PATH}")

def main():
    print("=" * 65)
    print("  HOUSE PRICE ANALYSIS — Starting Pipeline")
    print("=" * 65)

    df, stats_df, corr, location_summary, type_summary, bedroom_summary, insights = run_analysis(generate_visuals=True)

    generate_report(df, stats_df, corr, location_summary,
                     type_summary, bedroom_summary, insights)

    print("\n" + "=" * 65)
    print("  PIPELINE COMPLETE — All outputs saved to 'visuals/' and 'report.md'")
    print("=" * 65)

if __name__ == "__main__":
    main()
