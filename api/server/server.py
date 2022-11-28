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


# Start server
app.include_router(api_router)
print(f"🚀 Listening on port {config['port']}")
config = sdk.internal.app_config
print(f"⬢ Kinetic: Connected to App: {config['app']['name']} {config['app']['index']} ")
print(f"⬢ Kinetic: Connected to API: {config['api']['name']} {config['api']['version']} ")
print(f"⬢ Kinetic: Connected to Environment: {config['environment']['name']} ({config['environment']['cluster']['name']}) ")

for mint in config['mints']:
    mint_airdrop_max = mint['airdrop_max']
    mint_symbol = mint['symbol']
    mint_airdrop = mint['airdrop']
    print(f"⬢ Kinetic: Mint: {mint.name} {mint['public_key']} ({mint.decimals} decimals) (Payment: { f'max {mint_airdrop_max} {mint_symbol}' if {mint_airdrop} != None else 'disabled'}) ")


# Initialize PaymentAccount
kinetic.find_or_create_account()
print("⬢ Payment: link /payment/<destination>/<amount>")
