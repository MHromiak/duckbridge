from duckbridge.server.server import Server
from duckbridge.constant.constants import Constants

import duckdb, logging
from duckdb import DuckDBPyConnection

class DuckbridgeServer(Server):
	logger = logging.getLogger(__name__)
	logger.addHandler(logging.NullHandler())
	
	def __init__(self):
		self.__connection : DuckDBPyConnection = None
		self.__port = None
		self.__host = None
		self.__auth_info = None

	def start(self, path: str, host : str = "127.0.0.1", port : int = 8080, 
		   readonly = True, extension_downloaded = False, auth_info: str = ""):
		self.__create_connection(path)
		self.__host = host
		self.__port = port
		self.__auth_info = auth_info

		if self.__connection != None:
			if not extension_downloaded:
				self._setup_extension(self.__connection)

			if readonly:
				httpserver_loaded : bool = self.__load_httpserver()
				if httpserver_loaded:
					self.__connection.execute(Constants.HTTPSERVER_START_QUERY.format(host=self.__host, port=self.__port, auth=self.__auth_info))
					self.logger.info("DuckbridgeServer | start | " + Constants.SERVER_START_SUCCESS_MESSAGE)

			else:
				self.logger.info("DuckbridgeServer | start | Server not started in readonly mode. Disabling HTTP requests until restarted in readonly mode")

	def stop(self):
			self.__load_httpserver()
			self.__connection.execute(Constants.HTTPSERVER_STOP_QUERY)
			self.logger.info(Constants.SERVER_STOP_SUCCESS_MESSAGE)
			self.__close_connection()

	def _setup_extension(self, connection):
		connection.execute(Constants.HTTPSERVER_PLUGIN_DOWNLOAD_QUERY)
		self.logger.info("DuckbridgeServer | setup_extension | " + Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE)

	def __create_connection(self, path : str):
		if not self.__connection_exists():
			try:
				self.__connection = duckdb.connect(path)
			except Exception as e:
				self.logger.error(f"DuckbridgeServer | create_connection | Could not create connection to DuckDB database. Exception: {e}")
				self.__connection = None
		
	def __close_connection(self):
		try:
			self.__connection.close()
			self.__connection= None
			self.logger.info("DuckbridgeServer | close_connection | " + Constants.CLOSE_CONNECTION_SUCCESS_MESSAGE.format(host=self.__host, port=self.__port))
		except Exception as e:
			self.logger.error("DuckbridgeServer | close_connection | Exception encountered when attempting to close DB connection. Connection may still be open. Exception: " + str(e))
		
	def __load_httpserver(self) -> bool:
		try:
			self.__connection.execute(Constants.LOAD_HTTPSERVER_QUERY)
			self.logger.info("DuckbridgeServer | load_httpserver | " + Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE)
			return True
		except Exception as e:
			self.logger.error("DuckbridgeServer | load_httpserver | " + Constants.LOAD_HTTPSERVER_FAILURE_MESSAGE)
			return False
		
	def __connection_exists(self) -> bool:
		if self.__connection != None:
			self.logger.error("DuckbridgeServer | create_connection | Could not create connection as one currently exists. Duckbridge does not yet support multiple connections per server")
			return True
		return False