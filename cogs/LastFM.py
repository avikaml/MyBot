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

    @commands.command(case_insensitive=True)
    async def lfset(self, ctx, username):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lfset command in {ctx.guild.name} (ID: {ctx.guild.id})")
        with sqlite3.connect(settings.db_name) as conn:
            try:
                if(await has_lastfm_username(ctx.author.id)): # Not tested with await
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

    # This is a temporary solution to changing the LastFM username, it will be part of lfset in the future.
    @commands.command(case_insensitive=True)
    async def lfchange(self,ctx, username):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lfchange command in {ctx.guild.name} (ID: {ctx.guild.id})")
        with sqlite3.connect(settings.db_name) as conn:
            try:
                if(not has_lastfm_username(ctx.author.id)):
                    await ctx.send("You don't have a LastFM username set.")
                    return
                
                cursor = conn.cursor()
                query = '''
                UPDATE users SET lastfm_username = ? WHERE discord_id = ?
                '''
                values = (username, ctx.author.id)
                cursor.execute(query, values)
                conn.commit()
                await ctx.send(f"Changed LastFM username to {username}")

            except Exception as e:
                await ctx.send(f"Error: {e}")
                logger.error(f"Error: {e}")

    @commands.command(case_insensitive=True, alias=['lf np'])
    async def lf(self, ctx, username=None):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf command in {ctx.guild.name} (ID: {ctx.guild.id})")
        if(username is None):
            if(not await has_lastfm_username(ctx.author.id)):
                await ctx.send("You don't have a LastFM username set.")
                return
        username = await get_lastfm_username(ctx.author.id)
        print(username)
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={self.api_key}&format=json"
            response = requests.get(url)
            data = response.json()

            tracks = data['recenttracks']['track']
            track = tracks[0]
            prev_track = tracks[1]
            artist = track['artist']['#text']
            song = track['name']
            album = track['album']['#text']
            image = track['image'][2]['#text']

            embed = discord.Embed(title=f"**{username}** is currently listening to: ", description=f" **{song}** by **{artist}** \n on **{album}**", color=discord.Color.default())
            embed.set_author(name="LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            embed.set_thumbnail(url=image)
            #embed.set_image(url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            embed.add_field(name="Previous track", value=f"{prev_track['name']} by {prev_track['artist']['#text']}", inline=False)
            #embed.set_footer(text=f"Previous track: {prev_track['name']} by {prev_track['artist']['#text']}")

            await ctx.send(embed=embed)

            #await ctx.send(f"**{username}** is currently listening to **{song}** by **{artist}** from the album **{album}**")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    # TBD
"""     @commands.Command(alias=['lf recent', 'lf recenttracks', 'lf recent tracks'])
    async def lfrecent(self, ctx, username=None):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf recent command in {ctx.guild.name} (ID: {ctx.guild.id})")
        if(username is None):
            if(not await has_lastfm_username(ctx.author.id)):
                await ctx.send("You don't have a LastFM username set.")
                return
        username = await get_lastfm_username(ctx.author.id)
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={self.api_key}&format=json"
            response = requests.get(url)
            data = response.json()

            tracks = data['recenttracks']['track']

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")
 """

async def get_lastfm_username(discord_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT lastfm_username FROM users WHERE discord_id = ?', (discord_id,))
    row = cursor.fetchone()

    conn.close()

    print(row[0])

    # If the user has a LastFM username set, return it, otherwise return None
    if row is not None:
        return row[0]
    else:
        return None

async def has_lastfm_username(discord_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT lastfm_username FROM users WHERE discord_id = ?', (discord_id,))
    row = cursor.fetchone()

    conn.close()

    return row is not None and row[0] is not None

""" async def get_recent_tracks(username): # should maybe use this, if it works, in the !lf command :))
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={self.api_key}&format=json"
    response = requests.get(url)
    data = response.json()

    tracks = data['recenttracks']['track']

    return tracks
 """
async def setup(client):
    await client.add_cog(LastFM(client, settings.lastfm_api_key, settings.lastfm_secret_api_key))