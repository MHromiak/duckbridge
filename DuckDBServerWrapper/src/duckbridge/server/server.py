from abc import ABC, abstractmethod

class Server(ABC):

	@abstractmethod
	def start(self):
		pass

	@abstractmethod
	def stop(self):
		pass