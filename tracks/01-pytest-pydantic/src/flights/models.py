from dataclasses import dataclass


@dataclass(frozen=True)
class Flight:
    flight_number: str
    origin: str
    destination: str
    status: str
    delay_minutes: int
