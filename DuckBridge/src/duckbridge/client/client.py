from abc import ABC, abstractmethod

class Client(ABC): # pragma: no cover

	@abstractmethod
	def execute(self):
		pass
	
	@abstractmethod
	def _convert(self):
		pass