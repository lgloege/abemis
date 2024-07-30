Getting Started
===============

This package is to facilitate calculating activity-based emissions.
The package is based on the `GHG Protocol for Cities <https://ghgprotocol.org/ghg-protocol-cities>`_.

Here we will go through the different calculations that can be made for each sector.

Stationary Energy
-----------------

Emissions from Stationary Energy sources are calculated
by multiplying fuel consumption (:math:`FC`) by
the corresponding emission factors (:math:`EF`) for each fuel:

.. math::

    E = \sum_{fuel} FC_{fuel} \cdot EF_{fuel}

**Python Code**

.. code-block:: Python

    abemis.stationary_energy.combustion()


----------------------------------------------------------------------

Transportation
-----------------

ASIF framework
..............

The `ASIF framework <https://www.adb.org/publications/transport-and-carbon-dioxide-emissions-forecasts-options-analysis-and-evaluation>`_ relates travel activity, mode share, energy intensity of each mode, fuel and vehicle type, and carbon content of each fuel to total emissions.

- **Activity** (:math:`A`): Often measured as VKT (vehicle kilometers traveled), reflecting the number and length of trips.
- **Mode share** (:math:`S`): Describes the portion of trips taken by different modes (e.g., walking, biking, public transport, private car) and vehicle types (e.g., motorcycle, car, bus, truck).
- **Energy Intensity** (:math:`I`): Energy consumed per vehicle kilometer, a function of vehicle types, characteristics (e.g., occupancy or load factor, represented as passengers per km or tonnes cargo per km), and driving conditions (e.g., drive cycles showing vehicle speed over time).
- **Fuel factor** (:math:`F`): Carbon content of the fuel, based on the composition of the local fuel stock.


.. math::
    E = \sum_{mode} \sum_{fuel} A_{mf} \cdot S_{mf} \cdot I_{mf} \cdot F_{mf}

**Python Code**

.. code-block:: Python

    abemis.transportation.asif()

Fuel Sales
..........

A fuel sales approach invo involves multiplying quantity of fuel sold within a year (:math:`Q`)
by a fuel specific emission factor (:math:`EF`).

.. math::

    E = \sum_{fuel} Q_f \cdot EF_f


Note that modern biofuels used in automobiles are often blends of (bio)ethanol or biodiesel
with fossil fuel-derived diesel or gasoline.
For example, E15 gasoline contains 15% ethanol and 85% gasoline,
while B20 biodiesel is 20% biodiesel and 80% petroleum diesel.

:math:`\text{CO}_2` emissions from the ethanol or biodiesel component are considered biogenic,
while :math:`\text{CO}_2` emissions from the fossil fuel component and all non-:math:`\text{CO}_2` gases
from both components are non-biogenic. Emission factors for blended fuels can be calculated as:

- **Biogenic CO2**: :math:`EF_{\text{biogenic CO2}} = EF_{\text{CO2 for ethanol}} \cdot \%_{\text{ethanol}}`

- **Non-biogenic CO2**: :math:`EF_{\text{non-biogenic CO2}} = EF_{\text{CO2 for petroleum}} \cdot (100\% - \%_{\text{ethanol}})`

- **Methane (CH4)**: :math:`EF_{\text{CH4}} = [EF_{\text{CH4 for ethanol}} \cdot \%_{\text{ethanol}}] + [EF_{\text{CH4 for petroleum}} \cdot (100\% - \%_{\text{ethanol}})]`

- **Nitrous Oxide (N2O)**: :math:`EF_{\text{N2O}} = [EF_{\text{N2O for ethanol}} \cdot \%_{\text{ethanol}}] + [EF_{\text{N2O for petroleum}} \cdot (100\% - \%_{\text{ethanol}})]`

Note that if the fuel blend percentage is based on volume, use volume-based emission factors;
if it is based on weight, use weight-based emission factors.

**Python Code**

.. code-block:: Python

    abemis.transportation.fuel_sales()

----------------------------------------------------------------------

Waste
-----------------

This sector encompasses solid waste as well as wastewater.
There are few methods for each

Methane Comittment
..................

Methane commitment (MC) is an estimate for solid waste sent to landfill.
This assigns landfill emissions based on waste disposed in a given year.
It takes a lifecycle and mass-balance approach and calculates landfill
emissions based on the amount of waste disposed in a given year,
regardless of when the emissions actually occur.
A portion of emissions are released every year after the waste is disposed.

.. math::
    CH_4 = MSW * L_o * (1 - f_{ref}) * (1 - OX)

where MSW is the mass of municiple solid waste in metric tonnes, Lo is the dimensionless methane generation potential,
frec is the fractional of methane recoved at the landfill, and OX is the oxidation factor.
GPC recommends using 0.1 for OX if the landfill is well-managed.

.. code-block:: Python

    abemis.waste.methane_commitment()


First Order Decay
................

First Order Decay (FOD) model for solid waste CH4 emissions and estimates actual yearly emissions.


.. math::

    E =  \bigg\{ \sum_x \big[ MSW_x \cdot Lo_x \cdot (1 - \exp^{-k}) \cdot \exp^{-k(t-x)} \big]  - R(t) \bigg\}  \cdot (1-OX)

where MSW is the mas of municple solid waste, Lo is the methane generation potential,
R is the methane collected/removed in the inventory year, OX is the oxidation factor,
and k is the methane genertation rate constant

.. code-block:: Python

    abemis.waste.fod()


