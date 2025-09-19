from typing import Dict
import pandas as pd


class RedfinClient:
    """
    Fetches city-level housing metrics from Redfin's Data Center sources:
      - median_sale_price (USD)
      - yoy_price_growth (% as whole number, e.g., 5.2)
      - five_year_price_growth (% as whole number)
      - housing_inventory (number, e.g., units as of the month, or months_of_supply)
    """

    def __init__(self):
        pass

    def compute_city_metrics_from_df(self, df: pd.DataFrame, city: str, state: str) -> Dict[str, float]:
        """
        Compute latest Redfin metrics for a specific city/state (expects region like 'City, ST').

        Input schema (required columns):
          - region_type: must equal 'city' for the target rows
          - region: exact city label, e.g., 'Austin, TX'
          - period_end: date column used for latest/lag lookups
          - median_sale_price: numeric series used for YoY and 5Y growth

        Inventory column:
          - Prefer 'inventory' (units). If absent, fall back to 'months_of_supply' (proxy).
        """
        # Normalize columns just in case
        df = df.copy()
        df.columns = [c.strip().lower() for c in df.columns]

        target_region = f"{city}, {state.upper()}"
        df_city = df[(df["region_type"].str.lower() == "city") & (df["region"] == target_region)].copy()
        if df_city.empty:
            raise ValueError(f"Redfin rows not found for region '{target_region}'")

        # ensure date sorting
        df_city["period_end"] = pd.to_datetime(df_city["period_end"])
        df_city.sort_values("period_end", inplace=True)

        # latest values
        latest_row = df_city.iloc[-1]
        latest_price = float(latest_row["median_sale_price"])

        # Inventory: prefer absolute unit count; fallback to months_of_supply
        if "inventory" in df_city.columns:
            latest_inventory = float(latest_row["inventory"])  # units (homes)
        elif "months_of_supply" in df_city.columns:
            latest_inventory = float(latest_row["months_of_supply"])  # months (proxy, not units)
        else:
            raise ValueError("Inventory column not found: expected 'inventory' or 'months_of_supply'")

        # locate 12 and 60 months ago for YoY and 5Y growth
        def lookup_months_ago(months: int) -> float | None:
            target_date = latest_row["period_end"] - pd.DateOffset(months=months)
            # closest earlier or equal period
            prior = df_city[df_city["period_end"] <= target_date]
            if prior.empty:
                return None
            return float(prior.iloc[-1]["median_sale_price"])

        price_12 = lookup_months_ago(12)
        price_60 = lookup_months_ago(60)

        def pct_change(new: float, old: float | None) -> float:
            if old is None or old == 0:
                return 0.0
            return round(((new - old) / old) * 100.0, 2)

        yoy = pct_change(latest_price, price_12)
        fivey = pct_change(latest_price, price_60)

        return {
            "median_sale_price": latest_price,
            "yoy_price_growth": yoy,
            "five_year_price_growth": fivey,
            "housing_inventory": latest_inventory,
        }
