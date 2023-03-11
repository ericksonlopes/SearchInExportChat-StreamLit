from dataclasses import dataclass
from typing import List


@dataclass
class PhoneLinksModel:
    """PhoneLinksModel"""
    phone: str
    links: List[str]

    def insert_link(self, links: str):
        self.links.extend(links)
