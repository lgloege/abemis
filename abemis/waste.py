"""waste activity-based emissions equations."""

import numpy as np

from .utils import convert_to_numpy
from .constants import Conversions

constants = Conversions()


@convert_to_numpy
def doc(A=0, B=0, C=0, D=0, E=0, F=0, *args, **kwargs):
    r"""Degradable organic carbon (DOC).

    Calculates total DOC from the fractional breakdown of municiple solid waste
    and its DOC content

    .. math::
        DOC = (0.15 \cdot A) + (0.2 \cdot B) + (0.4 \cdot C) + (0.43 \cdot D) + (0.24 \cdot E) + (0.15 \cdot F)

    Parameters
    ----------
    A : float:
        Fraction of solid waste that is food
    B : float:
        Fraction of solid waste that is garden waste and other plant debris
    C : float:
        Fraction of solid waste that is paper
    D : float:
        Fraction of solid waste that is wood
    E : float:
        Fraction of solid waste that is textiles
    F : float:
        Fraction of solid waste that is industrial waste

    Returns
    -------
    float
        degradable of organic carbon in municipal solid waste
        units: (tonnes C / tonnes waste)

    References
    ----------
    .. [1] World Resources Institute, C40 Cities Climate Leadership Group, and ICLEI -
        Local Governments for Sustainability. (2014).
        Chapter 8: Waste. In `Global Protocol for Community-Scale Greenhouse Gas Emission Inventories <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=96>`__.
        WRI, C40, and ICLEI.

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories Volume 5 Waste <https://www.ipcc-nggip.iges.or.jp/public/gp/english/5_Waste.pdf#page=9>`_

    .. [3]   `2006 IPCC Guidelines for National Greenhouse Gas Inventories Volume 5 Waste` <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/5_Volume5/V5_2_Ch2_Waste_Data.pdf#page=14>`_

    Notes
    -----
    * Followed Equation 8.1 in GPC version 7 [1]_
    * Equation adapted from Equation 5.4 in [2]_
    * Fractions from table 2.4 in [3]_
    """  # noqa: E501
    assert all(
        0 <= v <= 1 for v in [A, B, C, D, E, F]
    ), "All fractions should be between 0 and 1"

    # DOC content in wet waste (table 2.4 in "2006 IPCC Guidelines ...")
    # TODO: this could be moved to constants
    frac = {
        "food": 0.15,
        "garden": 0.2,
        "paper": 0.4,
        "wood": 0.43,
        "textiles": 0.24,
        "industrial": 0.15,  # unsure where GPC gets this value
    }

    doc = (
        (frac["food"] * A)
        + (frac["garden"] * B)
        + (frac["paper"] * C)
        + (frac["wood"] * D)
        + (frac["textiles"] * E)
        + (frac["industrial"] * F)
    )

    return doc


def _management_level_to_mcf(management_level: str, *args, **kwargs):
    """Methane correction factor (MCF) from management level.

    See Equation 8.4 in [1]_

    .. _mcf:

    Parameters
    ----------
    management_level : str
        one of the following:

        *  managed
        *  managed_well
        *  managed_poorly
        *  unmanaged_more5m
        * unmanaged_less5m
        * uncategorized

    Returns
    -------
    float
        methane correction factor
        Units: dimesionless

    References
    ----------
    .. [1] World Resources Institute, C40 Cities Climate Leadership Group, and ICLEI -
        Local Governments for Sustainability. (2014).
        Chapter 8: Waste. In `Global Protocol for Community-Scale Greenhouse Gas Emission Inventories <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=100>`__.
        WRI, C40, and ICLEI.
    """  # noqa: E501
    dic = {
        "managed": 1,
        "managed_well": 0.5,
        "managed_poorly": 0.7,
        "unmanaged_more5m": 0.8,
        "unmanaged_less5m": 0.4,
        "uncategorized": 0.6,
    }

    mcf = dic.get(management_level.lower())

    if mcf is None:
        raise Exception(f"Error: {management_level} not in {dic.keys()}")

    return mcf


