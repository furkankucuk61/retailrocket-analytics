
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project paths 
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
IMAGES_DIR = BASE_DIR / "images"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


# -----------------------------------
# 1. LOAD REPORTS ( RAPORLARI YÜKLE)
# -----------------------------------

top_viewed = pd.read_csv(
    REPORTS_DIR / "top_viewed_products.csv"
)

top_purchased = pd.read_csv(
    REPORTS_DIR / "top_purchased_products.csv"
)

category = pd.read_csv(
    REPORTS_DIR / "category_performance.csv"
)


# -----------------------------------
# 2. TOP VIEWED PRODUCTS (EN ÇOK GÖRÜNTÜLENEN ÜRÜNLER)
# -----------------------------------

top_viewed = top_viewed.sort_values(
    "view_count",
    ascending=True
)

fig, ax = plt.subplots(figsize=(10, 7))

sns.barplot(
    data=top_viewed,
    x="view_count",
    y="itemid",
    ax=ax
)

ax.set_title("Top 10 Most Viewed Products")
ax.set_xlabel("View Events")
ax.set_ylabel("Product ID")

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "top_viewed_products.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# -----------------------------------
# 3. TOP PURCHASED PRODUCTS (EN ÇOK SATIN ALINAN ÜRÜNLER)
# -----------------------------------

top_purchased = top_purchased.sort_values(
    "transaction_count",
    ascending=True
)

fig, ax = plt.subplots(figsize=(10, 7))

sns.barplot(
    data=top_purchased,
    x="transaction_count",
    y="itemid",
    ax=ax
)

ax.set_title("Top 10 Most Purchased Products")
ax.set_xlabel("Purchase Events")
ax.set_ylabel("Product ID")

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "top_purchased_products.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# -----------------------------------
# 4. TOP CATEGORIES BY PURCHASES (KATEGORİLERİN SATIN ALMA SAYISINA GÖRE EN İYİLER)
# -----------------------------------

top_categories = (
    category
    .nlargest(10, "total_transactions")
    .sort_values("total_transactions")
)

fig, ax = plt.subplots(figsize=(10, 7))

sns.barplot(
    data=top_categories,
    x="total_transactions",
    y="categoryid",
    ax=ax
)

ax.set_title("Top 10 Categories by Purchase Events")
ax.set_xlabel("Purchase Events")
ax.set_ylabel("Category ID")

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "top_categories_by_purchases.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# -----------------------------------
# 5. CATEGORY PURCHASE-TO-VIEW RATIO (KATEGORİ SATIN ALMA-GÖRÜNTÜLEME ORANI)
# -----------------------------------

top_conversion_categories = (
    category[
        category["total_views"] >= 5000
    ]
    .nlargest(10, "purchase_to_view_pct")
    .sort_values("purchase_to_view_pct")
)

fig, ax = plt.subplots(figsize=(10, 7))

sns.barplot(
    data=top_conversion_categories,
    x="purchase_to_view_pct",
    y="categoryid",
    ax=ax
)

ax.set_title(
    "Top Categories by Purchase-to-View Event Ratio"
)

ax.set_xlabel("Purchase-to-View Event Ratio (%)")
ax.set_ylabel("Category ID")

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "top_categories_by_event_ratio.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


print("Product visualization completed!")
print(f"Charts saved in: {IMAGES_DIR}")
