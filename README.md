# kinetic-python-starter

This starter shows how to implement a simple API that allows you to send KIN to a Solana account using [Kinetic](https://github.com/kin-labs/kinetic).

Read the details in `.env.example` about how to create an Payment Account.

Make sure to protect your endpoints for malicious users, so they don't drain your Payment Account.

It also implements the webhook listener for the Kinetic API.

## Requirements

- Basic Python knowledge
- Python 3.10+
- Poetry 1.20.x

## Running this project

### 1. Clone the repo

```shell
git clone https://github.com/kin-starters/kinetic-python-starter
cd kinetic-python-starter
```

### 2. Install the dependencies

```shell
make install
```

### 3. Configure your environment

You need to create the `.env` file and configure the settings. All the env vars are required.

Read the `.env.example` file for configuration options.

```shell
// Or use your editor to copy the file...
cp .env.example .env
```

### 4. Run the server

```shell
make start
```

### 5. Invoke the endpoint

You can now invoke the `/payment` endpoint on the API, adding the public key of the Solana destination account as the first and the amount of KIN to send as second parameter:

```shell
curl http://localhost:9876/payment/FaFGzKRFhrQffH7voPUgzpJA2ngsvJvtYPXcye6w4DJ9/42
```
