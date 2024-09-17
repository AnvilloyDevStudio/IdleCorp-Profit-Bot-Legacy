import discord
from discord.ext import commands, tasks
import json
import datetime
import asyncio
from pathlib import Path
from cmds.string_handler import string_handler
from cmds.custom_exception import custom_exception
from cmds.calculate import calculate
from cmds.you_know import you_know
import re, time

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

class speed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["speed"]["speed"])
    async def speed(self, ctx, *, args):#facilities, number
        correct = string_handler.location(str, int, args, True)
        if correct == True:
            pass
        elif correct[0] == False:
            if correct[1][0] == "int":
                raise custom_exception.MissingRequiredArgument("number")
            await ctx.send("`EN0007`: Can't determind arguments")
            return
        elif correct == "int":
            raise custom_exception.MissingRequiredArgument("number")
        args = string_handler.filter(args, True)
        print(args)
        if args[0][0].startswith("--"):
            flag, fac = args[0][0].lower()[2:], args[0][1:]
            flagals = {"sec": "second", "s": "second", "min": "minute", "m": "minute", "hr": "hour", "h": "hour", "d": "day"}
            if flag in flagals: flag = flagals[flag]; unit = flag
            elif flag not in flagals.values():
                await ctx.send("`EN0003`: Invalid flag")
                return
        else: fac = args[0]; unit = "second"
        num = args[1]
        if num == []:
            num = 1
        fac = " ".join(fac).lower()
        for a, b in als["ic"]["facilities"].items():
            if b != None:
                if fac in b:
                    fac = a
        fac = fac.split(" ")
        fac = "_".join(fac).lower()
        with open("icdetail.json", mode="r", encoding="utf8") as f:
            icd = json.load(f)
        if not fac in icd["facilities"].keys():
            await ctx.send("`EN0004`: Cannot find facility: {}".format(" ".join(args[0])))
            return
        if type(num) == list: 
            for a in num:
                num = a
        if type(num) == str:
            if num.endswith(('k', 'm', 'b')):
                a = num[:-1]
                if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", a):
                    tnum = a.replace(',', '')
                    if num.endswith("k"):
                        num = float(tnum)*1000
                    elif num.endswith("m"):
                        num = float(tnum)*1000000
                    else:
                        num =float(tnum)*1000000000
                else:
                    await ctx.send("`EN0006`: Number input error")
                    return
            else:
                if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", num):
                    num = float(num.replace(",", ""))
                else:
                    await ctx.send("`EN0006`: Number input error")
                    return
        if "flag" in locals(): num *= {"day": 60*60*24, "hour": 60*60, "minute": 60}.get(flag, 1)
        sol = calculate.product_speed(fac, "all", num)
        if sol[0] == "None":
            cs_pd = "None"
        else:
            cs_pd = list(sol[0].keys())
            cs_sp = list(sol[0].values())
        if sol[1] != "None:":
            pd_pd = list(sol[1].keys())
            pd_sp = list(sol[1].values())
        else:
            pd_pd = "None"
        s = []
        s2 = []
        if not cs_pd == "None":
            for a, b in zip(cs_pd, cs_sp):
                try:
                    float(b)
                    b = f"{float(b):,}"
                except:
                    b = b.split(".")
                    b = f"{int(b[0]):,}.{b[1]}"
                s.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", b))))
            c = "\n".join(s)
        else:
            c = "None"
        if not pd_pd == "None":
            for a, b in zip(pd_pd, pd_sp):
                try:
                    float(b)
                    b = f"{float(b):,}"
                except:
                    b = b.split(".")
                    b = f"{int(b[0]):,}.{b[1]}"
                s2.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", b))))
            p = "\n".join(s2)
        else:
            p = "None"
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), description="Unit: "+unit.capitalize(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Note", value="The result of this command is for calculation the basic values only, The actual production speeds may vary", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(3)
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(speed(bot))