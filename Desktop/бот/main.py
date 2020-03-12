from flask import Flask, request
import telebot
from telebot import types
import time
import config
from random import random, randint, choice
import re
import os
import pyexecute

app = Flask(__name__)

machine = os.environ.get('HOMESTATION')

token = os.environ.get('PEREKUR_TOKEN_BOT')
if not token:
	token = config.token

bot = telebot.TeleBot(token, threaded=False)

if not machine:
	@app.route('/%s/' % token, methods=["POST"])
	def webhook():
	    bot.process_new_updates([telebot.types.Update.de_json(
	    	request.stream.read().decode("utf-8"))]
	    )
	    return 'ok', 200

def update_smesharik_data():
	smeshariks_data = pyexecute.get_smeshariks_data()
	bool_ = False
	for id_, username in smeshariks_data:
		user = bot.get_chat_member(config.smeshariki_id, id_)
		if user.user.username != username:
			pyexecute.update_smesharik_data(id_, username)
			bool_ = True
	return bool_



secrete_word = ["H", "O", "L", "M","S"]
ans_seq = []

def questions(num, message):
	markup_yes_no = types.InlineKeyboardMarkup()
	button_yes = types.InlineKeyboardButton(text='Yes',
		callback_data=f'c_smeshariks_yes_{num}')
	button_no = types.InlineKeyboardButton(text='No',
		callback_data=f'c_smeshariks_no_{num}')
	markup_yes_no.add(button_yes, button_no)
	if num == 1:
		text = 'Первый вопрос:\nВ смешариках 11 участников?'
	elif num == 2:
		text = 'Егор Плглв и Юля Тарасенко начали встречаться 30 ноября?'
	elif num == 3:
		text = 'Хотел ли Рома отрезать себе средний палец?'
	elif num == 4:
		text = 'Дошила ли Инна трусы Юле на День Рождения?'
	elif num == 5:
		text = '5. У Пушкина - 3,  у Артема - 9, у Даника - 27, а у Егора - ?'
		bot.send_message(message.chat.id, text, parse_mode='Markdown')
		return None

	bot.send_message(message.chat.id,
			text, parse_mode='Markdown', reply_markup=markup_yes_no)

avramenko_photo = (
	'AgADAgAD36sxG7Eq6EnbadnHZFg7N1hBhA8ABFzmU1SwlQo8EK4DAAEC',
	'AgADAgADC6wxGxhT6UmcTbb3_sI2Kqraug8ABGOcpGElGJlwezMAAgI',
	'AgADAgAD4KsxG7Eq6EkdYfAAAa49Tax7_7cPAAT3O4lRR-82I8eQAQABAg',
	'AgADAgAD4asxG7Eq6EnsrDAqDs4q5wzfuQ8ABFu4C_9K2n1gqDQAAgI',
	'AgADAgADDKwxGxhT6Ul857xG-RDG8hX38Q4ABKHTxNum7qpuVsUBAAEC',
	'AgADAgADDawxGxhT6UlolK1UiqUZKLjPuQ8ABEGvBSl-TD2cojMAAgI',
	'AgADAgAD4asxG7Eq6EnsrDAqDs4q5wzfuQ8ABFu4C_9K2n1gqDQAAgI',
	'AgADAgAD4qsxG7Eq6EmrC8zSGC-oinT3tw8ABNmWa2Jjwc3P_ZMBAAEC',
	'AgADAgAD46sxG7Eq6ElS-MdxvDaFY8Hjug8ABFwWfqBjwY7UPCEAAgI',
	'AgADAgAD36sxG7Eq6EnbadnHZFg7N1hBhA8ABFzmU1SwlQo8EK4DAAEC',
	'AgADAgADDqwxGxhT6UlrCe57YEhsGnzTuQ8ABDFtYtuF_Om-EDMAAgI',
	'AgADAgAD4KsxG7Eq6EkdYfAAAa49Tax7_7cPAAT3O4lRR-82I8eQAQABAg'
)

@bot.message_handler(func=lambda message: ans_seq[0] == 'holms' if ans_seq else False)
def holms(message):
	if message.text.lower() == 'holms':
		bot.send_message(message.chat.id, 'Ты прав')
		ans_seq.pop()
		ans_seq.append('avramenko')

		bot.send_message(message.chat.id, 'В книге про Шерлока Холмса была определенная азбука:')
		for photo_id in avramenko_photo:
			bot.send_photo(message.chat.id, photo_id)

		bot.send_message(message.chat.id, 'Удачи брат')
	else:
		bot.send_message(message.chat.id, 'У тебя есть еще несколько попыток. А потом Юля бросит тебя')

