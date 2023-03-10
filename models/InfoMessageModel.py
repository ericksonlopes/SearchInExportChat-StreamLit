from dataclasses import dataclass
from datetime import datetime


@dataclass
class InfoMessageModel:
    message: str
    date: datetime
