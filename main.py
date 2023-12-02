import discord
import datetime
import pytz
from pytz import timezone
from discord.utils import get
from discord.ext import commands, tasks
from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageOps
from io import BytesIO
import io
import requests


class eternity(commands.Bot):
	def __init__(self):
		intents = discord.Intents.all()
		intents.message_content = True
		super().__init__(intents=intents)

	async def on_ready(self):

		print(f'Бот активирован! \n' \
			  f'Название бота: {bot.user.name} \n' \
			  f'Айди бота: {bot.user.id} \n' \
			  ''
			  )

		self.banner_update.start()
		bot.remove_command('help')

	@tasks.loop(seconds=15)
	async def banner_update(self):
		print("Запущен цикл обновления баннера")
		# получаем время, которое было 2 часа назад
		two_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=2)


		time1 = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
		timeout = time1.strftime('%H:%M')
		print("Получаем время")

		# создаем словарь для хранения количества сообщений каждого участника
		message_count = {}
		# перебираем все текстовые каналы на сервере
		guild = bot.get_guild(1111380919299874869)#УКАЖИ ID СВОЕГО СЕРВЕРА
		for channel in guild.text_channels:
			# перебираем все сообщения в канале, опубликованные за последние 2 часа
			async for message in channel.history(after=two_hours_ago):
				# проверяем, что сообщение было отправлено участником сервера
				members = guild.members
				if message.author in members and not message.author.bot:
					# увеличиваем количество сообщений для данного участника
					if message.author in message_count:
						message_count[message.author] += 1
					else:
						message_count[message.author] = 1
		print("Обработка сообщений закончена")
		try:
			most_active_member = max(message_count, key=message_count.get)

			activity = most_active_member.activity

			self.guild = self.get_guild(1111380919299874869)#УКАЖИ ID СВОЕГО СЕРВЕРА
			voice_users = sum(len(vc.members) for vc in self.guild.voice_channels)
			mbrs = self.guild.members
			server_members = len(self.guild.members)
			banner = Image.open("BannerLite.png")

			draw = ImageDraw.Draw(banner)

			font = ImageFont.truetype("status.ttf", size=96)
			if activity != None:
				font = ImageFont.truetype("status.ttf", size=64)
				draw.text((615, 777), f"{activity.name}"[:20], font=font, fill="grey")
			else:
				font = ImageFont.truetype("status.ttf", size=64)
				draw.text((615, 777), "Статус не задан", font=font, fill="grey")

			if voice_users < 10:
				font = ImageFont.truetype("ofont.ru_Montserrat.ttf", size=107)
				draw.text((1608, 807), f"{voice_users}", font=font, fill="white")
			else:
				font = ImageFont.truetype("ofont.ru_Montserrat.ttf", size=80)
				draw.text((2568, 2750), f"{voice_users}", font=font, fill="white")

			font = ImageFont.truetype("name.ttf", size=96)
			draw.text((615, 684), f'{most_active_member.name}'[:20], fill='white', font=font)

			font = ImageFont.truetype("name.ttf", size=65)
			draw.text((1364, 150), f'{timeout}', fill='white', font=font)

			url = str(most_active_member.display_avatar.url)[:-10]

			response = requests.get(url, stream=True)
			response = Image.open(io.BytesIO(response.content))
			response = response.convert('RGBA')

			# Обрезка изображения до круга
			response = ImageOps.fit(response, (320, 320), method=Image.LANCZOS, centering=(0.5, 0.5))
			mask = Image.new('L', (320, 320), 0)
			draw = ImageDraw.Draw(mask)
			draw.ellipse((0, 0, 320, 320), fill=255)
			response.putalpha(mask)
			# Вставка измененного изображения
			banner.paste(response, (227, 601), response)
			print("Баннер изменён")
			with BytesIO() as ImageBinary:
				banner.save(ImageBinary, "png")
				ImageBinary.seek(0)
				await self.guild.edit(banner=ImageBinary.read())
		except:
			pass


bot = eternity()

token = ''
bot.run(token)