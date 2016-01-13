#!/usr/bin/env python
from __future__ import print_function 

import sys
import os
import datetime
import getpass
import configparser
import shutil


def run_setup():
	# Reads in the config file .gnip if exists
	config = configparser.ConfigParser()
	config.read('./.gnip')

	# Py2 Compatability for 'input' function
	if hasattr(__builtins__, 'raw_input'):
		input=raw_input

	# Does User want to overwrite?
	try:
		config.add_section('creds')
	except configparser.DuplicateSectionError:
		overwrite = input("File ./.gnip already exists. Overwrite? (Y/N) ")
		if overwrite.lower() not in ['y','yes','','yup','ye','yep','affirmative','yessir','yepums','si','oui','ok']:
			print("Exiting.")
			sys.exit()
		else:
			# Overwritting .gnip
			shutil.move("./.gnip","./.gnip.old")
			config = configparser.ConfigParser()
			config.read('./.gnip')
			config.add_section('creds')

	# Asking for username and password for Gnip
	un = input("Username: ")
	config.set('creds', 'un', un)
	password = ""
	password1 = "not set"

	# Get user password
	while password != password1:
		password = getpass.getpass("Password: ")
		password1 = getpass.getpass("Password again: ")
	config.set('creds', 'pwd', password1)

	# Asking for account name
	config.add_section('endpoint')
	account_name = input("Endpoint URL. Enter your Account Name (eg https://historical.gnip.com/accounts/<account name>/): ")
	config.set('endpoint', 'url', "https://historical.gnip.com/accounts/{}/".format(account_name))
	config.add_section('tmp')
	config.set('tmp','prevUrl', "")

	# Write config to .gnip
	with open("./.gnip","w") as f:
		config.write(f)

	print("Done creating file ./.gnip")
	print("Configuration setup complete.")
	print("\nUpdating path information in get_data_files.bash...")

	currentPath = os.getcwd()
	state = 0

	with open("./get_data_files.bash","wb") as outf:
	    with open("./get_data_files.bash.orig","rb") as inf:
	        for line in inf:
	            newline = line
	            if line.startswith("AUTOPATH="):
	                state = 1
	                newline = "# Auto updated: %s\n# %s"%(datetime.datetime.now(), line)
	            else:
	                if state == 1:
	                    newline = "AUTOPATH=%s\n"%currentPath + line
	                    state = 2
	            outf.write(newline)

	# For Python3 permission has to be in the format Zero Oh ###
	# Seems to work for Python 2.7 too
	os.chmod("./get_data_files.bash", 0o755)

	print("Done.")


if __name__ == '__main__':
	run_setup()
	os.system("chmod og-w .gnip")
