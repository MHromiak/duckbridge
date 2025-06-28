from duckdbserverwrapper.server.server import Server
from duckdbserverwrapper.constant.constants import Constants
from duckdbserverwrapper.enum.authentication_enum import AuthenticationEnum

import duckdb, logging

class DuckDBServer(Server):
	logger = logging.getLogger(__name__)
	logger.addHandler(logging.NullHandler())

	def __init__(self):
		self.connection = None
		self.port = None
		self.host = None
		self.auth_info = None

	def start(self, path: str, host : str = "127.0.0.1", port : int = 8080, 
		   readonly = True, extension_downloaded = False, auth_type: AuthenticationEnum = AuthenticationEnum.NOTHING, auth_info: str = ""):
		self.__create_connection(path)
		self.host = host
		self.port = port
		self.auth_info = auth_info

		if self.connection != None:
			if not extension_downloaded:
				self._setup_extension(self.connection)
				extension_downloaded = True

			if readonly:
				httpserver_loaded : bool = self.__load_httpserver()
				if httpserver_loaded:
					self.connection.execute(Constants.HTTPSERVER_START_QUERY.format(host=host, port=port, auth=self.auth_info))
					self.logger.info(Constants.SERVER_START_SUCCESS_MESSAGE)

			else:
				print("Server not started in readonly mode. Disabling HTTP requests until restarted in readonly mode.")

	def stop(self):
			self.__load_httpserver()
			self.connection.execute(Constants.HTTPSERVER_STOP_QUERY)
			self.logger.info(Constants.SERVER_STOP_SUCCESS_MESSAGE)
			self.__close_connection()

	def _setup_extension(self, connection):
		connection.execute(Constants.HTTPSERVER_PLUGIN_DOWNLOAD_QUERY)
		self.logger.info(Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE)

	def __create_connection(self, path : str):
		try:
			self.connection = duckdb.connect(path)
		except Exception as e:
			self.logger.error("Could not create connection to DuckDB database. Exception: " + e)
			self.connection = None
		
	def __close_connection(self):
		try:
			self.connection.close()
			self.connection= None
			self.logger.info(Constants.CLOSE_CONNECTION_SUCCESS_MESSAGE.format(host=self.host, port=self.port))
		except Exception as e:
			self.logger.error("Exception encountered when attempting to close DB connection to " + self.host + ":" + str(self.port) \
				+ ". Connection may still be open. Exception: " + e)
		
	def __load_httpserver(self) -> bool:
		try:
			self.connection.execute(Constants.LOAD_HTTPSERVER_QUERY)
			self.logger.info(Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE)
			return True
		except Exception as e:
			self.logger.error(Constants.LOAD_HTTPSERVER_FAILURE_MESSAGE)
			return False