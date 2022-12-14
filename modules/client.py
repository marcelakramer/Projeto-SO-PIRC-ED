#!/usr/bin/env python3
import socket
import sys

TAM_MSG = 1024 
HOST = '127.0.0.1'
PORT = 40000


def decode_cmd_usr(cmd_usr):
	cmd_map = {
		'register': 'register',  # [USERNAME] [PASSWORD] = register a new user
		'check': 'check', # [BOOK ISBN] = check if a book is available for loan
		'list': 'list', # [USERNAME] [PASSWORD] = check the user's loan list
		'loan': 'loan', # [BOOK ISBN] [USERNAME] [PASSWORD] = loan a book
		'info': 'info', # [LOAN ID] = check loan's info
		'renew': 'renew', # [LOAN ID] [USERNAME] [PASSWORD] = renew a book loan
		'return': 'return', # [LOAN ID] = return a book
		'quit': 'quit', # quit the connection
	}
	tokens = cmd_usr.split()
	if tokens[0].lower() in cmd_map:
		return " ".join(tokens)
	else:
		return False
		
if len(sys.argv) == 2:
	HOST = sys.argv[1]
elif len(sys.argv) == 3:
	PORT = int(sys.argv[2])
else:
	print('Invalid command. Please, restart the client.')
	

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

		if not cmd:
			print(f'\n-ERR \nInvalid command: {cmd_usr}\n')

		elif cmd.upper() == 'QUIT':
			print('+OK\nDisconnecting...')
			break

		else:
			sock.send(str.encode(cmd))
			data = sock.recv(TAM_MSG)

			if not data: 
				break

			data = data.decode()
			print(f'\n{data}')
	else:
		print(f'\n-ERR \nInvalid command: {cmd_usr}\n')

sock.close()
