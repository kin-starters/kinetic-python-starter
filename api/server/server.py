from fastapi import FastAPI, APIRouter
from kinetic_sdk import KineticSdk

from server.server_config import get_server_config


config = get_server_config()

app = FastAPI(title="Kinetic Python Starter", openapi_url="/openapi.json")
api_router = APIRouter()


# Setup Kinetic SDK
sdk = KineticSdk.setup(
    endpoint=str(config['endpoint']),
    environment=str(config['environment']),
    index=str(config['index']),
)

@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


@api_router.get("/health", status_code=200)
def health() -> dict:
    """
    Health GET
    """
    print(sdk.config)
    return {"msg": "Healthy"}


app.include_router(api_router)

