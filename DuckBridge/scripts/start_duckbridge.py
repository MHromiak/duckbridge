from duckbridge.server.duckdb_server import DuckDBServer
import time
import os

HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", "8080")
AUTH = os.getenv("AUTH", "")
PATH = os.getenv("PATH", "default.db")


bridge = DuckDBServer()
bridge.start(path=PATH,
					host=HOST,
					port=PORT,
					readonly=True,
					extension_downloaded=False,
					auth_info=AUTH)
