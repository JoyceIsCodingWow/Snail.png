import discord
from discord.ext import commands
from discord.ext.commands import Bot
import math

class misc_commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def help(self, ctx):
		author = ctx.message.author
		embedVar = discord.Embed(title="Misc commands", description="Gives you a list of the misc commands.", color=16714423)
		embedVar.set_author(name="Snail.png", icon_url="https://cdn.discordapp.com/avatars/756682052736385184/638737b828dcdd243c1207536547f68b.webp?size=1024")
		embedVar.add_field(name="s!invite", value="Gives you the bots invite link. `s!invite`", inline=False)
		embedVar.add_field(name="s!server", value="Gives you the invite for the bots support server. `s!server`", inline=False)
		embedVar.add_field(name='s!suggest', value="Lets you suggest a feature for the bot. `s!suggest {suggestion}`")
		embedVar.add_field(name="s!userinfo", value="Gives you a users information. `s!userinfo {User}`", inline=False)
		embedVar.add_field(name="s!pfp", value="Gives you a users profile picture. `s!pfp {User}`", inline=False)
		embedVar.add_field(name='s!vote', value=' Gives you the link to upvote snail on discord.ly.', inline=False)
		embedVar.add_field(name="Moderator Commands", value="Gives you a list of all moderation comamnds.", inline=False)
		embedVar.add_field(name="s!ban", value="Bans a member. `s!ban {User} {reason}`", inline=False)
		embedVar.add_field(name='s!kick', value='Kicks a member. `s!kick {User} {reason}`', inline=False)
		embedVar.add_field(name='s!purge', value='Purges the given amount of messages. `s!purge {Amount}`', inline=False)
		embedVar.add_field(name='s!lockdown', value='locks down a channel. `s!lockdown`, `s!unlockdown`', inline=False)
		embedVar.add_field(name='s!setup', value='Lets you setup certain bot features. `s!setup`', inline=False)
		embedVar.add_field(name='Voice commands', value='Gives you a list of all voice related commands (currently doesnt do much)', inline=False)
		embedVar.add_field(name='s!join', value='Joins a voice channel. `s!join`, `s!leave`', inline=False)
		await author.send(embed=embedVar)
		await ctx.send('Sent you a DM!')

	@commands.command()
	async def invite(self, ctx):
		response = ('<https://discord.com/oauth2/authorize?client_id=756682052736385184&scope=bot&permissions=8>')
		await ctx.send(response)

	@commands.command(aliases=['support'])
	async def server(self, ctx):
		await ctx.send(f"https://discord.gg/C6AnGyr")

	@commands.command(aliases=['whois', 'profile'])
	async def userinfo(self, ctx, member: discord.Member):
		if member == None:
			member = ctx.message.author
		account_created = member.created_at.strftime("%b %d, %Y")
		account_join = member.joined_at.strftime("%b %d, %Y")
		color = member.color
		avatar = member.avatar_url
		member_name = member.name
		member_discrim = member.discriminator
		member_mention = member.mention
		userid = member.id
		hashtag = ('#')
		embedVar = discord.Embed(description=member_mention, color=color)
		embedVar.set_author(name=member_name + hashtag + member_discrim, icon_url=avatar)
		embedVar.set_thumbnail(url=avatar)
		embedVar.add_field(name='User ID', value=userid, inline=False)
		embedVar.add_field(name='Account Created At', value=account_created, inline=False)
		embedVar.add_field(name='Joined Server At', value=account_join, inline=False)
		await ctx.send(embed=embedVar)

	@commands.command(aliases=['picture', 'profilepicture'])
	async def pfp(self, ctx, member: discord.Member):
		avatar = member.avatar_url
		member_name = member.name
		color = member.color
		member_discrim = member.discriminator
		embedVar = discord.Embed(description=f"{member_name}#{member_discrim}'s Profile picture", color=color)
		embedVar.set_image(url=avatar)
		await ctx.send(embed=embedVar)

	@commands.command(aliases=['upvote'])
	async def vote(self, ctx):
		await ctx.send(f"You can upvote snail at https://discordbotlist.com/bots/snailpng. Voting currently doesnt do anything, but if you would like to suggest something you can suggest it with `s!suggest`")





def setup(bot):
    bot.add_cog(misc_commands(bot))