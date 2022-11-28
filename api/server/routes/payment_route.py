from fastapi import HTTPException, Request
from libs.kinetic import Kinetic


def payment_route(req: Request, kinetic: Kinetic, destination: str, amount: int) -> dict:
    payment_secret = kinetic.config.get('payment_secret')
    auth_secret = req.headers.get('authorization')
    if ((payment_secret != '' and 'payment_secret' != None)
        and (auth_secret is None or auth_secret != payment_secret)
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return kinetic.payment(amount, destination)


