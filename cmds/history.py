from pathlib import Path
import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.calculate import calculate
import os
from cmds.string_handler import string_handler
from cmds.custom_exception import custom_exception
from cmds.calculate import calculate
from PIL import Image, ImageColor, ImageDraw, ImageFont
import re, textwrap, random
from cmds.repeating_decimal_sol import repeating_dec_sol
import fractions
from collections import deque
import bitdotio

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)
with open("icdetail.json", mode="r", encoding="utf8") as f:
    icd = json.load(f)
with open("help.json", mode="r", encoding="utf8") as f:
    hps = json.load(f)
with open("rules.json", mode="r", encoding="utf8") as f:
    rulej = json.load(f)
with open("updates.json", mode="r", encoding="utf8") as f:
    udslist = json.load(f)

db = bitdotio.bitdotio("6cCg_cknNfbKVqNk84Q2JeV8vVXL")

class history(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][0])
    async def history(self, ctx):
        await ctx.send("History `command`:\n`Alpha_0_1`\n`Alpha_0_2_1`\n`Alpha_0_3_0`"
        "\n`Beta_0_1_0`\n`Beta_0_2_0`\n`Beta-0_3_0`\n`Beta_0_4_0`\n`Beta_0_5_0`\n`Beta_0_6_0`\n`Beta_0_6_1`"
        "\n\nNote:\nAliases system not include in here\n"
        "\n`Stable_1_0`\n`Stable_1_0_1`\n`Stable_1_0_2`"
        "History `server_icon`:\n`1`"
        "\nHistory for history points and timestamps:\n`server`\n`idlecorpprofit`"
        "Suggest for more, or suggest more aliases")
    
    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Alpha_0_1"][0])
    async def Alpha_0_1(self, ctx):
        await ctx.send("History: Alpha_0_1 commands:\n`command`")
    
    @Alpha_0_1.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandA01(self, ctx):
        await ctx.send("History: Command commands:\n`profit`")

    @commandA01.command(aliases=als["cogs"]["history"]["history"][1]["Alpha_0_1"][1]["profit"])
    async def profit(self, ctx, fac, typ, num: int=1):
        if num == 1:
            sol = calculate.product_speed(fac, typ)
        else:
            sol = calculate.product_speed(fac, typ, num)
        pd = list(sol.keys())
        sp = list(sol.values())
        s = []
        for a, b in zip(pd, sp):
            s.append(" | ".join(list((a, b))))
        c = "\n".join(s)
        embed = discord.Embed(title=fac)

        await ctx.send(f"{fac}```\n{c}\n```")

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Alpha_0_2_1"][0])
    async def Alpha_0_2_1(self, ctx):
        await ctx.send("History: Alpha_0_2_1 commands:\n`command`")

    @Alpha_0_2_1.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    @commands.has_role("Owner")
    async def commandA021(self, ctx):
        await ctx.send("History: Command commands:\n`listcogs`")
    
    @commandA021.command(aliases=als["cogs"]["history"]["history"][1]["Alpha_0_2_1"][1]["listcogs"])
    @commands.has_role("Owner")
    async def listcogs(self, ctx):
        for filename in os.listdir('./cmds'):
            if filename.endswith('.py'):
                lists = (f'{filename[:-3]}')
                await ctx.send(lists)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Alpha_0_3_0"][0])
    async def Alpha_0_3_0(self, ctx):
        await ctx.send("History: Alpha_0_3_0 commands:\n`command`")

    @Alpha_0_3_0.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandA030(self, ctx):
        await ctx.send("History: Command commands:\n`speed`\n`profit`")

    @commandA030.command(aliases=als["cogs"]["history"]["history"][1]["Alpha_0_3_0"][1]["speed"])
    async def speed(self, ctx, *, args):#facilities, number
        correct = string_handler.location(str, int, args)
        if correct == True:
            pass
        elif correct[0] == False:
            if correct[1][0] == "int":
                raise custom_exception.MissingRequiredArgument("number")
            await ctx.send("Can't determind arguments")
            return
        elif correct == "int":
            raise custom_exception.MissingRequiredArgument("number")
        args = string_handler.filter(args)
        fac = args[0]
        num = args[1]
        if num == []:
            num = 1
        fac = "_".join(fac)
        if type(num) == list: 
            for a in num:
                num = a
        sol = calculate.product_speed(fac, "all", num)
        print(sol)
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
                s.append(" | ".join(list(("**"+a.replace("_", " ")+"**", b))))
            c = "\n".join(s)
        else:
            c = "None"
        if not pd_pd == "None":
            for a, b in zip(pd_pd, pd_sp):
                s2.append(" | ".join(list(("**"+a.replace("_", " ")+"**", b))))
            p = "\n".join(s2)
        else:
            p = "None"
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_, color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandA030.command(aliases=als["cogs"]["history"]["history"][1]["Alpha_0_3_0"][1]["profit"])
    async def profit(self, ctx, *, args):#facility, number
        correct = string_handler.location(str, int, args)
        if correct == True:
            pass
        elif correct[0] == False:
            if correct[1][0] == "int":
                raise custom_exception.MissingRequiredArgument("number")
            await ctx.send("Can't determind arguments")
            return
        elif correct == "int":
            raise custom_exception.MissingRequiredArgument("number")
        args = string_handler.filter(args)
        fac = args[0]
        num = args[1]
        if num == []:
            num = 1
        fac = "_".join(fac)
        if type(num) == list: 
            for a in num:
                num = a
        sol = calculate.product_profit(fac, "all", num)
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
                s.append(" | ".join(list(("**"+a.replace("_", " ")+"**", "$"+b))))
            c = "\n".join(s)
        else:
            c = "None"
        if not pd_pd == "None":
            for a, b in zip(pd_pd, pd_sp):
                s2.append(" | ".join(list(("**"+a.replace("_", " ")+"**", "$"+b))))
            p = "\n".join(s2)
        else:
            p = "None"
        if type(sol[2]) == list:
            pfs = sol[2]
            for a in list(pfs[0].values()):
                pf = "**Max** | $"+a+"\n"
            for a in list(pfs[1].values()):
                pf += "**Min** | $"+a
        else:
            pf = "$"+sol[2]
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_, color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Profit", value=pf, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Beta_0_1_0"][0])
    async def Beta_0_1_0(self, ctx):
        await ctx.send("History: Beta_1_0 commands:\n`command`")

    @Beta_0_1_0.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandB010(self, ctx):
        await ctx.send("History: Command commands:\n`ping`\n`version`")

    @commandB010.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_1_0"][1]["ping"])
    async def ping(self, ctx):
        await ctx.send(f'**{round(self.bot.latency*1000, 2)}** ms')

    @commandB010.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_1_0"][1]["version"])
    async def version(self, ctx):
        await ctx.send(f"The bot version is: **{jdata['version']}**")

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Beta_0_2_0"][0])
    async def Beta_0_2_0(self, ctx):
        await ctx.send("History: Beta_2_0 commands:\n`command`")

    @Beta_0_2_0.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandB020(self, ctx):
        await ctx.send("History: Command commands:\n`speed`\n`profit`")

    @commandB020.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_2_0"][1]["speed"])
    async def speed(self, ctx, *, args):#facilities, number
        correct = string_handler.location(str, int, args)
        if correct == True:
            pass
        elif correct[0] == False:
            if correct[1][0] == "int":
                raise custom_exception.MissingRequiredArgument("number")
            await ctx.send("Can't determind arguments")
            return
        elif correct == "int":
            raise custom_exception.MissingRequiredArgument("number")
        args = string_handler.filter(args)
        fac = args[0]
        num = args[1]
        if num == []:
            num = 1
        fac = "_".join(fac)
        if type(num) == list: 
            for a in num:
                num = a
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
                s.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", b))))
            c = "\n".join(s)
        else:
            c = "None"
        if not pd_pd == "None":
            for a, b in zip(pd_pd, pd_sp):
                s2.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", b))))
            p = "\n".join(s2)
        else:
            p = "None"
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB020.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_2_0"][1]["profit"])
    async def profit(self, ctx, *, args):#facility, number
        correct = string_handler.location(str, int, args)
        if correct == True:
            pass
        elif correct[0] == False:
            if correct[1][0] == "int":
                raise custom_exception.MissingRequiredArgument("number")
            await ctx.send("Can't determind arguments")
            return
        elif correct == "int":
            raise custom_exception.MissingRequiredArgument("number")
        args = string_handler.filter(args)
        fac = args[0]
        num = args[1]
        if num == []:
            num = 1
        fac = "_".join(fac)
        if type(num) == list: 
            for a in num:
                num = a
        sol = calculate.product_profit(fac, "all", num)
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
                s.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
            c = "\n".join(s)
        else:
            c = "None"
        if not pd_pd == "None":
            for a, b in zip(pd_pd, pd_sp):
                s2.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
            p = "\n".join(s2)
        else:
            p = "None"
        if type(sol[2]) == list:
            pfs = sol[2]
            for a in list(pfs[0].values()):
                pf = "**Max** | $"+a+"\n"
            for a in list(pfs[1].values()):
                pf += "**Min** | $"+a
        else:
            pf = "$"+sol[2]
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Profit", value=pf, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB020.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_2_0"][1]["search"])
    async def search(self, ctx, ctn=None):
        if ctn == None:
            await ctx.send("What you want to search?Just need to enter something.")
        else:
            embed = discord.Embed(title="Search", color=discord.Color.from_rgb(int("35", 16), int("12", 16), int("38", 16)), timestamp= datetime.datetime.now())
            imgname = ""
            if not str(datetime.datetime.now().date()) == "2021-04-01":
                embed.add_field("Haven't this command", "This command is not usable")
                await ctx.send(embed=embed)
                return
            if ctn == "when":
                embed.add_field(name="Result", value="ERROR: Time collection! Pleace make sure you have time to do this and try again")
                img = Image.new("1", (100, 100), 255)
                font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
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
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
            elif ctn == "end":
                embed.add_field(name="Result", value="When UTC...")
                img = Image.new("1", (100, 100), 255)
                font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
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
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
            await ctx.send(file=discord.File(imgname), embed=embed)
            if imgname:
                os.remove(imgname)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["server_icon"][0])
    async def server_icon(self, ctx):
        await ctx.send("Server icon version: `1`")

    @server_icon.command(name="1", aliases=als["cogs"]["history"]["history"][1]["server_icon"][1]["1"])
    async def one(self, ctx):
        embed = discord.Embed(title="Server icon", description="Version 1 (v.1)", color=discord.Colour.light_gray(), timestamp= datetime.datetime.now())
        image = discord.File("ICP server icon v1.png", filename="icon.png")
        embed.set_thumbnail(url="attachment://icon.png")
        embed.add_field(name="Server Icon on the right side", value="You can see what's the difference of them.")
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(file=image, embed=embed)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Beta_0_3_0"][0])
    async def Beta_0_3_0(self, ctx):
        await ctx.send("History: Beta_3_0 commands:\n`command`")

    @Beta_0_3_0.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandB030(self, ctx):
        await ctx.send("History: Command commands:\n`help`\n`info`\n`profit`\n`rules`\n`search`\n`speed`\n`updates`")

    @commandB030.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_3_0"][1]["help"])
    async def help(self, ctx, *, cmd=None):
        if cmd == None:
            embed = discord.Embed(title="Help", description="Won't show Admin's, Owner's, Developer's commands", color=discord.Colour.green(), timestamp= datetime.datetime.now())
            for a, b in hps["commands"].items():
                embed.add_field(name=a.capitalize(), value=f"Descriptions/Features: {b[0]}\nSyntax: {b[1]}", inline=False)
        else:
            can = True
            cd = cmd
            cmds = cmd.split()
            if len(cmds) == 3:
                if cmds[-1] == "command":
                    cmds = [cmds[0]]+["command"]
            out = []
            for a, b in hps["info"]["aliases"].items():
                for e, f in b.items():
                    for a in cmds:
                        if isinstance(f, dict):
                            if ("__init__" in f) and (a in f["__init__"]):
                                    out.append(e)
                            else:
                                g = f

                                for c, d in g.items():
                                    if a in d:
                                        out.append(c)
                                    elif isinstance(d, dict):
                                        if "__init__" in d and d["__init__"] == a:
                                            out.append(d["__init__"])
                                            continue
                                    g = d
                        elif a in f:
                            out.append(e)
            cmds = out
            embed = discord.Embed(title="Help -- "+cmds[0].capitalize(), color=discord.Colour.green(), timestamp= datetime.datetime.now())
            res = hps["commands"][cmds[0]]
            for a, b in hps["info"].items():
                if a == "aliases":
                    for c, d in b.items():
                        e = d
                        for cmd in cmds:
                            if cmd not in e: continue
                            e = e[cmd]
                        res.append(f["__init__"] if isinstance(f, dict) else f)
                        can = False
                        break
                elif a == "details":
                    for c, d in b.items():
                        e = d
                        for cmd in cmds:
                            if cmd not in e: continue
                            e = e[cmd]
                        if type(e) == dict and "__init__" not in e: continue
                        s = e["__init__"] if isinstance(e, dict) else e
                        if not s: break
                        # if re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s):
                        #     if re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s) == "-1":
                        #         s = s.format(cmds[-1])
                        #     elif re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s) == "-2":
                        #         s - s.format(cmds[-2])
                        if "{" and "}" in s: s - s.format(**zip([str(-g) for g in range(1, len(cmds)+1)[::-1]], cmds[:-1]))
                        res.append(s)
                        can = False
                        break
            if can == True:
                await ctx.send("Cannot find command info named `{}`".format(cd))
                return
            out = [("Description: "+res[0])]+[("Syntax: "+res[1])]+[("Aliases: "+", ".join(res[2]))]
            if len(res) == 4:
                out.append("Details: "+res[3])
            embed.add_field(name=" ".join(cmds), value="\n\n".join(out), inline=False)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB030.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_3_0"][1]["info"])
    async def info(self, ctx, *, req):
        icinfo = icd["info"]
        debug = []
        infoals = dict(list(als["ic"]["assets"].items())+list(als["ic"]["facilities"].items()))
        for a, b in infoals.items():
            if not b == None:
                if req in b:
                    debug.append(a)
            else:
                reqsl = req
        if len(debug) > 1:
            await ctx.send("Happened an unexpected or imposible thing, E1")
        elif debug:
            reqsl, = debug
        else:
            reqsl = req
        reqsl = "_".join(reqsl.split(" "))
        check = list(icinfo["assets"].keys())+list(icinfo["facilities"])
        if not reqsl in check:
            await ctx.send(f"Cannot find info of: {req}, check your input")
            return
        if reqsl in icinfo["assets"].keys():
            infoclass = "assets"
        elif reqsl in icinfo["facilities"].keys():
            infoclass = "facilities"
        theinfo = icinfo[infoclass][reqsl]
        embed = discord.Embed(title=f"Info -- {infoclass.capitalize()}", color=discord.Colour.greyple(), timestamp= datetime.datetime.now())
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="_ _", inline=False)
        output = []
        if infoclass == "assets":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            stuff = []
            if theinfo["market"] == True:
                stuff.append("It's tradable in market")
            elif theinfo["market"] == False:
                stuff.append("It's not tradable in market")
            if theinfo["retail"] == False:
                stuff.append("It cannot sold in retail store")
                stuff.append("It cannot be scrapped")
            else:
                stuff.append("It can sold in retail store")
                stuff.append("It can be scrapped into {} scraps".format(theinfo["retail"]))
            # output.append("\n".join(stuff))
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\n\n"+"\n".join(stuff), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if not als["ic"]["assets"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["assets"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if reqsl == "led":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Light-emitting_diode)")
            elif reqsl == "rubber":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/synthetic_rubber)")
            elif reqsl == "energy":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/electricity)")
            elif reqsl == "lamp":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/light_fixture)")
            elif reqsl == "ccd":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/charge-coupled_device)")
            elif reqsl == "hq":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Headquarters)")
            elif theinfo["wikipedia"] != "None":
                stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "facilities":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"], inline=False)
            stuff = []
            for a, b in theinfo["construct"].items():
                if not a == "money":
                    stuff.append(str(b)+" **"+a.capitalize()+"**")
                else:
                    stuff.append("$"+f"{b:,}")
            # output.append("**Construction materials:**\n"+"\n".join(stuff))
            embed.add_field(name="Construction materials:", value="\n".join(stuff), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if not als["ic"]["facilities"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["facilities"][reqsl]))
            else: output.append("Aliases: None")
            if reqsl == "steel_mill":
                if random.randint(1, 50) == 1:
                    output.append("*I always typo this facility as \"still mill\"*")
            if reqsl == "furniture_factory":
                if random.randint(1, 5) == 1:
                    output.append("*Why the IdleCorp Wiki page has so many words...*")
                if random.randint(1, 10) == 1:
                    output.append("*Because the IdleCorp Wiki page has too many work, I had to change the layout of all...*")
            if reqsl.split("_")[-1] == "factory":
                if random.randint(1, 20) == 1:
                    output.append("*I really want to know who made this facility page...*")
            if reqsl == "research_chemical_factory":
                if random.randint(1, 3) == 1:
                    output.append("*Why this facility has so many aliases...*")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if reqsl == "":
                stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            else:
                stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        # embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="\n\n".join(output))
        await ctx.send(embed=embed)

    @commandB030.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_3_0"][1]["profit"])
    async def profit(self, ctx, *, args):#facility, number
        correct = string_handler.location(str, int, args, True)
        if correct == True:
            pass
        elif correct[0] == False:
            if correct[1][0] == "int":
                raise custom_exception.MissingRequiredArgument("number")
            await ctx.send("Cannot determine arguments")
            return
        elif correct == "int":
            raise custom_exception.MissingRequiredArgument("number")
        args = string_handler.filter(args, True)
        fac = args[0]
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
            await ctx.send("Invalid facility: {}".format(" ".join(args[0])))
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
                    await ctx.send("Number input error")
                    return
            else:
                if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", num):
                    num = float(num.replace(",", ""))
                else:
                    await ctx.send("Number input error")
                    return
        sol = calculate.product_profit(fac, "all", num)
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
                s.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
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
                s2.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
            p = "\n".join(s2)
        else:
            p = "None"
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
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Profit", value=pf, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB030.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_3_0"][1]["rules"])
    async def rules(self, ctx, *, args=None):
        if args != None:
            arg = string_handler.filter(args)
            check = 1
            for a in arg:
                if a == []:
                    check = 0
            if check == 1:
                check = string_handler.location(str, int, args)
                if check != True:
                    await ctx.send("Arguments error")
                    return
            else:
                if args.isdigit():
                    args = int(args)
            if arg[1] != []:
                if len(arg[1]) > 1:
                    await ctx.send("Too much argument: type number")
                    return
                for a in arg[1]:
                    num = a
            else:
                num = None
            if arg[0] != []:
                if len(arg[0]) > 1:
                    await ctx.send("Too much argument: type string")
                    return
                for a in arg[0]:
                    if a.startswith("--"):
                        flag = a[2:]
                    else:
                        await ctx.send("Argument error: type string")
                        return
            else:
                flag = None
            if flag == None:
                rule = dict([next(reversed(rulej.items()))])
                for a in rule.values():
                    ru = a
                for a in rule.keys():
                    version = a
            else:
                ru = rulej[flag]
                version = flag
            if num == None:
                prints = []
                for a, b in ru.items():
                    if a == "end":
                        for c in b:
                            prints.append(c)
                        continue
                    if type(b) == list:
                        count = 1
                        for c in b:
                            if a == "head_notes":
                                prints.append("*"+c+"*")
                            elif a == "rules":
                                prints.append(f"**{count}.**"+c)
                                count += 1
                            else:
                                prints.append(c)
                    else:
                        prints.append(b)
                #Version (END)
                prints.append(f"\n**v.{version}** of the server rules")
                half = int(len(prints)/2)
                a = prints[:half]
                b = prints[half:]
                embed = discord.Embed(title="Server Rules", color=discord.Colour.orange(), timestamp= datetime.datetime.now())
                embed.add_field(name="_ _", value="\n".join(a), inline=False)
                embed.add_field(name="_ _", value="\n".join(b), inline=False)
            else:
                rule = f"**{num}.**"+ru["rules"][num-1]
                embed = discord.Embed(title="Server Rules", description=rule+f"\n\nv.{version}", color=discord.Colour.orange(), timestamp= datetime.datetime.now())
                # embed.add_field(name="Server Rules", value=rule+f"\n\nv.{version}", inline=False)
        else:
            ru = dict([next(reversed(rulej.items()))])
            for a in ru.values():
                rule = a
            for a in ru.keys():
                version = a
            prints = []
            for a, b in rule.items():
                if a == "end":
                    for c in b:
                        prints.append(c)
                    continue
                if type(b) == list:
                    count = 1
                    for c in b:
                        if a == "head_notes":
                            prints.append("*"+c+"*")
                        elif a == "rules":
                            prints.append(f"**{count}.**"+c)
                            count += 1
                        else:
                            prints.append(c)
                else:
                    prints.append(b)
            #Version (END)
            prints.append(f"\n**v.{version}** of the server rules")
            half = int(len(prints)/2)
            a = prints[:half]
            b = prints[half:]
            embed = discord.Embed(title="Server Rules", color=discord.Colour.orange(), timestamp= datetime.datetime.now())
            embed.add_field(name="_ _", value="\n".join(a), inline=False)
            embed.add_field(name="_ _", value="\n".join(b), inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB030.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_3_0"][1]["search"])
    async def search(self, ctx, ctn=None):
        if ctn == None:
            await ctx.send("What you want to search?Just need to enter something.")
        else:
            embed = discord.Embed(title="Search", color=discord.Color.from_rgb(int("35", 16), int("12", 16), int("38", 16)), timestamp= datetime.datetime.now())
            imgname = ""
            if not str(datetime.datetime.now().date()) == "2021-04-01":
                embed.add_field(name="Haven't this command", value="This command is not usable")
                await ctx.send(embed=embed)
                return
            if ctn == "when":
                embed.add_field(name="Result", value="ERROR: Time collection! Pleace make sure you have time to do this and try again")
                img = Image.new("1", (100, 100), 255)
                font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
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
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
            elif ctn == "end":
                embed.add_field(name="Result", value="When UTC...")
                img = Image.new("1", (100, 100), 255)
                font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
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
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
            await ctx.send(file=discord.File(imgname), embed=embed)
            if imgname:
                os.remove(imgname)
    
    @commandB030.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_3_0"][1]["speed"])
    async def speed(self, ctx, *, args):#facilities, number
        correct = string_handler.location(str, int, args, True)
        if correct == True:
            pass
        elif correct[0] == False:
            if correct[1][0] == "int":
                raise custom_exception.MissingRequiredArgument("number")
            await ctx.send("Can't determind arguments")
            return
        elif correct == "int":
            raise custom_exception.MissingRequiredArgument("number")
        args = string_handler.filter(args, True)
        fac = args[0]
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
            await ctx.send("Cannot find facility: {}".format(" ".join(args[0])))
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
                    await ctx.send("Number input error")
                    return
            else:
                if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", num):
                    num = float(num.replace(",", ""))
                else:
                    await ctx.send("Number input error")
                    return
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
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB030.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_3_0"][1]["updates"])
    async def updates(self, ctx, *, args=None):
        def defformver(ver):
            if ver == "Alpha.0.2":
                formver = "Alpha.1"
            elif ver in ("Alpha.0.2.1", "Alpha.0.3.0", "Beta.0.1.0"):
                formver = "Alpha.2"
            else:
                formver = "Alpha.2"
            return formver
        if args != None:
            arg = string_handler.filter(args)
            if arg[1]:
                await ctx.send("Argument error: type number")
                return
            flags = string_handler.flags(arg[0])
            if flags[1]:
                await ctx.send("Argument error: type string1")
                return
            if len(flags[0]) > 1:
                await ctx.send("Argument error: type string2")
                return
            elif len(flags[0]) == 1:
                for a in flags[0]:
                    flag = a
            else:
                flag = None
            if flag != None:
                if arg[0].index(flag) > 0:
                    await ctx.send("Argument error: type string3")
                    return
            if flag != None:
                flag = flag[2:]
            if len(flags[2]) > 1:
                await ctx.send("Argument error: type string4")
                return
            elif len(flags[2]) == 1:
                for a in flags[2]:
                    mores = a
            else:
                mores = None
            if flag == None:
                theud = dict([next(reversed(udslist.items()))])
                for a in theud.keys():
                    version = a
                for a in theud.values():
                    ud = a
            else:
                ud = udslist[flag]
                version = flag
            if mores != None:
                more = mores.split(".")
                stuff = []
                for a in more:
                    stuff.append(a.replace("_", " "))
                # if len(more) == 1:
                #     for a in more:
                #         for c, d in als["updates list"]["first"].items():
                #             if a in c:
                #                 a = c
                #         prints =  ud[a]
                # else:
                fn = ""
                b = ud
                first = als["updates list"]["first"]
                second = als["updates list"]["second"]
                third = als["updates list"]["third"]
                i = 0
                moo = []
                for a in more:
                    if i == 0:
                        for c, d in first.items():
                            if a in d:
                                a = c
                                f = c
                    else:
                        if f != "plans to update":
                            for c, d in second.items():
                                if a in d:
                                    a = c
                        else:
                            for c, d in third.items():
                                if a in d:
                                    a = c
                    b = b[a]
                    moo.append(a)
                    i += 1
                more = moo
                store = b
                nothing = "\n**Nothing to show**"
                if not store:
                    prints = nothing
                else:
                    if type(store) == list:
                        prints = "\n".join(store)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == dict:
                        noth = 0
                        store2 = []
                        for a, b in store.items():
                            if more[0] == "commands":
                                if a in ("adds", "changes", "deletes"):
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            if a.istitle():
                                                store2.append(a+" -- "+b)
                                            else:
                                                store2.append("`"+a+"` -- "+b)
                                        # prints = "\n".join(store)
                                else:
                                    if a.istitle():
                                        store2.append(+a+" -- "+b)
                                    else:store2.append("`"+a+"` -- "+b)
                            elif more[0] == "other":
                                if b:
                                    store2.append("\""+a+"\" -- "+b)
                            elif more[0] == "plans to update":
                                if a in ud["plans to update"].keys():
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            store2.append("\""+a.capitalize()+"\" -- "+b.capitalize())
                                        # prints = "\n".join(store)
                                else:
                                    store2.append("\""+a.capitalize()+"\" -- "+b.capitalize())
                        if store2:
                            prints = "\n".join(store2)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == str:
                        if len(store.split(" ")) == 1:
                            prints = store.capitalize()
                        else:
                            prints = store
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                prints += f"\n\nVersion: **v.{version}**"
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                embed.add_field(name=version+fn, value=prints, inline=False)
            else:
                formver = defformver(version)
                prints = []
                for a, b in ud.items():
                    if type(b) == list:
                        if not b:
                            continue
                        if formver == "Alpha.1":
                            if a == "note":
                                A1 = ""
                            else:
                                A1 = ":"
                        else:
                            A1 = ":"
                        prints.append("**"+a.capitalize()+A1+"**")
                        for c in b:
                            prints.append("> "+c)
                    elif type(b) == dict:
                        prints.append("**"+a.capitalize()+":**")
                        for c, d in b.items():
                            if not d:
                                continue
                            if a == "other":
                                prints.append("> \""+c+"\" -- "+d)
                                continue
                            prints.append("> **"+c.capitalize()+":**")
                            for e, f in d.items():
                                if a == "commands":
                                    if a.istitle():
                                        prints.append("> "+e+" -- "+f)
                                    else:
                                        prints.append("> `"+e+"` -- "+f)
                                if a == "plans to update":
                                    prints.append("> \""+e+"\" -- "+f.capitalize())
                    else:
                        prints.append(b)
                b = []
                for a in prints:
                    if "{}" in a:
                        a = a.format(version)
                    b.append(a)
                prints = b
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                embed.add_field(name=version, value="\n".join(prints), inline=False)
        else:
            theud = dict([next(reversed(udslist.items()))])
            for a in theud.keys():
                version = a
            for a in theud.values():
                ud = a
            formver = defformver(version)
            prints = []
            for a, b in ud.items():
                if type(b) == list:
                    if formver == "Alpha.1":
                        if a == "note":
                            A1 = ""
                        else:
                            A1 = ":"
                    else:
                        if not b:
                            continue
                        A1 = ":"
                    prints.append("**"+a.capitalize()+A1+"**")
                    for c in b:
                        prints.append("> "+c)
                elif type(b) == dict:
                    prints.append("**"+a.capitalize()+":**")
                    for c, d in b.items():
                        if not d:
                            continue
                        if a == "other":
                            prints.append("> \""+c+"\" -- "+d)
                            continue
                        prints.append("> **"+c.capitalize()+":**")
                        for e, f in d.items():
                            if a == "commands":
                                if e.istitle():
                                    prints.append("> "+e+" -- "+f)
                                else:
                                    prints.append("> `"+e+"` -- "+f)
                            if a == "plans to update":
                                prints.append("> \""+e+"\" -- "+f.capitalize())
                else:
                    prints.append(b)
            b = []
            for a in prints:
                if "{}" in a:
                    a = a.format(version)
                b.append(a)
            prints = b
            a = "\n".join(prints)
            embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
            embed.add_field(name=version, value=a, inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Beta_0_4_0"][0])
    async def Beta_0_4_0(self, ctx):
        await ctx.send("History: Beta_4_0 commands:\n`command`")

    @Beta_0_4_0.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandB040(self, ctx):
        await ctx.send("History: Command commands:\n`info`\n`help`\n`profit`\nupdates")

    @commandB040.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_4_0"][1]["info"])
    async def info(self, ctx, *, req):
        icinfo = icd["info"]
        debug = []
        infoals = dict(list(als["ic"]["assets"].items())+list(als["ic"]["facilities"].items()))
        for a, b in infoals.items():
            if not b == None and req in b:
                debug.append(a)
        if len(debug) > 1:
            await ctx.send("`EN0401`: Happened an unexpected or imposible thing, E1: Aliases")
            return
        elif debug:
            reqsl, = debug
        else:
            reqsl = req
        reqsl = "_".join(reqsl.split(" "))
        check = list(icinfo["assets"].keys())+list(icinfo["facilities"])
        if not reqsl in check:
            await ctx.send(f"`EN0004`: Cannot find info of: {req}, check your input")
            return
        if reqsl in icinfo["assets"].keys():
            infoclass = "assets"
        elif reqsl in icinfo["facilities"].keys():
            infoclass = "facilities"
        theinfo = icinfo[infoclass][reqsl]
        embed = discord.Embed(title=f"Info -- {infoclass.capitalize()}", color=discord.Colour.greyple(), timestamp= datetime.datetime.now())
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="_ _", inline=False)
        output = []
        if infoclass == "assets":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            stuff = []
            if theinfo["market"] == True:
                stuff.append("It's tradable in market")
            elif theinfo["market"] == False:
                stuff.append("It's not tradable in market")
            if theinfo["retail"] == False:
                stuff.append("It cannot sold in retail store")
                stuff.append("It cannot be scrapped")
            else:
                stuff.append("It can sold in retail store")
                stuff.append("It can be scrapped into {} scraps".format(theinfo["retail"]))
            # output.append("\n".join(stuff))
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\n\n"+"\n".join(stuff), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if not als["ic"]["assets"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["assets"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if reqsl == "led":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Light-emitting_diode)")
            elif reqsl == "rubber":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/synthetic_rubber)")
            elif reqsl == "energy":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/electricity)")
            elif reqsl == "lamp":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/light_fixture)")
            elif reqsl == "ccd":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/charge-coupled_device)")
            elif reqsl == "hq":
                stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Headquarters)")
            elif theinfo["wikipedia"] != "None":
                stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "facilities":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"], inline=False)
            stuff = []
            for a, b in theinfo["construct"].items():
                if not a == "money":
                    stuff.append(f"{b}"+" **"+a.capitalize()+"**")
                else:
                    stuff.append("$"+f"{b:,}")
            # output.append("**Construction materials:**\n"+"\n".join(stuff))
            embed.add_field(name="Construction materials:", value="\n".join(stuff), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if not als["ic"]["facilities"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["facilities"][reqsl]))
            else: output.append("Aliases: None")
            if reqsl == "steel_mill":
                if random.randint(1, 50) == 1:
                    output.append("*I always typo this facility as \"still mill\"*")
            if reqsl == "furniture_factory":
                if random.randint(1, 5) == 1:
                    output.append("*Why the IdleCorp Wiki page has so many words...*")
                if random.randint(1, 10) == 1:
                    output.append("*Because the IdleCorp Wiki page has too many work, I had to change the layout of all...*")
            if reqsl.split("_")[-1] == "factory":
                if random.randint(1, 20) == 1:
                    output.append("*I really want to know who made this facility page...*")
            if reqsl == "research_chemical_factory":
                if random.randint(1, 3) == 1:
                    output.append("*Why this facility has so many aliases...*")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if reqsl == "":
                stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            else:
                stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        # embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="\n\n".join(output))
        await ctx.send(embed=embed)

    @commandB040.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_4_0"][1]["help"])
    async def help(self, ctx, *, cmd=None):
        if cmd == None:
            embed = discord.Embed(title="Help", description="Won't show Admin's, Owner's, Developer's commands", color=discord.Colour.green(), timestamp= datetime.datetime.now())
            for a, b in hps["commands"].items():
                embed.add_field(name=a.capitalize(), value=f"Descriptions/Features: {b[0]}\nSyntax: {b[1]}", inline=False)
        else:
            can = True
            cd = cmd
            cmds = cmd.split()
            if len(cmds) == 3:
                if cmds[-1] == "command":
                    cmds = [cmds[0]]+["command"]
            out, fir = [], False
            for a, b in hps["info"]["aliases"].items():
                for e, f in b.items():
                    for a in cmds:
                        if isinstance(f, dict):
                            if ("__init__" in f) and (a in f["__init__"]):
                                    fir = True
                                    out.append(e)
                            else:
                                g = f

                                for c, d in g.items():
                                    if a in d:
                                        out.append(c)
                                    elif isinstance(d, dict):
                                        if "__init__" in d and d["__init__"] == a:
                                            out.append(d["__init__"])
                                            continue
                                    g = d
                        elif a in f:
                            fir = True
                            out.append(e)
            cmds = out
            if fir == False or cmds[0] not in hps["commands"]:
                await ctx.send("`EN0004`: Cannot find command info named `{}`".format(cd))
                return
            embed = discord.Embed(title="Help -- "+cmds[0].capitalize(), color=discord.Colour.green(), timestamp= datetime.datetime.now())
            res = hps["commands"][cmds[0]]
            for a, b in hps["info"].items():
                if a == "aliases":
                    for c, d in b.items():
                        e = d
                        for cmd in cmds:
                            if cmd not in e: continue
                            e = e[cmd]
                        res.append(f["__init__"] if isinstance(f, dict) else f)
                        can = False
                        break
                elif a == "details":
                    for c, d in b.items():
                        e = d
                        for cmd in cmds:
                            if cmd not in e: continue
                            e = e[cmd]
                        if type(e) == dict and "__init__" not in e: continue
                        s = e["__init__"] if isinstance(e, dict) else e
                        if not s: break
                        # if re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s):
                        #     if re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s) == "-1":
                        #         s = s.format(cmds[-1])
                        #     elif re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s) == "-2":
                        #         s - s.format(cmds[-2])
                        if "{" and "}" in s: s - s.format(**zip([str(-g) for g in range(1, len(cmds)+1)[::-1]], cmds[:-1]))
                        res.append(s)
                        can = False
                        break
            if can == True:
                await ctx.send("`EN0004`: Cannot find command info named `{}`".format(cd))
                return
            out = [("Description: "+res[0])]+[("Syntax: "+res[1])]+[("Aliases: "+", ".join(res[2]))]
            if len(res) == 4:
                out.append("Details: "+res[3])
            embed.add_field(name=" ".join(cmds), value="\n\n".join(out), inline=False)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    def B040product_profit(facility, types, num=1):
        fac = icd["facilities"][facility]
        if not types in ("consumes", "produces", "all"):
            return
        if types == "all":
            tya = fac["consumes"]
            tyb = fac["produces"]
        else:
            ty = fac[types]
            if ty == "None":
                return None
        speed = fac["speed"]
        con_pfr = {}
        pro_pfr = {}
        if types == "consumes":
            for a, b in ty.items():
                money = icd["assets"][a]
                c = b*int(num)*money
                con_pf = repeating_dec_sol.repeating_dec_sol(c, speed)
                con_pfr[a] = con_pf
            return con_pfr
        elif types == "produces":
            for a, b in ty.items():
                money = icd["assets"][a]
                c = b*int(num)*money
                pro_pf = repeating_dec_sol.repeating_dec_sol(c, speed)
                pro_pfr[a] = pro_pf
            return pro_pfr
        elif types == "all":
            if not tya == "None":
                for a, b in tya.items():
                    if type(speed) == list:
                        speed = fac["speed"]
                        count = 0
                        for d in speed:
                            if a == "money":
                                money = 1
                            else:
                                money = icd["assets"][a]
                            c = b*int(num)*money
                            if c == int(c):
                                c = int(c)
                            else:
                                while c != int(c):
                                    c *= 10
                                    d *= 10
                                c = int(c)
                            con_pf = repeating_dec_sol.repeating_dec_sol(c, d)
                            con_pfr[a+(("_Min("+str(d)+")") if count == 1 else ("_Max("+str(d)+")"))] = con_pf
                            count = 1
                    else:
                        if a == "money":
                            money = 1
                        else:
                            money = icd["assets"][a]
                        c = b*int(num)*money
                        if c == int(c):
                            c = int(c)
                        else:
                            while c != int(c):
                                c *= 10
                                speed *= 10
                            c = int(c)
                        con_pf = repeating_dec_sol.repeating_dec_sol(c, speed)
                        con_pfr[a] = con_pf
            else:
                con_pfr = "None"
            if not tyb == "None":
                for a, b in tyb.items():
                    speed = fac["speed"]
                    if type(speed) == list:
                        count = 0
                        for d in speed:
                            if a == "money":
                                money = 1
                            else:
                                money = icd["assets"][a]
                            c = b*int(num)*money
                            if c == int(c):
                                c = int(c)
                            else:
                                while c != int(c):
                                    c *= 10
                                    d *= 10
                                c = int(c)
                            pro_pf = repeating_dec_sol.repeating_dec_sol(c, d)
                            pro_pfr[a+(("_Min("+str(d)+")") if count == 1 else ("_Max("+str(d)+")"))] = pro_pf
                            count = 1
                    else:
                        speed = fac["speed"]
                        if a == "money":
                            money = 1
                        else:
                            money = icd["assets"][a]
                        c = b*int(num)*money
                        if c == int(c):
                            c = int(c)
                        else:
                            while c != int(c):
                                c *= 10
                                speed *= 10
                            c = int(c)
                        pro_pf = repeating_dec_sol.repeating_dec_sol(c, speed)
                        pro_pfr[a] = pro_pf
            else:
                pro_pfr = "None"
            if con_pfr == "None":
                if len(list(pro_pfr.values())) == 1:
                    for a in list(pro_pfr.values()):
                        pfs = a 
            else:
                speed = fac["speed"]
                assets = icd["assets"]
                if type(speed) == list:
                    i = 0
                    pfss = []
                    for r in speed:
                        for a, b in tyb.items():
                            if a == "money":
                                pdm = 1
                            else:
                                pdm = assets[a]
                            pdttm = b*pdm*int(num)
                        csttm = []
                        for a, b in tya.items():
                            csm = assets[a]
                            csttm.append(csm*b*int(num))
                        cstm = 0
                        for a in csttm:
                            cstm += a
                        pfbf = pdttm-cstm
                        if pfbf == int(pfbf):
                            pfbf = int(pfbf)
                        else:
                            while pfbf != int(pfbf):
                                pfbf *= 10
                                r *= 10
                            pfbf = int(pfbf)
                        pfs = repeating_dec_sol.repeating_dec_sol(pfbf, r)
                        if i == 1:
                            pfss.append({"Min": pfs})
                        else:
                            pfss.append({"Max": pfs})
                        i += 1
                    return [con_pfr, pro_pfr, pfss]
                for a, b in tyb.items():
                    if a == "money":
                        pdm = 1
                    else:
                        pdm = assets[a]
                    pdttm = b*pdm*int(num)
                csttm = []
                for a, b in tya.items():
                    csm = assets[a]
                    csttm.append(csm*b*int(num))
                cstm = 0
                for a in csttm:
                    cstm += a
                pfbf = pdttm-cstm
                if pfbf == int(pfbf):
                    pfbf = int(pfbf)
                else:
                    while pfbf != int(pfbf):
                        pfbf *= 10
                        speed *= 10
                    pfbf = int(pfbf)
                pfs = repeating_dec_sol.repeating_dec_sol(pfbf, speed)
            return [con_pfr, pro_pfr, pfs]

    @commandB040.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_4_0"][1]["profit"])
    async def profit(self, ctx, *, args):#facility, number
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
        fac = args[0]
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
        sol = history.B040product_profit(fac, "all", num)
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
                s.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
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
                s2.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
            p = "\n".join(s2)
        else:
            p = "None"
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
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Profit", value=pf, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB040.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_4_0"][1]["search"])
    async def search(self, ctx, ctn=None):
        if ctn == None:
            await ctx.send("What you want to search?Just need to enter something.")
        else:
            if ctn.split()[0] in ("--April", "--0401", "--april", "--aprilfool"):
                datetime.date = datetime.date(2021, 4, 1)
            else:
                datetime.date = datetime.datetime.now().date()
            embed = discord.Embed(title="Search", color=discord.Color.from_rgb(int("35", 16), int("12", 16), int("38", 16)), timestamp= datetime.datetime.now())
            imgname = ""
            if not str(datetime.date) == "2021-04-01":
                embed.add_field(name="Haven't this command", value="This command is not usable")
                await ctx.send(embed=embed)
                return
            if ctn == "when":
                embed.add_field(name="Result", value="ERROR: Time collection! Pleace make sure you have time to do this and try again")
                img = Image.new("1", (100, 100), 255)
                font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
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
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
            elif ctn == "end":
                embed.add_field(name="Result", value="When UTC...")
                img = Image.new("1", (100, 100), 255)
                font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
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
                imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                imgname = f"Search{imgnum}.jpg"
                img.save(imgname)
                embed.set_thumbnail(url="attachment://"+imgname)
            await ctx.send(file=discord.File(imgname), embed=embed)
            if imgname:
                os.remove(imgname)

    @commandB040.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_4_0"][1]["updates"])
    async def updates(self, ctx, *, args=None):
        def defformver(ver):
            if ver == "Alpha.0.2":
                formver = "Alpha.1"
            elif ver in ("Alpha.0.2.1", "Alpha.0.3.0", "Beta.0.1.0"):
                formver = "Alpha.2"
            else:
                formver = "Alpha.2"
            return formver
        if args != None:
            arg = string_handler.filter(args)
            if arg[1]:
                await ctx.send("`EN0008`: Argument error: type number")
                return
            flags = string_handler.flags(arg[0])
            if flags[1]:
                await ctx.send("`EN0001`: Flag type error, `--`")
                return
            if len(flags[0]) > 1:
                await ctx.send("`EN0002`: Too many flags")
                return
            elif len(flags[0]) == 1:
                for a in flags[0]:
                    flag = a
            else:
                flag = None
            if flag != None:
                if arg[0].index(flag) > 0:
                    await ctx.send("`EN0007`: Argument flag error")
                    return
            if flag != None:
                flag = flag[2:]
            if len(flags[2]) > 1:
                await ctx.send("`EN0008`: String")
                return
            elif len(flags[2]) == 1:
                for a in flags[2]:
                    mores = a
            else:
                mores = None
            if flag == None:
                theud = dict([next(reversed(udslist.items()))])
                for a in theud.keys():
                    version = a
                for a in theud.values():
                    ud = a
            else:
                ud = udslist[flag]
                version = flag
            if mores != None:
                more = mores.split(".")
                stuff = []
                for a in more:
                    stuff.append(a.replace("_", " "))
                # if len(more) == 1:
                #     for a in more:
                #         for c, d in als["updates list"]["first"].items():
                #             if a in c:
                #                 a = c
                #         prints =  ud[a]
                # else:
                fn = ""
                b = ud
                first = als["updates list"]["first"]
                second = als["updates list"]["second"]
                third = als["updates list"]["third"]
                i = 0
                moo = []
                for a in more:
                    if i == 0:
                        for c, d in first.items():
                            if a in d:
                                a = c
                                f = c
                    else:
                        if f != "plans to update":
                            for c, d in second.items():
                                if a in d:
                                    a = c
                        else:
                            for c, d in third.items():
                                if a in d:
                                    a = c
                    if a not in b:
                        await ctx.send("`EN0004`: The argument is invalid or unexist in this version of update")
                    b = b[a]
                    moo.append(a)
                    i += 1
                more = moo
                store = b
                nothing = "\n**Nothing to show**"
                if not store:
                    prints = nothing
                else:
                    if type(store) == list:
                        prints = "\n".join(store)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == dict:
                        noth = 0
                        store2 = []
                        for a, b in store.items():
                            if more[0] == "commands":
                                if a in ("adds", "changes", "deletes"):
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            if a.istitle():
                                                store2.append(a+" -- "+b)
                                            else:
                                                store2.append("`"+a+"` -- "+b)
                                        # prints = "\n".join(store)
                                else:
                                    if a.istitle():
                                        store2.append(+a+" -- "+b)
                                    else:store2.append("`"+a+"` -- "+b)
                            elif more[0] == "other":
                                if b:
                                    store2.append("\""+a+"\" -- "+b)
                            elif more[0] == "plans to update":
                                if a in ud["plans to update"].keys():
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            store2.append("\""+a.capitalize()+"\" -- "+b.capitalize())
                                        # prints = "\n".join(store)
                                else:
                                    store2.append("\""+a.capitalize()+"\" -- "+b.capitalize())
                        if store2:
                            prints = "\n".join(store2)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == str:
                        if len(store.split(" ")) == 1:
                            prints = store.capitalize()
                        else:
                            prints = store
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                prints += f"\n\nVersion: **v.{version}**"
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                embed.add_field(name=version+fn, value=prints, inline=False)
            else:
                formver = defformver(version)
                prints = []
                for a, b in ud.items():
                    if type(b) == list:
                        if not b:
                            continue
                        if formver == "Alpha.1":
                            if a == "note":
                                A1 = ""
                            else:
                                A1 = ":"
                        else:
                            A1 = ":"
                        prints.append("**"+a.capitalize()+A1+"**")
                        for c in b:
                            prints.append("> "+c)
                    elif type(b) == dict:
                        prints.append("**"+a.capitalize()+":**")
                        for c, d in b.items():
                            if not d:
                                continue
                            if a == "other":
                                prints.append("> \""+c+"\" -- "+d)
                                continue
                            prints.append("> **"+c.capitalize()+":**")
                            for e, f in d.items():
                                if a == "commands":
                                    if a.istitle():
                                        prints.append("> "+e+" -- "+f)
                                    else:
                                        prints.append("> `"+e+"` -- "+f)
                                if a == "plans to update":
                                    prints.append("> \""+e+"\" -- "+f.capitalize())
                    else:
                        prints.append(b)
                b = []
                for a in prints:
                    if "{}" in a:
                        a = a.format(version)
                    b.append(a)
                prints = b
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                if len("\n".join(prints)) > 1000:
                    a, b = "\n".join(prints[:len(prints)//2]), "\n".join(prints[len(prints)//2:])
                    embed.add_field(name=version, value=a, inline=False)
                    embed.add_field(name="_ _", value=b, inline=False)
                else:
                    embed.add_field(name=version, value="\n".join(prints), inline=False)
        else:
            theud = dict([next(reversed(udslist.items()))])
            for a in theud.keys():
                version = a
            for a in theud.values():
                ud = a
            formver = defformver(version)
            prints = []
            for a, b in ud.items():
                if type(b) == list:
                    if formver == "Alpha.1":
                        if a == "note":
                            A1 = ""
                        else:
                            A1 = ":"
                    else:
                        if not b:
                            continue
                        A1 = ":"
                    prints.append("**"+a.capitalize()+A1+"**")
                    for c in b:
                        prints.append("> "+c)
                elif type(b) == dict:
                    prints.append("**"+a.capitalize()+":**")
                    for c, d in b.items():
                        if not d:
                            continue
                        if a == "other":
                            prints.append("> \""+c+"\" -- "+d)
                            continue
                        prints.append("> **"+c.capitalize()+":**")
                        for e, f in d.items():
                            if a == "commands":
                                if e.istitle():
                                    prints.append("> "+e+" -- "+f)
                                else:
                                    prints.append("> `"+e+"` -- "+f)
                            if a == "plans to update":
                                prints.append("> \""+e+"\" -- "+f.capitalize())
                else:
                    prints.append(b)
            b = []
            for a in prints:
                if "{}" in a:
                    a = a.format(version)
                b.append(a)
            prints = b
            embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
            if len("\n".join(prints)) > 1000:
                a, b = "\n".join(prints[:len(prints)//2]), "\n".join(prints[len(prints)//2:])
                embed.add_field(name=version, value=a, inline=False)
                embed.add_field(name="_ _", value=b, inline=False)
            else:
                a = "\n".join(prints)
                embed.add_field(name=version, value=a, inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Beta_0_5_0"][0])
    async def Beta_0_5_0(self, ctx):
        await ctx.send("History: Beta_5_0 commands:\n`command`")

    @Beta_0_5_0.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandB050(self, ctx):
        await ctx.send("History: Command commands:\n`profit`\n`info`\n`speed`")

    @commandB050.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_5_0"][1]["profit"])
    async def profit(self, ctx, *, args):#facility, number
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
        fac = args[0]
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
        sol = calculate.product_profit(fac, "all", num)
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
                s.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
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
                s2.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
            p = "\n".join(s2)
        else:
            p = "None"
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
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Profit", value=pf, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**!\nThe **profit** is meaning that if your sourse of the facility is from buying from npc market, then the profit, if you are not buying the sourse from npc market, then the **produces** part.", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB050.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_5_0"][1]["info"])
    async def info(self, ctx, *, req):
        icinfo = icd["info"]
        debug = []
        infoals = {}
        for a in als["ic"].values():
            infoals = infoals | a
        for a, b in infoals.items():
            if not b == None and req in b:
                debug.append(a)
        if len(debug) > 1:
            await ctx.send("`EN0401`: Happened an unexpected or imposible thing, E1: Aliases")
            return
        elif debug:
            reqsl, = debug
        else:
            reqsl = req
        reqsl = "_".join(reqsl.split(" "))
        if reqsl.endswith("_u"): reqsl, techlv = reqsl[:-2], 1
        elif reqsl.endswith("_uu"): reqsl, techlv = reqsl[:-3], 2
        else: techlv = 0
        check = [b for a in icinfo.values() for b in a.keys()]
        if not reqsl in check:
            await ctx.send(f"`EN0004`: Cannot find info of: {req}, check your input")
            return
        for a in icinfo:
            if reqsl in icinfo[a]:
                infoclass = a
        theinfo = icinfo[infoclass][reqsl]
        embed = discord.Embed(title=f"Info -- {infoclass.capitalize()}", color=discord.Colour.greyple(), timestamp= datetime.datetime.now())
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="_ _", inline=False)
        output = []
        if infoclass == "assets":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            stuff = []
            if theinfo["market"] == True:
                stuff.append("It's tradable in market")
            elif theinfo["market"] == False:
                stuff.append("It's not tradable in market")
            if theinfo["retail"] == False:
                stuff.append("It cannot sold in retail store")
                stuff.append("It cannot be scrapped")
            else:
                stuff.append("It can sold in retail store")
                stuff.append("It can be scrapped into {} scraps".format(theinfo["retail"]))
            # output.append("\n".join(stuff))
            stuff2 = ["NPC market buy price(if valid): "+str(icd["assets"][reqsl]*2)]
            stuff2.append("NPC market sell price: "+str(icd["assets"][reqsl]))
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\n\n"+"\n".join(stuff)+"\n\n"+"\n".join(stuff2), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["assets"]:
                await ctx.send("`EN0402`: Cannot find assets -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["assets"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["assets"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if reqsl == "led": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Light-emitting_diode)")
            elif reqsl == "rubber": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/synthetic_rubber)")
            elif reqsl == "energy": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/electricity)")
            elif reqsl == "lamp": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/light_fixture)")
            elif reqsl == "ccd": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/charge-coupled_device)")
            elif reqsl == "hq": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Headquarters)")
            elif theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "facilities":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"], inline=False)
            stuff = []
            for a, b in theinfo["construct"].items():
                if not a == "money":
                    stuff.append(f"{b:,}"+" **"+a.capitalize()+"**")
                else:
                    stuff.append("$"+f"{b:,}")
            # output.append("**Construction materials:**\n"+"\n".join(stuff))
            embed.add_field(name="Construction materials:", value="\n".join(stuff), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            stuff = "**Consumes**\n"
            facpro = icd["facilities"][reqsl]
            stuff += "None\n" if facpro["consumes"] == "None" else "\n".join([f"**{a.capitalize()}** | {b:,}" for a, b in facpro["consumes"].items()])+"\n"
            stuff += "**Produces**\n"
            stuff += "None\n" if facpro["produces"] == "None" else "\n".join([f"**{a.capitalize()}** | {b:,}" for a, b in facpro["produces"].items()])+"\n"
            stuff += "Speed: "+str(icd["facilities"][reqsl]["speed"])+" seconds"
            embed.add_field(name="Production:", value=stuff, inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["facilities"]:
                await ctx.send("`EN0402`: Cannot find facilities -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["facilities"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["facilities"][reqsl]))
            else: output.append("Aliases: None")
            if reqsl == "steel_mill":
                if random.randint(1, 50) == 1:
                    output.append("*I always typo this facility as \"still mill\"*")
            if reqsl == "furniture_factory":
                if random.randint(1, 5) == 1:
                    output.append("*Why the IdleCorp Wiki page has so many words...*")
                if random.randint(1, 10) == 1:
                    output.append("*Because the IdleCorp Wiki page has too many work, I had to change the layout of all...*")
            if reqsl.split("_")[-1] == "factory":
                if random.randint(1, 20) == 1:
                    output.append("*I really want to know who made this facility page...*")
            if reqsl == "research_chemical_factory":
                if random.randint(1, 3) == 1:
                    output.append("*Why this facility has so many aliases...*")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "blueprints":
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\n\nRarity: {}".format(theinfo["rarity"])+"\n\nAll blueprints **cannot** trade and be sold in the market and the retail stores.", inline=False)
            stuff = []
            for a, b in theinfo["require"].items():
                stuff.append(f"{b:,}"+" **"+a.capitalize()+"**")
            embed.add_field(name="Requires:", value="\n".join(stuff), inline=False)
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["blueprints"]:
                await ctx.send("`EN0402`: Cannot find blueprints -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["blueprints"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["blueprints"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "technologies":
            stuff = []
            if techlv == 2:
                if theinfo["upgrade"]["uu"] == "None":
                    await ctx.send("`EN0004`: The tech haven't \"uu\" upgrade")
                    return
                stuff.append(theinfo["upgrade"]["uu"]["icinfo"])
                stuff.append("Rarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["upgrade"]["uu"]["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
            elif techlv == 1:
                if theinfo["upgrade"]["u"] == "None":
                    await ctx.send("`EN0004`: The tech haven't \"u\" upgrade")
                    return
                stuff.append(theinfo["upgrade"]["u"]["icinfo"])
                stuff.append("Rarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["upgrade"]["u"]["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
                if theinfo["upgrade"]["uu"] != "None": stuff.append("\nNext upgrade: "+reqsl.replace("_", " ")+"uu")
            else:
                stuff.append(theinfo["icinfo"])
                stuff.append("\nRarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
                if theinfo["upgrade"]["u"] != "None": stuff.append("\nNext upgrade: "+reqsl.replace("_", " ")+"u")
            stuff.append("The tech affected on "+theinfo["affect"].capitalize())
            embed.add_field(name="IdleCorp Info(Examine):", value="\n".join(stuff), inline=False)
            stuff = "\n".join(["Level {} boost: {}".format(a, theinfo["boost"][a].replace("+", "and")) for a in range(len(theinfo["boost"]))])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["technologies"]:
                await ctx.send("`EN0402`: Cannot find blueprints -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["technologies"][reqsl+("_u" if techlv == 1 else ("_uu" if techlv == 2 else ""))] == None:
                output.append("Aliases: "+", ".join(als["ic"]["technologies"][reqsl+("_u" if techlv == 1 else ("_uu" if techlv == 2 else ""))]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "services":
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\nAffect: "+theinfo["effect"]+"\nCost: **${:,}**".format(theinfo["cost"]), inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["services"]:
                await ctx.send("`EN0402`: Cannot find services -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["services"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["services"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            if stuff: output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "pollicies":
            embed.add_field(name="IdleCorp Info(Examine):", value="Affect: "+theinfo["affect"]+"\nCost: {} *Funding points*".format(theinfo["cost"]), inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["services"]:
                await ctx.send("`EN0402`: Cannot find services -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["policies"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["policies"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            if stuff: output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        # embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="\n\n".join(output))
        await ctx.send(embed=embed)

    @commandB050.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_5_0"][1]["speed"])
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
        fac = args[0]
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
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["server"][0])
    async def server(self, ctx):
        await ctx.send("Server history:\n`joins`")

    @server.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["server"][1]["joins"])
    async def joins(self, ctx):
        await ctx.send("```2021-01-23 -- IdleCorp joined as the begin of the server setup\n2021-03-07 -- Teemaw joined```")

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["idlecorpprofit"][0])
    async def idlecorpprofit(self, ctx):
        await ctx.send("IdleCorp Profit history:\n`begin`")

    @idlecorpprofit.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["idlecorpprofit"][1]["begin"])
    async def begin(self, ctx):
        await ctx.send("welcome to suggest on what can add and will be added in the near future.")

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_0"][0])
    async def Beta_0_6_0(self, ctx):
        await ctx.send("History: Beta_0_6_0 commands:\n`command`")

    @Beta_0_6_0.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandB060(self, ctx):
        await ctx.send("History: Command commands:\n`profit`\n`info`\n`speed`")

    @commandB060.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_0"][1]["updates"])
    async def updates(self, ctx, *, args=None):
        def defformver(ver):
            if ver == "Alpha.0.2":
                formver = "Alpha.1"
            elif ver in ("Alpha.0.2.1", "Alpha.0.3.0", "Beta.0.1.0"):
                formver = "Alpha.2"
            else:
                formver = "Alpha.2"
            return formver
        if args != None:
            arg = string_handler.filter(args)
            if arg[1]:
                await ctx.send("`EN0008`: Argument error: type number")
                return
            flags = string_handler.flags(arg[0])
            if flags[1]:
                await ctx.send("`EN0001`: Flag type error, `--`")
                return
            if len(flags[0]) > 1:
                await ctx.send("`EN0002`: Too many flags")
                return
            elif len(flags[0]) == 1:
                for a in flags[0]:
                    flag = a
            else:
                flag = None
            if flag != None:
                if arg[0].index(flag) > 0:
                    await ctx.send("`EN0007`: Argument flag error")
                    return
            if flag != None:
                flag = flag[2:]
            if len(flags[2]) > 1:
                await ctx.send("`EN0008`: String")
                return
            elif len(flags[2]) == 1:
                for a in flags[2]:
                    mores = a
            else:
                mores = None
            if flag == None:
                theud = dict([next(reversed(udslist.items()))])
                for a in theud.keys():
                    version = a
                for a in theud.values():
                    ud = a
            else:
                ud = udslist[flag]
                version = flag
            if mores != None:
                more = mores.split(".")
                stuff = []
                for a in more:
                    stuff.append(a.replace("_", " "))
                # if len(more) == 1:
                #     for a in more:
                #         for c, d in als["updates list"]["first"].items():
                #             if a in c:
                #                 a = c
                #         prints =  ud[a]
                # else:
                fn = ""
                b = ud
                first = als["updates list"]["first"]
                second = als["updates list"]["second"]
                third = als["updates list"]["third"]
                i = 0
                moo = []
                for a in more:
                    if i == 0:
                        for c, d in first.items():
                            if a in d:
                                a = c
                                f = c
                    else:
                        if f != "plans to update":
                            for c, d in second.items():
                                if a in d:
                                    a = c
                        else:
                            for c, d in third.items():
                                if a in d:
                                    a = c
                    if a not in b:
                        await ctx.send("`EN0004`: The argument is invalid or unexist in this version of update")
                    b = b[a]
                    moo.append(a)
                    i += 1
                more = moo
                store = b
                nothing = "\n**Nothing to show**"
                if not store:
                    prints = nothing
                else:
                    if type(store) == list:
                        prints = "\n".join(store)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == dict:
                        noth = 0
                        store2 = []
                        for a, b in store.items():
                            if more[0] == "commands":
                                if a in ("adds", "changes", "deletes"):
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            if a.istitle():
                                                store2.append(a+" -- "+b)
                                            else:
                                                store2.append("`"+a+"` -- "+b)
                                        # prints = "\n".join(store)
                                else:
                                    if a.istitle():
                                        store2.append(+a+" -- "+b)
                                    else:store2.append("`"+a+"` -- "+b)
                            elif more[0] == "other":
                                if b:
                                    store2.append("\""+a+"\" -- "+b)
                            elif more[0] == "plans to update":
                                if a in ud["plans to update"].keys():
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            store2.append("\""+a.capitalize()+"\" -- "+b.capitalize())
                                        # prints = "\n".join(store)
                                else:
                                    store2.append("\""+a.capitalize()+"\" -- "+b.capitalize())
                        if store2:
                            prints = "\n".join(store2)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == str:
                        if len(store.split(" ")) == 1:
                            prints = store.capitalize()
                        else:
                            prints = store
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                prints += f"\n\nVersion: **v.{version}**"
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                embed.add_field(name=version+fn, value=prints, inline=False)
            else:
                formver = defformver(version)
                prints = []
                for a, b in ud.items():
                    if type(b) == list:
                        if not b:
                            continue
                        if formver == "Alpha.1":
                            if a == "note":
                                A1 = ""
                            else:
                                A1 = ":"
                        else:
                            A1 = ":"
                        prints.append("**"+a.capitalize()+A1+"**")
                        for c in b:
                            prints.append("> "+c)
                    elif type(b) == dict:
                        prints.append("**"+a.capitalize()+":**")
                        for c, d in b.items():
                            if not d:
                                continue
                            if a == "other":
                                prints.append("> \""+c+"\" -- "+d)
                                continue
                            prints.append("> **"+c.capitalize()+":**")
                            for e, f in d.items():
                                if a == "commands":
                                    if a.istitle():
                                        prints.append("> "+e+" -- "+f)
                                    else:
                                        prints.append("> `"+e+"` -- "+f)
                                if a == "plans to update":
                                    prints.append("> \""+e+"\" -- "+f.capitalize())
                    else:
                        prints.append(b)
                b = []
                for a in prints:
                    if "{}" in a:
                        a = a.format(version)
                    b.append(a)
                prints = b
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                if len("\n".join(prints)) > 1000:
                    a, b = prints[:len(prints)//2], prints[len(prints)//2:]
                    tlist = (deque(a), deque(b))
                    for i in range(2):
                        while len("\n".join(tlist[i])) > 1000:
                            if i == 0: tlist[1].appendleft(tlist[0].pop())
                            else: tlist[0].append(tlist[1].popleft())
                    a, b = tlist
                    embed.add_field(name=version, value="\n".join(a), inline=False)
                    embed.add_field(name="_ _", value="\n".join(b), inline=False)
                else:
                    embed.add_field(name=version, value="\n".join(prints), inline=False)
        else:
            theud = dict([next(reversed(udslist.items()))])
            for a in theud.keys():
                version = a
            for a in theud.values():
                ud = a
            formver = defformver(version)
            prints = []
            for a, b in ud.items():
                if type(b) == list:
                    if formver == "Alpha.1":
                        if a == "note":
                            A1 = ""
                        else:
                            A1 = ":"
                    else:
                        if not b:
                            continue
                        A1 = ":"
                    prints.append("**"+a.capitalize()+A1+"**")
                    for c in b:
                        prints.append("> "+c)
                elif type(b) == dict:
                    prints.append("**"+a.capitalize()+":**")
                    for c, d in b.items():
                        if not d:
                            continue
                        if a == "other":
                            prints.append("> \""+c+"\" -- "+d)
                            continue
                        prints.append("> **"+c.capitalize()+":**")
                        for e, f in d.items():
                            if a == "commands":
                                if e.istitle():
                                    prints.append("> "+e+" -- "+f)
                                else:
                                    prints.append("> `"+e+"` -- "+f)
                            if a == "plans to update":
                                prints.append("> \""+e+"\" -- "+f.capitalize())
                else:
                    prints.append(b)
            b = []
            for a in prints:
                if "{}" in a:
                    a = a.format(version)
                b.append(a)
            prints = b
            embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
            if len("\n".join(prints)) > 1000:
                a, b = prints[:len(prints)//2], prints[len(prints)//2:]
                tlist = (deque(a), deque(b))
                for i in range(2):
                    while len("\n".join(tlist[i])) > 1000:
                        if i == 0: tlist[1].appendleft(tlist[0].pop())
                        else: tlist[0].append(tlist[1].popleft())
                a, b = tlist
                embed.add_field(name=version, value="\n".join(a), inline=False)
                embed.add_field(name="_ _", value="\n".join(b), inline=False)
            else:
                a = "\n".join(prints)
                embed.add_field(name=version, value=a, inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB060.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_0"][1]["speed"])
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
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(1.2)
        await msg.edit(embed=embed)

    @commandB060.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_0"][1]["profit"])
    async def profit(self, ctx, *, args):#facility, number
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
        if "flag" in locals(): num *= {"day": 60*60*24, "hour": 60*60, "minute": 60}.get(flag, 1)
        sol = calculate.product_profit(fac, "all", num)
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
                s.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
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
                s2.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
            p = "\n".join(s2)
        else:
            p = "None"
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
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), description="Unit: "+unit.capitalize(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Profit", value=pf, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s).\nThe **profit** is meaning that if your sourse of the facility is from buying from npc market, then the profit, if you are not buying the sourse from npc market, then the **produces** part.", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(1.2)
        await msg.edit(embed=embed)

    @commandB060.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_0"][1]["profitcomplete"])
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
        print(sol, soland)
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
            print(s2)
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
                pfland = "**Max** | $"+a+"\n"
            for a in list(pfs[1].values()):
                try:
                    float(a)
                    a = f"{float(a):,}"
                except:
                    a = a.split(".")
                    a = f"{int(a[0]):,}.{a[1]}"
                pfland += "**Min** | $"+a
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
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s).\nThe **profit** is meaning that if your sourse of the facility is from buying from npc market, then the profit, if you are not buying the sourse from npc market, then the **produces** part.", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(1.2)
        await msg.edit(embed=embed)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_1"][0])
    async def Beta_0_6_1(self, ctx):
        await ctx.send("History: Beta_0_6_1 commands:\n`command`")

    @Beta_0_6_1.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandB061(self, ctx):
        await ctx.send("History: Command commands:\n`search`\n`profitcomplete`")

    @commandB061.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_1"][1]["search"])
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
                    imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                    imgname = f"Search{imgnum}.jpg"
                    img.save(imgname)
                    embed.set_thumbnail(url="attachment://"+imgname)
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
                    imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                    imgname = f"Search{imgnum}.jpg"
                    img.save(imgname)
                    embed.set_thumbnail(url="attachment://"+imgname)
                elif ctn == "end":
                    embed.add_field(name="Result", value="When UTC...")
                    img = Image.new("1", (100, 100), 255)
                    font = ImageFont.FreeTypeFont('Arial.ttf', size=20)
                    ImageDraw.Draw(img).text((50, 50), "Search", anchor="mm", fill="black", font=font, align="center")
                    imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                    imgname = f"Search{imgnum}.jpg"
                    img.save(imgname)
                    embed.set_thumbnail(url="attachment://"+imgname)
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
                    imgnum = len([file for file in os.listdir() if file.endswith(".jpg")])
                    imgname = f"Search{imgnum}.jpg"
                    img.save(imgname)
                    embed.set_thumbnail(url="attachment://"+imgname)
                await ctx.send(file=discord.File(imgname), embed=embed)
                if imgname:
                    os.remove(imgname)
            else:
                embed.add_field(name="Result", value=ctn, inline=False)
                await ctx.send(embed=embed)

    def B061produce_remain(fac, facdt, num=1, land=1):
        faclist = icd["facilities"]
        faccs = faclist[fac]["consumes"]
        facspeed = faclist[fac]["speed"]
        assets = icd["assets"]
        res1 = []
        res2 = []
        ld = []
        for a, b in facdt:
            pd, = faclist[a]["produces"].keys()
            f, = faclist[a]["produces"].values()
            f = fractions.Fraction(f*b, faclist[a]["speed"])
            sp = f-fractions.Fraction(faccs[pd]*num, facspeed)
            b = repeating_dec_sol.repeating_dec_sol(sp.numerator, sp.denominator)
            res1.append((pd, (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b))
            b = sp*fractions.Fraction(str(assets[pd]))
            ld.append(b)
            b = repeating_dec_sol.repeating_dec_sol(b.numerator, b.denominator)
            res2.append((pd, (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b))
        pfld = sum(ld)/land
        res3 = repeating_dec_sol.repeating_dec_sol(pfld.numerator, pfld.denominator)
        res3 = (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b
        return [res1, res2, res3]

    def B061facratio(fac, num=1):
        faclist = icd["facilities"]
        faccs = faclist[fac]["consumes"]
        facspeed = faclist[fac]["speed"]
        if faccs == "None":
            return [f"0:{num}", f"(0:{num}, 0:{num})", [("N/A", 0)]]
        facpd = []
        for a in faccs:
            for b in faclist:
                for c in faclist[b]["produces"].keys():
                    if c == a:
                        facpd.append((b, c))
        stuff = [b for a, b in facpd]
        rep = []
        for a in range(len(stuff)):
            for b in stuff:
                if stuff.count(b) > 1:
                    rep.append(b)
        energy = 0
        if "energy" in rep:
            energy = 1
        if energy: facpd = [("solar_power_plant" if a == "coal_power_plant" else a, b) for a, b in facpd]
        stuff1 = []
        depfrac1 = []
        depfrac2 = []
        firstfacdt = []
        for f, g in facpd:
            # a = fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
            b = fractions.Fraction(faccs[g], faclist[fac]["speed"])*num
            count = 0
            while b > 0:
                b-=fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
                count += 1
            firstfacdt.append((f, count))
            stuff1.append(str(count))
            frac1 = fractions.Fraction(faccs[g], facspeed)/fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
            afrac = [fractions.Fraction(faccs[g], faclist[fac]["speed"]), fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])]
            if afrac.index(min(afrac)):
                afrac = (max(afrac)/min(afrac), 1)
            else:
                afrac = (1, max(afrac)/min(afrac))
            depfrac1.append(":".join((str(int(float(f))) if float(f).is_integer() else f) if re.fullmatch(r"[0-9]+[.][0-9]+", f) else f for f in [repeating_dec_sol.repeating_dec_sol(a.numerator, a.denominator) for a in calculate.simratio(afrac)]))
            bfrac = []
            for a in afrac:
                if type(a) == fractions.Fraction:
                    b = repeating_dec_sol.repeating_dec_sol(a.numerator, a.denominator)
                    bfrac.append((str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b)
                else: bfrac.append(str(a))
            depfrac2.append(":".join(bfrac))
        # a = True
        # b = [decimal.Decimal(str(1.2337)), decimal.Decimal(str(1.22)), decimal.Decimal(str(7.177))]
        # re = b
        # while a:
        #     bfr = []
        #     stuff = []
        #     for c in re:
        #         c*=10
        #         bfr.append(c)
        #         stuff.append(True if int(c)!=float(c) else False)
        #     if True in stuff: a = True
        #     if list(set(stuff)) == [False]: a = False
        #     re = bfr
        # for a, b in facpd:
        #     a, = faclist[f]["produces"].values()
        #     b = fractions.Fraction(faccs[g], facspeed)
        # intrat = calculate.simratio([fractions.Fraction(faclist[a]["produces"][b], faclist[a]["speed"]) for a, b in facpd]+[fractions.Fraction(faccs[], 1)])
        # print(intrat) # ":".join([repeating_dec_sol.repeating_dec_sol(a.numerator, a.denominator) for a in intrat])+":1", 
        return (":".join(stuff1)+":1", ", ".join([f"({a}, {b})" for a, b in zip(depfrac1, depfrac2)]), firstfacdt)

    @commandB061.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_1"][1]["profitcomplete"])
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
        facratio = history.B061facratio(fac, num)
        firstfac = calculate.firstfac(fac, facratio[2])
        remain = history.B061produce_remain(fac, facratio[2], num, firstfac[2])
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
                pfland = "**Max** | $"+a+"\n"
            for a in list(pfs[1].values()):
                try:
                    float(a)
                    a = f"{float(a):,}"
                except:
                    a = a.split(".")
                    a = f"{int(a[0]):,}.{a[1]}"
                pfland += "**Min** | $"+a
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
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s).\nThe **profit** is meaning that if your sourse of the facility is from buying from npc market, then the profit, if you are not buying the sourse from npc market, then the **produces** part.", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(3)
        await msg.edit(embed=embed)

    @commandB061.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_1"][1]["updates"])
    async def updates(self, ctx, *, args=None):
        def defformver(ver):
            if ver == "Alpha.0.2":
                formver = "Alpha.1"
            elif ver in ("Alpha.0.2.1", "Alpha.0.3.0", "Beta.0.1.0"):
                formver = "Alpha.2"
            else:
                formver = "Alpha.2"
            return formver
        if args != None:
            arg = string_handler.filter(args)
            if arg[1]:
                await ctx.send("`EN0008`: Argument error: type number")
                return
            flags = string_handler.flags(arg[0])
            if flags[1]:
                await ctx.send("`EN0001`: Flag type error, `--`")
                return
            if len(flags[0]) > 1:
                await ctx.send("`EN0002`: Too many flags")
                return
            elif len(flags[0]) == 1:
                for a in flags[0]:
                    flag = a
            else:
                flag = None
            if flag != None:
                if arg[0].index(flag) > 0:
                    await ctx.send("`EN0007`: Argument flag error")
                    return
            if flag != None:
                flag = flag[2:]
            if len(flags[2]) > 1:
                await ctx.send("`EN0008`: String")
                return
            elif len(flags[2]) == 1:
                for a in flags[2]:
                    mores = a
            else:
                mores = None
            if flag == None:
                theud = dict([next(reversed(udslist.items()))])
                for a in theud.keys():
                    version = a
                for a in theud.values():
                    ud = a
            else:
                ud = udslist[flag]
                version = flag
            if mores != None:
                more = mores.split(".")
                stuff = []
                for a in more:
                    stuff.append(a.replace("_", " "))
                # if len(more) == 1:
                #     for a in more:
                #         for c, d in als["updates list"]["first"].items():
                #             if a in c:
                #                 a = c
                #         prints =  ud[a]
                # else:
                fn = ""
                b = ud
                first = als["updates list"]["first"]
                second = als["updates list"]["second"]
                third = als["updates list"]["third"]
                i = 0
                moo = []
                for a in more:
                    if i == 0:
                        for c, d in first.items():
                            if a in d:
                                a = c
                    else:
                        if a != "plans to update":
                            for c, d in second.items():
                                if a in d:
                                    a = c
                        else:
                            for c, d in third.items():
                                if a in d:
                                    a = c
                    if a not in b:
                        await ctx.send("`EN0004`: The argument is invalid or unexist in this version of update")
                    b = b[a]
                    moo.append(a)
                    i += 1
                more = moo
                store = b
                nothing = "\n**Nothing to show**"
                if not store:
                    prints = nothing
                else:
                    if type(store) == list:
                        prints = "\n".join(store)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == dict:
                        noth = 0
                        store2 = []
                        for a, b in store.items():
                            if more[0] == "commands":
                                if a in ("adds", "changes", "deletes"):
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            if a.istitle():
                                                store2.append(a+" -- "+b)
                                            else:
                                                store2.append("`"+a+"` -- "+b)
                                        # prints = "\n".join(store)
                                else:
                                    if a.istitle():
                                        store2.append(+a+" -- "+b)
                                    else:store2.append("`"+a+"` -- "+b)
                            elif more[0] == "other":
                                if b:
                                    store2.append("\""+a+"\" -- "+b)
                            elif more[0] == "plans to update":
                                if a in ud["plans to update"].keys():
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            store2.append("\""+a.capitalize()+"\" -- "+b.capitalize())
                                        # prints = "\n".join(store)
                                else:
                                    store2.append("\""+a.capitalize()+"\" -- "+b.capitalize())
                        if store2:
                            prints = "\n".join(store2)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == str:
                        if len(store.split(" ")) == 1:
                            prints = store.capitalize()
                        else:
                            prints = store
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                prints += f"\n\nVersion: **v.{version}**"
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                embed.add_field(name=version+fn, value=prints, inline=False)
            else:
                formver = defformver(version)
                prints = []
                for a, b in ud.items():
                    if type(b) == list:
                        if not b:
                            continue
                        if formver == "Alpha.1":
                            if a == "note":
                                A1 = ""
                            else:
                                A1 = ":"
                        else:
                            A1 = ":"
                        prints.append("**"+a.capitalize()+A1+"**")
                        for c in b:
                            prints.append("> "+c)
                    elif type(b) == dict:
                        prints.append("**"+a.capitalize()+":**")
                        for c, d in b.items():
                            if not d:
                                continue
                            if a == "other":
                                prints.append("> \""+c+"\" -- "+d)
                                continue
                            prints.append("> **"+c.capitalize()+":**")
                            for e, f in d.items():
                                if a == "commands":
                                    if a.istitle():
                                        prints.append("> "+e+" -- "+f)
                                    else:
                                        prints.append("> `"+e+"` -- "+f)
                                if a == "plans to update":
                                    prints.append("> \""+e+"\" -- "+f.capitalize())
                    else:
                        prints.append(b)
                b = []
                for a in prints:
                    if "{}" in a:
                        a = a.format(version)
                    b.append(a)
                prints = b
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                if len("\n".join(prints)) > 1000:
                    a, b = prints[:len(prints)//2], prints[len(prints)//2:]
                    tlist = (deque(a), deque(b))
                    for i in range(2):
                        while len("\n".join(tlist[i])) > 1000:
                            if i == 0: tlist[1].appendleft(tlist[0].pop())
                            else: tlist[0].append(tlist[1].popleft())
                    a, b = tlist
                    embed.add_field(name=version, value="\n".join(a), inline=False)
                    embed.add_field(name="_ _", value="\n".join(b), inline=False)
                else:
                    embed.add_field(name=version, value="\n".join(prints), inline=False)
        else:
            theud = dict([next(reversed(udslist.items()))])
            for a in theud.keys():
                version = a
            for a in theud.values():
                ud = a
            formver = defformver(version)
            prints = []
            for a, b in ud.items():
                if type(b) == list:
                    if formver == "Alpha.1":
                        if a == "note":
                            A1 = ""
                        else:
                            A1 = ":"
                    else:
                        if not b:
                            continue
                        A1 = ":"
                    prints.append("**"+a.capitalize()+A1+"**")
                    for c in b:
                        prints.append("> "+c)
                elif type(b) == dict:
                    prints.append("**"+a.capitalize()+":**")
                    for c, d in b.items():
                        if not d:
                            continue
                        if a == "other":
                            prints.append("> \""+c+"\" -- "+d)
                            continue
                        prints.append("> **"+c.capitalize()+":**")
                        for e, f in d.items():
                            if a == "commands":
                                if e.istitle():
                                    prints.append("> "+e+" -- "+f)
                                else:
                                    prints.append("> `"+e+"` -- "+f)
                            if a == "plans to update":
                                prints.append("> \""+e+"\" -- "+f.capitalize())
                else:
                    prints.append(b)
            b = []
            for a in prints:
                if "{}" in a:
                    a = a.format(version)
                b.append(a)
            prints = b
            embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
            if len("\n".join(prints)) > 1000:
                a, b = prints[:len(prints)//2], prints[len(prints)//2:]
                tlist = (deque(a), deque(b))
                for i in range(2):
                    while len("\n".join(tlist[i])) > 1000:
                        if i == 0: tlist[1].appendleft(tlist[0].pop())
                        else: tlist[0].append(tlist[1].popleft())
                a, b = tlist
                embed.add_field(name=version, value="\n".join(a), inline=False)
                embed.add_field(name="_ _", value="\n".join(b), inline=False)
            else:
                a = "\n".join(prints)
                embed.add_field(name=version, value=a, inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commandB061.group(name="task", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_1"][1]["task"][0])
    async def taskB061(self, ctx):
        command = ctx.message.content.split(" ")
        if len(command) == 1:
            await ctx.send("task add\ntask change\ntask remove\n""on_work, pause, finished, waiting")
        else:
            await ctx.send("Wrong subcommand")

    @taskB061.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_1"][1]["task"][1]["add"])
    async def add(self, ctx, task):
        with open("data.json", mode="r", encoding="utf8") as f:
            dt = json.load(f)
        dt.setdefault("tasks", {})
        dt["tasks"].setdefault("on_work", [])
        if task in dt["tasks"]["on_work"]:
            await ctx.send("The task is already exist!")
            return
        dt["tasks"]["on_work"].append(task)
        with open("data.json", mode="w", encoding="utf8") as f:
            json.dump(dt, f, ensure_ascii=False, indent=4)
        await ctx.send(f"Added {task} into tasks stats.")

    @taskB061.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_1"][1]["task"][1]["change"])
    async def change(self, ctx, task, status):
        with open("data.json", mode="r", encoding="utf8") as f:
            dt = json.load(f)
        if dt["tasks"] == {}:
            await ctx.send("Haven't any tasks")
            return
        if dt["tasks"]["on_work"] == []:
            await ctx.send("Haven't any tasks")
            return
        if not status in ("on_work", "pause", "finished", "waiting"):
            await ctx.send("Invalid status was given")
            return
        dt["tasks"].setdefault("pause", [])
        dt["tasks"].setdefault("finished", [])
        dt["tasks"].setdefault("waiting", [])
        if task in dt["tasks"]["on_work"]:
            work = "on_work"
        elif task in dt["tasks"]["pause"]:
            work = "pause"
        elif task in dt["tasks"]["finished"]:
            work = "finished"
        elif task in dt["task"]["waiting"]:
            work = "waiting"
        else:
            await ctx.send("The task which was given is not exist")
            return
        dt["tasks"][work].remove(task)
        dt["tasks"][status].append(task)
        with open("data.json", mode="w", encoding="utf8") as f:
            json.dump(dt, f, ensure_ascii=False, indent=4)
        await ctx.send(f"Changed \"{task}\" to {status}")

    @taskB061.command(aliases=als["cogs"]["history"]["history"][1]["Beta_0_6_1"][1]["task"][1]["remove"])
    async def remove(self, ctx, task):
        with open("data.json", mode="r", encoding="utf8") as f:
            dt = json.load(f)
        count = 0
        same = 0
        for a, b in dt["tasks"].items():
            for c in b:
                if task == c:
                    same += 1
                else:
                    if task in c:
                        count += 1
        success = 0
        if count == 0:
            await ctx.send("Can't found")
            return
        elif count == 1:
            for a, b in dt["tasks"].items():
                for s in b[:]:
                    if task == s:
                        success = 1
                        b.remove(s)
                        await ctx.send("Remove success")
                for s in b[:]:
                    if task in s and success == 0:
                        success = 1
                        b.remove(s)
                        await ctx.send("Remove success")
            if success == 0:
                await ctx.send("Remove not success")
        else:
            await ctx.send("Invalid task")
        with open("data.json", mode="w", encoding="utf8") as f:
            json.dump(dt, f, indent=4)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Stable_1_0"][0])
    async def Stable_1_0(self, ctx):
        await ctx.send("History: Stable_1_0 commands:\n`command`")

    @Stable_1_0.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandS10(self, ctx):
        await ctx.send("History: Command commands:\n`search`\n`profitcomplete`")

    @commandS10.command(aliases=als["cogs"]["history"]["history"][1]["Stable_1_0"][1]["info"])
    async def info(self, ctx, *, req):
        icinfo = icd["info"]
        debug = []
        infoals = {}
        for a in als["ic"].values():
            infoals.update(a)
        for a, b in infoals.items():
            if not b == None and req in b:
                debug.append(a)
        if len(debug) > 1:
            await ctx.send("`EN0401`: Happened an unexpected or imposible thing, E1: Aliases")
            return
        elif debug:
            reqsl, = debug
        else:
            reqsl = req
        reqsl = "_".join(reqsl.split(" "))
        if reqsl.endswith("_u"): reqsl, techlv = reqsl[:-2], 1
        elif reqsl.endswith("_uu"): reqsl, techlv = reqsl[:-3], 2
        else: techlv = 0
        check = [b for a in icinfo.values() for b in a.keys()]
        if not reqsl in check:
            await ctx.send(f"`EN0004`: Cannot find info of: {req}, check your input")
            return
        for a in icinfo:
            if reqsl in icinfo[a]:
                infoclass = a
        theinfo = icinfo[infoclass][reqsl]
        embed = discord.Embed(title=f"Info -- {infoclass.capitalize()}", color=discord.Colour.greyple(), timestamp= datetime.datetime.now())
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="_ _", inline=False)
        ifimg = None
        output = []
        if infoclass == "assets":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            stuff = []
            if theinfo["market"] == True:
                stuff.append("It's tradable in market")
            elif theinfo["market"] == False:
                stuff.append("It's not tradable in market")
            if theinfo["retail"] == False:
                stuff.append("It cannot sold in retail store")
                stuff.append("It cannot be scrapped")
            else:
                stuff.append("It can sold in retail store")
                stuff.append("It can be scrapped into {} scraps".format(theinfo["retail"]))
            # output.append("\n".join(stuff))
            stuff2 = ["NPC market buy price(if valid): "+str(icd["assets"][reqsl]*2)]
            stuff2.append("NPC market sell price: "+str(icd["assets"][reqsl]))
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\n\n"+"\n".join(stuff)+"\n\n"+"\n".join(stuff2), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["assets"]:
                await ctx.send("`EN0402`: Cannot find assets -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["assets"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["assets"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if reqsl == "led": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Light-emitting_diode)")
            elif reqsl == "rubber": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/synthetic_rubber)")
            elif reqsl == "energy": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/electricity)")
            elif reqsl == "lamp": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/light_fixture)")
            elif reqsl == "ccd": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/charge-coupled_device)")
            elif reqsl == "hq": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Headquarters)")
            elif theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            ifimg = rf"images/info/{reqsl}.png" if Path(f"images/info/{reqsl}.png").is_file() else r"images/info/box.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "facilities":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"], inline=False)
            stuff = []
            for a, b in theinfo["construct"].items():
                if not a == "money":
                    stuff.append(f"{b:,}"+" **"+a.capitalize()+"**")
                else:
                    stuff.append("$"+f"{b:,}")
            # output.append("**Construction materials:**\n"+"\n".join(stuff))
            embed.add_field(name="Construction materials:", value="\n".join(stuff), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            stuff = "**Consumes**\n"
            facpro = icd["facilities"][reqsl]
            stuff += "None\n" if facpro["consumes"] == "None" else "\n".join([f"**{a.capitalize().replace('_', ' ')}** | {b:,}" for a, b in facpro["consumes"].items()])+"\n"
            stuff += "**Produces**\n"
            stuff += "None\n" if facpro["produces"] == "None" else "\n".join([f"**{a.capitalize().replace('_', ' ')}** | {b:,}" for a, b in facpro["produces"].items()])+"\n"
            stuff += "Speed: "+str(icd["facilities"][reqsl]["speed"])+" seconds"
            embed.add_field(name="Production:", value=stuff, inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["facilities"]:
                await ctx.send("`EN0402`: Cannot find facilities -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["facilities"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["facilities"][reqsl]))
            else: output.append("Aliases: None")
            if reqsl == "steel_mill":
                if random.randint(1, 50) == 1:
                    output.append("*I always typo this facility as \"still mill\"*")
            if reqsl == "furniture_factory":
                if random.randint(1, 5) == 1:
                    output.append("*Why the IdleCorp Wiki page has so many words...*")
                if random.randint(1, 10) == 1:
                    output.append("*Because the IdleCorp Wiki page has too many work, I had to change the layout of all...*")
            if reqsl.split("_")[-1] == "factory":
                if random.randint(1, 20) == 1:
                    output.append("*I really want to know who made this facility page...*")
            if reqsl == "research_chemical_factory":
                if random.randint(1, 3) == 1:
                    output.append("*Why this facility has so many aliases...*")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            if Path(f"images/info/{reqsl}.png").is_file(): ifimg = fr"images/info/{reqsl}.png"
            elif reqsl.endswith("mine"): ifimg = r"images/info/mine.png"
            elif reqsl in ("ccd_factory", "cpu_factory", "cell_phone_factory", "laptop_factory", "digital_camera_factory", "television_factory"): ifimg = "images/info/tech_facility.png"
            elif reqsl in ("retail_store", "research_facility", "customer_support_center", "hq"): ifimg = r"images/info/office_building.png"
            elif reqsl in ("research_chemical_factory", "prescription_drug_factory"): ifimg = r"images/info/chemical_plant.png"
            else: ifimg = r"images/info/facility.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "blueprints":
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\n\nRarity: {}".format(theinfo["rarity"])+"\n\nAll blueprints **cannot** trade and be sold in the market and the retail stores.", inline=False)
            stuff = []
            for a, b in theinfo["require"].items():
                stuff.append(f"{b:,}"+" **"+a.capitalize()+"**")
            embed.add_field(name="Requires:", value="\n".join(stuff), inline=False)
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["blueprints"]:
                await ctx.send("`EN0402`: Cannot find blueprints -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["blueprints"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["blueprints"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            output.append("\n".join(stuff))
            ifimg = r"images/info/blueprint.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "technologies":
            stuff = []
            if techlv == 2:
                if theinfo["upgrade"]["uu"] == "None":
                    await ctx.send("`EN0004`: The tech haven't \"uu\" upgrade")
                    return
                stuff.append(theinfo["upgrade"]["uu"]["icinfo"])
                stuff.append("Rarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["upgrade"]["uu"]["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
            elif techlv == 1:
                if theinfo["upgrade"]["u"] == "None":
                    await ctx.send("`EN0004`: The tech haven't \"u\" upgrade")
                    return
                stuff.append(theinfo["upgrade"]["u"]["icinfo"])
                stuff.append("Rarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["upgrade"]["u"]["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
                if theinfo["upgrade"]["uu"] != "None": stuff.append("\nNext upgrade: "+reqsl.replace("_", " ")+"uu")
            else:
                stuff.append(theinfo["icinfo"])
                stuff.append("\nRarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
                if theinfo["upgrade"]["u"] != "None": stuff.append("\nNext upgrade: "+reqsl.replace("_", " ")+"u")
            stuff.append("The tech affected on "+theinfo["affect"].capitalize())
            embed.add_field(name="IdleCorp Info(Examine):", value="\n".join(stuff), inline=False)
            stuff = "\n".join(["Level {} boost: {}".format(a, theinfo["boost"][a].replace("+", "and")) for a in range(len(theinfo["boost"]))])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["technologies"]:
                await ctx.send("`EN0402`: Cannot find blueprints -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["technologies"][reqsl+("_u" if techlv == 1 else ("_uu" if techlv == 2 else ""))] == None:
                output.append("Aliases: "+", ".join(als["ic"]["technologies"][reqsl+("_u" if techlv == 1 else ("_uu" if techlv == 2 else ""))]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            ifimg = r"images/info/technology.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "services":
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\nAffect: "+theinfo["effect"]+"\nCost: **${:,}**".format(theinfo["cost"]), inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["services"]:
                await ctx.send("`EN0402`: Cannot find services -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["services"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["services"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            if stuff: output.append("\n".join(stuff))
            ifimg = r"images/info/crane.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "pollicies":
            embed.add_field(name="IdleCorp Info(Examine):", value="Affect: "+theinfo["affect"]+"\nCost: {} *Funding points*".format(theinfo["cost"]), inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["services"]:
                await ctx.send("`EN0402`: Cannot find services -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["policies"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["policies"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            if stuff: output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        # embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="\n\n".join(output))
        if ifimg == None: await ctx.send(embed=embed)
        else:
            ifimg = discord.File(ifimg)
            embed.set_thumbnail(url=r"attachment://"+ifimg.filename)
            await ctx.send(embed=embed, file=ifimg)

    @commandS10.command(aliases=als["cogs"]["history"]["history"][1]["Stable_1_0"][1]["help"])
    async def help(self, ctx, *, cmd=None):
        if cmd == None:
            embed = discord.Embed(title="Help", description="Won't show Admin's, Owner's, Developer's commands", color=discord.Colour.green(), timestamp= datetime.datetime.now())
            for a, b in hps["commands"].items():
                embed.add_field(name=a.capitalize(), value=f"Descriptions/Features: {b[0]}\nSyntax: {b[1]}", inline=False)
        else:
            can = True
            cd = cmd
            cmds = cmd.split()
            if len(cmds) == 3:
                if cmds[-1] == "command":
                    cmds = [cmds[0]]+["command"]
            out, fir = [], False
            for a, b in hps["info"]["aliases"].items():
                for e, f in b.items():
                    for a in cmds:
                        if isinstance(f, dict):
                            if e != cmds[0]: continue
                            if ("__init__" in f) and (a in f["__init__"]):
                                    fir = True
                                    out.append(e)
                            else:
                                g = f

                                for c, d in g.items():
                                    if a in d:
                                        out.append(c)
                                    elif isinstance(d, dict):
                                        if "__init__" in d and d["__init__"] == a:
                                            out.append(d["__init__"])
                                            continue
                                    g = d
                        elif a in f or a == e:
                            fir = True
                            out.append(e)
            cmds = out
            if fir == False or cmds[0] not in hps["commands"]:
                await ctx.send("`EN0004`: Cannot find command info named `{}`".format(cd))
                return
            embed = discord.Embed(title="Help -- "+cmds[0].capitalize(), color=discord.Colour.green(), timestamp= datetime.datetime.now())
            res = hps["commands"][cmds[0]]
            for a, b in hps["info"].items():
                if a == "aliases":
                    for c, d in b.items():
                        for e, f in d.items():
                            g = f
                            if e != cmds[0]: continue
                            for cmd in cmds:
                                if cmd not in g: continue
                                if not isinstance(g, dict): break
                                g = g[cmd]
                            res.append(g["__init__"] if isinstance(g, dict) else g)
                            can = False
                            break
                elif a == "details":
                    for c, d in b.items():
                        e = d
                        for cmd in cmds:
                            if cmd not in e: continue
                            e = e[cmd]
                        if type(e) == dict and "__init__" not in e: continue
                        s = e["__init__"] if isinstance(e, dict) else e
                        if not s: break
                        # if re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s):
                        #     if re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s) == "-1":
                        #         s = s.format(cmds[-1])
                        #     elif re.search(r"(?<=\{)([A-Za-z0-9-])+(?<=\})", s) == "-2":
                        #         s - s.format(cmds[-2])
                        if "{" and "}" in s: s - s.format(**zip([str(-g) for g in range(1, len(cmds)+1)[::-1]], cmds[:-1]))
                        res.append(s)
                        can = False
                        break
            if can == True:
                await ctx.send("`EN0004`: Cannot find command info named `{}`".format(cd))
                return
            out = [("Description: "+res[0])]+[("Syntax: "+res[1])]+[("Aliases: "+", ".join(res[2]))]
            if len(res) == 4:
                out.append("Details: "+res[3])
            embed.add_field(name=" ".join(cmds), value="\n\n".join(out), inline=False)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_1"][0])
    async def Stable_1_0_1(self, ctx):
        await ctx.send("History: Stable_1_0_1 commands:\n`command`")

    @Stable_1_0_1.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandS101(self, ctx):
        await ctx.send("History: Command commands:\n`search`\n`profitcomplete`")

    @commandS101.command(aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_1"][1]["speed"])
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
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s). In Alpha.0.2, this command just calculate for one-type-facility in **one action**! ", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(3)
        await msg.edit(embed=embed)

    @commandS101.command(aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_1"][1]["profit"])
    async def profit(self, ctx, *, args):#facility, number
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
        if "flag" in locals(): num *= {"day": 60*60*24, "hour": 60*60, "minute": 60}.get(flag, 1)
        sol = calculate.product_profit(fac, "all", num)
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
                s.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
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
                s2.append(" | ".join(list(("**"+a.capitalize().replace("_", " ")+"**", "$"+b))))
            p = "\n".join(s2)
        else:
            p = "None"
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
        fac_ = fac.replace("_", " ")
        embed = discord.Embed(title=fac_.capitalize(), color=discord.Colour.blue(), description="Unit: "+unit.capitalize(), timestamp= datetime.datetime.now())
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Consumes", value=c, inline=False)
        embed.add_field(name="Produces", value=p, inline=False)
        embed.add_field(name="Profit", value=pf, inline=False)
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s).\nThe **profit** is meaning that if your sourse of the facility is from buying from npc market, then the profit, if you are not buying the sourse from npc market, then the **produces** part.", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(3)
        await msg.edit(embed=embed)

    @commandS101.command(aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_1"][1]["profitcomplete"])
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
            if flag in flagals.values(): flag = flag; unit = flag
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
        embed.add_field(name="Note", value="The result of this command can't get anything of region(s).\nThe **profit** is meaning that if your sourse of the facility is from buying from npc market, then the profit, if you are not buying the sourse from npc market, then the **produces** part.", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        ukwembed = discord.Embed(title="Did you know", color=discord.Colour.darker_gray(), timestamp= datetime.datetime.now())
        ukwembed.add_field(name="_ _", value=you_know.you_know())
        ukwembed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        ukwembed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=ukwembed)
        time.sleep(3)
        await msg.edit(embed=embed)

    @commandS101.group(name="suggest", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_1"][1]["suggest"][0])
    async def suggestS101(self, ctx):
        command = ctx.message.content.split(" ")
        if len(command) == 1:
            await ctx.send("Commands:\n`suggest add`\n`suggest edit`\n`suggest vote`\n`suggest info`"+("\n`suggest change`\n`suggest remove`" if [a for a in ctx.author.roles if a.name in ("Owner", "ICP Developer")] else ""))
        else:
            await ctx.send("Wrong subcommand")

    @suggestS101.command(aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_1"][1]["suggest"][1]["info"])
    async def info(self, ctx, suggest_id:int):
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" WHERE suggestion_id = {}".format(suggest_id))
            if not cursor:
                await ctx.send("`EN0006`: The suggestion id was invalid.")
                return
            value = dict(zip([a[0] for a in cursor.description], cursor.fetchall()[0]))
        embed = discord.Embed(title="Suggestion info", color=discord.Colour.from_rgb(255, 255, 190), description="**{}**".format(len(value["votes"])), timestamp=datetime.datetime.now())
        embed.set_author(name=str(self.bot.get_user(value["user_id"])), icon_url=self.bot.get_user(value["user_id"]).avatar_url)
        embed.add_field(name="{} \t\t\t [{}]".format(value["suggestion_id"], value["status"].capitalize().replace("_", " ")), value="{}\n\nSuggestion creator: <@!{}>\nCreated at: {} {}:{}".format(value["suggestions"], value["user_id"], value["date"].date(), value["date"].hour, value["date"].minute))
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @suggestS101.command(aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_1"][1]["updates"])
    async def updates(self, ctx, *, args=None):
        def defformver(ver):
            if ver == "Alpha.0.2":
                formver = "Alpha.1"
            elif ver in ("Alpha.0.2.1", "Alpha.0.3.0", "Beta.0.1.0"):
                formver = "Alpha.2"
            else:
                formver = "Alpha.2"
            return formver
        if args != None:
            arg = string_handler.filter(args)
            if arg[1]:
                await ctx.send("`EN0008`: Argument error: type number")
                return
            flags = string_handler.flags(arg[0])
            if flags[1]:
                await ctx.send("`EN0001`: Flag type error, `--`")
                return
            if len(flags[0]) > 1:
                await ctx.send("`EN0002`: Too many flags")
                return
            elif len(flags[0]) == 1:
                for a in flags[0]:
                    flag = a
            else:
                flag = None
            if flag != None:
                if arg[0].index(flag) > 0:
                    await ctx.send("`EN0007`: Argument flag error")
                    return
            if flag != None:
                flag = flag[2:]
            if len(flags[2]) > 1:
                await ctx.send("`EN0008`: String")
                return
            elif len(flags[2]) == 1:
                for a in flags[2]:
                    mores = a
            else:
                mores = None
            if flag == None:
                theud = dict([next(reversed(udslist.items()))])
                for a in theud.keys():
                    version = a
                for a in theud.values():
                    ud = a
            else:
                ud = udslist[flag]
                version = flag
            if mores != None:
                more = mores.split(".")
                stuff = []
                for a in more:
                    stuff.append(a.replace("_", " "))
                # if len(more) == 1:
                #     for a in more:
                #         for c, d in als["updates list"]["first"].items():
                #             if a in c:
                #                 a = c
                #         prints =  ud[a]
                # else:
                fn = ""
                b = ud
                first = als["updates list"]["first"]
                second = als["updates list"]["second"]
                third = als["updates list"]["third"]
                i = 0
                moo = []
                for a in more:
                    if i == 0:
                        for c, d in first.items():
                            if a in d:
                                a = c
                    else:
                        if a != "plans to update":
                            for c, d in second.items():
                                if a in d:
                                    a = c
                        else:
                            for c, d in third.items():
                                if a in d:
                                    a = c
                    if a not in b:
                        await ctx.send("`EN0004`: The argument is invalid or unexist in this version of update")
                    b = b[a]
                    moo.append(a)
                    i += 1
                more = moo
                store = b
                nothing = "\n**Nothing to show**"
                if not store:
                    prints = nothing
                else:
                    if type(store) == list:
                        prints = "\n".join(store)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == dict:
                        noth = 0
                        store2 = []
                        for a, b in store.items():
                            if more[0] == "commands":
                                if a in ("adds", "changes", "deletes"):
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            if a.istitle():
                                                store2.append(a+" -- "+b)
                                            else:
                                                store2.append("`"+a+"` -- "+b)
                                        # prints = "\n".join(store)
                                else:
                                    if a.istitle():
                                        store2.append(+a+" -- "+b)
                                    else:store2.append("`"+a+"` -- "+b)
                            elif more[0] == "other":
                                if b:
                                    store2.append("\""+a+"\" -- "+b)
                            elif more[0] == "plans to update":
                                if a in ud["plans to update"].keys():
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            store2.append("\""+a.capitalize()+"\" -- "+(b if b.startswith("v") else b.capitalize()))
                                        # prints = "\n".join(store)
                                else:
                                    store2.append("\""+a.capitalize()+"\" -- "+(b if b.startswith("v") else b.capitalize()))
                        if store2:
                            prints = "\n".join(store2)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == str:
                        if len(store.split(" ")) == 1:
                            prints = store.capitalize()
                        else:
                            prints = store
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                prints += f"\n\nVersion: **v.{version}**"
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                embed.add_field(name=version+fn, value=prints, inline=False)
            else:
                formver = defformver(version)
                prints = []
                for a, b in ud.items():
                    if type(b) == list:
                        if not b:
                            continue
                        if formver == "Alpha.1":
                            if a == "note":
                                A1 = ""
                            else:
                                A1 = ":"
                        else:
                            A1 = ":"
                        prints.append("**"+a.capitalize()+A1+"**")
                        for c in b:
                            prints.append("> "+c)
                    elif type(b) == dict:
                        if not next([len(a) for a in b.values()]): continue
                        prints.append("**"+a.capitalize()+":**")
                        for c, d in b.items():
                            if not d:
                                continue
                            if a == "other":
                                prints.append("> \""+c+"\" -- "+d)
                                continue
                            prints.append("> **"+c.capitalize()+":**")
                            for e, f in d.items():
                                if a == "commands":
                                    if a.istitle():
                                        prints.append("> "+e+" -- "+f)
                                    else:
                                        prints.append("> `"+e+"` -- "+f)
                                if a == "plans to update":
                                    prints.append("> \""+e+"\" -- "+f.capitalize())
                    else:
                        prints.append(b)
                b = []
                for a in prints:
                    if "{}" in a:
                        a = a.format(version)
                    b.append(a)
                prints = b
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                if len("\n".join(prints)) > 1000:
                    a, b = prints[:len(prints)//2], prints[len(prints)//2:]
                    tlist = (deque(a), deque(b))
                    for i in range(2):
                        while len("\n".join(tlist[i])) > 1000:
                            if i == 0: tlist[1].appendleft(tlist[0].pop())
                            else: tlist[0].append(tlist[1].popleft())
                    a, b = tlist
                    embed.add_field(name=version, value="\n".join(a), inline=False)
                    embed.add_field(name="_ _", value="\n".join(b), inline=False)
                else:
                    embed.add_field(name=version, value="\n".join(prints), inline=False)
        else:
            theud = dict([next(reversed(udslist.items()))])
            for a in theud.keys():
                version = a
            for a in theud.values():
                ud = a
            formver = defformver(version)
            prints = []
            for a, b in ud.items():
                if type(b) == list:
                    if formver == "Alpha.1":
                        if a == "note":
                            A1 = ""
                        else:
                            A1 = ":"
                    else:
                        if not b:
                            continue
                        A1 = ":"
                    prints.append("**"+a.capitalize()+A1+"**")
                    for c in b:
                        prints.append("> "+c)
                elif type(b) == dict:
                    if not next((len(a) for a in b.values())): continue
                    prints.append("**"+a.capitalize()+":**")
                    for c, d in b.items():
                        if not d:
                            continue
                        if a == "other":
                            prints.append("> \""+c+"\" -- "+d)
                            continue
                        prints.append("> **"+c.capitalize()+":**")
                        for e, f in d.items():
                            if a == "commands":
                                if e.istitle():
                                    prints.append("> "+e+" -- "+f)
                                else:
                                    prints.append("> `"+e+"` -- "+f)
                            if a == "plans to update":
                                prints.append("> \""+e+"\" -- "+f.capitalize())
                else:
                    prints.append(b)
            b = []
            for a in prints:
                if "{}" in a:
                    a = a.format(version)
                b.append(a)
            prints = b
            embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
            if len("\n".join(prints)) > 1000:
                a, b = prints[:len(prints)//2], prints[len(prints)//2:]
                tlist = (deque(a), deque(b))
                for i in range(2):
                    while len("\n".join(tlist[i])) > 1000:
                        if i == 0: tlist[1].appendleft(tlist[0].pop())
                        else: tlist[0].append(tlist[1].popleft())
                a, b = tlist
                embed.add_field(name=version, value="\n".join(a), inline=False)
                embed.add_field(name="_ _", value="\n".join(b), inline=False)
            else:
                a = "\n".join(prints)
                embed.add_field(name=version, value=a, inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @history.group(invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_2"][0])
    async def Stable_1_0_2(self, ctx):
        await ctx.send("History: Stable_1_0_2 commands:\n`command`")

    @Stable_1_0_2.group(name="command", invoke_without_command=True, aliases=als["cogs"]["history"]["history"][1]["command"])
    async def commandS102(self, ctx):
        await ctx.send("History: Command commands:\n`search`\n`profitcomplete`")

    @commandS102.command(aliases=als["cogs"]["history"]["history"][1]["Stable_1_0_2"][1]["updates"])
    async def updates(self, ctx, *, args=None):
        def defformver(ver):
            if ver == "Alpha.0.2":
                formver = "Alpha.1"
            elif ver in ("Alpha.0.2.1", "Alpha.0.3.0", "Beta.0.1.0"):
                formver = "Alpha.2"
            else:
                formver = "Alpha.2"
            return formver
        if args != None:
            arg = string_handler.filter(args)
            if arg[1]:
                await ctx.send("`EN0008`: Argument error: type number")
                return
            flags = string_handler.flags(arg[0])
            if flags[1]:
                await ctx.send("`EN0001`: Flag type error, `--`")
                return
            if len(flags[0]) > 1:
                await ctx.send("`EN0002`: Too many flags")
                return
            elif len(flags[0]) == 1:
                for a in flags[0]:
                    flag = a
            else:
                flag = None
            if flag != None:
                if arg[0].index(flag) > 0:
                    await ctx.send("`EN0007`: Argument flag error")
                    return
            if flag != None:
                flag = flag[2:]
            if len(flags[2]) > 1:
                await ctx.send("`EN0008`: String")
                return
            elif len(flags[2]) == 1:
                for a in flags[2]:
                    mores = a
            else:
                mores = None
            if flag == None:
                theud = dict([next(reversed(udslist.items()))])
                for a in theud.keys():
                    version = a
                for a in theud.values():
                    ud = a
            else:
                ud = udslist[flag]
                version = flag
            if mores != None:
                more = mores.split(".")
                stuff = []
                for a in more:
                    stuff.append(a.replace("_", " "))
                # if len(more) == 1:
                #     for a in more:
                #         for c, d in als["updates list"]["first"].items():
                #             if a in c:
                #                 a = c
                #         prints =  ud[a]
                # else:
                fn = ""
                b = ud
                first = als["updates list"]["first"]
                second = als["updates list"]["second"]
                third = als["updates list"]["third"]
                i = 0
                moo = []
                for a in more:
                    if i == 0:
                        for c, d in first.items():
                            if a in d:
                                a = c
                    else:
                        if a != "plans to update":
                            for c, d in second.items():
                                if a in d:
                                    a = c
                        else:
                            for c, d in third.items():
                                if a in d:
                                    a = c
                    if a not in b:
                        await ctx.send("`EN0004`: The argument is invalid or unexist in this version of update")
                    b = b[a]
                    moo.append(a)
                    i += 1
                more = moo
                store = b
                nothing = "\n**Nothing to show**"
                if not store:
                    prints = nothing
                else:
                    if type(store) == list:
                        prints = "\n".join(store)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == dict:
                        noth = 0
                        store2 = []
                        for a, b in store.items():
                            if more[0] == "commands":
                                if a in ("adds", "changes", "deletes"):
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            if a.istitle():
                                                store2.append(a+" -- "+b)
                                            else:
                                                store2.append("`"+a+"` -- "+b)
                                        # prints = "\n".join(store)
                                else:
                                    if a.istitle():
                                        store2.append(+a+" -- "+b)
                                    else:store2.append("`"+a+"` -- "+b)
                            elif more[0] == "other":
                                if b:
                                    store2.append("\""+a+"\" -- "+b)
                            elif more[0] == "plans to update":
                                if a in ud["plans to update"].keys():
                                    if not b:
                                        prints = nothing
                                        noth = 1
                                    else:
                                        store2.append("**"+a.capitalize()+":**")
                                        for a, b in b.items():
                                            store2.append("\""+a.capitalize()+"\" -- "+(b if b.startswith("v") else b.capitalize()))
                                        # prints = "\n".join(store)
                                else:
                                    store2.append("\""+a.capitalize()+"\" -- "+(b if b.startswith("v") else b.capitalize()))
                        if store2:
                            prints = "\n".join(store2)
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                    elif type(store) == str:
                        if len(store.split(" ")) == 1:
                            prints = store.capitalize()
                        else:
                            prints = store
                        store = []
                        for a in more:
                            store.append(a.capitalize())
                        a = " - ".join(store)
                        fn = f" -- {a}"
                prints += f"\n\nVersion: **v.{version}**"
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                embed.add_field(name=version+fn, value=prints, inline=False)
            else:
                formver = defformver(version)
                prints = []
                for a, b in ud.items():
                    if type(b) == list:
                        if not b:
                            continue
                        if formver == "Alpha.1":
                            if a == "note":
                                A1 = ""
                            else:
                                A1 = ":"
                        else:
                            A1 = ":"
                        prints.append("**"+a.capitalize()+A1+"**")
                        for c in b:
                            prints.append("> "+c)
                    elif type(b) == dict:
                        if not next((len(a) for a in b.values())): continue
                        prints.append("**"+a.capitalize()+":**")
                        for c, d in b.items():
                            if not d:
                                continue
                            if a == "other":
                                prints.append("> \""+c+"\" -- "+d)
                                continue
                            prints.append("> **"+c.capitalize()+":**")
                            for e, f in d.items():
                                if a == "commands":
                                    if a.istitle():
                                        prints.append("> "+e+" -- "+f)
                                    else:
                                        prints.append("> `"+e+"` -- "+f)
                                if a == "plans to update":
                                    prints.append("> \""+e+"\" -- "+f.capitalize())
                    else:
                        prints.append(b)
                b = []
                for a in prints:
                    if "{}" in a:
                        a = a.format(version)
                    b.append(a)
                prints = b
                embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
                if len("\n".join(prints)) > 1000:
                    a, b = prints[:len(prints)//2], prints[len(prints)//2:]
                    tlist = (deque(a), deque(b))
                    for i in range(2):
                        while len("\n".join(tlist[i])) > 1000:
                            if i == 0: tlist[1].appendleft(tlist[0].pop())
                            else: tlist[0].append(tlist[1].popleft())
                    a, b = tlist
                    embed.add_field(name=version, value="\n".join(a), inline=False)
                    embed.add_field(name="_ _", value="\n".join(b), inline=False)
                else:
                    embed.add_field(name=version, value="\n".join(prints), inline=False)
        else:
            theud = dict([next(reversed(udslist.items()))])
            for a in theud.keys():
                version = a
            for a in theud.values():
                ud = a
            formver = defformver(version)
            prints = []
            for a, b in ud.items():
                if type(b) == list:
                    if formver == "Alpha.1":
                        if a == "note":
                            A1 = ""
                        else:
                            A1 = ":"
                    else:
                        if not b:
                            continue
                        A1 = ":"
                    prints.append("**"+a.capitalize()+A1+"**")
                    for c in b:
                        prints.append("> "+c)
                elif type(b) == dict:
                    if not next((len(a) for a in b.values())): continue
                    prints.append("**"+a.capitalize()+":**")
                    for c, d in b.items():
                        if not d:
                            continue
                        if a == "other":
                            prints.append("> \""+c+"\" -- "+d)
                            continue
                        prints.append("> **"+c.capitalize()+":**")
                        for e, f in d.items():
                            if a == "commands":
                                if e.istitle():
                                    prints.append("> "+e+" -- "+f)
                                else:
                                    prints.append("> `"+e+"` -- "+f)
                            if a == "plans to update":
                                prints.append("> \""+e+"\" -- "+f.capitalize())
                else:
                    prints.append(b)
            b = []
            for a in prints:
                if "{}" in a:
                    a = a.format(version)
                b.append(a)
            prints = b
            embed = discord.Embed(title="Bot Updates", color=discord.Colour.blurple(), timestamp= datetime.datetime.now())
            if len("\n".join(prints)) > 1000:
                a, b = prints[:len(prints)//2], prints[len(prints)//2:]
                tlist = (deque(a), deque(b))
                for i in range(2):
                    while len("\n".join(tlist[i])) > 1000:
                        if i == 0: tlist[1].appendleft(tlist[0].pop())
                        else: tlist[0].append(tlist[1].popleft())
                a, b = tlist
                embed.add_field(name=version, value="\n".join(a), inline=False)
                embed.add_field(name="_ _", value="\n".join(b), inline=False)
            else:
                a = "\n".join(prints)
                embed.add_field(name=version, value=a, inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(history(bot))