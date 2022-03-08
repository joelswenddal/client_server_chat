## Client - Server Chat App

### Description
This program uses TCP sockets to enact a simple chat client. The program includes 2 files: chat_server.py and chat_client.py.


### Instructions for running programs:

- Ensure Python 3 is installed on your machine.
- Download  chat_client.py and chat_server.py and locate in a convenient directory.
- Open two shell processes and navigate to the relevant directory in both.
- In one, run python chat_server.py (run this first)
- In the other, run python chat_client.py (run this second)
- Currently, the program is set to run locally (127.0.0.1)
- The server will connect first and listen for the client to make a connection. Once the client connects, they will be prompted to enter the first message, which will be sent to the server. Parties continue to take turns sending messages.
- Note that for both client and server, hitting ‘Enter’ on the keyboard will send the message. It is not allowed to send a message with no content (although an empty space is allowed). For an empty message, the sending party will be re-prompted to enter a message with content.
- For both client and server, sending the message ‘/q’ will signal that the party is leaving the room and will close down the connection.
Note that when the server breaks the connection with the client, they still have the option to keep listening for new connections. After a closed connection with a client, the server side will receive the option to keep listening by entering ‘Y’. If they enter something else, the listening socket will be closed.

