
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "events.csv"
REPORT_PATH = PROJECT_ROOT / "reports"

REPORT_PATH.mkdir(parents=True, exist_ok=True)


def load_data():
    """Load raw dataset.( Ham veri kümesini yükler. )"""

    df = pd.read_csv(DATA_PATH)

    return df


def analyze_missing_values(df):
    """Analyze missing values by event type.( Etkinlik türüne göre eksik değerleri analiz eder. )"""

    print("\nMISSING VALUES BY EVENT TYPE")
    print("=" * 50)

    missing_by_event = (
        df.groupby("event")["transactionid"]
        .agg(
            total_records="count",
        )
    )

    # Calculate actual missing and non-missing values (Gerçek eksik ve eksik olmayan değerleri hesapla )
    missing_counts = (
        df.groupby("event")["transactionid"]
        .agg(
            missing=lambda x: x.isna().sum(),
            non_missing=lambda x: x.notna().sum()
        )
    )

    print(missing_counts)

    missing_counts.to_csv(
        REPORT_PATH / "missing_values_by_event.csv"
    )

    return missing_counts

def analyze_duplicates(df):
    """Analyze exact duplicate records.( Tam yinelenen kayıtları analiz eder. )"""

    print("\nDUPLICATE ANALYSIS")
    print("=" * 50)

    duplicate_rows = df[df.duplicated(keep=False)]

    print("Total duplicate rows:", df.duplicated().sum())

    print("\nDuplicate distribution by event:")
    print(duplicate_rows["event"].value_counts())

    print("\nSample duplicate records:")
    print(duplicate_rows.head(10))

    duplicate_rows.to_csv(
        REPORT_PATH / "duplicate_records.csv",
        index=False
    )


def analyze_transactions(df):
    """Check transaction data consistency.( İşlem veri tutarlılığını kontrol eder. )"""

    print("\nTRANSACTION VALIDATION")
    print("=" * 50)

    transaction_events = df[df["event"] == "transaction"]

    print(
        "Total transaction events:",
        len(transaction_events)
    )

    print(
        "Transaction events with missing ID:",
        transaction_events["transactionid"].isna().sum()
    )

    print(
        "Unique transaction IDs:",
        transaction_events["transactionid"].nunique()
    )

    print(
        "Transaction events without item ID:",
        transaction_events["itemid"].isna().sum()
    )

def analyze_timestamps(df):
    """Check timestamp validity.( Zaman damgası geçerliliğini kontrol eder. )"""

    print("\nTIMESTAMP ANALYSIS")
    print("=" * 50)

    dates = pd.to_datetime(
        df["timestamp"],
        unit="ms",
        utc=True,
        errors="coerce"
    )

    print("Invalid timestamps:", dates.isna().sum())
    print("Earliest timestamp:", dates.min())
    print("Latest timestamp:", dates.max())

    print("\nEvents by year and month:")

    monthly_events = (
        dates.dt.to_period("M")
        .value_counts()
        .sort_index()
    )

    print(monthly_events)


def main():

    df = load_data()

    analyze_missing_values(df)

    analyze_duplicates(df)

    analyze_transactions(df)

    analyze_timestamps(df)

    print("\nDATA QUALITY ANALYSIS COMPLETED!")


if __name__ == "__main__":
    main()