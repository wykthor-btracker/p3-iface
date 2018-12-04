# -*- coding: utf-8 -*-
#imports
import re
import pdb
import hashlib
# pdb.set_trace()
#imports#

#variables#
onlyLetters = re.compile("^[a-zA-Z]*$")
onlyLettersAndWhitespace = re.compile("^[a-zA-Z ]*$")
lettersNumbersAndWhitespace = re.compile("^[\w ]*$")
passwordPattern = re.compile("^[\w\W]*$")
#variables

#classes#
class messageBox:
	def __init__(self,messages = list()):
		self.messages = messages

	def push(self,message):
		self.messages.append(message)

	def peek(self):
		if(self.messages):
			return self.messages[-1]

	def list(self):
		return [(index,self.messages[index]) for index in range(len(self.messages))]


class user:
	def __init__(self,active = False):
		self.attrs = dict()
		self.messageBox = messageBox()
		self.active = active
		self.friends = dict()
		self.requests = dict()
		self.groups = dict()

	def create(self,username,password,name):
		if(not reMatch(str(username),onlyLetters)):
			raise Exception("Invalid username")
		self.username = username
		self.password = hashPass(password)
		self.name = name
		self.active = True
		return(self)

	def delete(self):
		for friend in self.friends:
			friend.friends.pop(self.username)
		for key in self.__dict__.keys():
			self.__dict__[key] = None

	def login(self,password):
		if(self.active):
			if(self.password == hashPass(password)):
				return self
		else:
			raise Exception("Wrong Password")

	def addAttr(self,key,value,conf = False):
		if(reMatch(key,onlyLettersAndWhitespace) and reMatch(value,passwordPattern)):
			if key in self.attrs.keys():
				if(conf):
					self.attrs[key] = value
				else:
					raise Exception("Not Confirmed")
			else:
				self.attrs[key] = value
		else:
			raise Exception("Invalid string")
		return True

	def showAttrs(self):
		return self.attrs

	def addFriend(self,userInst):
		if(userInst.active):
			if(isIn(userInst.requests,self.username)):
				self.friends[userInst.username] = userInst
				userInst.requests.pop(self.username)
				userInst.friends[self.username] = self
			else:
				self.requests[userInst.username] = userInst
		else:
			raise Exception("Inactive User")
		return True

	def sendMessage(self,message):
		if(message["receiver"].active):
			if(checkMessage(message)):
				message["receiver"].messageBox.push(message)
			else:
				raise Exception("Malformed Message")
		else:
			raise Exception("Inactive User")
		return True

class group:
	def __init__(self,name,desc,owner):
		self.owner = owner
		self.name = name
		self.desc = desc
		self.members = dict()

	def addMember(self,userInst):
		if(userInst.active):
			self.members[userInst.username] = userInst
			userInst.groups[self.name] = self
		else:
			raise Exception("Inactive User")

class users:
	def __init__(self):
		self.users = dict()
		self.communities = dict()

	def addCommunity(self,groupInst):
		if(not isIn(self.communities,groupInst.name)):
			self.communities[groupInst.name] = groupInst
		else:
			raise Exception("Community name already in use")

	def addUser(self,userInst):
		if(not isIn(self.users,userInst.username)):
			self.users[userInst.username] = userInst
		else:
			raise Exception("Username already in use.")

	def retrieveUser(self,name = "",login=False):
		if(isIn(self.users,name)):
			return self.users[name]
		matches = {uName: userInst for uName, userInst in self.users.items() if uName in name}
		if(matches and not login):
			return matches
		else:
			return None

	def retrieveCommunity(self,name):
		if(isIn(self.communities,name)):
			return self.communities[name]
		matches = {cName: commInst for cName, userInst in self.communities.items() if cName in name}
		if(matches):
			return matches
		else:
			return None

	def login(self,username,password):
		if(isIn(self.users,username)):
			return attempt(self.users[username].login(password))
		else:
			raise Exception("User does not exist")

#classes

#functions#
def isIn(dicto,key):
	try:
		dicto[key]
	except:
		return False
	return True
def checkMessage(message):
	fields = set(["sender","receiver","body"])
	message = set(message.keys())
	return message.issubset(fields)

def attempt(function,*args):
	if(not callable(function)):
		raise Exception("{} is not a callable object.".format(function))
	try:
		res = function(*args)
		return res
	except Exception as e:
		return e.args[0]

def reMatch(string,pattern):
	return re.search(pattern,string) is not None

def hashPass(password):
	password = str(password)
	if(reMatch(password,passwordPattern)):
		return hashlib.sha512(password.encode("utf-8")).hexdigest()
	else:
		raise Exception("Malformed Password")

def test():
	f = user()
	g = user()
	g.create("name","xablau","john")
	f.create("sname","boo","jane")
	userL = users()
	userL.addUser(f)
	userL.addUser(g)
	g.addFriend(f)
	f.addFriend(g)
	g.sendMessage({"sender":g,"receiver":f,"body":"Oi"})
	assert(g.login("xablau")==g)
	return(g,f,userL)
#functions

#main#
def main(*args, **kwargs):
	return None
#main

if(__name__ == "__main__"):
	main()
