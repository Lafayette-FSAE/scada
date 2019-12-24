import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as tk_ScrolledText

from time import strftime

# Load the YAML config file
# Should probably be handled by another module eventually
import yaml
config = {}
with open("config.yaml", 'r') as stream:
	try:
		config = yaml.safe_load(stream)
	except yaml.YAMLError as exc:
		print(exc)


# Define a class to implement the SCADA App and GUI
# Inherits from a Tkinter Frame
class SCADA_APP(tk.Frame):
	
	# Init and store the parent Frame and init the application
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
		self.tabsParent = ttk.Notebook(self.master)
		self.sensorDataTab = ttk.Frame(self.tabsParent)
		self.liveChartTab = ttk.Frame(self.tabsParent)
		self.systemConfigTab = ttk.Frame(self.tabsParent)
		self.canDumpTab = ttk.Frame(self.tabsParent)
		self.scadaLogTab = ttk.Frame(self.tabsParent)
		self.scadaConfigTab = ttk.Frame(self.tabsParent)
		self.tabsParent.add(self.sensorDataTab, text='Sensor Data')
		self.tabsParent.add(self.liveChartTab, text='Live Charts')
		self.tabsParent.add(self.systemConfigTab, text='Config System')
		self.tabsParent.add(self.canDumpTab, text='CAN Dump')
		self.tabsParent.add(self.scadaLogTab, text='SCADA Log')
		self.tabsParent.add(self.scadaConfigTab, text='SCADA Config File')
		self.tabsParent.pack(side='top', fill=tk.BOTH, expand=True)

		# Construct the tabs
		self.init_tab_sensorData()			# Create the Sensor Data tab
		self.init_tab_liveCharts()			# Create the Live Charts tab
		self.init_tab_configSystem()		# Create the Config System tab
		self.init_tab_canDump()				# Create the CAN Dump tab
		self.init_tab_scadaLog()			# Create the SCADA Log tab
		self.init_tab_scadaConfigFile()		# Create the SCADA Config File tab

		# Create status bar
		self.statusBar = tk.Frame(self.master, relief=tk.SUNKEN, borderwidth=1)
		self.statusBar.pack(side='bottom', padx=2, pady=2, fill=tk.X, expand=False)
		self.exitButton = tk.Button(self.statusBar, text='Quit', command=quit, width=10)
		self.exitButton.pack(side='right', padx=2, pady=2)
		self.timeValue = tk.StringVar()
		self.timeValue.set('00:00:00 AM')
		self.timeLabel = tk.Label(self.statusBar, textvariable=self.timeValue)
		self.timeLabel.pack(side='left', padx=2, pady=2)


	# Construct the Sensor Data tab
	def init_tab_sensorData(self):
		sensorValues = {}
		sensorInfoFrame = tk.LabelFrame(self.sensorDataTab, text='Sensors')
		sensorInfoFrame.pack(padx=2, pady=2, fill=tk.Y, expand=True)
		sensorGroups = config['sensors']
		for group in sensorGroups:
			frame = tk.LabelFrame(sensorInfoFrame, text=group)
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
		driveFSMFrame = tk.LabelFrame(self.sensorDataTab, text='Drive State FSM')
		driveFSMFrame.pack(padx=2, pady=2, fill=tk.BOTH, expand=False)
		driveFSMNodes = config['drive_states']
		for node in driveFSMNodes:
			label = tk.Label(driveFSMFrame, text=node, relief=tk.GROOVE, bg='dodger blue', height=2)
			label.pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)
			driveFSMLabels[node] = label

		sloopFrame = tk.LabelFrame(self.sensorDataTab, text='Safety Loop')
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
		self.configScrolledText = tk_ScrolledText.ScrolledText(self.scadaConfigTab)
		self.configScrolledText.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
		self.configScrolledText.insert(tk.INSERT, yaml.dump(config))
		self.configScrolledText.config(state=tk.DISABLED)
		print('Init SCADA Config tab complete')


	# Function to update the state of the program outside of the GUI's mainloop
	def update_program(self):
		self.timeValue.set(strftime('%D  %I:%M:%S %p'))
		
		self.master.update_idletasks()
		self.master.after_idle(self.update_program)


	# Quits SCADA
	def quit(self):
		self.master.destroy()


# \/ For testing the class only \/
root = tk.Tk()
app = SCADA_APP(root)
app.update_program()
app.mainloop()