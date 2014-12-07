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

#############
### Goals ###
#############

### 1. Identify user
### 2. Identify purpose (source)

### Possible users: 
### 1. Yourself
### 2. Someone else 

### The difference: Settings button

### Possible purposes (sources):
### 1. View self (search or home) (GET)
### 2. View other user  (search) (GET)
### 3. Wall Posts (redirections from wall.py) (GET) - No difference; generation is same. Editing is handled by wall.py. 
###    Hidden field -> Acteduser. Cookie -> Actinguser. Textarea -> Post. This is how wall.py will access necessary info and redirect.
###    Page will be accessed by simple query string get so that the search function doesn't have to consist of "form links"

### Universal purpose: 
### Render page with data from userObject;
### Settings button based on who is viewing

#############
# End Goals #
#############

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

### Indentify Target User ####

# Whose page are we viewing? 
# We can find out via query strings, as all requests for profile.py are passed in the URL or by POST

# If user clicked on link to self in navbar: QS will be profile:profile (GET in URL)
# If user was redirected to themselves upon login, QS will be profile:profile (GET in URL)
# If user clicked on link to taget in search: QS will be target:user (POST)

if 'profile' in qsDict.keys(): # If user targeted self
	selfTarget = True
	target = currentuser # Store browsing user's username as target (the one in the cookie)
else:
	selfTarget = False

if 'target' in qsDict.keys(): # If another user is the target
	target = qsDict['target'] # Store it 
	if currentuser == target: # This takes care of what happens if the user finds themselves via search
		selfTarget = True

#######################
### Page Generation ### 
#######################

# Now that we have info about who is browsing (currentuser), 
# whether or not the session is valid, and whose page is being viewed,
# we can generate the profile.py page. 

########################
###### HTML STUFF ######
########################

### Standard Profile ### 

standardHTML = '''
<!DOCTYPE html>
<html>
<head>
	<title>stuybook</title>
	<link rel="stylesheet" type="text/css" href="profile.css">
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
		<div class="pic_wrapper">
			<img src="%s">
			<div class="name">
				%s
			</div>
			<div class="message">
				%s
			</div>
				%s
		</div>
		<div class="wall_cont">
			<div class="wall_post">
				<form method="POST" action="wall.py">	
					<textarea rows="6" name="wallpost" cols="70" placeholder="Post on their wall!"></textarea>
					<input type="hidden" name="acteduser" value="%s">
					<input class="button" type="submit" name="submit" value="submit">
				</form>
			</div>
			<div class="wall">
				%s
			</div>
		</div>

	</div>
</body>
</html>
'''
# Order: (imgurl, name, message, button, acted, wall)
### Wall format:
### Sample User: Sample Content<br><hr><br>Sample User: Sample Content<br><hr><br> 
### Function must be written for conversion from object's variable.

settingsButton = '''
<form class="settings" method="POST" action="settings.py">
	<input class="button" type="submit" name="settings" value="settings">
</form>
'''

### If user is on own page (as determined by boolean) use this in the substitution tuple.
### Otherwise use "". 

### Redirection - Session Not Found HTML ###

# Redirects user to login page because cookie not found / invalid 

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

######################
### END HTML STUFF ###
######################

#######################
### PAGE GENERATION ###
#######################

#print "Content-Type: text/html"
#print

### Pull User Data ###

s = shelve.open('data.db') # Open database; no write-back is necessary for this process. 
targetUser = s[target] # Pull the user object of the target.

### Reference from object definition:

# self.walltext = [] 
# def newWallPost(self, poster, message):
# 	line = [poster, message]
# 	self.walltext.append(line)

### Example walltext list:

# [[poster0, message0], [poster1, message1], [poster2, message2]]

### Wall format:
### Sample User: Sample Content<br><hr><br>Sample User: Sample Content<br><hr><br> 
### Function must be written for conversion from object's variable.

def convertWallToHTML(L): # Takes wall list, returns wall HTML
	output = ""
	separator = "<br><hr><br>"
	for post in L:
		author = post[0]
		message = post[1]
		line = author + ": " + message + separator
		output += line
	return output

# In general, on the site the username is used. Full name stays hidden

image = targetUser.picurl
aboutme = targetUser.aboutme
walltext = convertWallToHTML(targetUser.walltext)
# username variable is called target
# button variable is called settingsButton; should be "" if viewing other user (based on boolean)
# actinguser variable is called currentuser


# redirectionToHome and selfTarget 

# Order: (imgurl, name, message, button, acteduser, wall)

s.close()

if redirectionToHome: # Unsuccessful Session Search
	print "Content-Type: text/html"
	print
	print redirectHTML
else: # Successful Session Found; proceed with profile
	if selfTarget: # Viewing own page
		print "Content-Type: text/html"
		print
		print standardHTML % (image, target, aboutme, settingsButton, target, walltext)
	else: # Viewing someone else's page
		print "Content-Type: text/html"
		print
		print standardHTML % (image, target, aboutme, '', target, walltext) # No settings button

