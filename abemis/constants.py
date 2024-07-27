"""
add constants here
use a Constant object to add metadata about the constant
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Constant:
    value: float
    long_name: str
    units: str

@dataclass(frozen=True)
class Conversions:
    kg_to_tonne = Constant(value=0.001, long_name="tonnes in a kilogram", units="dimensionless")
    g_to_tonne = Constant(value=10**(-6), long_name="tonnes in a gram", units="dimensionless")
    N_to_N2O = Constant(value=44/28, long_name="ratio of N2O to N2", units="dimensionless")
    C_to_CO2 = Constant(value=44/12, long_name="ratio of CO2 to C", units="dimensionless")
    year_to_days = Constant(value=365, long_name="days in a year", units="days/year")
    CH4_to_C = Constant(value=16/12, long_name="ratio CH4 to C", units="dimensionless")
    kg_to_Gg = Constant(value=10**-6, long_name="gigarams in a kilogram", units="dimensionless")


@dataclass(frozen=True)
class GWP100_AR6:
    CO2 = Constant(value=1, long_name="GWP for CO2", units="dimensionless")
    CH4_fossil = Constant(value=29.8, long_name="GWP for CH4 from fossil origin, including feedbacks", units="mass CO2 / mass CH4")
    CH4_non_fossil = Constant(value=27.2, long_name="GWP for CH4 from non-fossil origin, including feedbacks", units="mass CO2 / mass CH4")
    N2O = Constant(value=273, long_name="GWP for N2O, including feedbacks", units="mass CO2 / mass N2O")
