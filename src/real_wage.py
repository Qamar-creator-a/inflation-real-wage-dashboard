from __future__ import annotations
import pandas as pd

def to_real_income(
    nominal: pd.Series,
    cpi: pd.Series,
    base_date: str | pd.Timestamp,
) -> pd.Series:
    """
    Convert nominal income to real income in base_date dollars.

    nominal and cpi must share the same DatetimeIndex (monthly).
    """
    if not isinstance(nominal.index, pd.DatetimeIndex) or not isinstance(cpi.index, pd.DatetimeIndex):
            raise TypeError("nominal and cpi must have DatetimeIndex")

    aligned_nominal, aligned_cpi = nominal.align(cpi, join="inner")
    if aligned_nominal.empty:
        raise ValueError("No overlapping dates between nominal and cpi")

    base_date = pd.to_datetime(base_date)
    if base_date not in aligned_cpi.index:
        raise ValueError("base_date not found in CPI index")

    cpi_base = aligned_cpi.loc[base_date]
    return aligned_nominal * (cpi_base / aligned_cpi)

def inflation_yoy(cpi: pd.Series) -> pd.Series:
    """Year-over-year inflation rate from CPI (monthly series)."""
    if not isinstance(cpi.index, pd.DatetimeIndex):
        raise TypeError("cpi must have DatetimeIndex")
    return cpi.pct_change(12)
