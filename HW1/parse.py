#Zack Barbari, zackaxal
#I certify that no unauthorized assistance has been received or given in the completion of this work.

import sys
input = ""
global current
current = 0
error_place = ""


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
	global error_place
	global current
	ascii = ord(input[current])
	if ascii == 10:
		return True
	if error_place == "":
		error_place = "CRLF"
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
	global error_place
	if letter():
		current += 1
		letdigstr()
		return True
	if error_place == "":
		error_place = "element"
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
	global error_place
	if char():
		current += 1
		string()
		error_place = ""
		return True
	if error_place == "":
		error_place = "string"
	return False


def mailbox():
	global current
	global error_place
	if string():
		if input[current] == '@':
			current += 1
			error_place = ""
			if domain():
				return True
	if error_place == "":
		error_place = "mailbox"
	return False


def path():
	global current
	global error_place
	if input[current] == '<':
		current += 1
		if mailbox():
			if input[current] == '>':
				current += 1
				error_place = ""
				return True
	if error_place == "":
		error_place = "path"
	return False


def whitespace():
	global error_place
	global current
	if SP():
		current += 1
		whitespace()
		error_place = ""
		return True
	if error_place == "":
		error_place = "whitespace"
	return False


def nullspace():
	global error_place
	whitespace()
	error_place = ""
	return True


def mailfromcmd(): 
	global current
	global error_place
	if input[0] == "M" and input[1] == "A" and input[2] == "I" and input[3] == "L":
		current = 4
		if whitespace():
			if input[current] == "F" and input[current+1] == "R" and input[current+2] == "O" and input[current+3] == "M" and input[current+4] == ":":
				current +=5
				if nullspace():
					if path():
						if nullspace():
							if CRLF():
								return True
	if error_place == "":
		error_place = "mail-from-cmd"
	return False

for line in sys.stdin:
	input = line
	print(f'{input}', end="")
	if mailfromcmd():
		print('Sender ok')
	else:
		print(f'ERROR -- {error_place}')
	error_place = ""
