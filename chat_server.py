

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        print('Waiting for message...')

        exchange_count = 0

        while True:
            data = conn.recv(1024)
            #print("Data received is: ", data)

            if not data:
                break

            data = data.decode('utf-8')

            if data != '/q':
                print(data)

            else:
                print("STATUS: Client pressed /q to quit chat. Goodbye")
                break

            if exchange_count == 0:
                print("Type /q to quit")
                print("Enter message to send...")

            print(">", end="")

            response = input()

            while response == '':
                print("Type /q to quit")
                print("Enter message to send...")
                print(">", end="")
                response = input()

            conn.sendall(bytes(response, 'UTF-8'))
            exchange_count += 1
            # conn.sendall(data)

        s.close()
