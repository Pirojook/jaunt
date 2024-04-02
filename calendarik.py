import telebot
from telebot import types
import datetime
import calendar
import os
from bot.models import *

# Словарь для хранения выбранных дат
selected_dates = {}

# Текущая дата
current_date = datetime.date.today()

# Текущий месяц
current_month = current_date.month

def create_calendar(year, month, user_id):
    user_profile = Users.objects.get(user_id=user_id)
    language_code = user_profile.language
    language_entry = language.objects.filter(language_code=language_code).first()
    months_ru = language_entry.months
    days_ru = language_entry.days
    markup = types.InlineKeyboardMarkup()
    month_days = calendar.monthrange(year, month)[1]
    month_start = datetime.date(year, month, 1)
    week_day = month_start.weekday()

    # Добавление названия текущего месяца на русском
    markup.row(types.InlineKeyboardButton(text=months_ru[month - 1], callback_data="ignore"))

    # Добавление названий дней недели на русском
    markup.row(*[types.InlineKeyboardButton(text=day, callback_data="ignore") for day in days_ru])

    for i in range(6):
        row = []
        for j in range(7):
            day_number = i * 7 + j + 1 - week_day
            if day_number < 1 or day_number > month_days or datetime.date(year, month, day_number) < current_date:
                row.append(types.InlineKeyboardButton(text=" ", callback_data="ignore"))
            else:
                date = datetime.date(year, month, day_number)
                callback_data = f"{year}-{month:02d}-{day_number:02d}"
                row.append(types.InlineKeyboardButton(text=str(day_number), callback_data=callback_data))
        markup.row(*row)

    # Добавление кнопок для перемещения к предыдущему и следующему месяцу
    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    markup.row(
        types.InlineKeyboardButton(text=f"◀️ {months_ru[prev_month - 1]}", callback_data=f"prev_{year}_{prev_month}"),
        types.InlineKeyboardButton(text=f"{months_ru[next_month - 1]} ▶️", callback_data=f"next_{year}_{next_month}"))

    return markup
