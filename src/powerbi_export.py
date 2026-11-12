
import pandas as pd
from pathlib import Path

# -----------------------------------
# 1. PROJECT PATHS ( Proje yolları )
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

REPORTS_DIR = BASE_DIR / "reports"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

POWERBI_DIR = BASE_DIR / "powerbi" / "data"
POWERBI_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------
# 2. HELPER FUNCTION ( YARDIMCI FONKSİYON )
# -----------------------------------

def export_report(source, destination):
    if source.exists():
        df = pd.read_csv(source)
        df.to_csv(destination, index=False)
        print(f"Exported: {destination.name}")
        return df

    print(f"Skipped (not found): {source.name}")
    return None


# -----------------------------------
# 3. EXPORT ANALYSIS TABLES ( ANALİZ TABLOLARINI DIŞA AKTAR )
# -----------------------------------

daily = export_report(
    REPORTS_DIR / "daily_performance.csv",
    POWERBI_DIR / "daily_performance.csv"
)

customer_segments = export_report(
    PROCESSED_DIR / "customer_segments.csv",
    POWERBI_DIR / "customer_segments.csv"
)

segment_summary = export_report(
    REPORTS_DIR / "customer_segment_summary.csv",
    POWERBI_DIR / "customer_segment_summary.csv"
)

products = export_report(
    REPORTS_DIR / "product_performance.csv",
    POWERBI_DIR / "product_performance.csv"
)

categories = export_report(
    REPORTS_DIR / "category_performance.csv",
    POWERBI_DIR / "category_performance.csv"
)

high_views_low_cart = export_report(
    REPORTS_DIR / "high_views_low_cart.csv",
    POWERBI_DIR / "high_views_low_cart.csv"
)

high_cart_low_purchase = export_report(
    REPORTS_DIR / "high_cart_low_purchase.csv",
    POWERBI_DIR / "high_cart_low_purchase.csv"
)


# -----------------------------------
# 4. EXECUTIVE KPI SUMMARY ( YÖNETİCİ KPI ÖZETİ )
# -----------------------------------

kpis = {}

if daily is not None:
    total_sessions = daily["total_sessions"].sum()
    converted_sessions = daily["converted_sessions"].sum()

    total_transactions = daily["total_transactions"].sum()
    total_events = daily["total_events"].sum()

    kpis["total_sessions"] = total_sessions
    kpis["converted_sessions"] = converted_sessions
    kpis["total_transactions"] = total_transactions
    kpis["total_events"] = total_events

    kpis["session_conversion_rate_pct"] = (
        converted_sessions / total_sessions * 100
        if total_sessions else 0
    )

if customer_segments is not None:
    kpis["total_customers"] = len(customer_segments)

    kpis["purchasing_customers"] = (
        customer_segments["converted"].sum()
    )

    kpis["customer_conversion_rate_pct"] = (
        customer_segments["converted"].mean() * 100
    )

if products is not None:
    kpis["total_products"] = products["itemid"].nunique()

if categories is not None:
    kpis["total_categories"] = categories["categoryid"].nunique()


kpi_summary = pd.DataFrame(
    [
        {"metric": metric, "value": value}
        for metric, value in kpis.items()
    ]
)

kpi_summary.to_csv(
    POWERBI_DIR / "executive_kpis.csv",
    index=False
)


# -----------------------------------
# 5. EXPORT SUMMARY TABLES ( ÖZET TABLOLARINI DIŞA AKTAR )
# -----------------------------------

print("\nEXECUTIVE KPI SUMMARY")
print(kpi_summary.to_string(index=False))

print("\nPOWER BI DATA EXPORT COMPLETED!")
print(f"Output directory: {POWERBI_DIR}")
