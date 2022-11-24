import os
from os.path import join, dirname
from dotenv import load_dotenv

class ServerConfig(object):
    pass

def get_server_config() -> ServerConfig:
    dotenv_path = join(dirname(__file__), '../../.env')
    load_dotenv(dotenv_path)

    required_env_vars = [
        'ENDPOINT',
        'ENVIRONMENT',
        'INDEX',
        'PAYMENT_ALLOW_EXISTING',
        'PAYMENT_ALLOW_NEW',
        'PAYMENT_MNEMONIC',
        'PORT',
    ]

    missing_env_vars = list(filter(lambda x: x not in os.environ.keys(), required_env_vars))

    if len(missing_env_vars) > 0:
        print("ERROR: Missing environment variables:" , missing_env_vars)
        os._exit(os.EX_OK)
    
    return {
        'endpoint': os.environ.get('ENDPOINT'),
        'environment': os.environ.get('ENVIRONMENT'),
        'index': int(os.environ.get('INDEX')),
        'payment_allow_existing': os.environ.get('PAYMENT_ALLOW_EXISTING') == 'true',
        'payment_allow_new': os.environ.get('PAYMENT_ALLOW_NEW') == 'true',
        'payment_max': os.environ.get('PAYMENT_MAX'), #  or os.environ.get('PAYMENT_AMOUNT')
        'payment_mnemonic': os.environ.get('PAYMENT_MNEMONIC'),
        'payment_secret': os.environ.get('PAYMENT_SECRET'),
        'port': os.environ.get('PORT'), # or '9876'
    }
