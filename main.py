import discord
from discord.ext import commands

# Put bot token in apikeys later and import from there as well as other api keys for the future
from apikeys import *

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

# Event: Respond to a command
# ctx : taking the inputs from discord
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


# Run the bot with the specified token
client.run(BOT_TOKEN)

