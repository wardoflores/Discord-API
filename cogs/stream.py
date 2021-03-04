import random 
import os 
from os import system
import shutil
import asyncio
import youtube_dl
import discord
from discord.ext import commands
from discord.utils import get 



ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   

ffmpeg_options = {
'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ydl_opts)
class stream(commands.Cog):
    def __init__(self, client):
        self.client = client

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        player = await stream.from_url(url, loop=client.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))

    def setup(client):
    client.add_cog(Text(client))