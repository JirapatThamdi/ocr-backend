import time
from datetime import datetime
from pydantic import BaseModel, Field, validator

class HistoryModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    image : str = Field(..., alias="photo")
    meter_reading : int = Field(..., alias="usage")
    usage_total : int = Field(..., alias="usageTotal")
    timestamp : int = Field(..., alias="timestamp")

    @validator("timestamp", pre=True, always=True)
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
                "usage": 10,
                "usage_total": 100,
            }
        }

class HistoryResponseModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    id : str = Field(..., alias="_id")
    image : str = Field(..., alias="photo")
    meter_reading : int = Field(..., alias="usage")
    usage_total : int = Field(..., alias="usageTotal")
    timestamp : int = Field(..., alias="timestamp")
    
    @validator("id", pre=True, always=True)
    def convert_object_id_to_str(cls, value):
        """
        Convert ObjectId to str for response.
        """
        return str(value)
    
    @validator("timestamp", pre=True, always=True)
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
                "usage": 10,
                "usage_total": 100,
            }
        }
