from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from passlib.hash import sha256_crypt
from starlette.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

from config.db import conn
from models.user import User
from schemas.user import user_entity, users_entity

routes = APIRouter()

@routes.get("/users", response_model=list[User], tags=["users"])
async def find_all_users():
    return users_entity(conn.pruebas.users.find())

@routes.post("/users", response_model=list[User], tags=["users"])
async def create_user(user_request : User):
    new_user = dict(user_request)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    id_save = conn.pruebas.users.insert_one(new_user).inserted_id
    user_request = user_entity(conn.pruebas.users.find_one({"_id":ObjectId(id_save)}))
    user_response = jsonable_encoder(user_request)
    return JSONResponse(status_code=HTTP_201_CREATED,content=user_response)

@routes.get("/users/{id}", response_model=list[User], tags=["users"])
async def find_user(id_request: str):
    find_user = user_entity(conn.pruebas.users.find_one({"_id":ObjectId(id_request)}))
    user_response = jsonable_encoder(find_user)
    return JSONResponse(content=user_response)

@routes.put("/users/{id}", response_model=list[User], tags=["users"])
async def update_user(id_request: str, user_request: User):
    new_user = dict(user_request)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    conn.pruebas.users.find_one_and_update(
        {"_id": ObjectId(id_request)},{"$set":dict(new_user)}
    )
    find_user = user_entity(conn.pruebas.users.find_one({"_id":ObjectId(id_request)}))
    user_response = jsonable_encoder(find_user)
    return JSONResponse(content=user_response)

@routes.delete("/users/{id}", response_model=list[User], tags=["users"])
async def delete_user(id_request: str):
    user_entity(conn.pruebas.users.find_one_and_delete({"_id":ObjectId(id_request)}))
    return Response(status_code=HTTP_204_NO_CONTENT)