from dataclasses import dataclass


@dataclass
class Stage:
    stageNumber: int
    squaresLocations: list[(int, int)]
    selectedSquares: list[(int, int)]
    actionTimes: list[float]
    errorCount: int
    errorLocations: list[(int,int)]

@dataclass
class Session:
    sessionNumber: int
    stages: list[Stage]
    errorStages: list[int]
    lastStage: int


@dataclass
class DataContainer:
    sessions: list[Session]