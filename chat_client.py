

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
MSGLEN = 1024


def mysend(connected_socket, message):

    bytes_sent = 0
    while bytes_sent < MSGLEN:
        sent = connected_socket.send(message[bytes_sent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        bytes_sent = bytes_sent + sent


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Type /q to quit\r\nEnter message to send...")

    while True:
        print(">", end="")
        message = input()

        while message == '':
            print("Type /q to quit")
            print("Enter message to send...")
            print(">", end="")
            message = input()

        if message == "/q":
            break

        s.sendall(bytes(message, "UTF-8"))
        #mysend(s, message)
        data = s.recv(1024)

        str_data = data.decode('utf-8')

        if str_data == "/q":
            print("STATUS: Server pressed /q to quit chat. Goodbye")
            break

        # print(f"{data!r}")
        print(str_data)

    s.close()
