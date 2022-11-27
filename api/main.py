from server import server
from server.server_config import get_server_config

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    config = get_server_config()

    uvicorn.run(server.app, host="0.0.0.0", port=int(config['port']), log_level="debug")

