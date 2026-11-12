from pathlib import Path
import pandas as pd

# Project root directory ( Proje ana dizini )
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Location of the data file ( Veri dosyasının konumu )
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "events.csv"

# Report folder ( Rapor klasörü )
REPORT_PATH = PROJECT_ROOT / "reports"
REPORT_PATH.mkdir(parents=True, exist_ok=True)

def load_data():
    """Loads raw event data from a CSV file.( Ham olay verisini CSV dosyasından yükler. )"""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Data file not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    print("\nDATASET SUCCESSFULLY LOADED")
    print("-" * 50)

    return df

def inspect_data(df):
    """Inspects the basic structure of the dataset.( Veri setinin temel yapısını inceler. )"""

    print("\n1. DATASET SHAPE")
    print(df.shape)

    print("\n2. COLUMN NAMES")
    print(df.columns.tolist())

    print("\n3. DATA TYPES")
    print(df.dtypes)

    print("\n4. FIRST 5 ROWS")
    print(df.head())

    print("\n5. MISSING VALUES")
    print(df.isnull().sum())

    print("\n6. DUPLICATE ROWS")
    print(df.duplicated().sum())

    print("\n7. UNIQUE VISITORS")
    print(df["visitorid"].nunique())

    print("\n8. UNIQUE PRODUCTS")
    print(df["itemid"].nunique())

    print("\n9. EVENT DISTRIBUTION")
    print(df["event"].value_counts())

    print("\n10. DATE RANGE")
    dates = pd.to_datetime(
        df["timestamp"], unit="ms", utc=True
    )
    print("Start:", dates.min())
    print("End:", dates.max())

    print("\n11. MEMORY USAGE")
    print(
        round(df.memory_usage(deep=True).sum() / 1024**2, 2),
        "MB"
    )

def save_profile(df):
    """It saves the basic data profile report. ( Temel veri profili raporunu kaydeder. )"""

    report_file = REPORT_PATH / "initial_data_profile.txt"

    with open(report_file, "w", encoding="utf-8") as file:
        file.write("RETAILROCKET - INITIAL DATA PROFILE\n")
        file.write("=" * 50 + "\n\n")

        file.write(f"Rows: {df.shape[0]}\n")
        file.write(f"Columns: {df.shape[1]}\n")
        file.write(
            f"Unique visitors: {df['visitorid'].nunique()}\n"
        )
        file.write(
            f"Unique products: {df['itemid'].nunique()}\n"
        )

        file.write("\nEVENT DISTRIBUTION\n")
        file.write(df["event"].value_counts().to_string())

        file.write("\n\nMISSING VALUES\n")
        file.write(df.isnull().sum().to_string())

    print(f"\nProfile saved: {report_file}")


if __name__ == "__main__":

    events_df = load_data()

    inspect_data(events_df)

    save_profile(events_df)

    print("\nDATA INSPECTION COMPLETED!")
