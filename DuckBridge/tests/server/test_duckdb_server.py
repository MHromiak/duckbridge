from duckbridge import *
from duckbridge.constant.constants import Constants

import os
import pathlib as pl
import unittest

class TestInternalServer(unittest.TestCase):

	def setUp(self):
		self.internal_server = DuckDBServer()
		self.internal_server.host = ""
		self.internal_server.port = 0
		self.server_logger_name = self.internal_server.__class__.logger.name

	def tearDown(self):
		self.internal_server._DuckDBServer__close_connection()
		os.remove(os.getcwd() + "\\temp.db")

	def assertIsFile(self, path):
		if not pl.Path(path).resolve().is_file():
			raise AssertionError("File does not exist: %s" % str(path))

	#TODO - make root path-agnostic. Locate it in the resources folder
	def test_create_connection_valid_connection(self):
		self.internal_server._DuckDBServer__create_connection(os.getcwd() + "\\temp.db")
		self.assertIsFile(os.getcwd() + "\\temp.db")
		self.assertIsNotNone(self.internal_server.connection)

	def test_setup_extension(self):
		with self.assertLogs(self.server_logger_name, level="INFO") as l:
			self.internal_server._DuckDBServer__create_connection(os.getcwd() + "\\temp.db")
			self.internal_server._setup_extension(self.internal_server.connection)

		self.assertTrue("INFO:" + self.server_logger_name + ":" + Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE in l.output)

	def test_load_httpserver_when_setup(self):
		with self.assertLogs(self.server_logger_name, level="INFO") as l:
			self.internal_server._DuckDBServer__create_connection(os.getcwd() + "\\temp.db")
			self.internal_server._setup_extension(self.internal_server.connection)
			self.internal_server._DuckDBServer__load_httpserver()
		self.assertTrue("INFO:" + self.server_logger_name + ":" + Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE in l.output)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE in l.output)

	def test_start(self):
		with self.assertLogs(self.server_logger_name, level="INFO") as l:
			self.internal_server.start(os.getcwd() + "\\temp.db", extension_downloaded=False)
		self.assertEqual("127.0.0.1", self.internal_server.host)
		self.assertEqual(8080, self.internal_server.port)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE in l.output)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE in l.output)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + Constants.SERVER_START_SUCCESS_MESSAGE in l.output)
	
		
if __name__ == "__main__":
	unittest.main()
	


