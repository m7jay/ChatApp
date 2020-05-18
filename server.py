import socket
import select

HEADER_LENGTH = 10
IP_Address = "127.0.0.1"
Port = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP_Address, Port))
server_socket.listen()

socket_list = [server_socket]
clients = {}

print(f"Started the server on {IP_Address}:{Port}...")

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())

        return {'header':message_header, 'data':client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for s in read_sockets:
        if s == server_socket:
            client_socket, client_addr = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue

            socket_list.append(client_socket)
            clients[client_socket] = user

            print("New connection established from {}:{}, username: {}".format(*client_addr, user['data'].decode("utf-8")))

        else:
            msg = receive_message(s)

            if msg is False:
                print("Failed to receive the msg from: {}".format(clients[s]["data"].decode("utf-8")))
                socket_list.remove(s)
                del clients[s]
                continue

            user = clients[s]
            print(f'Received msg from {user["data"].decode("utf-8")}: {msg["data"].decode("utf-8")}')

            for client in clients:
                if client != s:
                    client.send(user["header"] + user["data"] + msg["header"] + msg["data"])

    for s in exception_sockets:
        socket_list.remove(s)
        del clients[s]

