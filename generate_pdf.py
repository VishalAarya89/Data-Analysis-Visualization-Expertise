import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from analysis import run_analysis, VISUALS_DIR

OUTPUT_PDF = "report.pdf"

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle", parent=styles["Title"], fontSize=22,
    textColor=colors.HexColor("#2E5EAA"), spaceAfter=4
)
subtitle_style = ParagraphStyle(
    "SubtitleStyle", parent=styles["Normal"], fontSize=10,
    textColor=colors.HexColor("#555555"), spaceAfter=14, alignment=TA_CENTER
)
h1_style = ParagraphStyle(
    "H1", parent=styles["Heading1"], fontSize=15,
    textColor=colors.HexColor("#2E5EAA"), spaceBefore=14, spaceAfter=8
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Heading2"], fontSize=12,
    textColor=colors.HexColor("#1B3A6B"), spaceBefore=10, spaceAfter=6
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"], fontSize=10, leading=15,
    alignment=TA_LEFT, spaceAfter=6
)
bullet_style = ParagraphStyle(
    "Bullet", parent=body_style, leftIndent=14, bulletIndent=4
)
caption_style = ParagraphStyle(
    "Caption", parent=styles["Normal"], fontSize=8.5,
    textColor=colors.HexColor("#777777"), alignment=TA_CENTER, spaceAfter=12
)

