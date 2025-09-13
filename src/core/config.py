"""Central thresholds and constants. 
Keep numeric thresholds in one place so scoring is simple and auditable."""
#Scoring thresholds
SCORING_THRESHOLDS = {
    "population_growth_pct_min": 17.0,
    "median_household_income_usd_min": 50000,
    "income_growth_pct_min": 4.0,
    "unemployment_rate_pctmax": 4.2,
    "job_growth_pct_min": 0.75,
    "home_ownership_rate_pct_max": 60.0,
    "median_age_max": 36.0,
    "median_sale_price_usd_max": 300000,
    "median_yoy_sale_price_growth_pct_min": 4.0,
    "median_5yrs_sale_price_growth_pct_min": 5.0,
    "property_tax_rate_pct_max": 1.7,
    "average_insurance_rate_usd_max": 6000,
    "median_rent_usd_min": 1000,
    "rent_yoy_growth_pct_min": 1.3,
    "rent_5yrs_growth_pct_min": 5.0,
    "rent_to_income_ratio_pct_max": 30.0,
    "rent_to_price_ratio_pct_max": 0.36
}
