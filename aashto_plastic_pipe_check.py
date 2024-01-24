"""AASHTO 12.12.3- Thermoplastic Pipe Checks"""

__version__ = "0.1.1"

from typing import Literal, Callable
import xlwings as xw
from pint import UnitRegistry, Quantity, Unit
from excalc_py import create_calculation, adapt_function

# xlwings interop
WB_NAME = "C:\\Users\\rteachey\\projects\\aashto_plastic_pipe_check\\AASHTO plastic pipe structural calcs.xlsx"
APP = xw.App(visible=False)
WB: xw.Book = APP.books.open(WB_NAME)
SH: xw.Sheet = WB.sheets[0]
OUTPUT_RNG = SH.range("CheckAll")

# pint interop
U = UnitRegistry()

RNG_UNITS_DICT = dict[str, (str, Unit | None)](
    pipe_type=("PipeType", None),
    D_nom=("D_nom", U.inch),
    H=("H", U.feet),
    H_gw=("H_gw", U.feet),
    γ_soil=("γ_soil", U.lbf / U.feet**3),
    Ms=("Ms", U.psi),
    E_prime=("E_prime", U.psi),
    soil_class=("SoilClass", None),
    compaction=("Proctor", None),
    proctor=("ProctorType", None),
    grain=("Grain", None),
    ν=("ν", None),
    E_long=("E_long", U.psi),
    E_short=("E_short", U.psi),
    Fy_long=("Fy_long", U.psi),
    Fy_short=("Fy_short", U.psi),
)


# adapt for units
def _its_a_quantity(quantity: Quantity) -> Quantity:
    return quantity


_ADAPT_DICT: dict[None | UnitRegistry, Callable] = {
    U: lambda quantity: quantity,
    # a str can be turned into a quantity
    None: lambda quantity_str: U.Quantity(quantity_str),
}


def _ensure_quantity(quantity: Quantity | str) -> Quantity:
    # handle a quantity from another pint unit registry
    registry = getattr(quantity, '_REGISTRY', None)
    return _ADAPT_DICT.setdefault(registry, _its_a_quantity)(quantity)


def _input_unit_adapter(unit: Unit) -> Callable[[Quantity | str], float]:
    def input_adapter(quantity):
        return _ensure_quantity(quantity).to(unit).magnitude
    return input_adapter


INPUT_RNG_DCT = {k: SH.range(v[0]) for k, v in RNG_UNITS_DICT.items()}
INPUT_UNITS_DCT = {
    k: _input_unit_adapter(v[1])
    for k, v in RNG_UNITS_DICT.items()
    if v[1] is not None
}


# noinspection PyUnusedLocal
@adapt_function(**INPUT_UNITS_DCT)
@create_calculation(OUTPUT_RNG, **INPUT_RNG_DCT)
def check(
    pipe_type: Literal["DR17", "DR32.5"] = None,
    D_nom: Quantity = None,
    H: Quantity = None,
    H_gw: Quantity = None,
    γ_soil: Quantity = None,
    Ms: Quantity = None,
    E_prime: Quantity = None,
    soil_class: Literal["I", "IA", "IB", "II", "III"] = None,
    compaction: Literal["Compacted", "Uncompacted", "85%", "90%", "95%", "100%"] = None,
    proctor: Literal["Standard Proctor", "Modified Proctor"] = None,
    grain: Literal["Gravel", "Sand"] = None,
    ν: float = None,
    E_long: Quantity = None,
    E_short: Quantity = None,
    Fy_long: Quantity = None,
    Fy_short: Quantity = None,
):
    """Uses the AASHTO plastic pipe structural calcs.xlsx spreadsheet to perform structural checks based on inputs."""
    ...
