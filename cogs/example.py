import discord
from discord.ext import commands

class Example(commands.Cog): # Cog must be in capital C

    def __init__(self, client):
        self.client = client

    # Events example
    @commands.Cog.listener() # must have this decorator for within a cog. Cog method must have capital C.
    async def on_ready(self): # self must be first parameter in a class
        print('Bot cog is ready.')

    # Commands example
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

def setup(client):
    client.add_cog(Example(client))
