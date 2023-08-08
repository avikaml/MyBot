import discord
from discord.ext import commands
import settings
import requests
import sqlite3
import SingletonLogger
import settings

logger = SingletonLogger.get_logger()

class LastFM(commands.Cog):
    def __init__(self, client, api_key, secret_api_key):
        self.client = client
        self.api_key = api_key
        self.secret_api_key = secret_api_key

    @commands.Cog.listener()
    async def on_ready(self):
        print('LastFM.py is ready')

    @commands.command()
    async def setlastfm(self, ctx, username):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the setlastfm command in {ctx.guild.name} (ID: {ctx.guild.id})")
        with sqlite3.connect(settings.db_name) as conn:
            try:
                if(has_lastfm_username(ctx.author.id)):
                    await ctx.send("You already have a LastFM username set.")
                    return
                #conn = sqlite3.connect(settings.db_name)
                cursor = conn.cursor()
                query = '''
                INSERT OR REPLACE INTO users (discord_id, lastfm_username)
                VALUES (?, ?)
                '''

                values = (ctx.author.id, username)

                cursor.execute(query, values)
                conn.commit()
                await ctx.send(f"Set LastFM username to {username}")

            except Exception as e:
                await ctx.send(f"Error: {e}")
                logger.error(f"Error: {e}") 

            """ finally: # THIS MIGHT NEED TO GO! ITS CAUSING PROBLEM
                conn.close() """


def has_lastfm_username(discord_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT lastfm_username FROM users WHERE discord_id = ?', (discord_id,))
    row = cursor.fetchone()

    conn.close()

    return row is not None and row[0] is not None

async def setup(client):
    await client.add_cog(LastFM(client, settings.lastfm_api_key, settings.lastfm_secret_api_key))