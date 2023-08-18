import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
import json
import settings
import logging
import SingletonLogger

logger = SingletonLogger.get_logger()

def get_server_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

# Create the bot instance with the specified prefix
client = commands.Bot(command_prefix=get_server_prefix, intents=discord.Intents.all())
    
# Event: Bot is ready
@client.event
# When the bot is ready to execute commands it will execute this function
async def on_ready():
    logger.info(f"User: {client.user} (ID: {client.user.id})")

@client.event
async def on_guild_join(guild):
    # Add the guild to the prefixes.json file
    with open('prefixes.json', "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    # Add the guild to the mutes.json file
    with open('cogs/jsonfiles/mutes.json', "r") as f:
        mute_role = json.load(f)
        mute_role[str(guild.id)] = None
    
    with open("cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)
    

@client.event
async def on_guild_remove(guild):
    # Remove the guild from the prefixes.json file
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    # Remove the guild from the mutes.json file
    with open('cogs/jsonfiles/mutes.json', "r") as f:
        mute_role = json.load(f)
        mute_role.pop(str(guild.id))
    
    with open("cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)

@client.command()
async def setprefix(ctx, *, newprefix: str):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = newprefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

# Event: Respond to a command
# ctx : Taking the inputs from discord(ctx = context)

@client.command()
async def hello(ctx):
    logger.info ("hello command called")
    await ctx.send("Hello! This is MyBot (Temporary Name).")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1136000176016871596)
    await channel.send(f'{member} has joined the server!')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1136000176016871596)
    await channel.send(f'{member} has left the server!')

# This is a normal function, not a discord event
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
        
async def main():
    async with client:
        await load()
        await client.start(settings.BOT_TOKEN, )

asyncio.run(main())