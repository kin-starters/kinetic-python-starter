from kinetic_sdk import Keypair

mnemonic = Keypair.generate_mnemonic()
keypair = Keypair.from_mnemonic(mnemonic)