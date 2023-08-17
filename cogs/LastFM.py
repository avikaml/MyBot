import discord
from discord.ext import commands
import settings
import requests
import sqlite3
import SingletonLogger
import settings
import urllib.parse
import datetime
from datetime import datetime, timedelta, timezone
import time
import asyncio
from modules.util import Pagination
import aiohttp

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

    @commands.command(case_insensitive=True, aliases=['lf np'])
    async def lf(self, ctx, username=None):
        ''' Returns the currently playing track of the user, or his last played track if he isn't playing anything. '''

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
            prev_track = tracks[1]
            artist_name = track['artist']['#text']
            song = track['name']
            album_name = track['album']['#text']
            image = track['image'][2]['#text']
            artist_name_encoded = urllib.parse.quote(artist_name)
            artist_url = f"https://www.last.fm/music/{artist_name_encoded}"
            album_name_encoded = urllib.parse.quote(album_name)
            album_url = f"https://www.last.fm/music/{album_name_encoded}"

            embed = discord.Embed(
                title=f"**{username}** - Now playing: ",
                url = f"https://www.last.fm/user/{username}",
                description = f" [**{song}**]({track['url']})" +
                              f" by [**{artist_name}**]({artist_url})" + f"\n on [**{album_name}**]({album_url})"
            )
            embed.set_author(name="LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            embed.set_thumbnail(url=image)
            embed.add_field(name="Previous track", value=f"**{prev_track['name']}** by **{prev_track['artist']['#text']}**", inline=False)

            # Get total playcount
            # url = f"http://ws.audioscrobbler.com/2.0/?method=user.getInfo&user={username}&api_key={self.api_key}&format=json"
            # playcount = await get_playcount(url)

            # Get individual track playcount
            url = f'http://ws.audioscrobbler.com/2.0/?method=user.getTrackScrobbles&user={username}&artist={artist_name}&track={track_name}&api_key={self.api_key}&format=json'
            response = requests.get(url)
            data = response.json()
            playcount = int(data['trackscrobbles']['@attr']['total'])
            embed.set_footer(text=f"Track scrobbles: {playcount}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    # NOTE TO SELF: can definitely modulize lfrecent, lftt etc into one function because they mostly do the same thing.
    @commands.command(aliases=['lf recent', 'lf recenttracks', 'lf recent tracks', 'lfrt'])
    async def lfrecent(self, ctx, username=None, page=1):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf recent command in {ctx.guild.name} (ID: {ctx.guild.id})")
        if(username is None):
            if(not await has_lastfm_username(ctx.author.id)):
                await ctx.send("You don't have a LastFM username set.")
                return
        username = await get_lastfm_username(ctx.author.id)
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={username}&api_key={self.api_key}&format=json"
            tracks = await get_recent_tracks(url)
            user_profile_url = f"https://www.last.fm/user/{username}"
            embed = discord.Embed(
                title=f"{username}'s recent tracks",
                url=f"{user_profile_url}",
                color=discord.Color.default()
            )
            embed.set_author(name=f"LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            #embed.set_thumbnail(url = ctx.author.avatar.url)

            track_list_value = await get_track_list(tracks)
            embed.description = track_list_value
            #await ctx.send(embed=embed)

            track_list_value = await get_track_list_batch(tracks, page)

            view = Pagination(track_list_value, embed)
            #message = await ctx.send(embed=embed)
            await ctx.send(embed=embed, view=view)
            
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")
    
    @commands.command(aliases=['lftt', 'lftoptrack'])
    async def lftoptracks(self, ctx, time='all', username=None, page=1):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf top tracks command in {ctx.guild.name} (ID: {ctx.guild.id})")
        if(username is None):
            if(not await has_lastfm_username(ctx.author.id)):
                await ctx.send("You don't have a LastFM username set.")
                return
        username = await get_lastfm_username(ctx.author.id)
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={username}&api_key={self.api_key}&format=json"
            tracks = await get_top_tracks(time, url)
            user_profile_url = f"https://www.last.fm/user/{username}"
            if time not in ('all', 'week', 'month', 'year', 'Year', 'Month', 'Week', 'All'):
                await ctx.send("Invalid time period. Please use `all`, `week`, `month`, or `year`.")
                return
            embed = discord.Embed(
                title=f"{username}'s top tracks ({time})",
                url=f"{user_profile_url}",
                color=discord.Color.default()
            )
            embed.set_author(name=f"LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            track_list_value = await get_top_tracks_base(tracks)
            track_list_value_desc = track_list_value[0:10]
            track_list_value_desc = "\n".join(track_list_value_desc)

            embed.description = track_list_value_desc

            track_list_value = await get_top_tracks_list_batch(tracks)
            #await ctx.send(embed=embed)

            view = Pagination(track_list_value, embed)
            #message = await ctx.send(embed=embed)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    @commands.command(aliases=['lf artist', 'lfartistinfo'])
    async def lfartist(self, ctx, artist=None, username=None, limit=10):
        ''' Get the user's top 10 albums and top 10 songs of a specific artist
            THIS COMMAND IS BROKEN - I will fix it later if possible!
           '''
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf artist command in {ctx.guild.name} (ID: {ctx.guild.id})")
        if(username is None): # 208 - 213 should be made into a function that is called becuase it is used in multiple commands
            if(not await has_lastfm_username(ctx.author.id)):
                await ctx.send("You don't have a LastFM username set.")
                return
        if(artist is None):
            await ctx.send("Please specify an artist.")
            return
        
        username = await get_lastfm_username(ctx.author.id)

        try:
            user_url = f"https://www.last.fm/user/{username}"
            albums_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={artist}&api_key={self.api_key}&format=json&limit={limit}"
            tracks_url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={artist}&api_key={self.api_key}&format=json&limit={limit}"
            
            user_album_playcount = await self.get_user_album_playcount(albums_url, username)
            sorted_albums = sorted(user_album_playcount.items(), key=lambda item: item[1], reverse=True)[:limit]
            albums_text = "\n".join([f"`{i+1}.` {album} - {playcount} plays" for i, (album, playcount) in enumerate(sorted_albums)])

            user_track_playcount = await self.get_user_track_playcount(tracks_url, username)
            sorted_tracks = sorted(user_track_playcount.items(), key=lambda item: item[1], reverse=True)[:limit]
            tracks_text = "\n".join([f"`{i+1}.` {track} - {playcount} plays" for i, (track, playcount) in enumerate(sorted_tracks)])

            embed = discord.Embed(
                title=f"{username}'s top tracks and albums of {artist}",
                url=user_url,
                color=discord.Color.default()
            )
            embed.set_author(name="LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            total_text = f"**Top Albums**\n{albums_text}\n\n**Top Tracks**\n{tracks_text}"
            embed.description = total_text

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")
    
    @commands.command(aliases=['lfta', 'lfalbums'])
    async def lftopalbums(self, ctx, time='all', username = None, page = 1):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf top albums command in {ctx.guild.name} (ID: {ctx.guild.id})")
        if(username is None):
            if(not await has_lastfm_username(ctx.author.id)):
                await ctx.send("You don't have a LastFM username set.")
                return
        username = await get_lastfm_username(ctx.author.id)
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={username}&api_key={self.api_key}&format=json"
            tracks = await get_top_tracks(time, url, 'topalbums')
            user_profile_url = f"https://www.last.fm/user/{username}"
            if time not in ('all', 'week', 'month', 'year', 'Year', 'Month', 'Week', 'All'):
                await ctx.send("Invalid time period. Please use `all`, `week`, `month`, or `year`.")
                return
            embed = discord.Embed(
                title=f"{username}'s top albums ({time})",
                url=f"{user_profile_url}",
                color=discord.Color.default()
            )
            embed.set_author(name=f"LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            track_list_value = await get_top_tracks_base(tracks)
            track_list_value_desc = track_list_value[0:10]
            track_list_value_desc = "\n".join(track_list_value_desc)

            embed.description = track_list_value_desc

            track_list_value = await get_top_tracks_list_batch(tracks)
            #await ctx.send(embed=embed)

            view = Pagination(track_list_value, embed)
            #message = await ctx.send(embed=embed)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    @commands.command(aliases=['lftartist', 'lftopartist', 'lftar'])
    async def lftopartists(self, ctx, time='all', username = None, page = 1):
        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the lf top artists command in {ctx.guild.name} (ID: {ctx.guild.id})")
        if(username is None):
            if(not await has_lastfm_username(ctx.author.id)):
                await ctx.send("You don't have a LastFM username set.")
                return
        username = await get_lastfm_username(ctx.author.id)
        try:
            url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={username}&api_key={self.api_key}&format=json"
            tracks = await get_top_tracks(time, url, 'topartists')
            user_profile_url = f"https://www.last.fm/user/{username}"
            if time not in ('all', 'week', 'month', 'year', 'Year', 'Month', 'Week', 'All'):
                await ctx.send("Invalid time period. Please use `all`, `week`, `month`, or `year`.")
                return
            embed = discord.Embed(
                title=f"{username}'s top albums ({time})",
                url=f"{user_profile_url}",
                color=discord.Color.default()
            )
            embed.set_author(name=f"LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
            track_list_value = await get_top_artists_base(tracks)
            track_list_value_desc = track_list_value[0:10]
            track_list_value_desc = "\n".join(track_list_value_desc)

            embed.description = track_list_value_desc

            track_list_value = await get_top_artists_list_batch(tracks)
            #await ctx.send(embed=embed)

            view = Pagination(track_list_value, embed)
            #message = await ctx.send(embed=embed)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"Error: {e}")
            logger.error(f"Error: {e}")

    async def get_user_album_playcount(self, albums_url, username):
            async with aiohttp.ClientSession() as session:
                async with session.get(albums_url) as response:
                    data = await response.json()

                    user_album_playcount = {}
                    if 'topalbums' in data and 'album' in data['topalbums']:
                        albums = data['topalbums']['album']
                        for album in albums:
                            album_name = album['name']
                            album_artist = album['artist']['name']
                            user_playcount = await self.get_user_playcount_for_album(album_artist, album_name, username)
                            user_album_playcount[f"{album_artist} - {album_name}"] = user_playcount

                    return user_album_playcount

    async def get_user_playcount_for_album(self, artist, album, username):
        album_info_url = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&artist={artist}&album={album}&api_key={self.api_key}&user={username}&format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(album_info_url) as response:
                data = await response.json()

                if 'album' in data and 'userplaycount' in data['album']:
                    return int(data['album']['userplaycount'])
                else:
                    return 0

    async def get_user_track_playcount(self, tracks_url, username):
        async with aiohttp.ClientSession() as session:
            async with session.get(tracks_url) as response:
                data = await response.json()

                user_track_playcount = {}
                if 'toptracks' in data and 'track' in data['toptracks']:
                    tracks = data['toptracks']['track']
                    for track in tracks:
                        track_name = track['name']
                        track_artist = track['artist']['name']
                        user_playcount = await self.get_user_playcount_for_track(track_artist, track_name, username)
                        user_track_playcount[f"{track_artist} - {track_name}"] = user_playcount

                return user_track_playcount

    async def get_user_playcount_for_track(self, artist, track, username):
        track_info_url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&artist={artist}&track={track}&api_key={self.api_key}&user={username}&format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(track_info_url) as response:
                data = await response.json()

                if 'track' in data and 'userplaycount' in data['track']:
                    return int(data['track']['userplaycount'])
                else:
                    return 0

async def get_top_tracks_list_batch(tracks):
    track_list = []
    for i, track in enumerate(tracks):
        track_name = track['name']
        if(len(track_name) > 20):
                track_name = track_name[0:20] + "..."
        artist_name = track['artist']['name']
        playcount = track['playcount']
        track_list.append(f"`{i+1}.` [{track_name} by {artist_name}]({track['url']}) - {playcount} plays")

    #track_list_value = "\n".join(track_list)
    return track_list

async def get_top_artists_list_batch(artists):
    artists_list = []
    for i, artist in enumerate(artists):
        artist_name = artist['name']
        playcount = artist['playcount']
        artists_list.append(f"`{i+1}.` [{artist_name}]({artist['url']}) - {playcount} plays")

    return artists_list

async def get_top_tracks_base(tracks, page=1):
    track_list = []
    for batch_start in range(0, len(tracks), 10):
        batch = tracks[batch_start : batch_start + 10]
        for j, track in enumerate(batch):
            track_name = track['name']
            if(len(track_name) > 20):
                track_name = track_name[0:20] + "..."
            artist_name = track['artist']['name']
            playcount = track['playcount']
            track_list.append(f"`{j+1}.` [{track_name} by {artist_name}]({track['url']}) - {playcount} plays")

    #track_list_value = "\n".join(track_list)
    return track_list

async def get_top_artists_base(artists, page=1):
    artists_list = []
    for batch_start in range(0, len(artists), 10):
        batch = artists[batch_start : batch_start + 10]
        for j, artist in enumerate(batch):
            artist_name = artist['name']
            playcount = artist['playcount']
            artists_list.append(f"`{j+1}.` [{artist_name}]({artist['url']}) - {playcount} plays")
    
    return artists_list

async def get_top_tracks(time, url, data_type='toptracks'):
    if(time == 'all' or time =='a' or time == 'All' or time == 'overall'):
        url += '&period=overall'
    elif(time == 'week' or time == 'w' or time == 'Week'):
        url += '&period=7day'
    elif(time == 'month' or time == 'm' or time == 'Month'):
        url += '&period=1month'
    elif(time == 'year' or time == 'y' or time == 'Year'):
        url += '&period=12month'
    else:
        url += '&period=overall'
    response = requests.get(url)
    data = response.json()
    if data_type == 'toptracks':
        tracks = data['toptracks']['track']
    elif data_type == 'topartists':
        tracks = data['topartists']['artist']
    else:
        tracks = data['topalbums']['album']
    return tracks
    

async def get_track_list_batch(tracks, page=1):
    track_list = []
    
    # Loop through batches of tracks (10 tracks per batch)
    for batch_start in range(0, len(tracks), 10):
        batch = tracks[batch_start : batch_start + 10]
        for j, track in enumerate(batch):
            artist_name = track['artist']['#text']
            # Replace spaces with %20 using urllib.parse.quote
            artist_name_encoded = urllib.parse.quote(artist_name)
            artist_url = f"https://www.last.fm/music/{artist_name_encoded}"

            # Have to do it like this cause of some problem with '@' in python
            now_playing = track.get('@attr', {}).get('nowplaying', None) 
            track_name = track['name']

            if(len(track_name) > 20):
                track_name = track_name[0:20] + "..."

            track_info = f"`{j+1 + batch_start}.` [{track['artist']['#text']}]({artist_url}) - " \
                            f"[{track_name}]({track['url']})"

            if(j == 0 and now_playing == 'true'):
                track_list.append(track_info + " - " + "Now playing")
            else:
                track_date = track.get('date', {}).get('uts', 'Unknown Date')
                timestamp = await format_time(track_date)
                track_list.append(track_info + " - " + f"{timestamp}")

    #track_list_value = "\n".join(track_list)
    return track_list

async def get_track_list(tracks, page=1): #page=1 ?????? (page-1)*10:page*10+10(0:10, 10:20,...)
    track_list = []
    for j, track in enumerate(tracks[(page-1)*10:page*10]):
        artist_name = track['artist']['#text']
        # Replace spaces with %20 using urllib.parse.quote
        artist_name_encoded = urllib.parse.quote(artist_name)
        artist_url = f"https://www.last.fm/music/{artist_name_encoded}"

        # Have to do it like this cause of some problem with '@' in python
        now_playing = track.get('@attr', {}).get('nowplaying', None) 
        track_name = track['name']

        if(len(track_name) > 20):
            track_name = track_name[0:20] + "..."

        track_info = f"`{j+1}.` [{track['artist']['#text']}]({artist_url}) - " \
                        f"[{track_name}]({track['url']})"

        if(j == 0 and now_playing == 'true'):
            track_list.append(track_info + " - " + "Now playing")
            
        else:
            track_date = track.get('date', {}).get('uts', 'Unknown Date') # Doing this because this works for some reason...
            timestamp = await format_time(track_date)
            track_list.append(track_info + " - " + f"{timestamp}")

    track_list_value = "\n".join(track_list)

    return track_list_value

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

# yoinked this code from a friend and made some minor changes, ty :)
async def format_time(timestamp):
    dt = datetime.utcfromtimestamp(int(timestamp))
    now = datetime.utcnow()
    diff = now - dt
    if diff < timedelta(minutes=1):
        return "just now"
    elif diff < timedelta(hours=1):
        minutes = diff.seconds // 60
        return f"{minutes} min{'s' if minutes > 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = diff.days
        return f"{days} day{'s' if days != 1 else ''} ago"

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                # Handle errors here
                response_text = await response.text()
                raise Exception(f"Error fetching URL: {response_text}")

async def setup(client):
    await client.add_cog(LastFM(client, settings.lastfm_api_key, settings.lastfm_secret_api_key))