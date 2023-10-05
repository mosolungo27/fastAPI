from fastapi import FastAPI
from routes.user import routes

app = FastAPI()

app.include_router(routes)