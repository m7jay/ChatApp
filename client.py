from socket import socket, AF_INET, SOCK_STREAM, gethostname

#create a connection to the server
s = socket(AF_INET, SOCK_STREAM)
s.connect((gethostname(), 1234))

def get_msg():
    full_msg = ""
    while True:
        msg = s.recv(8)
        if len(msg) <= 0:
            break
        full_msg += msg.decode("utf-8")
    return full_msg

if __name__ == "__main__":
    while True:
        msg = get_msg()
        if len(msg) > 0:
            print(msg)