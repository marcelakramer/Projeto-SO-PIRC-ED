import sys
sys.path.append('./..')

#import src.library as Library
from src.library import Library
from structures.exceptions import *

import socket
import os
import datetime

TAM_MSG = 1024 
HOST = '0.0.0.0' 
PORT = 40000 

def process_msg_client(msg, con, client):
	msg = msg.decode()
	print('client', client, 'enviou', msg)
	msg = msg.split()
	if msg[0].upper() == 'REGISTER' and len(msg) == 3:
		try:
			library.register_user(msg[1],msg[2])
			con.send(str.encode(f"+OK \nUser '{msg[1]}' registered successfully.\n"))
   
		except AlreadyExistingObjectException:
			con.send(str.encode(f'-ERR\nUser already registered\n'))

	elif msg[0].upper() == 'CHECK' and len(msg) == 2:
		try:
			book_title = library.bookshelf.getBook(int(msg[1])).title
			if library.check_available(int(msg[1])):
				con.send(str.encode(f"+OK \n'The book {book_title}' is available for loan.\n"))
			else:
				con.send(str.encode(f"-ERR \nThe book '{book_title}' is unavailable for loan.\n"))

		except AbsentObjectException:
			con.send(str.encode(f"-ERR \nThe book is not registered.\n"))

	elif msg[0].upper() == 'LIST' and len(msg) == 3:
		try:
			loanlist = library.check_loan_list(msg[1], msg[2])
			con.send(str.encode(f"+OK \nUser '{msg[1]}' loan list: \n{loanlist}"))

		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'LOAN' and len(msg) == 4:
		try:
			loan = library.loan_book(int(msg[1]), msg[2], msg[3])
			if loan[0]:
				book_title = library.bookshelf.getBook(int(msg[1])).title
				con.send(str.encode(f"+OK \nLoan Nº{loan[1]} of book '{book_title}' made successfully by '{msg[2]}'.\n"))
		
		except AbsentObjectException:
			con.send(str.encode(f"-ERR \nThe book is not registered.\n"))
		except UnavailableObjectException:
			con.send(str.encode(f"-ERR \nThe book is unavailable for loan.\n"))
		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'INFO' and len(msg) == 4:
		try:
			loan_info = library.check_loan_info(int(msg[1]), msg[2], msg[3])
			con.send(str.encode(f"+OK \nLoan information: {loan_info}"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERR \nUser '{msg[2]}' has no loan Nº {msg[1]}.\n"))
		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'RENEW' and len(msg) == 4:
		try:
			if library.renew_loan(int(msg[1]), msg[2], msg[3]):
				con.send(str.encode(f"+OK \nLoan Nº{msg[1]} was renewed succesfully by '{msg[2]}'.\n"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERR \nUser '{msg[2]}' has no loan Nº {msg[1]}.\n"))
		except UnavailableObjectException:
			con.send(str.encode(f"+OK \nLoan Nº{msg[1]} is already late.\n"))
		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'RETURN' and len(msg) == 4:
		try:
			library.return_book(int(msg[1]), msg[2], msg[3])
			con.send(str.encode(f"+OK \nLoan Nº{msg[1]} was returned succesfully by '{msg[2]}'.\n"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERR \nUser '{msg[2]}' has no loan Nº {msg[1]}.\n"))
		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'QUIT' and len(msg) == 1:
		con.send(str.encode('+OK \nDisconnecting...\n'))
		return False

	else:
		con.send(str.encode(f'-ERR \nInvalid command: {msg}'))
	return True
	
def process_client(con, client):
	print('Connected client: ', client)
	while True:
		msg = con.recv(TAM_MSG)
		if not msg or not process_msg_client(msg, con, client):
			break
	con.close()
	print('Disconnected client: ', client)
	
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.bind(serv)
sock.listen(50)

library = Library()
library.register_book(10, 'Harry Potter')
library.register_book(20, 'O Pequeno Príncipe')
library.register_book(30, 'Dom Quixote')
library.register_book(40, 'Hamlet')
library.register_book(50, 'Os Miseráveis')

while True:
	try:
		con, client = sock.accept()
	except:
		break
	pid = os.fork()
	if pid == 0:
		sock.close()
		process_client(con, client)
		break
	else:
		con.close()
sock.close()
