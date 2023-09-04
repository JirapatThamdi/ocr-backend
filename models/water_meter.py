import time
from datetime import datetime
from enum import Enum, IntEnum
from typing import Optional
from pydantic import BaseModel, Field, validator

class WaterMeterModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    person_id : int = Field(..., alias="personId")
    photo_id : int = Field(..., alias="photoId")
    bill_id : int = Field(..., alias="billId")
    usage : int = Field(..., alias="usage")
    usage_total : int = Field(None, alias="usageTotal")

    class Config:
        """
        Extends BaseModel.Config to define the Base Model model's configuration.
        """
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "meter_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "person_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "photo_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "bill_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "usage": 10,
            }
        }

class WaterMeterResponseModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    id : int = Field(..., alias="_id")
    person_id : int = Field(..., alias="personId")
    photo_id : int = Field(..., alias="photoId")
    bill_id : int = Field(..., alias="billId")
    usage : int = Field(..., alias="usage")
    created_at: str = Field(..., alias="createdAt")
    updated_at: str = Field(..., alias="updatedAt")
    usage_total : int = Field(None, alias="usageTotal")

    @validator("created_at", "updated_at", pre=True, always=True)
    def convert_unix_timestamp_to_readable(cls, value):
        """
        Convert UTC timestamp in seconds to readable format.
        """
        return datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    
    @validator("id","person_id","photo_id","bill_id", pre=True, always=True)
    def convert_object_id_to_str(cls, value):
        """
        Convert ObjectId to str for response.
        """
        return str(value)

    class Config:
        """
        Extends BaseModel.Config to define the Base Model model's configuration.
        """
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "meter_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "person_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "photo_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "bill_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "usage": 10,
                "created_at": "2021-05-28 00:00:00",
                "updated_at": "2021-05-28 00:00:00",
            }
        }
