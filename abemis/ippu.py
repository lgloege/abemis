from .constants import Conversions
constants = Conversions()

from .utils import convert_to_numpy

@convert_to_numpy
def cement_production(M, EF):
    """CO2 emissions from cement production

    .. math::

        E = M \\cdot EF

    Parameters
    ----------
    M : float
        Weight (mass) of clinker produced
        Units: metric tonnes

    EF : float
        Emission factor
        units: CO2 / tonne clinker

    Returns
    --------
    float
        CO2 emissions in tonnes

    References
    -----
    .. [1] `Equation 9.2 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=114>`_
    """
    #  Link to default emission factor calculation:
    # 2.2.1.2 of Page 2.11 from Chapter 2 of Volume 3 of 2006 IPCC Guidelines for National Greenhouse Gas Inventories
    return M*EF


convert_to_numpy
def lime_production(M, EF):
    """CO2 emissions from lime production

    .. math::

        E = \\sum_i M_i \\cdot EF_i

    where i is the type of lime

    Parameters
    ----------
    M : float
        Weight (mass) of lime produced of lime type i
        units: metric tonnes
    EF : float
        emission factor, CO2 per mass unit of lime produced of lime type i
        units: CO2 / tonne lime

    Returns
    --------
    float
        CO2 emissions in tonnes

    References
    ----------
    .. [1] `Equation 9.3 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=114>`_
    """
    #   Link to default emission factor calculation:
    #  Table 2.4 of Page 2.22 from Chapter 2 of Volume 3 of 2006 IPCC Guidelines for National Greenhouse Gas Inventories
    return M*EF


convert_to_numpy
def glass_production(M, EF, CR):
    """CO2 emissions from glass production

    .. math::

        E = \\sum_i M_i \\cdot EF_i \\cdot (1 - CR_i)

    where i is the type of glass

    Parameters
    ----------
    M : float
        Mass of melted glass of type i (e.g., float, container, fiber glass, etc.),
        units: tonnes
    EF : float
        Emission factor for manufacturing of glass of type i,
        units:  tonnes CO2 / tonne glass melted
    CR : float
        Cullet ratio for manufacturing of glass of type i
        Cullet ratio is the fraction of the furnace charge represented by cullet.

    Returns
    --------
    float
        CO2 emissions in tonnes

    References
    ----------
    .. [1] `Equation 9.4 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=114>`_
    """
    # link to default emission factor calculation
    # Table 2.6 of Page 2.30 from Chapter 2 of Volume 3 of 2006 IPCC Guidelines for National Greenhouse Gas Inventories
    return M*EF*(1-CR)


convert_to_numpy
def non_energy_product_use(NEU, CC, ODU):
    """CO2 emissions from non-energy product use

    .. math::

        E = \\sum_i (NEU_i \\cdot CC_i \\cdot ODU_i) \\cdot CO2:C


    Parameters
    ----------
    NEU : float
        non-energy use of fuel i
        units: TJ
    CC : float
        specific carbon content of fuel i,
        units: tonne C / TJ (equivalent to kg C / GJ)
    ODU : float
        Fracion of fuel oxidized during use
        units: dimensionless

    Returns
    --------
    float
        CO2 emissions
        units: tonnes

    References
    ----------
    .. [1] `Equation 9.5 in GPC version 7 <https://ghgprotocol.org/sites/default/files/standards/GPC_Full_MASTER_RW_v7.pdf#page=118>`_
    """
    # Source: Equation adapted from 2006 IPCC Guidelines for National Greenhouse Gas Inventories Volume 3 Industrial Processes and Product Use available at:
    # www.ipcc-nggip.iges.or.jp/public/2006gl/vol3.html
    CO2_to_C = constants.C_to_CO2.value
    return NEU*CC*ODU * CO2_to_C