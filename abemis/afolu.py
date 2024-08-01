import numpy as np

from .utils import convert_to_numpy
from .constants import Conversions
constants = Conversions()

@convert_to_numpy
def enteric_fermentation_ch4(N, EF):
    """CH4 emissions from enteric fermentation

    .. math::

        CH4 = \\sum_t N_t \\cdot EF_t \\cdot tonne:kg

    where t is the livestock category

    Parameters
    ----------
    N : float
        Number of animals (head)
    EF : float
        Emission factor for enteric fermentation
        units: kg / head / year

    Returns
    --------
    float
        CH4 emissions in tonnes

    References
    ----------
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=125>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 10: Emissions from livestock and manure management <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf#page=28>`_
    """
    kg_to_tonnes = constants.kg_to_tonne.value
    return N * EF * kg_to_tonnes

@convert_to_numpy
def manure_management_ch4(N, EF):
    """CH4 emissions from manure management

    .. math::

        CH4 = \\sum_t N_t \\cdot EF_t \\cdot tonne:kg

    where t is the livestock category

    Parameters
    ----------
    N : float
        Number of animals for each livestock category
    EF : float
        Emission factor for manure management
        units: kg / head / year

    Returns
    --------
    float
        CH4 emissions
        units: tonnes

    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=126>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 10: Emissions from livestock and manure management <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf#page=37>`_
    """
    kg_to_tonnes = constants.kg_to_tonne.value
    return N * EF * kg_to_tonnes

@convert_to_numpy
def manure_management_n2o(N, NEX, MS, EF):
    """N2O emissions from manure management

    .. math::

        N2O = \sum_t (N_t \cdot NEX_t \cdot MS_t) \cdot EF_t \cdot tonne:kg

    where t is the livestock category.

    .. note::

        this also requires a sum across the different manure management systems (MMS)

    Parameters
    ----------
    N : float
        Number of animals for each livestock category
    EF : float
        Emission factor for direct N2O-N emissions from MMS,
        units: kg N2O-N / kg N in MSS
    NEX : float
        Annual nitrogren excretion for livestock category T, kg N per animal per year (see Equation 10.4)
    MS : float
        Fraction of total annual nitrogen excretion managed in MMS for each livestock category

    Returns
    --------
    float
        N2O emissions in tonnes

    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=127>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 10: Emissions from livestock and manure management <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf#page=54>`_
    """
    N_to_N2O = constants.N_to_N2O.value
    kg_to_tonnes = constants.kg_to_tonne.value

    return (N*NEX*MS) * EF * N_to_N2O * kg_to_tonnes

@convert_to_numpy
def nex(N, TAM):
    """Annual N excretion rates

    .. math::

        Nex = \\sum_t  N_t \\cdot TAM_t

    where t is the livestock category

    Parameters
    ----------
    N : float
       Default N excretion rate
       units: kg N / tonne animal / day
    TAM : float
        Typical animal mass for livestock category T, kg per animal

    Returns
    --------
    float
       Annual N excretion for livestock category T
       units: kg N / animal / year

    Notes
    -----
    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=127>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 10: Emissions from livestock and manure management <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf#page=57>`_
    """
    kg_to_tonne = constants.kg_to_tonne.value
    days_in_year = constants.year_to_days.value
    return N * TAM * kg_to_tonne * days_in_year


@convert_to_numpy
def delta_c(FL, CL, GL, WL, SL, OL):
    """Changes in ecosystem C stocks

    .. math::

        \\Delta C_{afolu} = \sum_{category} \\Delta C_{category}

    where the categories are:

    * forest land
    * crop land
    * grassland
    * wetland
    * settlement
    * other lands

    Parameters
    ----------
    FL : float
       forest land
    CL : float
        crop land
    GL : float
        grass land
    WL : float
        wetlands
    SL : float
        settlements
    OL : float
        other lands

    Returns
    --------
    float
       Total annual carbon stock change
       units: tonnes CO2 / year


    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=129>`_

    .. [2] `2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 2: generic methodologies applicable to multiple land-use categories
        <https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch02_Generic%20Methods.pdf#page=7>`_
    """
    C_to_CO2 = 44/12
    AFOLU = FL + CL + GL + WL + SL + OL
    return AFOLU * C_to_CO2


@convert_to_numpy
def biomass_burning(A, B, CF, EF):
    """emissions from biomass burning

    .. math::

        E = A \\cdot M_b \\cdot CF \\cdot EF \\cdot kg:g

    Parameters
    ----------
    A : float
        Area of burnt land
        units: hectares
    B : float
        Mass of fuel available for combustion. This includes biomass, ground litter and dead wood.
        NB The latter two may be assumed to be zero except where this is a land-use change.
        units: tonnes / hectare
    CF : float
        Combustion factor (a measure of the proportion of the fuel that is actually combusted)
        units: dimensionless
    EF : float
       Emission factor
       units: g GHG / kg of dry matter burnt

    Returns
    --------
    float
       emissions
       units: tonnes of gas

    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=130>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 2: generic methodologies applicable to multiple land-use categories
        <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_02_Ch2_Generic.pdf#page=42>`_

    Notes
    -----

    * GPC [1]_ states this is GHG emissions in CO2-equivalent units and the IPCC [2]_ uses
     a different emission factor for each gas. We suggest following the IPCC
    """
    # TODO: put this in constants
    # this this converts EF so units are in tonnes in end
    g_to_kg = 0.001
    return A  * B * CF * EF * g_to_kg

