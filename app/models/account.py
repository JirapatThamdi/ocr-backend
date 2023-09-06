import time

from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Union

from app.models.history import HistoryModel

class coordinateModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    type: str = 'Point'
    coordinates: list[Union[float, int, None]]

    class Config:
        """
        Extends BaseModel.Config to define the Base Model model's configuration.
        """
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "type": "Point",
                "coordinates": [123, 123],
            }
        }

class AccountModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    number : str = Field(..., alias="number")
    name : str = Field(..., alias="name")
    address : str = Field(..., alias="address")
    location : coordinateModel = Field(..., alias="location")
    history : list[HistoryModel] = Field(None, alias="history")
    created_at : float = Field(None, alias="createdAt")
    updated_at : float = Field(None, alias="updatedAt")

    @validator("created_at","updated_at", pre=True, always=True)
    def convert_unix_timestamp_to_readable(cls, value):
        """
        Convert UTC timestamp in seconds to readable format.
        """ 
        return time.time()

    class Config:
        """
        Extends BaseModel.Config to define the Base Model model's configuration.
        """
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "number": "115",
                "name": "Jane doe",
                "address": "123",
                "location": {
                    "type": "Point",
                    "coordinates": [
                    -73.856077,
                    40.848447
                    ]
                }
            }
        }

class AccountResponseModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    id : str = Field(..., alias="_id")
    number : str = Field(..., alias="number")
    name : str = Field(..., alias="name")
    address : str = Field(..., alias="address")
    location : coordinateModel = Field(..., alias="location")
    created_at : str = Field(..., alias="createdAt")
    updated_at : str = Field(..., alias="updatedAt")
    
    @validator("id", pre=True, always=True)
    def convert_object_id_to_str(cls, value):
        """
        Convert ObjectId to str for response.
        """
        return str(value)
    
    @validator("created_at","updated_at", pre=True, always=True)
    def convert_unix_timestamp_to_readable(cls, value):
        """
        Convert UTC timestamp in seconds to readable format.
        """ 
        return datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    class Config:
        """
        Extends BaseModel.Config to define the Base Model model's configuration.
        """
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "name": "John",
                "address": "123",
            }
        }

class UpdateAccountModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    number : str = Field(None, alias="number")
    name : str = Field(None, alias="name")
    address : str = Field(None, alias="address")
    location : coordinateModel = Field(None, alias="location")
    history : list[HistoryModel] = Field(None, alias="history")

    class Config:
        """
        Extends BaseModel.Config to define the Base Model model's configuration.
        """
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "John",
                "address": "123",
                "location": {
                        "type": "Point",
                        "coordinates": [-73.856077, 40.848447]
                    },
                "history": [{"image":"/storage/example.png",
                            "meter_reading": 1234,
                            "Usage_total": 1234,
                            "timestamp": "2021-05-28 12:00:00"
                    }]
            }
        }
