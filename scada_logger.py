import logging
import queue

class QueueHandler(logging.Handler):
	
	def __init__(self, log_queue):
		super().__init__()
		self.log_queue = log_queue
		self.formatter = logging.Formatter('%(asctime)s: %(message)s')
		self.setFormatter(self.formatter)

	def emit(self, record):
		self.log_queue.put(record)