Incineration
............

This includes incineration of waste and has separate equations for CO2, CH4, and N2O


**CO2**

.. math::

    CO2 = m \cdot \sum_i (WF_i \cdot dm_i \cdot CF_i \cdot FCF_i \cdot OF_i) \cdot CO2:C

where i is the type of the Solid Waste incinerated such as paper/cardboard, textile, food waste, etc.
m is the mass of waste, WF is the fraction of the waste type, dm is the dry matter content,
cf is the carbon fraction in dry matter, fcf is the fraction that is fossil carbon,
and ox is the oxidation factor.

**CH4 and N2O**

.. math::

    E = \sum_i IW_i \cdot EF_i

where IW is the amount of solid waste, EF is the emission factor,
and  i is the category or type of waste incinerated/open-burned, specified as follows:

* MSW: municipal solid waste
* ISW: industrial solid waste
* HW: hazardous waste
* CW: clinical waste
* SS: sewage sludge
* others (that must be specified)

.. code-block:: Python

    abemis.waste.incineration_co2()
    abemis.waste.incineration_ch4()
    abemis.waste.incineration_n2o()


Wastewater
..........


**CH4**

.. math::

    E = [(TOW - S) \cdot EF - R] \cdot tonne:kg

where TOW is the total organic content in the wastewater, EF is the emission factor,
S is organic content removed from the sludge, and R is the amount of methane recovered.


**Indirect N2O**

.. math::

    E = [(P \cdot protein \cdot F_{NRP} \cdot  F_{NON-CON} \cdot F_{IND-CON}) - N_{sludge}] \cdot EF \cdot conversion

Where P the population served by water treatment plant, protein is the annual per capita protein consumption,
:math:`F_{NRP}` is a factor to adjust for non-consumed protein, :math:`F_{NON-CON}` is fraction of nitrogen in protein,
:math:`F_{IND-CON}` is factor for industrial and commercial co-discharged protein into the sewer system,
N is nitrogen removed with sludge, and EF is the emission factor


.. code-block:: Python

    abemis.waste.wastewater_ch4()
    abemis.waste.wastewater_n2o_indirect()

----------------------------------------------------------------------

Industrial processes, and product use (IPPU)
-----------------

Cement
......

.. math::

    E = M \cdot EF

where M is the mass of clinker produced and EF is the emission factor.

.. code-block:: Python

    abemis.ippu.cement_production()

Lime
....

.. math::

    E = \sum_i M_i \cdot EF_i

where M is the mass, EF is the emission factor, and  i is limestone or dolomite.

.. code-block:: Python

    abemis.ippu.lime_production()

Glass
.....

.. math::

    E = \sum_i M_i \cdot EF_i \cdot (1 - CR_i)

where M is the mass of melted glass, EF is the emission factor, CR is the cullet ratio,
and i the type of glass.


.. code-block:: Python

    abemis.ippu.glass_production()

Non-energy product use
......................


.. math::

    E = \sum_{fuel} (NEU_{fuel} \cdot CC_{fuel} \cdot ODU_{fuel}) \cdot CO2:C


where NEU is the non-energy use in TJ, CC is the carbon content of the fuel,
and ODU is the fraction of fuel oxizied during use. Total emission requires summing across all fuel types.

.. code-block:: Python

    abemis.ippu.non_energy_product_use()

----------------------------------------------------------------------

Agriculture, forestry, and other land use (AFOLU)
-----------------

Biomass Burning
...............

.. code-block:: Python

    abemis.afolu.biomass_burning()

Enteric Fermentation
....................

.. math::

    CH4 = \sum_t N_t \cdot EF_t \cdot tonne:kg


where N is the number of animals, EF is the emission factor, and t is the type of livestock.

.. code-block:: Python

    abemis.afolu.enteric_fermentation_ch4()


Manure Management
.................

**CH4**

.. math::

    CH4 = \sum_t N_t \cdot EF_t \cdot tonne:kg

where N is the number of animals, EF is the emission factor, and t is the type of livestock.

**N2O**

.. math::

    N2O = \sum_t (N_t \cdot NEX_t \cdot MS_t) \cdot EF_t \cdot tonne:kg

where N is the number of animals, EF is the emission factor,
NEX is the annual nitrogren excretion, and MS is fraction of total annual nitrogen excretion managed.

Note there may be multiple manure management systems (MMS).
If so, then this requires summing across them.

.. code-block:: Python

    abemis.afolu.manure_management_ch4()
    abemis.afolu.manure_management_n2o()
    abemis.afolu.manure_management_n2o_indirect()

Liming
......

.. math::

    CO2 = \sum_t (M_t * EF_t) * CO2:C

Where M is the amount of limestone or dolomite, EF is the emission factor, where t is the limestone or dolomite


.. code-block:: Python

    abemis.afolu.liming()

Urea Application
................

.. math::

    CO2 = \sum_t (M_t * EF_t) * CO2:C

where M is the mass of urea and EF is the emission factor

.. code-block:: Python

    abemis.afolu.urea_fertilization()

Rice Cultivation
................

.. math::

    CH4 = t \cdot A \cdot EF \cdot tonnes:kg

where t is the cultivation period in days, A is the harvested area, and EF is the emission factor.
Note that you may need to sum across different ecosystems, water regimes, type and amount of organic amendments,
and other conditions under which CH4 emissions from rice may vary.

.. code-block:: Python

    abemis.afolu.rice_cultivation_ch4()
