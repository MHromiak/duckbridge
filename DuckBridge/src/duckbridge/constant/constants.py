
class Constants:

	HTTPSERVER_PLUGIN_DOWNLOAD_QUERY = "INSTALL httpserver FROM community;"
	LOAD_HTTPSERVER_QUERY = "LOAD httpserver;"
	HTTPSERVER_START_QUERY = "SELECT httpserve_start('{host}', '{port}', '{auth}');"
	HTTPSERVER_STOP_QUERY = "SELECT httpserve_stop();"


	HTTPSERVER_INSTALL_SUCCESS_MESSAGE = "Successfully installed HTTPSERVER"
	LOAD_HTTPSERVER_SUCCESS_MESSAGE = "Loaded HTTPSERVER"
	LOAD_HTTPSERVER_FAILURE_MESSAGE = "Failure to load HTTPSERVER. Is the extension installed on this connection?"
	CLOSE_CONNECTION_SUCCESS_MESSAGE = "Connection closed to {host}:{port}"
	SERVER_START_SUCCESS_MESSAGE = "Successfully started server"
	SERVER_START_FAILURE_MESSAGE = "Failed to start server"
	SERVER_STOP_SUCCESS_MESSAGE = "Successfully stopped server"
	SERVER_STOP_FAILURE_MESSAGE = "Failed to stop server"