import discord
import os # For cog loading pre start
import random # For 8ball command replies.
from discord.ext import commands

client = commands.Bot(command_prefix = '.') # client variable def. # 

# Bot ready and status configuration
@client.event
async def on_ready(): # When the bot has all the information it needs on Discord.
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with myself')) 
    print("Bot is ready.")
    print('We have logged in as {0.user}'.format(client))

# Greetings event
@client.event
async def on_message(message):
    # if message.author == client.user: # Disabled since im alone in prac server lol
        # return

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')

# member join prompt
@client.event # prompts a member has joined
async def on_member_join(member): # member is an object in discord lib
    print("f'{member} has joined a server.")

# member left prompt
@client.event # prompts a member has left
async def on_member_remove(member):
    print("f'{member} has left the server.")


# clear command
@client.command()
async def clear(ctx, amount=0):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.channel.purge(limit=amount+1)

# clear command error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to use this command.')
    

# kick command
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None): # defined the member parameter as the member object of discord lib. # * says all the parameters passed in after ctx and member goes to reason.
    await member.kick(reason=reason)

# ban command
@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member): # * enables bot to read member with spaces.
    banned_users = await ctx.guild.bans() # Generates a list of banned users.
    member_name, member_discriminator = member.split('#') # To make the bot properly read the name and discriminator

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


# ping command
client.command()
async def ping(ctx): # `ctx` is context, mandatory parameter.
    await ctx.send(f'Pong! {client.latency * 1000}ms') # Bot responds Pong! to command `ping` # client latency says actual ping # ms is not mandatory.

# await asyncio.sleep(60)


# 8ball command
@client.command(aliases=['8ball']) # 8ball command aliases that can be called rather than acutal func.
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes - definetly.',
                'You may rely on it',
                'As I see it, yes.',
                'most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.',
                'Reply hazy, try again.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now',
                'Concentrate and ask again.',
                'Don\'t count on it.',
                'my reply is no.',
                'my sources say no.',
                'Outlook not very good',
                'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

# load cog command
@client.command()
async def load(ctx, extension): # extension will be the cog that you want to load.
    client.load_extension(f'cogs.{extension}') # cogs is the folder in the same directory as this code, extension is the python file called.

# unload cog command
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

# reload cog command
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

 
client.run('') # Use Bot token in Parameter / Bot token is a code that links your code to an app so that the code can manipulate the application.
