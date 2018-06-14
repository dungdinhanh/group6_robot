from bluetooth import *
import json
import time
import threading
import requests

# Dependencies for web server
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging





def listen_to_robot():
    while True:
        if server_socket is None:
            continue
        post_data = str(server_socket.recv(1024))
        if len(post_data) == 0:
            continue
        requests.post("http://localhost:4000/response", data=post_data)


def read_file_to_robot():
    while True:
        if server_socket is None:
            continue
        file_in = open("sr.txt", "r")
        commands = file_in.readline()
        if len(commands) == 0:
            continue
        server_socket.send(commands)
        file_in.close()
        file_in = open("sr.txt", "w")
        file_in.close()

class ListenThread(threading.Thread):
    def run(self):
        listen_to_robot()

class ReadFile(threading.Thread):
    def run(self):
        read_file_to_robot()


if __name__ == '__main__':
    list_thread = ListenThread(name="listen")
    read_file = ReadFile(name="read")
    list_thread.run()
    read_file.run()
