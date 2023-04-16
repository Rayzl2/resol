from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, redirect, request, url_for
from telebot import types
import threading
import telebot
import smtplib as smtp

bot = telebot.TeleBot('6164055128:AAH2Wt6rMSA8QpXMuRWtWSu-2v792eNG4gw')
bot_notice = telebot.TeleBot('6082532435:AAGM1fn49L7e82dzEjZHfVu67GUTWx1U5yk')
application = Flask(__name__)


@application.route('/')
def index():
    data=[
    { 
        "h1": open("texts/h1-home.txt").readline(),
        "p": open("texts/p-home.txt").read(),
        "title": open("texts/title.txt").read(),
    
    }, 
    { 
        "p": open("texts/history-p.txt").read(),

    }, 
    {
        "p": open("texts/sols-p.txt").read(),
        "block1": open("texts/sol-b1.txt").read(),
        "block2": open("texts/sol-b2.txt").read(),
        "block3": open("texts/sol-b3.txt").read(),
        "block4": open("texts/sol-b4.txt").read(),
    }, 
    {
        "nc1":  open("texts/news-category1.txt").read(),
        "nc2":  open("texts/news-category2.txt").read(),
        "nc3":  open("texts/news-category3.txt").read(),
        "nc4":  open("texts/news-category4.txt").read(),
        "nt1":  open("texts/news-b1.txt").read(),
        "nt2":  open("texts/news-b2.txt").read(),
        "nt3":  open("texts/news-b3.txt").read(),
        "nt4":  open("texts/news-b4.txt").read(),
        "nd1":  open("texts/news-date1.txt").read(),
        "nd2":  open("texts/news-date2.txt").read(),
        "nd3":  open("texts/news-date3.txt").read(),
        "nd4":  open("texts/news-date4.txt").read(),
        
    },
    {
        "block1": open("texts/cl-b1.txt").read(),
        "block2": open("texts/cl-b2.txt").read(),
        "block3": open("texts/cl-b3.txt").read(),
        "block4": open("texts/cl-b4.txt").read(),
        "block5": open("texts/cl-b5.txt").read(),
        "block6": open("texts/cl-b6.txt").read(),
    }
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
    bot_notice.send_message(5845778657, f'Новая заявка! 📝\nИмя клиента: {name}\nСообщение: {m}\nАдрес почты клиента: {email}')
    
    
    # MAIL SENTt

    msg = MIMEMultipart()
    msg['From'] = 'resol@dmitriyeff.ru'
    msg['To'] = 'info@resol.im'
    msg['Subject'] = 'Новая заявка с сайта!'
    message = f'Новая заявка! 📝\nИмя клиента: {name}\nСообщение: {m}\nАдрес почты клиента: {email}'
    msg.attach(MIMEText(message))
    try:
        mailserver = smtp.SMTP('smtp.yandex.ru',587)
        mailserver.set_debuglevel(True)
    # Определяем, поддерживает ли сервер TLS
        mailserver.ehlo()
    # Защищаем соединение с помощью шифрования tls
        mailserver.starttls()
    # Повторно идентифицируем себя как зашифрованное соединение перед аутентификацией.
        mailserver.ehlo()
        mailserver.login('resol@dmitriyeff.ru', 'qhkqkzhzmvpzraqf')
        mailserver.sendmail('resol@dmitriyeff.ru','info@resol.im',msg.as_string())
        mailserver.quit()
        print("Письмо успешно отправлено")
    except smtp.SMTPException:
        print("Ошибка: Невозможно отправить сообщение")


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
        btn2 = types.KeyboardButton("Заголовок")
        btn1 = types.KeyboardButton("Главная")
        back = types.KeyboardButton("История")
        back1 = types.KeyboardButton("Наши решения")
        back2 = types.KeyboardButton("Выбор")
        back3 = types.KeyboardButton("Клиенты")
        back4 = types.KeyboardButton("Новости")
        back5 = types.KeyboardButton("Связь")
        back6 = types.KeyboardButton("Назад")


        markup.add(btn2, btn1, back, back1, back2, back3, back4, back5, back6)
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Отлично. Выберите раздел, который надо отредактировать! 🗂', reply_markup=markup), selector)

    elif message.text == 'Получить список всех заявок 📊':
        bot.send_message(message.chat.id, 'Подождите... Происходит формирования выдачи данных из базы ⚙️')

    elif message.text == 'Заголовок':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        bot.send_message(message.chat.id, 'Актуальный заголовок на сайте: ' + open("texts/title.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введите новый заголовок'), title)
    
    
    elif message.text == 'Главная':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Текст - H1")
        back = types.KeyboardButton("Текст - p")
        back1 = types.KeyboardButton("Назад")
        markup.add(btn1, back, back1)

        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Выберите какой раздел отредактировать', reply_markup=markup), home)


    elif message.text == 'Клиенты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Текст - p")
        back1 = types.KeyboardButton("Блоки")
        back2 = types.KeyboardButton("Блок 2")
        back3 = types.KeyboardButton("Блок 3")
        back4 = types.KeyboardButton("Блок 4")
        back4 = types.KeyboardButton("Блок 5")
        back4 = types.KeyboardButton("Блок 6")
        markup.add(back1)

        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Выберите какой раздел отредактировать', reply_markup=markup), clients)
        
        
    elif message.text == 'История':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Текст - p")
        back1 = types.KeyboardButton("Назад")
        markup.add(back, back1)

        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Выберите какой раздел отредактировать', reply_markup=markup), history)
        
    
    elif message.text == 'Наши решения':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Текст - p")
        back1 = types.KeyboardButton("Блоки")
        back2 = types.KeyboardButton("Блок 2")
        back3 = types.KeyboardButton("Блок 3")
        back4 = types.KeyboardButton("Блок 4")
        markup.add(back, back1)

        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Выберите какой раздел отредактировать', reply_markup=markup), solutions)
        
    elif message.text == 'Новости':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Категория 1")
        back1 = types.KeyboardButton("Категория 2")
        back2 = types.KeyboardButton("Категория 3")
        back3 = types.KeyboardButton("Категория 4")
        
        back5 = types.KeyboardButton("Текст 1")
        back6 = types.KeyboardButton("Текст 2")
        back7 = types.KeyboardButton("Текст 3")
        back8 = types.KeyboardButton("Текст 4")
        
        back9 = types.KeyboardButton("Дата 1")
        back10 = types.KeyboardButton("Дата 2")
        back11 = types.KeyboardButton("Дата 3")
        back12 = types.KeyboardButton("Дата 4")
        markup.add(back, back5, back9, back1, back6, back10, back2, back7, back11, back3, back8, back12)

        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Выберите какой раздел отредактировать', reply_markup=markup), news)
# HOME SECTION

def title(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/title.txt', 'w') as file:
                file.write(message.text)
    
    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def home(message):
    if message.text == 'Текст - H1':
        
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/h1-home.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введите новый текст'), home_h1)

    elif message.text == 'Текст - p':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/p-home.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введите новый текст'), home_p)

def home_h1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/h1-home.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def home_p(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/p-home.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def bot_start():
    bot.polling()


# HOME SECTION - END


# HISTORY SECTION

def history(message):

    if message.text == 'Текст - p':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/history-p.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введите новый текст'), history_p)


def history_p(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/history-p.txt', 'w') as file:
            file.write(message.text)

    bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup)

# HISTORY SECTION - END

# SOLUTIONS SECTION
def solutions(message):
    if message.text == 'Текст - p':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/sols-p.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Введите новый текст'), sols_p)
    
    elif message.text == 'Блоки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Текст 1")
        back = types.KeyboardButton("Картинка 1")
        
        btn2 = types.KeyboardButton("Текст 2")
        back2 = types.KeyboardButton("Картинка 2")
        
        btn3 = types.KeyboardButton("Текст 3")
        back3 = types.KeyboardButton("Картинка 3")
        
        btn4 = types.KeyboardButton("Текст 4")
        back4 = types.KeyboardButton("Картинка 4")
        markup.add(btn1, back, btn2, back2, btn3, back3, btn4, back4)
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Что поменять?', reply_markup=markup), sol_blocks)

def sols_p(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/sols-p.txt', 'w') as file:
            file.write(message.text)

    bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup)


def sol_blocks(message):
    if message.text == 'Картинка 1':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), sol_pic_1)
    
    elif message.text == 'Картинка 2':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), sol_pic_2)
    
    elif message.text == 'Картинка 3':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), sol_pic_3)
    
    elif message.text == 'Картинка 4':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), sol_pic_4)
    
    elif message.text == 'Текст 1':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/sol-b1.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), sol_p_1)
    
    elif message.text == 'Текст 2':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/sol-b2.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), sol_p_2)
    
    elif message.text == 'Текст 3':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/sol-b3.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), sol_p_3)
    
    elif message.text == 'Текст 4':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/sol-b4.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), sol_p_4)
    

