import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime

class error_handler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send(f"You're missing the `{error.param.name}` argument, which is required for this command to work properly.")
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You need the `{error.missing_perms[0]}` permission to run this command.")
		if isinstance(error, commands.MissingRole):
			await ctx.send(f"You need to have the `{error.missing_role}` role to run this command.")
		if isinstance(error, commands.NotOwner):
			await ctx.send('You are not registered as an owner')
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f"I'm missing the following permssions '{error.missing_perms[0]}' needed to run this command")
		if isinstance(error, commands.NoPrivateMessage):
			await ctx.send('This command cannot be ran in dms.')
		if isinstance(error, commands.CommandNotFound):
			return

def setup(bot):
    bot.add_cog(error_handler(bot))