import discord
from discord import embeds
from discord.ext import commands, tasks
import json
import datetime
import asyncio
from pathlib import Path
import bitdotio

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

db = bitdotio.bitdotio("83JQ_sPGfbNhEz7Hs4Gwzk4yqQXf")

class status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks_status.start()
        self.suggestions_status.start()

    @tasks.loop(seconds=20)
    async def tasks_status(self):
        await self.bot.wait_until_ready()
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT datetime FROM \"BenChueng0422/IdleCorp-Profit\".\"check_update log\" WHERE tables = \'tasks\'")
            datacheck = cursor.fetchone()[0]
            # execute SQL query using execute() method.
            cursor.execute("SELECT * from \"BenChueng0422/IdleCorp-Profit\".\"tasks\"")
            # Get the fields name (only once!)
            # field_name = [field[0] for field in cursor.description]
            # Fetch a single row using fetchone() method.
            values = cursor.fetchall()
        # create the row dictionary to be able to call row['login']
        date = values[-1][-1]
        if date == datacheck:
            return
        rows = dict(values[:-1])
        # bd.partial_update_column("BenChueng0422", "IdleCorp-Profit", "tasks", "")
        # print(bd.list_columns("BenChueng0422", "IdleCorp-Profit", "tasks"))
        # print(bd.retrieve_column("BenChueng0422", "IdleCorp-Profit", "tasks", "on_work"))
        # guild = self.bot.get_guild(jdata["guild_id"])
        channel = self.bot.get_channel(801052238377648138)
        message = await channel.fetch_message(802863649709752340)
        # datafile = Path("data.json")
        # if datafile.is_file():
        #     with open("data.json", mode="r", encoding="utf8") as jf:
        #         dt = json.load(jf)
        #     embed = discord.Embed(title="Tasks")
        #     try:
        #         dt.get("tasks")
        #         try:
        #             dt["tasks"].get("on_work")
        #             count = 0
        #             mark = 0
        #             for a, b in dt["tasks"].items():
        #                 count += 1
        #                 if not dt["tasks"][a] == []:
        #                     pass
        #                 else:
        #                     mark += 1
        #             if mark == count:
        #                 raise
        #         except:
        #             raise
        #         tasks = {}
        #         for a, b in dt["tasks"].items():
        #             if not dt["tasks"][a] == []:
        #                 for b in dt["tasks"][a]:
        #                     tasks[b] = a
        #         works = {}
        #         for a, b in tasks.items():
        #             works.setdefault(b, []).append(a)
        #         for a, b in works.items():
        #             dd = "\n".join(b)
        #             embed.add_field(name=a, value=dd, inline=False)
        #     except:
        #         embed.add_field(name="None", value="None", inline=False)
        embed = discord.Embed(title="Tasks")
        for a, b in rows.items():
            if b and len("\n".join(b)):
                embed.add_field(name=a, value="\n".join(b), inline=False)
        with db.get_connection().cursor() as cursor:
            cursor.execute("UPDATE \"BenChueng0422/IdleCorp-Profit\".\"check_update log\" SET datetime = \'{}\' WHERE tables = \'tasks\'".format(date))
        await message.edit(content=None, embed=embed)


    @tasks.loop(seconds=10)
    async def suggestions_status(self):
        await self.bot.wait_until_ready()
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT datetime FROM \"BenChueng0422/IdleCorp-Profit\".\"check_update log\" WHERE tables = \'suggestions\'")
            date = cursor.fetchone()[0]
            cursor.execute("SELECT datetime FROM \"BenChueng0422/IdleCorp-Profit\".\"last_update log\" WHERE tables = \'suggestions\'")
            datacheck = cursor.fetchone()[0]
            cursor.execute("SELECT * from \"BenChueng0422/IdleCorp-Profit\".\"suggestions\"")
            values = cursor.fetchall()
        if date == datacheck:
            return
        value = sorted([dict(zip([a[0] for a in cursor.description], a)) for a in values], key=lambda k: len(k["votes"]), reverse=True)
        channel = self.bot.get_channel(856913820978642964)
        message = await channel.fetch_message(856914255064203274)
        embed = discord.Embed(title="Suggestions")
        res = [[]]
        ind = 0
        for a in value:
            if len("\n".join(res[ind]+["{}  [{}] Votes: **{}** -- by: <@!{}>".format(a["suggestion_id"], a["status"].capitalize().replace("_", " "), len(a["votes"]), a["user_id"])]))>1000:
                ind += 1
                res.append([])
                if ind>5: break
            res[ind].append("{}  [{}] Votes: **{}** -- by: <@!{}>".format(a["suggestion_id"], a["status"].capitalize().replace("_", " "), len(a["votes"]), a["user_id"]))
        for a in res:
            embed.add_field(name="_ _", value="\n".join(a), inline=False)
        with db.get_connection().cursor() as cursor:
            cursor.execute("UPDATE \"BenChueng0422/IdleCorp-Profit\".\"check_update log\" SET datetime = \'{}\' WHERE tables = \'suggestions\'".format(date))
        await message.edit(content=None, embed=embed)

def setup(bot):
    bot.add_cog(status(bot))