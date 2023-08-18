import discord
from discord.ext import commands
import SingletonLogger

logger = SingletonLogger.get_logger()

class Fun(commands.Cog):
    """Funny global commands"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun.py is ready')

    @commands.command(aliases=["Shawty","SHAWTY"])
    async def shawty(self, ctx):
        url = "https://cdn.discordapp.com/attachments/1011911070962679858/1141421500302368798/Download.mp4"
        await ctx.send(url)
    
    @commands.command(aliases=["Longershawty", "shawty2"])
    async def longershawty(self, ctx):
        url = "https://cdn.discordapp.com/attachments/998019130940727328/1136317007986438289/thatshotg-1686754469265195008-1.mp4"
        await ctx.send(url)

    @commands.command(aliases=["rina", "Rina", "rip", "Rip", "riprina", "Karina"])
    async def karina(self, ctx):
        url = "https://cdn.discordapp.com/attachments/998019130940727328/1137069962461184010/ssstwitter.com_1691149012054.mp4"
        await ctx.send(url)

    @commands.command(aliases=["Wonter","WONTER"])
    async def wonter(self, ctx):
        url = "https://cdn.discordapp.com/attachments/1011911070962679858/1141011298608496691/1bfe4343d3c8f26253bc97c804be2dd9.mp4"
        await ctx.send(url)

    @commands.command(aliases=["Birthday"])
    async def birthday(self, ctx):
        url = "https://cdn.discordapp.com/attachments/1011911070962679858/1036162992070459422/75f93f3f4d2eaa9bac340f56c017f492.mp4"
        await ctx.send(url)
    
    @commands.command(aliases=["wake", "Wakeup", "WAKEUP"])
    async def Wake(self, ctx):
        url = "https://cdn.discordapp.com/attachments/1011911070962679858/1036163053923872808/3aa3471bdf126f421ce557f6ed1b5a91.mp4"
        await ctx.send(url)
    
    @commands.command(aliases=["ugotgames", "UGOTGAMES", "Yougotgames", "games", "Games", "GAMES"])
    async def yougotgames(self, ctx):
        url = "https://media.discordapp.net/attachments/771665123391569961/1140297249918824618/63c56ad4594cb434d4af4ea2b38557a4.png?width=507&height=676"
        await ctx.send(url)

async def setup(client):
    await client.add_cog(Fun(client))