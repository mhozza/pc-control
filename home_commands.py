#!/usr/bin/env python

import logging
import os
import platform
import toml
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


SLEEP_COMMAND = "SUSPEND"


def load_config():
    return toml.load(Path(__file__).parent / "config.toml")


def sleep():
    logging.debug("#sleep")
    if platform.system() == "Windows":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        os.system("wall System is going to sleep.")
        os.system("systemctl suspend")


def request_handler_factory(config):
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                url = urlparse(self.path)
                params = parse_qs(url.query)
                logging.debug(params)
                if params.get("key", [None])[0] == config["key"]:
                    if params.get("command", [None])[0] == SLEEP_COMMAND:
                        sleep()
            except Exception as e:
                logging.exception(e)

    return RequestHandler


class Server:
    def __init__(self):
        self.config = load_config()
        logging.debug(self.config)
        server_address = ("0.0.0.0", self.config.get("port", 8001))
        logging.info("setting up server... %s", server_address)
        self.server = HTTPServer(server_address, request_handler_factory(self.config))
        logging.debug(self.server)

    def start(self):
        logging.info("running server...")
        self.server.serve_forever()
        logging.info("finished.")

    def stop(self):
        self.server.shutdown()
        logging.debug("shuting down server")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = Server()
    server.start()
