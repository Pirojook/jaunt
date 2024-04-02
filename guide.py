import telebot
from telebot import *
from telebot.types import InputMediaPhoto

from django.conf import settings
import os
from bot.models import *

TOKEN = "6674653580:AAFtXjJ1C5QmQKT9GbUgdwtV5z_kybua8Lw"
bot = telebot.TeleBot(TOKEN)
group_id = -1002014979375

def guide_name(message):
    global user_id
    user_id = message.from_user.id
    user_profile = Users.objects.get(user_id=user_id)
    language_code = user_profile.language
    global language_entry
    language_entry = language.objects.filter(language_code=language_code).first()
    global name
    name = message.text
    bot.send_message(user_id, language_entry.guide_price)
    bot.register_next_step_handler(message, guide_price)

def guide_price(message):
    global user_id
    user_id = message.from_user.id
    user_profile = Users.objects.get(user_id=user_id)
    language_code = user_profile.language
    global language_entry
    language_entry = language.objects.filter(language_code=language_code).first()
    global price
    price = message.text
    bot.send_message(user_id, language_entry.guide_language)
    bot.register_next_step_handler(message, guide_language)

def guide_language(message):
    global language
    language = message.text
    bot.send_message(user_id, language_entry.guide_durability)
    bot.register_next_step_handler(message, guide_durability)

def guide_durability(message):
    global durability
    durability = message.text
    bot.send_message(user_id, language_entry.guide_number)
    bot.register_next_step_handler(message, guide_number)

def guide_number(message):
    global number
    number = message.text.strip()
    if re.match(r'^\+998\d{9}$', number) and len(number) == 13:
        bot.send_message(user_id, language_entry.guide_license)
        bot.register_next_step_handler(message, guide_license)
    else:
        bot.send_message(user_id, language_entry.guide_number)
        bot.register_next_step_handler(message, guide_number)
def guide_license(message):
    global file_path_license
    global  downloaded_license
    license = message.photo[-1].file_id
    file_info = bot.get_file(license)
    file_path_license = file_info.file_path
    downloaded_license = bot.download_file(file_path_license)
    file_name = os.path.join(settings.MEDIA_ROOT, file_path_license)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_license)
    bot.send_message(user_id, language_entry.guide_photo)
    bot.register_next_step_handler(message, guide_photo)

def guide_photo(message):
    if language_entry:
        photo = message.photo[-1].file_id
        file_info = bot.get_file(photo)
        file_path_photo = file_info.file_path
        downloaded_photo = bot.download_file(file_path_photo)
        file_name = os.path.join(settings.MEDIA_ROOT, file_path_photo)
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_photo)

        bot.send_message(user_id, "Nice")
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

def ad_id_():
    return ad_id