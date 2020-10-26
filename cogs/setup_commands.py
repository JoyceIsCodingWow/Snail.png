import discord
from discord.ext import commands
from discord.ext.commands import Bot
import sqlite3

class setup_commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True)
	@commands.is_owner()
	async def setup(self, ctx):
		hi = discord.Embed(color=0xadd8e6)
		hi.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
		hi.add_field(name='s!setup modlog', value='Set the channel to send bans, kicks, warnings, etc. to.', inline=True)
		hi.add_field(name='s!setup messagelog', value='Set the channel to send message edits and deleted messages to.')
		hi.add_field(name='s!setup welcome', value='Set the channel to send welcome messages to.')
		hi.add_field(name='s!setup list', value='Shows the channels that are already set up.')
		await ctx.send(embed=hi)

	@setup.command()
	@commands.is_owner()
	async def modlog(self, ctx, channel: discord.TextChannel):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT modlog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO snail(guild_id, modlog_channel) VALUES(?, ?)")
			val = (ctx.guild.id, channel.id)
			await ctx.send(f"{channel.mention} Has been set as the mod-log channel.")
		elif result is not None:
			sql = ("UPDATE snail SET modlog_channel = ? WHERE guild_id = ?")
			val = (channel.id, ctx.guild.id)
			await ctx.send(f"{channel.mention} Has been set as the mod-log channel.")
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

	@setup.command()
	@commands.is_owner()
	async def messagelog(self, ctx, channel: discord.TextChannel):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT messagelog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO snail(guild_id, messagelog_channel) VALUES(?, ?)")
			val = (ctx.guild.id, channel.id)
			await ctx.send(f"{channel.mention} Has been set as the message-log channel.")
		elif result is not None:
			sql = ("UPDATE snail SET messagelog_channel = ? WHERE guild_id = ?")
			val = (channel.id, ctx.guild.id)
			await ctx.send(f"{channel.mention} Has been set as the message-log channel.")
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

	@setup.command()
	@commands.is_owner()
	async def welcome(self, ctx, channel: discord.TextChannel):
		await ctx.send(f"{channel.mention} Has been set as the welcome message channel.")

	@setup.command()
	@commands.is_owner()
	async def muterole(self, ctx, role: discord.Role):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT muterole FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result is None:
			sql = ("INSERT INTO snail(guild_id, muterole) VALUES(?, ?)")
			val = (ctx.guild.id, role.id)
			await ctx.send(f"**{role}** Has been added as this servers mute role.")
		elif result is not None:
			sql = ("UPDATE snail SET muterole = ? WHERE guild_id = ?")
			val = (role.id, ctx.guild.id)
			await (f"**{role}** Has been updated as the servers mute role")
		cursor.execute(sql, val)
		db.commit()
		cursor.close()
		db.close()

	@setup.command()
	@commands.is_owner()
	async def list(self, ctx):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT modlog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		if result == None:
			result = "Not set up yet"
		if result != None:
			result = f"<#{int(result[0])}>"
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT messagelog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result1 = cursor.fetchone()
		if result1 == None:
			result1 = "Not set up yet"
		if result1 != None:
			result1 = f"<#{int(result1[0])}>"
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT welcome_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result2 = cursor.fetchone()
		if result2 != None:
			result2 = f"<#{int(result2[0])}>"
		if result2 == None:
			result2 = "Not set up yet"
		embed = discord.Embed(color=0xadd8e6)
		embed.add_field(name='Mod-log channel', value=f"{result}")
		embed.add_field(name='Message-log channel', value=f"{result1}")
		embed.add_field(name='Welcome channel', value=f"{result2}")
		await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(setup_commands(bot))