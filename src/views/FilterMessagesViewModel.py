from dataclasses import dataclass, field

from pandas import DataFrame


@dataclass
class FilterMessagesViewModel:
    data_frame: DataFrame
    amount_filter: int = field(default=0)
    amount_numbers: int = field(default=0)
