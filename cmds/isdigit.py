import discord
from discord.ext import commands
import json
import datetime
import asyncio

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class isdigit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def isdigit(string):
        a = int(''.join(filter(str.isdigit, string)))
        return a

def setup(bot):
    bot.add_cog(isdigit(bot))