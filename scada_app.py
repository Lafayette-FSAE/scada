from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tk_ScrolledText
from config import Config
from time import strftime


# Define a class to implement the SCADA App and GUI
# Inherits from a Tkinter Frame
class SCADA_APP(Frame):
	
	# Init and store the parent Frame and init the application
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()
		self.running = True


	# Quits SCADA
	def quit_scada(self):
		self.running = False


	# Begin initializing the GUI
	def init_window(self):
		self.master.title('pySCADA GUI')
		self.master.geometry('1280x720')
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
		sensorValues = {}
		sensorInfoFrame = LabelFrame(self.sensorDataTab, text='Sensors')
		sensorInfoFrame.pack(padx=2, pady=2, fill=Y, expand=True)
		sensorGroups = Config.get('sensors') # config['sensors']
		for group in sensorGroups:
			frame = LabelFrame(sensorInfoFrame, text=group)
			frame.pack(side='left', padx=5, pady=10, fill=Y, expand=True)
			i = 0
			maxWidth = 0
			labelValueDict = {}
			for sensor in sensorGroups[group]:
				length = len(sensor)
				if length > maxWidth:
					maxWidth = length
			for sensor in sensorGroups[group]:
				sensorLabel = Label(frame, text=sensor, width=maxWidth, anchor='w')
				sensorLabel.grid(row=i, column=0, padx=5, pady=5)
				labelVar = StringVar()
				labelVar.set('--')
				valueLabel = Label(frame, textvariable=labelVar, width=5, background='light blue')
				valueLabel.grid(row=i, column=1, padx=5, pady=5)
				labelValueDict[sensor] = labelVar
				i = i + 1
			sensorValues[group] = labelValueDict

		driveFSMLabels = {}
		driveFSMFrame = LabelFrame(self.sensorDataTab, text='Drive State FSM')
		driveFSMFrame.pack(padx=2, pady=2, fill=BOTH, expand=False)
		driveFSMNodes = Config.get('drive_states')
		for node in driveFSMNodes:
			label = Label(driveFSMFrame, text=node, relief=GROOVE, background='dodger blue')
			label.pack(side='left', padx=5, pady=10, fill=BOTH, expand=True)
			driveFSMLabels[node] = label

		sloopFrame = LabelFrame(self.sensorDataTab, text='Safety Loop')
		sloopFrame.pack(padx=2, pady=2, fill=BOTH, expand=False)
		sloopSystemLabels = {}
		sloopSystemFrame = LabelFrame(sloopFrame, text='Systems')
		sloopSystemFrame.pack(side='top', padx=2, pady=2, fill=BOTH, expand=True)
		sloopSystems = Config.get('sloop_systems')
		for system in sloopSystems:
			label = Label(sloopSystemFrame, text=system, relief=GROOVE, background='salmon')
			label.pack(side='left', padx=5, pady=10, fill=BOTH, expand=True)
			sloopSystemLabels[system] = label
		sloopNodeLabels = {}
		sloopNodeFrame = LabelFrame(sloopFrame, text='Nodes')
		sloopNodeFrame.pack(side='bottom', padx=2, pady=2, fill=BOTH, expand=True)
		sloopNodes = Config.get('sloop_nodes')
		for node in sloopNodes:
			label = Label(sloopNodeFrame, text=node, relief=GROOVE, background='green2')
			label.pack(side='left', padx=5, pady=10, fill=BOTH, expand=True)
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
		self.configScrolledText.pack(padx=10, pady=10, fill=BOTH, expand=True)
		self.configScrolledText.insert(INSERT, Config.string_dump())
		self.configScrolledText.config(state=DISABLED)
		print('Init SCADA Config tab complete')


	# Function to update the state of the program outside of the GUI's mainloop
	def update_program(self):
		self.timeValue.set(strftime('%D  %I:%M:%S %p'))


# SCADA's main method
def main():
	root = Tk()
	app = SCADA_APP(root)
	while app.running:
		app.update_program()
		app.update_idletasks()
		app.update()
	app.destroy()


if __name__ == '__main__':
	main()