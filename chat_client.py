# Student: Joel Swenddal
# Course: CS 372
# Semester: Winter 2022
# Assignment: Project 4
# Description: Program uses a socket to enable a simple synchronous chat between a client and server
# Sources:
# 1) Kurose and Ross, Computer Networking: A Top-Down Approach, 7th Edition, Pearson
# 2) Python 3 Documentation: http://docs.python.org/3/library/socket.html

import socket
import sys

HOST = "127.0.0.1"
PORT = 65432
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

    except socket.error as msg:
        print('Failed to create socket. Error code: ' +
              str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()

    s.connect((serverName, serverPort))

    print("Connected to ", HOST, " on port ", PORT)

    return s


def sendMessage(connected_socket):
    '''
    Takes a connected socket and prompts the user for input
    for a message. Assembles and sends the message to the server. 
    Returns the number of bytes sent or -1 if the client is quitting
    the connection
    '''
    print(">", end="")
    message = input()
    quit = False

    while message == '':
        print("You cannot send an empty message")
        print("Type /q to quit")
        print("Enter message to send...")
        print(">", end="")
        message = input()

    if message == "/q":
        print("STATUS: You pressed /q to leave the chat. Goodbye")
        quit = True

    # add delimiter
    message += '>\r\n<'

    bytes_sent = 0

    while bytes_sent < MSGLEN:
        sent = connected_socket.send(bytes(message[bytes_sent:], "UTF-8"))
        if sent == 0:
            #raise RuntimeError("socket connection broken")
            break
        bytes_sent = bytes_sent + sent

    # if message sent to server is the quit signal
    # signal that server should close too (return -1)
    if quit:
        bytes_sent = -1

    return bytes_sent


def recvMessage(connected_socket):
    '''
    Receives a message from a server. Returns the number
    of bytes received or -1 in the case of an empty transmission
    or a message that the server is ending the connection
    '''
    response = bytearray()
    #bytes_received = 0
    buffer = b''

    while b'>\r\n<' not in buffer:
        #print("Waiting on receive from server")
        part = connected_socket.recv(MSGLEN)

        if not part:
            return -1

        buffer += part
        # print(buffer)

    response, sep, buffer = buffer.partition(b'>\r\n<')

    str_data = response.decode('utf-8')

    if str_data == "/q":
        print("STATUS: Server pressed /q to leave chat. Goodbye")
        return -1

    print(str_data)
    #print("Length of received message is: ", len(response))

    return len(response)


def main():

    s = setSocket(HOST, PORT)
    print("Type /q to quit\r\nEnter message to send...")

    while True:

        send_result = sendMessage(s)
        #print("Bytes sent", send_result)

        if send_result < 0:
            break

        rec_result = recvMessage(s)

        if rec_result < 0:
            break

    s.close()


if __name__ == "__main__":

    main()
