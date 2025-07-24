from abc import ABC, abstractmethod

class Server(ABC): # pragma: no cover

	@abstractmethod
	def start(self):
		pass

	@abstractmethod
	def stop(self):
		pass