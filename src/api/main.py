# Standard Library Imports
import logging

# Third Party Imports
from fastapi import FastAPI
from routers.user_router import router
from utils.database import mongo_connect

log = logging.getLogger("uvicorn")
allow_headers = ["*"]


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router, tags=["Users"], prefix="/user")
    application.add_event_handler("startup", mongo_connect)
    return application


app = create_application()


@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint of the API.

    Returns:
        A welcome message to the API.
    """
    return {"message": "Welcome to the V1 app!"}


@app.get("/health", tags=["Health"], status_code=200)
async def health_check():
    """Health check endpoint of the API.

    Returns:
        A welcome message to the API.
    """
    return {"message": "healthy"}


@app.on_event("startup")
async def startup_event():
    log.info("Starting up API")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down API")
