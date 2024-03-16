import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
import pathlib
from app.routes import router as api_router


environment = os.getenv("APP_ENV")

if environment == "prod":
    app = FastAPI(docs_url=None, redoc_url=None)
elif environment == "dev":
    app = FastAPI()
else:
    app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    cwd = pathlib.Path(__file__).parent.resolve()
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_config=f"{cwd}/log.ini", reload=True)
