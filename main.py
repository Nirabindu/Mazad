from fastapi import FastAPI
from sql_app import models, database
from fastapi.staticfiles import StaticFiles
from routers import admin_function,address,individual_function,search,story,business_dev,otp,user_profile_services,user_auth
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
app.include_router(otp.router)
app.include_router(user_profile_services.router)
app.include_router(address.router)
app.include_router(individual_function.router)
app.include_router(search.router)

app.include_router(admin_function.router)
app.include_router(business_dev.router)


app.include_router(story.router)






