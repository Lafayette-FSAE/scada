import can
import time

Pack_id = 0x0A

bus = can.interface.Bus(
	bustype='socketcan',
	channel='can0',
	bitrate=125000
)

# index_lookup = {
	
# }

# Make SDO requests for all Cell Temperatures
def get_cell_temps():
	cells = []

	for index in range(1,5):
		print(index)

		message = can.Message(
			arbitration_id = 0x60A,
			data = [0x40, 0x03, 0x30, index, 0x00, 0x00, 0x00, 0x00]
		)

		message.is_extended_id = False

		bus.send(message)

		time.sleep(0.1)
get_cell_temps()