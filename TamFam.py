from websocket import create_connection as cc
import json
import time
import os
import datetime
import requests

class TamFam:
	ws = None
	seq = 1
	session = None
	
	def __init__(self, session):
		self.session = session
		self.ws = cc('wss://ws.tamtam.chat/websocket')
		self.ws.send(json.dumps({"ver":10,"cmd":0,"seq":self.seq,"opcode":6,"payload":{"userAgent":{"deviceType":"WEB","appVersion":"2.0.17","osVersion":"Windows","locale":"ru","deviceName":"Chrome","screen":"1024x768 2.0x","headerUserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3810.0 Safari/537.36"}}}))
		self.seq += 1
		self.ws.send(json.dumps({"ver":10,"cmd":0,"seq":self.seq,"opcode":1,"payload":{"interactive":True}}))
		self.seq += 1
		self.ws.recv()
		self.ws.recv()
	
	def apiRequest(self, opcode, payload):
		data = {"ver": 10, "cmd": 0, "seq": self.seq, "opcode": opcode, "payload": payload}
		self.ws.send(json.dumps(data))
		self.seq += 1
		return json.loads(self.ws.recv())
	
	def phoneLogin(self, phone):
		login = self.apiRequest(17, {"phone": phone})
		return login['payload']['verifyToken']
	
	def completePhoneLogin(self, token, code):
		code = self.apiRequest(18, {"authTokenType": "PHONE", "token": token, "verifyCode": code})
		if not 'AUTH' in code['payload']['tokenTypes']:
			token = code['payload']['tokenTypes']['NEW']
			reg = self.apiRequest(23, {"token": token,"tokenType": "NEW","deviceType": "WEB","deviceId": "WEB:1","name": "New User"})
			token = reg['payload']['token']
		else:
			token = code['payload']['tokenTypes']['AUTH']
			auth = self.apiRequest(23, {"deviceId": "WEB:1", "deviceType": "WEB", "token": token, "tokenType": "AUTH"})
			token = auth['payload']['token']
		login = self.apiRequest(19, {"token": token, "userAgent":{"deviceType":"WEB","appVersion":"2.0.17","osVersion":"Windows","locale":"ru","deviceName":"Chrome","screen":"1024x768 2.0x","headerUserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3810.0 Safari/537.36"},"chatsSync":0,"contactsSync":0,"presenceSync":0})
		open('%s.ttsession' % self.session, 'w').write(token)
		return login
		
	def globalSearch(self, query):
		return self.apiRequest(60, {"query": query, "count": 30, "type": "ALL"})
	
	def resolveUser(self, contactId):
		return self.apiRequest(32, {"contactIds": [contactId]})
	
	def resolveChat(self, chatId):
		return self.apiRequest(48, {"chatIds":[chatId]})
	
	def joinChannel(self, username):
		return self.apiRequest(57, {"link":"https://tt.me/" + username})
	
	def leaveChannel(self, chatId):
		return self.apiRequest(58, {"chatId": chatId})
	
	def sendMessage(self, chatId, text):
		return self.apiRequest(64, {"notify": True,"type": "USER","chatId": chatId, "message":{"cid": int(time.mktime(datetime.datetime.now().timetuple()) * 1000), "text": text,"detectShare": True}})
	
	def updateUsername(self, username):
		return self.apiRequest(16, {"link": username})
	
	def updateName(self, name):
		return self.apiRequest(16, {"name": name})
	
	def updateDescription(self, description):
		return self.apiRequest(16, {"description": description})
	
	def updateAvatar(self, image):
		self.ws.recv()
		url = self.apiRequest(80, {"count": 1, "profile": True})
		r = requests.post('https://msgproxy.mycdn.me/__proxy_host/' + url['payload']['url'].replace('https://', ''), files={'file': open(image, 'rb')}).json()
		token = r['photos'].items()[0][1]['token']
		return self.apiRequest(16, {"photoToken": token})
		
	def loginFromSession(self):
		token = open('session.ttsession', 'r').read()
		login = self.apiRequest(19, {"token": token,"userAgent":{"deviceType":"WEB","appVersion":"2.0.17","osVersion":"Windows","locale":"ru","deviceName":"Chrome","screen":"1024x768 2.0x","headerUserAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3810.0 Safari/537.36"},"chatsSync":1559393601918,"contactsSync":1559393110636,"presenceSync":1559393600,"configHash":"4a24a5f0-0000000000000000-c00001cc-0000000000000001-5f24db9d-0000000000000000-00000000-0"})
		return login
	
	def getSessions(self):
		return self.apiRequest(96, None)
	
	def reportChannel(self, chatId):
		return self.apiRequest(117, {"chatId": chatId, "complaint": "SPAM"})
	
	def createContact(self, phone):
		return self.apiRequest(41, {"phone": phone})