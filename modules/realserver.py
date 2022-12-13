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
			con.send(str.encode(f"+OK \nUser '{msg[1]}' registered successfully."))
   
		except AlreadyExistingObjectException:
			con.send(str.encode(f'-ERROR\nUser already registered'))

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
			book_title = library.bookshelf.getBook(int(msg[1])).title
			if library.check_available(int(msg[1])):
				con.send(str.encode(f"+OK \n'{book_title}' is available for loan.\n"))
			else:
				con.send(str.encode(f"-ERROR \nThe book '{book_title}' is unavailable for loan.\n"))

		except AbsentObjectException:
			con.send(str.encode(f"-ERROR \nThe book '{book_title}' is not registered.\n"))

	elif msg[0].upper() == 'LOAN':
		try:
			loan = library.loan_book(int(msg[1]), msg[2], msg[3])
			if loan[0]:
				book_title = library.bookshelf.getBook(int(msg[1])).title
				con.send(str.encode(f"+OK \nLoan Nº{loan[1]} of book '{book_title}' made successfully by '{msg[2]}'.\n"))
   
		except UnavailableObjectException:
			con.send(str.encode(f"-ERROR \nThe book '{book_title}' is unavailable.\n"))

	elif msg[0].upper() == 'INFO':
		try:
			loan_info = library.check_loan_info(int(msg[1]), msg[2], msg[3])

			con.send(str.encode(f"+OK \nLoan information: {loan_info}\n"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERROR \n'User {msg[2]}' has no loan Nº {msg[1]}.\n"))

	elif msg[0].upper() == 'RENEW':
		try:
			if library.renew_loan(int(msg[1]), msg[2], msg[3]):
				con.send(str.encode(f"+OK \nLoan Nº{msg[1]} was renewed succesfully by '{msg[2]}'.\n"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERROR \n'User {msg[2]}' has no loan Nº {msg[1]}.\n"))
		except UnavailableObjectException:
			con.send(str.encode(f"+OK \nLoan Nº{msg[1]} is already late.\n"))



	elif msg[0].upper() == 'RETURN':
		try:
			library.return_book(int(msg[1]), msg[2], msg[3])
			con.send(str.encode(f"+OK \nLoan Nº{msg[1]} was returned succesfully by '{msg[2]}'.\n"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERROR \n'User {msg[2]}' has no loan Nº {msg[1]}.\n"))

	else:
		con.send(str.encode('-ERROR \nInvalid command.\n'))
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