from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tk_ScrolledText
import config
import logging

# Define a class to implement the SCADA App and GUI
# Inherits from a Tkinter Frame
class SCADA_GUI(Frame):
	
	# Init and store the parent Frame and init the application
	def __init__(self):
		self.master = Tk()
		Frame.__init__(self, self.master)
		self.init_window()
		self.running = True


	# Begin initializing the GUI
	def init_window(self):
		self.master.title('pySCADA')
		# self.master.geometry('1280x720')
		self.master.resizable(0, 0)
		self.master.protocol('WM_DELETE_WINDOW', self.quit_scada) # Calls the quit_scada function when the window is closed

		# Configure tabs
		tabsParent = Notebook(self.master)
		self.sensorDataTab = Frame(tabsParent)	# Create a frame for each tab
		self.liveChartTab = Frame(tabsParent)
		self.systemConfigTab = Frame(tabsParent)
		self.canDumpTab = Frame(tabsParent)
		self.scadaLogTab = Frame(tabsParent)
		self.scadaConfigTab = Frame(tabsParent)
		tabsParent.add(self.sensorDataTab, text='Sensor Data')	# Add each tab's frame to the notebook
		tabsParent.add(self.liveChartTab, text='Live Charts')
		tabsParent.add(self.systemConfigTab, text='Config System')
		tabsParent.add(self.canDumpTab, text='CAN Dump')
		tabsParent.add(self.scadaLogTab, text='SCADA Log')
		tabsParent.add(self.scadaConfigTab, text='SCADA Config File')
		tabsParent.pack(side='top', fill=BOTH, expand=True)

		# Dictionaries that will need to be altered over time
		self.sensorValueVars = {}
		self.sensorValueLabels = {}
		self.driveFSMLabels = {}
		self.sloopSystemLabels = {}
		self.sloopNodeLabels = {}

		# Construct the tabs
		self.init_tab_sensorData()			# Create the Sensor Data tab
		self.init_tab_liveCharts()			# Create the Live Charts tab
		self.init_tab_configSystem()		# Create the Config System tab
		self.init_tab_canDump()				# Create the CAN Dump tab
		self.init_tab_scadaLog()			# Create the SCADA Log tab
		self.init_tab_scadaConfigFile()		# Create the SCADA Config File tab

		# Create status bar
		statusBar = Frame(self.master, relief=SUNKEN, borderwidth=1)
		statusBar.pack(side='bottom', padx=1, pady=1, fill=X, expand=False)
		exitButton = Button(statusBar, text='Quit', command=self.quit_scada, width=10)
		exitButton.pack(side='right', padx=2, pady=2)
		self.timeValue = StringVar()
		self.timeValue.set('0/0/00  00:00:00 AM')
		timeLabel = Label(statusBar, textvariable=self.timeValue)
		timeLabel.pack(side='left', padx=2, pady=2)


	# Construct the Sensor Data tab
	def init_tab_sensorData(self):
		sensorInfoFrame = LabelFrame(self.sensorDataTab, text='Sensors')
		sensorInfoFrame.pack(padx=2, pady=2, fill=Y, expand=True)
		sensorGroups = config.get('GUI').get('Sensors')
		for group in sensorGroups:
			frame = LabelFrame(sensorInfoFrame, text=group)
			frame.pack(side='left', padx=5, pady=10, fill=Y, expand=True)
			i = 0
			maxWidth = 0
			valueVarDict = {}
			valueLabelDict = {}
			for sensor in sensorGroups[group]:
				length = len(sensor)
				if length > maxWidth:
					maxWidth = length
			for sensor in sensorGroups[group]:
				sensorLabel = Label(frame, text=sensor, width=maxWidth+2, anchor='w')
				sensorLabel.grid(row=i, column=0, padx=5, pady=5)
				labelVar = StringVar()
				labelVar.set('--')
				valueLabel = Label(frame, textvariable=labelVar, width=6, anchor='center', background='light blue')
				valueLabel.grid(row=i, column=1, padx=5, pady=5)
				valueVarDict[sensor] = labelVar
				valueLabelDict[sensor] = valueLabel
				i = i + 1
			self.sensorValueVars[group] = valueVarDict
			self.sensorValueLabels[group] = valueLabelDict

		driveFSMFrame = LabelFrame(self.sensorDataTab, text='Drive State FSM')
		driveFSMFrame.pack(padx=2, pady=2, fill=BOTH, expand=False)
		driveFSMNodes = config.get('GUI').get('Drive States')
		for node in driveFSMNodes:
			frame = Frame(driveFSMFrame, height=30, width=0)
			frame.pack(side='left', padx=10, pady=10, fill=BOTH, expand=True)
			frame.pack_propagate(0)
			label = Label(frame, text=node, anchor='center', relief=GROOVE, background='dodger blue')
			label.pack(padx=0, pady=0, fill=BOTH, expand=True)
			self.driveFSMLabels[node] = label

		sloopFrame = LabelFrame(self.sensorDataTab, text='Safety Loop')
		sloopFrame.pack(padx=2, pady=2, fill=BOTH, expand=False)
		sloopSystemFrame = LabelFrame(sloopFrame, text='Systems')
		sloopSystemFrame.pack(side='top', padx=2, pady=2, fill=BOTH, expand=True)
		sloopSystems = config.get('GUI').get('Safety Loop Systems')
		for system in sloopSystems:
			frame = Frame(sloopSystemFrame, height=30, width=0)
			frame.pack(side='left', padx=10, pady=10, fill=BOTH, expand=True)
			frame.pack_propagate(0)
			label = Label(frame, text=system, anchor='center', relief=GROOVE, background='salmon')
			label.pack(padx=0, pady=0, fill=BOTH, expand=True)
			self.sloopSystemLabels[system] = label
		sloopNodeFrame = LabelFrame(sloopFrame, text='Nodes')
		sloopNodeFrame.pack(side='bottom', padx=2, pady=2, fill=BOTH, expand=True)
		sloopNodes = config.get('GUI').get('Safety Loop Nodes')
		for node in sloopNodes:
			frame = Frame(sloopNodeFrame, height=30, width=0)
			frame.pack(side='left', padx=10, pady=10, fill=BOTH, expand=True)
			frame.pack_propagate(0)
			label = Label(frame, text=node, anchor='center', relief=GROOVE, background='green2')
			label.pack(padx=0, pady=0, fill=BOTH, expand=True)
			self.sloopNodeLabels[node] = label
		logging.info('Init Sensor Data tab complete')


	# Construct the Live Charts tab
	def init_tab_liveCharts(self):
		logging.info('Init Live Charts tab complete')


	# Construct the Config System tab
	def init_tab_configSystem(self):
		logging.info('Init Config System tab complete')


	# Construct the CAN Dump tab
	def init_tab_canDump(self):
		self.canDumpScrolledText = tk_ScrolledText.ScrolledText(self.canDumpTab)
		self.canDumpScrolledText.pack(padx=10, pady=10, fill=BOTH, expand=True)
		self.canDumpScrolledText.config(state=DISABLED)
		logging.info('Init CAN Dump tab complete')


	# Construct the SCADA Log tab
	def init_tab_scadaLog(self):
		self.scadaLogScrolledText = tk_ScrolledText.ScrolledText(self.scadaLogTab)
		self.scadaLogScrolledText.pack(padx=10, pady=10, fill=BOTH, expand=True)
		self.scadaLogScrolledText.config(state=DISABLED)
		logging.info('Init SCADA Log tab complete')


	# Construct the SCADA Config File tab
	def init_tab_scadaConfigFile(self):
		self.configScrolledText = tk_ScrolledText.ScrolledText(self.scadaConfigTab)
		self.configScrolledText.pack(padx=10, pady=10, fill=BOTH, expand=True)
		self.configScrolledText.insert(INSERT, config.string_dump())
		self.configScrolledText.config(state=DISABLED)
		logging.info('Init SCADA Config tab complete')


	# Updates a sensor value
	def set_value(self, group, sensor, value):
		self.sensorValueVars.get(group).get(sensor).set(value)
		logging.info('Sensor Update: {} - {}, {}'.format(group, sensor, value))

	# Quits SCADA
	def quit_scada(self):
		logging.info('Shutting down... Goodbye')
		self.running = False




# \/   		   \/
# \/  Testing  \/
# \/  		   \/


def main():
	import scada_logger
	from time import strftime

	app = SCADA_GUI()
	scada_logger.set_text_window(app.scadaLogScrolledText)
	
	app.sensorValues.get('GLV').get('Voltage').set('24 V') # Test changing a value
	logging.info('Set GLV Voltage to 24 V')
	
	while app.running:
		app.timeValue.set(strftime('%D  %I:%M:%S %p'))
		app.update_idletasks()
		app.update()
	
	app.destroy()


if __name__ == '__main__':
	main()