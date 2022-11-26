from fastapi import FastAPI, APIRouter, Response, Request
from kinetic_sdk import KineticSdk, Keypair

from server.server_config import get_server_config
from libs.kinetic import Kinetic
from server.routes.payment_route import payment_route
from server.routes.uptime_route import uptime_route
from server.routes.webhook_route import webhook_route


config = get_server_config()

app = FastAPI(title="Kinetic Python Starter", openapi_url="/openapi.json")
api_router = APIRouter()


# Setup Kinetic SDK
sdk = KineticSdk.setup(
    endpoint=str(config['endpoint']),
    environment=str(config['environment']),
    index=config['index'],
)

# Create instance of our Kinetic helper class
kinetic = Kinetic(config, sdk, Keypair.from_mnemonic(config['payment_mnemonic']))

@api_router.get("/payment/{destination}/{amount}", status_code=200)
def payment(destination: str, amount: int, req: Request, res: Response) -> dict:
    return payment_route(req, res, kinetic, destination, amount)


@api_router.get("/webhook/{type}", status_code=200)
def webhook(type: str) -> dict:
    return webhook_route(kinetic, type)


@app.get("/uptime", status_code=200)
def uptime() -> dict:
    return uptime_route()


app.include_router(api_router)

