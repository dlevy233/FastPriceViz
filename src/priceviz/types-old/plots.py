from enum import Enum
from typing import List, Optional, Union, Literal
from priceviz.types.data import MarketData, BucketedDataFromObjectStore, DateTimeRange
from pydantic import BaseModel, Field

class PlotPosition(Enum):
    OVERLAY = "overlay"
    SIDE = "side"
    BELOW = "below"

class DisplayMode(Enum):
    HTML = "html"

class LineSpec(BaseModel):
    ticker: str
    column: str
    position: PlotPosition
    color: Optional[str] = None
