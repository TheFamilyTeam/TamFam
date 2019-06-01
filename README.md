# TamFam
A python library to interact with TamTam's API

NB: This is not meant to communicate with the BOT API, but rather with the official user API.

# Dependencies
* websocket
* requests
* json
* time
* os
* datetime

# Creating a Bot
```python
if __name__ == '__main__':
	a = TamFam("session")
	
	if not os.path.isfile("%s.ttsession" % a.session):
		x = a.phoneLogin(raw_input('Phone number: '))
		l = a.completePhoneLogin(x, raw_input('SMS Code: '))
		name = l['payload']['profile']['names'][0]['name']
		print("Logged in as %s!" % name)
	else:
		l = a.loginFromSession()
		name = l['payload']['profile']['names'][0]['name']
		print("Logged in as %s (session)!" % name)
	
	# Example Bot
	while 1:
		update = json.loads(a.ws.recv())
		if update['opcode'] == 128:
			cid = update['payload']['chatId']
			text = update['payload']['message']['text']
			a.sendMessage(cid, 'https://github.com/TheFamilyTeam')
```
