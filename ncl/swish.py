#!/usr/bin/env python3

"""
Swish Python Re-Implementation
By Macarthur Inbody <admin-contact@transcendental.us>
AGPLv3 or later.
"""
d = [83,74,89,42,77,60,67,72,45,58,62,59,69]
i:int = 0
print("Hello, do you have a password for me?")
i_str: str = ""
i_str = input()

def check(i_str:str,i:int) -> bool:
	if not (i<=8):
		return check5(i_str,i)

	if not (i % 2 == 0):
		return check2(i_str,i)

	return check10(i_str,i)

def check2(i_str:str,i:int) -> bool:
	if i_str[0:1] == chr(d[i]+i):
		#have to do this b/c otherwise the variable won't be incremented right.
		i+=1  
		return check(i_str[1:],i)
	else:
		return False

def check10(i_str:str,i:int) -> bool:
	if i_str[0:1] == chr(d[i]):
		#have to do this b/c otherwise the variable won't be incremented right.	
		i+=1
		return check(i_str[1:],i)
	else:
		return False

def check5(i_str:str,i:int) -> bool:
	if i_str[0:1] == chr(d[i] -i):
		if i == 12:
			return True
		else:
			#have to do this b/c otherwise the variable won't be incremented right.
			i+=1				  
			return check5(i_str[1:],i)
	else:
		return False
	
if check(i_str,0):
	print("Awesome! You got the password!")
else:
	print("Nope, that's not the right password :(")
