
import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------
# 1. PROJECT PATHS ( proje yolları)
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------
# 2. LOAD CUSTOMER DATA ( müşteri verilerini yükle)
# --------------------------------

customers = pd.read_csv(
    DATA_DIR / "customer_features.csv"
)

print("Customer data loaded successfully!")
print("Total customers:", len(customers))


# --------------------------------
# 3. CUSTOMER SEGMENTATION ( müşteri segmentasyonu)
# --------------------------------

conditions = [
    customers["converted"] == 1,

    (customers["converted"] == 0) &
    (customers["addtocart"] > 0),

    (customers["converted"] == 0) &
    (customers["addtocart"] == 0) &
    (customers["view"] > 0)
]

segments = [
    "Purchasers",
    "Cart Abandoners",
    "Product Browsers"
]

customers["customer_segment"] = np.select(
    conditions,
    segments,
    default="Other Interactions"
)


# --------------------------------
# 4. HIGH ENGAGEMENT FLAG ( yüksek etkileşim bayrağı)
# --------------------------------

engagement_threshold = customers["total_events"].quantile(0.90)

customers["high_engagement"] = (
    customers["total_events"] >= engagement_threshold
)

print("\nHIGH ENGAGEMENT THRESHOLD")
print(engagement_threshold)


# --------------------------------
# 5. SEGMENT SUMMARY ( segment özeti)
# --------------------------------

segment_summary = (
    customers
    .groupby("customer_segment")
    .agg(
        customer_count=("visitorid", "count"),
        avg_events=("total_events", "mean"),
        median_events=("total_events", "median"),
        avg_products=("unique_products", "mean"),
        avg_sessions=("session_count", "mean"),
        avg_transactions=("unique_transactions", "mean")
    )
    .reset_index()
)

segment_summary["customer_share_pct"] = (
    segment_summary["customer_count"] /
    len(customers) * 100
)

segment_summary = segment_summary.sort_values(
    "customer_count",
    ascending=False
)


# --------------------------------
# 6. HIGH ENGAGEMENT ANALYSIS ( yüksek etkileşim analizi)
# --------------------------------

engagement_summary = (
    customers
    .groupby("high_engagement")
    .agg(
        customer_count=("visitorid", "count"),
        avg_events=("total_events", "mean"),
        purchase_rate=("converted", "mean"),
        avg_sessions=("session_count", "mean")
    )
    .reset_index()
)

engagement_summary["purchase_rate_pct"] = (
    engagement_summary["purchase_rate"] * 100
)


# --------------------------------
# 7. SAVE RESULTS ( sonuçları kaydet)
# --------------------------------

customers.to_csv(
    DATA_DIR / "customer_segments.csv",
    index=False
)

segment_summary.to_csv(
    REPORTS_DIR / "customer_segment_summary.csv",
    index=False
)

engagement_summary.to_csv(
    REPORTS_DIR / "engagement_summary.csv",
    index=False
)


# --------------------------------
# 8. DISPLAY RESULTS ( sonuçları görüntüle)
# --------------------------------

print("\nCUSTOMER SEGMENT SUMMARY")
print(
    segment_summary.round(2).to_string(index=False)
)

print("\nHIGH ENGAGEMENT SUMMARY")
print(
    engagement_summary.round(2).to_string(index=False)
)

print("\nSEGMENTATION COMPLETED SUCCESSFULLY!")
