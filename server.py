import socket
import threading
import sys

host = "127.0.0.1"
port = int(sys.argv[1])
password = sys.argv[2]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
print(f"Server started on port {port}. Accepting connections...")
server.listen(10)

client_list = {}


def broadcast(message):
    for client in client_list.keys():
        client.send(message.encode('utf-8'))


def broadcast_not_self(message, client_socket):
    for client in client_list.keys():
        if client != client_socket:
            client.send(message.encode('utf-8'))


def handle_messages(client, name):
    while True:
        try:
            message = client.recv(1024)

            if not message:

                client_list.pop(client)

                print(f"{name} left the chatroom")

                broadcast_not_self(f"{name} left the chatroom\n", client)

                break

            str = ""

            message = message.decode().rstrip("\n")

            if message.find(":dm") != -1:

                reciever = message.split(" ")[1]
                recv_msg = message.replace(":dm ", "")
                recv_msg = recv_msg.replace(reciever + " ", "")

                for key in client_list:

                    if client_list[key] == reciever:

                        dm_str = f"{name} -> {reciever}: {recv_msg}"

                        print(dm_str)

                        client.send((dm_str + "\n").encode("utf-8"))

                        key.send((dm_str + "\n").encode("utf-8"))

                        break
            else:

                if message == ":Exit":
                    str = f"{name} left the chatroom"
                    client_list.pop(client)

                else:
                    str = f"{name}: {message}"

                print(str)

                broadcast(f"{str}\n")
        except:
            break


def handle_clients():
    while True:
        socket, address = server.accept()

        msg = socket.recv(1024).decode().split("\n")
        name = msg[1]
        pw = msg[0]

        if pw != password:

            socket.close()
            continue

        else:
            if name in client_list.values() or name.find(' ') != -1:
                socket.send(
                    f"Either a duplicate name or a name that contains spaces\n".encode('utf-8'))
                socket.close()
                continue

            else:
                socket.send(f"Welcome!\n".encode('utf-8'))

            client_list[socket] = name

        broadcast_msg = (f"{name} joined the chatroom")
        print(broadcast_msg)
        broadcast_not_self(broadcast_msg + "\n", socket)

        thread = threading.Thread(target=handle_messages, args=(socket, name))
        thread.start()


handle_clients()
