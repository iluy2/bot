import telebot

from telebot import types
import time

# from threading import Thread
# from telebot.util import webhook_google_functions

# 5274807635:AAEtdRC26DuAF6CMsZ_tq_51TUu8mOw1Bvg
bot = telebot.TeleBot("5274807635:AAEtdRC26DuAF6CMsZ_tq_51TUu8mOw1Bvg")


@bot.message_handler(commands='start')
def send_welcome(message):
    hello_message = "Привет " + '👋' + " Начнём?)\n Выбирай свой статус:"
    keyboard = types.InlineKeyboardMarkup()
    key_ab = types.InlineKeyboardButton(text="Абитуриент 👦🏻", callback_data='a')
    keyboard.add(key_ab)
    key_st = types.InlineKeyboardButton(text="Студент 👨🏻‍🦳", callback_data='s')
    keyboard.add(key_st)
    bot.send_message(message.from_user.id, text=hello_message, reply_markup=keyboard)


hello = "Хэй 👋🏻\n Это бот МИРЭА! Чтобы начать, введи /start, а далее: \n📌 Жми на кнопку \"абитуриент 👦🏻\" и " \
        "выбирай:\n✔️ тест 🤷🏻 - пройти тест на выбор направления 🙈️\n📌 Жми \"студент 👨🏻‍🦳\" и выбирай:\n✔️ " \
        "че по парам 🥴 - бот покажет твоё расписание 😁\n✔️ дз 😪 - запиши дз и бот напомнит о нём " \
        "🤤\n✔️ КАКАЯ ЛЕСТНЦА ⁉️ - подскажет по какой лестнице быстрее добраться)"


@bot.message_handler(commands=['desc'])
def desc_message(message):
    bot.send_message(message.from_user.id, hello)


users = {}


@bot.message_handler(content_types=['text'])
def get_mes(message):
    bot.send_message(message.chat.id, 'Что нужно запомнить?')
    bot.register_next_step_handler(message, get_message)


def get_message(message):
    alert = message.text
    chat_id = message.chat.id
    answer = f'{str(message.chat.first_name)}, через сколько минут напомнить?'
    bot.send_message(message.chat.id, text=answer)
    bot.register_next_step_handler(message, get_time)
    users[chat_id] = [alert]


def get_time(message):
    timelaps = message.text
    chat_id = message.chat.id
    users[chat_id].insert(1, timelaps)
    while not timelaps.isdigit():
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста  ')
        bot.register_next_step_handler(message, get_time)
        users[chat_id].pop()
        break
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_b = types.InlineKeyboardButton(text=" Назад ⏮", callback_data='back')
        keyboard.add(key_b)
        bot.send_message(message.chat.id, text='Запомнил ✅ \nВернуться в меню? ', reply_markup=keyboard)
        check_in(message)


def check_in(message):
    chat_id = message.chat.id
    timelaps = users[chat_id][1]
    alert = users[chat_id][0]
    time.sleep(int(timelaps) * 60)
    bot.send_message(message.chat.id, text=f'📌 НАПОМИНАНИЕ: {alert}')


@bot.message_handler(content_types=['text'])
def get_lest(message):
    bot.send_message(message.chat.id, 'Какой кабинет? 🤓')
    bot.register_next_step_handler(message, get_kab)


def get_kab(message):
    ch = message.text
    while not ch.isdigit():
        bot.send_message(message.chat.id, 'Цифрами, пожалуйста  ')
        bot.register_next_step_handler(message, get_kab)
        break
    else:
        which_stairs(message)


