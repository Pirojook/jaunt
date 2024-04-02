import telebot
import sqlite3
from sqlite3 import *
from telebot import *
from telebot.types import InputMediaPhoto
from db import Database
from django.conf import settings
from django.core.management.base import BaseCommand
import os
import re
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jaunt.settings')
import django
django.setup()
from bot.models import *
import datetime
from calendarik import *
if not settings.configured:
    settings.configure()
bot_settings = BotSettings.objects.first()
if not bot_settings:
    print("The bot's running")
db = Database('db.sqlite3')
TOKEN = "6674653580:AAFtXjJ1C5QmQKT9GbUgdwtV5z_kybua8Lw"
bot = telebot.TeleBot(TOKEN)
group_id = -1002014979375
admins = [1274853032]
path_to_file = "/home/jaunt/media/media"

@bot.message_handler(commands=['start'])
def handle_message(message):
    global user_id
    global user_profile
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    user_profile = Users.objects.filter(user_id=user_id).first()
    global menu
    def menu(language_entry):
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        find_tour = types.KeyboardButton(language_entry.find_tour)
        imguider = types.KeyboardButton(language_entry.imguider)
        contact_menu = types.KeyboardButton(language_entry.contact_menu)
        menu.add(find_tour, imguider, contact_menu)
        bot.send_message(message.chat.id, language_entry.text_welcome, reply_markup=menu)
    if user_profile is None:
        Users.objects.create(
            user_id=user_id,
            first_name = first_name,
            username = username,
        )
        keylan = types.InlineKeyboardMarkup()
        it1 = types.InlineKeyboardButton(text="Русский", callback_data="ru")
        it2 = types.InlineKeyboardButton(text="English", callback_data="en")
        keylan.add(it1, it2)
        bot.send_message(message.chat.id, "Выберите язык:\nSelect language:", reply_markup=keylan)
    else:
        user_profile = Users.objects.get(user_id=user_id)
        language_code = user_profile.language
        global language_entry
        language_entry = language.objects.filter(language_code=language_code).first()
        if language_entry:
            menu(language_entry)

@bot.message_handler(content_types=['text', 'photo'])
def lala(message):
    if language_entry:
        if message.text == language_entry.find_tour:
            markup = create_calendar(current_date.year, current_date.month, user_id)
            bot.send_message(message.chat.id, language_entry.choose_day, reply_markup=markup)

        elif message.text == language_entry.contact_menu:
            bot.send_message(message.chat.id, language_entry.contact_text)
            bot.register_next_step_handler(message, forward_to_moderators)

        elif message.text == language_entry.imguider:
            def guide_name(message):
                if message.text == language_entry.back:
                    menu(language_entry)
                if message.text and message.text != language_entry.back:
                    global name
                    name = message.text
                    bot.send_message(user_id, language_entry.guide_price, reply_markup=back)
                    bot.register_next_step_handler(message, guide_price)
                elif message.photo:
                    bot.send_message(message.chat.id, language_entry.guide_name, reply_markup=back)
                    bot.register_next_step_handler(message, guide_name)

            global back
            back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            bback = types.KeyboardButton(language_entry.back)
            back.add(bback)
            bot.send_message(message.chat.id, language_entry.guide_name, reply_markup=back)
            bot.register_next_step_handler(message, guide_name)
        elif message.chat.id == group_id:
            if message.from_user.id in admins:
                bot.send_message(id, message.text)

        def guide_price(message):
            if message.text == language_entry.back:
                menu(language_entry)
            if message.text and message.text != language_entry.back:
                global price
                price = message.text.strip()
                if re.match(r'^[0-9]+$', price):
                    bot.send_message(user_id, language_entry.guide_language, reply_markup=back)
                    bot.register_next_step_handler(message, guide_language)
                else:
                    bot.send_message(user_id, language_entry.guide_price, reply_markup=back)
                    bot.register_next_step_handler(message, guide_price)
            elif message.photo:
                bot.send_message(user_id, language_entry.guide_price, reply_markup=back)
                bot.register_next_step_handler(message, guide_price)

        def guide_language(message):
            if message.text == language_entry.back:
                menu(language_entry)
            if message.text and message.text != language_entry.back:
                global language
                language = message.text
                bot.send_message(user_id, language_entry.guide_durability, reply_markup=back)
                bot.register_next_step_handler(message, guide_durability)
            elif message.photo:
                bot.send_message(user_id, language_entry.guide_language, reply_markup=back)
                bot.register_next_step_handler(message, guide_language)

        def guide_durability(message):
            if message.text == language_entry.back:
                menu(language_entry)
            if message.text and message.text != language_entry.back:
                global durability
                durability = message.text
                bot.send_message(user_id, language_entry.guide_number, reply_markup=create_keyboard())
                bot.register_next_step_handler(message, guide_number)
            if message.photo:
                bot.send_message(user_id, language_entry.guide_durability, reply_markup=back)
                bot.register_next_step_handler(message, guide_durability)

        def guide_number(message):
            if message.text == language_entry.back:
                menu(language_entry)
            if message.text and message.text != language_entry.back:
                global number
                number = message.text.strip()
                if re.match(r'^\+998\d{9}$', number) and len(number) == 13:
                    bot.send_message(user_id, language_entry.guide_license, reply_markup=back)
                    bot.register_next_step_handler(message, guide_license)
                else:
                    bot.send_message(user_id, language_entry.guide_number, reply_markup=create_keyboard())
                    bot.register_next_step_handler(message, guide_number)
            elif message.contact:
                contact = message.contact
                number = f"{contact.phone_number}"
                bot.send_message(user_id, language_entry.guide_license, reply_markup=back)
                bot.register_next_step_handler(message, guide_license)
            elif message.photo:
                bot.send_message(user_id, language_entry.guide_number, reply_markup=create_keyboard())
                bot.register_next_step_handler(message, guide_number)

        def create_keyboard():
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
            share = telebot.types.KeyboardButton(text=language_entry.share_contant, request_contact=True)
            bback = types.KeyboardButton(language_entry.back)
            keyboard.add(share, bback)
            return keyboard

        def guide_license(message):
            if message.photo:
                global file_path_license
                global  downloaded_license
                license = message.photo[-1].file_id
                file_info = bot.get_file(license)
                file_path_license = file_info.file_path
                downloaded_license = bot.download_file(file_path_license)
                file_name = os.path.join(settings.MEDIA_ROOT, file_path_license)
                with open(file_name, 'wb') as new_file:
                    new_file.write(downloaded_license)
                bot.send_message(user_id, language_entry.guide_photo, reply_markup=back)
                bot.register_next_step_handler(message, guide_photo)
            if message.text and message.text != language_entry.back:
                bot.send_message(user_id, language_entry.guide_license, reply_markup=back)
                bot.register_next_step_handler(message, guide_license)
            elif message.text == language_entry.back:
                menu(language_entry)
        def guide_photo(message):
            if language_entry:
                if message.photo:
                    photo = message.photo[-1].file_id
                    file_info = bot.get_file(photo)
                    file_path_photo = file_info.file_path
                    downloaded_photo = bot.download_file(file_path_photo)

                    file_name = os.path.join(settings.MEDIA_ROOT, file_path_photo)

                    with open(file_name, 'wb') as new_file:
                        new_file.write(downloaded_photo)
                    menu(language_entry)

                    ad = guide.objects.create(id_guide=user_id,
                                              name=name,
                                              price=price,
                                              language=language,
                                              durability=durability,
                                              number=number,
                                              license=file_path_license,
                                              photo=file_path_photo)
                    global ad_id
                    ad_id = ad.id
                    ad_text = language_entry.ad.format(
                        name=name,
                        durability=durability,
                        price=price,
                        language=language,
                        number=number,
                    )
                    ad_text = ad_text.replace('\\n', '\n')
                    photok = InputMediaPhoto(media=downloaded_photo, caption=ad_text)
                    licens = InputMediaPhoto(media=downloaded_license, caption=ad_text)
                    bot.send_media_group(group_id, [photok, licens])

                    accept_menu = types.InlineKeyboardMarkup()
                    accept = types.InlineKeyboardButton(text="Опубликовать", callback_data="accept")
                    reject = types.InlineKeyboardButton(text="Отмена", callback_data="deny")
                    accept_menu.add(accept, reject)
                    bot.send_message(group_id, ad_text, reply_markup=accept_menu)

                if message.text and message.text != language_entry.back:
                    bot.send_message(user_id, language_entry.guide_photo)
                    bot.register_next_step_handler(message, guide_photo)

                elif message.text == language_entry.back:
                    menu(language_entry)
