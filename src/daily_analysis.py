
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "events.csv"
REPORT_PATH = PROJECT_ROOT / "reports"

REPORT_PATH.mkdir(parents=True, exist_ok=True)


def load_data():
    df = pd.read_csv(DATA_PATH)

    df["datetime"] = pd.to_datetime(
        df["timestamp"],
        unit="ms",
        utc=True
    )

    return df


def create_sessions(df):
    print("\nSESSION IDENTIFICATION")
    print("=" * 50)

    df = df.sort_values(
        ["visitorid", "datetime"]
    ).copy()

    time_gap = (
        df.groupby("visitorid")["datetime"].diff()
    )

    new_session = (
        time_gap.isna()
        | (time_gap > pd.Timedelta(minutes=30))
    )

    df["session_number"] = (
        new_session.groupby(df["visitorid"])
        .cumsum()
        .astype("int32")
    )

    return df


def build_session_table(df):
    print("\nBUILDING SESSION TABLE")
    print("=" * 50)

    session_keys = ["visitorid", "session_number"]

    sessions = (
        df.groupby(session_keys)
        .agg(
            session_start=("datetime", "min"),
            session_end=("datetime", "max"),
            total_events=("event", "size"),
            transaction_count=("transactionid", "nunique")
        )
        .reset_index()
    )

    # A session is converted if it contains a transaction ( bir işlem içeren bir oturum dönüştürülür)
    sessions["converted"] = (
        sessions["transaction_count"] > 0
    ).astype("int8")

    # Assign each session to its start date (UTC) ( her oturumu başlangıç tarihine (UTC) atayın)
    sessions["date"] = (
        sessions["session_start"].dt.floor("D")
    )

    return sessions


def calculate_daily_metrics(sessions):
    print("\nDAILY PERFORMANCE ANALYSIS")
    print("=" * 50)

    daily = (
        sessions.groupby("date")
        .agg(
            total_sessions=("session_number", "size"),
            converted_sessions=("converted", "sum"),
            total_transactions=("transaction_count", "sum"),
            total_events=("total_events", "sum")
        )
    )

    # Include calendar days with no sessions ( oturum olmayan takvim günlerini dahil et)
    full_dates = pd.date_range(
        start=daily.index.min(),
        end=daily.index.max(),
        freq="D",
        tz="UTC"
    )

    daily = daily.reindex(
        full_dates,
        fill_value=0
    )

    daily.index.name = "date"

    daily["conversion_rate"] = (
        daily["converted_sessions"]
        / daily["total_sessions"].replace(0, pd.NA)
        * 100
    )

    daily["day_of_week"] = daily.index.day_name()

    daily = daily.reset_index()

    daily.to_csv(
        REPORT_PATH / "daily_performance.csv",
        index=False
    )

    print("\nFirst 10 days:")
    print(
    daily.head(10).to_string(
        index=False,
        formatters={
            "conversion_rate": "{:.2f}".format
            }
        )
    )

    print("\nDaily metrics summary:")
    print(
        daily[
            [
                "total_sessions",
                "converted_sessions",
                "total_transactions",
                "conversion_rate"
            ]
        ].describe().round(2)
    )

    return daily


def calculate_weekday_metrics(daily):
    print("\nWEEKDAY PERFORMANCE ANALYSIS")
    print("=" * 50)

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekday = (
        daily.groupby("day_of_week")
        .agg(
            total_sessions=("total_sessions", "sum"),
            converted_sessions=("converted_sessions", "sum"),
            total_transactions=("total_transactions", "sum"),
            active_days=("date", "count")
        )
    )

    weekday["conversion_rate"] = (
        weekday["converted_sessions"]
        / weekday["total_sessions"].replace(0, pd.NA)
        * 100
    )

    weekday["avg_sessions_per_day"] = (
        weekday["total_sessions"]
        / weekday["active_days"]
    )

    weekday = weekday.reindex(weekday_order).reset_index()

    weekday.to_csv(
        REPORT_PATH / "weekday_performance.csv",
        index=False
    )

    print(weekday.round(2).to_string(index=False))

    return weekday


def main():
    df = load_data()

    df = create_sessions(df)

    sessions = build_session_table(df)

    daily = calculate_daily_metrics(sessions)

    calculate_weekday_metrics(daily)

    print("\nDAILY ANALYSIS COMPLETED!")
    print("Reports saved in:", REPORT_PATH)


if __name__ == "__main__":
    main()
