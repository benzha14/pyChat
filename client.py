import socket
import threading
import sys
import os
from datetime import datetime

host = sys.argv[1]
port = int(sys.argv[2])
password = sys.argv[3]
name = sys.argv[4]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def check_password():
    # check password and username
    client.send(f"{password}\n".encode('utf-8'))
    client.send(f"{name}\n".encode('utf-8'))

    verfication = client.recv(1024).decode('utf-8').rstrip("\n")

    if (verfication != "Welcome!"):
        print(verfication)
        client.close()
        return False
    else:
        print(f"Connecting to {host} on port {port}...")
        print(verfication)
        return True


def receive_msg():
    while True:
        try:
            message = client.recv(1024)

            if not message:
                os._exit(1)

            print(message.decode().rstrip("\n"))
        except:
            break


def send_msg():
    while True:
        try:

            user_input = input()
            message = ""

            if user_input == ":)":
                message = "[feeling happy]\n"

            elif user_input == ":(":
                message = "[feeling sad]\n"

            elif user_input == ":mytime":
                current_time = datetime.now()
                message = f"It's {current_time.strftime('%H')}:{current_time.strftime('%M')} on {current_time.strftime('%a')}, {current_time.strftime('%d')} {current_time.strftime('%b')}, {current_time.strftime('%Y')}.\n"

            elif user_input == ":Exit":
                message = user_input + "\n"
                client.send(message.encode('utf-8'))
                client.close()
                break
            else:
                message = user_input + "\n"

            client.send(message.encode('utf-8'))
        except:
            client.close()
            break


if check_password():
    receive_thread = threading.Thread(target=receive_msg)
    receive_thread.start()
    send_thread = threading.Thread(target=send_msg)
    send_thread.start()
