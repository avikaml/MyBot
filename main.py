import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio

import logging

# Put bot token in apikeys later and import from there as well as other api keys for the future
from apikeys import *

'''
Figure out Logger later - Logger setup
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w') -
'''

# Set the command prefix for your bot (e.g., '!bot_command')
bot_prefix = "!"

# Create the bot instance with the specified prefix
client = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())
    
# Event: Bot is ready
@client.event
# When the bot is ready to execute commands it will execute this function
async def on_ready():
    print("Bot is ready.")
    print(f'Logged in as {client.user.name}')
    print(f'Bot ID: {client.user.id}')
    print('------')

# This is a normal function, not a discord event
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            #print(f"Loaded {filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(BOT_TOKEN)

# Event: Respond to a command
# ctx : Taking the inputs from discord

@client.command()
async def hello(ctx):
    await ctx.send("Hello! This is MyBot (Temporary Name).")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1136000176016871596)
    await channel.send(f'{member} has joined the server! gayyyyyyyy')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1136000176016871596)
    await channel.send(f'{member} has left the server! gayyyyyyyy')

asyncio.run(main())

# For learning purposes - "send" sends a message to the channel the command was made in
''''@client.command(aliases=["Ping","PING","pING"]) # Necessary for the bot to recognize this as a command
async def ping(ctx):
    bot_latency = round(client.latency * 1000)
    await ctx.send(f"Pong! {bot_latency} ms.")
'''

''' NO LONGER NEEDED: '''

# Run the bot with the specified token
#client.run(BOT_TOKEN)

