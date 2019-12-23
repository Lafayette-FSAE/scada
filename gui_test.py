import tkinter as tk
import tkinter.ttk as ttk
import yaml

config = {}
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

root = tk.Tk()
# root.geometry('1280x720')
root.resizable(0, 0)
root.title('pySCADA GUI')

sensorValues = {}
sensorInfoFrame = tk.LabelFrame(root, text='Sensors', relief=tk.RIDGE, borderwidth=3)
sensorInfoFrame.pack(padx=2, pady=2, fill=tk.Y, expand=True)
sensorGroups = config['sensors']
for group in sensorGroups:
	frame = tk.LabelFrame(sensorInfoFrame, text=group, relief=tk.RIDGE, borderwidth=2)
	frame.pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)
	i = 0
	maxWidth = 0
	labelValueDict = {}
	for sensor in sensorGroups[group]:
		length = len(sensor)
		if length > maxWidth:
			maxWidth = length
	for sensor in sensorGroups[group]:
		sensorLabel = tk.Label(frame, text=sensor, width=maxWidth, anchor='w')
		sensorLabel.grid(row=i, column=0, padx=5, pady=5)
		labelVar = tk.StringVar()
		labelVar.set('--')
		valueLabel = tk.Label(frame, textvariable=labelVar, width=5, bg='light blue')
		valueLabel.grid(row=i, column=1, padx=5, pady=5)
		labelValueDict[sensor] = labelVar
		i = i + 1
	sensorValues[group] = labelValueDict

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