import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.string_handler import string_handler
from collections import deque

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)
with open("updates.json", mode="r", encoding="utf8") as f:
    udslist = json.load(f)

class updates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["updates"]["updates"])
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
                        if not sum([len(a) for a in b.values()]): continue
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
                    if not sum([len(a) for a in b.values()]): continue
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
    bot.add_cog(updates(bot))