
import pandas as pd
from pathlib import Path

# -----------------------------------
# 1. PROJECT PATHS ( Proje yolları )
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------
# 2. LOAD PRODUCT DATA ( Ürün verilerini yükle )
# -----------------------------------

products = pd.read_csv(
    REPORTS_DIR / "product_performance.csv"
)

print("Products loaded:", len(products))


# -----------------------------------
# 3. CALCULATE EVENT RATIOS ( Etkinlik oranlarını hesapla )
# -----------------------------------

products["cart_to_view_pct"] = (
    products["addtocart_count"] /
    products["view_count"].replace(0, pd.NA) * 100
)

products["purchase_to_cart_pct"] = (
    products["transaction_count"] /
    products["addtocart_count"].replace(0, pd.NA) * 100
)

products["purchase_to_view_pct"] = (
    products["transaction_count"] /
    products["view_count"].replace(0, pd.NA) * 100
)

# Replace undefined ratios with zero for display. ( Görüntüleme için tanımsız oranları sıfırla değiştir.)
# Eligibility filters below ensure denominators are positive. ( Aşağıdaki uygunluk filtreleri paydaların pozitif olmasını sağlar.)
products[
    [
        "cart_to_view_pct",
        "purchase_to_cart_pct",
        "purchase_to_view_pct"
    ]
] = products[
    [
        "cart_to_view_pct",
        "purchase_to_cart_pct",
        "purchase_to_view_pct"
    ]
].fillna(0)


# -----------------------------------
# 4. HIGH VIEWS, LOW CART ( YÜKSEK GÖRÜNTÜLEME, DÜŞÜK SEPET )
# -----------------------------------

# Minimum view volume reduces noisy results. ( Minimum görüntüleme hacmi gürültülü sonuçları azaltır.)
view_eligible = products[
    products["view_count"] >= 100
].copy()

# Use the lower quartile as a relative benchmark.( Düşük çeyreği göreceli bir kıyaslama olarak kullanın.)
cart_rate_threshold = view_eligible[
    "cart_to_view_pct"
].quantile(0.25)

high_views_low_cart = view_eligible[
    view_eligible["cart_to_view_pct"] <= cart_rate_threshold
].copy()

high_views_low_cart = high_views_low_cart.sort_values(
    ["view_count", "cart_to_view_pct"],
    ascending=[False, True]
)

high_views_low_cart.to_csv(
    REPORTS_DIR / "high_views_low_cart.csv",
    index=False
)


# -----------------------------------
# 5. HIGH CART, LOW PURCHASE ( YÜKSEK SEPET, DÜŞÜK SATIN ALMA )
# -----------------------------------

# Minimum cart volume reduces noisy results. ( Minimum sepet hacmi gürültülü sonuçları azaltır.)
cart_eligible = products[
    products["addtocart_count"] >= 10
].copy()

purchase_rate_threshold = cart_eligible[
    "purchase_to_cart_pct"
].quantile(0.25)

high_cart_low_purchase = cart_eligible[
    cart_eligible["purchase_to_cart_pct"] <= purchase_rate_threshold
].copy()

high_cart_low_purchase = high_cart_low_purchase.sort_values(
    ["addtocart_count", "purchase_to_cart_pct"],
    ascending=[False, True]
)

high_cart_low_purchase.to_csv(
    REPORTS_DIR / "high_cart_low_purchase.csv",
    index=False
)


# -----------------------------------
# 6. DISPLAY RESULTS ( SONUÇLARI GÖSTER )
# -----------------------------------

display_columns = [
    "itemid",
    "view_count",
    "addtocart_count",
    "transaction_count",
    "cart_to_view_pct",
    "purchase_to_cart_pct"
]

print("\nCART-TO-VIEW LOWER QUARTILE THRESHOLD:")
print(round(cart_rate_threshold, 2), "%")

print("\nHIGH VIEWS, LOW CART")
print(
    high_views_low_cart[display_columns]
    .head(20)
    .round(2)
    .to_string(index=False)
)

print("\nPURCHASE-TO-CART LOWER QUARTILE THRESHOLD:")
print(round(purchase_rate_threshold, 2), "%")

print("\nHIGH CART, LOW PURCHASE")
print(
    high_cart_low_purchase[display_columns]
    .head(20)
    .round(2)
    .to_string(index=False)
)

print("\nOPPORTUNITY ANALYSIS SUMMARY")
print("High views, low cart:", len(high_views_low_cart))
print("High cart, low purchase:", len(high_cart_low_purchase))

print("\nPRODUCT OPPORTUNITY ANALYSIS COMPLETED!")
