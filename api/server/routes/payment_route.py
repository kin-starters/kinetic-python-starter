from fastapi import HTTPException, Request
from libs.kinetic import Kinetic


def payment_route(req: Request, kinetic: Kinetic, destination: str, amount: int) -> dict:
    payment_auth_secret = kinetic.config.get('payment_auth_secret')
    auth_secret = req.headers.get('authorization')
    if ((payment_auth_secret != '' and 'payment_auth_secret' != None)
        and (auth_secret is None or auth_secret != payment_auth_secret)
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return kinetic.payment(amount, destination)


