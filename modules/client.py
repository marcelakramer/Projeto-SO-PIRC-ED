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
		'login': 'login', # [LOGIN] [USERNAME] [PASSWORD] = log in a registered user
		'check': 'check', # [BOOK ISBN] = check if a book is available for loan
		'list': 'list', # [USERNAME] [PASSWORD] = check the user's loan list
		'loan': 'loan', # [BOOK ISBN] [USERNAME] [PASSWORD] = loan a book
		'info': 'info', # [LOAN ID] = check loan's info
		'renew': 'renew', # [LOAN ID] [USERNAME] [PASSWORD] = renew a book loan
		'return': 'return', # [LOAN ID] = return a book
		'booklist': 'booklist', # [BOOKLIST] = show all books
		'quit': 'quit', # quit the connection
	}
	tokens = cmd_usr.split()
	if tokens[0].lower() in cmd_map:
		return " ".join(tokens)
	
	return cmd_usr

		
if len(sys.argv) == 2:
	HOST = sys.argv[1]
elif len(sys.argv) == 3:
	PORT = int(sys.argv[2])


print('Servidor:', HOST+':'+str(PORT))

serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)

print('Para encerrar use QUIT ou CTRL+C\n')

while True:
	try:
		cmd_usr = input('KES> ')
		print(cmd_usr.split(' '))
	except KeyboardInterrupt:
		print('\nDisconnecting...')
		break
	
	if cmd_usr != '':
		cmd = decode_cmd_usr(cmd_usr)

		"""if cmd.upper() == 'QUIT':
			print('+OK 29\nDisconnecting...')
			break"""
		if not LOGGED:
			if (cmd_usr.split(' ')[0].upper() == 'REGISTER' or cmd_usr.split(' ')[0].upper() == 'LOGIN'):
				sock.send(str.encode(cmd))
				data = sock.recv(TAM_MSG)

				if not data: 
					break
 
				data = data.decode()
				print(f'\n{data}')

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
				elif data[1] == '40':
					print('Invalid command.\n')
				elif data[1] == '41':
					print('User already registered.\n')
				elif data[1] == '42':
					print('Username and/or password incorrect.\n')
				elif data[1] == '29':
					print('Client disconnect request received successfully.\n')
					break
 
			elif cmd_usr.split(' ')[0].upper() == 'QUIT':
				
				sock.send(str.encode(cmd))
				data = sock.recv(TAM_MSG)
    

				data = data.decode()
				print(f'\n{data}')

				data = data.split(' ')

				if data[1] == '29':
					print('Client disconnect request received successfully.\n')
					break
					
				
				
     
			else:
				print(f'\n You need to be logged in to use this command.\n')
		elif LOGGED and (cmd_usr.split(' ')[0].upper() == 'LOGIN'):
			print('\nUser already logged in.\n')

		elif LOGGED and (cmd_usr.split(' ')[0].upper() == 'REGISTER'):
			print('\nSession already initialized.\n')
				
		else:
			cmd += ' ' + USERNAME
			sock.send(str.encode(cmd))
			data = sock.recv(TAM_MSG)

			if not data: 
				break

			data = data.decode()
			print(f'\n{data}')
			
			data = data.split(' ')
			if data[1] == '22':
				print('Booklist accessed successfully.')
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
			elif data[1] == '43':
				print('Book not registered.\n')
			elif data[1] == '44':
				print('Book unavailable for loan.\n')
			elif data[1] == '45':
				print('Unexistent loan for this user.\n')
			elif data[1] == '46':
				print('Loan already late.\n')

	else:
		print(f'\n-ERR 40 {cmd_usr}\n\nInvalid command.\n')

sock.close()
