from dataclasses import dataclass

import xarray as xr


@dataclass
class RomsNCFiles:
    grd: str
    nud: str
    ini: str
    bry: str
    clm: str
    his: str
    avg: str
    qks: str
    dia: str
    frc: str
    rivers: str
    tides: str


@dataclass
class AppState:
    ds: object = None
    da: object = None
    cbar: str = "viridis"

    @property
    def current_slice(self):
        slice_str = self.da._title_for_slice(truncate=1000)
        sliced = {}
        for slc in slice_str.split(","):
            sliced[slc.split("=")[0].strip()] = slc.split("=")[1].strip()

        return sliced

    @property
    def var(self):
        return self.da.name


# representative variable for each ROMS file
REP_VAR = RomsNCFiles(
    grd="h",
    nud="temp_NudgeCoef",
    ini="temp",
    bry="temp_west",
    clm="temp",
    his="temp",
    avg="temp",
    qks="temp",
    dia="undefined",
    frc="Pair",
    rivers="river_salt",
    tides="tide_Eamp",
)
