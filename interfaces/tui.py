from blessed import Terminal
term = Terminal()

import config
import can_utils

columns = config.get('GUI').get('Sensors')

Motor = config.get('GUI').get('Sensors').get('Motor')
TSI = config.get('GUI').get('Sensors').get('TSI')

def update():
	print(term.clear())

	motor_data = []

	for key in Motor:
		target = Motor.get(key).get('data_target')
		value = can_utils.data_cache.get(target)
		motor_data.append((key, value))

	print_column(motor_data, 'MOTOR:', 10, 0)

	tsi_data = []

	for key in TSI:
		target = TSI.get(key).get('data_target')
		value = can_utils.data_cache.get(target)
		tsi_data.append((key, value))

	print_column(tsi_data, 'TSI:', 50, 0)

def print_column(data, label, x=0, y=0):
	
	print(term.move_y((term.height // 2) - len(data) // 2 ))

	col = ''

	col += term.move_x(x)
	col += term.bold_underline(label)
	col += term.move_down(1)

	for name, value in data:
		col += term.move_x(x)
		col += '{}'.format(name)
		col += term.move_x(x + 20)
		col += '{}'.format(value)

		col += term.move_down(1)


	print(col)

import threading

def update_timer():

	update()
	threading.Timer(0.1, update_timer).start()

def begin():
	with term.fullscreen():
		update_timer()