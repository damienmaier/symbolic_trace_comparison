import json
import pathlib

BACKEND_TRACE_FILE = pathlib.Path('/tmp/backend_trace.json')
SYMQEMU_TRACE_ADDRESSES_FILE = pathlib.Path('/tmp/symqemu_addresses.json')
MAX_DISTANCE = 0x10000

with open(BACKEND_TRACE_FILE) as file:
    backend_trace = json.load(file)

with open(SYMQEMU_TRACE_ADDRESSES_FILE) as file:
    symqemu_addresses = json.load(file)

for entry in backend_trace:
    print(f'pc : {hex(entry["pc"])}')
    for address in entry['symbolicAddresses']:

        def is_close(area) -> bool:
            return area['address'] <= address <= area['address'] + MAX_DISTANCE

        def distance(area) -> int:
            return address - area['address']

        close_areas = list(filter(is_close, symqemu_addresses))
        if close_areas:
            closest_area = min(close_areas, key=distance)
            address_to_print = f'{closest_area["name"]}+{hex(distance(closest_area))}'
        else:
            address_to_print = hex(address)

        print(f'    {address_to_print}')