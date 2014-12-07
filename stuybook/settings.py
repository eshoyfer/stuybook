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
#    a) The cookie exists. The user is logged in.   ----> Normal page
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

### HTML stuff ### 

settingsHTML = '''
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
		<span style="font-size: 2em">Settings</span><br><hr><br>
		<strong>Username</strong>: %s <br><hr><br>
		<strong>Password</strong>: 
			<form method="POST" action="settings.py">
				<input type="password" name="passwordinput"> <br><br>
				<input class="button" type="submit" name="password" value="submit"> <br><br><hr><br>
			</form>
		<strong>About me</strong>:<br> 
			<form method="POST" action="settings.py">
				<textarea rows="6" name="aboutmeinput" cols="70" value="%s"></textarea> <br>
				<input class="button" type="submit" name="aboutme" value="submit"> <br><br><hr><br> 
			</form>
		<strong>Picture url</strong>: 
			<form method="POST" action="settings.py">
				<input type="text" name="picurlinput" value="%s"> <br><br>
				<input class="button" type="submit" name="picurl" value="submit"> <br><br><hr><br>
			</form>

	</div> 
</body>
</html>
'''
# Tuple format: (username, aboutme, picurl)

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
### End HTML stuff ### 

### Editing User Object ### 

# Upon editing something in settings.py, the page redirects to itself. 
# This means that every time it is opened, it must check if any editing operations were requested
# and perform them upon the file object. 
# Only after doing this can it serve the HTML (the HTML will reflect any modifications made prior to generation).

if not redirectionToHome: # Object modification should only be done if we're in a successful session.
	# Accessing user object
	s = shelve.open('data.db', writeback=True) # Open database with writeback ability - all modifications to objects will be automatically saved
	currentUser = s[currentuser] # Get the object of the user whose information is being edited
	# Possible things that can be modified: password, aboutme, picurl
	editingOperationRequested = False
	if 'password' in qsDict.keys() or 'aboutme' in qsDict.keys() or 'picurl' in qsDict.keys(): 
		editingOperationRequested = True
	if editingOperationRequested: # Input fields associated - Password: passwordinput ; About me: aboutmeinput ; Picture: picurlinput
		if 'password' in qsDict.keys(): # If the password was requested for modification
			try:
				passwordinput = qsDict['passwordinput']
			except:
				passwordinput = ''
			currentUser.changePass(passwordinput)
		if 'aboutme' in qsDict.keys(): # If the about me field was requested for modification
			try:
				aboutmeinput = qsDict['aboutmeinput']
			except:
				aboutmeinput = ''
			currentUser.changeAboutMe(aboutmeinput)
		if 'picurl' in qsDict.keys():
			try:
				picurlinput = qsDict['picurlinput'] # If the pic url field was requested for modification
			except:
				picurlinput = ''
			currentUser.changePicUrl(picurlinput)
		# At this point the requested modifications have been performed
	s.close() # Database closed; modifications to objects saved. Modification complete. 

### End Editing User Object ###

### Start HTML Output ### 

# It will either redirect to the homepage (if session failed) or generate the settings page. 

if redirectionToHome: # Unsuccessful Session; redirect home
	print "Content-Type: text/html"
	print
	print redirectHTML

if not redirectionToHome: # Successful Session; generate settings
	# Tuple format: (username, aboutme, picurl)
	s = shelve.open('data.db') # No writeback needed; we're just pulling info.
	currentUser = s[currentuser]
	# username is currentuser
	aboutMeRestored = currentUser.aboutme
	pictureUrlRestored = currentUser.picurl
	s.close()
	print "Content-Type: text/html"
	print
	print settingsHTML % (currentuser, aboutMeRestored, pictureUrlRestored)


