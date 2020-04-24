# CTF enumerators
Lots of different enumrators that I've written that'll help simplify things for people.
Includes the following services/abilities.

## Mongodb Password/Username guesser in optimal time
This works only through a NoSQL injection that utilizes the REGEX operator inside of MongoDB. This lets us write a regex expression that gets us every possible character that any username or password contains. Then we utilize this information to build the username and password lists. It does this in optimal time. The Time is O(n+m^l) where n is the total characterset(printable ascii in this case). m is number of unique characters in the password/username. l is the length of the password/username. It is always faster than trying all possible characters for all positions because unless the length of the username/password is 93 characters(the default characterset). 

If it is 92 charaters long then time will be.
93+(92^92) or 4.661010870363696\*10^180
If we tried all possible characters in all possible positions it'd be 1.260176182005854\*10^181
Or roughly 1/3rd the amount of operations. This is where knowing some complexity analysis will greatly help you.<br />

The script will also show you the password/username characterset after it gets it, along with the username(s) and password(s) that it is able to utilize. You can apply this same approach for any time you're able to utilize regex or a substring operator to get credentials.<br />

It utilizes Python, Requests, and Regex Modules.

[Optimal MongoDB Credential Getter](https://github.com/133794m3r/ctf_utils/blob/master/get_mongodb_creds.py)
<br />

## I h8 PowerShell
The first powershell script I ever wrote. The obtuse language is the reason for this title. I had tried other scripts wrote by other people but they didn't work on the local machine so that I had to write my own. It is a powershell script to give you all services where you have full control over as the currently logged in user that are also normally run as SYSTEM and also are not currently running. This script will then give you a small list of services to try. It is useful for this type of priviledge escalation.

[I h8 PowerShell Service Enumerator](https://github.com/133794m3r/ctf_utils/blob/master/ih8ps_service_injection_enumerator.ps1)
<br />

## Docker Registry Enumerator
This script will download all of the blogs from a docker registries first entry as far as the projects. It will then download each commit/version for you. Followed by extracting all of the tgz files for you into the folder specified. This will then let you search through them for important information such as ssh keys, passwords etc. It will also give you a progress bar while downloading the data in chunks so that you know that it's doing something.

[Docker Registry Enumerator](https://github.com/133794m3r/ctf_utils/blob/master/docker_registry_enumerator.py)

This utility is written in Python and utilizes the Requests library, JSON, and the Tar modules.<br />
<br />

## Redis Insecurity
This script will let you target a vulnerable redis server that has the default configurations and no password set. Simply supply to it the username you want to target, the hostname, and what folder you want to save the ssh key to to hack the thing. Then it'll open up the ssh shell for you and login you leaving you with a shell on the remote machine. It's pure bash and only requires ssh, and redis-cli to run.

[Redis Insecurity](https://github.com/133794m3r/ctf_utils/blob/master/redis_insecurity.sh)
### Usage
./redis_insecurity.sh {username} {host_to_target} {target_directory}
<br />

## Sam Copy

This powershell script will dump all of the SAM Registry hive that contains the usernames and passwords of all users. This only works if you already an administrator. It's primary purpose is if you don't have metasploit to utilize the meteterpreter utility to dump the password for you. It creates the zip files and then shows the data as a base64 encoded string so that you can copy->paste it back to your own terminal if you don't have any other way to get files off of the machine. All of this is done in pure powershell.

[Sam Copy](https://github.com/133794m3r/ctf_utils/blob/master/sam_copy.ps1)
<br />

## Swish Python Reimpelementation
During NCL Team game one of the challenges required you to reverse engineer a program wrote in Swift 1.4. As the code was too old to easily compile that only left trying to decode it's obtuse and strange syntax. The program was also wrote to make it utilize all features of the langauge to make it look even more complex than it was. To help my teammate and other competitors to be able to understand what the original program was trying to do I've rewritten that code in Python. It should be run as Python3 but nothing in it prevents it from running under Python2. It also produces the same exact output as the original program when given the same inputs(based upon control flow analysis of the original program). Given the correct string(the "flag") it will say that the password is correct proving that it works identically to it.

[Swish.py](https://github.com/133794m3r/ctf_utils/blob/master/ncl/swish.py)

I chose Python because how simple the language is. But I may also include a JavaScript version of the same code in the future.
<br />
## Natas 18, 25 Solvers

These scripts are only here so that I have them publicly available so that students could have a copy of the script for their ITP-270 course when they were going to write/utilize tools entirely in Python that were related to the cybersecurity field. Natas18 is all about doing a session hijacker. It could have been done in burpsuite but instead I wrote it in Python utilizing Requests, and RegEx.<br />

The natas 25 solver is here to show them how to bypass a directory traversal filter and also how to get the flag by messing with the user agent header field. Showing them how you can bypass security if the person didn't write the site properly.<br />
[Natas 18 Script](https://github.com/133794m3r/ctf_utils/blob/master/otw/natas18.py)

[Natas 25 Script](https://github.com/133794m3r/ctf_utils/blob/master/otw/natas25.py)
<br />

Languages: PowerShell, BASH, Python

License: AGPLv3
