from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, HttpUrl


class ListingBase(BaseModel):
    source: str
    external_id: str
    title: str
    url: HttpUrl
    address: str | None = None
    price_rub: Decimal
    floor: int
    building_year: int
    property_type: str
    area_sqm: Decimal | None = None
    tenant: str | None = None


class ListingCreate(ListingBase):
    pass


class ListingRead(ListingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ai_summary: str | None = None
    investment_score: int | None = None
    created_at: datetime
    updated_at: datetime

