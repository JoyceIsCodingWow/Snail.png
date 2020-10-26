import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
import sqlite3

now = datetime.now()

class mod_events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	@commands.Cog.listener()
	async def on_member_join(self, member):
		if memeber.guild.id != 724360414829215766:
			return
		channel = self.bot.get_channel(766835252651884544)
		channel.send(f"hiiiiiii {member.mention}")

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild != None:
			return
		if message.author == self.bot.user:
			return
		user = message.author.name
		user_discrim = message.author.discriminator
		user_avatar = message.author.avatar_url
		channel = self.bot.get_channel(767970704393371698)
		content = message.content
		sent_at = message.created_at.strftime("%b %d, %Y")
		embedVar = discord.Embed()
		embedVar.set_author(name=user + ('#') +user_discrim, icon_url=user_avatar)
		embedVar.add_field(name=sent_at, value=content)
		await channel.send(embed=embedVar)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		message = after
		if message.author == self.bot.user:
			return
		if message.guild.id == None:
			return
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT messagelog_channel FROM snail WHERE guild_id = {message.guild.id}")
		result = cursor.fetchone()
		if result is None:
			return
		else:
			time = now.strftime("%m/%d/%y, %H:%M")
			embedSex = discord.Embed(title='Message link', description=f"{message.author.mention} Edited a message in {message.channel.mention}", url=f"https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",  color=0xFF0000)
			embedSex.set_footer(text=f"Author ID: {message.author.id} │ Edited At {time}")
			embedSex.set_author(name=message.author, icon_url=message.author.avatar_url)
			embedSex.add_field(name='Message before:', value=before.content, inline=False)
			embedSex.add_field(name='Message after:', value=after.content, inline=False)
			channel = self.bot.get_channel(id=int(result[0]))
			await channel.send(embed=embedSex)

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.guild.id == None:
			return
		if message.author == self.bot.user:
			return
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT messagelog_channel FROM snail WHERE guild_id = {message.guild.id}")
		result = cursor.fetchone()
		if result is None:
			return
		else:
			content = message.content
			time = now.strftime("%m/%d/%y, %H:%M")
			embedHi = discord.Embed( description=f"{message.author.mention} deleted a message in {message.channel.mention}", color=0xFF0000)
			embedHi.set_author(name=message.author, icon_url=message.author.avatar_url)
			embedHi.set_footer(text=f"author ID: {message.author.id} │ message ID: {message.id} │")
			embedHi.add_field(name=f"Message deleted at {time}", value=content, inline=False)
			channel = self.bot.get_channel(id=int(result[0]))
			await channel.send(embed=embedHi)

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		channel = self.bot.get_channel(764986104281169940)
		await channel.send(f"<@453271030543155210> snail has joined **{guild.name}**")

def setup(bot):
    bot.add_cog(mod_events(bot))