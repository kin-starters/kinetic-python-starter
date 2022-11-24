from fastapi import FastAPI, APIRouter
from kinetic_sdk import KineticSdk, Keypair

from server.server_config import get_server_config
from libs.kinetic import Kinetic


config = get_server_config()

app = FastAPI(title="Kinetic Python Starter", openapi_url="/openapi.json")
api_router = APIRouter()


# Setup Kinetic SDK
sdk = KineticSdk.setup(
    endpoint=str(config['endpoint']),
    environment=str(config['environment']),
    index=str(config['index']),
)

# Create instance of our Kinetic helper class
kinetic = Kinetic(config, sdk, Keypair.from_mnemonic(config['payment_mnemonic']))

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
    return {"msg": "Healthy"}


app.include_router(api_router)

