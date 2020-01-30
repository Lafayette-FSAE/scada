from blessed import Terminal

term = Terminal()

data = [
	('test', 14),
	('second', 17),
	('second', 13),
]

def print_column(data, label, x=0, y=0):
	print(term.move_y((term.height // 2) - len(data) // 2 ))

	col = ''

	col += term.move_x(10)
	col += term.bold_underline(label)
	col += term.move_down(1)

	for name, value in data:
		col += term.move_x(10)
		col += '{}'.format(name)
		col += term.move_x(30)
		col += '{}'.format(value)


		 #{value}'.format(name=name, value=value)
		col += term.move_down(1)


	print(col)

def begin():
	with term.fullscreen():
		print_column(data, label='TSI')
		# term.inkey()