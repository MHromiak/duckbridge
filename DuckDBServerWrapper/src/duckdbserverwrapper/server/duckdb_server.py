from duckdbserverwrapper.server.server import Server
from abc import ABC, abstractmethod

class DuckDBServer(Server, ABC):

	@abstractmethod
	def _setup_extension(self):
		pass

	@abstractmethod
	def execute(self, host : str, body : str):
		pass

	
