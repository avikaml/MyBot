import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener() # Decorator
    async def on_ready(self):
        print('Moderation.py is ready')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
            if count > 100:
                await ctx.send(embed = discord.Embed(color=discord.Color.red(), title=f"My limit is 100 message"))
            elif count <= 100 and count > 0:
                await ctx.channel.purge(limit=count + 1)
                await ctx.send(embed = discord.Embed(color=discord.Color.green(), title=f"Deleted {count} messages"))
            else:
                await ctx.send(embed = discord.Embed(color=discord.Color.red(), title=f"Please enter a number between 1 and 100"))
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, modreason):
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title="Success!", color = discord.Color.green())
        conf_embed.add_field(name="Member kicked:", value=f"{member.mention} has been kicked by {ctx.author.mention}", inline = False)
        conf_embed.add_field(name="Reason: ", value=modreason, inline = False)

        await ctx.send(embed=conf_embed)
        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member,  *, modreason):
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title="Success!", color = discord.Color.green())
        conf_embed.add_field(name="Member banned:", value=f"{member.mention} has been banned by {ctx.author.mention}", inline = False)
        conf_embed.add_field(name="Reason: ", value=modreason, inline = False)

        await ctx.send(embed=conf_embed)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userID):
        user = discord.Object(id=userID)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title="Success!", color = discord.Color.green())
        conf_embed.add_field(name="Member unbanned:", value=f"<@{userID}> has been unbanned by {ctx.author.mention}", inline = False)

        await ctx.send(embed=conf_embed)

async def setup(client):
    await client.add_cog(Moderation(client))
