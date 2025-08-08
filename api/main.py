import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routers import index as indexRoute
from api.models import model_loader
from api.dependencies.config import conf
from .controllers import users
from .models.model_loader import index


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)