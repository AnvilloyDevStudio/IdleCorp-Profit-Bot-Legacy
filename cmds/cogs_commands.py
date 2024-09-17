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

class cogs_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["cog_commands"]["listcogs"])
    @commands.has_any_role(801052590389329930, 801052697498746920)
    async def listcogs(self, ctx):
        lists = []
        for filename in os.listdir('./cmds'):
            if filename.endswith('.py'):
                lists.append(f'{filename[:-3]}')
        await ctx.send("\n".join(lists))

    def load_aliases(input_):
        lists = als["cogs_loads"]
        for a, b in lists.items():
            for c in b:
                if input_ == c:
                    return a

    @commands.command(aliases=als["cogs"]["cog_commands"]["load"])
    @commands.has_any_role(801052590389329930, 801052697498746920)
    async def load(self, ctx, extension):
        lists = als["cogs_loads"]
        res = []
        for a in lists.values():
            if type(a) == list:
                for b in a:
                    res.append(b)
            else:
                res.append(a)
        if not extension in res:
            self.bot.load_extension(f'cmds.{extension}')
            await ctx.send(f'Loaded **{extension}**')
        else:
            a = cogs_commands.load_aliases(extension)
            self.bot.load_extension(f'cmds.{a}')
            await ctx.send(f'Loaded **{a}**')

    @commands.command(aliases=als["cogs"]["cog_commands"]["unload"])
    @commands.has_any_role(801052590389329930, 801052697498746920)
    async def unload(self, ctx, extension):
        lists = als["cogs_loads"]
        res = []
        for a in lists.values():
            if type(a) == list:
                for b in a:
                    res.append(b)
            else:
                res.append(a)
        if not extension in res:
            self.bot.unload_extension(f'cmds.{extension}')
            await ctx.send(f'Unloaded **{extension}**')
        else:
            a = cogs_commands.load_aliases(extension)
            self.bot.unload_extension(f'cmds.{a}')
            await ctx.send(f'Unloaded **{a}**')

    @commands.command(aliases=als["cogs"]["cog_commands"]["reload"])
    @commands.has_any_role(801052590389329930, 801052697498746920)
    async def reload(self, ctx, extension):
        lists = als["cogs_loads"]
        res = []
        for a in lists.values():
            if type(a) == list:
                for b in a:
                    res.append(b)
            else:
                res.append(a)
        if not extension in res:
            self.bot.reload_extension(f'cmds.{extension}')
            await ctx.send(f'Reloaded **{extension}**')
        else:
            a = cogs_commands.load_aliases(extension)
            self.bot.reload_extension(f'cmds.{a}')
            await ctx.send(f'Reloaded **{a}**')

    @commands.command(aliases=als["cogs"]["cog_commands"]["sss"])
    @commands.has_any_role(801052590389329930, 801052697498746920)
    async def sss(self, ctx):
        for filename in os.listdir('./cmds'):
            if filename.endswith('.py'):
                files = (f'{filename[:-3]}')
                filename = files
                try:
                    self.bot.load_extension(f"cmds.{filename}")
                except commands.ExtensionAlreadyLoaded:
                    # print(filename + 'a')
                    await ctx.send(files + ' | ' + '已啟用')
                except commands.ExtensionNotLoaded:
                    # print(filename + 'b')
                    await ctx.send(files + ' | ' + '己關閉')
                else:
                    # print(filename + 'c')
                    self.bot.unload_extension(f"cmds.{filename}")
                    await ctx.send(files + ' | ' + '己關閉')

def setup(bot):
    bot.add_cog(cogs_commands(bot))
