import logging

log = logging.getLogger(__name__)

def handle_address_read(reg_map, plt, address, count=1):
    log.debug(f"handle_address_read for address {address} count={count}")
    if address not in reg_map:
        log.warning(f"handle_address_read for address {address} count={count} not in reg_map")
        return [0] * count

    reg = reg_map[address]
    if "read" not in reg:
        log.warning(f"handle_address_read for address {address} count={count} no read method")
        return [0] * count
    
    read_call = reg["read"]["call"]
    read_args = reg["read"]["read_args"]
    read_divisor = reg["read"].get("divisor", 1)
    read_multiplier = reg["read"].get("multiplier", 1)
    read_clean_func = reg["read"].get("clean_func", lambda x: x)
    
    # Use getattr to dynamically call the method on the platform interface
    method = getattr(plt, read_call)
    log.debug(f"handle_address_read for address {address} count={count} calling {read_call} with args {read_args}")
    
    # Handle both positional and keyword arguments
    if "args" in read_args:
        # Use positional arguments
        result = method(*read_args["args"])
    else:
        # Use keyword arguments
        result = method(**read_args)
    
    log.debug(f"handle_address_read for address {address} count={count} result={result}")
    
    # Handle single value vs list of values
    if not isinstance(result, list):
        result = [result]
    
    # Apply divisor and multiplier, then clean function
    return [read_clean_func((x / read_divisor) * read_multiplier) for x in result]


def handle_address_write(reg_map, plt, address, values):
    log.debug(f"handle_address_write for address {address} values={values}")
    if address not in reg_map:
        return False

    reg = reg_map[address]
    if "write" not in reg:
        return False
    
    write_call = reg["write"]["call"]
    write_args = reg["write"].get("write_args", {})
    write_divisor = reg["write"].get("divisor", 1)
    write_multiplier = reg["write"].get("multiplier", 1)
    write_clean_func = reg["write"].get("clean_func", lambda x: x)
    write_value_key = reg["write"].get("write_value_key", "value")
    
    # Use getattr to dynamically call the method on the platform interface
    method = getattr(plt, write_call)
    
    # Handle each value in the list
    for i, value in enumerate(values):
        # Apply clean function and multiplier
        processed_value = write_clean_func((value/write_divisor) * write_multiplier)
        
        # Call the method with the processed value
        if len(write_args) > 0:
            # If there are predefined args, use them and append the value
            method(**write_args, **{write_value_key: processed_value})
        else:
            # If no predefined args, just pass the value
            method(processed_value)
    
    return True


def gen_holding_registers():

    registers = {}

    # If the register is read-only, we need to not set the write args
    # If the register is write-only, we need to not set the read args

    ## For the first 100 registers, just map to digital inputs
    for i in range(100):
        registers[i] = {
            "read": {"call": "get_di", "read_args": {"args": [i]}},
        }

    ## For the next 100 registers, map to analog inputs where the value is the analog input value / 1000
    for i in range(100, 200):
        registers[i] = {
            "read": {"call": "get_ai", "read_args": {"args": [i - 100]}, "divisor": 1000},
        }

    ## For the next 100 registers, map to digital outputs
    for i in range(200, 300):
        registers[i] = {
            "read": {"call": "get_do", "read_args": {"args": [i - 200]}, "clean_func": lambda x: x > 0},
            "write": {"call": "set_do", "write_args": {"do": i - 200}, "write_value_key": "value", "clean_func": lambda x: x > 0}
        }

    ## For the next 100 registers, map to analog outputs where the value is the analog output value * 1000
    for i in range(300, 400):
        registers[i] = {
            "read": {"call": "get_ao", "read_args": {"args": [i - 300]}, "multiplier": 1000},
            "write": {"call": "set_ao", "write_args": {"ao": i - 300}, "write_value_key": "value", "multiplier": 1000}
        }

    ## Set some special registers
    registers[401] = {
        "read": {"call": "get_system_voltage", "read_args": {}, "divisor": 1000},
    }
    registers[402] = {
        "read": {"call": "get_system_temperature", "read_args": {}, "divisor": 100}, 
    }
    registers[403] = {
        "read": {"call": "get_immunity_seconds", "read_args": {}},
        "write": {"call": "set_immunity_seconds", "write_args": {}},
    }
    registers[404] = {
        "write": {"call": "schedule_startup", "write_args": {}},
    }
    registers[405] = {
        "write": {"call": "schedule_shutdown", "write_args": {}},
    }
    registers[406] = {
        "write": {"call": "shutdown", "write_args": {}},
    }
    return registers