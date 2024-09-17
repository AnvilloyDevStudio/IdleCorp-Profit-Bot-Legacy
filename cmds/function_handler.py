import discord
from discord.ext import commands, tasks
import json
import datetime
import asyncio
from pathlib import Path
import inspect

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class function_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_args(function):
        return list(dict(inspect.signature(function).parameters).keys())

def setup(bot):
    bot.add_cog(function_handler(bot))