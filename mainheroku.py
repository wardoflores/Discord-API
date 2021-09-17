#! python3
# Discord Bot with Admin and music playing Features.
# Eduardo Jose Flores III: https://github.com/Coalemus
# Copyright (c) Eduardo Jose Flores III

# from secret import TOKEN # API token defined in separate module.
import random # For 8ball, and greetings command replies.
from random import randint
import os # For cog loading pre start.
from os import system
import shutil # For music player feature.
import asyncio
import youtube_dl # For music player.
import discord
from discord import opus
from discord.ext import commands
from discord.utils import get
from discord import Spotify

opus.load_opus('libopus.so.0')
discord.opus.is_loaded()

intents = discord.Intents.all() # For spotify command.

client = commands.Bot(command_prefix = '.', intents=intents)

sound_folder = r'D:\Music\Sound Effects' # Put your own sound effects directory here.
log_channel_id = client.get_channel(821008061480697896)
tag_dict={'tag1': ['name1', 'name2'],
          'tag2': ['name1', 'name2', 'name3']}



'''

Bot ready and status configuration.
When the bot has all the information it needs on Discord,
it 'prints Bot is ready.'

'''
@client.event

async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('3-6-9'))
    print("Bot is ready.")
    print('We have logged in as {0.user}'.format(client))

'''

Shutdown command, only owner role can execute.

'''

@client.command(
    aliases=['shit', 'rest'],
    brief="Closes bot.",
    description="Closes bot, reopen by running main.py script.")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting off... Bye!")
    await ctx.bot.close()

'''

Spotify info display.

'''
@client.command(
    brief="Displays user Spotify activity.",
    description="Only works if the activity displayed under User is 'Listening to Spotify.")
async def spotify(ctx, *, user: discord.Member = None):
    if user == None:
        user = ctx.author
        pass

    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed = discord.Embed(
                    title = f"{user.name}'s Spotify", 
                    description = "Listening to {}".format(activity.title), 
                    color = discord.Colour.green())
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                embed.set_footer(text="Song started at {}".format(activity.created_at.strftime("%H:%M")))
                await ctx.send(embed=embed)
                return
    
    await ctx.send(f"{user.name} is not listening to Spotify")
    return

'''

Debugging messages and channel specific functions.

'''
@client.event

