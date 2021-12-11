from dataclasses import dataclass


@dataclass
class Stock:
    id: int
    name: str
    country: str
    price: float
    date: str
