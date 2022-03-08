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


def socketSetUp():
    '''
    Function sets up a TCP socket and listens for connections. 
    When a connection is received it returns a tuple with the listening 
    socket, the connected socket and the connecting client address.
    '''

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, PORT))

    except socket.error as msg:

        print('Bind failed. Error Code: ', str(msg[0]), ' Message ', msg[1])
        sys.exit()

    s.listen()
    print("Server listening on: ", HOST, " on port ", PORT)

    conn, addr = s.accept()

    return (s, conn, addr)


def socketContinue(bound_socket):

    bound_socket.listen()
    print("Server listening on: ", HOST, " on port ", PORT)

    conn, addr = bound_socket.accept()

    return (bound_socket, conn, addr)


def recvMessage(connected_socket):
    '''
    Receives a message from a client. Returns the number
    of bytes received or -1 in the case of an empty transmission
    or a message that the client is ending the connection
    '''

    response = bytearray()
    #bytes_received = 0
    buffer = b''

    while b'>\r\n<' not in buffer:

        part = connected_socket.recv(MSGLEN)

        if not part:
            return -1

        buffer += part
        # print(buffer)

    response, sep, buffer = buffer.partition(b'>\r\n<')

    str_data = response.decode('utf-8')

    if str_data == '/q':
        print("STATUS: Client pressed /q to leave chat.")
        return -1

    print(str_data)
    #print("Length of received message is: ", len(response))

    return len(response)


def sendMessage(connected_socket, exchange_count):
    '''
    Takes a connected socket and prompts the user for input
    for a message. Assembles and sends the message to the client.
    Returns the number of bytes sent or -1 if the server is quitting
    the connection
    '''
    quit = False

    if exchange_count == 0:
        print("Type /q to quit")
        print("Enter message to send...")

    print(">", end="")

    message = input()

    while message == '':
        print("You cannot send an empty message")
        print("Type /q to quit")
        print("Enter message to send...")
        print(">", end="")
        message = input()

    if message == "/q":
        print("STATUS: You pressed /q to leave the chat with the client.")
        quit = True

    # add delimiter
    message += '>\r\n<'

    bytes_sent = 0

    while bytes_sent < MSGLEN:
        sent = connected_socket.send(bytes(message[bytes_sent:], "UTF-8"))
        if sent == 0:

            break
        bytes_sent = bytes_sent + sent

    # if message sent to client is the quit signal
    # signal that client should close too (return -1)
    if quit:
        bytes_sent = -1

    return bytes_sent


def main():

    running = True

    s, conn, addr = socketSetUp()

    while running:

        with conn:
            print(f"Connected by {addr}")
            print('Waiting for message...')

            exchange_count = 0

            while True:

                rec_result = recvMessage(conn)

                if rec_result < 0:
                    break

                send_result = sendMessage(conn, exchange_count)
                #print("Bytes sent", send_result)
                exchange_count += 1

                if send_result < 0:
                    break

            conn.close

        print(
            "Enter Y if you would like the server to continue to accept connections: ", end='')

        choice = input()

        if choice == "Y" or choice == 'y':
            #running = True
            s, conn, addr = socketContinue(s)

        else:
            running = False
            print("Shutting down the server. Goodbye")

    s.close


if __name__ == "__main__":

    main()