def sol_p_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/sol-b1.txt', 'w') as file:
            file.write(message.text)

    bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup)
    

def sol_p_2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/sol-b2.txt', 'w') as file:
            file.write(message.text)

    bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup)
    
def sol_p_3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/sol-b3.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)
    
    
def sol_p_4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/sol-b4.txt', 'w') as file:
            file.write(message.text)

    bo.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def sol_pic_1(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/Group 224.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)


def sol_pic_2(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/Group 225.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)


def sol_pic_3(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/Group 226.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)



def sol_pic_4(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/Group 227.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)

# SOLUTION SECTION - END

# NEWS SECTION
def news(message):
    if message.text == 'Категория 1':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-category1.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_c1)
    
    elif message.text == 'Категория 2':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-category2.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_c2)
    
    elif message.text == 'Категория 3':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-category3.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_c3)
    
    elif message.text == 'Категория 4':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("news-category4.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_c4)
    
    elif message.text == 'Текст 1':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-b1.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_t1)
    
    elif message.text == 'Текст 2':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-b2.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_t2)
    
    elif message.text == 'Текст 3':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-b3.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_t3)
    
    elif message.text == 'Текст 4':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-b4.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_t4)
    
    elif message.text == 'Дата 1':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-date1.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_d1)
    
    elif message.text == 'Дата 2':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-date2.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_d2)
    
    elif message.text == 'Дата 3':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-date3.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_d3)
    
    elif message.text == 'Дата 4':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/news-date4.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), news_d4)
    

