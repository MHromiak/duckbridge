from duckdbserverwrapper.server.server import Server
from duckdbserverwrapper.constant.constants import Constants
from duckdbserverwrapper.enum.authentication_enum import AuthenticationEnum

import duckdb

class DuckDBServer(Server):

	def __init__(self):
		self.connection = None
		self.port = None
		self.host = None
		self.auth_info = ''

	def start(self, path: str, host : str = "127.0.0.1", port : int = 8080, 
		   readonly = True, extension_downloaded = False, auth: AuthenticationEnum = AuthenticationEnum.NOTHING):
		self.__create_connection(path)
		self.host = host
		self.port = port

		if not extension_downloaded:
			self._setup_extension(self.connection)
			extension_downloaded = True

		if readonly:
			self.__load_httpserver()
			self.connection.execute(Constants.HTTPSERVER_START_QUERY.format(host=host, port=port, auth=self.auth_info))
			print(Constants.SERVER_START_SUCCESS_MESSAGE)

		else:
			print("Server not started in readonly mode. Disabling HTTP requests until restarted in readonly mode.")

	def stop(self):
			self.__load_httpserver()
			self.connection.execute(Constants.HTTPSERVER_STOP_QUERY)
			print(Constants.SERVER_STOP_SUCCESS_MESSAGE)
			self.__close_connection()

	def _setup_extension(self, connection):
		connection.execute(Constants.HTTPSERVER_PLUGIN_DOWNLOAD_QUERY)
		print(Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE)

	def __create_connection(self, path : str):
		try:
			self.connection = duckdb.connect(path)
		except Exception as e:
			raise Exception("Could not create connection to DuckDB database. Exception: " + e)
		
	def __close_connection(self):
		try:
			self.connection.close()
			self.connection= None
			print(Constants.CLOSE_CONNECTION_SUCCESS_MESSAGE.format(host=self.host, port=self.port))
		except Exception as e:
			raise Exception("Exception encountered when attempting to close DB connection to " + self.host + ":" + str(self.port) \
				+ ". Connection may still be open. Exception: " + e)
		
	def __load_httpserver(self):
		try:
			self.connection.execute(Constants.LOAD_HTTPSERVER_QUERY)
			print(Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE)
		except Exception as e:
			raise Exception(Constants.LOAD_HTTPSERVER_FAILURE_MESSAGE)