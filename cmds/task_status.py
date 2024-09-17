import re
import discord
from discord.ext import commands
import json
import datetime
import asyncio
import bitdotio

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

db = bitdotio.bitdotio("83JQ_sPGfbNhEz7Hs4Gwzk4yqQXf")

class tasks_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=als["cogs"]["task_status"]["task"][0])
    @commands.has_any_role(801052590389329930, 801052697498746920)
    async def task(self, ctx):
        command = ctx.message.content.split(" ")
        if len(command) == 1:
            await ctx.send("Commands:\n`task add`\n`task change`\n`task remove`\nParameters: on_work, pause, finished, waiting")
        else:
            await ctx.send("Wrong subcommand")

    def task_aliases(_dict, mark):
        out = []
        mark = mark.lower()
        for a, b in _dict.items():
            ind = 0
            for b in b:
                if mark == b.lower():
                    return (a, ind)
                if mark in b.lower():
                    out.append((a, ind))
                ind += 1
        if len(out)>1:
            return (False, len(out))
        return out[0]

    @task.command(aliases=als["cogs"]["task_status"]["task"][1]["add"])
    async def add(self, ctx, *, args):
        arg = [a.strip() for a in args.split("|")]
        check = {"o": "on_work", "p": "paused", "f": "finished", "w": "waiting"}
        if arg[-1] in check: arg = arg[:-1]+[check[arg[-1]]]
        _type = "on_work" if arg[-1] not in ("on_work", "paused", "finished", "waiting") else arg[-1]
        print(arg)
        task = " ".join(arg[:-1] if arg[-1] in ("on_work", "paused", "finished", "waiting") else arg)
        print(task)
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM \"BenChueng0422/IdleCorp-Profit\".\"tasks\" WHERE type != \'last_time\'")
            fetch = dict(cursor.fetchall())
            if task in sum(list(fetch.values()), start=[]):
                await ctx.send("`ED1001`: The task you sent was exixt in the list.")
                return
            cursor.execute("UPDATE \"BenChueng0422/IdleCorp-Profit\".\"tasks\" AS t SET value = c.value FROM (VALUES (\'{}\', \'{}\'::JSON), (\'last_time\', \'\"{}\"\'::JSON)) AS c(type, value) WHERE c.type = t.type".format(_type, json.dumps(fetch[_type]+[task]), datetime.datetime.now()))
        await ctx.send(f"Added `{task}` into the tasks stats.")

    @task.command(aliases=als["cogs"]["task_status"]["task"][1]["change"])
    async def change(self, ctx, *, args):
        arg = [a.strip() for a in args.split("|")]
        check = {"o": "on_work", "p": "paused", "f": "finished", "w": "waiting"}
        if arg[-1] in check: arg = arg[:-1]+[check[arg[-1]]]
        _type = "on_work" if arg[-1] not in ("on_work", "paused", "finished", "waiting") else arg[-1]
        task = " ".join(arg[:-1]) if arg[-1] in ("on_work", "paused", "finished", "waiting") else " ".join(arg)
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM \"BenChueng0422/IdleCorp-Profit\".\"tasks\"")
            value = dict(cursor.fetchall())
            res = tasks_status.task_aliases(value, task)
            if not res[0]:
                if res[1] == 0:
                    await ctx.send("`EN0004`: Invalid task, haven't any task was matched.")
                else:
                    await ctx.send("`EN0004`: Invalid task, more than one tasks were matched.")
                return
            # s = []
            # for a, b in value.items():
            #     for c in b:
            #         if task in c:
            #             s.append(a)
            # if len(s) > 1:
            #     await ctx.send("`EN0004`: More than one tasks were matched.")
            #     return
            # if _type in s:
            if _type == res[0]:
                await ctx.send("`EN0004`: The task were matched in same status.")
                return
            task = value[res[0]][res[1]]
            value[res[0]].pop(res[1])
            value[_type].append(task)
            cursor.execute("UPDATE \"BenChueng0422/IdleCorp-Profit\".\"tasks\" AS t SET value = c.value FROM (VALUES (\'{}\', \'{}\'::JSON), (\'{}\', \'{}\'::JSON), (\'last_time\', \'\"{}\"\'::JSON)) AS c(type, value) WHERE c.type = t.type".format(res[0], json.dumps(value[res[0]]), _type, json.dumps(value[_type]), str(datetime.datetime.now())))
        await ctx.send(f"Changed `{task}` to {_type}")

    @task.command(aliases=als["cogs"]["task_status"]["task"][1]["remove"])
    async def remove(self, ctx, *, task):
        task = task.strip()
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM \"BenChueng0422/IdleCorp-Profit\".\"tasks\"")
            value = dict(cursor.fetchall())
            res = tasks_status.task_aliases(value, task)
            if not res[0]:
                if res[1] == 0:
                    await ctx.send("`EN0004`: Invalid task, haven't any task was matched.")
                else:
                    await ctx.send("`EN0004`: Invalid task, more than one tasks were matched.")
                return
            task = value[res[0]][res[1]]
            value[res[0]].pop(res[1])
            cursor.execute("UPDATE \"BenChueng0422/IdleCorp-Profit\".\"tasks\" AS t SET value = c.value FROM (VALUES (\'{}\', \'{}\'::JSON), (\'last_time\', \'\"{}\"\'::JSON)) AS c(type, value) WHERE c.type = t.type".format(res[0], json.dumps(value[res[0]]), str(datetime.datetime.now())))
            await ctx.send(f"The task `{task}` has removed sucessfully.")

def setup(bot):
    bot.add_cog(tasks_status(bot))