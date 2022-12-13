import sys
sys.path.append('./..')

#import src.library as Library
from src.library import Library
from structures.exceptions import *

import socket
import os

TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '0.0.0.0' # IP do Servidor
PORT = 40003 # Porta que o Servidor escuta
def processa_msg_cliente(msg, con, cliente):
	msg = msg.decode()
	print('Cliente', cliente, 'enviou', msg)
	msg = msg.split()
	if msg[0].upper() == 'REGISTER' and len(msg) == 3:
		try:
			library.register_user(msg[1],msg[2])
			print('funcionou', library.users)
			con.send(str.encode('+OK {}\n'.format(msg[1])))
   
		except AlreadyExistingObjectException:
			con.send(str.encode(f'+ERROR: User already registered\n'))

		""""
		nome_arq = " ".join(msg[1:])
		print('Arquivo solicitado:', nome_arq)
		try:
			status_arq = os.stat(nome_arq)
			con.send(str.encode('+OK {}\n'.format(status_arq.st_size)))
			arq = open(nome_arq, "rb")
			while True:
				dados = arq.read(TAM_MSG)
				if not dados: break
				con.send(dados)
		except Exception as e:
			con.send(str.encode('-ERR {}\n'.format(e)))"""

	elif msg[0].upper() == 'CHECK':
		try:
			if library.check_available(int(msg[1])):
				print('EXISTE')
				con.send(str.encode('+OK {}\n'.format(msg[1])))


		except Exception as e:
			con.send(str.encode('-ERROR {}\n'.format(e)))

	elif msg[0].upper() == 'LOAN':
		try:
			if library.loan_book(int(msg[1]), msg[2], msg[3]):
				print('funcionou', library.users)
				con.send(str.encode('+OK {}\n'.format(msg[1])))
   
		except Exception as e:
			con.send(str.encode('-ERROR {}\n'.format(e)))

	elif msg[0].upper() == 'INFO':
		# check_loan_info

		try:
			res = library.check_loan_info(int(msg[1]), msg[2], msg[3])

			con.send(str.encode(res))
   
		except Exception as e:
			con.send(str.encode('-ERROR {}\n'.format(e)))

	elif msg[0].upper() == 'RENEW':
		# check_loan_info

		try:
			if library.renew_loan(int(msg[1]), msg[2], msg[3]):
				con.send(str.encode('+OK Loan was renewed succesfully\n'))
   
		except Exception as e:
			con.send(str.encode('-ERROR {}\n'.format(e)))


	elif msg[0].upper() == 'RETURN':
		# check_loan_info

		try:
			library.return_book(int(msg[1]), msg[2], msg[3])
			
			con.send(str.encode('+OK Loan was returned succesfully\n'))
   
		except Exception as e:
			con.send(str.encode('-ERROR {}\n'.format(e)))


	else:
		con.send(str.encode('-ERR Invalid command\n'))
	return True
	
def processa_cliente(con, cliente):
	print('Cliente conectado', cliente)
	while True:
		msg = con.recv(TAM_MSG)
		if not msg or not processa_msg_cliente(msg, con, cliente): break
	con.close()
	print('Cliente desconectado', cliente)
	
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(50)

library = Library()
library.register_book(22, 'Bolsonarismo Radical')
library.register_book(13, 'Corinthians')

while True:
	try:
		con, cliente = sock.accept()
	except:
		break
	pid = os.fork()
	if pid == 0:
		sock.close()
		processa_cliente(con, cliente)
		break
	else:
		con.close()
sock.close()