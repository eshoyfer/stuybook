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

### User Identification ### 

# This is done via cookies.
# Possibilities: 
#    a) The cookie exists. The user is logged in.   ----> Edit acteduser object and redirect to profile.py (GET version)
#    b) The cookie does not exist. The user is not logged in. ----> Redirect to home.html

cookie = Cookie.SimpleCookie()
try:
	cookie_string = os.environ.get('HTTP_COOKIE') # retrive cookie as string
	if not cookie_string: # If no cookie found, they are not logged in. Redirect to homepage.
		redirectionToHome = True
	cookie.load(cookie_string) # turn back into cookie object 
	redirectionToHome = False # If the cookie object was found and loaded successfully then there is no need to redirect to home. Successful login.
except:
	redirectionToHome = True # If any of the above raised an excepetion then the user is not successfully logged in. Redirect to homepage.

if not redirectionToHome: # Now we identify who the user is
	currentuser = cookie['currentuser'].value

### End User Identification

### HTML Stuff ###

searchoutputHTML = '''
<!DOCTYPE html>
<html>
<head>
	<title>stuybook</title>
	<link rel="stylesheet" type="text/css" href="settings.css">
	<link rel="icon" type="image/png" href="favi.png">
</head>
<body>
	<div class="nav_cont">
		<div class="nav_items">
			<ul>
				<li style="font-family:HelveticaNeue; color:white;">stuybook</li>
				<li>
					<form method="POST" action="search.py">
						<input style="height: 30px; width: 300px;" type="text" name="search" placeholder="Search users...">
					</form>
				</li>
				<li>
					<form method="POST" action="profile.py">
						<input class="button" type="submit" name="profile" value="profile">
					</form>
				</li>
				<li>
					<form method="POST" action="logout.py">
						<input class="button" type="submit" name="logout" value="logout">
					</form>
				</li>
			</ul>
		</div>
	</div>
	<div class="main_cont">
		<span style="font-size: 2em">Search (case-sensitive)</span><br><hr><br>
		%s
	</div>
</body>
</html>
'''

redirectHTML = '''
<!DOCTYPE html>
<html>
<head>
	<title>stuybook</title>
	<link rel="stylesheet" type="text/css" href="homeredirect.css">
	<link rel="icon" type="image/png" href="favi.png">
	<meta http-equiv="Refresh" content="5; url=login.html">
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
			<div class="failure">
				You're not logged in! Redirecting...
			</div>
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
</html>
'''

### End HTML Stuff ### 

### Reference ###

# <form method="POST" action="search.py">
#	<input style="height: 30px; width: 300px;" type="text" name="search" placeholder="Search users...">
# </form>

# <a href="profile.py?target=user">User</a><br><hr><br>
# <a href="profile.py?target=user">User</a><br><hr><br>
# <a href="profile.py?target=user">User</a><br><hr><br>
# <a href="profile.py?target=user">User</a><br><hr><br>

### End Reference ###

### HTML Generating Search Function

def searchHTML(search):
	output = ""
	HTMLline = '<a href="profile.py?target=%s">%s</a><br><hr><br>'
	for user in userList:
		if search in user: # if content of search in content of username string
			thisline = (HTMLline % (user, user)) + '\n'
			output += thisline
	return output

if redirectionToHome: # Invalid Session
	print "Content-Type: text/html"
	print
	print redirectHTML

if not redirectionToHome: # Valid Session
	### Start Search Function ###
	### Obtain Userlist
	usersStream = open('users.txt', 'r')
	users = usersStream.read() # Format: "user1,user2,user3,"
	usersStream.close()
	userList = users.split(',') # Format: [user1, user2, user3, ""]
	userList = userList[:-1] # Format: [user1, user2, user3] - The final userList.
	try:
		searchQuery = qsDict['search']
	except:
		searchQuery = ""
	searchProduct = searchHTML(searchQuery)
	print "Content-Type: text/html"
	print
	print searchoutputHTML % searchProduct