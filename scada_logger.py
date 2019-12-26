import logging
from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tk_ScrolledText
import queue


class SCADALogger():
	def __init__(self):
		logging.basicConfig(filename='scada_log.txt', filemode='w', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
		self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S %p')
		self.logQueue = queue.Queue()
		self.handler = SCADALoggingHandler(None, self.logQueue)
		self.handler.setFormatter(self.formatter)
		self.logger = logging.getLogger()
		self.logger.addHandler(self.handler)
		logging.info('Logging initialized')

	def setTextWindow(self, textWindow=None):
		self.handler.setTextWindow(textWindow)


class SCADALoggingHandler(logging.Handler):
	def __init__(self, textWindow=None, msgQueue=None):
		logging.Handler.__init__(self)
		self.textWindow = textWindow
		self.msgQueue = msgQueue

	def emit(self, record):
		if self.msgQueue:
			self.msgQueue.put(record)
			if self.textWindow:
				self.poll_queue()

	def poll_queue(self):
		while not self.msgQueue.empty():
			msg = self.format(self.msgQueue.get())
			self.textWindow.configure(state='normal')
			self.textWindow.insert(END, msg+'\n')
			self.textWindow.configure(state='disabled')
			self.textWindow.yview(END)

	def setTextWindow(self, textWindow=None):
		self.textWindow = textWindow