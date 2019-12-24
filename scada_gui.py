import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as tk_ScrolledText

# Load the YAML config file
# Should probably be handled by another module eventually
import yaml
config = {}
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)


# Define a class to implement the GUI
# Inherits from a Tkinter Frame
class SCADA_GUI(tk.Frame):
	
	# Init and store the parent Frame
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.master = master
		self.init_window()


	# Begin initializing the GUI
	def init_window(self):
		self.master.title('pySCADA GUI')
		self.master.geometry('1280x720')
		self.master.resizable(0, 0)

		# Configure tabs
		self.tabs_parent = ttk.Notebook(self.master)
		self.sensor_data_tab = ttk.Frame(self.tabs_parent)
		self.chart_tab = ttk.Frame(self.tabs_parent)
		self.system_config_tab = ttk.Frame(self.tabs_parent)
		self.candump_tab = ttk.Frame(self.tabs_parent)
		self.scada_log_tab = ttk.Frame(self.tabs_parent)
		self.scada_config_tab = ttk.Frame(self.tabs_parent)
		self.tabs_parent.add(self.sensor_data_tab, text='Sensor Data')
		self.tabs_parent.add(self.chart_tab, text='Live Charts')
		self.tabs_parent.add(self.system_config_tab, text='Config System')
		self.tabs_parent.add(self.candump_tab, text='CAN Dump')
		self.tabs_parent.add(self.scada_log_tab, text='SCADA Log')
		self.tabs_parent.add(self.scada_config_tab, text='SCADA Config File')
		self.tabs_parent.pack(fill=tk.BOTH, expand=True)

		# Create the Sensor Data tab
		self.init_tab_sensorData()
		
		# Create the Live Charts tab
		self.init_tab_liveCharts()
		
		# Create the Config System tab
		self.init_tab_configSystem()
		
		# Create the CAN Dump tab
		self.init_tab_canDump()
		
		# Create the SCADA Log tab
		self.init_tab_scadaLog()
		
		# Create the SCADA Config File tab
		self.init_tab_scadaConfigFile()


	# Construct the Sensor Data tab
	def init_tab_sensorData(self):
		# Sensor Data tab setup
		sensorValues = {}
		sensorInfoFrame = tk.LabelFrame(self.sensor_data_tab, text='Sensors', relief=tk.RIDGE, borderwidth=3)
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
		driveFSMFrame = tk.LabelFrame(self.sensor_data_tab, text='Drive State FSM', relief=tk.RIDGE, borderwidth=3)
		driveFSMFrame.pack(padx=2, pady=2, fill=tk.BOTH, expand=False)
		driveFSMNodes = config['drive_states']
		for node in driveFSMNodes:
			label = tk.Label(driveFSMFrame, text=node, relief=tk.GROOVE, bg='dodger blue', height=2)
			label.pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)
			driveFSMLabels[node] = label

		sloopFrame = tk.LabelFrame(self.sensor_data_tab, text='Safety Loop', relief=tk.RIDGE, borderwidth=3)
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
		print('Init Sensor Data tab complete')


	# Construct the Live Charts tab
	def init_tab_liveCharts(self):
		print('Init Live Charts tab complete')


	# Construct the Config System tab
	def init_tab_configSystem(self):
		print('Init Config System tab complete')


	# Construct the CAN Dump tab
	def init_tab_canDump(self):
		print('Init CAN Dump tab complete')


	# Construct the SCADA Log tab
	def init_tab_scadaLog(self):
		print('Init SCADA Log tab complete')


	# Construct the SCADA Config File tab
	def init_tab_scadaConfigFile(self):
		self.configScrolledText = tk_ScrolledText.ScrolledText(self.scada_config_tab)
		self.configScrolledText.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
		self.configScrolledText.insert(tk.INSERT, yaml.dump(config))
		self.configScrolledText.config(state=tk.DISABLED)
		print('Init SCADA Config tab complete')

# \/ For testing the class only \/
root = tk.Tk()
app = SCADA_GUI(root)
app.mainloop()