#Zack Barbari, zackaxal
#I certify that no unauthorized assistance has been received or given in the completion of this work.

import sys
input = ""
global current
current = 0
state = 0
sender = ""
recipients = []
email = ""
pathstart = -1
pathend = -1


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
	if string():
		if input[current] == '@':
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
	if input[0] == "M" and input[1] == "A" and input[2] == "I" and input[3] == "L":
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
	if input[0] == "R" and input[1] == "C" and input[2] == "P" and input[3] == "T":
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
	if input[0] == "D" and input[1] == "A" and input[2] == "T" and input[3] == "A":
		current = 4
		if nullspace():
			if CRLF():
				current = 0
				return True
	current = 0
	return False

def commandcheck(key):
	global current
	match key:
		case 0:
			if mailname():
				current = 0
				return True
			current = 0
			return False
		case 1:
			if rcptname():
				current = 0
				return True
			current = 0
			return False
		case 2:
			if datacmd():
				current = 0
				return True
			current = 0
			return False
def resetemail():
	global current
	global state
	global sender
	global recipients
	global email
	state = 0
	current = 0
	sender = ""
	recipients = []
	email = ""



for line in sys.stdin:
	input = line
	print(f'{input}', end="")
	match state:
		#Only accepting MAIL FROM:
		case 0:
			if mailfromcmd():
				print('250 OK')
				state = 1
				sender = input[pathstart:pathend]
			else:
				if commandcheck(1) or commandcheck(2):
					print('503 Bad sequence of commands')
				elif commandcheck(0):
					print('501 Syntax error in parameters or arguments')
				else:
					print('500 Syntax error: command unrecognized')
				resetemail()
		#Only accepting RCPT TO:
		case 1:
			if rcpttocmd():
				print('250 OK')
				state = 2
				recipients.append(input[pathstart:pathend])
			else:
				if commandcheck(0) or commandcheck(2):
					print('503 Bad sequence of commands')
				elif commandcheck(1):
					print('501 Syntax error in parameters or arguments')
				else:
					print('500 Syntax error: command unrecognized')
				resetemail()
		#Accepting both RCPT TO: and DATA
		case 2:
			if rcpttocmd():
				print('250 OK')
				recipients.append(input[pathstart:pathend])
			elif datacmd():
				print('354 Start mail input; end with <CRLF>.<CRLF>')
				state = 3
			else:
				if commandcheck(0):
					print('503 Bad sequence of commands')
				elif commandcheck(1):
					print('501 Syntax error in parameters or arguments')
				else:
					print('500 Syntax error: command unrecognized')
				resetemail()
		#Email body input
		case 3:
			if input[0] == "." and ord(input[1]) == 10:
				print('250 OK')
				for i in range(len(recipients)):
					#print(recipients[i][1:-1])
					file = open(f'HW2/forward/{recipients[i][1:-1]}', 'a')
					file.write(f'From: {sender}\n')
					for e in range(len(recipients)):
						file.write(f'To: {recipients[e]}\n')
					file.write(f'{email}')
				resetemail()
			else:
				email += input
