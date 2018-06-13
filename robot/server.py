from bluetooth import *
import json
import time
import threading

from socket import *
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

mac_address = "D4:36:39:D1:E3.1F"
port_ev3 = 1
max_data = 2048



from socket import *


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=S, port=9000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

# def createServer():
#     serversocket = socket(AF_INET, SOCK_STREAM)
#     serversocket.bind(('localhost',9000))
#     serversocket.listen(5)
#     while(1):
#         (clientsocket, address) = serversocket.accept()
#         a = "HTTP/1.1 200 OK\n" \
#          +"Content-Type: text/html\n"\
#          +"\n"\
#          +"<html><body>Hello World</body></html>\n"
#         b = a.encode('utf-8')
#         clientsocket.send(b)
#         clientsocket.shutdown(SHUT_WR)
#         clientsocket.close()
#
#     serversocket.close()
#
# createServer()

def connect_to_ev3(mac_address, port_ev3):
    server_socket = BluetoothSocket(RFCOMM)
    server_socket.connect((mac_address, port_ev3))
    #server_socket.recv(1024)
    return server_socket


class EvConnect:
    connector = None

    @staticmethod
    def get_instance():
        if EvConnect.connector is None:
            EvConnect.connector = EvConnect()
        return EvConnect.connector

    @staticmethod
    def clear_instance():
        EvConnect.connector = None

    def __init__(self):
        self.data = ""
        self.mac_address = mac_address
        self.port_ev3 = port_ev3
        self.server_socket = None
        self.set_up_connection()
        self.receive_message = ""
        self.send_message = ""

    def set_up_connection(self):
        self.server_socket = connect_to_ev3(mac_address, port_ev3)

    def get_data(self):
        if self.server_socket is None:
            return
        string_data = str(self.server_socket.recv(max_data))
        print(string_data)
        return string_data
        # do something to back to client

    def send_data(self, str_data):
        if self.server_socket is None:
            return None
        self.server_socket.send(str_data)
        self.send_message = str_data


class EvListenThread(threading.Thread):
    def run(self):
        ev3_connector = EvConnect.get_instance()
        while ev3_connector.server_socket is None:
            continue
        while True:
            str_message = ev3_connector.get_data()
            #do smth back to client
            print(str_message)


def take_fake_input():
    print("Input the list of codes. If you want to stop push -1")
    list_action = []
    while True:
        a = input(int)
        if a == -1:
            break
    mess = {}
    mess['list_action'] = list_action
    mess['default'] = 'on'
    return mess


ev3_connect = EvConnect.get_instance()
ev3_connect.set_up_connection()
ev3_listener = EvListenThread(name="listener")
ev3_listener.start()

fake_mess = take_fake_input()
ev3_connect.send_data(json.dumps(fake_mess))