def news_c1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-category1.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)


def news_c2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-category2.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)


def news_c3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-category3.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)


def news_c4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-category4.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)



def news_t1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-b1.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)


def news_t2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-b2.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)


def news_t3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-b3.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)


def news_t4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-b4.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)


def news_d1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-date1.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def news_d2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-date2.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def news_d3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-date3.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def news_d4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/news-date4.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

# NEWS SECTION - END

# CLIENT SECTION

def clients(message):
    if message.text == 'Блоки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Текст 1")
        back = types.KeyboardButton("Картинка 1")
        
        btn2 = types.KeyboardButton("Текст 2")
        back2 = types.KeyboardButton("Картинка 2")
        
        btn3 = types.KeyboardButton("Текст 3")
        back3 = types.KeyboardButton("Картинка 3")
        
        btn4 = types.KeyboardButton("Текст 4")
        back4 = types.KeyboardButton("Картинка 4")
        
        btn5 = types.KeyboardButton("Текст 5")
        back5 = types.KeyboardButton("Картинка 5")
        
        btn6 = types.KeyboardButton("Текст 6")
        back6 = types.KeyboardButton("Картинка 6")
        
        markup.add(btn1, back, btn2, back2, btn3, back3, btn4, back4, btn5, back5, btn6, back6)
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Что поменять?', reply_markup=markup), client_blocks)
    

def client_blocks(message):
    if message.text == 'Картинка 1':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), cl_pic_1)
    
    elif message.text == 'Картинка 2':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), cl_pic_2)
    
    elif message.text == 'Картинка 3':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), cl_pic_3)
    
    elif message.text == 'Картинка 4':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), cl_pic_4)
        
    elif message.text == 'Картинка 5':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), cl_pic_5)
    
    elif message.text == 'Картинка 6':
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новую картинку как ДОКУМЕНТ!'), cl_pic_6)
    
    
    elif message.text == 'Текст 1':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/cl-b1.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), cl_p_1)
    
    elif message.text == 'Текст 2':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/cl-b2.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), cl_p_2)
    
    elif message.text == 'Текст 3':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/cl-b3.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), cl_p_3)
    
    elif message.text == 'Текст 4':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/cl-b4.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), cl_p_4)
        
    elif message.text == 'Текст 5':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/cl-b5.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), cl_p_5)
    
    elif message.text == 'Текст 6':
        bot.send_message(message.chat.id, 'Актуальный текст на сайте:' + open("texts/cl-b6.txt").read())
        bot.register_next_step_handler(bot.send_message(message.chat.id, 'Пришлите новый текст'), cl_p_6)


def cl_pic_1(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/client1.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)

def cl_pic_2(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/client2.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)

def cl_pic_3(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/client3.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)

def cl_pic_4(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/client4.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)

def cl_pic_5(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/client5.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)

def cl_pic_6(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        src = 'static/img/client6.png';
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Редактировать сайт 📝")
        back = types.KeyboardButton("Получить список всех заявок 📊")
        markup.add(btn1, back)
        bot.send_message(chat_id, "Файл успешно загружен!", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, e)


def cl_p_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/cl-b1.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def cl_p_2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/cl-b2.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def cl_p_3(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/cl-b3.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def cl_p_4(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/cl-b4.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def cl_p_5(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/cl-b5.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)

def cl_p_6(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Редактировать сайт 📝")
    back = types.KeyboardButton("Получить список всех заявок 📊")
    markup.add(btn1, back)
    with open('texts/cl-b6.txt', 'w') as file:
            file.write(message.text)

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Текст успешно изменен! Проверьте сайт.\nhttps://resol.im', reply_markup=markup), selector)



threading.Thread(target=bot_start).start()
if __name__ == "__main__":
    application.run(debug=True, threaded=True, host='0.0.0.0')
