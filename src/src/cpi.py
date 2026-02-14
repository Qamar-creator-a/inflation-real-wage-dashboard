from fredapi import Fred

fred = Fred()  # reads FRED_API_KEY from environment

def get_cpi():
    # CPI-U (monthly index)
    cpi = fred.get_series("CPIAUCSL")
    cpi.name = "cpi"
    return cpi