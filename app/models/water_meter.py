from pydantic import BaseModel, Field, validator
from app.models.history import HistoryModel
# meter number, longtitude, latitude
class WaterMeterModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    person_id : int = Field(..., alias="personId")
    lat_long : list[str] = Field(..., alias="latLong")
    history : list[HistoryModel] = Field(..., alias="history")

    class Config:
        """
        Extends BaseModel.Config to define the Base Model model's configuration.
        """
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "person_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "lat_long": ["123", "123"],
                "history": [{"usage": 123, "usage_total": 1234}],
            }
        }

class WaterMeterResponseModel(BaseModel):
    """
    Extends BaseModel to define the Base Model model.
    """
    id : int = Field(..., alias="_id")
    person_id : int = Field(..., alias="personId")
    lat_long : list[str] = Field(..., alias="latLong")
    history : list[HistoryModel] = Field(..., alias="history")
    
    @validator("id","person_id", pre=True, always=True)
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
                "id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "person_id": "60b0f7a6f2d6f4f4d4f4d4f4",
                "lat_long": ["123", "123"],
                "history": [{"usage": 123, "usage_total": 1234}],
            }
        }
