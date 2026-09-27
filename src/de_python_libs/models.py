from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class FlightEvent(BaseModel):
    flight_id: str = Field(min_length=3)
    icao24: str
    event_type: str
    event_ts: datetime

    @field_validator("icao24")
    @classmethod
    def icao24_must_be_hex(cls, v: str) -> str:
        v = v.lower()
        if len(v) != 6 or any(c not in "0123456789abcdef" for c in v):
            raise ValueError("icao24 musi mieć 6 znaków hex")
        return v
