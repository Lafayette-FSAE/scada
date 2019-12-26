import logging
from tkinter import *
from tkinter.ttk import *
import tkinter.scrolledtext as tk_ScrolledText

def scada_logging_init():
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S %p') # %m/%d/%Y 
	logging.info('Logging initialized')

def scada_logging_init_window(textWindow):
	handler = SCADALoggingHandler(textWindow)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S %p')
	handler.setFormatter(formatter)
	logger = logging.getLogger()
	logger.addHandler(handler)
	logging.info('Handler added')


class SCADALoggingHandler(logging.Handler):
	def __init__(self, textWindow):
		logging.Handler.__init__(self)
		self.textWindow = textWindow

	def emit(self, record):
		msg = self.format(record)
		self.textWindow.configure(state='normal')
		self.textWindow.insert(END, msg+'\n')
		self.textWindow.configure(state='disabled')
		self.textWindow.yview(END)