def df_to_table(df: pd.DataFrame, col_widths=None, font_size=8) -> Table:
    df_reset = df.reset_index()
    data = [list(df_reset.columns)] + df_reset.astype(str).values.tolist()

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E5EAA")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F5FA")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def build_pdf():
    print("[PDF] Loading data and running analysis pipeline...")
    df, stats_df, corr, location_summary, type_summary, bedroom_summary, insights = run_analysis(generate_visuals=True)

    doc = SimpleDocTemplate(
        OUTPUT_PDF, pagesize=A4,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm
    )

    story = []

    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("🏠 House Price Analysis", title_style))
    story.append(Paragraph("Data Analysis Portfolio — Project 2", subtitle_style))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#2E5EAA"), thickness=1.2))
    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph(
        "<b>Author:</b> Vishal Arya &nbsp;|&nbsp; Full Stack Developer &amp; Data Analyst &nbsp;|&nbsp; Servana Tech",
        body_style
    ))
    story.append(Paragraph(
        "<b>GitHub:</b> github.com/VishalAarya89", body_style
    ))
    story.append(Spacer(1, 1 * cm))

    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        f"This report analyzes a dataset of <b>{insights['total_properties']} residential "
        f"properties</b> to identify the key factors driving house prices, compare value "
        f"across locations and property types, and provide actionable recommendations for "
        f"buyers, sellers, and investors. The average property price is "
        f"<b>Rs. {insights['overall_avg_price']:,.0f}</b>, with <b>{insights['top_price_driver']}</b> "
        f"emerging as the strongest price driver (correlation = {insights['top_price_driver_val']:.2f}).",
        body_style
    ))

    story.append(Paragraph("2. Dataset Overview", h1_style))
    overview_data = [
        ["Metric", "Value"],
        ["Total Records", str(len(df))],
        ["Locations", ", ".join(df["Location"].unique())],
        ["Property Types", ", ".join(df["Property_Type"].unique())],
        ["Price Range", f"Rs. {df['Price'].min():,.0f} – Rs. {df['Price'].max():,.0f}"],
        ["Area Range", f"{df['Area'].min():,.0f} – {df['Area'].max():,.0f} sq.ft"],
    ]
    t = Table(overview_data, colWidths=[5 * cm, 10 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E5EAA")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F5FA")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    story.append(Paragraph("3. Data Cleaning Summary", h1_style))
    for line in [
        "Checked for and removed duplicate records",
        "Verified no missing values across all columns",
        "Validated all Price and Area values are positive",
        "Standardized text fields (Location, Property_Type)",
        "Engineered new feature: <b>Price_per_sqft</b> for value comparison",
    ]:
        story.append(Paragraph(f"•  {line}", bullet_style))

    story.append(PageBreak())

    story.append(Paragraph("4. Statistical Summary", h1_style))
    stats_display = stats_df.copy()
    for col in stats_display.columns:
        if col == "Variance":
            stats_display[col] = stats_display[col].apply(lambda x: f"{x:,.0f}" if x < 1_000_000 else f"{x:.3e}")
        else:
            stats_display[col] = stats_display[col].apply(lambda x: f"{x:,.2f}")
    story.append(df_to_table(stats_display, col_widths=[2.7*cm, 1.95*cm, 1.95*cm, 1.95*cm, 1.95*cm, 2.9*cm, 1.8*cm, 1.95*cm], font_size=7.5))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("5. Correlation Analysis", h1_style))
    story.append(Image(f"{VISUALS_DIR}/01_correlation_heatmap.png", width=12*cm, height=9.4*cm))
    story.append(Paragraph("Figure 1: Correlation heatmap of all numeric features against Price.", caption_style))

    story.append(Image(f"{VISUALS_DIR}/05_feature_importance.png", width=11*cm, height=6.9*cm))
    story.append(Paragraph("Figure 2: Feature importance ranked by correlation strength with Price.", caption_style))

    story.append(Paragraph("6. Price Distribution", h1_style))
    story.append(Image(f"{VISUALS_DIR}/02_price_histogram.png", width=12*cm, height=7.5*cm))
    story.append(Paragraph("Figure 3: Distribution of property prices with mean and median markers.", caption_style))

    story.append(PageBreak())

    story.append(Paragraph("7. Area vs Price Relationship", h1_style))
    story.append(Image(f"{VISUALS_DIR}/03_area_vs_price_scatter.png", width=13*cm, height=8.9*cm))
    story.append(Paragraph("Figure 4: Scatter plot showing the strong positive relationship between Area and Price.", caption_style))

    story.append(PageBreak())

    story.append(Paragraph("8. Location-Based Analysis", h1_style))
    loc_display = location_summary.copy()
    loc_display["Avg_Price"] = loc_display["Avg_Price"].apply(lambda x: f"Rs. {x:,.0f}")
    loc_display["Median_Price"] = loc_display["Median_Price"].apply(lambda x: f"Rs. {x:,.0f}")
    loc_display["Avg_Area"] = loc_display["Avg_Area"].apply(lambda x: f"{x:,.0f}")
    loc_display["Avg_Price_per_sqft"] = loc_display["Avg_Price_per_sqft"].apply(lambda x: f"Rs. {x:,.0f}")
    loc_display = loc_display.rename(columns={
        "Avg_Price_per_sqft": "Price/sqft",
        "Property_Count": "Count"
    })
    story.append(df_to_table(loc_display, col_widths=[3*cm, 2.9*cm, 2.9*cm, 2.2*cm, 2.6*cm, 1.9*cm], font_size=8))
    story.append(Spacer(1, 0.3 * cm))

    story.append(Image(f"{VISUALS_DIR}/04_boxplot_by_location.png", width=11*cm, height=7.6*cm))
    story.append(Paragraph("Figure 5: Price distribution comparison across the three locations.", caption_style))

    story.append(PageBreak())

    story.append(Paragraph("9. Property Type Analysis", h1_style))
    type_display = type_summary.copy()
    type_display["Avg_Price"] = type_display["Avg_Price"].apply(lambda x: f"Rs. {x:,.0f}")
    type_display["Median_Price"] = type_display["Median_Price"].apply(lambda x: f"Rs. {x:,.0f}")
    type_display["Avg_Area"] = type_display["Avg_Area"].apply(lambda x: f"{x:,.0f}")
    story.append(df_to_table(type_display, col_widths=[3.5*cm, 3*cm, 3*cm, 3*cm, 2.5*cm]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Image(f"{VISUALS_DIR}/07_property_type_pie.png", width=9*cm, height=9*cm))
    story.append(Paragraph("Figure 6: Proportional distribution of property types in the dataset.", caption_style))

    story.append(PageBreak())

    story.append(Paragraph("10. Bedroom Impact Analysis", h1_style))
    bed_display = bedroom_summary.copy()
    bed_display["Avg_Price"] = bed_display["Avg_Price"].apply(lambda x: f"Rs. {x:,.0f}")
    bed_display["Avg_Area"] = bed_display["Avg_Area"].apply(lambda x: f"{x:,.0f}")
    story.append(df_to_table(bed_display, col_widths=[3*cm, 4*cm, 4*cm, 3*cm]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Image(f"{VISUALS_DIR}/06_avg_price_by_bedrooms.png", width=12*cm, height=8.6*cm))
    story.append(Paragraph("Figure 7: Average property price across different bedroom counts.", caption_style))

    story.append(Image(f"{VISUALS_DIR}/08_age_vs_price.png", width=12*cm, height=8.6*cm))
    story.append(Paragraph("Figure 8: Relationship between property age and price.", caption_style))

    story.append(PageBreak())

    story.append(Paragraph("11. Key Findings", h1_style))
    findings = [
        f"<b>{insights['top_price_driver']}</b> has the strongest positive relationship with "
        f"price (correlation = {insights['top_price_driver_val']:.2f}), making it the single "
        f"most important factor in price determination.",

        f"<b>{insights['weakest_driver']}</b> shows the weakest relationship with price "
        f"(correlation = {insights['weakest_driver_val']:.2f}), suggesting it plays a minor "
        f"role compared to other features.",

        f"<b>{insights['most_valuable_location']}</b> is the most valuable location with an "
        f"average price of Rs. {insights['most_valuable_location_price']:,.0f}, while "
        f"<b>{insights['least_valuable_location']}</b> has the lowest average price.",

        f"<b>{insights['most_valuable_type']}</b> properties command the highest average price "
        f"at Rs. {insights['most_valuable_type_price']:,.0f}.",

        f"The average price per square foot is Rs. {insights['avg_price_per_sqft']:,.2f}, with "
        f"<b>{insights['cheapest_location_per_sqft']}</b> offering the best value per square foot.",
    ]
    for i, finding in enumerate(findings, 1):
        story.append(Paragraph(f"{i}.  {finding}", bullet_style))

    story.append(Paragraph("12. Business Insights", h1_style))
    for line in [
        f"<b>Key Price Drivers:</b> {insights['top_price_driver']} is by far the dominant "
        f"driver of price — far stronger than room counts or property age.",
        "<b>Most Valuable Features:</b> Larger properties in premium locations "
        "(City Center) command significantly higher prices per square foot.",
        "<b>High-Demand Areas:</b> City Center properties have the highest average price, "
        "indicating strong demand and limited supply in central locations.",
    ]:
        story.append(Paragraph(f"•  {line}", bullet_style))

    story.append(Paragraph("13. Recommendations", h1_style))

    story.append(Paragraph("For Investors", h2_style))
    story.append(Paragraph(
        f"•  Prioritize properties in <b>{insights['most_valuable_location']}</b> for "
        f"long-term appreciation, or evaluate <b>{insights['cheapest_location_per_sqft']}</b> "
        f"for a better entry price per square foot.", bullet_style
    ))
    story.append(Paragraph(
        "•  Larger area properties show the most consistent price scaling — a safer bet for "
        "capital preservation.", bullet_style
    ))

    story.append(Paragraph("For Sellers (Pricing Strategy)", h2_style))
    story.append(Paragraph(
        f"•  Price properties based primarily on <b>{insights['top_price_driver']}</b>, the "
        f"strongest value driver identified — not on bedroom or bathroom count alone.",
        bullet_style
    ))
    story.append(Paragraph(
        "•  Older properties should be priced competitively to offset the age-related "
        "depreciation trend observed in the data.", bullet_style
    ))

    story.append(Paragraph("For Buyers", h2_style))
    story.append(Paragraph(
        "•  Compare <b>Price per sq.ft</b> across locations rather than absolute price alone "
        "— it provides a fairer basis for comparing value.", bullet_style
    ))

    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#CCCCCC"), thickness=0.7))
    story.append(Paragraph(
        "Report generated automatically by analysis.py + generate_pdf.py — "
        "Multi-Domain Data Analysis Portfolio by Vishal Arya, Servana Tech.",
        caption_style
    ))

    doc.build(story)
    print(f"[PDF] Report saved to: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_pdf()
