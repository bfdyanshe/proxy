import socket
import threading

bind_ip = "localhost"
bind_port = 8021

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)
print(bind_ip,bind_port)

def handler_client(client_socket):
	request=client_socket.recv(2049)
	print"[*]Recvived: %s"%request
	client_socket.send("OVER")
	client_socket.close()

while True:
	client,addr=server.accept()#.accept() return a pair (conn,address)where conn is a new socket object usable to send and receive data on the connection
	print"[*]Accepted Connection from:%s:%d"%(addr[0],addr[1])
	client_handler=threading.Thread(target=handler_client,args=(client,))
	client_handler.start()