@convert_to_numpy
def methane_generation_potential(
    mcf, doc, docf: float = 0.6, f: float = 0.5, *args, **kwargs
):
    r"""Methane Generation Potential.

    specifies the amount of methane generated per ton of solid waste

    .. math::

        L_o = MCF \cdot DOC \cdot DOC_F \cdot F \cdot CH4:C

    Parameters
    ----------
    mcf : float
        methane correction factor:
        see :ref:`management_level_to_mcf <mcf>`

        * managed = 1
        * managed well = 0.5
        * managed poorly = 0.7
        * unmanaged (>5m deep) = 0.8
        * unmanaged (<5m deep) = 0.4
        * uncategorized = 0.6

        Units: dimensionless

    doc : float
        Degradable organic carbon
        Units: (tonnes C / tonnes waste)

    docf : float
        Fraction of DOC that is ultimately degraded.
        Reflects that some carbon does not degrade
        Assumed equal to 0.6
        Units: dimensionless

    f : float
        fraction of methane in landfill gas
        Default range 0.4-0.6 (usually taken to be 0.5)
        Units: dimensionless


    Returns
    -------
    float
        Methane generation potential
        Units: tonnes of CH4

    References
    ----------
    .. [1] Equation 8.4 in `GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=100>`_
    """  # noqa: E501
    CH4_TO_C = constants.CH4_to_C.value
    return mcf * doc * docf * f * CH4_TO_C


def _management_level_to_oxidation_factor(management_level: str, *args, **kwargs):
    """Oxidation factor from management level.

    Parameters
    ----------
    management_level : str
        one of the following:

        * managed
        * managed_well
        * managed_poorly
        * unmanaged_more5m
        * unmanaged_less5m
        * uncategorized

    Returns
    -------
    float
        oxidation factor
        Units: dimensionless
    """  # noqa: E501
    dic = {
        "managed": 0.1,
        "managed_well": 0.1,
        "managed_poorly": 0.1,
        "unmanaged_more5m": 0,
        "unmanaged_less5m": 0,
        "uncategorized": 0,
    }

    ox = dic.get(management_level.lower())

    if ox is None:
        raise Exception(f"Error: {management_level} not in {dic.keys()}")

    return ox


@convert_to_numpy
def methane_commitment(msw, lo, frec, ox, *args, **kwargs):
    r"""Methane commitment (MC) estimate for solid waste sent to landfill.

    MC assigns landfill emissions based on waste disposed in a given year.
    It takes a lifecycle and mass-balance approach and calculates landfill
    emissions based on the amount of waste disposed in a given year,
    regardless of when the emissions actually occur.
    A portion of emissions are released every year after the waste is disposed.

    .. math::
        CH_4 = MSW \cdot L_o \cdot (1 - f_{ref}) \cdot (1 - OX)

    Parameters
    ----------
    msw: float
        mass of solid waste (MSW) sent to landfill
        Units: Metric tonnes

    lo: float
        methane generation potential
        Units: dimensionless

    frec: float
        Fraction of methane recovered at the landfill
        (flared or energy recovery)
        Units: dimensionless

    ox: float
        oxidation factor

        * 0.1 for well-managed landfills (see [1]_)
        * 0 for unmanaged landfills (see [1]_)

        Units: dimensionless

    Returns
    -------
    float
        methane emissions
        Units: Tonnes CH4

        asdfasdf


    References
    ----------
    .. [1] `Equation 8.3 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=99>`_
    """  # noqa: E501
    assert 0 <= frec <= 1, "frec must be between 0 and 1"
    assert 0 <= ox <= 1, "oxidation factor (ox) must be between 0 and 1"

    return msw * lo * (1 - frec) * (1 - ox)


def _biological_treatment_ef(treatment, gas, wet_or_dry):
    """Biological treatment emissions factor.

    Parameters
    ----------
    treatment : str
        treatment type, either compoosting or anaerobic_digestion

    gas : str
        gas either ch4 or n2o

    wet_or_dry : str
        wet or dry emission factor

    Returns
    -------
    float
        emission factor
        Units: (grams of gas / kilograms of waste)

    References
    ----------
    .. [1] `Table 8.3 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=101>`_
    .. [2] original source: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 5, Chapter 4: Biological Treatment of Solid Waste
    """  # noqa: E501
    treatment = treatment.lower()
    gas = gas.lower()
    wet_or_dry = wet_or_dry.lower()

    assert treatment in [
        "composting",
        "anaerobic_digestion",
    ], "treatment must be either composting or anaerobic_digestion"
    assert gas in ["ch4", "n2o"], "gas must be either ch4 or n2o"
    assert wet_or_dry in ["wet", "dry"], "wet_or_dry must be either wet or dry"

    efs = {
        "composting": {"ch4": {"dry": 10, "wet": 4}, "n2o": {"dry": 0.6, "wet": 0.24}},
        "anaerobic_digestion": {
            "ch4": {
                "dry": 2,
                "wet": 0.8,
            },
            "n2o": {"dry": None, "wet": None},
        },
    }

    return efs.get(treatment).get(gas).get(wet_or_dry)


