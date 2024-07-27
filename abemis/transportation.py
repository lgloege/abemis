def asif_framework(
    a: float,
    s: float,
    i: float,
    f: float) -> float:
    """ASIF framework for transportation emissions

    .. math::
        E = A*S*I*F

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
    ------
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
    """

    return a * s * i * f