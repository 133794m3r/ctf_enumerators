# CTF enumerators
Lots of different enumrators that I've written that'll help simplify things for people.
Includes the following services/abilities.

## Mongodb Password/Username guesser in optimal time
This works only through a NoSQL injection that utilizes the REGEX operator inside of MongoDB. This lets us write a regex expression that gets us every possible character that any username or password contains. Then we utilize this information to build the username and password lists. It does this in optimal time. The Time is O(n+m^l) where n is the total characterset(printable ascii in this case). m is number of unique characters in the password/username. l is the length of the password/username. It is always faster than trying all possible characters for all positions because unless the length of the username/password is 93 characters(the default characterset). 

If it is 92 charaters long then time will be.
93+(92^92) or 4.661010870363696*10^180
If we tried all possible characters in all possible positions it'd be 1.260176182005854*10^181
Or roughly 1/3rd the amount of operations. This is where knowing some complexity analysis will greatly help you.

The script will also show you the password/username characterset after it gets it, along with the username(s) and password(s) that it is able to utilize.

It utilizes Python, Requests, and Regex Modules.


## I h8 PowerShell
The first powershell script I ever wrote. The obtuse language is the reason for this title. I had tried other scripts wrote by other people but they didn't work on the local machine so that I had to write my own. It is a powershell script to give you all services where you have full control over as the currently logged in user that are also normally run as SYSTEM and also are not currently running. This script will then give you a small list of services to try. It is useful for this type of priviledge escalation.


## Docker Registry Enumerator
This script will download all of the blogs from a docker registries first entry as far as the projects. It will then download each commit/version for you. Followed by extracting all of the tgz files for you into the folder specified. This will then let you search through them for important information such as ssh keys, passwords etc. It will also give you a progress bar while downloading the data in chunks so that you know that it's doing something.

This utility is written in Python and utilizes the Requests library, JSON, and the Tar modules.


## Sam Copy
This powershell script will dump all of the SAM Registry hive that contains the usernames and passwords of all users. This only works if you already an administrator. It's primary purpose is if you don't have metasploit to utilize the meteterpreter utility to dump the password for you. It creates the zip files and then shows the data as a base64 encoded string so that you can copy->paste it back to your own terminal if you don't have any other way to get files off of the machine. All of this is done in pure powershell.

## Natas 18, 25 Solvers
These scripts are only here so that I have them publicly available so that students could have a copy of the script for their ITP-270 course when they were going to write/utilize tools entirely in Python that were related to the cybersecurity field. Natas18 is all about doing a session hijacker. It could have been done in burpsuite but instead I wrote it in Python utilizing Requests, and RegEx.

The natas 25 solver is here to show them how to bypass a directory traversal filter and also how to get the flag by messing with the user agent header field. Showing them how you can bypass security if the person didn't write the site properly.

Languages: PowerShell, BASH, Python
License: AGPLv3
