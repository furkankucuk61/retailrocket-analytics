
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
REPORT_PATH = PROJECT_ROOT / "reports"

REPORT_PATH.mkdir(parents=True, exist_ok=True)


def load_features():
    customers = pd.read_csv(
        PROCESSED_PATH / "customer_features.csv",
        index_col=0
    )

    sessions = pd.read_csv(
        PROCESSED_PATH / "session_features.csv"
    )

    return customers, sessions


def calculate_funnel(data, level):
    if level == "customer":
        total = len(data)
    else:
        total = len(data)

    stages = {
        "view": (data["view"] > 0).sum(),
        "addtocart": (data["addtocart"] > 0).sum(),
        "transaction": (data["transaction"] > 0).sum()
    }

    funnel = pd.DataFrame({
        "stage": list(stages.keys()),
        "count": list(stages.values())
    })

    funnel["percentage_of_total"] = (
        funnel["count"] / total * 100
    )

    funnel["conversion_from_previous_stage"] = (
        funnel["count"] /
        funnel["count"].shift(1) * 100
    )

    funnel.loc[0, "conversion_from_previous_stage"] = 100

    print(f"\n{level.upper()} FUNNEL")
    print("=" * 50)
    print(funnel.round(2).to_string(index=False))

    funnel.to_csv(
        REPORT_PATH / f"{level}_funnel.csv",
        index=False
    )

    return funnel


def main():
    customers, sessions = load_features()

    print("CUSTOMER AND SESSION ANALYSIS")
    print("=" * 50)

    print("Total customers:", len(customers))
    print("Total sessions:", len(sessions))

    customer_funnel = calculate_funnel(
        customers,
        "customer"
    )

    session_funnel = calculate_funnel(
        sessions,
        "session"
    )

    print("\nCONVERSION KPIs")
    print("=" * 50)

    customer_conversion = customers["converted"].mean() * 100
    session_conversion = sessions["converted"].mean() * 100

    print(
        f"Customer conversion rate: "
        f"{customer_conversion:.2f}%"
    )

    print(
        f"Session conversion rate: "
        f"{session_conversion:.2f}%"
    )

    print("\nANALYSIS COMPLETED!")


if __name__ == "__main__":
    main()
