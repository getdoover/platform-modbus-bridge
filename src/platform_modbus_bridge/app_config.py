from pathlib import Path

from pydoover import config


class PlatformModbusBridgeConfig(config.Schema):
    def __init__(self):
        # these 2 are device specific, and inherit from the device-set variables.
        # However, the user can override them if they wish.

        self.modbus_host = config.String("Modbus Host", default="0.0.0.0", description="The host to listen on for modbus connections. 0.0.0.0 means listen on all interfaces.")
        self.modbus_port = config.Integer("Modbus Port", default=5002, minimum=1, maximum=65535, description="The port to listen on for modbus connections.")

        self.platform_interface_host = config.String("Platform Interface Host", default="127.0.0.1", description="The host to connect to the platform interface.")
        self.platform_interface_port = config.Integer("Platform Interface Port", default=50053, minimum=1, maximum=65535, description="The port to connect to the platform interface.")

        # self.sim_app_key = config.Application("Simulator App Key", description="The app key for the simulator")


if __name__ == "__main__":
    PlatformModbusBridgeConfig().export(Path(__file__).parent.parent.parent / "doover_config.json", "platform_modbus_bridge")
