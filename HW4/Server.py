#Zack Barbari, zackaxal
#I certify that no unauthorized assistance has been received or given in the completion of this work.
import sys
import socket
input = ""
global current
current = 0
state = -2
sender = ""
recipients = []
hosts = []
email = ""
pathstart = -1
pathend = -1
hoststart = -1
#hostindex = -1
partner = ""
import os

def special():
	global current
	if input[current] in ['<', '>', '(', ')', '[', ']', ',', ';', ':', '@', '"', '\\', '.']:
		return True
	return False

def SP():
	global current
	if input[current] == "	" or input[current] == " ":
		return True
	return False

def CRLF():
	global current
	ascii = ord(input[current])
	if ascii == 10:
		return True
	return False

def char():
	global current
	if not(special() or SP()):
		return (ord(input[current]) < 128)
	return False

def digit():
	global current
	ascii = ord(input[current])
	return (ascii >= 48 and ascii <= 57)

def letter():
	global current
	ascii = ord(input[current])
	return (ascii >= 65 and ascii <= 90) or (ascii >= 97 and ascii <= 122)

def letdig():
	global current
	return (letter() or digit())

def letdigstr():
	global current
	if letdig():
		current += 1
		letdigstr()
		return True
	return False

def element():
	global current
	if letter():
		current += 1
		letdigstr()
		return True
	return False

def domain():
	global current
	if element():
		if input[current] == ".":
			current += 1
			if domain():
				return True
		else:
			return True
	return False

def string():
	global current
	if char():
		current += 1
		string()
		return True
	return False

def mailbox():
	global current
	global hoststart
	if string():
		if input[current] == '@':
			hoststart = current
			current += 1
			if domain():
				return True
	return False

def path():
	global pathstart
	global pathend
	global current
	if input[current] == '<':
		pathstart = current
		current += 1
		if mailbox():
			if input[current] == '>':
				current += 1
				pathend = current
				return True
	return False

def whitespace():
	global current
	if SP():
		current += 1
		whitespace()
		return True
	return False

def nullspace():
	whitespace()
	return True

def mailname():
	global current
	if len(input) >= 10 and input[0] == "M" and input[1] == "A" and input[2] == "I" and input[3] == "L":
		current = 4
		if whitespace():
			if input[current] == "F" and input[current+1] == "R" and input[current+2] == "O" and input[current+3] == "M" and input[current+4] == ":":
				current +=5
				return True
	return False

def mailfromcmd():
	global current
	if mailname():
		if nullspace():
			if path():
				if nullspace():
					if CRLF():
						current = 0
						return True
	current = 0
	return False

def rcptname():
	global current
	if len(input) >= 7 and input[0] == "R" and input[1] == "C" and input[2] == "P" and input[3] == "T":
		current = 4
		if whitespace():
			if input[current] == "T" and input[current+1] == "O" and input[current+2] == ":":
				current +=3
				return True
	return False
def rcpttocmd():
	global current
	if rcptname():
		if nullspace():
			if path():
				if nullspace():
					if CRLF():
						current = 0
						return True
	current = 0
	return False

def datacmd():
	global current
	if len(input) >= 4 and input[0] == "D" and input[1] == "A" and input[2] == "T" and input[3] == "A":
		current = 4
		if nullspace():
			if CRLF():
				current = 0
				return True
	current = 0
	return False

def commandcheck(key):
	global current
	if key == 0:
		if mailname():
			current = 0
			return True
		current = 0
		return False
	elif key == 1:
		if rcptname():
			current = 0
			return True
		current = 0
		return False
	elif key == 2:
		if datacmd():
			current = 0
			return True
		current = 0
		return False

def arbitrarytext():
	global input
	global current
	#print(current)
	ascii = ord(input[current])
	if (ascii >= 20 and ascii <= 127):
		current += 1
		arbitrarytext()
		return True
	return False

def helomsg():
	global current
	global input
	global partner
	if len(input) >= 4 and input[0] == "H" and input[1] == "E" and input[2] == "L" and input[3] == "O":
		current += 4
		if whitespace():
			if arbitrarytext():
				if CRLF():
					current = 0
					partner = input[4:].strip()
					return True
	#print (current)
	#print (input[0])
	current = 0
	return False

def hostpresent():
	global hosts
	global pathend
	#global hostindex
	for i in range(len(hosts)):
		if input[hoststart:pathend] == hosts[i]:
			#hostindex = i
			return True
	#hostindex = len(hosts)
	return False

recieve = False

try:
	PORT = int(sys.argv[1])
	HOST = socket.gethostname()
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	soc.bind((HOST, PORT))
	conn = ''
	addr = ''

	def newlisten():
		global soc
		global conn
		#print(conn)
		global state
		global recieve
		global addr
		#print("LISTEN")
		soc.listen()
		#print(conn)
		try:
			conn, addr = soc.accept()
			#print("LISTEN2")
		except BaseException as e:
			print(e)
			#print(soc)
			#print(conn)
			soc.close()
			#print(soc)
			#print("r")
			sys.exit()
			#print("b")
		#print(conn)
		#print(f'connection from {addr}')
		#print(f'220 {HOST}')
		conn.sendall(f'220 {HOST}\n'.encode())
		state = -1
		recieve = True

	if conn == '':
		newlisten()
	#recieve = True
except Exception as er:
	print(er)
	soc.close()
	#print("a")
	sys.exit()

def resetemail():
	#print("E")
	global conn
	global current
	global state
	global sender
	global recipients
	global email
	global open
	global recieve
	global hosts
	global input
	global partner
	global soc
	conn.close()
	partner = ""
	state = -2
	current = 0
	sender = ""
	recipients = []
	hosts = []
	email = ""
	msginput = ''
	input = ''
	recieve = False
	newlisten()
	#print("know")

