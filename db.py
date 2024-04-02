import sqlite3
import telebot
import os
from pathlib import Path
from django.conf import settings
from PIL import Image
bot = telebot.TeleBot("6674653580:AAFtXjJ1C5QmQKT9GbUgdwtV5z_kybua8Lw")
BASE_DIR = Path(__file__).resolve().parent.parent
class Database:
	def __init__(self, db_file):
		self.connection = sqlite3.connect(db_file, check_same_thread=False)
		self.cursor = self.connection.cursor()

	def lang_ru(self, user_id):
		with self.connection:
			return self.cursor.execute("UPDATE bot_users SET language = ? WHERE user_id = ?",
									   ("Русский", user_id))

	def lang_en(self, user_id):
		with self.connection:
			return self.cursor.execute("UPDATE bot_users SET language = ? WHERE user_id = ?",
									   ("English", user_id))

	def is_guide(self, id):
		with self.connection:
			return self.cursor.execute("UPDATE bot_guide SET is_guide=1 WHERE id=?",
									   (id,))

	def del_guide(self, id):
		with self.connection:
			return self.cursor.execute("DELETE FROM bot_guide WHERE id=?",
									   (id,))

	def all_guiders(self, user_id):
		with self.connection:
			self.cursor.execute("SELECT * FROM bot_guide WHERE is_guide = 1")
			rows = self.cursor.fetchall()
			for row in rows:
				data_list = list(row)[1:-4]
				name, language, price, durability,  number = data_list
				message = "Имя: {name}\nЯзык: {language}\nЦена: ${price}\nПродолжительность: {durability} часов\nНомер: {number}".format(
					name=name, durability=durability, price=price, language=language, number=number)

				lol = row[-1].replace("/", "\\")
				photo_path = os.path.join(settings.MEDIA_ROOT, lol)
				with open(photo_path, 'rb') as photo:
					bot.send_photo(user_id, photo, caption=message)
