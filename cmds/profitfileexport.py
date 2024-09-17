import discord
from discord.ext import commands
import json
import datetime
import asyncio
import os, io, pathlib
import sys
from cmds.repeating_decimal_sol import repeating_dec_sol
from cmds.calculate import calculate
from cmds.custom_exception import custom_exception
from cmds.string_handler import string_handler
from cmds.you_know import you_know
import re, time
import zipfile

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)
with open("profitfiledata.json", mode="r", encoding="utf8") as f:
    pffdt = json.load(f)

class profitfileexport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["profitfileexport"]["profitfileexport"])
    async def profitfileexport(self, ctx, *, args=""):
        args = args.split(" ")
        theals = {"sec": "second", "s": "second", "min": "minute", "m": "minute", "hr": "hour", "h": "hour", "d": "day"}
        flags = [a for a in args if a.startswith("--")]
        oriargs = args
        args = list(set(args)-set(flags))
        comp = emb = pastver = False
        if "--zip" in flags:
            if oriargs.index("--zip") != 0:
                await ctx.send("`EN0007`: The position of flag is invalid")
                return
            comp = True
            flags.remove("--zip")
        if "--embed" in flags:
            if oriargs.index("--embed") != 0:
                await ctx.send("`EN0007`: The position of flag is invalid")
                return
            emb = True
            flags.remove("--embed")
        if "--Beta" in flags:
            if (oriargs.index("--Beta") != 0) and (oriargs.index("--Beta") != 1 and len([a for a in oriargs if a.startswith("--")]) != 2):
                await ctx.send("`EN0007`: The position of flag is invalid")
                return
            pastver = True
            flags.remove("--Beta")
        if len(flags) > 0:
            await ctx.send("`EN0003`: Invalid flag detected")
            return
        if len(args) > 2:
            await ctx.send("`EN0006`: Too many arguments")
            return
        t = 0
        if not args:
            arg = ""
        else:
            arg, = args
        for a in [arg]:
            if pastver:
                pasts = [("1.0" if a[8:]=="p" else a[10:]) for a in os.listdir(r"icpfiles/Ori-files")]
                if a in pasts:
                    if comp:
                        resf = discord.File(r"icpfiles/RARs/"+os.listdir(r"icpfiles/RARs")[pasts.index(a)])
                    else:
                        resf = discord.File(r"icpfiles/Ori-files/"+os.listdir(r"icpfiles/Ori-files")[pasts.index(a)]+r"/profit.txt")
                    await ctx.send("Version: v.Beta."+a, file=resf)
                    return
                elif not a:
                    if comp: resf = discord.File(r"icpfiles/RARs/"+os.listdir(r"icpfiles/RARs")[-1])
                    else: resf = discord.File(r"icpfiles/Ori-files/"+os.listdir(r"icpfiles/Ori-files")[-1]+r"/profit.txt")
                    await ctx.send("Version: v.Beta."+pasts[-1], file=resf)
                    return
                else:
                    await ctx.send("`EN0004`: Invalid Beta version")
                    return
            else:
                if a in pffdt: ver = a
                else: ver = list(pffdt.keys())[-1]
                t+=1
        if arg:
            if arg not in list(theals.keys())+list(theals.values()):
                await ctx.send("`EN0004`: Invalid argument detected")
                return
            if arg in theals.values(): unit = arg
            elif arg in theals: unit = theals[arg]
            else:
                await ctx.send("`EN0003`: Invalid flag")
                return
        else: unit = "second"
        with open("icdetail.json", mode="r", encoding="utf8") as f:
            icd = json.load(f)
        result = []
        num = {"day": 60*60*24, "hour": 60*60, "minute": 60}.get(unit, 1)
        for fac in icd["facilities"]:
            facratio = calculate.facratio(fac)
            if emb: firstfac = calculate.firstfac(fac, facratio[2])
            else: firstfac = calculate.firstfac(fac, facratio[2], True)
            remain = calculate.produce_remain(fac, facratio[2], 1, firstfac[2])
            sol = calculate.product_profit(fac, "all", num)
            soland = calculate.product_profitpland(fac, "all", num, firstfac[2])
            if type(icd["facilities"][fac]["speed"]) == list or fac == "car_factory":
                print(("facratio", facratio), ("firstfac", firstfac), ("remain", remain), ("sol", sol), ("soland", soland), sep="\n\n")
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
                        if emb:
                            if count != 2: s.append(" | ".join(list(("> **"+b.capitalize().replace("_", " ")+"**", "$"+c))))
                            else: s.append(" | ".join(list(("**"+b.capitalize().replace("_", " ")+"**", "$"+c+"/land"))))
                        else:
                            if count != 2: s.append(" | ".join(list(("| "+b.capitalize().replace("_", " "), "$"+c))))
                            else: s.append(" | ".join(list(("| "+b.capitalize().replace("_", " "), "$"+c+"/land"))))
                    s2.append("\n".join(s))
                else:
                    if emb:s2.append(">  None")
                    else: s2.append("| None")
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
                    if emb: pf = "> **Max** | $"+a+"\n"
                    else: pf = "| Max | $"+a+"\n"
                for a in list(pfs[1].values()):
                    try:
                        float(a)
                        a = f"{float(a):,}"
                    except:
                        a = a.split(".")
                        a = f"{int(a[0]):,}.{a[1]}"
                    if emb: pf += "> **Min** | $"+a
                    else: pf += "| Min | $"+a
            else:
                pf = sol[2]
                try:
                    float(pf)
                    pf = f"{float(pf):,}"
                except:
                    pf = pf.split(".")
                    pf = f"{int(pf[0]):,}.{pf[1]}"
                if emb: pf = "> $"+pf
                else: pf = "| $"+pf
            if type(soland[2]) == list:
                pfs = soland[2]
                for a in list(pfs[0].values()):
                    try:
                        float(a)
                        a = f"{float(a):,}"
                    except:
                        a = a.split(".")
                        a = f"{int(a[0]):,}.{a[1]}"
                    if emb: pfland = "> **Max** | $"+a+"\n"
                    else: pfland = "| Max | $"+a+"\n"
                for a in list(pfs[1].values()):
                    try:
                        float(a)
                        a = f"{float(a):,}"
                    except:
                        a = a.split(".")
                        a = f"{int(a[0]):,}.{a[1]}"
                    if emb: pfland += "> **Min** | $"+a
                    else: pfland += "| Min | $"+a
            else:
                pfland = soland[2]
                try:
                    float(pfland)
                    pfland = f"{float(pfland):,}"
                except:
                    pfland = pfland.split(".")
                    pfland = f"{int(pfland[0]):,}.{pfland[1]}"
                if emb: pfland = "> $"+pfland+"/land"
                else: pfland = "| $"+pfland+"/land"
            rem = []
            for a, b in remain[0]:
                try:
                    float(b)
                    b = f"{float(b):,}"
                except:
                    b = b.split(".")
                    b = f"{int(b[0]):,}.{b[1]}"
                if emb: rem.append("> **"+a.capitalize()+"** | "+b)
                else: rem.append("| "+a.capitalize()+" | "+b)
            if emb: rem.append("> ")
            else: rem.append("------")
            for a, b in remain[1]:
                try:
                    float(b)
                    b = f"{float(b):,}"
                except:
                    b = b.split(".")
                    b = f"{int(b[0]):,}.{b[1]}"
                if emb: rem.append("> **"+a.capitalize()+"** | $"+b)
                else: rem.append("| "+a.capitalize()+" | $"+b)
            rem = "\n".join(rem)
            if type(icd["facilities"][fac]["speed"])==list:
                sp = [str(a)+"s" for a in icd["facilities"][fac]["speed"]]
                sp.insert(1, "to")
            if emb: result.append([fac.capitalize().replace("_", " "), "**Construct materials**\n"+"\n".join([f"> **{a.capitalize().replace('_', ' ')}** | {b}" if a != "money" else f"> ${b}" for a, b in icd["info"]["facilities"][fac]["construct"].items()])+"\n\n**Consumes**\n"+c+"\n**Produces**\n"+p+"\n\n**Profit**\n"+pf+"\n\nRatio(order follow to above): "+facratio[0]+" "+facratio[1]+"\nFirst Facility(First Fac)\n"+firstfac[0]+"\n"+firstfac[1]+"\n**Produce Remains**\n"+rem+"\n"+"Speed: "+(" ".join(sp) if type(icd["facilities"][fac]["speed"])==list else str(icd["facilities"][fac]["speed"])+"s")+"\n\n\n_ _"])
            else: result.append(fac.capitalize().replace("_", " ")+"\nConstruct materials\n"+"\n".join([f"| {a.capitalize().replace('_', ' ')} | {b}" if a != "money" else f"| ${b}" for a, b in icd["info"]["facilities"][fac]["construct"].items()])+"\nConsumes\n"+c+"\nProduces\n"+p+"\nProfit\n"+pf+"\nRatio(order follow to above): "+facratio[0]+" "+facratio[1]+"\nFirst Facility(First Fac)\n"+firstfac[0]+"\n"+firstfac[1]+"\nProduce Remains\n------\n"+rem+"\n------\n"+"Speed: "+(" ".join(sp) if type(icd["facilities"][fac]["speed"])==list else str(icd["facilities"][fac]["speed"])+"s"))
        # embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), description="Unit: "+unit.capitalize(), timestamp= datetime.datetime.now())
        # embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        # embed.add_field(name="Consumes", value=c, inline=False)
        # embed.add_field(name="Produces", value=p+"\n\n"+pland, inline=False)
        # embed.add_field(name="Profit", value=pf+"\n\n"+pfland, inline=False)
        # embed.add_field(name="Complete Information", value="Ratio(order follow to above): "+facratio[0]+" "+facratio[1]+"\n\n**First Facility(First Fac)/Require facilities:**\n"+firstfac[0]+"\n"+firstfac[1], inline=False)
        # embed.add_field(name="Produce Remains", value=rem, inline=False)
        # embed.add_field(name="Note", value="The result of this command can't get anything of region(s).\nThe **profit** is meaning that if your sourse of the facility is from buying from npc market, then the profit, if you are not buying the sourse from npc market, then the **produces** part.", inline=False)
        # embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        if not emb:
            ver = list(pffdt)[-1]
            fdt = io.BytesIO(("Unit: "+unit.capitalize()+"\n\n"+"\n\n".join(result)).encode())
            if comp:
                faclist = []
                for a in icd["facilities"]:
                    stuff = []
                    i = [0, 0]
                    for b, c in icd["facilities"][a].items():
                        if b in ("consumes", "produces"):
                            e = ["consumes", "produces"].index(b)
                            if i[e]==0:
                                stuff.append(b.capitalize())
                            if c == "None":
                                stuff.append("| None")
                            else:
                                for d, f in c.items():
                                    if d == "money":
                                        stuff.append(f"| ${f}")
                                    stuff.append("| {} | {}".format(d.capitalize().replace("_", " "), f))
                        if b == "consumes": i[0]+=1
                        else: i[1]+=1
                    if type(icd["facilities"][a]["speed"]) == list:
                        speed = []
                        for b in icd["facilities"][a]["speed"]:
                            b = string_handler.numberToBase(b, 60)
                            if len(b)<2: b.insert(0, 0)
                            speed.append(":".join(["0"+str(a) if len(str(a))<2 else str(a) for a in b]))
                        speed.insert(1, "to")
                        speed = " ".join(speed)
                    else:
                        b = string_handler.numberToBase(icd["facilities"][a]["speed"], 60)
                        if len(b)<2: b.insert(0, 0)
                        speed = ":".join(["0"+str(a) if len(str(a))<2 else str(a) for a in b])
                    faclist.append(a.capitalize().replace("_", " ")+"\nConstruct materials\n"+"\n".join([f"| {a.capitalize().replace('_', ' ')} | {b}" if a != "money" else f"| ${b}" for a, b in icd["info"]["facilities"][a]["construct"].items()])+"\n"+"\n".join(stuff)+"\nEvery "+speed)
                facspeed = []
                num = {"day": 60*60*24, "hour": 60*60, "minute": 60}.get(unit, 1)
                for f in icd["facilities"]:
                    sol = calculate.product_speed(f, "all", num)
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
                    stuff = ["Consumes"]
                    if not cs_pd == "None":
                        for a, b in zip(cs_pd, cs_sp):
                            try:
                                float(b)
                                b = f"{float(b):,}"
                            except:
                                b = b.split(".")
                                b = f"{int(b[0]):,}.{b[1]}"
                            s.append("| "+" | ".join((a.capitalize().replace("_", " "), b)))
                        stuff.append("\n".join(s))
                    else:
                        stuff.append("| None")
                    stuff.append("Produces")
                    if not pd_pd == "None":
                        for a, b in zip(pd_pd, pd_sp):
                            try:
                                float(b)
                                b = f"{float(b):,}"
                            except:
                                b = b.split(".")
                                b = f"{int(b[0]):,}.{b[1]}"
                            s2.append("| "+" | ".join((a.capitalize().replace("_", " "), b)))
                        stuff.append("\n".join(s2))
                    else:
                        stuff.append("| None")
                    if type(icd["facilities"][f]["speed"]) == list:
                        speed = []
                        for b in icd["facilities"][f]["speed"]:
                            b = string_handler.numberToBase(b, 60)
                            if len(b)<2: b.insert(0, 0)
                            speed.append(":".join(["0"+str(a) if len(str(a))<2 else str(a) for a in b]))
                        speed.insert(1, "to")
                        speed = " ".join(speed)
                    else:
                        b = string_handler.numberToBase(icd["facilities"][f]["speed"], 60)
                        if len(b)<2: b.insert(0, 0)
                        speed = ":".join(["0"+str(a) if len(str(a))<2 else str(a) for a in b])
                    facspeed.append(f.capitalize().replace("_", " ")+"\n"+"\n".join(stuff)+"\nEvery "+speed)
                with io.BytesIO() as buffer:
                    zf = zipfile.ZipFile(buffer, "x", zipfile.ZIP_DEFLATED, compresslevel=9)
                    zf.writestr("profit.txt", fdt.getvalue())
                    zf.writestr("facility_list.txt", io.BytesIO("\n\n".join(faclist).encode()).getvalue())
                    zf.writestr("production_speed.txt", io.BytesIO(("Unit: "+unit.capitalize()+"\n\n"+"\n\n".join(facspeed)).encode()).getvalue())
                    for a, b in pffdt[ver].items():
                        zf.writestr(a, io.BytesIO("\n".join(b).encode()).getvalue())
                    zf.close()
                    buffer.seek(0)
                    resf = discord.File(buffer, "IdleCorp Profit.zip")
            else: resf = discord.File(fdt, "profit.txt")
            await ctx.send(content="Version: v."+ver, file=resf)
        else:
            embed = [discord.Embed(title="Profit Embed Full")]
            check = 0
            for a, b in result:
                if check+len(a+b) > 5800:
                    embed.append(discord.Embed())
                    check = 0
                check+=len(a+b)
                if len(b)>1024:
                    b = b.split("\n")
                    embed[-1].add_field(name=a, value="\n".join(b[:len(b)//2]), inline=False)
                    embed[-1].add_field(name="_ _", value="\n".join(b[len(b)//2:]), inline=False)
                else:
                    embed[-1].add_field(name=a, value=b, inline=False)
            for a in embed:
                if not ctx.author.dm_channel:
                    await ctx.author.create_dm()
                await ctx.author.dm_channel.send(embed=a)
            await ctx.send("It has sent via your DM")
        # ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        # ukwembed.add_field(name="_ _", value=you_know.you_know())
        # ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        # ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        # msg = await ctx.send(embed=ukwembed)
        # time.sleep(3)
        # await msg.edit(embed=embed)
        # await msg.edit(content="Version:", embed=None, file=resf)

def setup(bot):
    bot.add_cog(profitfileexport(bot))