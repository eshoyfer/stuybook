import shelve
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


elvin = User("Elvins", "Elvin Shoyfer", "password")

s = shelve.open('data.db', writeback = True)
user = s["Elvins"]
print user.picurl
user.changePicUrl('www.google.com')
print user.picurl
s.close()

s = shelve.open('data.db', writeback = True)
newuser = s["Elvins"]
print user.picurl
s.close()

# When you use writeback mode it will automatically save
# changes in the current memory
# the changes that you did to an objects stuff itself is autosaved
# They will also be applied in the memory that youre using at the moment


