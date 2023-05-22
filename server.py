import socket
from _thread import *


class Client():
	def __init__(self, conn, addr, server):
		self.conn = conn
		self.addr = addr
		self.server = server
		self.online = True
		self.username = None
		self.hash = None
		self.authenticated = False

	# Send a message to this client
	def send(self, message):
		# TODO: actually send the message
		print("send called")

	# Close the connection to the client and mark them as offline
	def close(self):
		# TODO
		print("close called")

	#TODO: Fix this authentication function
	def auth(self):

		user_info = ""
		status = ""

		while status != "success":

			try:
				msg = self.conn.recv(1024)
				msg = msg.decode()

				credentials = msg.split()

				file = open("user-pass.txt", "r")

				for info in file:
					user_info = info.split()

					if user_info[0] == credentials[0] and user_info[1] == credentials[1]:
						status = "s"
						print("Credentials confirmed.")
						self.authenticated = True
						self.conn.send(status.encode())
						file.close()
						break

				if status != "success":
					print("Did you just print here?")
					self.conn.send("f".encode())
			except:
				continue

	# TODO: convert this to use the client class
	#thread_client will be a thread that is running for each client to handled messages
	def loop(self):

		#user_auth(conn, addr)

		#welcome the client
		self.send("Welcome to Secure Chat!")

		#client main loop
		while self.online:
			try:
				#try to recieve a message from the client
				msg = self.conn.recv(1024)

				#if a message has been recieved
				if msg:
					#print the message for debugging
					#TODO: remove this print to because eventually all the traffic will be encrypted
					print((addr[0] + ": " + msg.decode()))

					#send the message to all the connected users except this client
					self.server.broadcast(msg, self)
				else:
					#this will handled when the server recieves a weird message. either a disconnect or error
					#regardless we want to disconnect the client
					self.close()

			except:
				continue

class ClientGroup():

	def __init__(self, members):
		self.members = members

	# Send a message to all members of the group
	def send(self, message):
		# TODO
		print("group send called")

class Server():
	def __init__(self, port, addr):
		# Set up server socket
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.ipaddr = addr
		self.port = port

		# When the server is offline don't try to make any connections
		self.online = True

		self.serverSocket.bind((self.ipaddr, self.port))
		self.serverSocket.listen(100)

		# Keep track of all the clients and the groups
		self.clients = []
		self.groups = []



	# TODO: do what main() used to do
	def loop(self):
		print('Waiting for clients...')
		#our main server loop
		while True:

			#accept a client
			conn, addr = self.serverSocket.accept()

			#add the connection onto the client list in order to make sure the list is always accurate
			newClient = Client(conn, addr, self)
			self.clients.append(newClient)

			print((addr[0] + ": connected!", addr))

			# Start the clint loop in a new thread
			start_new_thread(newClient.loop, ())


	# Send a message to all clients except for 'sender'
	# Pass sender=null to broadcast to all
	def broadcast(self, msg, sender):
		#loop through all currently connected clients and send the message
		for client in self.clients:

			#if the client is not the one specified to be ignored
			if client != sender:
				try:
					#send the message to the client
					client.send(msg)
				except:
					#if something goes wrong then disconnect the client
					client.close()
					self.remove(client)

	# Remove a client and close it's connection
	def remove(self, client):
		if client in self.clients:
			client.close()
			self.clients.remove(client)

	# Close all client connections and close the server socket
	def close(self):
		print("server close called")

		# Close the connections to all clients
		for client in self.clients:
			client.close()
			self.clients.remove(client)

		# Close the server socket
		# TODO: is this how to close this socket?
		self.serverSocket.close()


print('Starting Server')
# TODO: take these parameters from the commandline
s = Server(64646, '127.0.0.1')
s.loop()