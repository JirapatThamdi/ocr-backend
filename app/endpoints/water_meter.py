import numpy as np
import os
import uuid
import cv2
import PIL

from io import StringIO
from PIL import Image
from bson import ObjectId
from fastapi import APIRouter, Body, File, UploadFile, status, Path
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate, paginate_aggregate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status

from app.models.water_meter import WaterMeterModel, WaterMeterResponseModel
from app.models.account import AccountModel, AccountResponseModel
from app.utils.logger import init_logger
from app.interface.mongodb import MongoInterface

logger = init_logger(__name__)

WATER_METER_COLLECTION = "users"

mongo_obj = MongoInterface(WATER_METER_COLLECTION)

router = APIRouter()

@router.post("/detect-meter")
async def detect_meter(file: UploadFile = File(...)):
    # save image to local
    img = Image.open(file.file)
    os.chdir("app/storage")
    filename = str(uuid.uuid4()) + ".jpg"
    img.save(filename)
    os.chdir("../..")

    return {"filename": filename, "usage": 123}

@router.get("/nearest-meter", response_description="get nearest house",
             response_model=list[AccountResponseModel], response_model_by_alias=False)
async def detect_nearest_house(long : float, lat : float):
    # get nearest house by coordinates (long, lat)
    query = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [long, lat]
                }
            }
        }
    }

    nearest_houses = await mongo_obj.get_documents_by_query(query)
    return nearest_houses

# @router.get("/history", response_description="get history",
#                 response_model=Page[WaterMeterResponseModel], response_model_by_alias=False)
# async def get_history():
#     #get data from mongo that in range of lat_long
#     history = await paginate(await mongo_obj.get_collection_object(),
#                             sort={"createdAt": 1})

#     return JSONResponse(status_code=status.HTTP_200_OK,
#                         content=jsonable_encoder(history, by_alias=False))

# @router.get("/history/{id}", response_description="get history",
#                 response_model=WaterMeterResponseModel, response_model_by_alias=False)
# async def get_history_by_id(id: str = Path(...)):
#     #get data from mongo that in range of lat_long
#     history = await mongo_obj.get_document_by_id(id)

#     return JSONResponse(status_code=status.HTTP_200_OK,
#                         content=jsonable_encoder(history, by_alias=False))

@router.post("/submit_usage", response_description="submit usage",
                response_model=WaterMeterResponseModel, response_model_by_alias=False)
async def submit_usage(water_meter: WaterMeterModel = Body(...)):
    #get data from mongo that in range of lat_long
    water_meter_dict = jsonable_encoder(water_meter)

    query = {"_id": ObjectId(water_meter_dict["_id"])}
    await mongo_obj.add_to_array_by_id(water_meter_dict["_id"], "history", water_meter_dict["history"][0])

    updated_document = await mongo_obj.get_document_by_query(query)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(updated_document, by_alias=False))
