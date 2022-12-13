#!/usr/bin/env python3
import socket
import sys
TAM_MSG = 1024 # Tamanho do bloco de mensagem
HOST = '127.0.0.1' # IP do Servidor
PORT = 40000 # Porta que o Servidor escuta
def decode_cmd_usr(cmd_usr):
	cmd_map = {
		'register': 'register',  # [USERNAME] [PASSWORD] = register a new user
		'check': 'check', # [BOOK ISBN] = check if a book is available for loan
		'loan': 'loan', # [BOOK ISBN] [USERNAME] [PASSWORD] = loan a book
		'info': 'info', # [LOAN ID] = check loan's info
		'renew': 'renew', # [LOAN ID] [USERNAME] [PASSWORD] = renew a book loan
		'return': 'return', # [LOAN ID] = return a book
		'quit': 'quit', # [LOAN ID] = return a book
	}
	tokens = cmd_usr.split()
	if tokens[0].lower() in cmd_map:
		#tokens[0] = cmd_map[tokens[0].lower()]
		return " ".join(tokens)
	else:
		return False
		
if len(sys.argv) > 1:
	HOST = sys.argv[1] # If an IP is passed in the script call, the host receivs it.
					   # Example: python client.py 192.168.0.5

print('Servidor:', HOST+':'+str(PORT))
serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)
print('Para encerrar use QUIT, CTRL+D ou CTRL+C\n')
while True:
	try:
		cmd_usr = input('BTP> ')
	except:
		cmd_usr = 'QUIT'

	cmd = decode_cmd_usr(cmd_usr)

	if not cmd:
		print('Comando indefinido:', cmd_usr)

	else:
		sock.send(str.encode(cmd))

		data = sock.recv(TAM_MSG)

		if not data: break

		msg_status = data.decode().split('\n')[0]
		data = data.decode()
		# data = data[len(msg_status)+1:]
		print(f'data 1: {data}')
		print(msg_status)
		cmd = cmd.split()
		cmd[0] = cmd[0].upper()

		if cmd[0] == 'QUIT':
			break

		elif cmd[0] == 'REGISTER':
			# 
			print(f'data 2: {data}')
			# while True:
			# 	arquivos = data.split('\n')
			# 	residual = arquivos[-1] # último sem \n fica para próxima
			# 	for arq in arquivos[:-1]:
			# 		print(arq)
			# 		num_arquivos -= 1
			# 	if num_arquivos == 0: break
			# data = sock.recv(TAM_MSG)
			#print(f'data 3: {data}')
			if not data: break
			
			# data = residual + data.decode()

		elif cmd[0] == 'CHECK':
			nome_arq = " ".join(cmd[1:])
			print('Recebendo:', nome_arq)
			arq = open(nome_arq, "wb")
			tam_arquivo = int(msg_status.split()[1])
			while True:
				arq.write(dados)
				tam_arquivo -= len(data)
				if tam_arquivo == 0: break
				data = sock.recv(TAM_MSG)
				if not data: break
			arq.close()

		elif cmd[0] == 'LOAN':
			nome_arq = " ".join(cmd[1:])
			print('Recebendo:', nome_arq)
			arq = open(nome_arq, "wb")
			tam_arquivo = int(msg_status.split()[1])
			while True:
				arq.write(data)
				tam_arquivo -= len(data)
				if tam_arquivo == 0: break
				dados = sock.recv(TAM_MSG)
				if not dados: break
			arq.close()

		elif cmd[0] == 'INFO':
			nome_arq = " ".join(cmd[1:])
			print('Recebendo:', nome_arq)
			arq = open(nome_arq, "wb")
			tam_arquivo = int(msg_status.split()[1])
			while True:
				arq.write(dados)
				tam_arquivo -= len(data)
				if tam_arquivo == 0: break
				dados = sock.recv(TAM_MSG)
				if not dados: break
			arq.close()

		elif cmd[0] == 'RENEW':
			nome_arq = " ".join(cmd[1:])
			print('Recebendo:', nome_arq)
			arq = open(nome_arq, "wb")
			tam_arquivo = int(msg_status.split()[1])
			while True:
				arq.write(dados)
				tam_arquivo -= len(data)
				if tam_arquivo == 0: break
				dados = sock.recv(TAM_MSG)
				if not dados: break
			arq.close()

		elif cmd[0] == 'QUIT':
			nome_arq = " ".join(cmd[1:])
			print('Recebendo:', nome_arq)
			arq = open(nome_arq, "wb")
			tam_arquivo = int(msg_status.split()[1])
			while True:
				arq.write(dados)
				tam_arquivo -= len(data)
				if tam_arquivo == 0: break
				dados = sock.recv(TAM_MSG)
				if not dados: break
			arq.close()


sock.close()