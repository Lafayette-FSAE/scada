import tkinter as tk
import tkinter.ttk as ttk

root = tk.Tk()
root.geometry('1280x720')
root.title('pySCADA GUI')

sensorInfoFrame = tk.Frame(root, relief=tk.RIDGE, borderwidth=4)
driveFSMFrame = tk.Frame(root, relief=tk.RIDGE, borderwidth=4)
sloopFrame = tk.Frame(root, relief=tk.RIDGE, borderwidth=4)

sensorInfoFrame.pack(fill=tk.BOTH, expand=True)
sensorInfoFrameText = tk.Label(sensorInfoFrame, text='Sensor Info')
sensorInfoFrameText.pack(padx=5, pady=5)
sensorGroups = ['GLV', 'TSI', 'Cooling', 'Motor Controller', 'Pack 1', 'Pack 2']
for node in sensorGroups:
	tk.Label(sensorInfoFrame, text=node, relief=tk.GROOVE, height=2).pack(side='left', padx=5, pady=10, fill=tk.X, expand=True)

driveFSMFrame.pack(fill=tk.BOTH, expand=False)
driveFSMFrameText = tk.Label(driveFSMFrame, text='Drive State FSM')
driveFSMFrameText.pack(padx=5, pady=5)
driveFSMNodes = ['GLV Off', 'GLV On', 'Precharge', 'TS Energized', 'Ready to Drive', 'AMS Fault', 'IMD Fault', 'Brake Overtravel']
for node in driveFSMNodes:
	tk.Label(driveFSMFrame, text=node, relief=tk.GROOVE, bg='dodger blue', height=2).pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)

sloopFrame.pack(fill=tk.BOTH, expand=False)
sloopFrameText = tk.Label(sloopFrame, text='Safety Loop State')
sloopFrameText.pack(padx=5, pady=5)
sloopNodes = ['TSI, S1', 'TSI, S2', 'Pack 1, S1', 'Pack 1, S2', 'Pack 2, S1', 'Pack 2, S2']
for node in sloopNodes:
	tk.Label(sloopFrame, text=node, relief=tk.GROOVE, bg='green2', height=2).pack(side='left', padx=5, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()