import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.calculate import calculate
from cmds.string_handler import string_handler

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)
with open("rules.json", mode="r", encoding="utf8") as f:
    rulej = json.load(f)

class rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["rules"]["rules"])
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
                    await ctx.send("`EN0007`: Arguments error")
                    return
            else:
                if args.isdigit():
                    args = int(args)
            if arg[1] != []:
                if len(arg[1]) > 1:
                    await ctx.send("`EN0007`: Too much argument: type number")
                    return
                for a in arg[1]:
                    num = a
            else:
                num = None
            if arg[0] != []:
                if len(arg[0]) > 1:
                    await ctx.send("`EN0007`: Too much argument: type string")
                    return
                for a in arg[0]:
                    if a.startswith("--"):
                        flag = a[2:]
                    else:
                        await ctx.send("`EN0007`: Argument error: type string")
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
        
def setup(bot):
    bot.add_cog(rules(bot))