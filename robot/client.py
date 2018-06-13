from bluetooth import *
import json
import time

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

