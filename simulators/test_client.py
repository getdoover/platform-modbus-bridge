import time

from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian

# Connect to Modbus server
print("Connecting to Modbus server at 127.0.0.1:5002")
client = ModbusTcpClient("127.0.0.1", port=5002)
client.connect()
print("Connected to Modbus server")

# --- Read a single register (address 10) ---
read_start_time = time.time()
read_result = client.read_holding_registers(100, count=1, slave=1)
print(f"Read duration: {(time.time() - read_start_time) * 1000} ms")
if read_result.isError():
    print("Read error at register 100")
else:
    print(f"Read from register 100: {read_result.registers[0]}")

# # --- Write a single register (address 10) ---
write_value = 123
write_start_time = time.time()
write_result = client.write_register(200, write_value, slave=1)
print(f"Wrote duration: {(time.time() - write_start_time) * 1000} ms")
print(f"Wrote {write_value} to register 200: {write_result}")


# # --- Read multiple registers (starting at address 20) ---
# read_result = client.read_holding_registers(20, count=3, slave=1)
# if read_result.isError():
#     print("Read error at registers 20-22")
# else:
#     print(f"Read from registers 20-22: {read_result.registers}")

# # --- Write multiple registers (starting at address 20) ---
# write_values = [11, 22, 33]
# write_result = client.write_registers(20, write_values, slave=1)
# print(f"Wrote {write_values} to registers starting at 20: {write_result}")

# # --- Write a float to two registers using BinaryPayloadBuilder ---
# builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.LITTLE)
# builder.add_32bit_float(3.14159)
# payload = builder.to_registers()
# client.write_registers(30, payload, slave=1)
# print(f"Wrote float 3.14159 to registers 30-31")

# # --- Read back float value ---
# read_result = client.read_holding_registers(30, count=2, slave=1)
# if not read_result.isError():
#     decoder = BinaryPayloadDecoder.fromRegisters(
#         read_result.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE
#     )
#     float_value = decoder.decode_32bit_float()
#     print(f"Read float from registers 30-31: {float_value}")

# Disconnect
client.close()