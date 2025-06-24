import asyncio
from pydoover.docker import run_app

from .application import PlatformModbusBridge
from .app_config import PlatformModbusBridgeConfig

def main():
    """
    Run the application.
    """
    # run_app(PlatformModbusBridgeApplication(config=PlatformModbusBridgeConfig()))

    ## Run the modbus bridge here.
    bridge = PlatformModbusBridge()
    asyncio.run(bridge.run_server())
