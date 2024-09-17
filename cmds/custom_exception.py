import discord
from discord.ext import commands, tasks
import json
import os
import datetime
import asyncio
import random
import time

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class custom_exception(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MissingRequiredArgument(Exception):
        def __init__(self, arg):
            self.arg = arg

def setup(bot):
    bot.add_cog(custom_exception(bot))