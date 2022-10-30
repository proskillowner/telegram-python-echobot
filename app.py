import re
from flask import Flask, request
import telegram
from echobot.credentials import bot_user_name, TOKEN, URL


bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def echo():
	update = telegram.Update.de_json(request.get_json(force=True), bot)

	if 'message' not in update:
		return 'cancel'

	chat_id = update.message.chat.id
	text = update.message.text.encode('utf-8').decode()

	if text == '/start':
		text = 'Welcome'
	else:
		text = re.sub(r'\W', '_', text)

	bot.sendChatAction(chat_id=chat_id, action='typing')

	sleep(1)

	bot.sendMessage(chat_id=chat_id, text=text)

	return 'ok'


@app.route('/setWebhook', methods=['GET', 'POST'])
def setWebhook():
	s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
	if s:
		return 'setWebhook success'
	else:
		return 'setWebhook fail'


@app.route('/')
def index():
	return '.'


if __name__ == '__main__':
	app.run(threaded=True)

