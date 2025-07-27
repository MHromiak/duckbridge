from abc import ABC, abstractmethod

class Server(ABC): # pragma: no cover

	@abstractmethod
	def start(self, path : str, host : str, port : int, readonly : bool, extension_downloaded: bool, auth_info : str) -> None:
		pass

	@abstractmethod
	def stop(self) -> None:
		pass