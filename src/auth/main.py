# Standard Library Imports
import logging

# Third Party Imports
from fastapi import FastAPI

app = FastAPI()
log = logging.getLogger("uvicorn")


@app.get("/")
async def read_root():
    """Root endpoint of the API.

    Returns:
        A welcome message to the API.
    """
    return {"message": "Welcome to the auth service!"}


@app.on_event("startup")
async def startup_event():
    log.info("Starting up AUTH")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down AUTH")
