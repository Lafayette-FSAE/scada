# python3
from tkinter import *
import yaml

config = {}

# read config from config.yaml file
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

window = Tk()
window.title('pySCADA GUI')
label = Label(window, text='Bus type: ' + config['bustype'])
label.pack()
window.mainloop()
