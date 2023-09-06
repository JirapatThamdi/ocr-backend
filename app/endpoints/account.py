import numpy as np
from fastapi import APIRouter, Body, File, UploadFile, status, Path
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette import status

from app.models.account import AccountResponseModel, AccountModel
from app.utils.logger import init_logger
from app.interface.mongodb import MongoInterface

logger = init_logger(__name__)

USER_COLLECTION = "users"

mongo_obj = MongoInterface(USER_COLLECTION, index_list=[("location", "2dsphere")])

router = APIRouter()

@router.post("/create-account", response_description="Create new account",
             response_model=AccountResponseModel, response_model_by_alias=False)
async def detect_nearest_house(data: AccountModel = Body(...)):
    #get data from mongo that in range of lat_long
    data_dict = jsonable_encoder(data)
    created_document = await mongo_obj.create_new_document(data_dict)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=jsonable_encoder(AccountResponseModel(**created_document),
                                                 by_alias=False))

@router.get("/account", response_description="Get account",
             response_model=Page[AccountResponseModel], response_model_by_alias=False)
async def get_history():
    #get data from mongo that in range of lat_long
    history = await paginate(await mongo_obj.get_collection_object(),
                            sort={"createdAt": 1})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(history, by_alias=False))