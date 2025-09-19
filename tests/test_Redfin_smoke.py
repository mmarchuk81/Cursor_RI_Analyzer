# tests/test_redfin_smoke.py
import pandas as pd
from src.providers.redfin_client import RedfinClient


def test_redfin_compute_city_metrics_from_df_min():
    # Build a tiny monthly series with 61 rows so 12m and 60m lookups exist
    periods = 61
    dates = pd.date_range("2020-01-31", periods=periods, freq="M")

    # Make prices so:
    #   latest = 110
    #   12 months ago = 100  -> YoY = ((110-100)/100)*100 = 10.00
    #   60 months ago = 80   -> 5Y  = ((110-80)/80)*100  = 37.50
    prices = [80] + [90] * (periods - 13) + [100] * 12 + [110]
    prices = prices[:periods]

    df = pd.DataFrame({
        "region_type": ["city"] * periods,
        "region": ["Austin, TX"] * periods,
        "period_end": dates,
        "median_sale_price": prices,
        "inventory": [1500] * periods,   # use units; comment out to test months_of_supply fallback
        # "months_of_supply": [2.4] * periods,
    })

    out = RedfinClient().compute_city_metrics_from_df(df, "Austin", "TX")

    assert out["median_sale_price"] == 110.0
    assert out["yoy_price_growth"] == 10.00
    assert out["five_year_price_growth"] == 37.50
    assert out["housing_inventory"] == 1500.0


def test_redfin_missing_city_raises():
    df = pd.DataFrame({
        "region_type": ["city"],
        "region": ["Austin, TX"],
        "period_end": [pd.Timestamp("2025-08-31")],
        "median_sale_price": [500000],
        "inventory": [1200],
    })
    try:
        RedfinClient().compute_city_metrics_from_df(df, "Dallas", "TX")
        assert False, "Expected ValueError for missing city"
    except ValueError:
        assert True
