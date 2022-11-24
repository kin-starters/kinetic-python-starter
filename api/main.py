from server import server

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(server.app, host="0.0.0.0", port=8001, log_level="debug")