@convert_to_numpy
def incineration_co2(m, wf, dm, cf, fcf, of):
    r"""non-biogenic CO2 emissions from incineration of waste.

    .. math::

        E = m \cdot \sum_i (WF_i \cdot dm_i \cdot CF_i \cdot FCF_i \cdot OF_i) \cdot CO2:C

    where i is the type of the Solid Waste incinerated such as paper/cardboard,
    textile, food waste, etc.

    Parameters
    ----------
    m : float
        mass of waste incinerated
    wf : float
        fraction of waste of type
    dm : float
        dry matter content of type
    cf : float
        fraction of carbon in dry matter of type
    fcf : float
        fraction of fossil carbon in total carbon component of type
    of : float
        oxidiation fraction or factor

    Returns
    -------
    float
        Total CO2 emissions from incineration of solid waste in tonnes

    References
    ----------
    .. [1] `Equation 8.6 in GPC version 1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=102>`_
    """  # noqa: E501
    # TODO: add assertion that sum(WF) == 1
    EF = wf * dm * cf * fcf * of
    C_to_CO2 = constants.C_to_CO2.value
    return m * EF * C_to_CO2


@convert_to_numpy
def incineration_ch4(IW, EF):
    r"""CH4 emissions from incineration.

    .. math::

        E = \sum_i IW_i \cdot EF_i

    where i is the category or type of waste incinerated/open-burned,
    specified as follows:

    * MSW: municipal solid waste
    * ISW: industrial solid waste
    * HW: hazardous waste
    * CW: clinical waste
    * SS: sewage sludge
    * others (that must be specified)

    Parameters
    ----------
    IW : float
       Amount of solid waste of type i incinerated or open-burned, in tonnes
    EF : float
       Aggregate CH4 emission factor, g CH4/ton of waste type i

    Returns
    -------
    float
       CH4 emissions in inventory year, in tonnes

    References
    ----------
    .. [1] `Equation 8.7 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=103>`_
    """  # noqa: E501
    g_to_tonnes = constants.g_to_tonne.value
    return IW * EF * g_to_tonnes


@convert_to_numpy
def incineration_n2o(IW, EF):
    r"""N2O emissions from incineration.

    .. math::

        E = \sum_i IW_i \cdot EF_i

    where i is the category or type of waste incinerated/open-burned,
    specified as follows:

    * MSW: municipal solid waste
    * ISW: industrial solid waste
    * HW: hazardous waste
    * CW: clinical waste
    * SS: sewage sludge
    * others (that must be specified)

    Parameters
    ----------
    IW : float
       Amount of solid waste of type i incinerated or open-burned, in tonnes
    EF : float
       Aggregate N2O emission factor, g CH4/ton of waste type i

    Returns
    -------
    float
       N2O emissions in inventory year, in tonnes

    References
    ----------
    .. [1] `Equation 8.8 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=105>`_
    """  # noqa: E501
    g_to_tonnes = constants.g_to_tonne.value
    return IW * EF * g_to_tonnes


@convert_to_numpy
def fod(msw, lo, r, ox, k, inventory_year):
    r"""First Order Decay (FOD) model for solid waste CH4 emissions.

    .. math::

        E =  \bigg\{ \sum_x \big[ MSW_x \cdot Lo_x \cdot (1 - \exp^{-k}) \cdot \exp^{-k(t-x)} \big]  - R(t) \bigg\}  \cdot (1-OX)

    Parameters
    ----------
    msw : float
        Total municipal solid waste disposed at solid waste disposal site
        in year x in tonnes
    lo : float
        Methane generation potential
    r : float
        Methane collected and removed (ton) in inventory year
    ox : float
        Oxidation factor

        * 0.1 for well-managed landfills
        * 0 for unmanaged landfills

    k : float
        Methane generation rate constant, which is related to the
        time taken for the DOC in waste to decay to half its initial mass
        (half-life)
    inventory_year : float
        Inventory year

    Returns
    -------
    float
        CH4 emissions

    References
    ----------
    .. [1] `Equation 8.2 from GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=99>`_
    .. [2] Based on `Equation 6 in CH4 emissions from solid waste disposal <https://www.ipcc-nggip.iges.or.jp/public/gp/bgp/5_1_CH4_Solid_Waste.pdf#page=5>`_
    """  # noqa: E501
    if isinstance(msw, np.ndarray):
        num_years = msw.size
    elif isinstance(msw, (list, tuple)):
        num_years = len(msw)
    else:
        msw_list = [msw]
        num_years = len(msw_list)

    years = np.arange(inventory_year - num_years + 1, inventory_year + 1)

    exp_term = np.exp(-k * (inventory_year - years))
    sum_term = np.sum(msw * lo * (1 - np.exp(-k)) * exp_term)

    emissions = (sum_term - r) * (1 - ox)

    return emissions


