import pandas as pd
from src.real_wage import to_real_income, inflation_yoy

def test_to_real_income_base_month_equals_nominal():
    idx = pd.to_datetime(["2024-01-01", "2024-02-01"])
    nominal = pd.Series([1000, 1000], index=idx)
    cpi = pd.Series([200, 220], index=idx)

    real = to_real_income(nominal, cpi, "2024-01-01")
    assert real.loc["2024-01-01"] == 1000
    # Feb real should be lower because CPI higher
    assert abs(real.loc["2024-02-01"] - (1000 * (200/220))) < 1e-9

def test_inflation_yoy():
    idx = pd.date_range("2023-01-01", periods=13, freq="MS")
    cpi = pd.Series(range(100, 113), index=idx)  # 100..112
    yoy = inflation_yoy(cpi)
    # At month 13: (112/100)-1
    assert abs(yoy.iloc[-1] - (112/100 - 1)) < 1e-9
