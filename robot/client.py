from bluetooth import *
import json
import time
import threading

# Example of how to create the client socket and send json to the robot.
server_socket = BluetoothSocket(RFCOMM)

server_socket.connect(("D4:36:39:D1:E3.1F", 1))
#
# <<<<<<< HEAD
# while True:
#     data = {}
#
#     data['list_action'] = [1, 2, 3]
#     json_data = json.dumps(data)
# =======
# >>>>>>> 7cf62506b441648cf98990f19f40bb6a17a68771

data = {}

data['list_action'] = [1, 3, 1, 4, 5]

json_data = json.dumps(data)

print(json_data)

server_socket.send(json_data)

print("Finished")

time.sleep(2)

#server_socket.close()

