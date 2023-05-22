import socket
from clib import *

class Connection():

	def __init__(self, addr, port=None, isServer=False, csock=None):
		self.addr = addr
		self.port = port
		self.isServer = isServer
		self.asmKey = None
		self.symKey = None

		if csock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			if self.isServer:
				#if this connection is a server we need to bind the port and listen for connections
				self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				self.sock.bind((self.addr, self.port))
				self.sock.listen(100)
			else:
				#if this connection is a client we need to connect to the server
				self.sock.connect((self.addr, self.port))
		else:
			self.sock = csock

	def send(self, message):
		totalsent = 0
		while totalsent < len(message):
			sent = self.sock.send(message[totalsent:])
			if sent == 0:
				return False
			totalsent += sent
		return True

	def sendUnencrypted(self, message):
		self.send("P" + str(len(message)) + message)

	def sendAsymmetric(self, algorithm, message):
		assert self.asmKey, "Cannot send without the asymmetric key!"
		cmsg = encrypt(algorithm, self.asmKey, message)
		self.send("C" + str(len(message)) + str(algorithm) + message)


	def sendSymmetric(self, message):
		assert self.asmKey, "Cannot send without the symmetric key!"
		cmsg = encrypt(A_AES, self.symKey, message)
		self.send("C" + str(len(message)) + str(A_AES) + message)

	def receive(self):
		msg = ""

		# Notes about the protocol:
		# Messages start with either "C" or "P" indicating whether the message is crypted or plain
		# Next are two bytes indicating the length of the message, exluding the first three bytes

		ctype = self.sock.recv(1).decode("utf-8")
		remaining = int.from_bytes(self.sock.recv(2), 'big')

		if ctype == "P":
			while remaining > 0:
				tmp = self.sock.recv(remaining)
				remaining -= len(tmp)
				msg += tmp.decode("utf-8")

		elif ctype == "C":
			algo = int.from_bytes(self.sock.recv(2), 'big')
			remaining -= 2
			cmsg = ""

			while remaining > 0:
				tmp = self.sock.recv(remaining)
				remaining -= len(tmp)
				cmsg += tmp.decode("utf-8")

			if algo == A_AES:
				key = self.symKey
			else:
				key = self.asmKey

				msg = decrypt(algo, key, cmsg)

		else:
			assert False, "Unknown encryption status recv'd!"

		return msg

	def close(self):
		self.sock.close()

	def accept(self):
		"""If the connection is a server connection return a new socket with a client connection."""
		newConn = None

		if self.isServer:
			sock, addr = self.sock.accept()
			newConn = Connection(addr, csock=sock)

		return newConn