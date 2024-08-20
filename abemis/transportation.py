"""Transportation equations."""

import numpy as np

from .utils import convert_to_numpy


@convert_to_numpy
def asif_framework(a: float, s: float, i: float, f: float) -> float:
    r"""ASIF framework for transportation emissions.

    .. math::
        E = A \cdot S \cdot I \cdot F

    See Chapter 7 of the GHG Protocol for Cities ([1]_) for more details

    Parameters
    ----------
    a : float
       activity (e.g. vehicle kilometers traveled).
       This may be different for different modes of transportation
    s : float
        mode share, this is the portion of trips taken by different modes of transportation
    i : float
        energy intensity by mode, (e.g. energy consumed per vehicle kilometer)
    f : float
        fuel factor, primarily based on the composition of the local fuel stock [2]_ [3]_

    Returns
    -------
    float
        transportation emissions (E)

    References
    ----------
    .. [1] World Resources Institute, C40 Cities Climate Leadership Group, and ICLEI -
        Local Governments for Sustainability. (2014).
        Chapter 7: Transportation. In `Global Protocol for Community-Scale Greenhouse Gas Emission Inventories <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=80>`__.
        WRI, C40, and ICLEI.

    .. [2] Cooper, E., Jiang X., Fong W. K., Schmied M., and GIZ.
        Scoping Study on Developing a Preferred Methodology and Tool to Estimate Citywide Transport Greenhouse Gas Emissions,
        unpublished, 2013
    .. [3] Schipper, L., Fabian, H., & Leather, J.
        Transport and Carbon Dioxide Emissions: Forecasts, Options Analysis, and Evaluation. 2009.
        https://www.adb.org/publications/transport-and-carbon-dioxide-emissions-forecasts-options-analysis-and-evaluation
    """  # noqa: E501
    return a * s * i * f


@convert_to_numpy
def fuel_sales(quantity: float, ef: float) -> float:
    r"""Emissions from fuel sales.

    .. math::

        E = \sum_{fuel} Q_f \cdot EF_f

    Parameters
    ----------
    quantity : float
        amount of fuel sold in the year
    ef : float
        emission factor for fuel

    Returns
    -------
    float
        transportation emissions (E)

    References
    ----------
    .. [1] `2006 IPCC Guidelines for National Greenhouse Gas Inventories Volume 2 Energy: Chapter 3 Mobile Combustion <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_3_Ch3_Mobile_Combustion.pdf#page=25>`_

    .. [2] Kennedy, Christopher, et al.
        "Methodology for inventorying greenhouse gas emissions from global cities."
        Energy policy 38.9 (2010): 4828-4837. doi: `10.1016/j.enpol.2009.08.050 <doi.org/10.1016/j.enpol.2009.08.050>`_
    """  # noqa: E501
    return np.sum(quantity * ef)

@convert_to_numpy
def electricity_charged(a, ef):
    r"""Greenhouse gas emissions from transport grid energy consumption.

    .. math::

        E = A \cdot EF

    Parameters
    ----------
    a : float
        activity, amount of electricity charged by transportation modes
        units: Tj
    ef : float
        emission factor of a given GHG by the grid supply.
        For CO2, it includes the carbon oxidation factor, assumed to be 1.
        units: kg gas / TJ

    Returns
    -------
    float
        emissions of transport grid energy consumption
    """  # noqa: E501
    return np.sum(a * ef)