from abc import ABC, abstractmethod

class Client(ABC):

	@abstractmethod
	def execute(self):
		pass
	
	@abstractmethod
	def _convert(self):
		pass