# Импортируем библиотеки и подключаем классы:
import requests
import telebot
import googletrans
from googletrans import Translator
from telebot import types
from classes import Cats, Numbers

# Создаем экземпляры классов:
cats = Cats(f'https://http.cat')
fakt = Numbers(url='http://numbersapi.com')
tr = Translator()

bot = telebot.TeleBot('5900277611:AAEQrtexi_iwAKeQ-vPDbQIIuXiVkxcrnhY') # токен бота

# Список кодов ошибок, доступных на сайте с API:
error_codes = [100, 101, 102, 103, 200, 201, 202, 203, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308,
400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 420, 421, 422, 423, 424, 425, 426, 429, 431, 444, 450, 451, 497, 498, 499,
500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 521, 522, 523, 525, 599]

@bot.message_handler(commands=['start', 'help']) # реакция бота на команды start, help
def start(message):
  first_message = f"<b>{message.from_user.first_name}</b>, привет!\nЭтот бот присылает фото котиков на любой код ответа сервера. Введи, пожалуйста, код (например, 502 или 301):"
  msg = bot.send_message(message.chat.id, first_message, parse_mode='html') # выводим сообщение-привествие и запрос ввода данных
  bot.register_next_step_handler(msg, response) # записываем введённые данные в переменную msg, response - функция от этой переменной, вызывается далее

@bot.message_handler(content_types=['text']) # реакция бота на введённое сообщение
def response(msg):
  s = msg.text # записываем ответ пользователя в переменную s
  if s.isdigit(): # проверяем, является ли числом
    if int(msg.text) in error_codes: # проверяем, есть ли в списке кодов с ошибками
      url = str(cats.get_cat_url(msg.text)) # получаем нужный url картинки
      bot.send_photo(msg.chat.id, url)  # отправляем картинку в чат
    else:
      error_message = f'Пожалуйста, введи корректный код ошибки или ответа сервера.\nОбычно это числа в промежутках: 100-103, 200-207, 300-308, 400-499, 500-599.\nНапример, 404 или 200.\n\nИнтересный факт о числе {s}:\n'
      fakt_str = str(fakt.get_fact(int(s))) # приводим к строке факт о числе, если его нет в списке кодов ответа
      error_message_rus = tr.translate(fakt_str, dest = 'ru').text # переведённый на русский язык факт
      error_message = error_message + error_message_rus  # добавляем к сообщению об ошибке факт о числе
      bot.send_message(msg.chat.id, error_message, parse_mode='html') # выводим сообщение об ошибке и факт
  else:
    error_message = 'Вы ввели не число. Введите, пожалуйста, число.'
    bot.send_message(msg.chat.id, error_message, parse_mode='html') # выводим сообщение об ошибке


bot.infinity_polling(none_stop=True, interval=0) # бот постоянно "слушает" ввод от пользователя