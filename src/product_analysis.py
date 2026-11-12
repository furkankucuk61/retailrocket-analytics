
import pandas as pd
from pathlib import Path

# -----------------------------------
# 1. PROJECT PATHS ( proje yolları)
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------
# 2. LOAD EVENT DATA ( etkinlik verilerini yükle)
# -----------------------------------

events = pd.read_csv(
    RAW_DIR / "events.csv",
    usecols=["visitorid", "event", "itemid"]
)

print("Events loaded:", len(events))


# -----------------------------------
# 3. PRODUCT PERFORMANCE ( ürün performansı)
# -----------------------------------

product_metrics = (
    events
    .groupby(["itemid", "event"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# Ensure all event columns exist ( Tüm etkinlik sütunlarının mevcut olduğundan emin olun)
for event_type in ["view", "addtocart", "transaction"]:
    if event_type not in product_metrics.columns:
        product_metrics[event_type] = 0

# Rename columns (Sütunları yeniden adlandır)
product_metrics = product_metrics.rename(
    columns={
        "view": "view_count",
        "addtocart": "addtocart_count",
        "transaction": "transaction_count"
    }
)

# Product-level event conversion proxy (Ürün düzeyinde etkinlik dönüşüm göstergesi)
product_metrics["purchase_to_view_pct"] = (
    product_metrics["transaction_count"] /
    product_metrics["view_count"].replace(0, pd.NA) * 100
).fillna(0)

product_metrics["cart_to_view_pct"] = (
    product_metrics["addtocart_count"] /
    product_metrics["view_count"].replace(0, pd.NA) * 100
).fillna(0)


# -----------------------------------
# 4. LOAD PRODUCT CATEGORY INFORMATION (Ürün kategori bilgilerini yükle)
# -----------------------------------

properties_1 = pd.read_csv(
    RAW_DIR / "item_properties_part1.csv"
)

properties_2 = pd.read_csv(
    RAW_DIR / "item_properties_part2.csv"
)

properties = pd.concat(
    [properties_1, properties_2],
    ignore_index=True
)

print("\nProperty columns:", properties.columns.tolist())

# Find category information ( Kategori bilgilerini bul)
category_properties = properties[
    properties["property"].astype(str).str.lower() == "categoryid"
].copy()

print(
    "Category property records:",
    len(category_properties)
)

# Keep the latest known category for each product ( Her ürün için en son bilinen kategoriyi saklayın)
category_properties["timestamp"] = pd.to_numeric(
    category_properties["timestamp"],
    errors="coerce"
)

category_properties = category_properties.sort_values(
    "timestamp"
)

product_categories = (
    category_properties
    .drop_duplicates("itemid", keep="last")
    [["itemid", "value"]]
    .rename(columns={"value": "categoryid"})
)

product_categories["categoryid"] = pd.to_numeric(
    product_categories["categoryid"],
    errors="coerce"
)


# -----------------------------------
# 5. LOAD CATEGORY TREE ( Kategori ağacını yükle)
# -----------------------------------

category_tree = pd.read_csv(
    RAW_DIR / "category_tree.csv"
)

print("\nCategory tree columns:")
print(category_tree.columns.tolist())

# -----------------------------------
# 6. COMBINE PRODUCT AND CATEGORY DATA (Ürün ve kategori verilerini birleştir)
# -----------------------------------

product_metrics = product_metrics.merge(
    product_categories,
    on="itemid",
    how="left"
)

product_metrics = product_metrics.merge(
    category_tree,
    on="categoryid",
    how="left"
)

print(
    "\nProducts with category:",
    product_metrics["categoryid"].notna().sum()
)

print(
    "Products without category:",
    product_metrics["categoryid"].isna().sum()
)


# -----------------------------------
# 7. TOP 10 PRODUCTS ( EN İYİ 10 ÜRÜN)
# -----------------------------------

top_viewed = product_metrics.nlargest(
    10, "view_count"
)

top_carted = product_metrics.nlargest(
    10, "addtocart_count"
)

top_purchased = product_metrics.nlargest(
    10, "transaction_count"
)

top_viewed.to_csv(
    REPORTS_DIR / "top_viewed_products.csv",
    index=False
)

top_carted.to_csv(
    REPORTS_DIR / "top_carted_products.csv",
    index=False
)

top_purchased.to_csv(
    REPORTS_DIR / "top_purchased_products.csv",
    index=False
)


# ----------------------------------- 
# 8. CATEGORY PERFORMANCE ( KATEGORİ PERFORMANSI)
# -----------------------------------

category_summary = (
    product_metrics
    .dropna(subset=["categoryid"])
    .groupby("categoryid")
    .agg(
        product_count=("itemid", "nunique"),
        total_views=("view_count", "sum"),
        total_addtocart=("addtocart_count", "sum"),
        total_transactions=("transaction_count", "sum")
    )
    .reset_index()
)

category_summary["purchase_to_view_pct"] = (
    category_summary["total_transactions"] /
    category_summary["total_views"].replace(0, pd.NA) * 100
).fillna(0)

category_summary["cart_to_view_pct"] = (
    category_summary["total_addtocart"] /
    category_summary["total_views"].replace(0, pd.NA) * 100
).fillna(0)

category_summary = category_summary.sort_values(
    "total_transactions",
    ascending=False
)

category_summary.to_csv(
    REPORTS_DIR / "category_performance.csv",
    index=False
)


# -----------------------------------
# 9. SAVE COMPLETE PRODUCT DATA ( TAM ÜRÜN VERİLERİNİ KAYDET)
# -----------------------------------

product_metrics.to_csv(
    REPORTS_DIR / "product_performance.csv",
    index=False
)


# -----------------------------------
# 10. DISPLAY RESULTS ( SONUÇLARI GÖSTER)
# -----------------------------------

print("\nTOP 10 VIEWED PRODUCTS")
print(
    top_viewed[
        ["itemid", "view_count", "addtocart_count", "transaction_count"]
    ].to_string(index=False)
)

print("\nTOP 10 CARTED PRODUCTS")
print(
    top_carted[
        ["itemid", "view_count", "addtocart_count", "transaction_count"]
    ].to_string(index=False)
)

print("\nTOP 10 PURCHASED PRODUCTS")
print(
    top_purchased[
        ["itemid", "view_count", "addtocart_count", "transaction_count"]
    ].to_string(index=False)
)

print("\nTOP 10 CATEGORIES BY TRANSACTIONS")
print(
    category_summary.head(10).round(2).to_string(index=False)
)

print("\nPRODUCT ANALYSIS COMPLETED!")
