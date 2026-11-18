from pydantic import AwareDatetime, BaseModel, Field


class FlightRecord(BaseModel):
    """Rekord lotu z danych zewnętrznych (CSV, API) — walidowany przy tworzeniu."""

    flight_number: str
    origin: str = Field(pattern=r"^[A-Z]{3}$")
    destination: str = Field(pattern=r"^[A-Z]{3}$")
    status: str
    delay_minutes: int  = Field(ge=-120)
    scheduled_departure: AwareDatetime
    gate: str | None = None