from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tk_ScrolledText
from time import strftime
# from config import Config
import config
import logging
from scada_logger import SCADALogger

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
		self.master.protocol('WM_DELETE_WINDOW', self.quit_scada)

		# Configure tabs
		self.tabsParent = Notebook(self.master)
		self.sensorDataTab = Frame(self.tabsParent)
		self.liveChartTab = Frame(self.tabsParent)
		self.systemConfigTab = Frame(self.tabsParent)
		self.canDumpTab = Frame(self.tabsParent)
		self.scadaLogTab = Frame(self.tabsParent)
		self.scadaConfigTab = Frame(self.tabsParent)
		self.tabsParent.add(self.sensorDataTab, text='Sensor Data')
		self.tabsParent.add(self.liveChartTab, text='Live Charts')
		self.tabsParent.add(self.systemConfigTab, text='Config System')
		self.tabsParent.add(self.canDumpTab, text='CAN Dump')
		self.tabsParent.add(self.scadaLogTab, text='SCADA Log')
		self.tabsParent.add(self.scadaConfigTab, text='SCADA Config File')
		self.tabsParent.pack(side='top', fill=BOTH, expand=True)

		# Construct the tabs
		self.init_tab_sensorData()			# Create the Sensor Data tab
		self.init_tab_liveCharts()			# Create the Live Charts tab
		self.init_tab_configSystem()		# Create the Config System tab
		self.init_tab_canDump()				# Create the CAN Dump tab
		self.init_tab_scadaLog()			# Create the SCADA Log tab
		self.init_tab_scadaConfigFile()		# Create the SCADA Config File tab

		# Create status bar
		self.statusBar = Frame(self.master, relief=SUNKEN, borderwidth=1)
		self.statusBar.pack(side='bottom', padx=1, pady=1, fill=X, expand=False)
		self.exitButton = Button(self.statusBar, text='Quit', command=self.quit_scada, width=10)
		self.exitButton.pack(side='right', padx=2, pady=2)
		self.timeValue = StringVar()
		self.timeValue.set('0/0/00  00:00:00 AM')
		self.timeLabel = Label(self.statusBar, textvariable=self.timeValue)
		self.timeLabel.pack(side='left', padx=2, pady=2)


	# Construct the Sensor Data tab
	def init_tab_sensorData(self):
		self.sensorValues = {}
		self.sensorInfoFrame = LabelFrame(self.sensorDataTab, text='Sensors')
		self.sensorInfoFrame.pack(padx=2, pady=2, fill=Y, expand=True)
		self.sensorGroups = config.get('sensors')
		for group in self.sensorGroups:
			frame = LabelFrame(self.sensorInfoFrame, text=group)
			frame.pack(side='left', padx=5, pady=10, fill=Y, expand=True)
			i = 0
			maxWidth = 0
			labelValueDict = {}
			for sensor in self.sensorGroups[group]:
				length = len(sensor)
				if length > maxWidth:
					maxWidth = length
			for sensor in self.sensorGroups[group]:
				sensorLabel = Label(frame, text=sensor, width=maxWidth+2, anchor='w')
				sensorLabel.grid(row=i, column=0, padx=5, pady=5)
				labelVar = StringVar()
				labelVar.set('--')
				valueLabel = Label(frame, textvariable=labelVar, width=6, anchor='center', background='light blue')
				valueLabel.grid(row=i, column=1, padx=5, pady=5)
				labelValueDict[sensor] = labelVar
				i = i + 1
			self.sensorValues[group] = labelValueDict

		self.driveFSMLabels = {}
		driveFSMFrame = LabelFrame(self.sensorDataTab, text='Drive State FSM')
		driveFSMFrame.pack(padx=2, pady=2, fill=BOTH, expand=False)
		driveFSMNodes = config.get('drive_states')
		for node in driveFSMNodes:
			label = Label(driveFSMFrame, text=node, anchor='center', relief=GROOVE, background='dodger blue')
			label.pack(side='left', padx=15, pady=10, fill=BOTH, expand=True)
			self.driveFSMLabels[node] = label

		self.sloopFrame = LabelFrame(self.sensorDataTab, text='Safety Loop')
		self.sloopFrame.pack(padx=2, pady=2, fill=BOTH, expand=False)
		self.sloopSystemLabels = {}
		self.sloopSystemFrame = LabelFrame(self.sloopFrame, text='Systems')
		self.sloopSystemFrame.pack(side='top', padx=2, pady=2, fill=BOTH, expand=True)
		self.sloopSystems = config.get('sloop_systems')
		for system in self.sloopSystems:
			label = Label(self.sloopSystemFrame, text=system, anchor='center', relief=GROOVE, background='salmon')
			label.pack(side='left', padx=15, pady=10, fill=BOTH, expand=True)
			self.sloopSystemLabels[system] = label
		self.sloopNodeLabels = {}
		self.sloopNodeFrame = LabelFrame(self.sloopFrame, text='Nodes')
		self.sloopNodeFrame.pack(side='bottom', padx=2, pady=2, fill=BOTH, expand=True)
		self.sloopNodes = config.get('sloop_nodes')
		for node in self.sloopNodes:
			label = Label(self.sloopNodeFrame, text=node, anchor='center', relief=GROOVE, background='green2')
			label.pack(side='left', padx=15, pady=10, fill=BOTH, expand=True)
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


	# Quits SCADA
	def quit_scada(self):
		logging.info('Shutting down... Goodbye')
		self.running = False



# \/ Eventually moved to the main.py file or something \/

# SCADA's main method
def main():
	logger = SCADALogger()
	app = SCADA_GUI()
	logger.setTextWindow(app.scadaLogScrolledText)
	app.sensorValues.get('GLV').get('Voltage').set('24 V') # Test changing a value
	logging.info('Set GLV Voltage to 24 V')
	while app.running:
		app.timeValue.set(strftime('%D  %I:%M:%S %p'))
		app.update_idletasks()
		app.update()
	app.destroy()


if __name__ == '__main__':
	main()