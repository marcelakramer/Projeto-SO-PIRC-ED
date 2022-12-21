from tempfile import NamedTemporaryFile
import shutil
import csv


import sys
sys.path.append('./..')

#import src.library as Library
from src.library import Library
from structures.exceptions import *


import socket
import threading

TAM_MSG = 1024 
HOST = '0.0.0.0' 
PORT = 40002

mutex = threading.Semaphore(1)

def process_msg_client(msg, con, client):
	msg = msg.decode()
	print(f'Client {client} sent {msg}')
	msg = msg.split()

	if msg[0].upper() == 'REGISTER' and len(msg) == 3:
		try:
			library.register_user(msg[1],msg[2]) # tries to register a new user passing the username and the password
			con.send(str.encode(f"+OK 20 {msg[1]}\n")) # sends successful status to the client
   

		# If it alteady exists
		except AlreadyExistingObjectException:
			con.send(str.encode(f'-ERR 43 \n'))

	elif msg[0].upper() == 'LOGIN' and len(msg) == 3:
		try:
			if library.login(msg[1],msg[2]):
				con.send(str.encode(f"+OK 21 {msg[1]}\n")) # sends successful status to the client
			else:
				con.send(str.encode(f'-ERR 44 \n'))
   
		# Password and/or username is incorrect
		except AbsentObjectException:
			con.send(str.encode(f'-ERR 44 \n'))


	# List all books
	elif msg[0].upper() == 'BOOKLIST' and len(msg) == 2:
		# calls method that returns an "inOrder" of all books
		booklist = library.bookList() 

		# sends successful status to the client
		con.send(str.encode(f"+OK 22 \n{booklist}")) 


	# Check if a book is available
	elif msg[0].upper() == 'CHECK' and len(msg) == 3 and msg[1].isdigit():
		try:
			# Gets the title of the book based on the ISBN
			book_title = library.bookshelf.get(int(msg[1])).title

			# Check if it is available
			if library.check_available(int(msg[1])):
				# sends successful status to the client
				con.send(str.encode(f"+OK 23 {book_title} \n")) 
			else:
				con.send(str.encode(f"-ERR 46 \n"))

		except AbsentObjectException:
			con.send(str.encode(f"-ERR 45 \n"))

			
	# Tries to loan a book
	elif msg[0].upper() == 'LOAN' and len(msg) == 3 and msg[1].isdigit():
		try:
			# Calls loan method passing the ISBN and the username
			
			loan = library.loan_book(int(msg[1]), msg[2])
			
			# loan[0] should be True if it worked
			if loan[0]:
				# Gets the title of the book based on the ISBN
				book_title = library.bookshelf.get(int(msg[1])).title

				con.send(str.encode(f"+OK 24 {loan[1]} {book_title}\n")) # sends successful status to the client
		
		# If a book is not registered:
		except AbsentObjectException:
			con.send(str.encode(f"-ERR 45 \n"))

		# If a book is not available for loan:
		except UnavailableObjectException:
			con.send(str.encode(f"-ERR 46 \n"))
		
			
	# Checks the info of a loan
	elif msg[0].upper() == 'INFO' and len(msg) == 3 and msg[1].isdigit():
		try:
			# Gets the information based on the ID and the username
			loan_info = library.check_loan_info(int(msg[1]), msg[2])
			con.send(str.encode(f"+OK 25 \n{loan_info}")) # sends successful status to the client
	
		# If the user has no loan with that ID
		except AbsentObjectException:
			con.send(str.encode(f"-ERR 47 \n"))

	
	# Returns all the loan list of a user
	elif msg[0].upper() == 'LIST' and len(msg) == 2:
		# calls the method to receive the data as a string
		loanlist = library.check_loan_list(msg[1])
		con.send(str.encode(f"+OK 26 {msg[1]} \n{loanlist}")) # sends successful status to the client
		
			
	# Renew an specific loan
	elif msg[0].upper() == 'RENEW' and len(msg) == 3 and msg[1].isdigit():
		try:
			# the renew_loan returns a boolean
			if library.renew_loan(int(msg[1]), msg[2]):
				con.send(str.encode(f"+OK 27 {msg[1]}\n")) # sends successful status to the client
   
		# If there is no loan for that user:
		except AbsentObjectException:
			con.send(str.encode(f"-ERR 47 \n"))

		# If loan is late (Not possible to renew a late loan)
		except UnavailableObjectException:
			con.send(str.encode(f"-ERR 48 \n"))
		
			
	# Returns a loaned book
	elif msg[0].upper() == 'RETURN' and len(msg) == 3 and msg[1].isdigit():
		try:
			# Calls the method to return a book passing the loan ID and the username
			library.return_book(int(msg[1]), msg[2])
			con.send(str.encode(f"+OK 28 {msg[1]}\n")) # sends successful status to the client
	
		# If that loan does not existe for that user:
		except AbsentObjectException:
			con.send(str.encode(f"-ERR 47 \n"))
		
	# To finish a client connection
	elif msg[0].upper() == 'QUIT' and (len(msg) == 1 or len(msg) == 2): 

		with open("library_loans.csv", "w") as loans:
				reader = library.loans
				writer = csv.writer(loans)

				for row in range(1,len(reader) +1):
					loan = reader.get(row)

					writer.writerow([loan.id,loan.book.id,loan.date,loan.renewal,loan.devolution,loan.returned,loan.status,loan.username])
		
		con.send(str.encode('+OK 29 \n')) # sends successful status to the client
		return False




	# If none of those methods matched the user input:
	else:
		msg = (' ').join(msg[:-1])
		con.send(str.encode(f'-ERR 40 {msg}\n'))
	return True


# Handles every new client connection
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

while True:
	try:
		con, client = sock.accept()
	except:
		break

	threading.Thread(target=process_client, args=(con, client)).start()

sock.close()
