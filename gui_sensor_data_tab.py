from tkinter import *
from tkinter.ttk import *
from config import Config

class SensorDataTab(Frame):
	def __init__(self, master=None, sensorValues=None, driveFSMLabels=None, sloopSystemLabels=None, sloopNodeLabels=None):
		Frame.__init__(self, master)
		self.master = master
		self.sensorValues = sensorValues
		self.driveFSMLabels = driveFSMLabels
		self.sloopSystemLabels = sloopSystemLabels
		self.sloopNodeLabels = sloopNodeLabels
		self.init_tab()

	def init_tab(self):
		self.sensorInfoFrame = LabelFrame(self.master, text='Sensors')
		self.sensorInfoFrame.pack(padx=2, pady=2, fill=Y, expand=True)
		self.sensorGroups = Config.get('sensors')
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

		driveFSMFrame = LabelFrame(self.master, text='Drive State FSM')
		driveFSMFrame.pack(padx=2, pady=2, fill=BOTH, expand=False)
		driveFSMNodes = Config.get('drive_states')
		for node in driveFSMNodes:
			label = Label(driveFSMFrame, text=node, anchor='center', relief=GROOVE, background='dodger blue')
			label.pack(side='left', padx=15, pady=10, fill=BOTH, expand=True)
			self.driveFSMLabels[node] = label

		self.sloopFrame = LabelFrame(self.master, text='Safety Loop')
		self.sloopFrame.pack(padx=2, pady=2, fill=BOTH, expand=False)
		self.sloopSystemFrame = LabelFrame(self.sloopFrame, text='Systems')
		self.sloopSystemFrame.pack(side='top', padx=2, pady=2, fill=BOTH, expand=True)
		self.sloopSystems = Config.get('sloop_systems')
		for system in self.sloopSystems:
			label = Label(self.sloopSystemFrame, text=system, anchor='center', relief=GROOVE, background='salmon')
			label.pack(side='left', padx=15, pady=10, fill=BOTH, expand=True)
			self.sloopSystemLabels[system] = label
		self.sloopNodeFrame = LabelFrame(self.sloopFrame, text='Nodes')
		self.sloopNodeFrame.pack(side='bottom', padx=2, pady=2, fill=BOTH, expand=True)
		self.sloopNodes = Config.get('sloop_nodes')
		for node in self.sloopNodes:
			label = Label(self.sloopNodeFrame, text=node, anchor='center', relief=GROOVE, background='green2')
			label.pack(side='left', padx=15, pady=10, fill=BOTH, expand=True)
			self.sloopNodeLabels[node] = label
		print('Init Sensor Data tab complete')