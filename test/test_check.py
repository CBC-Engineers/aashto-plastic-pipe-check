import pytest
from aashto_plastic_pipe_check import check, U, APP
from pint import UnitRegistry

FOREIGN_REG = UnitRegistry()


@pytest.fixture(autouse=True, scope="session")
def xw_app():
    yield APP
    APP.quit()


@pytest.fixture(
    params=[
        dict(
            pipe_type=None,
            D_nom=None,
            H=None,
            H_gw=None,
            γ_soil=None,
            Ms=None,
            soil_class=None,
            compaction=None,
            proctor=None,
            grain=None,
            ν=None,
            E_long=None,
            E_short=None,
            Fy_long=None,
            Fy_short=None,
        ),
        dict(
            pipe_type=None,
            D_nom=None,
            H=None,
            H_gw=None,
            γ_soil=None,
        ),
        dict(
            pipe_type="32.5",
            D_nom=48*U.inch,
            H=10*U.ft,
            H_gw=10*U.ft,
            γ_soil=120.0*U.lbf/U.ft**3,
        ),
        dict(
            pipe_type="32.5",
            D_nom="48 * inch",
            H="10 * ft",
            H_gw="10 * ft",
            γ_soil="120.0 * lbf / ft ** 3",
        ),
        dict(
            pipe_type="32.5",
            D_nom=48 * FOREIGN_REG.inch,
            H=10 * FOREIGN_REG.ft,
            H_gw=10 * FOREIGN_REG.ft,
            γ_soil=120.0 * FOREIGN_REG.lbf / FOREIGN_REG.ft ** 3,
        ),
    ], ids=("All None", "Partial None", "Partial w units", "Partial str units", "Foreign pint unit registry")
)
def check_kwargs(request):
    return request.param


def test_check(check_kwargs):
    result = check(**check_kwargs)
    assert result
