from kinetic_sdk import Keypair

def generate_keypair():
    mnemonic = Keypair.generate_mnemonic()
    keypair = Keypair.from_mnemonic(mnemonic)

    print('Generated keypair:', { 
        'mnemonic': str(keypair.mnemonic),
        'secret_key': keypair.secret_key,
        'public_key': keypair.public_key
    })

if __name__ == "__main__":
    generate_keypair()