@bot.message_handler(func=lambda message: ans_seq[0] == 'avramenko' if ans_seq else False)
def avram(message):
	if message.text.lower() == 'zno avramenko':
		bot.send_message(message.chat.id, 'И эту загадку ты решил!', parse_mode='Markdown')
		ans_seq.pop()

		bot.send_message(message.chat.id, 'Следующая загадка\nНомер помойки / 10')
		ans_seq.append('pomoika')
		bot.send_sticker(message.chat.id, 'CAADAgADDQADvWd7JB-x4_siRcCPAg')
	else:
		bot.send_message(message.chat.id, 'Не верно, ебош еще')

@bot.message_handler(func=lambda message: ans_seq[0] == 'pomoika' if ans_seq else False)
def pomoika(message):
	try:
		text = float(message.text)
	except ValueError:
		bot.send_message(message.chat.id, 'Только числа!')
		return None

	if text == 2.7:
		bot.send_message(message.chat.id, 'Верно! А теперь переведи это'
			' в 200 бальную систему ЗНО')
		ans_seq.pop()
		ans_seq.append('200')
	else:
		bot.send_message(message.chat.id, 'ПОМОЙКИ НОМЕР / 10')

@bot.message_handler(func=lambda message: ans_seq[0] == '200' if ans_seq else False)
def zno_200(message):
	try:
		text = float(message.text)
	except ValueError:
		bot.send_message(message.chat.id, 'Только числа!')
		return None

	if text == 107:
		bot.send_message(message.chat.id, 'Ты почти у цели!!!')
		ans_seq.pop()

		ans_seq.append('avtoshkola')
		bot.send_message(message.chat.id, 'Введи слово из выделенных букв')
		bot.send_photo(message.chat.id, 'AgADAgAD7qsxGzAh4ElanWLJnm_Qu51GhA8ABE3A_JD0sFuHtakDAAEC')
	else:
		bot.send_message(message.chat.id, 'Еще попытка...')

@bot.message_handler(func=lambda message: ans_seq[0] == 'avtoshkola' if ans_seq else False)
def avtoshkola(message):
	if message.text.lower() == 'автошкола':
		bot.send_message(message.chat.id, 'Наконец-то... ждем тебя на этом месте в 10:00')
		ans_seq.pop()
	else:
		bot.send_message(message.chat.id, 'ПИ контракт ХИРЭ братан')

@bot.message_handler(commands=['s_dr_plglv'])
def test_func(message):
	question = 1
	bot.send_message(message.chat.id, 'Доброе утро.')

	bot.send_message(message.chat.id, 'Готовь свои извилины и никакой Берш тебе не поможет.')

	questions(question, message)


@bot.callback_query_handler(func=lambda call: secrete_word)
def query_handler(call):
	num_question = int(call.data[-1])
	count_word = len(secrete_word)
	answer_status_true = num_question + count_word == 6
	if not answer_status_true:
		alert_text = "КЫШ"

	if call.data.startswith('c_smeshariks_yes'):
		# first
		if call.data == 'c_smeshariks_yes_1' and answer_status_true:
			alert_text = "Правильно!"

		# second
		elif call.data == 'c_smeshariks_yes_2' and answer_status_true:
			alert_text = "Правильно!"

		# third
		elif call.data == 'c_smeshariks_yes_3' and answer_status_true:
			alert_text = "Ну и дурак ты конечно... дам тебе еще попытку"

		# forth
		elif call.data == 'c_smeshariks_yes_4' and answer_status_true:
			alert_text = "Ну и дурак ты конечно... дам тебе еще попытку"

		bot.answer_callback_query(callback_query_id=call.id,
			text=alert_text, show_alert=False)

		if alert_text == "Правильно!":
			secrete_liter = random.choice(secrete_word)
			secrete_word.remove(secrete_liter)
			bot.send_message(call.message.chat.id,
				secrete_liter, parse_mode='Markdown')

			questions(num_question + 1, call.message)

	elif call.data.startswith('c_smeshariks_no'):
		# first
		if call.data == 'c_smeshariks_no_1' and answer_status_true:
			alert_text = "Ну и дурак ты конечно... дам тебе еще попытку"

		# second
		elif call.data == 'c_smeshariks_no_2' and answer_status_true:
			alert_text = "Ну и дурак ты конечно... дам тебе еще попытку"

		# third
		elif call.data == 'c_smeshariks_no_3' and answer_status_true:
			alert_text = "Правильно!"

		# forth
		elif call.data == 'c_smeshariks_no_4' and answer_status_true:
			alert_text = "Правильно!"

		bot.answer_callback_query(callback_query_id=call.id,
				text=alert_text, show_alert=False)

		if alert_text == "Правильно!":
			secrete_liter = random.choice(secrete_word)
			secrete_word.remove(secrete_liter)
			bot.send_message(call.message.chat.id,
				secrete_liter, parse_mode='Markdown')

			questions(num_question + 1, call.message)
			if num_question == 4:
				ans_seq.append(True)

