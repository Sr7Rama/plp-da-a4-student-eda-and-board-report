"""Generate the reproducible student and Duka Electronics sample datasets."""

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent


def generate_student_performance() -> pd.DataFrame:
    rng = np.random.default_rng(55)
    n_students = 500
    students = pd.DataFrame(
        {
            "student_id": [f"STU{i:04d}" for i in range(1, n_students + 1)],
            "gender": rng.choice(
                ["Male", "Female"], size=n_students, p=[0.48, 0.52]
            ),
            "hours_studied": rng.uniform(2, 20, size=n_students).round(1),
            "attendance_rate": rng.uniform(60, 100, size=n_students).round(1),
            "previous_score": rng.integers(40, 100, size=n_students),
        }
    )
    students["final_score"] = np.clip(
        students["hours_studied"] * 1.5
        + students["attendance_rate"] * 0.4
        + students["previous_score"] * 0.3
        + rng.normal(0, 5, n_students),
        0,
        100,
    ).round(1)
    return students


def generate_duka_sales() -> pd.DataFrame:
    rng = np.random.default_rng(2026)
    n_orders = 1000
    product_names = rng.choice(
        [
            "Smartphone",
            "Wireless Headphones",
            "Laptop",
            "Smart TV",
            "Soundbar",
        ],
        size=n_orders,
        p=[0.33, 0.19, 0.18, 0.15, 0.15],
    )
    prices_kes = {
        "Smartphone": 15000,
        "Wireless Headphones": 3500,
        "Laptop": 55000,
        "Smart TV": 35000,
        "Soundbar": 8000,
    }
    return pd.DataFrame(
        {
            "order_id": [f"DK{i:05d}" for i in range(1, n_orders + 1)],
            "order_date": (
                pd.to_datetime("2026-01-01")
                + pd.to_timedelta(rng.integers(0, 181, n_orders), unit="D")
            ).strftime("%Y-%m-%d"),
            "branch": rng.choice(
                ["Nairobi", "Mombasa", "Kisumu", "Nakuru"],
                size=n_orders,
                p=[0.38, 0.24, 0.21, 0.17],
            ),
            "product_name": product_names,
            "quantity": rng.choice([1, 2, 3], size=n_orders, p=[0.72, 0.18, 0.10]),
            "unit_price_kes": pd.Series(product_names).map(prices_kes),
            "channel": rng.choice(
                ["In-Store", "Online"], size=n_orders, p=[0.52, 0.48]
            ),
        }
    )


if __name__ == "__main__":
    generate_student_performance().to_csv(
        PROJECT_DIR / "student_performance.csv", index=False
    )
    generate_duka_sales().to_csv(PROJECT_DIR / "duka_sales.csv", index=False)
    print("Generated student_performance.csv (500 rows) and duka_sales.csv (1,000 rows).")
