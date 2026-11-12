
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

# Load reports
segments = pd.read_csv(
    REPORTS_DIR / "customer_segment_summary.csv"
)

engagement = pd.read_csv(
    REPORTS_DIR / "engagement_summary.csv"
)

# -----------------------------------
# CHART 1: Customer Segment Distribution
# -----------------------------------

segments = segments.sort_values(
    "customer_count",
    ascending=True
)

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    data=segments,
    x="customer_count",
    y="customer_segment",
    ax=ax
)

ax.set_title("Customer Segment Distribution")
ax.set_xlabel("Number of Customers")
ax.set_ylabel("Customer Segment")

for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", padding=4)

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "customer_segment_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# -----------------------------------
# CHART 2: Purchase Rate by Engagement
# -----------------------------------

engagement["engagement_group"] = engagement[
    "high_engagement"
].map({
    False: "Low Engagement",
    True: "High Engagement"
})

fig, ax = plt.subplots(figsize=(9, 6))

sns.barplot(
    data=engagement,
    x="engagement_group",
    y="purchase_rate_pct",
    ax=ax
)

ax.set_title("Purchase Rate by Engagement Level")
ax.set_xlabel("Customer Engagement")
ax.set_ylabel("Purchase Rate (%)")

for container in ax.containers:
    ax.bar_label(
        container,
        fmt="%.2f%%",
        padding=4
    )

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "purchase_rate_by_engagement.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

print("Customer segmentation charts created!")
print(f"Saved in: {IMAGES_DIR}")
