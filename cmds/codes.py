import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.calculate import calculate

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)
with open("codes.json", mode="r", encoding="utf8") as f:
    cdslist = json.load(f)

class codes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Update:
    #   U, perm(D/A/N), {from 0}type(command(Hiperm), command(normal), event(include you_know), codes), commands(add, change, remove, add(history), change(history), remove(history), codes, aliases, other), size(history(1), statusread(1), status(2), codes(1), aliases(1), you_know(2)), number(two digits)
    # Error:
    #   E, perm(D/A/N), {from 0}type(command, command(specific), event), {from 0}type(badargument, looperror, defineerror, checkerror(permission etc), argumenterror(unexpect)), number(two digits)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @commands.group(invoke_without_command=True, aliases=als["cogs"]["codes"]["codes"][0])
    async def codes(self, ctx):
        if " ".join(ctx.message.content.split()[1:]) in ("version", "v"):
            await ctx.send("The code version is {}, the versions have: {}".format(cdslist["version"], ", ".join([a.capitalize() for a in cdslist["oldver"].keys()]+[cdslist["version"]])))
            return
        elif " ".join(ctx.message.content.split()[1:]) in ("list", "l"):
            if discord.utils.get(ctx.author.roles, name="Owner") or discord.utils.get(ctx.author.roles, name="ICP Deceloper"):
                await ctx.send("The list of codes:\n"+"\n".join([b for a in cdslist["codes"].values() for b in a.keys()])+"\n\nCode version: v.{}".format(cdslist["version"]))
            elif discord.utils.get(ctx.author.roles, name="Admin"):
                await ctx.send("The list of codes:\n"+"\n".join([b for a in cdslist["codes"].values() for b in a.keys() if "D" not in b])+"\n\nCode version: v.{}".format(cdslist["version"]))
            else:
                await ctx.send("The list of codes:\n"+"\n".join([b for a in cdslist["codes"].values() for b in a.keys() if "D" or "A" not in b])+"\n\nCode version: v.{}".format(cdslist["version"]))
            return
        await ctx.send("Commands: `update`, `error`\n"
        "The current Codes version is v.{}".format(cdslist["version"]))

    @codes.command(aliases=als["cogs"]["codes"]["codes"][1]["update"])
    async def update(self, ctx, *, args):
        await self.bot.wait_until_ready()
        cds = cdslist["codes"]
        oldnew = cdslist["oldnew"]
        oldver = cdslist["oldver"]
        guild = self.bot.get_guild(jdata["guild_id"])
        args = args.split()
        code = args[-1]
        if len(args) != 1:
            oth = args[:-1]
            for a in oth:
                if not a.startswith("--"):
                    await ctx.send("`EN0001`: Flags error (\"--\")")
                    return
            if len(oth) > 1:
                await ctx.send("`EN0002`: Flags error, 1")
                return
            oth, = oth
            if oth == "--old":
                if code not in cds["update"].keys():
                    for a, b in oldnew.items():
                        if a == code:
                            code = b
            elif oth[2:].lower() in oldver.keys():
                oth = oth[2:].lower()
                if oldver[oth].setdefault("update"):
                    if oldver[oth]["update"].setdefault(code):
                        if "D" or "A" in code:
                            if "D" in code and not (discord.utils.get(ctx.author.roles, name="Owner") or discord.utils.get(ctx.author.roles, name="ICP Developer")):
                                await ctx.send("`EN0301`: The code is required permissions.")
                                return
                            elif "A" and not discord.utils.get(ctx.author.roles, name="Admin"):
                                await ctx.send("`EN0302`: The code is required permissions.")
                                return
                            else:
                                embed = discord.Embed(title=f"Update code {a}", description=oldver[oth]["update"][code]+"\n\nCode v."+cdslist["version"], color=discord.Color.dark_red(), timestamp= datetime.datetime.now())
                                embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
                                await ctx.send(embed=embed)
                                return
                        else:
                            embed = discord.Embed(title=f"Update code {a}", description=oldver[oth]["update"][code]+"\n\nCode v."+cdslist["version"], color=discord.Color.dark_red(), timestamp= datetime.datetime.now())
                            embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
                            await ctx.send(embed=embed)
                            return
                    else:
                        await ctx.send(f"`EN1001`: Invalid code entered in {oth}.")
                        return
            else:
                await ctx.send("`EN0003`: Invalid flag.")
                return
        for a, b in cds["update"].items():
            if code == a:
                if code[1] != "N" and not (discord.utils.get(ctx.author.roles, name="Owner") or discord.utils.get(ctx.author.roles, name="Admin") or discord.utils.get(ctx.author.roles, name="ICP Developer")):
                    break
                embed = discord.Embed(title=f"Update code {a}", description=b+"\n\nCode v."+cdslist["version"], color=discord.Color.dark_red(), timestamp= datetime.datetime.now())
                embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return
        #Check Error
        if code[0] != "U":
            await ctx.send("`EN1002`: Wrong code type")
            return
        if len(code) == 1:
            await ctx.send("`EN1001`: Invalid code entered")
            return
        if code[1] == "D":
            if not (discord.utils.get(ctx.author.roles, name="Owner") or discord.utils.get(ctx.author.roles, name="ICP Deceloper")):
                await ctx.send("`EN0301`: The code is required permissions.")
                return
        elif code[1] == "A":
            if not discord.utils.get(ctx.author.roles, name="Admin"):
                await ctx.send("`EN0302`: The code is required permissions.")
                return
        await ctx.send("`EN1001`: Invalid code entered")
            
    @codes.command(aliases=als["cogs"]["codes"]["codes"][1]["error"])
    async def error(self, ctx, *, args):
        await self.bot.wait_until_ready()
        cds = cdslist["codes"]
        oldnew = cdslist["oldnew"]
        oldver = cdslist["oldver"]
        guild = self.bot.get_guild(jdata["guild_id"])
        args = args.split()
        code = args[-1]
        if len(args) != 1:
            oth = args[:-1]
            for a in oth:
                if not a.startswith("--"):
                    await ctx.send("`EN0001`: Flags error (\"--\")")
                    return
            if len(oth) > 1:
                await ctx.send("`EN0002`: Flags error, 1")
                return
            oth, = oth
            if oth == "--old":
                if code not in cds["error"].keys():
                    for a, b in oldnew.items():
                        if a == code:
                            code = b
            elif oth[2:].lower() in oldver.keys():
                oth = oth[2:].lower()
                if oldver[oth].setdefault("error"):
                    if oldver[oth]["error"].setdefault(code):
                        if "D" or "A" in code:
                            if "D" in code and not (discord.utils.get(ctx.author.roles, name="Owner") or discord.utils.get(ctx.author.roles, name="ICP Developer")):
                                await ctx.send("`EN0301`: The code is required permissions.")
                                return
                            elif "A" and not discord.utils.get(ctx.author.roles, name="Admin"):
                                await ctx.send("`EN0302`: The code is required permissions.")
                                return
                            else:
                                embed = discord.Embed(title=f"Error code {a}", description=oldver[oth]["error"][code]+"\n\nCode v."+cdslist["version"], color=discord.Color.dark_red(), timestamp= datetime.datetime.now())
                                embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
                                await ctx.send(embed=embed)
                                return
                        else:
                            embed = discord.Embed(title=f"Error code {a}", description=oldver[oth]["update"][code]+"\n\nCode v."+cdslist["version"], color=discord.Color.dark_red(), timestamp= datetime.datetime.now())
                            embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
                            await ctx.send(embed=embed)
                            return
                    else:
                        await ctx.send(f"`EN1001`: Invalid code entered in {oth}.")
                        return
            else:
                await ctx.send("`EN0003`: Invalid flag.")
                return
        for a, b in cds["error"].items():
            if code == a:
                if code[1] != "N" and not (discord.utils.get(ctx.author.roles, name="Owner") or discord.utils.get(ctx.author.roles, name="Admin") or discord.utils.get(ctx.author.roles, name="ICP Developer")):
                    break
                embed = discord.Embed(title=f"Error code {a}", description=b+"\n\nCode v."+cdslist["version"], color=discord.Color.dark_red(), timestamp= datetime.datetime.now())
                embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return
        #Check Error
        if code[0] != "E":
            await ctx.send("`EN1002`: Wrong code type")
            return
        if len(code) == 1:
            await ctx.send("`EN1001`: Invalid code entered")
            return
        if code[1] == "D":
            if not (discord.utils.get(ctx.author.roles, name="Owner") or discord.utils.get(ctx.author.roles, name="ICP Deceloper")):
                await ctx.send("`EN0301`: The code is required permissions.")
                return
        elif code[1] == "A":
            if not discord.utils.get(ctx.author.roles, name="Admin"):
                await ctx.send("`EN0302`: The code is required permissions.")
                return
        await ctx.send("`EN1001`: Invalid code entered")

def setup(bot):
    bot.add_cog(codes(bot))