import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.calculate import calculate
import re
import decimal, math, numexpr

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

class calculationcmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="calculate", aliases=als["cogs"]["calculationcmds"]["calculate"])
    async def calculations(self, ctx, option, *, express):
        res = []
        express = [a.strip() for a in express.split("|")]
        if option in ("+", "plus", "p"):
            for a in express:
                b = [decimal.Decimal(a.strip()) for a in re.split("[,+]", a)]
                res.append(str(sum(b)))
        elif option in ("*", "x" "times", "t"):
            for a in express:
                b = [decimal.Decimal(a.strip()) for a in re.split("[,*]", a)]
                res.append(str(math.prod(b)))
        else:
            for a in express:
                res.append(str(numexpr.evaluate(a)))
        await ctx.send("Result:\n"+"\n".join(res))

def setup(bot):
    bot.add_cog(calculationcmds(bot))