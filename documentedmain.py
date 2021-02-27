import os # For cog loading pre start.
import random # For 8ball command replies.
import shutil # For music player feature.
import youtube_dl # For music player.
import discord
from discord.ext import commands
from discord.utils import get 
import logging
from self_chat import chatbot_response_b
import tensorflow as tf
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
chat_history_ids = []
step = 0

client = commands.Bot(command_prefix = '.') # client variable def. # 


# Bot ready and status configuration
@client.event
async def on_ready(): # When the bot has all the information it needs on Discord.
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with myself')) 
    print("Bot is ready.")
    print('We have logged in as {0.user}'.format(client))

# on message and NLP(GPT2) code
@client.event
async def on_message(message):
    global step
    if message.content.startswith("*"):
        to_send=chatbot_response_b(step=step, user=message.content)
        print(to_send)
        try:
            await message.channel.send(to_send)
        except:
            await message.channel.send("No response...")

    if message.author == client.user:
        return
    
    if message.content.startswith("$"):
        if message.content("$spam"):
            pass
        print(message.content)
    
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

# unban command
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

# Voice channel Join command command

@client.command(pass_context=True, aliases=['j','joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}\n')

# Voice channel Leave command

@client.command(pass_context=True, aliases=['l','lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'The bot has left {channel}')
        await ctx.send(f'Left {channel}')   
    else:
        print('Bot was told to leave voice channel, but was not in one.')
        await ctx.send('Dont think I am in a voice channel.')

# music player Play command

@client.command(pass_context=True, aliases=['p','pla'])
async def play(ctx, url: str):
    
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith("mp3"):
                        os.rename(file, "song.mp3")

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
    
            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song.\n")    
    
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print('Removed old song file')
    except PermissionError:
        print('Trying to delete song file, but its being played.')
        await ctx.send('ERROR: music playing')
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send('Getting everything ready now.')

    voice = get(client.voice_clients, guild=ctx.guild) 

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }   
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio now.\n')
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'Renamed file: {file}\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit('-', 2)
    await ctx.send(f'Playing: {nname[0]}')
    print('Playing\n')

# music player Pause command

@client.command(pass_context=True, aliases=['pa','pau'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("music paused")
        voice.pause()
        await ctx.send("music paused")
    else:
        print("music not playing failed pause")
        await ctx.send("music not playing failed pause")

# music player Resume command

@client.command(pass_context=True, aliases=['r','res'])
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("music is not paused")
        await ctx.send("music is not paused")

# music player Stop command

@client.command(pass_context=True, aliases=['s','sto'])
async def stop(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("music stopped")
        voice.stop()
        await ctx.send("music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")

# music player Queue command

queues = {}

@client.command(pass_context=True, aliases=['q','que'])
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\\song{q_num}.%(ext)s")

    ydl_opts = { # Youtube_dl Options
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }   
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio now.\n')
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff sng{q_num} -f " + '"' + q_path + '"' + " -s " + url)

    await ctx.send("Adding song " + str(q_num) + " to the queue.")    

    print("Song added to queue\n")

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
 
client.run('')  
# Use Bot token in Parameter /
#  Bot token is a code that links your code to an app so that the code can manipulate the application.
