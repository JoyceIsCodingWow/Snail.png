import discord
from discord.ext import commands
from discord.ext.commands import Bot

class voice_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        response = ('<@756682052736385184> has joined the voice channel')
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(response)

    @commands.command()
    async def leave(self, ctx):
        response = ('<@756682052736385184> has left the voice channel')
        await ctx.voice_client.disconnect()
        await ctx.send(response)

    @commands.command()
    async def souljaboy(self, ctx): # Doesnt work. i think i dont remember
        voice_channel = ctx.author.voice.channel
        channel = None
        if voice_channel != None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source="C:/Users/ilove/Pictures/mp3/SouljaBoy.mp3"))

            while vc.is_playing():
                sleep(.1)
            await vc.disconnect()
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")



def setup(bot):
    bot.add_cog(voice_commands(bot))
