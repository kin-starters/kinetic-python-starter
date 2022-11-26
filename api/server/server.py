from fastapi import FastAPI, APIRouter, Body, Request
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

# Payment Routes, pass in our Kinetic helper class
@api_router.get("/payment/{destination}/{amount}", status_code=200)
def payment(destination: str, amount: int, req: Request) -> dict:
    return payment_route(req, kinetic, destination, amount)


# Webhook Routes, pass in our Kinetic helper class
@api_router.post("/webhook/{type}", status_code=200)
def webhook(type: str, payload: dict = Body()) -> dict:
    return webhook_route(payload, kinetic, type)


@app.get("/uptime", status_code=200)
def uptime() -> dict:
    return uptime_route()


app.include_router(api_router)

