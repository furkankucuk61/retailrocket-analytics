
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project directories (proje dizinleri)
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
IMAGES_DIR = BASE_DIR / "images"

# Create images directory if it does not exist ( resim dizini yoksa oluştur)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Visualization style ( görselleştirme stili)
sns.set_theme(style="whitegrid", palette="deep")


# Load daily performance data ( günlük performans verilerini yükle)
daily = pd.read_csv(
    REPORTS_DIR / "daily_performance.csv",
    parse_dates=["date"]
)

# Load weekday performance data ( haftanın günü performans verilerini yükle)
weekday = pd.read_csv(
    REPORTS_DIR / "weekday_performance.csv"
)


# -----------------------------------
# CHART 1: Daily Sessions and Purchases ( günlük oturumlar ve satın almalar)
# -----------------------------------

fig, ax1 = plt.subplots(figsize=(14, 6))

ax1.plot(
    daily["date"],
    daily["total_sessions"],
    label="Total Sessions",
    linewidth=1.8
)

ax1.set_xlabel("Date")
ax1.set_ylabel("Total Sessions")
ax1.set_title("Daily Sessions and Converted Sessions")
ax1.tick_params(axis="x", rotation=45)

ax2 = ax1.twinx()

ax2.plot(
    daily["date"],
    daily["converted_sessions"],
    label="Converted Sessions",
    linewidth=1.8,
    linestyle="--"
)

ax2.set_ylabel("Converted Sessions")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc="upper right"
)

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "daily_sessions_and_conversions.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# -----------------------------------
# CHART 2: Daily Conversion Rate ( günlük dönüşüm oranı)
# -----------------------------------

daily["rolling_conversion_rate"] = (
    daily["conversion_rate"].rolling(window=7).mean()
)

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    daily["date"],
    daily["conversion_rate"],
    label="Daily Conversion Rate",
    alpha=0.45,
    linewidth=1
)

ax.plot(
    daily["date"],
    daily["rolling_conversion_rate"],
    label="7-Day Moving Average",
    linewidth=2
)

ax.set_title("Daily Conversion Rate Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Conversion Rate (%)")
ax.tick_params(axis="x", rotation=45)
ax.legend()

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "daily_conversion_rate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


# -----------------------------------
# CHART 3: Weekday Conversion Rate ( haftanın günü dönüşüm oranı)
# -----------------------------------

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday["day_of_week"] = pd.Categorical(
    weekday["day_of_week"],
    categories=weekday_order,
    ordered=True
)

weekday = weekday.sort_values("day_of_week")

fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(
    data=weekday,
    x="day_of_week",
    y="conversion_rate",
    ax=ax
)

ax.set_title("Conversion Rate by Day of Week")
ax.set_xlabel("Day of Week")
ax.set_ylabel("Conversion Rate (%)")
ax.tick_params(axis="x", rotation=30)

fig.tight_layout()

fig.savefig(
    IMAGES_DIR / "weekday_conversion_rate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)


print("All visualizations created successfully!")

print(f"Images saved in: {IMAGES_DIR}")
