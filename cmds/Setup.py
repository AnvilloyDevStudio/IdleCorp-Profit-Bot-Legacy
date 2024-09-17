import discord
from discord.ext import commands
import json
import datetime
import asyncio

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if jdata["VSCode"] == "No":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Version {jdata['version']}"))
        print("Now online")

def setup(bot):
    bot.add_cog(Setup(bot))