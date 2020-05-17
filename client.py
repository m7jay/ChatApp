from socket import socket, AF_INET, SOCK_STREAM, gethostname

HEADER_SIZE = 10
#create a connection to the server
s = socket(AF_INET, SOCK_STREAM)
s.connect((gethostname(), 1243))

def get_msg():
    full_msg = ""
    is_new_msg = True
    while True:
        msg = s.recv(16)
        if is_new_msg:
            msg_len = int(msg[:HEADER_SIZE])
            is_new_msg = False
        full_msg += msg.decode("utf-8")

        if len(full_msg) - HEADER_SIZE == msg_len:
            print(f"msg recieved... size = {len(full_msg)}")
            print(full_msg[HEADER_SIZE:])
            is_new_msg = True
            full_msg = ""

#    return full_msg

if __name__ == "__main__":
    while True:
        get_msg()
