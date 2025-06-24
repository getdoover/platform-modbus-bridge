import logging
from typing import Any, Optional

from pydoover.docker import PlatformInterface

from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore.store import BaseModbusDataBlock
from pymodbus.device import ModbusDeviceIdentification

from .mappings import gen_holding_registers, handle_address_read, handle_address_write

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class VirtualBlock(BaseModbusDataBlock):
    """
    A data block that can just resolve results from read/write operations.
    """
    
    def __init__(self, reg_map: Optional[dict[int, dict[str, Any]]] = None, platform_interface: PlatformInterface = None):
        self.reg_map = reg_map
        self.platform_interface = platform_interface
    
    def validate(self, address, count=1):
        return True  # assume always valid

    def getValues(self, address, count=1):
        """Synchronous method called by pymodbus - we need to handle this carefully"""
        try:
            log.debug(f"getValues for at address {address} count={count}")
            if self.reg_map is None:
                return [0] * count
            return handle_address_read(self.reg_map, self.platform_interface, address, count)
        except Exception as e:
            log.error(f"Error in getValues for at address {address}: {e}")
            return [0] * count

    def setValues(self, address, values):
        """Synchronous method called by pymodbus - we need to handle this carefully"""
        try:
            log.debug(f"setValues for at address {address} values={values}")
            if self.reg_map is None:
                return False
            return handle_address_write(self.reg_map, self.platform_interface, address, values)
        except Exception as e:
            log.error(f"Error in setValues for at address {address}: {e}")


class PlatformModbusBridge:

    def __init__(self):
        log.info("PlatformModbusBridge initialized")
        self.platform_interface = PlatformInterface(app_key="", plt_uri="localhost:50053")

    async def run_server(self, server_ip: str = "0.0.0.0", server_port: int = 5002):
        log.info("Setting up Modbus server...")
        
        # Create data blocks with async callbacks
        store = ModbusSlaveContext(
            di=VirtualBlock(None, self.platform_interface),
            co=VirtualBlock(gen_holding_registers(), self.platform_interface),
            hr=VirtualBlock(gen_holding_registers(), self.platform_interface),
            ir=VirtualBlock(gen_holding_registers(), self.platform_interface),
        )
        context = ModbusServerContext(slaves=store, single=True)

        identity = ModbusDeviceIdentification()
        identity.VendorName = 'Doover'
        identity.ProductName = 'Platform Modbus Bridge'
        identity.ModelName = 'PlatformModbusBridge'
        identity.MajorMinorRevision = '1.0'

        log.info(f"Starting async Modbus TCP server on {server_ip}:{server_port}")
        try:
            await StartAsyncTcpServer(context, identity=identity, address=(server_ip, server_port))
        except Exception as e:
            log.error(f"Failed to start Modbus server: {e}")
            raise
        log.info("Modbus server finished")