msginput = ''

while (recieve):
	try:
		#print(state)
		#print(f'START: {input}')
		#input = conn.recv(2048).decode()
		#print(f'HERE IN SOCKET {input}', end="")
		if len(input) == 5 and input[0] == "Q" and input[1] == "U" and input[2] == "I" and input[3] == "T":
			#print(f'INPUT: {input}')
			#print(f'221 {HOST} closing connection')
			conn.sendall(f'221 {HOST} closing connection\n'.encode())
			resetemail()
			#print('se')
			state = -2
		#Accepting HELO message
		if state == -1:
			input = conn.recv(2048).decode()
			if helomsg():
				#print(f'250 Hello {partner} pleased to meet you')
				conn.sendall(f'250 Hello {partner} pleased to meet you\n'.encode())
				state = 0
			else:
				#print(f'ERROR -> {input}')
				#print(len(input))
				resetemail()
		#Only accepting MAIL FROM:
		if state == 0:
			msginput = conn.recv(2048).decode()
			#msginput = 'MAIL FROM:<jack@cs.unc.edu>\nRCPT TO:<.jeffay@cs.unc.edu >\n'
			#msginput = 'MAIL FROM:<jeffay@cs.un*c.edu>\n'
			#msginput = ' MAIL FROM:<jeffay@cs.unc.edu>\n'
			#msginput = 'MAIL FROM:<jack@cs.unc.edu>\nRCPT TO:<jake@cs.unc.edu>\n MAIL FROM:<jeffay@unc.edu>\n'
			msginput = msginput.split('\n')
			for i in range(len(msginput)):
				msginput[i] += '\n'
			msginput.pop(len(msginput)-1)
			input = msginput[0]
			#print(msginput)
			#print(input)
			if mailfromcmd():
				#print('250 OK')
				conn.send('250 OK\n'.encode())
				state = 1
				msginput.pop(0)
			else:
				if commandcheck(1) or commandcheck(2):
					#print('503 Bad sequence of commands')
					conn.senadall('503 Bad sequence of commands\n'.encode())
				elif commandcheck(0):
					#print('501 Syntax error in parameters or arguments')
					conn.sendall('501 Syntax error in parameters or arguments\n'.encode())
				else:
					#print('500 Syntax error: command unrecognized')
					conn.sendall('500 Syntax error: command unrecognized\n'.encode())
				#resetemail()
				state = -3
		#Only accepting RCPT TO:
		elif state == 1:
			input = msginput[0]
			#print(input)
			if rcpttocmd():
				#print('250 OK')
				conn.send('250 OK\n'.encode())
				state = 2
				msginput.pop(0)
				if not hostpresent():
					hosts.append(input[hoststart:pathend])
				recipients.append(input[pathstart:pathend])
			else:
				if commandcheck(0) or commandcheck(2):
					#print('503 Bad sequence of commands')
					conn.send('503 Bad sequence of commands\n'.encode())
				elif commandcheck(1):
					#print('501 Syntax error in parameters or arguments')
					conn.send('501 Syntax error in parameters or arguments\n'.encode())
				else:
					#print('500 Syntax error: command unrecognized')
					conn.send('500 Syntax error: command unrecognized\n'.encode())
				#resetemail()
				state = -3
		#Accepting both RCPT TO: and DATA
		elif state == 2:
			input = msginput[0]
			#print(input)
			if rcpttocmd():
				#print('250 OK')
				conn.send('250 OK\n'.encode())
				msginput.pop(0)
				if not hostpresent():
					hosts.append(input[hoststart:pathend])
				recipients.append(input[pathstart:pathend])
			elif datacmd():
				#print('354 Start mail input; end with <CRLF>.<CRLF>')
				conn.send('354 Start mail input; end with <CRLF>.<CRLF>\n'.encode())
				state = 3
				msginput.pop(0)
				#print(msginput[0])
			else:
				if commandcheck(0):
					#print('503 Bad sequence of commands')
					conn.send('503 Bad sequence of commands\n'.encode())
				elif commandcheck(1):
					#print('501 Syntax error in parameters or arguments')
					conn.send('501 Syntax error in parameters or arguments\n'.encode())
				else:
					#print('500 Syntax error: command unrecognized')
					conn.send('500 Syntax error: command unrecognized\n'.encode())
				#resetemail()
				state = -3
		#Email body input
		elif state == 3:
			input = msginput[0]
			#print(input)
			if len(input) == 2 and input[0] == "." and ord(input[1]) == 10:
				#print('250 OK')
				conn.sendall('250 OK\n'.encode())
				input = conn.recv(2048).decode()
				for i in range(len(hosts)):
					#print(recipients[i][1:-1])
					pathfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'forward', hosts[i][1:-1])
					file = open(pathfile, 'a')
					print(f'PATH: {pathfile}')
					print(email)
					file.write(email)
					file.close()
				state = -2
				#print("Successfully written")
				#print(input)
			else:
				email += input
				msginput.pop(0)
		elif (state == -2):
			state = -1
		elif (state == -3):
			input = conn.recv(2048).decode()
	except Exception as error:
		print(error)
		conn.send('CLOSE CONNECTION'.encode())
		#print('errororor')
		resetemail()
	except KeyboardInterrupt as error:
		#print(soc)
		soc.close()
#except:
	#print('There was an error while parsing your email.')
	#resetemail()


#if state == 3:
	#print('501 Syntax error in parameters or arguments')
	#conn.send('501 Syntax error in parameters or arguments\n'.encode())
#print(soc.getsockname())
#soc.shutdown(socket.SHUT_RDWR)
#print(soc)
soc.close()
