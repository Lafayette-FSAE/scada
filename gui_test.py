import tkinter as tk
import tkinter.ttk as ttk
import yaml

config = {}
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

# for group in config['sensors']:
# 	print(group)
# 	for sensor in config['sensors'][group]:
# 		print(sensor)

root = tk.Tk()
root.geometry('1280x720')
root.title('pySCADA GUI')

sensorInfoFrame = tk.LabelFrame(root, text='Sensors', relief=tk.RIDGE, borderwidth=3)
sensorInfoFrame.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)
sensorGroups = config['sensors']
for node in sensorGroups:
	frame = tk.LabelFrame(sensorInfoFrame, text=node, relief=tk.RIDGE, borderwidth=2)
	frame.pack(side='left', padx=10, pady=10, fill=tk.BOTH, expand=True)
	for sensor in sensorGroups[node]:
		label = tk.Label(frame, text=sensor)
		label.pack(padx=5, pady=5)

driveFSMFrame = tk.LabelFrame(root, text='Drive State FSM', relief=tk.RIDGE, borderwidth=3)
driveFSMFrame.pack(padx=2, pady=2, fill=tk.BOTH, expand=False)
driveFSMNodes = config['drive_states']
for node in driveFSMNodes:
	tk.Label(driveFSMFrame, text=node, relief=tk.GROOVE, bg='dodger blue', height=2).pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)

sloopFrame = tk.LabelFrame(root, text='Safety Loop State', relief=tk.RIDGE, borderwidth=3)
sloopFrame.pack(padx=2, pady=2, fill=tk.BOTH, expand=False)
sloopNodes = config['sloop_nodes']
for node in sloopNodes:
	tk.Label(sloopFrame, text=node, relief=tk.GROOVE, bg='green2', height=2).pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()