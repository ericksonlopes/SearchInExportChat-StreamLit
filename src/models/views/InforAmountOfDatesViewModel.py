from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class InforAmountOfDatesViewModel:
    data_frame: DataFrame
    average_per_day: int
    average_per_week: int
    average_per_month: int
    day_with_more_messages: str
    day_with_less_messages: str
    amout_day_more_messages: int
    amout_day_less_messages: int
    amount_od_days: int = 0

