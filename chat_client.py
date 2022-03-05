

import socket
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
MSGLEN = 1024


def setSocket(serverName, serverPort):
    '''
    Function takes a serverName (string) and serverPort (int) 
    and sets up a client TCP socket and establishes
    a connection. Returns a reference to the opened
    and connected socket
    '''
    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.setblocking(0)

    except socket.error as msg:
        print('Failed to create socket. Error code: ' +
              str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()

    s.connect((serverName, serverPort))

    return s


def sendMessage(connected_socket):

    print(">", end="")
    message = input()
    quit = False

    while message == '':
        print("Type /q to quit")
        print("Enter message to send...")
        print(">", end="")
        message = input()

    if message == "/q":
        print("STATUS: You pressed /q to leave the chat. Goodbye")
        quit = True

    bytes_sent = 0

    while bytes_sent < MSGLEN:
        sent = connected_socket.send(bytes(message[bytes_sent:], "UTF-8"))
        if sent == 0:
            #raise RuntimeError("socket connection broken")
            break
        bytes_sent = bytes_sent + sent

    # if message sent to client is the quit signal
    # signal that client should close too (return -1)
    if quit:
        bytes_sent = -1

    return bytes_sent


def recvMessage(connected_socket):

    response = bytearray()
    bytes_received = 0
    buffer = b''

    while b'\r\n' not in buffer:
        #print("Waiting on receive from server")
        part = connected_socket.recv(MSGLEN)

        if not part:
            return -1

        buffer += part
        print(buffer)

    response, sep, buffer = buffer.partition(b'\r\n')

    #print("Part received: ", part)
    # if len(part) <= 0:
    # break
    # return
    # response.extend(part)
    #bytes_received = bytes_received + len(part)

    str_data = response.decode('utf-8')
    #print("Decoded response: ", str_data)
    #print("Response length is ", bytes_received)

    if str_data == "/q":
        print("STATUS: Server pressed /q to leave chat. Goodbye")
        return -1

    # print(f"{data!r}")
    print(str_data)
    print("Length of received message is: ", len(response))

    return len(response)


def main():

    s = setSocket(HOST, PORT)
    print("Type /q to quit\r\nEnter message to send...")

    while True:

        send_result = sendMessage(s)
        print("Bytes sent", send_result)

        if send_result < 0:
            break

        rec_result = recvMessage(s)

        if rec_result < 0:
            break

    s.close()


if __name__ == "__main__":

    main()
