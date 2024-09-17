import discord
from discord.ext import commands
import json
import os
import datetime
import asyncio
import random

with open("setting.json", mode="r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

class you_know(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def you_know():
        with open("you_know.json", mode="r", encoding="utf8") as f:
            ykl = json.load(f)
        return random.choice(ykl["list"])

def setup(bot):
    bot.add_cog(you_know(bot))