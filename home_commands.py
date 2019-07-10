#!/usr/bin/env python

import os
import toml
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

config = toml.load(Path(__file__).parent / "config.toml")

KEY = config["key"]
SLEEP_COMMAND = "SUSPEND"


def sleep():
    os.system("wall System is going to sleep.")
    os.system("systemctl suspend")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        url = urlparse(self.path)
        params = parse_qs(url.query)
        print(params)
        if params.get("key", [None])[0] == KEY:
            if params.get("command", [None])[0] == SLEEP_COMMAND:
                sleep()
        return


def run():
    server_address = ("0.0.0.0", config.get("port", 8001))
    print("starting server...", server_address)
    httpd = HTTPServer(server_address, RequestHandler)
    print("running server...")
    httpd.serve_forever()


run()
