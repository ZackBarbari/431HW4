#Zack Barbari, zackaxal
#I certify that no unauthorized assistance has been received or given in the completion of this work.

import sys
response = ""
current = 0
state = 0

def SP():
	global current
	if response[current] == "	" or response[current] == " ":
		return True
	return False

def CRLF():
	global current
	ascii = ord(response[current])
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

def breakread():
	global file
	print('QUIT')
	#file.close()
	file = False

def arbitrarytext():
	global current
	#print(current)
	ascii = ord(response[current])
	if ascii >= 20 and ascii <= 127:
		current += 1
		arbitrarytext()
		return True
	return False

def responsecode(code):
	global state
	global current
	#print(response[:3])
	if (response[:3] == code):
		current = 3
		if whitespace():
			if arbitrarytext():
				if CRLF():
					return True
	return False

def getresponse(code):
	global response
	global file
	response = sys.stdin.readline()
	sys.stderr.write(response)
	if not responsecode(code):
		breakread()

def bodyread():
	global fileline
	global file
	global state
	if len(fileline) >= 5 and fileline[0] == 'F' and fileline[1] == 'r' and fileline[2] == 'o' and fileline[3] == 'm' and fileline[4] == ':':
		print('.')
		getresponse('250')
		if file:
			print(f'MAIL FROM: {fileline[6:-1]}')
			getresponse('250')
			state = 1
	else:
		print(fileline[:-1])

file = open(sys.argv[1], 'r')

while(file):
	fileline = file.readline()
	#EOF case
	if fileline == '' and state > 1:
		if state == 2:
			print('DATA')
			getresponse('354')
		if file:
			print('.')
			getresponse('250')
			if file:
				breakread()
		break
	match state:
		#Reading From:
		case 0:
			if len(fileline) >= 5 and fileline[0] == 'F' and fileline[1] == 'r' and fileline[2] == 'o' and fileline[3] == 'm' and fileline[4] == ':':
				print(f'MAIL FROM: {fileline[6:-1]}')
				getresponse('250')
				state = 1
			else:
				breakread()
		#Reading To:
		case 1:
			if len(fileline) >= 3 and fileline[0] == 'T' and fileline[1] == 'o' and fileline[2] == ':':
				print(f'RCPT TO: {fileline[4:-1]}')
				getresponse('250')
				state = 2
			else:
				breakread()
		#Reading To: or input body
		case 2:
			if len(fileline) >= 3 and fileline[0] == 'T' and fileline[1] == 'o' and fileline[2] == ':':
				print(f'RCPT TO: {fileline[4:-1]}')
				getresponse('250')
			else:
				print('DATA')
				getresponse('354')
				state = 3
				if file:
					bodyread()
		case 3:
			bodyread()
