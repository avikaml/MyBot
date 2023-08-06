import discord
from discord.ext import commands
import settings

logger = settings.logging.getLogger("bot")

class Avatar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Avatar.py is ready')

    @commands.command(aliases=["Avatar","AVATAR"])
    async def avatar(self, ctx, member : discord.Member=None): 
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"{member}'s Avatar", color=discord.Color.blue())
        embed.set_image(url=member.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Avatar(client))