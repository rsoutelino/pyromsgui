from dataclasses import dataclass


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
