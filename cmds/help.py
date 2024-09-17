import discord
from discord.ext import commands, tasks
import json
import datetime
import asyncio
from pathlib import Path
import re

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("help.json", mode="r", encoding="utf8") as f:
    hps = json.load(f)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["help"]["help"])
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
                            print("a")
                            if ("__init__" in f) and ((a in f["__init__"]) or a == e):
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

def setup(bot):
    bot.add_cog(help(bot))