def which_stairs(message):
    kab = message.text
    chat_id = message.chat.id
    if 0 < int(kab) <= 110 or 199 < int(kab) <= 210 or 299 < int(kab) <= 310 or 399 < int(kab) <= 437:
        bot.send_message(message.chat.id,
                         text='✔️чтобы попасть в ' + kab + ' кабинет поднимайся по "Главной лестнице" 1️⃣')
    elif 110 < int(kab) <= 125 or 210 < int(kab) <= 225 or 310 < int(kab) <= 325:
        bot.send_message(message.chat.id,
                         text='✔️чтобы попасть в ' + kab + ' кабинет поднимайся по "Ректоркой лестнице" 2️⃣')
    elif 125 < int(kab) <= 140 or 255 < int(kab) <= 240 or 325 < int(kab) <= 340:
        bot.send_message(message.chat.id,
                         text='✔️чтобы попасть в ' + kab + ' кабинет поднимайся по "Вкусной лестнице" 3️⃣')
    elif 140 < int(kab) <= 199 or 240 < int(kab) <= 299 or 340 < int(kab) <= 399 or 437 < int(kab) <= 470:
        bot.send_message(message.chat.id,
                         text='✔️чтобы попасть в ' + kab + ' кабинет поднимайся по "Бета-лестнице" 4️⃣')
    keyboard = types.InlineKeyboardMarkup()
    key_b = types.InlineKeyboardButton(text=" Назад ⏮", callback_data='back')
    keyboard.add(key_b)
    bot.send_message(message.chat.id, text="Вернуться в меню?", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "a":
        keyboard = types.InlineKeyboardMarkup()
        key_test = types.InlineKeyboardButton(text="✔️ тест 🤷🏻 ", callback_data='test')
        keyboard.add(key_test)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        ab_text = "Удачи с поступлением 😉\nЧем можем помочь?"
        bot.send_message(call.message.chat.id, text=ab_text, reply_markup=keyboard)
    elif call.data == "s":
        keyboard = types.InlineKeyboardMarkup()
        key_rasp = types.InlineKeyboardButton(text="✔️ че по парам 🥴 ", callback_data='rasp')
        keyboard.add(key_rasp)
        key_dz = types.InlineKeyboardButton(text="✔️ дз 😪 ", callback_data='dz')
        keyboard.add(key_dz)
        key_lest = types.InlineKeyboardButton(text="✔️ КАКАЯ ЛЕСТНЦА ⁉️ ", callback_data='lest')
        keyboard.add(key_lest)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        st_text = "Чего надобно, старче? 🧐"
        bot.send_message(call.message.chat.id, text=st_text, reply_markup=keyboard)
    elif call.data == "back":
        back_keyboard = types.InlineKeyboardMarkup()
        call_button_back_a = types.InlineKeyboardButton(text="Абитуриенту 👦🏻", callback_data="a")
        call_button_back_s = types.InlineKeyboardButton(text="Студенту 👨🏻‍🦳", callback_data="s")
        back_keyboard.add(call_button_back_a)
        back_keyboard.add(call_button_back_s)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Куда?",
                              reply_markup=back_keyboard)
    elif call.data == 'dz':
        bot.send_message(call.message.chat.id, 'Запиши дз, а я напомню о нём, через сколько скажешь :)')
        get_mes(call.message)
    elif call.data == 'lest':
        bot.send_message(call.message.chat.id, text="Пока можем подсказать только по кабинетам Стромынки :(")
        get_lest(call.message)
    elif call.data == "rasp":
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text=" Институт перспективных технологий и индустриального "
                                                "программирования 🤪 ", callback_data='1')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text=" Институт технологий управления 😎 ", callback_data='2')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text=" Институт информационных технологий 😏 ", callback_data='3')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text=" Институт кибербезопасности и цифровых технологий 🤯 ",
                                           callback_data='4')
        keyboard.add(key_4)
        key_5 = types.InlineKeyboardButton(text=" Институт радиоэлектроники и информатики 🥴 ", callback_data='5')
        keyboard.add(key_5)
        key_6 = types.InlineKeyboardButton(text=" Институт тонких химических технологий им. М.В. Ломоносова 🤓",
                                           callback_data='6')
        keyboard.add(key_6)
        key_7 = types.InlineKeyboardButton(text=" Институт искусственного интеллекта 🤫",
                                           callback_data='7')
        keyboard.add(key_7)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        rasp_text = "Какой институт? 📈"
        bot.send_message(call.message.chat.id, text=rasp_text, reply_markup=keyboard)
    elif call.data == "1":
        keyboard = types.InlineKeyboardMarkup()
        key_11 = types.InlineKeyboardButton(text="1 🤪 (Вернадка) ", callback_data='11')
        keyboard.add(key_11)
        key_12 = types.InlineKeyboardButton(text=" 2 😎 (Вернадка) ", callback_data='12')
        keyboard.add(key_12)
        key_13 = types.InlineKeyboardButton(text=" 3 😏 (Вернадка) ", callback_data='13')
        keyboard.add(key_13)
        key_14 = types.InlineKeyboardButton(text=" 4 🤯 (Вернадка) ", callback_data='14')
        keyboard.add(key_14)
        key_111 = types.InlineKeyboardButton(text="1 🤪 (Стромынка) ", callback_data='111')
        keyboard.add(key_111)
        key_122 = types.InlineKeyboardButton(text=" 2 😎 (Стромынка) ", callback_data='122')
        keyboard.add(key_122)
        key_133 = types.InlineKeyboardButton(text=" 3 😏 (Стромынка) ", callback_data='133')
        keyboard.add(key_133)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        rasp4_text = "Какой курс? 📈"
        bot.send_message(call.message.chat.id, text=rasp4_text, reply_markup=keyboard)
    elif call.data == "11":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/0b6/pm7cr2hg5nzrc9kgypyko6cg2l2t2vb5/%D0%98%D0%9F%D0%A2%D0%98%D0%9F_1%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "12":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/6e2/y1hqce8u2m9ro0kt15gncsa3ha8f1yqx/%D0%98%D0%9F%D0%A2%D0%98%D0%9F_2%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "13":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/5a8/546eknrnl4kgayuqpfxn8bardcq9v7aa/%D0%98%D0%9F%D0%A2%D0%98%D0%9F_3%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "14":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/323/mai3nn0i2lwnstypssj6mtx883q85rx6/%D0%98%D0%9F%D0%A2%D0%98%D0%9F_4%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "111":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/d41/it2lyic7g2gezpius04yd2w17ys15teu/%D0%98%D0%9F%D0%A2%D0%98%D0%9F_%D0%A1%D1%82%D1%80%D0%BE%D0%BC%D1%8B%D0%BD%D0%BA%D0%B0%201%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "122":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/fc2/hv2ltlh6oeqiow0m4ka0sn7z026mrb0o/%D0%98%D0%9F%D0%A2%D0%98%D0%9F_%D0%A1%D1%82%D1%80%D0%BE%D0%BC%D1%8B%D0%BD%D0%BA%D0%B0%202%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "133":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/5cc/11zr5jt3p2g9um540zd13qbfz7ro1jkw/%D0%98%D0%9F%D0%A2%D0%98%D0%9F_%D0%A1%D1%82%D1%80%D0%BE%D0%BC%D1%8B%D0%BD%D0%BA%D0%B0%203%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)

    elif call.data == "2":
        keyboard = types.InlineKeyboardMarkup()
        key_21 = types.InlineKeyboardButton(text="1 🤪 (Вернадка) ", callback_data='21')
        keyboard.add(key_21)
        key_22 = types.InlineKeyboardButton(text=" 2 😎 (Вернадка) ", callback_data='22')
        keyboard.add(key_22)
        key_23 = types.InlineKeyboardButton(text=" 3 😏 (Вернадка) ", callback_data='23')
        keyboard.add(key_23)
        key_211 = types.InlineKeyboardButton(text="1 🤪 (Стромынка) ", callback_data='211')
        keyboard.add(key_211)
        key_222 = types.InlineKeyboardButton(text=" 2 😎 (Стромынка) ", callback_data='222')
        keyboard.add(key_222)
        key_233 = types.InlineKeyboardButton(text=" 3 😏 (Стромынка) ", callback_data='233')
        keyboard.add(key_233)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        rasp4_text = "Какой курс? 📈"
        bot.send_message(call.message.chat.id, text=rasp4_text, reply_markup=keyboard)
    elif call.data == "21":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/35e/br00d8kyznyyehxt6b7fmp4a2ntjnkqo/%D0%98%D0%A2%D0%A3_1%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "22":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/b5a/fsffx5iucow86mir0hvau2q7dwuc60n3/%D0%98%D0%A2%D0%A3_2%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "23":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/fa1/g77w2zj0a3dxzp6g2bzxmxa2phy2mzm3/%D0%98%D0%A2%D0%A3_3%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "211":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/115/abh7ag2u041nzb3f6axjbn6exyk9v21g/%D0%98%D0%A2%D0%A3%201%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "222":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/29b/ewewko8opl8lujjkz54ym2rkag0qmsxk/%D0%98%D0%A2%D0%A3%202%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "233":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/637/x8lyvgk4hsf0bg2y0726e8iuuuhc8wbi/%D0%98%D0%A2%D0%A3%203%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)

    elif call.data == "3":
        keyboard = types.InlineKeyboardMarkup()
        key_31 = types.InlineKeyboardButton(text="1 🤪 ", callback_data='31')
        keyboard.add(key_31)
        key_32 = types.InlineKeyboardButton(text=" 2 😎 ", callback_data='32')
        keyboard.add(key_32)
        key_33 = types.InlineKeyboardButton(text=" 3 😏 ", callback_data='33')
        keyboard.add(key_33)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        rasp4_text = "Какой курс? 📈"
        bot.send_message(call.message.chat.id, text=rasp4_text, reply_markup=keyboard)
    elif call.data == "31":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/10f/4hou1bgun6zg3ej93bzi859yct743gsf/%D0%98%D0%98%D0%A2_1%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "32":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/620/1c9mzk3h0ukgyhm8zjpfnywkdtuy24er/%D0%98%D0%98%D0%A2_2%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "33":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/995/km8f4ocqffyf2j42c7mtaq4er2ibk3o7/%D0%98%D0%98%D0%A2_3%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)

    elif call.data == "4":
        keyboard = types.InlineKeyboardMarkup()
        key_41 = types.InlineKeyboardButton(text="1 🤪 ", callback_data='41')
        keyboard.add(key_41)
        key_42 = types.InlineKeyboardButton(text=" 2 😎 ", callback_data='42')
        keyboard.add(key_42)
        key_43 = types.InlineKeyboardButton(text=" 3 😏 ", callback_data='43')
        keyboard.add(key_43)
        key_44 = types.InlineKeyboardButton(text=" 4 🤯 ", callback_data='44')
        keyboard.add(key_44)
        key_45 = types.InlineKeyboardButton(text=" 5 👨🏻‍🦳 ", callback_data='45')
        keyboard.add(key_45)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        rasp4_text = "Какой курс? 📈"
        bot.send_message(call.message.chat.id, text=rasp4_text, reply_markup=keyboard)
    elif call.data == "41":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/025/vuqzbk2ehbqooaplqnqko90rn6s45dh1/%D0%98%D0%9A%D0%91%201%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "42":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/631/vne1ao2r6iu97uz00qgb0figrpfk0cky/%D0%98%D0%9A%D0%91%202%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "43":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/16f/5c30ei4022sf4ba92nsoossxs3tzor25/%D0%98%D0%9A%D0%91%203%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "44":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/953/366mdlpjrt2ui2fcf95n9bi8hr24wbw6/%D0%98%D0%9A%D0%91%204%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "45":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/0fb/miawos4l015jgkof728ohj8fgrf2pmor/%D0%98%D0%9A%D0%91%205%20%D0%BA%D1%83%D1%80%D1%81%202%20%D1%81%D0%B5%D0%BC.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)

    elif call.data == "5":
        keyboard = types.InlineKeyboardMarkup()
        key_51 = types.InlineKeyboardButton(text="1 🤪 ", callback_data='51')
        keyboard.add(key_51)
        key_52 = types.InlineKeyboardButton(text=" 2 😎 ", callback_data='52')
        keyboard.add(key_52)
        key_53 = types.InlineKeyboardButton(text=" 3 😏 ", callback_data='53')
        keyboard.add(key_53)
        key_54 = types.InlineKeyboardButton(text=" 4 🤯 ", callback_data='54')
        keyboard.add(key_54)
        key_55 = types.InlineKeyboardButton(text=" 5 👨🏻‍🦳 ", callback_data='55')
        keyboard.add(key_55)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        rasp4_text = "Какой курс? 📈"
        bot.send_message(call.message.chat.id, text=rasp4_text, reply_markup=keyboard)
    elif call.data == "51":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/2a3/3wapdwax3kt3wifa7ka8ghh66jdeagw6/%D0%98%D0%A0%D0%AD%D0%98_1%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "52":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/65f/0k0oqesr2mtbacxhsecl9qecnvekcrna/%D0%98%D0%A0%D0%AD%D0%98_2%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "53":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/cab/9adgkpsf4cvkbffqf10waqwvhw98ml40/%D0%98%D0%A0%D0%AD%D0%98_3%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "54":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/012/oqabp22tppn6t509gmeu1v6pu0ya47qi/%D0%98%D0%A0%D0%AD%D0%98_4%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "55":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/82b/5u8ai5tpfvcjjd4664sg4393os209bd3/%D0%98%D0%A0%D0%AD%D0%98_5%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)

    elif call.data == "6":
        keyboard = types.InlineKeyboardMarkup()
        key_61 = types.InlineKeyboardButton(text="1 🤪 ", callback_data='61')
        keyboard.add(key_61)
        key_62 = types.InlineKeyboardButton(text=" 2 😎 ", callback_data='62')
        keyboard.add(key_62)
        key_63 = types.InlineKeyboardButton(text=" 3 😏 ", callback_data='63')
        keyboard.add(key_63)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        rasp4_text = "Какой курс? 📈"
        bot.send_message(call.message.chat.id, text=rasp4_text, reply_markup=keyboard)
    elif call.data == "61":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/751/2unplota2uvqnexokd1ivbcis3wtw9bh/%D0%98%D0%A2%D0%A5%D0%A2_%D0%B1%D0%B0%D0%BA_1%D0%BA_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "62":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/067/e8p1m1l7vp8puoty5mryorr014xtxjij/%D0%98%D0%A2%D0%A5%D0%A2_%D0%B1%D0%B0%D0%BA_2%D0%BA_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "63":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/4e0/pb9i0jlv8bp9n8xwwz8a2a8c4mgaxz0e/%D0%98%D0%A2%D0%A5%D0%A2_%D0%B1%D0%B0%D0%BA_3%D0%BA_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)

    elif call.data == "7":
        keyboard = types.InlineKeyboardMarkup()
        key_71 = types.InlineKeyboardButton(text="1 🤪 ", callback_data='71')
        keyboard.add(key_71)
        key_72 = types.InlineKeyboardButton(text=" 2 😎 ", callback_data='72')
        keyboard.add(key_72)
        key_73 = types.InlineKeyboardButton(text=" 3 😏 ", callback_data='73')
        keyboard.add(key_73)
        key_74 = types.InlineKeyboardButton(text=" 4 🤯 ", callback_data='74')
        keyboard.add(key_74)
        key_75 = types.InlineKeyboardButton(text=" 5 👨🏻‍🦳 ", callback_data='75')
        keyboard.add(key_75)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        rasp4_text = "Какой курс? 📈"
        bot.send_message(call.message.chat.id, text=rasp4_text, reply_markup=keyboard)
    elif call.data == "71":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/776/r84ei7psnezs42it5s83xv9vc098y2cc/%D0%98%D0%98%D0%98_1%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "72":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/cac/99baousulysqdy9xwz4sae9zl5d39oke/%D0%98%D0%98%D0%98_2%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "73":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/68b/ri7wmsg0egdypmb8ymo2sdqv90zz0ohs/%D0%98%D0%98%D0%98_3%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "74":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/903/djobrtq0kals2kjdktx8z7vc9varr0vo/%D0%98%D0%98%D0%98_4%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "75":
        bot.send_message(call.from_user.id,
                         text="Ссылка на Exel файл: https://webservices.mirea.ru/upload/iblock/7a7/isvduiiwyz5amriq8d9xr8g5ucc9dl06/%D0%98%D0%98%D0%98_5%20%D0%BA%D1%83%D1%80%D1%81_21-22_%D0%B2%D0%B5%D1%81%D0%BD%D0%B0_%D0%BE%D1%87%D0%BA%D0%B0.xlsx")
        call.data = 's'
        time.sleep(2)
        callback_worker(call)
    elif call.data == "test":
        keyboard = types.InlineKeyboardMarkup()
        key_76 = types.InlineKeyboardButton (text = "Физика", callback_data= '76')
        keyboard.add(key_76)
        key_77 = types.InlineKeyboardButton (text = "Информатика", callback_data= '77')
        keyboard.add(key_77)
        key_78 = types.InlineKeyboardButton (text = "Дизайн", callback_data= '78')
        keyboard.add(key_78)
        key_79 = types.InlineKeyboardButton (text = "Биология и химия", callback_data= '79')
        keyboard.add(key_79)
        key_80 = types.InlineKeyboardButton (text = "Обществознание", callback_data= '80')
        keyboard.add(key_80)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        prof_text = 'Не можешь решить какое направление выбрать? Мы поможем! \n Что тебе интересно изучить?'
        bot.send_message(call.message.chat.id, text=prof_text, reply_markup=keyboard)
    elif call.data == "76":
        keyboard = types.InlineKeyboardMarkup()
        key_81 = types.InlineKeyboardButton(text="Радиоэлектроника!📻", callback_data="81")
        keyboard.add(key_81)
        key_82 = types.InlineKeyboardButton(text="Приборостроение!⚙", callback_data='82')
        keyboard.add(key_82)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        fiz_text = "Какой раздел физики тебя привлекает больше? \n Hа радиотехнике ты будешь принимать участие в разраб" \
                   "отке радиоприборов или даже космической радионавигации 🚀 \n На приборостроении тебя научат произво" \
                   "дственно-технологическим видам практической деятельности и робототехнике 🤖"
        bot.send_message(call.message.chat.id, text=fiz_text, reply_markup=keyboard)
    elif call.data == "81":
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "Тогда тебе подойдут следующие направления 😉 \n 11.03.01 https://vk.cc/cdZy6q \n 11.03.04 https://vk.cc/cdZydR \n 11.05.01 https://vk.cc/cdZyhS \n 12.05.01 https://vk.cc/cdZyud \n 28.03.01 https://vk.cc/cdZywr", reply_markup=keyboard)
    elif call.data == "82":
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id,
                         text="Тогда тебе подойдут следующие направления 😉 \n 11.03.03 https://vk.cc/cdZyHG \n 12.03.01 https://vk.cc/cdZyKR \n 12.03.04 https://vk.cc/cdZyPJ \n 15.03.01 https://vk.cc/cdZyTp \n 15.03.04 https://vk.cc/cdZyYZ \n 15.03.06 https://vk.cc/cdZz1t", reply_markup=keyboard)
    elif call.data == "77":
        keyboard = types.InlineKeyboardMarkup()
        key_83 = types.InlineKeyboardButton(text="Объекто-оринтированое програмирование ", callback_data="83")
        keyboard.add(key_83)
        key_84 = types.InlineKeyboardButton(text="Информационная безопасность", callback_data='84')
        keyboard.add(key_84)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "Готов углубиться в програмирование и проектирование сложных систем?😎 \n На какой стороне ты? ПРограмирование для эксплуатации сложных систем и сетевого обеспечения? \n Или ты хочешь стоять на страже информационного порядка?", reply_markup=keyboard)
    elif call.data == "83":
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "Тогда рассмотри эти направления 😉 \n 01.03.02 https://vk.cc/cdZz8q \n 01.03.04 https://vk.cc/cdZzaF \n 01.03.05 https://vk.cc/cdZze1 \n 02.03.02 https://vk.cc/cdZzfo \n 05.03.03 https://vk.cc/cdZziU \n 09.03.01 https://vk.cc/cdZzlP \n 09.03.02 https://vk.cc/cdZzox \n 11.03.02 https://vk.cc/cdZzrw \n 27.03.03 https://vk.cc/cdZzvV",reply_markup=keyboard)
    elif call.data == "84":
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "Тебе стоит рассотреть такие направления 😉 \n 10.03.01 https://vk.cc/cdZzBq \n 10.05.01 https://vk.cc/cdZzIe \n 10.05.02 https://vk.cc/cdZzKh \n 10.05.03 https://vk.cc/cdZzMm \n 10.05.04 https://vk.cc/cdZzOv \n 10.05.05 https://vk.cc/cdZzSh  ", reply_markup=keyboard)
    elif call.data == "78":
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "Ну наконец-то у нас будет красивая визуалзация проектов 👾 \n 29.03.04 https://vk.cc/cdZzXO \n 54.03.01 https://vk.cc/cdZzZk" ,reply_markup=keyboard)
    elif call.data == "79":
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "О! ИТХТ им. М.В. Ломоносова нуждается в тебе! \n 04.03.01 https://vk.cc/cdZA22 \n 18.03.01 https://vk.cc/cdZA5d \n 19.03.01 https://vk.cc/cdZAa2 \n 20.03.01 https://vk.cc/cdZAcJ \n 22.03.01 https://vk.cc/cdZAg3", reply_markup=keyboard)
    elif call.data == "80":
        keyboard = types.InlineKeyboardMarkup()
        key_85 = types.InlineKeyboardButton (text = "Хочу управлять!", callback_data= "85")
        keyboard.add(key_85)
        key_86 = types.InlineKeyboardButton(text = "Право и юриспруденция!", callback_data="86")
        keyboard.add(key_86)
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "Что тебе по душе - право и юриспруденция или управление и экономика?" ,reply_markup=keyboard)
    elif call.data == "85":
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "Ну держи, депутат 💼 \n 27.03.01 https://vk.cc/cdZAnc \n 27.03.05 https://vk.cc/cdZApv \n 38.03.01 https://vk.cc/cdZAsn \n 38.03.02 https://vk.cc/cdZAvj \n 38.03.03 https://vk.cc/cdZAzk \n 38.03.04 https://vk.cc/cdZAD8 \n 38.03.05 https://vk.cc/cdZAGt \n 38.05.01 https://vk.cc/cdZAK4 \n 46.03.02 https://vk.cc/cdZAMC \n 38.03.10 https://vk.cc/cdZAPI ",reply_markup= keyboard)
    elif call.data == "86":
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text="Назад ⏮", callback_data='back')
        keyboard.add(key_back)
        bot.send_message(call.message.chat.id, text= "Эти направления просто созданы для тебя ⚖ \n 40.03.01 https://vk.cc/cdZAVi \n 40.05.01 https://vk.cc/cdZAXH",reply_markup = keyboard)


bot.polling()