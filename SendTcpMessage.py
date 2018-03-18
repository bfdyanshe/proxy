#coding=utf-8
import socket
import sys

if len(sys.argv[1:])!=3:
	print"Usage:./SendTcpMessage.py [targetIP] [targetPORT] [message]"
	sys.exit(0)

target_ip=sys.argv[1]#这个默认输入的是字符串
target_port=int(sys.argv[2])#所以要转换格式
if sys.argv[3]=='None':
	message="nice to meet you:)"
else:
	message=sys.argv[3]

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((target_ip,target_port))#starting connection
client.send(message)
response=client.recv(2048)

print response

