#!/bin/python

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import research
import json
import importlib

def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','application/json')
    self.end_headers()
    importlib.reload(research)
    response = research.research()
    self.wfile.write(bytes(json.dumps(response), "utf-8"))


handler = BaseHTTPRequestHandler
handler.do_GET = do_GET
server = HTTPServer(server_address=('', 80), RequestHandlerClass=handler)
server.serve_forever()
