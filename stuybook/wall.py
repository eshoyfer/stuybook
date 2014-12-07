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

### Reference ### 

# 				<form method="POST" action="wall.py">	
# 					<textarea rows="6" name="wallpost" cols="70" placeholder="Post on their wall!"></textarea>
# 					<input type="hidden" name="acteduser" value="%s">
# 					<input class="button" type="submit" name="submit" value="submit">
# 				</form>

# acting (posting) user from cookie 
# acteduser from acteduser hidden field 
# wallpost from wallpost textarea

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

### End User Identification ###

### Acted User Modification ###

if not redirectionToHome: # This stuff should only happen in an active session.
	acted = qsDict['acteduser']
	try:
		post = qsDict['wallpost']
	except:
		post = ''

	### HTML Exploit Fix ### 
		
	temp = ''
	for character in post:
		if character != '<' and character != '>':
			temp += character
		else:
			temp += ' '
	post = temp

	s = shelve.open('data.db', writeback=True) # Open database with writeback ability - all modifications to objects will be automatically saved
	actedUser = s[acted] # Get the object of the user whose information is being edited
	actedUser.newWallPost(currentuser, post) # Currentuser is the poster; new wall post is written.
	s.close()
	# Writing complete. Redirection can now begin.

### HTML stuff ###

notLoggedInHTML = '''
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

successHTML = '''
<!DOCTYPE html>
<html>
<head>
	<title>stuybook</title>
	<link rel="stylesheet" type="text/css" href="homeredirect.css">
	<link rel="icon" type="image/png" href="favi.png">
	<meta http-equiv="Refresh" content="0; url=profile.py?target=%s">
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
			<div class="success">
				Posted! Redirecting...
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

# The target must be the acteduser. 

### End HTML Stuff ###

### Redirection Process ### 

if redirectionToHome:
	print "Content-Type: text/html"
	print
	print notLoggedInHTML

if not redirectionToHome:
	print "Content-Type: text/html"
	print
	print successHTML % acted

