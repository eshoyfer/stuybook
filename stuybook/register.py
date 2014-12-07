#!/usr/bin/python
print "Content-Type: text/html"
print

import cgi
import cgitb
cgitb.enable()

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

def isValidUsername(username):
	invalidchars = '.,?:!";{}[] ' # some punctuation and spaces
	for char in invalidchars:
		if char in username:
			return False
	if username == '':
		return False
	return True


# Later on, the weak truth value of the ErrorMessage and SuccessMessage strings 
# will be used to determine the course of action for the script to take.
ErrorMessage = ""
SuccessMessage = ""
BlankField = False

### Obtaining Data ###
try: 
	realname = qsDict['name']
	username = qsDict['user']
	password = qsDict['pass']
except:
	ErrorMessage = "Error: You left a field blank!"
	BlankField = True

if 'name' not in qsDict.keys():
	realname = ''
	BlankField = True

if 'user' not in qsDict.keys():
	username = ''

if 'pass' not in qsDict.keys():
	password = ''

### Registration Process ### 

if not BlankField:
	if isValidUsername(username):			# Check 1: Valid Username? 
		usersStream = open('users.txt', 'r')
		users = usersStream.read() # Format: "user1,user2,user3,"
		usersStream.close()
		userList = users.split(',') # Format: [user1, user2, user3, ""]
		userList = userList[:-1] # Format: [user1, user2, user3] - The final userList.
		if username in userList:
			ErrorMessage = "Error: Username taken!"
		else:
			userObject = User(username, realname, password) ## See the __init__ function of this object: auto adds user to users.txt, sets default settings
			s = shelve.open('data.db', writeback=True)
			s[username] = userObject ## Write the new user object to the database dictionary. The key to this object is the username string.
			s.close()
			SuccessMessage = "You have successfully registered!" ## At this point the Registration process is complete, with the user object stored.

	else:
		ErrorMessage = "Error: Invalid Username! No spaces or punctuation."
else:
	ErrorMessage = "Error: You left a field blank!"

### Next Steps ###

HTMLheader = '''
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
HTMLcloser = '''
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

def failureWrapper(message):
	opener = '<div class="failure">'
	closer = '</div>'
	return opener + message + closer

if SuccessMessage:
	HTMLbody = successWrapper(SuccessMessage)
	print HTMLheader + HTMLbody + HTMLcloser
else:
	HTMLbody = failureWrapper(ErrorMessage)
	print HTMLheader + HTMLbody + HTMLcloser


