import discord
from discord.ext import commands
import json
import datetime
import asyncio
import os
import sys
from cmds.repeating_decimal_sol import repeating_dec_sol
from cmds.calculate import calculate
from cmds.custom_exception import custom_exception
from cmds.string_handler import string_handler
from cmds.you_know import you_know
import re, time

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

class profitcomplete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["profitcomplete"]["profitcomplete"])
    async def profitcomplete(self, ctx, *, args):#facility, number
        correct = string_handler.location(str, int, args, True)
        if correct == True:
            pass
        elif correct[0] == False:
            if correct[1][0] == "int":
                raise custom_exception.MissingRequiredArgument("number")
            await ctx.send("`EN0005`: Cannot determine arguments")
            return
        elif correct == "int":
            raise custom_exception.MissingRequiredArgument("number")
        args = string_handler.filter(args, True)
        if args[0][0].startswith("--"):
            flag, fac = args[0][0].lower()[2:], args[0][1:]
            flagals = {"sec": "second", "s": "second", "min": "minute", "m": "minute", "hr": "hour", "h": "hour", "d": "day"}
            if flag in flagals: flag = flag; unit = flag
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
            await ctx.send("`EN0004`: Invalid facility: {}".format(" ".join(args[0])))
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
        facratio = calculate.facratio(fac, num)
        firstfac = calculate.firstfac(fac, facratio[2])
        remain = calculate.produce_remain(fac, facratio[2], num, firstfac[2])
        if "flag" in locals(): num *= {"day": 60*60*24, "hour": 60*60, "minute": 60}.get(flag, 1)
        sol = calculate.product_profit(fac, "all", num)
        soland = calculate.product_profitpland(fac, "all", num, firstfac[2])
        s2 = []
        count = 0
        for a in (sol[0], sol[1], soland[1]):
            s = []
            if not a == "None":
                for b, c in zip(a.keys(), a.values()):
                    try:
                        float(c)
                        c = f"{float(c):,}"
                    except:
                        c = c.split(".")
                        c = f"{int(c[0]):,}.{c[1]}"
                    if count != 2: s.append(" | ".join(list(("**"+b.capitalize().replace("_", " ")+"**", "$"+c))))
                    else: s.append(" | ".join(list(("**"+b.capitalize().replace("_", " ")+"**", "$"+c+"/land"))))
                s2.append("\n".join(s))
            else:
                s2.append("None")
            count+=1
        c, p, pland = s2
        if type(sol[2]) == list:
            pfs = sol[2]
            for a in list(pfs[0].values()):
                try:
                    float(a)
                    a = f"{float(a):,}"
                except:
                    a = a.split(".")
                    a = f"{int(a[0]):,}.{a[1]}"
                pf = "**Max** | $"+a+"\n"
            for a in list(pfs[1].values()):
                try:
                    float(a)
                    a = f"{float(a):,}"
                except:
                    a = a.split(".")
                    a = f"{int(a[0]):,}.{a[1]}"
                pf += "**Min** | $"+a
        else:
            pf = sol[2]
            try:
                float(pf)
                pf = f"{float(pf):,}"
            except:
                pf = pf.split(".")
                pf = f"{int(pf[0]):,}.{pf[1]}"
            pf = "$"+pf
        if type(soland[2]) == list:
            pfs = soland[2]
            for a in list(pfs[0].values()):
                try:
                    float(a)
                    a = f"{float(a):,}"
                except:
                    a = a.split(".")
                    a = f"{int(a[0]):,}.{a[1]}"
                pfland = "**Max** | $"+a+"/land\n"
            for a in list(pfs[1].values()):
                try:
                    float(a)
                    a = f"{float(a):,}"
                except:
                    a = a.split(".")
                    a = f"{int(a[0]):,}.{a[1]}"
                pfland += "**Min** | $"+a+"/land"
        else:
            pfland = soland[2]
            try:
                float(pfland)
                pfland = f"{float(pfland):,}"
            except:
                pfland = pfland.split(".")
                pfland = f"{int(pfland[0]):,}.{pfland[1]}"
            pfland = "$"+pfland+"/land"
        rem = []
        for a, b in remain[0]:
            try:
                float(b)
                b = f"{float(b):,}"
            except:
                b = b.split(".")
                b = f"{int(b[0]):,}.{b[1]}"
            rem.append("**"+a.capitalize()+"** | "+b)
        rem.append("")
        for a, b in remain[1]:
            try:
                float(b)
                b = f"{float(b):,}"
            except:
                b = b.split(".")
                b = f"{int(b[0]):,}.{b[1]}"
            rem.append("**"+a.capitalize()+"** | $"+b)
        rem = "\n".join(rem)
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), description="Unit: "+unit.capitalize(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p+"\n\n"+pland, inline=False)
        embed.add_field(name="Profit", value=pf+"\n\n"+pfland, inline=False)
        embed.add_field(name="Complete Information", value="Ratio(order follow to above): "+facratio[0]+" "+facratio[1]+"\n\n**First Facility(First Fac)/Require facilities:**\n"+firstfac[0]+"\n"+firstfac[1], inline=False)
        embed.add_field(name="Produce Remains", value=rem, inline=False)
        embed.add_field(name="Note", value="The result of this command is for calculation the basic values only, the actual profit may vary.\nThe calculation on **profit** also takes into account the consumption of the facility. While the **produce** section describes the gross profit without taking into account consumption.", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(3)
        await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(profitcomplete(bot))