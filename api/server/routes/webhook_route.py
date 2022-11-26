from fastapi import HTTPException
from libs.kinetic import Kinetic


def error(message):
    print(f"⚠️ Webhook Error: {message}")
    raise HTTPException(status_code=404, detail=message)

def success():
    return 'Ok'

def webhook_route(payload: dict, kinetic: Kinetic, type: str) -> dict:
    if type == 'balance':
        return kinetic.handle_balance_webhook(payload['balance'], payload['change'], error, success)
    elif type == 'event':
        return kinetic.handle_event_webhook(payload['transaction'], error, success)
    elif type == 'verify':
        return kinetic.handle_verify_webhook(payload['transaction'], error, success)
    else:
        return error('Webhook type supported.')

    print(payload)
    return success()

