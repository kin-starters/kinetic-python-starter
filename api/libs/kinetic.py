from kinetic_sdk import Keypair
from kinetic_sdk import KineticSdk

# import { AppConfigMint, KineticSdk, Transaction } from '@kin-kinetic/sdk'
# import { Commitment, TransactionType } from '@kin-kinetic/solana'

# import { ServerConfig } from '../server/server-config'

class Kinetic(object):

    def __init__(self, config, sdk: KineticSdk, keypair: Keypair):
        self.config = config
        self.sdk = sdk
        self.keypair = keypair


    def mint(self):
        return self.sdk.config.mint


    def public_key(self):
        return self.keypair.public_key


    def payment(self, amount: int, destination: str):
        # Check if amount is below the maximum
        if amount > int(self.config.payment_max):
            raise f"Payment amount is too large, max is {self.config.payment_max}"
    
        # If we don't allow funding existing accounts, check if the destination account has funds
        if self.config.payment_allow_existing is None:
            # Check to see if the destination account already has funds
            result = self.sdk.get_balance(destination)

            if result['balance'] is not 0:
                raise f"Account '{destination}' is already funded: {result['balance']} Kin"
    
        # If we don't allow new accounts, check to see if the account exists
        if self.config.payment_allow_new is None:
            found = self.sdk.get_token_accounts(destination)

            if len(found) == 0:
                raise f"Can't send payment to new account {destination}."
    

        try:
            print(f"⬢ Payment: sending {amount} Kin to {destination}...")
            tx = self.submit_payment(
                amount,
                destination,
                sender_create=self.config.payment_allow_new
            )
            print(f"⬢ Payment: sent {amount} Kin to {destination}... {tx.explorer} ")
            return tx
        except Exception as err:
            raise f"Account {destination} something went wrong: {err} "


    def find_or_create_account(self):
        """ Helper function initializes the account. """
        public_key = self.public_key()

        print(f"⬢ Payment: account: {self.sdk.get_explorer_url(f'address/{public_key}')}")
        print(f"⬢ Payment: address: ${public_key}")
        print(f"⬢ Payment: allow empty accounts: {'yes' if self.config.payment_allow_new is True else 'no'}")
        print(f"⬢ Payment: allow existing accounts: {'yes' if self.config.payment_allow_existing is True else 'no'}")
        print(f"⬢ Payment: max: {self.config.paymentMax}")
        print(f"⬢ Payment: secret: {'enabled' if self.config.payment_secret is True else 'disabled'}")

        account = self.sdk.get_balance(self.public_key)

        print(f"⬢ Payment: balance: ${account.balance} {self.mint.symbol} ")

        if account.balance is '0':
            # If the default Kinetic mint has airdrop enabled, we can fund ourselves...
            if self.mint.airdrop and self.mint.airdrop_max is not None:
                print(f"⬢ Payment: account: {public_key} is empty, requesting airdrop of {str(self.mint.airdrop_max)} {self.mint.symbol}...")

                tx = self.sdk.request_airdrop(
                    account=self.public_key,
                    amount=str(self.mint.airdrop_max)
                )

                print(f"⬢ Payment: request: {self.sdk.get_explorer_url(f'tx/{tx.signature}')}")
            else:
                print(f"⬢ Payment: account: Make sure to fund this account with some {self.mint.symbol}.")


    def handle_balance_webhook(self, balance: str, change: str, error, success):
        print(f"📨 Webhook: Balance: { balance, change }") # FIXME: Stringify
        return success()


    def handle_event_webhook(self, transaction, error, success):
        amount = transaction.amount
        destination = transaction.destination
        signature = transaction.signature

        print(f"📨 Webhook: Event: sent {amount} to {destination} {self.sdk.get_explorer_url(f'tx/{signature}')}")
        return success()


    def handle_verify_webhook(self, transaction, error, success):
        amount = transaction.amount
        destination = destination.amount

        # Check if the amount is above the minimum
        if int(amount) < 100:
            return Exception('Amount too low...')

        # Check if the destination address is not the payment account
        if destination == self.public_key:
            return Exception('Destination is payment account...')

        # Add your own verification here...
        print(f"📨 Webhook: Verify: sending {amount} to {destination} ")
        return success()

    
    def _create_account(self):
        print(f"⬢ Payment: account: creating account {self.public_key()}...")
        # Create Account
        created = self.sdk.create_account(
            owner=self.keypair,
            commitment='Finalized',
        )
        print(f"⬢ Payment: account: created account {self.sdk.get_explorer_url(f'tx/${created.signature}')}...")
        # Resolve Token Account
        return self.sdk.get_token_accounts(self.public_key())


    def _submit_payment(
        self,
        amount: str,
        destination: str,
        sender_create: bool
    ):
        tx = self.sdk.make_transfer(
            amount = amount,
            commitment = 'Confirmed',
            destination = destination,
            owner = self.keypair,
            sender_create = sender_create,
            type = 'Earn',
        )

        return {
          'success': True,
          'amount': amount ,
          'destination': destination,
          'tx': tx.signature,
          'explorer': self.sdk.get_explorer_url(f"tx/{tx.signature}"),
        }
