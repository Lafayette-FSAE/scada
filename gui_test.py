import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as tk_ScrolledText
import yaml

# Load the YAML config file
config = {}
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)

# Create base window
root = tk.Tk()
root.geometry('1280x720')
root.resizable(0, 0)
root.title('pySCADA GUI')

# Configure tabs
tabs_parent = ttk.Notebook(root)
default_tab = ttk.Frame(tabs_parent)
chart_tab = ttk.Frame(tabs_parent)
system_config_tab = ttk.Frame(tabs_parent)
candump_tab = ttk.Frame(tabs_parent)
scada_log_tab = ttk.Frame(tabs_parent)
scada_config_tab = ttk.Frame(tabs_parent)
tabs_parent.add(default_tab, text='Sensor Data')
tabs_parent.add(chart_tab, text='Live Charts')
tabs_parent.add(system_config_tab, text='Config System')
tabs_parent.add(candump_tab, text='CAN Dump')
tabs_parent.add(scada_log_tab, text='SCADA Log')
tabs_parent.add(scada_config_tab, text='SCADA Config File')
tabs_parent.pack(fill=tk.BOTH, expand=True)

# Sensor Data tab setup
sensorValues = {}
sensorInfoFrame = tk.LabelFrame(default_tab, text='Sensors', relief=tk.RIDGE, borderwidth=3)
sensorInfoFrame.pack(padx=2, pady=2, fill=tk.Y, expand=True)
sensorGroups = config['sensors']
for group in sensorGroups:
	frame = tk.LabelFrame(sensorInfoFrame, text=group, relief=tk.RIDGE, borderwidth=2)
	frame.pack(side='left', padx=5, pady=10, fill=tk.Y, expand=True)
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

driveFSMLabels = {}
driveFSMFrame = tk.LabelFrame(default_tab, text='Drive State FSM', relief=tk.RIDGE, borderwidth=3)
driveFSMFrame.pack(padx=2, pady=2, fill=tk.BOTH, expand=False)
driveFSMNodes = config['drive_states']
for node in driveFSMNodes:
	label = tk.Label(driveFSMFrame, text=node, relief=tk.GROOVE, bg='dodger blue', height=2)
	label.pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)
	driveFSMLabels[node] = label

sloopFrame = tk.LabelFrame(default_tab, text='Safety Loop', relief=tk.RIDGE, borderwidth=3)
sloopFrame.pack(padx=2, pady=2, fill=tk.BOTH, expand=False)
sloopSystemLabels = {}
sloopSystemFrame = tk.LabelFrame(sloopFrame, text='Systems')
sloopSystemFrame.pack(side='top', padx=2, pady=2, fill=tk.BOTH, expand=True)
sloopSystems = config['sloop_systems']
for system in sloopSystems:
	label = tk.Label(sloopSystemFrame, text=system, relief=tk.GROOVE, bg='salmon', height=2)
	label.pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)
	sloopSystemLabels[system] = label
sloopNodeLabels = {}
sloopNodeFrame = tk.LabelFrame(sloopFrame, text='Nodes')
sloopNodeFrame.pack(side='bottom', padx=2, pady=2, fill=tk.BOTH, expand=True)
sloopNodes = config['sloop_nodes']
for node in sloopNodes:
	label = tk.Label(sloopNodeFrame, text=node, relief=tk.GROOVE, bg='green2', height=2)
	label.pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)
	sloopNodeLabels[node] = label

# SCADA Config File tab setup
configScrolledText = tk_ScrolledText.ScrolledText(scada_config_tab)
configScrolledText.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
configScrolledText.insert(tk.INSERT, yaml.dump(config))
configScrolledText.config(state=tk.DISABLED)

root.mainloop()