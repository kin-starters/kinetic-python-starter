from kinetic_sdk.keypair import Keypair
from kinetic_sdk import KineticSdk
from kinetic_sdk import Commitment

import json

class Kinetic(object):

    def __init__(self, config, sdk: KineticSdk, keypair: Keypair):
        self.config = config
        self.sdk = sdk
        self.keypair = keypair


    def mint(self):
        return self.sdk.internal.app_config['mint']


    def public_key(self):
        return self.keypair.public_key


    def payment(self, amount: int, destination: str):
        # Check if amount is below the maximum
        if amount > int(self.config['payment_max']):
            raise Exception(f"Payment amount is too large, max is {self.config['payment_max']}")
    
        # If we don't allow funding existing accounts, check if the destination account has funds
        if self.config['payment_allow_existing'] is None:
            # Check to see if the destination account already has funds
            result = self.sdk.get_balance(destination)

            if result['balance'] != 0:
                raise Exception(f"Account '{destination}' is already funded: {result['balance']} Kin")
    
        # If we don't allow new accounts, check to see if the account exists
        if self.config['payment_allow_new'] is None:
            found = self.sdk.get_token_accounts(destination)

            if len(found) == 0:
                raise Exception(f"Can't send payment to new account {destination}.")
    

        try:
            tx = self._submit_payment(
                str(amount),
                destination,
                sender_create = self.config['payment_allow_new']
            )
            return tx
        except Exception as err:
            raise Exception(f"Account {destination} something went wrong: {err} ")


    def find_or_create_account(self):
        """ Helper function initializes the account. """
        public_key = self.public_key()
        mint = self.mint()

        print(f"⬢ Payment: account: {self.sdk.get_explorer_url(f'address/{public_key}')}")
        print(f"⬢ Payment: address: {public_key}")
        print(f"⬢ Payment: allow empty accounts: {'yes' if self.config['payment_allow_new'] is True else 'no'}")
        print(f"⬢ Payment: allow existing accounts: {'yes' if self.config['payment_allow_existing'] is True else 'no'}")
        print(f"⬢ Payment: auth secret: {'enabled' if self.config['payment_auth_secret'] is True else 'disabled'}")
        print(f"⬢ Payment: max: {self.config['payment_max']}")

        
        # Get the balance of this account
        account = self.sdk.get_balance(account=str(public_key))

        if (len(account.tokens) == 0):
            # If the account doesn't have any tokens, create it.
            self._create_account()
    

        print(f"⬢ Payment: balance: {account['balance']} {mint['symbol']} ")

        if account.balance == '0':
            # If the default Kinetic mint has airdrop enabled, we can fund ourselves...
            if mint['airdrop'] and mint['airdrop_max'] is not None:
                print(f"⬢ Payment: account: {public_key} is empty, requesting airdrop of {str(mint['airdrop_max'])} {mint.get('symbol')}...")

                tx = self.sdk.request_airdrop(
                    account=public_key,
                    amount=str(mint['airdrop_max'])
                )

                print(f"⬢ Payment: request: {self.sdk.get_explorer_url(f'tx/{tx.signature}')}")
            else:
                print(f"⬢ Payment: account: Make sure to fund this account with some {mint['symbol']}.")


    def handle_balance_webhook(self, balance: str, change: str, error, success):
        output = {
            'balance': balance, 
            'change': change
        }
        print(f"📨 Webhook: Balance: {json.dumps(output, indent=2)})")
        return success()


    def handle_event_webhook(self, payload, error, success):
        amount = payload.amount
        destination = payload.destination
        signature = payload.signature

        print(f"📨 Webhook: Event: sent {amount} to {destination} {self.sdk.get_explorer_url(f'tx/{signature}')}")
        return success()


    def handle_verify_webhook(self, payload, error, success):
        amount = payload.amount
        destination = payload.amount

        # Check if the amount is above the minimum
        if int(amount) < 100:
            return error('Amount too low...')

        # Check if the destination address is not the payment account
        if destination == self.public_key:
            return error('Destination is payment account...')

        # Add your own verification here...
        print(f"📨 Webhook: Verify: sending {amount} to {destination} ")
        return success()

    
    def _create_account(self):
        print(f"⬢ Payment: account: creating account {self.public_key()}...")
        # Create Account
        created = self.sdk.create_account(
            owner=self.keypair,
            commitment=Commitment('Finalized'),
        )
        print(f"⬢ Payment: account: created account {self.sdk.get_explorer_url(f'tx/{created.signature}')}...")
        # Resolve Token Account
        return self.sdk.get_token_accounts(self.public_key())


    def _submit_payment(
        self,
        amount: str,
        destination: str,
        sender_create
    ):
        tx = self.sdk.make_transfer(
            amount = amount,
            commitment = Commitment('Confirmed'),
            destination = destination,
            owner = self.keypair,
            sender_create = sender_create
            # type = 'Earn',
        )

        return {
          'success': True,
          'amount': amount ,
          'destination': destination,
          'tx': tx.signature,
          'explorer': self.sdk.get_explorer_url(f"tx/{tx.signature}"),
        }
