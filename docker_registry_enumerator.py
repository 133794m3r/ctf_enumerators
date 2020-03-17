#!/bin/env python3
"""
Docker Registry Enumerator.
By Macarthur Inbody 2019-
Licensed AGPLv3 or Later 
Will get you all of the blobs from the first imgae that it sees in the registry.
"""
#so that I can get the time of everything.
import time
#my lovely banner.
#so i can get stdout, and stderr.
import sys
#modern argument parser library.
import argparse
import os
import requests
print('''

\033[1;97m###################################
#\033[22m \033[1;92mMacarthur Presents\033[97;1m	          #
#\033[22m \033[1;31mDocker Registry Enumerator \033[97;1m	  #
#\033[22m Get them \033[32;1mblobs\033[32;1m quick and fast. \033[97;1m #
###################################\033[0m
''')


def mkdir_p(path):
	import errno
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

def extract_all(filename,extraction_path='.'):
	mkdir_p(extraction_path)
	os.system(f"tar --exclude='dev' -zxf {filename} -C {extraction_path}")
		
def get_blobs(json_obj):
	return [ item['blobSum'] for item in json_obj['fsLayers'] ]
def enumerate_docker(username='admin',password='admin',directory='/tmp/docker_dump',url=None):
	"""
	Enumerate Docker Registry Service
	This will only do the first image that it sees for right now.
	arguments:
		url {string} This is the base url we're going to hit. It doesn't need the /v2 or /v1 at the end.
		directory {string} where we're going to store the blobs.
		username {string} the username to use.
		password {string} the passwoerd we're going to use.
	"""
	mkdir_p(directory)
	catalog=[]
	auth=requests.auth.HTTPBasicAuth(username,password)	
	url=url+'/v2'
	with requests.get(url+'/_catalog',auth=auth) as response:
		catalog=response.json()
	
	print(catalog)
	with requests.get(url+'/'+catalog['repositories'][0]+'/manifests/latest',auth=auth) as response:
		blobs=get_blobs(response.json())
		
	#so that I can parse the JSON strings into objects.
	import json


	size=1024*1024
	current_ten_perc=0
	for blob in blobs:
		print("Currently downloading {}".format(blob))
		current_total=0
		auth=requests.auth.HTTPBasicAuth(username,password)
		request=requests.get(base_url+blob, auth=auth, allow_redirects=True,stream=True)
		file_size=int(request.headers.get('content-length'))
		ten_perc=file_size/10.0
		perc=0
		current_ten_perc=0
		at_boundary=0;
		current_file=f"{directory}/{blob}.tgz".replace(":","-")
		print("It is is sized {:,}KiB".format(round(file_size/1024.0,2)))
		with open(current_file,'wb') as blob_file:
			for chunk in request.iter_content(chunk_size=size):
				if chunk:
					blob_file.write(chunk)
					current_total+=size
					current_ten_perc+=size
					if current_total > file_size:
						perc=1
					elif current_ten_perc >= ten_perc:
						current_ten_perc=0
						perc=round((current_total/(ten_perc)),2)
						print("Downloaded: {:,} MiB which is {}%".format(round(current_total/(1024*1024),2),round(perc*10,2)))
		print(f"We are now extracting {blob}.tgz")
		extract_all(current_file,current_file[0:-4])
		
		
def main():
	import argparse
	parser=argparse.ArgumentParser(description='''How to use the Docker Registry Enumerator.\nThis utilitity will download all blobs from the first entry of a docker registry.\n
Then it will get you the blobs, extract them to the chosen directory and finally leave you with the folders to sift through.\nYou need to pass the username,password, and url of the site you're targetting, and also the filename of the folder where you want the files to go. Otherwise defaults will be utilized.''')
	username="admin"
	password="admin"
	directory="/tmp/docker_dump"
	url=None
	parser.add_argument('-u',
		metavar='{USERNAME}',
		type=str,
		help="The username we're going to utilize. Defaults to admin.",
		required=False)
	parser.add_argument('-p',
		metavar='{PASSWORD}',
		type=str,
		help='The password to use. Defaults to admin.',
		required=False)
	parser.add_argument('-o',
	    metavar='{OUTPUT_DIRECTORY}',
	    type=str,
	    help="The full path to the output directory. If you don't include a / it'll put it in your current directory.",
	    required=False)
	parser.add_argument('-d',
		metavar='{URL_TO_TARGET}',
		type=str,
		help='The url to target. It needs to be the base url. Do not include anything outside of {REGISTRY|WHATEVER}.URL. The rest will be handled by the script.',
		required=False)

	if len(sys.argv) == 1:
		parser.print_help(sys.stdout)
		sys.exit(0)
	else:
		args=parser.parse_args()
		print(args)
		if args.u is not None:
			username=args.u
		if args.p is not None:
			password=args.p
		if args.d is not None:
			url=args.d
		if args.o is not None:
			directory=args.o
		"""
		elif args.h:
			out_len=len(input_list)
			unknown=input_list[out_len-1]
			parser.print_help(sys.stdout)
		"""
		enumerate_docker(username='admin',password='admin',directory=directory,url=url)
		#enumerate_docker(username=username,password=password,url=url,directory=directory)

if __name__ == "__main__":
	main()
