"""
Basic tests for an application.

This ensures all modules are importable and that the config is valid.
"""

def test_import_app():
    from platform_modbus_bridge.application import PlatformModbusBridgeApplication
    assert PlatformModbusBridgeApplication

def test_config():
    from platform_modbus_bridge.app_config import PlatformModbusBridgeConfig

    config = PlatformModbusBridgeConfig()
    assert isinstance(config.to_dict(), dict)