
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "events.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed"

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_PATH)

    # Unix timestamp: milliseconds -> UTC datetime (Unix zaman damgası: milisaniye -> UTC tarih ve saat)
    df["datetime"] = pd.to_datetime(
        df["timestamp"],
        unit="ms",
        utc=True
    )

    return df


def create_time_features(df):
    print("\nTIME FEATURE ENGINEERING")
    print("=" * 50)

    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.day_name()
    df["month"] = df["datetime"].dt.month

    print("Time features created.")
    print("\nEvents by hour:")
    print(df["hour"].value_counts().sort_index())

    print("\nEvents by day of week:")
    print(df["day_of_week"].value_counts())

    return df


def create_sessions(df):
    print("\nSESSION IDENTIFICATION")
    print("=" * 50)

    # Sort events by visitor and time
    df = df.sort_values(
        ["visitorid", "datetime"]
    ).copy()

    # Time difference between consecutive events of each visitor (Her ziyaretçinin ardışık etkinlikleri arasındaki zaman farkı)
    time_gap = (
        df.groupby("visitorid")["datetime"]
        .diff()
    )

    # A new session starts if the gap exceeds 30 minutes (30 dakikayı aşarsa yeni bir oturum başlar)
    new_session = (
        time_gap.isna()
        | (time_gap > pd.Timedelta(minutes=30))
    )

    # Session numbers are unique within each visitor (Ziyaretçi başına benzersiz oturum numaraları)
    df["session_number"] = (
        new_session.groupby(df["visitorid"])
        .cumsum()
        .astype("int32")
    )

    print("Session numbers created.")
    print("Unique sessions:", 
          df[["visitorid", "session_number"]]
          .drop_duplicates().shape[0])

    return df


def create_session_features(df):
    print("\nSESSION FEATURE ENGINEERING")
    print("=" * 50)

    session_keys = ["visitorid", "session_number"]

    sessions = (
        df.groupby(session_keys)
        .agg(
            session_start=("datetime", "min"),
            session_end=("datetime", "max"),
            total_events=("event", "size"),
            unique_products=("itemid", "nunique"),
            transaction_count=("transactionid", "nunique")
        )
        .reset_index()
    )

    sessions["duration_minutes"] = (
        sessions["session_end"] - sessions["session_start"]
    ).dt.total_seconds() / 60

    event_counts = (
        df.groupby(session_keys + ["event"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    sessions = sessions.merge(
        event_counts,
        on=session_keys,
        how="left"
    )

    for event in ["view", "addtocart", "transaction"]:
        if event not in sessions.columns:
            sessions[event] = 0

    sessions["converted"] = (
        sessions["transaction"] > 0
    ).astype("int8")

    sessions.to_csv(
        OUTPUT_PATH / "session_features.csv",
        index=False
    )

    print("Total sessions:", len(sessions))
    print("Sessions with purchase:", sessions["converted"].sum())

    return sessions


def create_customer_features(df, sessions):
    print("\nCUSTOMER FEATURE ENGINEERING")
    print("=" * 50)

    customer_events = (
        df.groupby(["visitorid", "event"])
        .size()
        .unstack(fill_value=0)
    )

    for event in ["view", "addtocart", "transaction"]:
        if event not in customer_events.columns:
            customer_events[event] = 0

    customer_events["total_events"] = (
        customer_events[["view", "addtocart", "transaction"]]
        .sum(axis=1)
    )

    customer_events["unique_products"] = (
        df.groupby("visitorid")["itemid"].nunique()
    )

    customer_events["unique_transactions"] = (
        df.groupby("visitorid")["transactionid"].nunique()
    )

    customer_events["session_count"] = (
        sessions.groupby("visitorid")["session_number"]
        .nunique()
    )

    customer_events["converted"] = (
        customer_events["transaction"] > 0
    ).astype("int8")

    customer_events = customer_events.fillna(0)

    customer_events.to_csv(
        OUTPUT_PATH / "customer_features.csv"
    )

    print("Unique customers:", len(customer_events))
    print(
        "Customers with at least one purchase:",
        customer_events["converted"].sum()
    )

    return customer_events


def main():
    df = load_data()

    df = create_time_features(df)
    df = create_sessions(df)

    sessions = create_session_features(df)

    customers = create_customer_features(
        df,
        sessions
    )

    print("\nFEATURE ENGINEERING COMPLETED!")
    print("Processed files saved in:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