@bot.message_handler(func=lambda message: ans_seq)
def answer_fifth(message):
	if not message.text.isdigit():
		bot.send_message(message.chat.id, 'Только числа!', parse_mode='Markdown')
		return None

	if int(message.text) == 29:
		secrete_liter = random.choice(secrete_word)
		secrete_word.remove(secrete_liter)
		bot.send_message(message.chat.id, text, parse_mode='Markdown')
		bot.send_message(message.chat.id, secrete_liter, parse_mode='Markdown')
		ans_seq.pop()

		bot.send_message(message.chat.id,
			'Введи слово', parse_mode='Markdown')
		ans_seq.append('holms')
	else:
		text = 'Еще варианты? Умник...'
		bot.send_message(message.chat.id, text, parse_mode='Markdown')



@bot.message_handler(commands=['perekur'])
def command_perekur(message):
	if message.chat.type == "group" or message.chat.type == "supergroup":
		users = pyexecute.get_smeshariks_username()
		perekur_text = ''
		perekur_text = perekur_text + config.perekur + '\n'
		for i in users:
			perekur_text = perekur_text +'@' + i + '\n'
		bot.send_message(message.chat.id, perekur_text)
	elif message.chat.type == "private":
		bot.send_message(message.chat.id, ".-.")

@bot.message_handler(commands=['obed'])
def command_obed(message):
	if message.chat.type == "group" or message.chat.type == "supergroup":
		users = pyexecute.get_smeshariks_username()
		obed_text = ''
		obed_text = obed_text + config.obed + '\n'
		for i in users:
			obed_text = obed_text +'@' + i + '\n'
		obed_text = obed_text + "хуй ;)"
		bot.send_message(message.chat.id, obed_text)
	elif message.chat.type == "private":
		bot.send_message(message.chat.id, ".-.")

@bot.message_handler(commands=['utro'])
def command_utro(message):
	if message.chat.type == "group" or message.chat.type == "supergroup":
		utro_text = ''
		utro_text = utro_text + config.utro + '\n'
		users = pyexecute.get_smeshariks_username()
		for i in users:
			utro_text = utro_text +'@' + i + '\n'
		utro_text = utro_text + "pora rabotat ;)"
		bot.send_message(message.chat.id, utro_text)
	elif message.chat.type == "private":
		bot.send_message(message.chat.id, ".-.")

@bot.message_handler(commands=['vse'])
def command_vse(message):
	if message.chat.type == "group" or message.chat.type == "supergroup":
		users = pyexecute.get_smeshariks_username()
		vse_text = ''
		vse_text = vse_text + config.vse + '\n'
		for i in users:
			vse_text = vse_text +'@' + i + '\n'
		vse_text = vse_text + "по домам ;)"
		bot.send_message(message.chat.id, vse_text)
	elif message.chat.type == "private":
		bot.send_message(message.chat.id, ".-.")

@bot.message_handler(commands=['max'])
def command_max(message):
	max_text = choice(config.max_text)
	bot.send_message(message.chat.id, max_text)

@bot.message_handler(commands=['buxat'])
def command_buxate(message):
	if message.chat.type == "group" or message.chat.type == "supergroup":
		users = pyexecute.get_smeshariks_username()
		users = ['@' + i + '\n' for i in users]
		text = config.buxat + '\n'
		for i in users:
			text = text + i
		bot.send_message(message.chat.id, text)
	elif message.chat.type == "private":
		bot.send_message(message.chat.id, ".-.")

@bot.message_handler(commands=['oficial_smesharik'],
	func=lambda message: message.from_user.id == config.user_admin)
def set_data(message):
	if message.reply_to_message:
		user_id = message.reply_to_message.from_user.id
		user = bot.get_chat_member(message.chat.id, user_id)
		add_status = pyexecute.set_smesharik_data(user_id, user.user.username)
		if add_status:
			bot.send_message(message.chat.id, 'Есть')
		else:
			bot.send_message(message.chat.id, 'Этот черт уже был')
	else:
		bot.send_message(message.chat.id, 'Только с reply\'ем на сообщение')

@bot.message_handler(commands=['update_usernames'])
def update_usernames(message):
	if update_smesharik_data():
		bot.send_message(message.chat.id, 'Обновлено')
	else:
		bot.send_message(message.chat.id, 'Все с прежними юзерами')

# TUK_TUK sticker
@bot.message_handler(func=lambda message: (message.text == 'тук тук' or message.text == 'Тук тук'))
def tuk_tuk_send(message):
    if randint(0,2) == 0:
	    bot.send_sticker(message.chat.id, config.tuk_tuk_S, reply_to_message_id=message.message_id)
# PIVO sticker
@bot.message_handler(func=lambda message: ('Пиво' == message.text or 'пиво' == message.text))
def haha_pivo_send(message):
    if randint(0,2) == 0:
	    bot.send_sticker(message.chat.id, config.haha_pivasik_S, reply_to_message_id=message.message_id)

@bot.message_handler(func=lambda message: True and
	message.chat.type == 'private')
def end_handl(message):
	bot.send_message(message.chat.id, '.-.')
