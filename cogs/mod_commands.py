import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime
import asyncio
import math
import sqlite3


now = datetime.now()

class mod_commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member: discord.Member, *, reason=None):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT modlog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()

		modlogchannel = self.bot.get_channel(id=int(result[0]))
		time = now.strftime("%m/%d/%y, %H:%M")

		if member == None:
			await ctx.send('You need to mention a user for this command to work.')
			return
		if member == ctx.message.author:
			await ctx.send('You cannot ban yourself')
			return
		if reason == None:
			reason = "Unspecified"

		embedVar = discord.Embed(color=0xFF0000)
		embedVar.set_author(name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
		embedVar.set_footer(text=f"Banned at: {time}")
		embedVar.set_thumbnail(url=member.avatar_url)
		embedVar.add_field(name=f"Banned:", value=f"{member} (ID={member.id})")
		embedVar.add_field(name='Reason:', value=reason, inline=False)

		await member.send(f"You have been banned from {ctx.guild.name} for {reason}")
		await member.ban(reason = reason)
		if result == None:
			await ctx.send(embed=embedVar)
		if result != None:
			await ctx.send(embed=embedVar)
			await modlogchannel.send(embed=embedVar)

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, id: int, reason=None):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT modlog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()

		modlogchannel = self.bot.get_channel(id=int(result[0]))
		time = now.strftime("%m/%d/%y, %H:%M")

		user = await self.bot.fetch_user(id)
		if reason == None:
			reason = "Unspecified"
		if user == None:
			await ctx.send('You need to specify a member for this to work')

		embedBingus = discord.Embed(color=0x008000)
		embedBingus.set_author(name=f"{ctx.author} ({ctx.author.id}", icon_url=ctx.author.avatar_url)
		embedBingus.set_thumbnail(url=user.avatar_url)
		embedBingus.set_footer(text=f"Unbanned at: {time}")
		embedBingus.add_field(name=f"Unbanned:", value=f"{user} (ID={user.id})", inline=False)
		embedBingus.add_field(name='Reason:', value=f"{reason}", inline=False)

		await ctx.guild.unban(user)
		if result == None:
			await ctx.send(embed=embedBingus)
		if result != None:
			await ctx.send(embed=embedBingus)
			await modlogchannel.send(embed=embedBingus)

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, *, reason=None):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT modlog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()

		modlogchannel = self.bot.get_channel(id=int(result[0]))
		time = now.strftime("%m/%d/%y, %H:%M")

		if member == None:
			await ctx.send('You need to memtion a user for this command to work.')
			return
		if member == ctx.message.author:
			await ctx.send('You cannot kick yourself.')
			return
		if reason == None:
			reason == "Unspecified"

		embedVar = discord.Embed(color=0xFFFF00)
		embedVar.set_author(name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
		embedVar.set_thumbnail(url=member.avatar_url)
		embedVar.set_footer(text=f"Kicked at: {time}")
		embedVar.add_field(name=f"Kicked: ", value=f"{member} (ID={member.id})")
		embedVar.add_field(name='Reason:', value=f"{reason}", inline=False)

		await member.kick(reason = reason)
		if result == None:
			await ctx.send(embed=embedVar)
		if result != None:
			await ctx.send(embed=embedVar)
			await modlogchannel.send(embed=embedVar)
		await member.send(f"You have been kicked from {ctx.guild.name} for {reason}")

	@commands.command(aliases=['clear', 'clean'])
	@commands.guild_only()
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, limit: int):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT messagelog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()
		messagelogchannel = self.bot.get_channel(id=int(result[0]))

		limit1 = limit + 1
		time = now.strftime("%m/%d/%y, %H:%M")

		embed = discord.Embed(color=0xFF0000)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"{limit} messages purged by {ctx.author} in {ctx.channel}", value=f"Purged at {time}")

		await ctx.channel.purge(limit=limit1)
		if result == None:
			await ctx.send(f'Purged {limit} messages.')
		if result != None:
			await ctx.send(f'Purged {limit} messages.')
			await messagelogchannel.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(manage_channels=True)
	async def lockdown(self, ctx):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT modlog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()

		modlogchannel = self.bot.get_channel(id=int(result[0]))
		time = now.strftime("%m/%d/%y, %H:%M")

		embed = discord.Embed(color=0xFF0000)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"{ctx.author} Started a lockdown in {ctx.channel}", value=f"Started at {time}.")

		await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
		if result == None:
			await ctx.send(f"<#{ctx.channel.id}> Is now locked down!")
		if result != None:
			await ctx.send(f"<#{ctx.channel.id}> Is now locked down!")
			await modlogchannel.send(embed=embed)

	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(manage_channels=True)
	async def unlockdown(self, ctx):
		db = sqlite3.connect('snail.sqlite')
		cursor = db.cursor()
		cursor.execute(f"SELECT modlog_channel FROM snail WHERE guild_id = {ctx.guild.id}")
		result = cursor.fetchone()

		modlogchannel = self.bot.get_channel(id=int(result[0]))
		time = now.strftime("%m/%d/%y, %H:%M")

		embed = discord.Embed(color=0x008000)
		embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
		embed.add_field(name=f"{ctx.author} Has ended the lockdown for {ctx.channel}", value=f"Ended at {time}")

		await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
		if result == None:
			await ctx.send(f"<#{ctx.channel.id}> Is no longer under lock down")
		if result != None:
			await ctx.send(f"<#{ctx.channel.id}> Is no longer under lock down")
			await modlogchannel.send(embed=embed)


def setup(bot):
    bot.add_cog(mod_commands(bot))