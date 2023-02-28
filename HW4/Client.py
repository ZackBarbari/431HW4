#Zack Barbari, zackaxal
#I certify that no unauthorized assistance has been received or given in the completion of this work.

import socket
import sys
response = ""
input = ""
inputp = ""
current = 0
state = -2
rcptstart = 0
rcpts = []
responsearray = []

def special():
	global input
	global current
	if input[current] in ['<', '>', '(', ')', '[', ']', ',', ';', ':', '@', '"', '\\', '.']:
		return True
	return False

def SP():
	global current
	global input
	if input[current] == "	" or input[current] == " ":
		return True
	return False

def CRLF():
	global current
	ascii = ord(input[current])
	if ascii == 10:
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

def breakread():
	global soc
	global sending
	global response
	#print('QUIT')
	soc.sendall('QUIT\n'.encode())
	#file.close()
	response = soc.recv(2048).decode()
	#print(f'EXP: 221, REC: {response}')
	print('Error in connection with server, please try again')
	sending = False

def arbitrarytext():
	global input
	global current
	#print(current)
	try:
		ascii = ord(input[current])
	except:
		return False
	if ascii >= 20 and ascii <= 127:
		current += 1
		arbitrarytext()
		return True
	return False

def responsecode(code):
	global state
	global current
	global input
	global inputp
	#print(response[:3])
	if (response[:3] == code):
		current = 3
		inputp = input
		input = response
		if whitespace():
			if arbitrarytext():
				if CRLF():
					input = inputp
					current = 0
					return True
	current = 0
	input = inputp
	return False

def getresponse(code):
	global response
	global file
	global soc
	global responsearray
	#print(soc.getsockname())
	if len(responsearray) == 0:
		temp = soc.recv(2048).decode()
		responsearray = temp.split('\n')
		for i in range(len(responsearray)):
			responsearray[i] += '\n'
		responsearray.pop(len(responsearray)-1)
	#response = soc.recv(2048).decode()
	#print(f'ARRAY: {responsearray}')
	response = responsearray[0]
	responsearray.pop(0)
	#print(f'EXP {code}, RES {response}')
	if not responsecode(code):
		breakread()

def char():
	global input
	global current
	if not(special() or SP() or CRLF()):
		return (ord(input[current]) < 128)
	return False

def digit():
	global input
	global current
	ascii = ord(input[current])
	return (ascii >= 48 and ascii <= 57)

def letter():
	global input
	global current
	ascii = ord(input[current])
	return (ascii >= 65 and ascii <= 90) or (ascii >= 97 and ascii <= 122)

def letdig():
	global input
	global current
	return (letter() or digit())

def letdigstr():
	global input
	global current
	if letdig():
		current += 1
		letdigstr()
		return True
	return False

def element():
	global input
	global current
	if letter():
		current += 1
		letdigstr()
		return True
	return False

def domain():
	global input
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
	global input
	if char():
		current += 1
		string()
		return True
	return False

def mailbox():
	global current
	global input
	if string():
		if input[current] == '@':
			current += 1
			if domain():
				return True
	#print(current)
	return False

def validfrom():
	global current
	global input
	if mailbox():
		if CRLF():
			current = 0
			return True
	current = 0
	return False

def validto():
	global input
	global current
	global rcptstart
	global rcpts
	if mailbox():
		if input[current] == ',':
			#print(input[rcptstart:current])
			rcpts.append(input[rcptstart:current])
			current += 1
			if nullspace():
				rcptstart = current
				if validto():
					current = 0
					return True
		else:
			rcpts.append(input[rcptstart:current])
			current = 0
			return True
	current = 0
	rcptstart = 0
	rcpts = []
	return False

#file = open(sys.argv[1], 'r')
#data = soc.recv(1024)
msg = ''
output = ''
inputstate = 0
input = True
sending = False
try:
	while(input):
		if inputstate == 0:
			print('From:')
			input = sys.stdin.readline()
			if validfrom():
				inputstate = 1
				fromline = input
				#fromline = 'bana@ag.a.\n'
				msg += (f'From: <{fromline[:-1]}>\n')
			else:
				print('Bad from grammar.')
		elif inputstate == 1:
			print('To:')
			input = sys.stdin.readline()
			if validto():
				#print(rcpts, len(rcpts))
				inputstate = 2
				#toline = input
				#toline = 'bana@ag.a.\n'
				msg += 'To: '
				for i in range(len(rcpts)):
					msg += (f'<{rcpts[i]}>')
					if i < len(rcpts)-1:
						msg += ', '
				msg += '\n'
			else:
				print('Bad to grammar.')
		elif inputstate == 2:
			print('Subject:')
			subjectline = sys.stdin.readline()
			inputstate = 3
			msg += (f'Subject: {subjectline}\n')
		elif inputstate == 3:
			print('Message:')
			messageread = True
			while(messageread):
				msgline = sys.stdin.readline()
				if len(msgline) == 2 and msgline[0] == '.' and ord(msgline[1]) == 10:
					messageread = False
					input = False
				else:
					msg += f'{msgline}'
except BaseException as error:
	print(error)
	sys.exit()

#print(f'|{msg}|')
try:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
except:
	print('Invalid number of parameters given, 2 expected (HOST and PORT)')
	sys.exit()

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#soc.settimeout(10)
try:
	soc.connect((HOST, PORT))
except BaseException as error:
	print(error)
	sys.exit()
#print(soc.recv(1024).decode())

getresponse('220')
if(soc):
	state = -1
	sending = True
	#print("Just a print, handshake recicved, yippee!")
try:
	while(sending):
		#print(state)
		#Sending HELO
		if state == -1:
			#print(f'HELO {socket.gethostname()}')
			soc.sendall(f'HELO {socket.gethostname()}\n'.encode())
			getresponse('250')
			state = 0
		#Reading From:
		elif state == 0:
			#print(f'MAIL FROM: <{fromline[:-1]}>')
			output = f'MAIL FROM: <{fromline[:-1]}>\n'
			for i in range(len(rcpts)):
				output += f'RCPT TO: <{rcpts[i]}>\n'
			output += f'DATA\n{msg}.\n'
			soc.sendall(output.encode())
			#soc.sendall(f'MAIL FROM: <{fromline[:-1]}>\n'.encode())
			getresponse('250')
			state = 1
		#Reading To:
		elif state == 1:
			for i in range(len(rcpts)):
				#print('iii')
				#print(f'RCPT TO: <{rcpts[i]}>')
				#soc.sendall(f'RCPT TO: <{rcpts[i]}>\n'.encode())
				getresponse('250')
			state = 2
		#Reading Subject:
		elif state == 2:
			#print('DATA')
			#soc.sendall('DATA\n'.encode())
			#print(soc.recv(2048).decode())
			getresponse('354')
			state = 3
		elif state == 3:
			#print(msg)
			#soc.sendall((f'{msg}').encode())
			#print('.')
			#soc.sendall('.\n'.encode())
			getresponse('250')
			#print('QUIT')
			soc.sendall('QUIT\n'.encode())
			getresponse('221')
			sending = False
except BaseException as error:
	print(error)
	soc.close()
	sys.exit()
#print(soc)
soc.close()
