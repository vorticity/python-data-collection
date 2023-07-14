from enum import Enum, unique


@unique
class TableConfigName(str, Enum):
    FARMING_PRACTICE_CONFIG = "FarmingPracticeConfig"


@unique
class TableViewName(str, Enum):
    FARMING_PRACTICE_TYPICAL_VIEW = "FarmingPracticeTypicalView"
    FARMING_PRACTICE_OFFERING_VIEW = "FarmingPracticeOfferingView"