@convert_to_numpy
def liming(M, EF):
    """CO2 emissions from liming

    .. math::

        CO2 = \\sum_t (M_t * EF_t) * CO2:C

    where t is the limestone or dolomite

    Parameters
    ----------
    M : float
        Amount of calcic limestone (CaCO3) or dolomite (CaMg(CO3)2)
        units: tonnes / year
    EF : float
        Emission factor
        units: tonne of C / tonne of stone

    Returns
    --------
    float
       CO2 emissions in tonnes

    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=130>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 11: N2O emissions from managed soils, and CO2 emissions from lime and urea application
        <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf#page=27>`_
    """
    C_to_CO2 = constants.C_to_CO2.value
    return M * EF * C_to_CO2

@convert_to_numpy
def urea_fertilization(M, EF):
    """CO2 emissions from urea application

    .. math::

        CO2 = \\sum_t (M_t * EF_t) * CO2:C

    Parameters
    ----------
    M : float
        Amount of urea fertilization
        units: tonnes urea / year
    EF : float
        Emission factor
        units: tonne of C / tonne of urea

    Returns
    --------
    co2: float
       CO2 emissions
       units: tonnes

    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=131>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 11: N2O emissions from managed soils, and CO2 emissions from lime and urea application
        <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf#page=32>`_
    """
    C_to_CO2 = constants.C_to_CO2.value
    return M * EF * C_to_CO2

@convert_to_numpy
def manure_management_n2o_indirect(n, nex, ms, frac, ef):
    """ Indirect N2O emissions due to volatilization of N from manure management

    Parameters
    ----------
    N : float
        Number of head of livestock per
    NEX : float
        Average N excretion per head of livestock category T, kg N per animal per year
    MS : float
        Fraction of total annual N excretion for each livestock category T that is managed in manure management system S
    frac : float
        Percent of managed manure nitrogen for livestock category T that volatilizes
        as NH3 and NOx in the manure management system S, %
    EF : float
        Emission factor for N2O emissions from atmospheric deposition of N on soils and water surfaces,
        kg N2O-N per kg NH3-N and NOx-N volatilized


    Returns
    --------
    float
        Indirect N2O emissions due to volatilization of N from manure management in tonnes

    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=137>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 10: Emissions from livestock and manure management <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_10_Ch10_Livestock.pdf#page=56>`_
    """
    # Nv: Amount of manure nitrogen that is lost due to volatilization of NH3 and NOx,
    # units: kg N per year.
    Nv = np.sum(n * nex * ms) * frac
    kg_to_tonne = constants.kg_to_tonne.value
    N_to_N2O = constants.N_to_N2O.value
    return Nv * ef * kg_to_tonne * N_to_N2O

@convert_to_numpy
def rice_cultivation_ch4(EF, T, A):
    """CH4 emissions from rice cultivation

    .. math::

        CH4 = t \\cdot A \\cdot EF \\cdot tonnes:kg

    .. note:

        You may need to sum across different ecosystems,
        water regimes, type and amount of organic amendments,
        and other conditions under which CH4 emissions from rice may vary

    Parameters
    ----------
    EF : float
        Daily emission factor
        units: kg CH4 / hectare / year
    t : float
        Cultivation period in days
        units: days
    A : float
        Harvested area
        units: hectares / year

    Returns
    --------
    float
       Methane emissions from rice cultivation
       units: Gg CH4 / year (note that a Gg == 1000 tonnes)

    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=138>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 5: Cropland <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_05_Ch5_Cropland.pdf#page=45>`_
    """
    kg_to_Gg = constants.kg_to_Gg.value
    return EF * T * A * kg_to_Gg

def _managed_soils_direct_n2o(inputs, os, prp):
    """ Indirect N2O emissions due to volatilization of N from manure management

    Parameters
    ----------
    inputs: float
        Direct N2O-N emissions from N inputs to managed soils, kg N2O-N per year
    os: float
        Direct N2O-N emissions from managed inorganic soils, kg N2O-N per year
    prp: float
         Direct N2O-N emissions from urine and dung inputs to grazed soils, kg N2O-N per year


    Returns
    --------
    float
        Direct N2O emissions produced from managed soils, in tonnes

    References
    -----
    .. [1] `GPC Version 1.1 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=132>`_

    .. [2] `2006 IPCC Guidelines for National Greenhouse Gas Inventories, Chapter 11: N2O emissions from managed soils, and CO2 emissions from lime and urea application
        <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_11_Ch11_N2O&CO2.pdf#page=7>`_
    """
    #TODO: implement this function and follow IPCC instead of GPC
    raise NotImplementedError("This function is not implemented yet.")

