from pydantic import BaseModel, Field, validator
from typing import List, Optional

class SpeedDial(BaseModel):
    id: Optional[str] = Field(None, alias='speedDialId')
    code: str
    description: Optional[str] = None
    number: str = Field(alias='dialedNumber')
    emergency_number: bool = Field(alias='emergencyNumber')
    india_telecom_code: Optional[bool] = Field(None, alias='indiaTelecomCode')

