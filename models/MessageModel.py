from dataclasses import dataclass
from datetime import datetime


@dataclass
class MessageModel:
    phone: str
    message: str
    date: datetime

    def concatenate(self, message: str):
        self.message += message
