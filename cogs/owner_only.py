import contextlib
import io
import json
import textwrap
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from copy import copy

class owner_only(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	@commands.is_owner()
	async def sudo(self, ctx, victim: discord.Member, *, command):
		new_message = copy(ctx.message)
		new_message.author = victim
		new_message.content = ctx.prefix + command
		await bot.process_commands(new_message)

	@commands.command(aliases=['pm', 'message'])
	@commands.is_owner()
	async def dm(self, ctx, user: discord.Member, *args):
		await user.send((" ".join(args)))
		await ctx.send(f"**{user}** has been DMed")

	@commands.command()
	@commands.is_owner()
	async def dstatus(self, ctx):
		guilds = len([s for s in self.bot.guilds]) 
		activity = discord.Activity(name=f"Snailing around in {guilds} guilds", type=discord.ActivityType.playing)
		await self.bot.change_presence(activity=activity)
		await ctx.send('My status has been set back to default')

	@commands.command()
	@commands.is_owner()
	async def status(self, ctx, *args):
		guilds = len([s for s in bot.guilds]) 
		STATUS = (" ".join(args))
		activity = discord.Activity(name=f"{STATUS}", type=discord.ActivityType.playing)
		await bot.change_presence(activity=activity)
		await ctx.send(f"My status has been changed to **{STATUS}**")

	@commands.command(aliases=['csay'])
	@commands.is_owner()
	async def channelsay(self, ctx, channel: discord.TextChannel, *args):
		await channel.send((" ".join(args)))
		await ctx.send(f"I have sent a message to {channel.mention}")

	@commands.command(aliases=['echo'])
	@commands.is_owner()
	async def say(self, ctx, *args):
		await ctx.message.delete()
		await ctx.send((" ".join(args)))

	@commands.command()
	@commands.is_owner()
	async def listguilds(self, ctx):
		guilds = [(i.name, len(i.members)) for i in self.bot.guilds]
		await ctx.send(guilds)

	@commands.command()
	@commands.is_owner()
	async def react(self, ctx, message: discord.Message, reaction: discord.Emoji):
		await message.add_reaction(reaction)

	@commands.command()
	@commands.is_owner()
	async def ghostping(self, ctx, *args):
		theping = (" ".join(args))
		ping = await ctx.send(theping)
		await ping.delete()
		await ctx.message.delete()

	@commands.command()
	@commands.is_owner()
	async def serverleave(self, ctx):
		await ctx.send('Goodbye :(')
		await ctx.guild.leave()


def setup(bot):
    bot.add_cog(owner_only(bot))