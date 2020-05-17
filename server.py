from socket import socket, AF_INET, SOCK_STREAM, gethostname

s = socket(AF_INET, SOCK_STREAM)
s.bind((gethostname(), 1234))
s.listen(5)

while True:
    print("Waiting for new connections...")
    client_socket, address = s.accept()
    print(f"Connection from {address} has been established...")
    client_socket.send(bytes("Hey there!", "utf-8"))
    client_socket.close()