import discord
from discord.ext import commands
import settings
import requests
import sqlite3
import SingletonLogger
import settings
import urllib.parse

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
        ''' allows a user to set their lastfm username.'''
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
        ''' change a users lastfm username.'''
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
        ''' Returns the currently playing track of the user, or his last played track if he isn't playing anything
            To be added:
            - Add a footer with amount of scrobbles on the song - currently just shows total amount of scrobbles on the user
        '''
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf command in {ctx.guild.name} (ID: {ctx.guild.id})")
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
            track = tracks[0]
            track_name = track['name']
            #print(track)
            prev_track = tracks[1]
            #print(prev_track)
            artist_name = track['artist']['#text']
            song = track['name']
            album_name = track['album']['#text']
            image = track['image'][2]['#text']
            artist_name_encoded = urllib.parse.quote(artist_name)
            artist_url = f"https://www.last.fm/music/{artist_name_encoded}"
            album_name_encoded = urllib.parse.quote(album_name)
            album_url = f"https://www.last.fm/music/{album_name_encoded}"

            #embed = discord.Embed(title=f"**{username}** - Now playing: ", description=f" **{song}** by **{artist}** \n on **{album}**", color=discord.Color.default())
            embed = discord.Embed(
                title=f"**{username}** - Now playing: ",
                url = f"https://www.last.fm/user/{username}",
                description = f" [**{song}**]({track['url']})" +
                              f" by [**{artist_name}**]({artist_url})" + f"\n on [**{album_name}**]({album_url})"
            )
            embed.set_author(name="LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            embed.set_thumbnail(url=image)
            embed.add_field(name="Previous track", value=f"**{prev_track['name']}** by **{prev_track['artist']['#text']}**", inline=False)

            # Get playcount
            url = f"http://ws.audioscrobbler.com/2.0/?method=user.getInfo&user={username}&api_key={self.api_key}&format=json"
            playcount = await get_playcount(url)
            embed.set_footer(text=f"Total scrobbles: {playcount}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    # TBC
    @commands.command(alias=['lf recent', 'lf recenttracks', 'lf recent tracks', 'lfrt'])
    async def lfrecent(self, ctx, username=None):
        ''' Returns the recent tracks played by the user
            To be added:
            - proper timestamp using the actual time lastfm give i guess or the datetime library?
            - add a reaction to the message to allow the user to go to the next page of track
            - add a reaction to the message to allow the user to go to the previous page of track
            - add a reaction to the message to allow the user to go to the first page of track
            - add a reaction to the message to allow the user to go to the last page of track
            Reference point : the lfc lf bot, it's very clean
            - Add proper timestamps to each song instead of what lastfm api gives
        '''

        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf recent command in {ctx.guild.name} (ID: {ctx.guild.id})")
        if(username is None):
            if(not await has_lastfm_username(ctx.author.id)):
                await ctx.send("You don't have a LastFM username set.")
                return
        username = await get_lastfm_username(ctx.author.id)
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={self.api_key}&format=json"
            tracks = await get_recent_tracks(url)
            #print(tracks[:1])
            # user_profile_url = f"https://www.last.fm/user/{username}"
            embed = discord.Embed(
                title=f"**{username}'s** recent tracks",
                url=f"https://www.last.fm/user/{username}",
                color=discord.Color.default()
            )
            embed.set_author(name="LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            embed.set_thumbnail(url = ctx.author.avatar.url)
            
            for j, track in enumerate(tracks[0:10]):
                artist_name = track['artist']['#text']
                # Replace spaces with %20 using urllib.parse.quote
                artist_name_encoded = urllib.parse.quote(artist_name)
                artist_url = f"https://www.last.fm/music/{artist_name_encoded}"
                #print(track)
                #print("attr" + track['@attr']['nowplaying'])
                now_playing = track.get('@attr', {}).get('nowplaying', None)

                if(j == 0 and now_playing == 'true'):
                    embed.add_field(name=f"", value=f"{j+1}. "+f"[{track['artist']['#text']}]({artist_url})" +" - " +
                                    f"[{track['name']}]({track['url']})" +
                                    " - " + "now playing...", inline=False)
                else:
                    embed.add_field(name=f"", value=f"{j+1}. "+f"[{track['artist']['#text']}]({artist_url})" +" - " +
                                 f"[{track['name']}]({track['url']})" +
                                 " - " + f"{track['date']['#text']}", inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

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

async def get_recent_tracks(url): # should maybe use this, if it works, in the !lf command :))
    response = requests.get(url)
    data = response.json()

    tracks = data['recenttracks']['track']

    return tracks

async def get_playcount(url):
    ''' Returns the total playcount of the user '''
    response = requests.get(url)
    data = response.json()
    playcount = data["user"]["playcount"]
    return playcount

async def setup(client):
    await client.add_cog(LastFM(client, settings.lastfm_api_key, settings.lastfm_secret_api_key))