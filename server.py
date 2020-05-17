from socket import socket, AF_INET, SOCK_STREAM, gethostname
import time
import pickle

"""
the max size of the msg is 10000000000
and the resulting header size is 10
"""
HEADER_SIZE = 10

s = socket(AF_INET, SOCK_STREAM)
s.bind((gethostname(), 1243))
s.listen(5)

while True:
    print("Waiting for new connections...")
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established...")
    msg = "Welcome to the server..."
    msg = f"{len(msg):<{HEADER_SIZE}}" + msg #add the header to the msg
    client_socket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        msg = f"The time is {time.time()}"
        msg = f"{len(msg):<{HEADER_SIZE}}" + msg
        print(msg)
        client_socket.send(bytes(msg, "utf-8"))
   # client_socket.close()