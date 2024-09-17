from re import template
import discord
from discord.ext import commands
import json
import os
import datetime
import asyncio
import random

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)
with open("newcomerguide.json", mode="r", encoding="utf8") as f:
    ncgl = json.load(f)

class ncguide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["ncguide"]["ncguide"])
    async def ncguide(self, ctx, *, parts=""):
        temp_ver = "1.0"
        if not parts:
            res = []
            for a in ncgl["guide"][0]["pages"]:
                res += a["content"]+["~~**--------------------------------------------------------**~~"]
                if a["name"] == "thanks":
                    res.pop()
            length = 0
            b = []
            c = []
            for a in res:
                if length+len(a)>1000:
                    b.append("\n".join(c))
                    c = []
                    length = 0
                c.append(a)
                length += len(a)+2
            b.append("\n".join(c))
            res = b
            if sum([len(a) for a in res])>6000: embed = discord.Embed(title="New comer guide", color=discord.Colour.from_rgb(200, 225, 255), description="Structure&template version: {}&{}\nVersion: {}".format(ncgl["guide"][0]["structure_version"], temp_ver, ncgl["guide"][0]["version"]))
            else: embed = discord.Embed(title="New comer guide", color=discord.Colour.from_rgb(200, 225, 255), description="Structure&template version: {}&{}\nVersion: {}".format(ncgl["guide"][0]["structure_version"], temp_ver, ncgl["guide"][0]["version"]), timestamp=datetime.datetime.now())
            embeds = [embed]
            ind = 1
            for a in res:
                print(embeds, a)
                embeds[-1].add_field(name="_ _", value=a, inline=False)
                if ind%6 == 0 and len(res[ind:])>0:
                    if len(res[ind:])>6: embeds.append(discord.Embed(color=discord.Colour.from_rgb(200, 225, 255)))
                    else: embeds.append(discord.Embed(color=discord.Colour.from_rgb(200, 225, 255), timestamp=datetime.datetime.now()))
                ind += 1
            print(embeds)
            embeds[-1].set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
            for a in embeds:
                await ctx.send(embed=a)
            return
        elif parts in ("versions", "vers"):
            await ctx.send("Valid guide versions:\n{}".format("\n".join(["`{}`".format(a["version"]) for a in ncgl["guide"]])))
            return
        arg = parts.lower()
        for a, b in ((".", ""), ("fac", "facilities"), ("&", "and"), (" n ", " and "), ("prod", "production"), ("pro", "production"), ("trade", "trading"), ("mk", "market"), ("res", "research"), ("tech", "technology"), ("reg", "region"), ("log", "logistics"), ("mod", "modifiers"), ("ser", "services"), ("sv", "services"), ("ric", "reincorporation"), ("ri", "reincorporation"), ("reincorp", "reincorporation"), ("misc", "miscellaneous")):
            arg = arg.replace(a, b)
        alsche = {"i": "intro", "it": "intro", "a": "assets", "f and p": "facilities and production", "t and m": "trading and market", "r and t": "research and technology", "r and l": "region and logistics", "m and s": "modifiers and services", "r and m": "reincorporation and miscellaneous", "t": "thanks", "thx": "thanks", "end": "thanks"}
        if arg in alsche: arg = alsche[arg]
        a = []
        for b in alsche.values(): a += b.split()
        if arg in a:
            for a, b in alsche.items():
                if arg in b: arg = b
        if arg not in [a["name"] for a in ncgl["guide"][0]["pages"]]:
            await ctx.send("`EN0004`: The part \"{}\" was invalid.".format(parts))
            return
        guidev = ncgl["guide"][0]
        embed = discord.Embed(title="New comer guide", description="Structure&template version: {}&{}\nVersion: {}".format(guidev["structure_version"], temp_ver, guidev["version"]), color=discord.Colour.from_rgb(200, 225, 255), timestamp=datetime.datetime.now())
        res = []
        c = []
        length = 0
        for a in next((a["content"] for a in guidev["pages"] if a["name"] == arg)):
            if length+len(a)>1000:
                res.append("\n".join(c))
                c = []
                length = 0
            c.append(a)
            length += len(a)+2
        res.append("\n".join(c))
        for a in range(len(res)):
            if not a:
                embed.add_field(name=arg.capitalize(), value=res[a], inline=False)
                continue
            embed.add_field(name="_ _", value=res[a], inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ncguide(bot))