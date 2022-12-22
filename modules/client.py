#!/usr/bin/env python3
import socket
import sys

MSG_SIZE = 1024 
HOST = '127.0.0.1'
PORT = 40000
LOGGED = False
USERNAME = ''
PASSWORD = ''

# catches the IP or IP/PORT if the client types it
if len(sys.argv) == 2:
	HOST = sys.argv[1]
elif len(sys.argv) == 3:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])

print('Library System\nServer:', HOST+':'+str(PORT)+'\n')

# creates the socket and connects it to the host and port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv = (HOST, PORT)
sock.connect(serv)

while True:
	try:
		command = input('KES -> ')
	except KeyboardInterrupt:
		print('\nDisconnecting...')
		break
	
	if command != '':
		# checks if the client is not logged 
		if not LOGGED:
			if (command.split(' ')[0].upper() == 'REGISTER' or command.split(' ')[0].upper() == 'LOGIN'):
				sock.send(str.encode(command)) # sends the command to the server
				data = sock.recv(MSG_SIZE) # receives a message from the server

				if not data: 
					break
 
				data = data.decode() # decodes the message received from the server
				print(data)

				# checks the code sent by the server and print the respective message
				data = data.split(' ')
				if data[1] == '20':
					LOGGED = True 
					USERNAME = command.split()[1] # gets the client username
					PASSWORD = command.split()[2] # gets the client password
					print('User registered successfully.\n')
				elif data[1] == '21':
					LOGGED = True
					USERNAME = command.split()[1] # gets the client username
					PASSWORD = command.split()[2] # gets the client password
					print('User logged in successfully.\n')
				elif data[1] == '29':
					print('Client disconnection request received successfully.\n')
					break
				elif data[1] == '40':
					print('Invalid command.\n')
				elif data[1] == '43':
					print('User already registered.\n')
				elif data[1] == '44':
					print('Username and/or password incorrect.\n')
 
			elif command.split(' ')[0].upper() == 'QUIT':
				
				sock.send(str.encode(command)) # sends the command to the server
				data = sock.recv(MSG_SIZE)  # receives a message from the server

				data = data.decode() # decodes the message received from the server

				data = data.split(' ')

				# checks the code sent by the server and print the respective message
				if data[1] == '29':
					print('+OK 29\n\nClient disconnection request received successfully.\n')
					break
     
			else: 
				# checks if the client tried to insert a valid command
				if (command.split(' ')[0].upper() in ('BOOKLIST', 'CHECK', 'LIST', 'LOAN', 'INFO', 'RENEW', 'RETURN')):
					print(f'-ERR 49\n\nLogin required.\n')
				else:
					print(f'-ERR 40 {command}\n\nInvalid command.\n')
				
		# checks if the client is logged and sent a 'login' command
		elif LOGGED and (command.split(' ')[0].upper() == 'LOGIN'):
			print('-ERR 42\n\nUser already logged in.\n')

		# checks if the client is logged and sent a 'register' command
		elif LOGGED and (command.split(' ')[0].upper() == 'REGISTER'):
			print('-ERR 41\n\nSession already initialized.\n')

		# the client is logged and sent a valid command		
		else:
			command += ' ' + USERNAME # attachs the client's username on the command
			sock.send(str.encode(command)) # sends the command to the server
			data = sock.recv(MSG_SIZE) # receives a message from the server

			if not data: 
				break

			data = data.decode() # decodes the message received from the server
			print(data)
			
			# checks the code sent by the server and print the respective message
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

	# if the command typed by the user does not match any of the valid commands
	else:
		print(f'\n-ERR 40 {command}\n\nInvalid command.\n')

sock.close() # closes the socket
