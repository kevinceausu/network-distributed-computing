import unittest
import requests
import os
from jsonrpcclient import request, parse

SERVER1 = "http://localhost:5001/"
SERVER2 = "http://localhost:5002/"
SERVER3 = "http://localhost:5003/"


class TestServer(unittest.TestCase):

    def rpc_call(self, server_url, method_name, params=None):
        if params is None:
            response = requests.post(server_url, json=request(method_name))
        else:
            response = requests.post(server_url, json=request(method_name, params=params))
        parsed = parse(response.json())
        return parsed.result

    #BASIC COMMANDS

    def test_ping(self):
        result = self.rpc_call(SERVER1, "ping")
        self.assertEqual(result, "pong")

    def test_whoareyou(self):
        result = self.rpc_call(SERVER1, "whoareyou")
        self.assertIn("server 1", result.lower())
        self.assertIn("5001", result)

    def test_get_version(self):
        result = self.rpc_call(SERVER1, "get_version")
        self.assertIn("3.", result)

    #FILESYSTEM COMMANDS

    def test_make_folder(self):
        foldername = "unit_test_folder"

        # Clean up before test in case it already exists
        if os.path.exists(foldername):
            try:
                os.rmdir(foldername)
            except:
                pass

        result = self.rpc_call(SERVER1, "make_folder", {"foldername": foldername})
        self.assertTrue("created" in result.lower() or "already exists" in result.lower())

    def test_search_found(self):
        # Search for a file that should exist in the current folder
        result = self.rpc_call(SERVER1, "search", {"filename": "s.py"})
        self.assertIn("found", result.lower())

    def test_search_not_found(self):
        result = self.rpc_call(SERVER1, "search", {"filename": "this_file_should_not_exist_123.txt"})
        self.assertIn("not found", result.lower())

    def test_delete_folder(self):
        foldername = "unit_test_delete_folder"

        # Ensure folder exists first
        if not os.path.exists(foldername):
            os.mkdir(foldername)

        result = self.rpc_call(SERVER1, "delete_folder", {"foldername": foldername})
        self.assertIn("deleted", result.lower())

    #Friend/network commands

    def test_online(self):
        result = self.rpc_call(SERVER1, "online", {"port": 5002})
        self.assertIn("online", result.lower())

    def test_list_friends(self):
#Make sure 5002 is known first
        self.rpc_call(SERVER1, "online", {"port": 5002})
        result = self.rpc_call(SERVER1, "list_friends")
        self.assertIn("5002", result)

    def test_heartbeat(self):
        #Make sure 5002 is in friends first
        self.rpc_call(SERVER1, "online", {"port": 5002})
        result = self.rpc_call(SERVER1, "heartbeat")
        self.assertTrue("5002" in result or "pong" in result.lower())

    def test_offline(self):
        # Make sure 5002 is present first
        self.rpc_call(SERVER1, "online", {"port": 5002})
        result = self.rpc_call(SERVER1, "offline", {"port": 5002})
        self.assertIn("offline", result.lower())

    #ADVANCED COMMANDS

    def test_pass_message(self):
        # Build simple network path: 5001 knows 5002, 5002 knows 5003
        self.rpc_call(SERVER1, "online", {"port": 5002})
        self.rpc_call(SERVER2, "online", {"port": 5003})

        result = self.rpc_call(SERVER1, "pass_message", {"msg": "hello test", "x": "3"})
        self.assertIn("message received by server 3", result.lower())

    def test_startup(self):
        # This attempts to start server 4
        result = self.rpc_call(SERVER1, "startup", {"x": "4"})
        self.assertIn("started server 4", result.lower())

    def test_shutdown(self):
        #This assumes server 4 has been started first
        self.rpc_call(SERVER1, "startup", {"x": "4"})
        result = self.rpc_call(SERVER1, "shutdown", {"x": "4"})
        self.assertTrue("shutdown signal sent" in result.lower() or "could not contact" in result.lower())

    def tearDown(self):
        import shutil

        folders = ["unit_test_folder", "unit_test_delete_folder"]

        for folder in folders:
            if os.path.exists(folder):
                try:
                    shutil.rmtree(folder)
                except:
                    pass

if __name__ == "__main__":
    unittest.main()