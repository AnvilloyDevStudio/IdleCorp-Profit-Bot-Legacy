import discord
from discord.ext import commands, tasks
import json
import datetime
import asyncio

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class member_jnl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(jdata['guild_id'])
        channel = guild.get_channel(801057721205522432)
        await channel.send(f"Welcome {member.mention} <:smile:{jdata['guild_id']}>, you can go to <#801060352108134440> to read Rules.")

    #成員退出
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(jdata['guild_id'])
        channel = guild.get_channel(801057721205522432)
        await channel.send(f"**{member}** leaved here(•_•)")

def setup(bot):
    bot.add_cog(member_jnl(bot))