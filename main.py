import sys
import can
import can_utils
import config
import logging
import scada_logger



bus = can_utils.bus(config.get('bus_info'))
notifier = can.Notifier(bus, [])

if(config.get('emulate_nodes')):

	# append emulators directory to include path
	sys.path.append('emulators')

	# check which emulators are enabled
	if(config.get('emulate_tsi')):
		import tsi_emulator

		tsi = tsi_emulator.Listener(node_id=3)
		notifier.add_listener(tsi)


	if(config.get('emulate_packs')):
		import ams_emulator

		pack1 = ams_emulator.Listener(node_id=2)
		notifier.add_listener(pack1)

		pack2 = ams_emulator.Listener(node_id=1)
		notifier.add_listener(pack2)

	if(config.get('emulate_cockpit')):
		pass

	if(config.get('emulate_motorcontroller')):
		pass


# modules
sys.path.append('modules')
sys.path.append('calibration')

import data_processor
processor = data_processor.Listener(node_id=4)

notifier.add_listener(processor)

sync = can.Message(arbitration_id=0x80, data=0x00)
sync.is_extended_id = False

read = can_utils.messages.sdo_read(node_id=2, index=[0x30, 0x01], subindex=0x02)

master_bus = can_utils.bus(config.get('bus_info'))
master_bus.send_periodic(sync, .1)


# \/				   \/
# \/  GUI Integration  \/
# \/				   \/


from scada_gui import SCADA_GUI
from time import strftime

app = SCADA_GUI()
scada_logger.set_text_window(app.scadaLogScrolledText)

app.set_value('GLV', 'Voltage', '24 V') # Test changing a value

test_value = 10

class GUIListener(can.Listener):
	def __init__(self, node_id, gui):
		self.node_id = node_id
		self.gui = gui

	def on_message_received(self, msg):
		global test_value
		function, node_id = can_utils.messages.get_info(msg)
		if function == 'PDO' and node_id == 3:
			# test_value = int(msg.data[4])
			pass

guiListener = GUIListener(node_id=6, gui=app)
notifier.add_listener(guiListener)

while app.running:

	app.set_value('TSI', 'HV Current', '{} A'.format(can_utils.data_cache.get('TSI', 'CURRENT')))
	app.set_value('TSI', 'High Voltage', '{} hundred W'.format(can_utils.data_cache.get('SCADA', 'TS_POWER')))
	app.timeValue.set(strftime('%D  %I:%M:%S %p'))
	app.update_idletasks()
	app.update()

app.destroy()
