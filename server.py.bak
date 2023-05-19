import ManageKeys
import select
import sys
import socket
import Queue
import serverUtil
import time
from thread import *
import address

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((address.HOST, address.PORT))
server.listen(10)
inputs = [server]
outputs = []
message_queues = {}
clientList = []


def main():
    symmetricKey = "Thisisasecretwow"
    print "Server established!\n"

    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for s in readable:
            if s is server:
                connection, clientAddr = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()
                print clientAddr[0] + " is connecting."
            else:
                data = s.recv(1024)
                if data:
                    command = data.split()
                    results = "false"

                    if len(command) >= 3:
                        if command[0] == "message":
                            """Maintains a list of clients for ease of broadcasting
                            a message to all available people in the chatroom"""
                            clientList.append(connection)

                            print command[1] + " & " + command[2] +  " have been invited!"

                            alg = command[3]

                            import Crypto.PublicKey.RSA as RSA
                            from Crypto.PublicKey.RSA import generate, importKey
                            #publicKey = RSA.importKey(command[4])

                            # Send public key-encrypted symmetric Key to user
                            results = symmetricKey

                            # Create a new thread for each user
                            scope = start_new_thread(clientThread,(connection,clientAddr))

                        elif command[0] == "register":
                            results = serverUtil.Register(command[1], command[2])
                        elif command[0] == "validate":
                            results = serverUtil.Validate(command[1], command[2])

                    message_queues[s].put(results)

                    if s not in outputs:
                        outputs.append(s)

                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                nextMessage = message_queues[s].get_nowait()
            except Queue.Empty:
                outputs.remove(s)
            else:
                s.send(nextMessage)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


def clientThread(conn, addr):
    conn.send("Welcome to this chatroom!")
    time.sleep(.1)
    isExitting = False
    while not isExitting:
            try:
                message = conn.recv(2048)
                if message:
                    if message != "!exit":
                        print "<" + addr[0] + "> " + message

                        message_to_send = "<" + addr[0] + "> " + message
                        broadcast(message_to_send, conn)
                    else:
                        print("\User closing chatroom.\n")
                        isExitting = True
                else:
                    isExitting = True
            except:
                continue


# Display text for all connected to see.
def broadcast(message, connection):
    for clients in clientList:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()

                # if the link is broken, we remove the client
                remove(clients)


"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
    if connection in clientList:
        clientList.remove(connection)


if __name__== "__main__":
  main()
