from duckbridge.server.server import Server
from duckbridge.constant.constants import Constants

import duckdb, logging
from duckdb import DuckDBPyConnection

class DuckbridgeServer(Server):
	"""
	A class enabling connection, setup, and administration
	of a DuckDB server.

	Attributes
	----------
	__connection : DuckDBPyConnection
		A connection to a database, encapsulated by httpserver.
	__port : int
		The exposed port of the host ip.
	__host : str
		The host ip exposed to requests.
	__auth_info : str
		Authentication string required for clients to make HTTP requests

	Methods
	-------
	start(path, host, port, readonly, extension_downloaded, auth_info) -> None:
		Start the server on http://host:port, with given 'auth', for database at path.
	stop() -> None:
		Stop the server's connection to the database. Only one connection is 
		associated with each server.
	_setup_extension(connection) -> None:
		Install the httpserver extension on the connection's database.
	__create_connection(path) -> None:
		Attempt to connect to a database located at 'path'.
	__close_connection() -> None:
		Attempt to close the server's database connection.
	__load_httpserver(self) -> bool:
		Load httpserver (if installed) on the database.
	__connection_exists() -> bool:
		Check if the server has an existing connection.
	"""

	logger = logging.getLogger(__name__)
	logger.addHandler(logging.NullHandler())
	
	def __init__(self):
		self.__connection : DuckDBPyConnection = None
		self.__port : int = None
		self.__host : str = None
		self.__auth_info : str = None

	def start(self, path: str, host : str = "127.0.0.1", port : int = 8080, 
			readonly = True, extension_downloaded = False, auth_info: str = "") -> None:
		"""
		Start the server on http://host:port, with given 'auth', for database at path.

		Parameters
		----------
			path : str - Path to the database file.
			host : str - Host ip exposed to requests.
			port : int - Exposed port of the host ip.
			readonly : bool - Designates the database as readonly (no edits) or mutable.
			extension_downloaded : bool - Flag to determine if httpserver 
				should be installed on the DB.
			auth_info : str - Authentication string in either 'username:password' or SSH string format.
				The colon between username and password is required.
		"""
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

	def stop(self) -> None:
		"""
		Stop the server's connection to the database. Only one connection is 
		associated with each server.
		"""
		self.__load_httpserver()
		self.__connection.execute(Constants.HTTPSERVER_STOP_QUERY)
		self.logger.info(Constants.SERVER_STOP_SUCCESS_MESSAGE)
		self.__close_connection()

	def _setup_extension(self, connection : DuckDBPyConnection) -> None:
		"""
		Install the httpserver extension on the connection's database.

		Parameters
		----------
			connection : DuckDBPyConnection - Connection associated with the database file.
		"""
		connection.execute(Constants.HTTPSERVER_PLUGIN_DOWNLOAD_QUERY)
		self.logger.info("DuckbridgeServer | setup_extension | " + Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE)

	def __create_connection(self, path : str) -> None:
		"""
		Attempt to connect to a database located at 'path'.

		The new connection is stored in the server's __connection 
		field. Note that if the database file does not exist, a 
		new one will be created - this is duckdb's intended behavior 
		and will not result in an error.

		If a connection already exists, a new one is not made and an 
		error is logged.

		Parameters
		----------
			path : str - Path to the database file.
		"""
		if not self.__connection_exists():
			try:
				self.__connection = duckdb.connect(path)
			except Exception as e:
				self.logger.error(f"DuckbridgeServer | create_connection | Could not create connection to DuckDB database. Exception: {e}")
				self.__connection = None
		else:
			self.logger.error("DuckbridgeServer | create_connection | Could not create connection as one currently exists. Duckbridge does not yet support multiple connections per server")
		
	#TODO: Determine if it makes more sense to raise an exception rather than just log the error.
	def __close_connection(self) -> None:
		"""
		Attempt to close the server's database connection.

		Upon failure, a connection may still exist. In such a case,
		it may be better to destroy the server object (deleting the
		connection) and starting anew.
		"""
		try:
			self.__connection.close()
			self.__connection= None
			self.logger.info("DuckbridgeServer | close_connection | " + Constants.CLOSE_CONNECTION_SUCCESS_MESSAGE.format(host=self.__host, port=self.__port))
		except Exception as e:
			self.logger.error("DuckbridgeServer | close_connection | Exception encountered when attempting to close DB connection. Connection may still be open. Exception: " + str(e))
		
	def __load_httpserver(self) -> bool:
		"""
		Load httpserver (if installed) on the database.

		This enables SQL query execution on the database via
		HTTP LDAP requests. Requests will fail if the extension
		is not loaded.

		Returns
		-------
			bool - True if the extension was loaded, False otherwise
		"""
		try:
			self.__connection.execute(Constants.LOAD_HTTPSERVER_QUERY)
			self.logger.info("DuckbridgeServer | load_httpserver | " + Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE)
			return True
		except Exception as e:
			self.logger.error("DuckbridgeServer | load_httpserver | " + Constants.LOAD_HTTPSERVER_FAILURE_MESSAGE)
			return False
		
	def __connection_exists(self) -> bool:
		"""
		Check if the server has an existing connection.

		Returns
		-------
			bool - True if the server has an existing connection,
				False otherwise.
		"""
		return self.__connection != None