async def on_message(message):
    if message.author == client.user:
        return
    
    hi_responses = ['hi~',
                'Hello~',
                'hello~',
                'Hey~',
                'hey~',
                'Yo~',
                'yo~',
                'Sup~',
                'sup~']

    ty_responses = ["You're welcome.",
                    'No problem.',
                    'Anytime.']

    if message.content.startswith('test'):
        embed = discord.Embed(title="test title!",
         description="Something something fix this later.",
          color=discord.Colour.greyple())
        embed.set_footer(icon_url = message.author.avatar_url, text = f"Requested by {message.author.name}")
        
        await message.channel.send('test!')
        await message.channel.send(embed=embed)

    if message.content.startswith(('Thankyou', 'thankyou', 'Thanks', 'ty', 'thanks', 'TY')):
        await message.channel.send(f"{random.choice(ty_responses)}")

    if message.content.startswith(('whatsup', 'hi', 'Hello', 'hello', 'Hey', 'hey', 'Yo', 'yo', 'Sup', 'sup')):
        await message.channel.send(f"{random.choice(hi_responses)}")

    if message.content.startswith(('ping', 'kahinay', 'internet', 'PLDT', 'Globe', 'lag', 'net')):
        embed = discord.Embed(title=f'Pong! {client.latency * 100 // .2}ms',
         description="Shows different pings for other users.",
          color=discord.Colour.green())
        embed.set_footer(icon_url = message.author.avatar_url, text = f"Requested by {message.author.name}")

        await message.channel.send(embed=embed) 

    if message.content.startswith(('Bye', 'goodbye', 'Babye', 'Byye', 'babyye', 'byyye', 'bye', 'babye', 'byye')):
        await message.channel.send("Bye! See you next time.")

    if message.content.startswith(('good morning', 'Good morning', 'Gm', 'gm', 'gud  morneng')):
        await message.channel.send("Good morning!")

    if message.content.startswith(('good night', 'Good night', 'Gn', 'gn', 'gud nayt')):
        await message.channel.send("Good night!")

    if message.channel.name == 'announcements':
            if message.content.startswith('debug'):
                await message.channel.send('debugged announcements!')

    if message.channel.name == 'log':
        if message.content.startswith('debug'):
            await message.channel.send('debugged logs!')

    if message.channel.name == 'general':
        if message.content.startswith('debug'):
            await message.channel.send('debugged General!')

    if message.channel.name == 'bot-playground':
        if message.content.startswith('debug'):
            await message.channel.send('debugged bot-playground!')
    
    if message.channel.name == 'vc-chat':
        if message.content.startswith('debug'):
            await message.channel.send('debugged vc-chat!')


    if message.channel.name == '3-6-9':
        if message.content.startswith('debug'):
            await message.channel.send('debugged 3-6-9!')

        # count == int(message.content)
        # if message.content != count:
        #   failed embed

        if message.content.startswith('1') and len(message.content) == 1:
            embed = discord.Embed(title="3-6-9!",
             description="Type clap if the number has 3, 6, or 9. Try to reach 4000!",
             color=discord.Colour.orange())
            embed.add_field(name = "Game start!",
             value = "Timer started (Under developement.) \n :clap: emoji doesn't work in code so type `clap` for now.",
             inline = True)

            await message.channel.send(embed=embed)

            # msg = await  get_channel(830912769292369940).history(limit=1).flatten()
            # msg = msg[0]

                # TODO make this logic into needing the right number to be inputted as +1 the previous message,
                # TODO ERROR: fetch_message missing 1 arhument: id
                # TODO Add timer.
                
                # await message.channel.send('this code work!')

        # TODO Logic for multiple iterations of numbers with 3 - 6 - 9 in different positions
        # TODO Mention loser

        if message.content.startswith('3') or message.content.startswith('6') or message.content.startswith('9'):
            embed = discord.Embed(title="Failed!",
                description="You need to :clap: , Reset to 1.",
                color=discord.Colour.red())
            await message.channel.send(embed=embed)
            asyncio.sleep(3)
            await message.channel.purge(bulk=True)
            
        if message.content.startswith(("\U0001f44f")):
            embed = discord.Embed(title=":clap:",
                description="Hope this has 1 *3*, *6*, or *9*, Else reset to *1*.",
                color=discord.Colour.green())
            await message.channel.send(embed=embed)

        if message.content.endswith('33') or message.content.endswith('36') and not message.content.endswith('6') or message.content.endswith('39') and not message.content.endswith('9'):
            embed = discord.Embed(title="Failed!",
                description="You need to :clap: :clap:, Reset to 1.",
                color=discord.Colour.red())
            await message.channel.send(embed=embed)
            asyncio.sleep(3)
            await message.channel.purge(bulk=True)

        if message.content.endswith('63') and not message.content.endswith('3') or message.content.endswith('66') or message.content.endswith('69') and not message.content.endswith('9'):
            embed = discord.Embed(title="Failed!",
                description="You need to :clap: :clap:, Reset to 1.",
                color=discord.Colour.red())
            await message.channel.send(embed=embed)
            asyncio.sleep(3)
            await message.channel.purge(bulk=True)

        if message.content.endswith('93') and not message.content.endswith('3') or message.content.endswith('96')  and not message.content.endswith('6') or message.content.endswith('99'):
            embed = discord.Embed(title="Failed!",
                description="You need to :clap: :clap:, Reset to 1.",
                color=discord.Colour.red())
            await message.channel.send(embed=embed)
            asyncio.sleep(3)
            await message.channel.purge(bulk=True)
        
        if message.content.startswith(("\U0001f44f" "\U0001f44f")) and not message.content.startswith(("\U0001f44f")):
            embed = discord.Embed(title=":clap: :clap:",
                description="Hope this has 2 *3*, *6*, or *9*, Else reset to *1*.",
                color=discord.Colour.green())
            await message.channel.send(embed=embed)

    await client.process_commands(message)

'''

prompts a member has joined; member is an object in discord lib.

'''
@client.event 

async def on_member_join(member):
    welcome = 748697685871296592
    channel = discord.TextChannel(guild=welcome, state=None, data=None)
    embed = discord.Embed(title=f' Test subject {member} has joined a server.',
    description="Your role will be set to verified automatically in 5 minutes.",
    color=discord.Colour.green())

    print(embed=embed)

    asyncio.sleep(300)

    ROLE = 748701878388523059

    role = get(member.guild.roles, name=ROLE)

    async with channel.typing():

        await member.add_roles(role)
        embed2 = discord.Embed(
            title=f"{member} was given {role}", 
            description="If you have time to provide feedback to improve the bot that would be well appreciated!", 
            color=discord.Colour.blue())

        print(embed=embed2)



