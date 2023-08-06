import discord
from discord.ext import commands
import tweepy
import settings
import re

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
        print('Twitter.py is ready but only !vx works')

    @commands.command()
    async def vx(self, ctx, tweet_url):
        # Check if the URL contains "twitter" and replace it with "vxtwitter"
        vxtwitter_url = tweet_url.replace("twitter", "vxtwitter")

        # Send the modified URL back to the user
        await ctx.send(vxtwitter_url)

        messages = []
        async for message in ctx.channel.history(limit=100):
            messages.append(message)

        for message in messages:
            if message.author == ctx.message.author and message.embeds:
                for embed in message.embeds:
                    if "twitter.com" in embed.url:
                        await message.delete()

    @commands.command()
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

def convert_twitter_links_to_vxtwitter(text):
    twitter_pattern = r"(https?://twitter\.com/(?:\w+)/(status|statuses)/(\d+))"
    replacement = r"https://vx.twitter.com/\3"

    vxtwitter_text = re.sub(twitter_pattern, replacement, text)
    return vxtwitter_text
