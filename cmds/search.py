import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.calculate import calculate
from cmds.string_handler import string_handler
import re
from PIL import Image, ImageColor, ImageDraw, ImageFont
import textwrap
import random
import os, io
import time

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

class search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["search"]["search"])
    async def search(self, ctx, *, ctn=None):
        if ctn == None:
            await ctx.send("What you want to search?Just need to enter something.")
        else:
            if ctn.split()[0] in ("--April", "--20210401", "--april", "--aprilfool"):
                datetimedate = datetime.datetime(2021, 4, 1)
                ctn = " ".join(ctn.split(" ")[1:])
            else:
                datetimedate = datetime.datetime.now().date()
            embed = discord.Embed(title="Search", color=discord.Color.from_rgb(int("35", 16), int("12", 16), int("38", 16)), timestamp= datetime.datetime.now())
            imgname = ""
            if str(datetimedate.date()) == "2021-04-01":
                if ctn == "when":
                    embed.add_field(name="Result", value="ERROR: Time collection! Pleace make sure you have time to do this and try again")
                    img = Image.new("1", (100, 100), 255)
                    font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                    ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                elif re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', ctn.split(" ")[0]) or re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', ctn):
                    clr = ctn.split(" ")[0]
                    ctn = " ".join(ctn.split(" ")[1:])
                    if clr.startswith("#"):
                        img = Image.new("RGB", (100,100), clr)
                        embed.add_field(name="Color", value=clr)
                        if ctn:
                            font = ImageFont.FreeTypeFont('Arial.ttf', size=15)
                            ImageDraw.Draw(img).multiline_text((50, 50), "\n".join(textwrap.wrap(ctn, 7)), anchor="mm", fill="black", font=font, align="center")
                    else:
                        img = Image.new("RGB", (100,100), "#"+clr)
                        embed.add_field(name="Color", value="#"+clr)
                        if ctn:
                            font = ImageFont.FreeTypeFont('Arial.ttf', size=15)
                            ImageDraw.Draw(img).multiline_text((50, 50), "\n".join(textwrap.wrap(ctn, 7)), anchor="mm", fill="black", font=font, align="center")
                elif ctn == "end":
                    embed.add_field(name="Result", value="When UTC...")
                    img = Image.new("1", (100, 100), 255)
                    font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                    ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                else:
                    errors = ["Watch your self 3 second then close your eyes 1 second, search again",
                    "Internet error, pleace reconnect your internet",
                    "You are too alone, try again",
                    "Your brain is going to explode! try again!",
                    "Your pc is getting hacked, make sure your pc is right then try again",
                    "Your pc will EXPLODE!!"]
                    embed.add_field(name="Result", value="Error:\n"+random.choice(errors))
                    img = Image.new("1", (100, 100), 255)
                    font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                    ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                with io.BytesIO() as buffer:
                    img.save(buffer, format='png')
                    buffer.seek(0)
                    imgg = discord.File(buffer, "search.png")
                    embed.set_thumbnail(url="attachment://"+imgg.filename)
                    await ctx.send(file=imgg, embed=embed)
            else:
                embed.add_field(name="Result", value=ctn, inline=False)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(search(bot))