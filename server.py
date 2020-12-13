import time
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)
start_time = datetime.now().strftime('%H:%M:%S %d.%m.%Y')
messages = [
	{'username': 'Server', 'text': 'Server is running', 'timestamp': time.time()}
]
users = {
	'': ''
}


@app.route('/')
def hello():
	return 'Hello, user! Это мессенджер. Его <a href="/status">статус</a>'


@app.route('/status')
def status():
	return {
		'name': 'Chat',
		'status': 'OK',
		'start_time': start_time,
		'curr_time': datetime.now().strftime('%H:%M:%S %d.%m.%Y'),
		'messages_count': len(messages),
		'users_count': len(users)
	}


# отправка сообщений
@app.route("/SendMessage")
def SendMessage():
	username = request.json['username']
	password = request.json['password']
	text = request.json['text']

	if username in users:
		if users[username] != password:
			return {'ok': False}
	else:
		users[username] = password

	messages.append({'username': username, 'text': text, 'timestamp': time.time()})

	return {'ok': True}


# получение сообщений
@app.route('/GetMessage')
def GetMessage():
	after = float(request.args['after'])
	result = []
	for message in messages:
		if message['timestamp'] > after:
			result.append(message)

	return {
		'messages': result
	}


app.run()
