from bluetooth import *
import json
import time

# Dependencies for web server
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

# Example of how to create the client socket and send json to the robot.
server_socket = BluetoothSocket(RFCOMM)


server_socket.connect(("00:17:E9:F8:72:06", 1))


data = {}

data['list_action'] = [1, 3, 1, 4, 5]

json_data = json.dumps(data)

print(json_data)

server_socket.send(json_data)

print("Finished")

time.sleep(2)

server_socket.close()

# Webserver
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        # Get size of data
        content_length = int(self.headers['Content-Length'])
        # Get data
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        # Parse JSON data
        requestObject = json.loads(post_data.decode('utf-8'))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting robot server...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping robot server...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()