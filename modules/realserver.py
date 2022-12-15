import sys
sys.path.append('./..')

#import src.library as Library
from src.library import Library
from structures.exceptions import *

import socket
import os
import threading
import time

TAM_MSG = 1024 
HOST = '0.0.0.0' 
PORT = 40000 

mutex = threading.Semaphore(1)

def process_msg_client(msg, con, client):
	msg = msg.decode()
	print(f'Client {client} sent {msg}')
	msg = msg.split()
	if msg[0].upper() == 'REGISTER' and len(msg) == 3:
		try:
			library.register_user(msg[1],msg[2])
			con.send(str.encode(f"+OK 21 {msg[1]}\n"))
   
		except AlreadyExistingObjectException:
			con.send(str.encode(f'-ERR 41 \n'))

	elif msg[0].upper() == 'CHECK' and len(msg) == 2 and msg[1].isdigit():
		try:
			book_title = library.bookshelf.getBook(int(msg[1])).title
			if library.check_available(int(msg[1])):
				con.send(str.encode(f"+OK 23 {book_title} \n"))
			else:
				con.send(str.encode(f"-ERR 44 \n"))

		except AbsentObjectException:
			con.send(str.encode(f"-ERR 43 \n"))

	elif msg[0].upper() == 'LIST' and len(msg) == 3:
		try:
			loanlist = library.check_loan_list(msg[1], msg[2])
			con.send(str.encode(f"+OK 26 {msg[1]} \n{loanlist}"))

		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'LOAN' and len(msg) == 4 and msg[1].isdigit():
		mutex.acquire()

		try:
			loan = library.loan_book(int(msg[1]), msg[2], msg[3])
			time.sleep(5)
			if loan[0]:
				book_title = library.bookshelf.getBook(int(msg[1])).title
				con.send(str.encode(f"+OK 24 {loan[1]} {book_title}\n"))
		
		except AbsentObjectException:
			con.send(str.encode(f"-ERR 43 \n"))
		except UnavailableObjectException:
			con.send(str.encode(f"-ERR 44 \n"))
		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

		mutex.release()

	elif msg[0].upper() == 'INFO' and len(msg) == 4 and msg[1].isdigit():
		try:
			loan_info = library.check_loan_info(int(msg[1]), msg[2], msg[3])
			con.send(str.encode(f"+OK 25 \n{loan_info}"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERR 45 \n"))
		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'RENEW' and len(msg) == 4 and msg[1].isdigit():
		try:
			if library.renew_loan(int(msg[1]), msg[2], msg[3]):
				con.send(str.encode(f"+OK 27 {msg[1]}\n"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERR 45 \n"))
		except UnavailableObjectException:
			con.send(str.encode(f"-ERR 46 \n"))
		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'RETURN' and len(msg) == 4 and msg[1].isdigit():
		try:
			library.return_book(int(msg[1]), msg[2], msg[3])
			con.send(str.encode(f"+OK 28 {msg[1]}\n"))
   
		except AbsentObjectException:
			con.send(str.encode(f"-ERR 45 \n"))
		except LoginFailException as lfe:
			con.send(str.encode(f"{lfe}\n"))

	elif msg[0].upper() == 'QUIT' and len(msg) == 1:
		con.send(str.encode('+OK 29 \n'))
		return False

	else:
		msg = (' ').join(msg)
		con.send(str.encode(f'-ERR 40 {msg}\n'))
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

	threading.Thread(target=process_client, args=(con, client)).start()

	# acredito que essa parte da implementação esteja errada, mas funciona	

	""" pid = os.fork()
	if pid == 0:
		sock.close()
		process_client(con, client)
		break
	else:
		con.close() """
sock.close()
