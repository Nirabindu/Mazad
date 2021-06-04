from fastapi import FastAPI
from sql_app import models, schemas, database
from fastapi.staticfiles import StaticFiles
from routers import Category
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.mount("/static", StaticFiles(directory="static"), name="static")

models.database.Base.metadata.create_all(database.engine)

app.include_router(Category.router)
