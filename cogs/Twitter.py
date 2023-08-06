import discord
from discord.ext import commands
import tweepy
import settings

class Twitter(commands.Cog):

    def __init__(self, client, api_key, api_secret_key, access_token, access_token_secret):
        self.client = client
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        # Setup Tweepy
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    @commands.Cog.listener() 
    async def on_ready(self):
        print('Twitter.py is ready')

    @commands.command(alias=['t'])
    async def tweet(self, ctx, tweet_url):
        try:
            # Extract the tweet ID from the tweet URL
            tweet_id = tweet_url.split('/')[-1]

            # Fetch tweet data using Tweepy
            tweet = self.api.get_status(tweet_id, tweet_mode='extended')

            # Create an embed
            embed = discord.Embed(title="Twitter Embed", color=discord.Color.blue())
            embed.description = tweet.full_text
            if 'media' in tweet.entities:
                media_urls = [media['media_url_https'] for media in tweet.entities['media']]
                if len(media_urls) == 1:
                    embed.set_image(url=media_urls[0])
                else:
                    for i, media_url in enumerate(media_urls):
                        embed.add_field(name=f"Media {i + 1}", value=media_url, inline=False)

            # Send the embed to the Discord channel
            await ctx.send(embed=embed)

        except tweepy.TweepyException as e:
            await ctx.send(f"Error: {e}")

async def setup(client):
    api_key = settings.twitter_api_key
    api_secret_key = settings.twitter_api_secret
    access_token = settings.twitter_access_token
    access_token_secret = settings.twitter_access_token_secret
    await client.add_cog(Twitter(client, api_key, api_secret_key, access_token, access_token_secret))