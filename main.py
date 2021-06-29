from fastapi import FastAPI
from sql_app import models, database
from fastapi.staticfiles import StaticFiles
from routers import admin,story,business_dev,otp,Individual_user_related_service,user_auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

models.database.Base.metadata.create_all(database.engine)

app.include_router(user_auth.router)
app.include_router(admin.router)
app.include_router(Individual_user_related_service.router)
app.include_router(story.router)
app.include_router(business_dev.router)
app.include_router(otp.router)




