#!/usr/bin/env python3
import socket
import sys

TAM_MSG = 1024 
HOST = '127.0.0.1'
PORT = 40000
LOGGED = False
USERNAME = ''
PASSWORD = ''

def decode_cmd_usr(cmd_usr):
	cmd_map = {
		'register': 'register',  # [USERNAME] [PASSWORD] = register a new user
		'login': 'login', # [USERNAME] [PASSWORD] = log in a registered user
		'check': 'check', # [BOOK ISBN] = check if a book is available for loan
		'list': 'list', # = check the user's loan list
		'loan': 'loan', # [BOOK ISBN] = loan a book
		'info': 'info', # [LOAN ID] = check loan's info
		'renew': 'renew', # [LOAN ID] = renew a book loan
		'return': 'return', # [LOAN ID] = return a book
		'booklist': 'booklist', # = show all books
		'quit': 'quit', # quit the connection
	}
	tokens = cmd_usr.split()
	if tokens[0].lower() in cmd_map:
		return " ".join(tokens)
	
	return cmd_usr

		
if len(sys.argv) == 2:
	HOST = sys.argv[1]
elif len(sys.argv) == 3:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])


print('Servidor:', HOST+':'+str(PORT))

serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)

print('Para encerrar use QUIT ou CTRL+C\n')

while True:
	try:
		cmd_usr = input('KES> ')
	except KeyboardInterrupt:
		print('\nDisconnecting...')
		break
	
	if cmd_usr != '':
		cmd = decode_cmd_usr(cmd_usr)

		if not LOGGED:
			if (cmd_usr.split(' ')[0].upper() == 'REGISTER' or cmd_usr.split(' ')[0].upper() == 'LOGIN'):
				sock.send(str.encode(cmd))
				data = sock.recv(TAM_MSG)

				if not data: 
					break
 
				data = data.decode()
				print(data)

				data = data.split(' ')
				if data[1] == '20':
					LOGGED = True
					USERNAME = cmd_usr.split()[1]
					PASSWORD = cmd_usr.split()[2]
					print('User registered successfully.\n')
				elif data[1] == '21':
					USERNAME = cmd_usr.split()[1]
					PASSWORD = cmd_usr.split()[2]
					LOGGED = True
					print('User logged in successfully.\n')
				elif data[1] == '29':
					print('Client disconnect request received successfully.\n')
					break
				elif data[1] == '40':
					print('Invalid command.\n')
				elif data[1] == '43':
					print('User already registered.\n')
				elif data[1] == '44':
					print('Username and/or password incorrect.\n')
 
			elif cmd_usr.split(' ')[0].upper() == 'QUIT':
				
				sock.send(str.encode(cmd))
				data = sock.recv(TAM_MSG)

				data = data.decode()

				data = data.split(' ')

				if data[1] == '29':
					print('+OK 29\n\nClient disconnect request received successfully.\n')
					break
     
			else:
				if (cmd_usr.split(' ')[0].upper() in ('BOOKLIST', 'CHECK', 'LIST', 'LOAN', 'INFO', 'RENEW', 'RETURN')):
					print(f'-ERR 49\n\nLogin required.\n')
				else:
					print(f'-ERR 40 {cmd_usr}\n\nInvalid command.\n')
				

		elif LOGGED and (cmd_usr.split(' ')[0].upper() == 'LOGIN'):
			print('-ERR 42\n\nUser already logged in.\n')

		elif LOGGED and (cmd_usr.split(' ')[0].upper() == 'REGISTER'):
			print('-ERR 41\n\nSession already initialized.\n')
				
		else:
			cmd += ' ' + USERNAME
			sock.send(str.encode(cmd))
			data = sock.recv(TAM_MSG)

			if not data: 
				break

			data = data.decode()
			print(data)
			
			data = data.split(' ')
			if data[1] == '22':
				print('Booklist accessed successfully.\n')
			elif data[1] == '23':
				print('Book available for loan.\n')
			elif data[1] == '24':
				print('Loan done successfully.\n')
			elif data[1] == '25':
				print('Loan info accessed successfully.\n')
			elif data[1] == '26':
				print('Loan list accessed successfully.\n')
			elif data[1] == '27':
				print('Loan renewed successfully.\n')
			elif data[1] == '28':
				print('Loan returned successfully.\n')
			elif data[1] == '29':
				print('Client disconnect request received successfully.\n')
				break
			elif data[1] == '40':
				print('Invalid command.\n')
			elif data[1] == '45':
				print('Book not registered.\n')
			elif data[1] == '46':
				print('Book unavailable for loan.\n')
			elif data[1] == '47':
				print('Unexistent loan for this user.\n')
			elif data[1] == '48':
				print('Loan already late.\n')

	else:
		print(f'\n-ERR 40 {cmd_usr}\n\nInvalid command.\n')

sock.close()
