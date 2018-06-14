import bluetooth
import threading
import json
import time
# from robot import ar_signal
import random
from ev3dev.ev3 import *

mLeft = LargeMotor('outB')
mRight = LargeMotor('outC')
fork = MediumMotor('outA')

us = UltrasonicSensor()
us.mode = 'US-DIST-CM'
cs = ColorSensor()
cs.mode = "COL-COLOR"
gs = GyroSensor()
ts = TouchSensor()

webclientAddress = 'FC:F8:AE:1F:00:F8'

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_socket.bind(("", port))
server_socket.listen(1)
web_client = None
web_client_message = ""


class ConnectedClient(threading.Thread):
    def __init__(self, socket, client_info):
        threading.Thread.__init__(self)
        self.socket = socket
        self.client_info = client_info
        self.message = None
        self.message_to_send = None

    def run(self):
        global web_client_message
        try:
            while True:
                data = self.socket.recv(1024)
                if len(data) == 0:
                    continue
                str_data = data.decode('utf-8')
                web_client_message = json.loads(str_data)
                print("self.message:", web_client_message)
                if self.message_to_send is not None:
                    print("sending")
                    self.socket.send(self.message_to_send)
                    self.message_to_send = None
        except IOError:
            pass
        self.socket.close()
        print(self.client_info, ": disconnected")


def stop():
    mLeft.stop()
    mRight.stop()
    fork.stop()


def forth():
    print("forward")
    run = True
    mLeft.run_forever(speed_sp=50)
    mRight.run_forever(speed_sp=50)
    time.sleep(1)
    while run:
        color_value = cs.value()
        # black: go straight forward
        if color_value == 1:
            mLeft.run_forever(speed_sp=50)
            mRight.run_forever(speed_sp=50)
        # green:stop
        elif color_value == 3:
            time.sleep(1)
            stop()
            run = False
            send_data_to_server()

        # red:stop
        elif color_value == 5:
            time.sleep(1)
            stop()
            run = False
        # other colors: adjust the direction and find the black line

        else:
            for i in range(1, 400):
                mLeft.run_timed(time_sp=20, speed_sp=150)
                mRight.run_timed(time_sp=20, speed_sp=-150)
                if cs.value() == 1:
                    break
            for j in range(1, 150):
                mRight.run_timed(time_sp=20, speed_sp=100)
                mLeft.run_timed(time_sp=20, speed_sp=-100)
                if cs.value() == 1:
                    break

        time.sleep(0.1)

# web_client.message_to_send = ar_signal.get_json()


def back():
    print("backwards")
    mLeft.run_forever(time_sp=20, speed_sp=-50)
    mRight.run_forever(time_sp=20, speed_sp=-50)


def left(): #test
    print("turning left")
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'
    mLeft.run_forever(speed_sp=-50)
    mRight.run_forever(speed_sp=50)
    while gs.value() > -90:
        print(gs.value())
        pass
    stop() #just add in


def right(): #test
    print("turning right")
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'
    mLeft.run_forever(speed_sp=50)
    mRight.run_forever(speed_sp=-50)
    while gs.value() < 90:
        print(gs.value())
        pass
    stop() #just add in


# def right():
#     print("turning right")
#     gs.mode = 'GYRO-RATE'
#     gs.mode = 'GYRO-ANG'
#     mLeft.run_forever(speed_sp=-50)
#     mRight.run_forever(speed_sp=50)
#     while gs.value() < 90:
#         print(gs.value())
#         pass
#     stop() #just add in
#
#
# def left():
#     print("turning left")
#     gs.mode = 'GYRO-RATE'
#     gs.mode = 'GYRO-ANG'
#     mLeft.run_forever(speed_sp=50)
#     mRight.run_forever(speed_sp=-50)
#     while gs.value() > -90:
#         print(gs.value())
#         pass
#     stop() #just add in


def forkup():
    run = True
    while run:
        # black: go straight forward
        color_value = cs.value()
        if color_value == 1:
            mLeft.run_forever(speed_sp=50)
            mRight.run_forever(speed_sp=50)
        # pick up cargo
        elif ts.value() == 1:
            print("lifting cargo")
            stop()
            fork.run_timed(time_sp=100, speed_sp=150)
            run = False
            send_data_to_server()

        # other colors: adjust the direction and find the black line
        else:
            for i in range(1, 400):
                mLeft.run_timed(time_sp=20, speed_sp=150)
                mRight.run_timed(time_sp=20, speed_sp=-150)
                if cs.value() == 1:
                    break
            for j in range(1, 150):
                mRight.run_timed(time_sp=20, speed_sp=100)
                mLeft.run_timed(time_sp=20, speed_sp=-100)
                if cs.value() == 1:
                    break


def forkdown():
    run = True
    while run:
        # black: go straight forward
        color_value = cs.value()
        if color_value == 1:
            mLeft.run_forever(speed_sp=50)
            mRight.run_forever(speed_sp=50)
        # red:put cargo down
        elif color_value == 5:
            print("putting cargo down")
            stop()
            fork.run_timed(time_sp=100, speed_sp=-150)
            run = False
            send_data_to_server()
        # other colors: adjust the direction and find the black line
        else:
            for i in range(1, 400):
                mLeft.run_timed(time_sp=20, speed_sp=150)
                mRight.run_timed(time_sp=20, speed_sp=-150)
                if cs.value() == 1:
                    break
            for j in range(1, 150):
                mRight.run_timed(time_sp=20, speed_sp=100)
                mLeft.run_timed(time_sp=20, speed_sp=-100)
                if cs.value() == 1:
                    break


def send_data_to_server():
    data = {}
    temp = random.uniform(10.0, 40.0)
    hum = random.uniform(10.0, 30.0)

    if temp > 20:
        data['temperature'] = 'good'
    elif 10 >= temp <= 20:
        data['temperature'] = 'acceptable'
    else:
        data['temperature'] = 'bad'

    if hum > 20:
        data['humidity'] = 'good'
    elif 10 >= hum <= 20:
        data['humidity'] = 'acceptable'
    else:
        data['humidity'] = 'bad'

    if ts.value() == 1:
        data['cargo'] = 'yes'
    else:
        data['cargo'] = 'no'

    json_data = json.dumps(data)

    web_client.message_to_send = json_data


while True:
    if web_client is None:
        print("waiting for client/server")
        client_socket, client_info = server_socket.accept()
        print(client_info, ": connection accepted")
        print("web_client")
        web_client = ConnectedClient(client_socket, client_info)
        print(web_client.message)
        web_client.setDaemon(True)
        web_client.start()
    # print("list_action", web_client.message['list_action'])
    print("web_client.message", web_client_message)
    # json = json.loads(web_client_message)
    if not web_client_message:
        time.sleep(0.5)
        continue
    else:
        for command in web_client_message['list_action']:
            if command == 1:
                forth()

            elif command == 2:
                back()

            elif command == 3:
                left()

            elif command == 4:
                right()

            elif command == 5:
                forkdown()

            elif command == 6:
                forkup()
            else:
                break
        web_client_message = None

time.sleep(1)
server_socket.close()
