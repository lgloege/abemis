"""Emission factor database."""

import pandas as pd
from pathlib import Path


def waste(region: str = None, gas: str = None, search: str = None, *args, **kwargs):
    """Get waste emission factors.

    Parameters
    ----------
    region : str, optional
        Full name of region (e.g. "United States of America"), by default None
    gas : str, optional
        full name of gas (e.g. "methane"), by default None
    search : str, optional
        phrase to search for in the description, by default None

    Returns
    -------
    pd.DataFrame
        pandas dataframe of emission factors
    """
    script_dir = Path(__file__).parent
    file_path = script_dir / "efdb" / "EFDB_waste.xlsx"

    df = pd.read_excel(file_path)

    if region:
        df = df.loc[df["Region / Regional Conditions"] == region]

    if gas:
        df = df.loc[df["Gas"] == gas.upper() + "\n"]

    if search:
        df = df.loc[df["Description"].str.contains(search, na=False)]

    return df


def ippu(region: str = None, gas: str = None, search: str = None, *args, **kwargs):
    """Get ippu emission factors.

    Parameters
    ----------
    region : str, optional
        Full name of region (e.g. "United States of America"), by default None
    gas : str, optional
        full name of gas (e.g. "methane"), by default None
    search : str, optional
        phrase to search for in the description, by default None

    Returns
    -------
    pd.DataFrame
        pandas dataframe of emission factors
    """
    script_dir = Path(__file__).parent
    file_path = script_dir / "efdb" / "EFDB_ippu.xlsx"

    df = pd.read_excel(file_path)

    if region:
        df = df.loc[df["Region / Regional Conditions"] == region]

    if gas:
        df = df.loc[df["Gas"] == gas]

    if search:
        df = df.loc[df["Description"].str.contains(search, na=False)]

    return df
