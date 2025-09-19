from src.metrics import CalculatedMetrics as CM, HousingMarket

def test_calculated_metrics_basic():
    #rent-to-price(monthly): 2000/30000*100 = 0.666...->0.67
    assert CM.rent_to_price_ratio(2000,300000) == 0.67
    #rent-to-income(annualized): 2000 *12/90000 *100 = 30.0 
    assert CM.rent_to_income_ratio(2000,80000) == 30.00

def test_calculated_metrics_edges():
    assert CM.rent_to_price_ratio(2000,0) == 0.0
    assert CM.rent_to_income_ratio(2000,0) == 0.0

def test_housingmarket_constructs():
    hm = HousingMarket (
        median_sale_price = 300000, 
        average_insurance = 2500,
        median_rent = 2000,
        yoy_price_growth = 4.25,
        five_year_price_growth = 6.2,
        property_tax_rate= 1.7,
        yoy_rent_growth=18.4,
        housing_inventory=2.5,
    )
    assert hm.median_sale_price == 300000
    assert hm.rent_to_price_ratio is None
    assert hm.rent_to_income_ratio is None
    