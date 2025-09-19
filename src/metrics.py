from dataclasses import dataclass
from typing import Optional


@dataclass
class HousingMarket:
    # USD
    median_sale_price: float

    # percents (whole-number percents, e.g., 5.2 means 5.2%)
    yoy_price_growth: float
    five_year_price_growth: float
    property_tax_rate: float

    # numeric, units (e.g., months of supply or unit count)
    housing_inventory: float

    # USD
    average_insurance: float
    median_rent: float

    # percents (whole-number percents)
    yoy_rent_growth: float
    five_year_rent_growth: float

    # calculated based on data from this module and Market Fundamentals module
    rent_to_price_ratio: Optional[float] = None
    rent_to_income_ratio: Optional[float] = None


class CalculatedMetrics:
    """Holds pure calculation helpers that return whole-number percents. Example: returns 7.5 for 7.5%."""

    @staticmethod
    def rent_to_income_ratio(median_rent: float, median_household_income: float) -> float:
        """
        Annualized rent-to-income percentage:
        (median_rent * 12) / median_household_income * 100
        """
        if median_household_income <= 0:
            return 0.0
        annual_rent = median_rent * 12.0
        return round((annual_rent / median_household_income) * 100.0, 2)

    @staticmethod
    def rent_to_price_ratio(median_rent: float, median_sale_price: float) -> float:
        """
        Monthly rent-to-price percentage:
        median_rent / median_sale_price * 100
        """
        if median_sale_price <= 0:
            return 0.0
        return round((median_rent / median_sale_price) * 100.0, 2)
