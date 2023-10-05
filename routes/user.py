from fastapi import APIRouter, Response
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
    return Response(status_code=HTTP_201_CREATED)

@routes.get("/users/{id}", response_model=list[User], tags=["users"])
async def find_user(id_request: str):
    return user_entity(conn.pruebas.users.find_one({"_id":ObjectId(id_request)}))

@routes.put("/users/{id}", response_model=list[User], tags=["users"])
async def update_user(id_request: str, user_request: User):
    new_user = dict(user_request)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    conn.pruebas.users.find_one_and_update(
        {"_id": ObjectId(id_request)},{"$set":dict(new_user)}
    )
    return user_entity(conn.pruebas.users.find_one({"_id":ObjectId(id_request)}))

@routes.delete("/users/{id}", response_model=list[User], tags=["users"])
async def delete_user(id_request: str):
    user_entity(conn.pruebas.users.find_one_and_delete({"_id":ObjectId(id_request)}))
    return Response(status_code=HTTP_204_NO_CONTENT)