@convert_to_numpy
def tow(p, bod, i):
    r"""Total organics in wastewater.

    .. math::

        TOW = P \cdot BOD \cdot I \cdot 365

    Parameters
    ----------
    p : float
        population in inventory year
    bod : float
        city-specific per capita BOD in inventory year,
        units: g/person/day

    i : float
        Correction factor for additional industrial BOD discharged into sewers

        In the absence of expert judgment,
        GPC suggests the following default values:

        * 1.25 for collected wastewater
        * 1.00 for uncollected

    Returns
    -------
    float
       For domestic wastewater: total organics in wastewater in inventory year,
       units: kg BOD/yr

    References
    ----------
    .. [1] `Equation 8.11 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=108>`_
    """  # noqa: E501
    days_in_year = constants.year_to_days
    return p * bod * i * days_in_year


@convert_to_numpy
def wasterwater_ch4_ef(B, MCF, U, T):
    r"""Wastewater CH4 emissions factor.

    .. math::

        EF = B \cdot MCF_j \cdot U_i \cdot T_{i,j}

    where i is the income group and j is the treatment/discharge pathway
    or system.

    Parameters
    ----------
    B : float
        Maximum CH4 producing capacity
        default values:

        * 0.6 kg CH4/kg BOD
        * 0.25 kg CH4/kg COD

    MCF : float
        Methane correction factor (fraction)
    U : float
        Fraction of population in income group i in inventory year
    T : float
        Degree of utilization (ratio) of treatment/discharge pathway or system,
        j, for each income group fraction i in inventory year

    Returns
    -------
    float
       Emission factor for each treatment and handling system

    References
    ----------
    .. [1] `Equation 8.11 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=108>`_
    """  # noqa: E501
    return B * MCF * U * T


@convert_to_numpy
def wastewater_ch4(tow, s, ef, r):
    r"""CH4 emissions from wastewater.

    .. math::

        E = [(TOW - S) \cdot EF - R] \cdot tonne:kg


    Parameters
    ----------
    TOW : float
        Organic content in the wastewater
        For domestic wastewater: total organics in wastewater in inventory year, kg BOD/yrNote 1 For industrial wastewater:
        total organically degradable material in wastewater from industry i in inventory year, kg COD/yr
    EF : float
        Emission factor kg CH4 per kg BOD or kg CH4 per kg CODNote 2
    S : float
        Organic component removed as sludge in inventory year, kg COD/yr or kg BOD/yr
    R : float
        Amount of CH4 recovered in inventory year, kg CH4/yr

    Returns
    -------
    float
       Total CH4 emissions
       units: metric tonnes

    References
    ----------
    .. [1] `Equation 8.9 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=107>`_
    """  # noqa: E501
    kg_to_tonnes = constants.kg_to_tonne.value
    E_kg = (tow - s) * ef - r
    E_tonnes = E_kg * kg_to_tonnes
    return E_tonnes


@convert_to_numpy
def wastewater_n2o_indirect(P, protein, Fnrp, Fnon, Find, N, EF):
    r"""Indirect N2O emissions from wastewater.

    .. math::

        E = [(P \cdot protein \cdot F_{NRP} \cdot  F_{NON-CON} \cdot F_{IND-CON}) - N_{sludge}] \cdot EF \cdot conversion

    Parameters
    ----------
    P : float
        Total population served by the water treatment plant
    protein: float
        Annual per capita protein consumption, kg/person/yr
    F_nrp : float
        Factor to adjust for non-consumed protein
        1.1 for countries with no garbage disposals,
        1.4 for countries with garbage disposals
    F_non-con : float
        Fraction of nitrogen in protein
        default: 0.16, kg N/kg protein
    F_ind-con : float
        Factor for industrial and commercial co-discharged protein into
        the sewer system
        deafult:

        * 1.25 Centralized systems
        * 0 Decentralized systems

    N : float
        Nitrogen removed with sludge,
        units: kg N / yr
        default: 0
    EF : float
        Emission factor for N2O emissions from discharged to wastewater
        units = kg N2O-N per kg N2O

    Returns
    -------
    float
       Emission factor for each treatment and handling system

    References
    ----------
    .. [1] `Equation 8.12 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=109>`_
    """  # noqa: E501
    N_to_N2O = constants.N_to_N2O.value
    kg_to_tonnes = constants.kg_to_tonne.value
    return ((P * protein * Fnrp * Fnon * Find) - N) * EF * N_to_N2O * kg_to_tonnes
