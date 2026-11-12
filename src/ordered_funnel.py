
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


def calculate_ordered_funnel(df):
    print("\nORDERED SESSION FUNNEL")
    print("=" * 55)

    session_events = (
        df.groupby(
            ["visitorid", "session_number", "event"]
        )["datetime"]
        .min()
        .unstack("event")
    )

    for event in ["view", "addtocart", "transaction"]:
        if event not in session_events.columns:
            session_events[event] = pd.NaT

    # Stage 1: session contains a product view ( oturum bir ürün görünümü içerir)
    has_view = session_events["view"].notna()

    # Stage 2: cart event occurs after the first view ( sepet olayı ilk görünümden sonra gerçekleşir)
    view_to_cart = (
        has_view
        & session_events["addtocart"].notna()
        & (
            session_events["addtocart"]
            > session_events["view"]
        )
    )

    # Stage 3: transaction occurs after the cart event ( işlem sepet olayından sonra gerçekleşir)
    cart_to_purchase = (
        view_to_cart
        & session_events["transaction"].notna()
        & (
            session_events["transaction"]
            > session_events["addtocart"]
        )
    )

    counts = [
        int(has_view.sum()),
        int(view_to_cart.sum()),
        int(cart_to_purchase.sum())
    ]

    funnel = pd.DataFrame({
        "stage": [
            "view",
            "addtocart_after_view",
            "transaction_after_addtocart"
        ],
        "session_count": counts
    })

    funnel["conversion_from_previous_stage"] = (
        funnel["session_count"]
        / funnel["session_count"].shift(1)
        * 100
    )

    funnel["conversion_from_previous_stage"] = (
        funnel["conversion_from_previous_stage"].fillna(100)
    )

    funnel["percentage_of_view_sessions"] = (
        funnel["session_count"]
        / counts[0] * 100
    )

    print(funnel.round(2).to_string(index=False))

    funnel.to_csv(
        REPORT_PATH / "ordered_session_funnel.csv",
        index=False
    )

    print("\nOrdered funnel report saved.")

    return funnel


def main():
    df = load_data()
    df = create_sessions(df)

    calculate_ordered_funnel(df)

    print("\nORDERED FUNNEL ANALYSIS COMPLETED!")


if __name__ == "__main__":
    main()
