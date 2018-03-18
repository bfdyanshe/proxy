import socket
import threading
import sys

#creating a receive traffic fuction
def receive_from(connection):#connection is a socket connection which 
														 #have been created already in foregone code
	buffer=""
	connection.settimeout(2)
	try:
		data_len=1
		while data_len:
			data=connection.recv(4096)
			data_len=len(data)
			buffer+=data
			if data_len<4096:
				break
	except:
			pass
	return buffer

def request_handler(buffer):
	return buffer
def response_handler(buffer):
	return buffer

def proxy_handler(client_socket,remote_host,remote_port,receive_first):
	#create a socket object
	remote_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#create a socket connection
	remote_socket.connect((remote_host,remote_port))

	if receive_first:
		remote_buffer=receive_from(remote_socket)
		remote_buffer=response_handler(remote_buffer)
		if len(remote_buffer):
			print"[<==]Sending %d bytes to localhost."%len(remote_buffer)
			client_socket.send(remote_buffer)
#the KEY part >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
	while True:
		#receive from client and send to remote
		local_buffer=receive_from(client_socket)
		if len(local_buffer):
			print"[==>]Received %d bytes from local host"%len(local_buffer)

			local_buffer=request_handler(local_buffer)
			remote_socket.send(local_buffer)
			print"[==>]Sent to remote."

		#receive from remote and send to client
		remote_buffer=receive_from(remote_socket)
		if len(remote_buffer):
			print"[<==]Received %d bytes from remote"%len(remote_buffer)

			remote_buffer=response_handler(remote_buffer)
			client_socket.send(remote_buffer)
			print"[<==]Sent to localhost."
#the KEY part <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
		if not len(local_buffer) or not len(remote_buffer):
			client_socket.close()
			remote_socket.close()
			print"[**]no data,close."
			break

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
	server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		server.bind((local_host,local_port))
	except:
		print"[!!]Failed to listen on %s:%d"%(local_host,local_port)
		sys.exit(0)
	print"[*]Listen on %s:%d"%(local_host,local_port)
	server.listen(5)
	#start thread to handle connection
	while True:
		client_socket,addr=server.accept()
		print"[==>]Received incoming connection from %s:%d"%(addr[0],addr[1])
		proxy_thread=threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
		proxy_thread.start()

def main():
	if len(sys.argv[1:])!=5:
		print"Usage:./prosxy.py [localHost] [localPort] [remoteHost] [remotePort] [receiveFirst]"
		sys.exit(0)
	local_host=sys.argv[1]
	local_port=int(sys.argv[2])
	remote_host=sys.argv[3]
	remote_port=int(sys.argv[4])
	receive_first=sys.argv[5]
	if "True" in receive_first:
		receive_first=True
	else:
		receice_first=False
	print receive_first
	server_loop(local_host,local_port,remote_host,remote_port,receive_first)

main()