'''

prompts a member has left.

'''
@client.event

async def on_member_remove(member):
    embed = discord.Embed(title="Someone left the server!",
     description="Something something fix this later.",
      color=discord.Colour.orange())
    print(embed)
    print("f'Test subject {member} has escaped the server.")

'''

Clears chat logs.

'''
@client.command(
    brief="Erases messages.", 
    description="Clears a specified amount of text depending on user input.")
async def clear(ctx, amount=0):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.channel.purge(limit=amount+1)

'''

Error for executing clear command.

'''
@client.command(
    brief="Permission error prompt.", 
    description="Prompts the user for unpermitted clear command.")
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to use this command.')

'''

Need to copy UserID of recepient of dm, enable Discord Developer mode.

'''
@client.command(
    brief="Direct message using bot.", 
    description="The bot sends a message specified by the User.")
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await client.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' sent to: " + target.name)

        except:
            await ctx.channel.send("Couldn't dm the given user.")

'''

Need to copy UserID of recepient of dm, enable Discord Developer mode.

'''
@client.command(
    brief="Bot messages all Users.", 
    description="The bot sends a message specified by the User to all members.")
async def dm_all(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print("'" + args + "' sent to: " + member.name)

            except:
                print("Couldn't send '" + args + "' to: " + member.name)

    else:
        await ctx.channel.send("A message was not provided.")

'''

Defined the member parameter as the member object of discord lib. 
* says all the parameters passed in after ctx and member goes to reason.

'''
@client.command(
    brief="Kicks a User.", 
    description="Speaks for itself.")
async def kick(ctx, member : discord.Member, *, reason=None): 
    await member.kick(reason=reason)

'''

Defined the member parameter as the member object of discord lib. 
* says all the parameters passed in after ctx and member goes to reason.

'''
@client.command(
    brief="Bans a User.", 
    description="Speaks for itself.")
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

'''

* function parameter enables bot to read member with spaces.
'banned_users' variable generates a list of banned users. 
'member_name', 'member_discriminator' variables To make the bot properly read the name and discriminator.

'''
@client.command(
    brief="Unbans a User.", 
    description="Speaks for itself.")
async def unban(ctx, *, member: discord.Member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

'''

Voice channel Join command.

'''
@client.command(pass_context=True, aliases=['j','joi'], 
brief="Bot joins in your Voice channel.", 
description="Use when you have already joined a Voice channel.")
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

    await ctx.send(f'joined {channel}')


'''

Voice channel Leave command.

'''
@client.command(pass_context=True, aliases=['l','lea'], 
brief="Bot leaves your Voice channel.", 
description="Only works if Bot is in your Voice channel.")
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

'''

music player Play command, slower than 'stream' command as
it downloads the .mp3 file then plays it.

'''
@client.command(pass_context=True, aliases=['p','pla'], 
brief="Plays a Youtube song. (Input yt link)", 
description="Only works if bot is run in its directory.")
async def playt(ctx, url: str): 
# TODO remove yt embed on command invoke.
# TODO string arg searches appropriate yt link.
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    
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
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")
    async with ctx.typing():
        await ctx.send("Getting everything ready now")

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
    async with ctx.typing():
        await ctx.send("Downloading Audio now...")
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading audio now\n")
                ydl.cache.remove()
                ydl.download([url])
        except:
            print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if spotify URL)")
            c_path = os.path.dirname(os.path.realpath(__file__))
            system("spotdl -f " + '"' + c_path + '"' + " -s " + url)  # make sure there are spaces in the -s

    async with ctx.typing():
        await ctx.send("Audio file downloaded. (Or failed to download.)")

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    
    videoID = url.split("watch?v=")[1].split("&")[0]

    embed = discord.Embed(
        title=f'Playing: {nname[0]}', 
        description="Click on the reactions to play/pause/stop/skip.", 
        color=discord.Colour.blue())
    # embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_thumbnail(url = "https://img.youtube.com/vi/{videoID}/0.jpg".format(videoID = videoID)) # or set_image
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    

    async with ctx.typing():
        embedsend = await ctx.send(embed=embed) 
        await embedsend.add_reaction('⏯️')
        await embedsend.add_reaction('⏹️')
        await embedsend.add_reaction('⏭️')


    print("playing\n")

'''

Can use resume command after.

'''
@client.command(pass_context=True, aliases=['pa','pau'], 
brief="Pauses a playing song.", 
description="Doesn't 'stop' a song, there's a seeparate command for that.")
async def pause(ctx): 
# TODO add reaction funtion to play and stream embed.

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("music paused")
        voice.pause()
        await ctx.send("music paused")
    else:
        print("music not playing failed pause")
        await ctx.send("music not playing failed pause")

'''

Can only be used on 'paused' songs and not a 'stopped' song.

'''
@client.command(pass_context=True, aliases=['r','res'], 
brief="Resumes a paused song.", 
description="Only resumes a 'paused' song and not a 'stopped' song.")
async def resume(ctx): 
# TODO add reaction function to play and stream embed.

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("music is not paused")
        await ctx.send("music is not paused")

'''

Cannot resume 'stopped' song.

'''
@client.command(pass_context=True, aliases=['s','sto'], 
brief="Stops current song.",
 description="It is not a pause command.")
async def stop(ctx): 
# TODO add reaction function to play and stream embed.

    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("music stopped")
        voice.stop()
        await ctx.send("music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")

queues = {}

'''

Works when using 'Play' command only.

'''
@client.command(pass_context=True, aliases=['q','que'], 
brief="Queues songs , predownloaded.", 
description="Tested for Play command only, add Issue if it doesn't work for Stream command.")
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir(r".\Queue")
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

    queue_path = os.path.abspath(os.path.realpath("Queue") + rf"\song{q_num}.%(ext)s")

    ydl_opts = {
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

    videoID = url.split("watch?v=")[1].split("&")[0]

    embed = discord.Embed(
        title=f"Adding song " + str(q_num) + " to the queue.", 
        description="This command only works when using with the play command.", 
        color=discord.Colour.teal())
    # embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_thumbnail(url = "https://img.youtube.com/vi/{videoID}/0.jpg".format(videoID = videoID)) # or set_image
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    

    async with ctx.typing():
        embed = await ctx.send(embed=embed) 

    print("Song added to queue\n")

'''

Next command for the music player.

'''
@client.command(
    pass_context=True, 
    aliases=['n', 'nex'],
    brief="Plays the next song.",
    description="Make sure to have songs in queue and be in the same voice channel as the bot playing music.")
async def next(ctx): 
# TODO add reaction function to play and stream embed.
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
        await ctx.send("Next Song")
    else:
        print("No music playing")
        await ctx.send("No music playing failed")

'''

Volume command, do `.volume {1-100}`.

'''
@client.command(
    pass_context=True, 
    aliases=['v', 'vol'],
    brief="Set volume from 1 - 100.",
    description="Make sure to be connected in the same voice channel as the bot.")
async def volume(ctx, volume: int): 

    if ctx.voice_client is None:
        return await ctx.send("Not connected to voice channel")

    print(volume/100)

    ctx.voice_client.source.volume = volume / 100
    await ctx.send(f"Changed volume to {volume}%")


'''

loads in separate modules from main code.
'extension' parameter will be the cog that you want to load.
cogs is the folder in the same directory as this code, extension is the python file called.

'''
@client.command(
    brief="Loads a cog.", 
    description="Cogs are 'Example', 'Test', 'soundboard', and 'stream'.")
async def load(ctx, extension): 
    client.load_extension(f'cogs.{extension}')

'''

Can only remove added cogs in Session.

'''
@client.command(
    brief="Unloads a cog.", 
    description="Cogs are 'Example', 'Test', 'soundboard', and 'stream'.")
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

'''

Reloads a specific, loaded cog in Session.

'''
@client.command(
    brief="Reloads a cog, refreshing it.", 
    description="Cogs are 'Example', 'Test', 'soundboard', and 'stream'.")
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

'''

Basic magic 8ball, can be repurposed into another 
random answer command.

'''

@client.command(aliases=['8ball'], brief="Basic 8ball.", 
    description="Don't depend on this.")
async def magic8ball(ctx, *, question):
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

'''

Pre-loaded cogs.

'''
client.load_extension('cogs.stream')
client.load_extension('cogs.soundboard')

'''

Add Bot token in a `secret.py` module in same directory of `main.py`, define a `TOKEN` variable there.
Bot token is a code that links your code to an app so that the code can manipulate the application.

'''

client.run("NzcwMzE1MTUxMjU3NjMyNzg4.X5bx4w.mYrK79hRM8Z4ZHoZf_XmYuyRi_0")