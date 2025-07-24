from duckbridge import *
from unittest.mock import patch

import os
import pathlib as pl
import unittest


class TestDuckbridgeServer(unittest.TestCase):

	def setUp(self):
		self.internal_server = DuckbridgeServer()
		self.internal_server.host = ""
		self.internal_server.port = 0
		self.server_logger_name = self.internal_server.__class__.logger.name

	def tearDown(self):
		self.internal_server._DuckbridgeServer__close_connection()
		try:
			os.remove(pl.Path(os.getcwd(), "temp.db"))
		except:
			pass

	def assertIsFile(self, path):
		if not pl.Path(path).resolve().is_file():
			raise AssertionError("File does not exist: %s" % str(path))

	def test_create_connection_valid_connection(self):
		self.internal_server._DuckbridgeServer__create_connection(pl.Path(os.getcwd(), "temp.db"))
		self.assertIsFile(pl.Path(os.getcwd(), "temp.db"))
		self.assertIsNotNone(self.internal_server._DuckbridgeServer__connection)

	def test_create_connection_while_connection_exists(self):
		self.assertIsNone(self.internal_server._DuckbridgeServer__connection)
		with patch.object(DuckbridgeServer, '_DuckbridgeServer__create_connection', return_value=None), self.assertNoLogs(self.server_logger_name, level="INFO") as l:
			self.internal_server.start("any_path")
		self.assertIsNone(self.internal_server._DuckbridgeServer__connection)
		self.assertIsNone(l)

	def test_setup_extension(self):
		with self.assertLogs(self.server_logger_name, level="INFO") as l:
			self.internal_server._DuckbridgeServer__create_connection(pl.Path(os.getcwd(), "temp.db"))
			self.internal_server._setup_extension(self.internal_server._DuckbridgeServer__connection)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + "DuckbridgeServer | setup_extension | " + Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE in l.output)

	def test_load_httpserver_when_setup(self):
		with self.assertLogs(self.server_logger_name, level="INFO") as l:
			self.internal_server._DuckbridgeServer__create_connection(pl.Path(os.getcwd(), "temp.db"))
			self.internal_server._setup_extension(self.internal_server._DuckbridgeServer__connection)
			self.internal_server._DuckbridgeServer__load_httpserver()
		self.assertTrue("INFO:" + self.server_logger_name + ":" + "DuckbridgeServer | setup_extension | " + Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE in l.output)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + "DuckbridgeServer | load_httpserver | " + Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE in l.output)

	def test_start(self):
		with self.assertLogs(self.server_logger_name, level="INFO") as l:
			self.internal_server.start(pl.Path(os.getcwd(), "temp.db"), extension_downloaded=False)
		self.assertEqual("127.0.0.1", self.internal_server._DuckbridgeServer__host)
		self.assertEqual(8080, self.internal_server._DuckbridgeServer__port)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + "DuckbridgeServer | setup_extension | " + Constants.HTTPSERVER_INSTALL_SUCCESS_MESSAGE in l.output)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + "DuckbridgeServer | load_httpserver | " + Constants.LOAD_HTTPSERVER_SUCCESS_MESSAGE in l.output)
		self.assertTrue("INFO:" + self.server_logger_name + ":" + "DuckbridgeServer | start | " + Constants.SERVER_START_SUCCESS_MESSAGE in l.output)
	
	def test_close_connection_with_no_connection_active(self):
		with self.assertLogs(self.server_logger_name, level="ERROR") as l:
			self.internal_server._DuckbridgeServer__close_connection()
		self.assertTrue(l.output[0].split(":")[0] == "ERROR")

	

if __name__ == "__main__":
	unittest.main()
	