def forward_to_moderators(message):
    global id
    id = message.from_user.id
    if message.photo and not message.text:
        photo_id = message.photo[-1].file_id
        caption = message.caption if message.caption else "Фото без комментария"
        forwarded_message = f"Фото от пользователя @{message.from_user.username}\nid: {id}\n\n"
        bot.send_photo(group_id, photo_id, caption=forwarded_message+caption)
        bot.reply_to(message, "Ваше фото успешно отправлено модераторам.")
    elif message.text:
        forwarded_message = f"Пользователь @{message.from_user.username} id: {id} написал:\n\n{message.text}"
        bot.send_message(group_id, forwarded_message)
        bot.reply_to(message, "Ваше сообщение успешно отправлено модераторам.")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        def call_menu(language_entry):
            menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            find_tour = types.KeyboardButton(language_entry.find_tour)
            imguider = types.KeyboardButton(language_entry.imguider)
            contact_menu = types.KeyboardButton(language_entry.contact_menu)
            menu.add(find_tour, imguider, contact_menu)
            bot.send_message(call.message.chat.id, language_entry.text_welcome, reply_markup=menu)
        if call.data == "ru":
            db.lang_ru(user_id)
            user_profile = Users.objects.get(user_id=user_id)
            language_code = user_profile.language
            language_entry = language.objects.filter(language_code=language_code).first()
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            call_menu(language_entry)
        elif call.data == "en":
            db.lang_en(user_id)
            user_profile = Users.objects.get(user_id=user_id)
            language_code = user_profile.language
            language_entry = language.objects.filter(language_code=language_code).first()
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            call_menu(language_entry)
        elif call.data == "accept":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            db.is_guide(ad_id)
        elif call.data == "deny":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            db.del_guide(ad_id)

    data = call.data.split('_')
    if len(data) == 3 and data[0] == 'prev':
        year, month = map(int, data[1:])
        current_month = month
        markup = create_calendar(year, month, user_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите дату:", reply_markup=markup)
    elif len(data) == 3 and data[0] == 'next':
        year, month = map(int, data[1:])
        current_month = month
        markup = create_calendar(year, month, user_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите дату:", reply_markup=markup)
    else:
        selected_date = call.data
        db.all_guiders(user_id)


bot.polling(none_stop=True)