from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import List, Union, Literal, Optional
from enum import Enum
import dask.dataframe as dd
import pandas as pd
from priceviz.utils import suggest_resources
from dask import delayed
from dask.delayed import Delayed
import logging

logger = logging.getLogger(__name__)

class DateTimeRange(BaseModel):
    start: datetime
    end: datetime

class MarketData(BaseModel):
    stock_name: str
    datetime_range: DateTimeRange
    open_price: List[float]
    close_price: List[float]
    high_price: List[float]
    low_price: List[float]
    volume: List[int]

class BucketedDataFromObjectStore(BaseModel):
    name: str
    filename: str
    datetime_ranges: List[DateTimeRange]
    values: List[float]

class CustomDataFromObjectStore(BaseModel):
    name: str
    filename: str
    datetime_index: List[datetime]
    values: List[Union[float, int, str]]

#class TimeSeriesInput(BaseModel):
#    data_source: Union[MarketData, BucketedDataFromObjectStore, CustomDataFromObjectStore]

class DataSourceType(str, Enum):
    MARKET_DATA = "market_data"
    FUNDAMENTAL_DATA = "fundamental_data"
    ALTERNATIVE_DATA = "alternative_data"

class TimeSeriesSource(BaseModel):
    filename: str
    source_type: DataSourceType
    ticker: str

class DataColumn(BaseModel):
    name: str
    value_description: str
    
DownsamplingStrategyType = Literal["average_pooling", "max_pooling", "min_pooling", "median_pooling"]

class DownsamplingStrategy(BaseModel):
    strategy: DownsamplingStrategyType

