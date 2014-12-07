#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()

import Cookie
import os

import hashlib
salt = "71D7BB50"
hash = lambda passw: hashlib.md5(passw + salt).hexdigest()

class User:
	def __init__(self, username, fullname, password):
		self.username = username
		self.name = fullname
		with open('users.txt', 'a') as fileStream:
			addition = username + ','
			fileStream.write(addition)
		self.hashedpass = hash(password)
		self.picurl = 'http://i.imgur.com/TLz5NnO.jpg'
		self.aboutme = 'This user has not set a description yet!'
		self.walltext = [['stuybook','Thanks for registering!']] # Each item in the list is a list in the form [poster, message]
	def changePass(self, newpass):
		self.hashedpass = hash(newpass)
	def changePicUrl(self, newurl):
		self.picurl = newurl
	def changeAboutMe(self, newabout):
		self.aboutme = newabout
	def newWallPost(self, poster, message):
		line = [poster, message]
		self.walltext.append(line)

import shelve

form = cgi.FieldStorage()
keys = form.keys()
qsDict = {}
for key in keys:
	value = form.getvalue(key)
	qsDict[key] = value

### End Library Stuff ### 

### ErrorMessage Initiation ###
ErrorMessage = ""

### Obtaining Data ###

try:
	username = qsDict['user']
	password = qsDict['pass']
except:
	ErrorMessage = "Error: You left a field blank!"

if 'user' not in qsDict.keys():
	username = ''
if 'pass' not in qsDict.keys():
	password = ''

### Userlist ###

usersStream = open('users.txt', 'r')
users = usersStream.read() # Format: "user1,user2,user3,"
usersStream.close()
userList = users.split(',') # Format: [user1, user2, user3, ""]
userList = userList[:-1] # Format: [user1, user2, user3] - The final userList.

### Login Process ###

### Logging in stores a cookie on client-side containing username. 

if username not in userList: # Check if valid username
	ErrorMessage = "Invalid username." # Invalid
else: # Valid
	s = shelve.open('data.db') # Open database; no write-back is necessary for this process.
	userObject = s[username] # Retreive the user object that corresponds to the username entered
	s.close()
	if hash(password) == userObject.hashedpass: # Is the password correct? This branch: yes
		### Cookie Creation ###

		### Cookie purpose: to store username of logged in user. ###
		cookie = Cookie.SimpleCookie() # New SimpleCookie object
		cookie['currentuser'] = username # Planting cookie: print cookie before Content-type
		ErrorMessage = ""
	else: # The password was incorrect
		ErrorMessage = "Incorrect password."

### Start HTML stuff for Error ###

errorHTMLheader = '''
<!DOCTYPE html>
<html>
<head>
	<title>stuybook</title>
	<link rel="stylesheet" type="text/css" href="homeredirect.css">
	<link rel="icon" type="image/png" href="favi.png">
	<meta http-equiv="Refresh" content="5; url=home.html">
</head>
<body>
	<div class="bg">
		<script>
			var random = Math.floor(Math.random() * 3);
			var pics = new Array();
			pics[0] = 'http://i.imgur.com/U1K0HSD.jpg';
			pics[1] = 'http://i.imgur.com/rsAyUzE.jpg';
			pics[2] = 'http://i.imgur.com/XTHspTI.jpg';
			var randompic = pics[random]
			var image = '<img src="' + randompic + '">';
			document.write(image);
		</script>
	</div>
	<div class="logo">
		<img src="logo_noshad_trans.png">
	</div>
	<div class="register">
'''
errorHTMLcloser = '''
	</div>

	<span class="message">
		a shoyfer, mcconnell, and szul ent. collab 
	</span>
	<div class="login">
		<a href="login.html">
			<div class="button">
				login
			</div>
		</a>
	</div>
</body>
'''

def failureWrapper(message):
	opener = '<div class="failure">'
	closer = '</div>'
	return opener + message + closer


### End HTML stuff for Error ### 

### Start HTML stuff for Success ###

successHTMLheader = '''
<!DOCTYPE html>
<html>
<head>
	<title>stuybook</title>
	<link rel="stylesheet" type="text/css" href="homeredirect.css">
	<link rel="icon" type="image/png" href="favi.png">
	<meta http-equiv="Refresh" content="1; url=profile.py?profile=profile">
</head>
<body>
	<div class="bg">
		<script>
			var random = Math.floor(Math.random() * 3);
			var pics = new Array();
			pics[0] = 'http://i.imgur.com/U1K0HSD.jpg';
			pics[1] = 'http://i.imgur.com/rsAyUzE.jpg';
			pics[2] = 'http://i.imgur.com/XTHspTI.jpg';
			var randompic = pics[random]
			var image = '<img src="' + randompic + '">';
			document.write(image);
		</script>
	</div>
	<div class="logo">
		<img src="logo_noshad_trans.png">
	</div>
	<div class="register">
'''
successHTMLcloser = '''
	</div>

	<span class="message">
		a shoyfer, mcconnell, and szul ent. collab 
	</span>
	<div class="login">
		<a href="login.html">
			<div class="button">
				login
			</div>
		</a>
	</div>
</body>
'''

def successWrapper(message):
	opener = '<div class="success">'
	closer = '</div>'
	return opener + message + closer

### End HTML stuff for Success ###

if ErrorMessage: # If there was an error
	print "Content-Type: text/html"
	print
	errorHTMLbody = failureWrapper(ErrorMessage)
	print errorHTMLheader + errorHTMLbody + errorHTMLcloser

if not ErrorMessage: # No error; successful login
	print cookie.output() # Plant cookie on client's machine
	print "Content-Type: text/html"
	print
	successHTMLbody = successWrapper("Login successful! Redirecting...")
	print successHTMLheader + successHTMLbody + successHTMLcloser









