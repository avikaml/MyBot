import discord
from discord.ext import commands
import json

# This is an untested cog, so it may not work -- Forgot to branch it as well

class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Mute.py is ready.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmute(self, ctx, *, role: discord.Role):
        with open('jsonfiles/mutes.json', "r") as f:
            mute_role = json.load(f)
            mute_role[str(ctx.guild.id)] = role.name
        
        with open("jsonfiles/mutes.json", "w") as f:
            json.dump(mute_role, f, indent=4)
        
        await ctx.send(f"The mute role has been set to {role.mention}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        with open('jsonfiles/mutes.json', "r") as f:
            mute_role = json.load(f)
        
        role = discord.utils.get(ctx.guild.roles, name=mute_role[str(ctx.guild.id)])
        await member.add_roles(role, reason=reason)
        await ctx.send(f"{member.mention} has been muted.")
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        with open('jsonfiles/mutes.json', "r") as f:
            mute_role = json.load(f)
        
        role = discord.utils.get(ctx.guild.roles, name=mute_role[str(ctx.guild.id)])
        await member.remove_roles(role, reason=reason)
        await ctx.send(f"{member.mention} has been unmuted.")

async def setup(client):
    await client.add_cog(Mute(client))