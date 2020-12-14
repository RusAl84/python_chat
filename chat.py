import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from ui import *
import requests
from datetime import datetime


class GUI(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.pushButton.clicked.connect(self.send)

		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.timer1_tick)
		self.timer.start(1)

		self.ui.lineEdit_2.setDisabled(True)
		self.last_timestamp = 0

	# получение сообщений
	def timer1_tick(self):
		response = requests.get('http://127.0.0.1:5000/GetMessage', params={'after': self.last_timestamp})
		messages = response.json()['messages']
		for message in messages:
			dt = datetime.fromtimestamp(message['timestamp'])
			dt = dt.strftime('%H:%M:%S %d.%m.%Y')
			self.ui.textBrowser.append(dt)
			self.ui.textBrowser.append(message['username'] + ': ' + message['text'])
			self.ui.textBrowser.append('')
			self.ui.textBrowser.repaint()
			self.last_timestamp = message['timestamp']

	# отправка сообщений
	def send(self):
		username = self.ui.lineEdit.text()
		password = self.ui.lineEdit_3.text()
		text = self.ui.lineEdit_2.text()
		requests.get(
			'http://127.0.0.1:5000/SendMessage',
			json={'username': username, 'password': password, 'text': text})

		self.ui.lineEdit_2.setText(' ')

		if password == '' or username == '':
			self.ui.lineEdit_2.setDisabled(True)
		else:
			self.ui.lineEdit_2.setDisabled(False)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	myapp = GUI()
	myapp.show()
	sys.exit(app.exec_())
