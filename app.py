import re
from flask import Flask, request
import telegram
from echobot.credentials import bot_user_name, TOKEN, URL


bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
	update = telegram.Update.de_json(request.get_json(force=True), bot)

	chat_id = update.message.chat.id
	msg_id = update.message.message_id

	text = update.message.text.encode('utf-8').decode()
	print('got text message :', text)

	if text == '/start':
		text = 'Welcome'
		bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)
	else:
		text = re.sub(r'\W', '_', text)
		bot.sendMessage(chat_id=chat_id, text=text, reply_to_message_id=msg_id)

	return 'ok'


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
	s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
	if s:
		return 'webhook setup ok'
	else:
		return 'webhook setup failed'


@app.route('/')
def index():
	return '.'


if __name__ == '__main__':
	app.run(threaded=True)

