import discord
from discord.ext import commands
from discord.ext import tasks
from pathlib import Path
import json
import os
import datetime
import asyncio
import random
import sys
from io import StringIO
from cmds.isdigit import isdigit

# Setup
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()

bot = discord.Client()
bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)

file_ = Path("VSCodemark")
if file_.is_file():
    jdata["VSCode"] = "Yes"
else:
    jdata["VSCode"] = "No"
with open("setting.json", mode="w", encoding="utf8") as f:
    json.dump(jdata, f, ensure_ascii=False, indent=4)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

@bot.command(aliases=als["main"]["ping"])
async def ping(ctx):
    if str(datetime.datetime.now().date()) == "2021-04-01":
        await ctx.send(f'**{round(bot.latency*1000000, 2)}** ms')
    else:
        await ctx.send(f'**{round(bot.latency*1000, 2)}** ms')

@bot.command(aliases=als["main"]["version"])
async def version(ctx):
    if str(datetime.datetime.now().date()) == "2021-04-01":
        await ctx.send(f"The bot version is: **v.204.211**")
    else:
        await ctx.send(f"The bot version is: **{jdata['version']}**")

loadextensioncount = 0
for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        filename = filename[:-3]
        black = jdata['load_blacklist']
        if not filename in black:
            if jdata["VSCode"] == "Yes":
                if filename == "error_handler":
                    continue
            # un = jdt['unload']
            # if not filename in un:
            bot.load_extension(f'cmds.{filename}')
            loadextensioncount += 1
            print(str(loadextensioncount) + '_' + filename + '_loaded')

if __name__ == "__main__":
    bot.run(jdata['Token'] if jdata["VSCode"] == "No" else "ODQwNTI3OTU3OTAxNDQzMDgy.YJZgqQ.8tLNlFkV-uN-y5QDQ3e70NxLLsM")