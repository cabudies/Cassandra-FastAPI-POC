from uuid import UUID
from typing import Optional, Any
from pydantic import BaseModel, root_validator


class CitiesSchema(BaseModel):
    name: str
    country: str
