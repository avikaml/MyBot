import discord
from discord.ext import commands

'''
Basic embed cog - This is a template for future embeds
'''

class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener() # Decorator
    async def on_ready(self):
        print('MyCog.py is ready')
    
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(title="Test Embed", description="Description of embed.", color=discord.Color.default())

        embed.set_author(name=f"Requested by {ctx.author.display_name}", icon_url=f"{ctx.author.avatar}")
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_image(url=ctx.guild.icon)
        embed.add_field(name="Field Name", value="Field Value", inline=False)
        embed.set_footer(text="This is a footer.", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(MyCog(client))