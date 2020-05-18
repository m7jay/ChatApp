"""
###     A server running on the local system listening to new connections, receive new messages and broadcast the message
###     uses a header for sending and receiving data
###     UTF-8 encoding is used for messages
"""
import socket
import select

HEADER_LENGTH = 10 #length of the message can be 10 digits
IP_Address = "127.0.0.1"
Port = 1234

"""
###     create server
###     AF_INET specifies the IPv4
###     SOCK_STREAM specifies the TCP
"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #to set the socket option to reuse the address

server_socket.bind((IP_Address, Port)) #binding the IP and the port
server_socket.listen() #listen to new connections

socket_list = [server_socket] #list of sockets
clients = {} #socket to user name mapping

print(f"Started the server on {IP_Address}:{Port}...")

"""
###     function to receive the messages in format,
###     | header | data |
"""
def receive_message(client_socket):
    try:
        #get the msg header
        message_header = client_socket.recv(HEADER_LENGTH) 

        #if header not received, client connection closed
        if not len(message_header):
            return False

        #get the message length
        message_length = int(message_header.decode("utf-8").strip()) 

        return {'header':message_header, 'data':client_socket.recv(message_length)}

    except:
        return False

while True:
    #get the list of sockets to be read and the list of sockets with exceptions
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

    for s in read_sockets:
        #if the socket is the server, then a new connection has come
        if s == server_socket:
            client_socket, client_addr = server_socket.accept()
            user = receive_message(client_socket) #receive the user name

            if user is False:
                continue

            socket_list.append(client_socket) #add the new socket to the list
            clients[client_socket] = user     #create a mapping of socket to user

            print("New connection established from {}:{}, username: {}".format(*client_addr, user['data'].decode("utf-8")))

        #new message arrived
        else:
            msg = receive_message(s)
            
            #if msg not received, something went wrong and connection lost
            if msg is False:
                print("Failed to receive the msg from: {}".format(clients[s]["data"].decode("utf-8")))
                socket_list.remove(s)
                del clients[s]
                continue

            user = clients[s]
            print(f'Received msg from {user["data"].decode("utf-8")}: {msg["data"].decode("utf-8")}')

            #send to message to other sockets
            for client in clients:
                if client != s:
                    client.send(user["header"] + user["data"] + msg["header"] + msg["data"])

    #if there is an exception socket, something went wrong, close it
    for s in exception_sockets:
        socket_list.remove(s)
        del clients[s]