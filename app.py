from flask import Flask, render_template, redirect, request, url_for
from telebot import types
import threading
import telebot

bot = telebot.TeleBot('6164055128:AAH2Wt6rMSA8QpXMuRWtWSu-2v792eNG4gw')
bot_notice = telebot.TeleBot('6082532435:AAGM1fn49L7e82dzEjZHfVu67GUTWx1U5yk')
application = Flask(__name__)


@application.route('/')
def index():
    data=[
    { "h1": open("texts/h1-home.txt").read(),
    "p": open("texts/p-home.txt").read(),
    
    }, { "p": open("texts/history-p.txt").read(),

    },
    ]
    return render_template('index.html', data=data)

@application.route('/request',methods = ['POST', 'GET'])
def requesting():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        email = request.form['email']
        notice(name, message, email)

        return redirect(url_for('index'), 301)



# TELEGRAM SERVER PART

def notice(name, m, email):
    bot_notice.send_message(1293788323, f'Новая заявка! 📝\nИмя клиента: {name}\nСообщение: {m}\nАдрес почты клиента: {email}')
    bot_notice.send_message(122167541, f'Новая заявка! 📝\nИмя клиента: {name}\nСообщение: {m}\nАдрес почты клиента: {email}')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Панель управления Resol\nДобро пожаловать! Выберите раздел управления.', reply_markup=markup), selector)


def selector(message):
    if message.text == 'Редактировать сайт 📝':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Главная")
        back = types.KeyboardButton("История")
        back1 = types.KeyboardButton("Наши решения")
        back2 = types.KeyboardButton("Выбор")
        back3 = types.KeyboardButton("Клиенты")
        back4 = types.KeyboardButton("Новости")
        back5 = types.KeyboardButton("Связь")
        back6 = types.KeyboardButton("Назад")


        markup.add(btn1, back, back1, back2, back3, back4, back5, back6)
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Отлично. Выберите раздел, который надо отредактировать! 🗂', reply_markup=markup), selector)

    elif message.text == 'Получить список всех заявок 📊':
        bot.send_message(message.chat.id, 'Подождите... Происходит формирования выдачи данных из базы ⚙️')


    elif message.text == 'Главная':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Текст - H1")
        back = types.KeyboardButton("Текст - p")
        back1 = types.KeyboardButton("Назад")
        markup.add(btn1, back, back1)

        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Выберите какой раздел отредактировать', reply_markup=markup), home)


    elif message.text == 'История':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Текст - p")
        back1 = types.KeyboardButton("Назад")
        markup.add(back, back1)

        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Выберите какой раздел отредактировать', reply_markup=markup), history)

# HOME SECTION

def home(message):
    if message.text == 'Текст - H1':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/h1-home.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введите новый текст'), home_h1)

    elif message.text == 'Текст - p':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/p-home.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введите новый текст'), home_p)

def home_h1(message):
    with open('texts/h1-home.txt', 'w') as file:
            file.write(message.text)

    bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im')

def home_p(message):
    with open('texts/p-home.txt', 'w') as file:
            file.write(message.text)

    bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im')

def bot_start():
    bot.polling()


# HOME SECTION - END


# HISTORY SECTION

def history(message):

    if message.text == 'Текст - p':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/history-p.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введите новый текст'), history_p)


def history_p(message):
    with open('texts/history-p.txt', 'w') as file:
            file.write(message.text)

    bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im')

threading.Thread(target=bot_start).start()
application.run(debug=True, threaded=True, host='0.0.0.0')
