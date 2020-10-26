import discord
import asyncio
from discord.ext import commands
import discord_webhook
from discord.ext.commands import Bot
import sqlite3
from copy import copy
import random
from datetime import datetime

bot = commands.Bot(command_prefix=commands.when_mentioned_or("s!"), case_insensitive=True)
bot.remove_command('help')


intents = discord.Intents(
    guilds=True,  # guild/channel join/remove/update
    members=True,  # member join/remove/update
    bans=True,  # member ban/unban
    emojis=True,  # emoji update
    integrations=False,  # integrations update
    webhooks=False,  # webhook update
    invites=False,  # invite create/delete
    voice_states=True,  # voice state update
    presences=False,  # member/user update for games/activities
    guild_messages=True,  # message create/update/delete
    dm_messages=True,  # message create/update/delete
    guild_reactions=True,  # reaction add/remove/clear
    dm_reactions=True,  # reaction add/remove/clear
    guild_typing=False,  # on typing
    dm_typing=False,  # on typing
)


@bot.event
async def on_ready():
    print('bot is running')
    guilds = len([s for s in bot.guilds])
    channel = bot.get_channel(765067077601198091)
    activity = discord.Activity(name=f"Snailing around in {guilds} guilds", type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)
    await channel.send('snail.png Is running')

extensions = ['owner_only', 'mod_commands', 'mod_events', 'misc_commands', 'voice_commands', 'error_handler']


@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:            
        bot.load_extension(extension)
        await ctx.send('**{}** was loaded'.format(extension))
    except Exception as error:
        await ctx.send('**{}** cannot be loaded. *{}*'.format(extension, error))

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:            
        bot.unload_extension(extension)
        await ctx.send('**{}** was unloaded'.format(extension))
    except Exception as error:
        await ctx.send('**{}** cannot be unloaded. *{}*'.format(extension, error))

@bot.command(aliases=['rld'])
@commands.is_owner()
async def reload(ctx, extension):
    try:            
        bot.reload_extension(extension)
        await ctx.send('**{}** was reloaded'.format(extension))
    except Exception as error:
        await ctx.send('**{}** cannot be reloaded. *{}*'.format(extension, error))

@bot.command()
@commands.is_owner()
async def reboot(ctx):
    for extension in extensions:
        try:
            bot.reload_extension(extension)
        except Exception as error:
            await ctx.send('**{}** cannot be loaded. *{}*'.format(extension, error))


if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    bot.run('TOKEN')
