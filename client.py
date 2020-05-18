import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP_Address = "127.0.0.1"
Port = 1234

my_user_name = input("Username: ")
user_name = my_user_name.encode("utf-8")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_Address, Port))
client_socket.setblocking(False)

username_header = f"{len(user_name):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + user_name)


while True:
    msg = input(f'{my_user_name} > ')

    if msg:
        msg = msg.encode("utf-8")
        msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(msg_header + msg)

    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)

            if not len(username_header):
                print("connection lost.")
                sys.exit()

            username_length = int(username_header.decode("utf-8").strip())
            user_name = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f'{user_name} > {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error: {}".format(str(e)))
            sys.exit()
        continue

    except Exception as e:
        print("General error: {}".format(str(e)))
        sys.exit()


