import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener() # Decorator
    async def on_ready(self):
        print('Ping.py is ready')

    # Commands are different in cogs than in main.py
    @commands.command(aliases=["Ping","PING","pING"])
    # Most put in self as the first parameter, but ctx is the first parameter
    async def ping(self, ctx): 
        bot_latency = round(self.client.latency * 1000) # In classes we have to use self.client instead of client
        await ctx.send(f"Pong! {bot_latency} ms.")


async def setup(client):
    await client.add_cog(Ping(client))