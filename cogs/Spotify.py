import discord
from discord.ext import commands
import aiohttp

# TBC
class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() 
    async def on_ready(self):
        print('Spotify.py is not ready for usage - TBC')
    
    @commands.command()
    async def sf(self, ctx, username):
        """Get the current playing track of a Spotify user."""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': 'Bearer YOUR_SPOTIFY_ACCESS_TOKEN'  # Replace with your Spotify access token
                }
                url = f"https://api.spotify.com/v1/me/player/currently-playing"
                response = await session.get(url, headers=headers)
                data = await response.json()

                if 'item' in data:
                    track = data['item']
                    track_name = track['name']
                    artist_name = track['artists'][0]['name']
                    album_name = track['album']['name']
                    track_url = track['external_urls']['spotify']

                    embed = discord.Embed(
                        title="Current Playing Track",
                        description=f"Track: [{track_name}]({track_url})\nArtist: {artist_name}\nAlbum: {album_name}",
                        color=discord.Color.default()
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("No current playing track.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(Spotify(bot))
