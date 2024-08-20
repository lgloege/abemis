"""stationary energy equations."""

import numpy as np

from .utils import convert_to_numpy


@convert_to_numpy
def combustion(a, ef):
    r"""Greenhouse gas emissions from stationary combustion.

    .. math::

        E = \sum_{fuel} A_{fuel} \cdot EF_{fuel}

    where fuel is coal, oil, natural gas, etc.

    Parameters
    ----------
    a : float
        activity, amount of fuel combusted
        units: Tj
    ef : float
        emission factor of a given GHG by type of fuel.
        For CO2, it includes the carbon oxidation factor, assumed to be 1.
        units: kg gas / TJ

    Returns
    -------
    float
        emissions of fuel by type
    """  # noqa: E501
    return np.sum(a * ef)

@convert_to_numpy
def grid_consumption(a, ef):
    r"""Greenhouse gas emissions from stationary grid energy consumption.

    .. math::

        E = A \cdot EF

    Parameters
    ----------
    a : float
        activity, amount of grid energy consumed
        units: Tj
    ef : float
        emission factor of a given GHG by the grid supply.
        For CO2, it includes the carbon oxidation factor, assumed to be 1.
        units: kg gas / TJ

    Returns
    -------
    float
        emissions of stationary energy consumption
    """  # noqa: E501
    return np.sum(a * ef)

