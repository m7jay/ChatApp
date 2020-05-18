"""
###     A client to connect to the server, introduce using the name, send and receive the messages
###     uses a header for sending and receiving data
###     UTF-8 encoding is used for messages
"""
import socket
import select
import errno
import sys

HEADER_LENGTH = 10 #length of the msg can be 10 digits
IP_Address = "127.0.0.1"
Port = 1234

#get user name
my_user_name = input("Username: ")
user_name = my_user_name.encode("utf-8")

"""
###     connect to the server
###     AF_INET specifies the IPv4
###     SOCK_STREAM specifies the TCP
"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_Address, Port))
client_socket.setblocking(False)

#user name is sent after connecting
username_header = f"{len(user_name):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + user_name)

#send a new message or wait for incoming messages
while True:
    msg = input(f'{my_user_name} > ') #new message to send

    if msg:
        #if message entered, send new message
        msg = msg.encode("utf-8")
        msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(msg_header + msg)

    #receive new messages form server in format,
    #| username_header | user_name | message_header | message |
    try:
        while True:
            #get full message by repeating the recv call, 
            #if msg is empty EAGAIN or EWOULDBLOCK exception will raised
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

    #if it is an expected exception, continue the send/receive loop
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error: {}".format(str(e)))
            sys.exit()
        continue
    
    #handle unknown exception
    except Exception as e:
        print("General error: {}".format(str(e)))
        sys.exit()