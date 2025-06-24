import asyncio
from pydoover.docker import run_app

from .application import PlatformModbusBridge
from .app_config import PlatformModbusBridgeConfig

def main():
    """
    Run the application.
    """
    # run_app(PlatformModbusBridgeApplication(config=PlatformModbusBridgeConfig()))

    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 5002

    ## Run the modbus bridge here.
    bridge = PlatformModbusBridge()
    asyncio.run(bridge.run_server(SERVER_IP, SERVER_PORT))

