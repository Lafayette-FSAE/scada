# import logging
# from tkinter import *
# from tkinter.ttk import *
# import tkinter.scrolledtext as tk_ScrolledText
# import queue
		

# class SCADALoggingHandler(logging.Handler):
# 	def __init__(self, textWindow=None, msgQueue=None):
# 		logging.Handler.__init__(self)
# 		self.textWindow = textWindow
# 		self.msgQueue = msgQueue

# 	def emit(self, record):
# 		if self.msgQueue:
# 			self.msgQueue.put(record)
# 			if self.textWindow:
# 				self.poll_queue()

# 	def poll_queue(self):
# 		while not self.msgQueue.empty():
# 			msg = self.format(self.msgQueue.get())
# 			self.textWindow.configure(state='normal')
# 			self.textWindow.insert(END, msg+'\n')
# 			self.textWindow.configure(state='disabled')
# 			self.textWindow.yview(END)

# 	def set_window(self, textWindow=None):
# 		self.textWindow = textWindow


# logging.basicConfig(filename='scada_log.txt', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# logQueue = queue.Queue()
# handler = SCADALoggingHandler(msgQueue=logQueue)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S %p')
# handler.setFormatter(formatter)

# rootLogger = logging.getLogger()
# rootLogger.addHandler(handler)

# logging.info('Logging initialized')


# def set_text_window(textWindow=None):
# 	handler.set_window(textWindow)