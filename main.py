"""
Main entry point for the agent.
"""
import atexit
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.utils import env_config as config
from app.utils.logger import init_logger

from app.endpoints import water_meter
from app.endpoints import account

logger = init_logger(__name__)


if __name__ == "main":
    config.print_config(logger)
    config.print_config_warning(logger)


app = FastAPI(
    title=config.PROJECT_NAME,
    description="OCR Engine Backend is a REST API service for managing the OCR Engine.",
    version=config.RELEASE_VERSION,
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json"
)
add_pagination(app)

# CORS Middleware
# allow_origins: A list of origins that may access the resource.
# allow_credentials: Whether to allow credentials.
# allow_methods: A list of HTTP methods that are supported by the resource.
# allow_headers: A list of HTTP headers that are supported by the resource.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Logger Middleware
# Log all requests with their response status code and time taken to process the request.
# ignores websocket requests internally

# fastapi routers
app.include_router(water_meter.router, tags=["water_meter"])
app.include_router(account.router, tags=["account"])
# mount assets
# assets.mount_assets(app, prefix="/assets")

@app.on_event("startup")
def startup_db_client():
    pass

@app.on_event("shutdown")
def shutdown_event():
    """
    Handle shutdown event triggered by the uvicorn server.
    """
    logger.warning("Shutting down server...")


if __name__ == "__main__":
    logger.info(".........................................................")
    logger.info("Starting server...")
    logger.info("http://%s:%s....", config.HOST, config.PORT)
    logger.info(".........................................................")

    @atexit.register
    def goodbye():
        """
        Triggered after the server is shutdown at exit.
        """
        logger.info("Goodbye!")

    uvicorn.run("main:app",
                port=config.PORT,
                log_level="warning",
                host=config.HOST,
                reload=False)
