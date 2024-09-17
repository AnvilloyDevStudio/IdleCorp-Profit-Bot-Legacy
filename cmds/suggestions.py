import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.calculate import calculate
import re
import decimal, math, numexpr, random
import bitdotio

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

db = bitdotio.bitdotio("6cCg_cknNfbKVqNk84Q2JeV8vVXL")

class suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=als["cogs"]["suggestions"]["suggest"][0])
    async def suggest(self, ctx):
        command = ctx.message.content.split(" ")
        if len(command) == 1:
            await ctx.send("Commands:\n`suggest add`\n`suggest edit`\n`suggest vote`\n`suggest info`"+("\n`suggest change`\n`suggest remove`" if [a for a in ctx.author.roles if a.name in ("Owner", "ICP Developer")] else ""))
        else:
            await ctx.send("Wrong subcommand")

    @suggest.command(aliases=als["cogs"]["suggestions"]["suggest"][1]["add"])
    async def add(self, ctx, *, suggest):
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT suggestion_id FROM \"BenChueng0422/IdleCorp-Profit\".\"suggestions\"")
            check = [a[0] for a in cursor.fetchall()]
            n_unique = True
            while n_unique:
                suggest_id = random.randint(1, 9999999)
                if suggest_id not in check: n_unique = False
            cursor.execute("INSERT INTO \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" (suggestions, user_id, suggestion_id) VALUES (\'{}\', {}, {}); UPDATE \"BenChueng0422/IdleCorp-Profit\".\"last_update log\" SET datetime = \'{}\' WHERE tables = \'suggestions\'".format(suggest, ctx.author.id, suggest_id, datetime.datetime.now()))
        await ctx.send("Added suggestion \"{}\"".format(suggest))

    @suggest.command(aliases=als["cogs"]["suggestions"]["suggest"][1]["edit"])
    async def edit(self, ctx, suggest_id: int, *, new_suggest):
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT suggestion_id, user_id FROM \"BenChueng0422/IdleCorp-Profit\".\"suggestions\"")
            check = dict(cursor.fetchall())
            if suggest_id not in check:
                await ctx.send("`EN0006`: The suggestion id was invalid.")
                return
            if ctx.author.id != check[suggest_id] or not [a for a in ctx.author.roles if a.name in ("Owner", "ICP Developer")]:
                await ctx.send("`EN0006`: You were not the creator of the suggestion.")
                return
            cursor.execute("UPDATE \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" SET suggestions = \'{}\' WHERE suggestion_id = {}; UPDATE \"BenChueng0422/IdleCorp-Profit\".\"last_update log\" SET datetime = \'{}\' WHERE tables = \'suggestions\'".format(new_suggest, suggest_id, datetime.datetime.now()))
        await ctx.send("Edited the suggestion `{}` to \"{}\"".format(suggest_id, new_suggest))

    @suggest.command(aliases=als["cogs"]["suggestions"]["suggest"][1]["vote"])
    async def vote(self, ctx, suggest_id:int):
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT votes FROM \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" WHERE suggestion_id = {}".format(suggest_id))
            value = cursor.fetchall()
            if not value:
                await ctx.send("`EN0006`: The suggestion id was invalid.")
                return
            if ctx.author.id in value[0][0]:
                await ctx.send("`EN0004`: You already voted the suggestion.")
                return
            value[0][0].append(ctx.author.id)
            cursor.execute("UPDATE \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" SET votes = \'{}\'::JSON WHERE suggestion_id = {}; UPDATE \"BenChueng0422/IdleCorp-Profit\".\"last_update log\" SET datetime = \'{}\' WHERE tables = \'suggestions\'".format(value[0][0], suggest_id, datetime.datetime.now()))
        await ctx.send("You has voted the suggestion `{}`".format(suggest_id))

    @suggest.command(aliases=als["cogs"]["suggestions"]["suggest"][1]["info"])
    async def info(self, ctx, suggest_id:int):
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" WHERE suggestion_id = {}".format(suggest_id))
            if not cursor:
                await ctx.send("`EN0006`: The suggestion id was invalid.")
                return
            value = dict(zip([a[0] for a in cursor.description], cursor.fetchall()[0]))
        embed = discord.Embed(title="Suggestion info", color=discord.Colour.from_rgb(255, 255, 190), description="**{}**".format(len(value["votes"])), timestamp=datetime.datetime.now())
        embed.set_author(name=str(self.bot.get_user(value["user_id"])), icon_url=self.bot.get_user(value["user_id"]).avatar_url)
        embed.add_field(name="{} \t\t\t [{}]".format(value["suggestion_id"], value["status"].capitalize().replace("_", " ")), value="{}\n\nSuggestion creator: <@!{}>\nCreated at: {} {}:{} (UTC)".format(value["suggestions"], value["user_id"], value["date"].date(), value["date"].hour, value["date"].minute))
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @suggest.command(aliases=als["cogs"]["suggestions"]["suggest"][1]["change"])
    @commands.has_any_role(801052590389329930, 801052697498746920)
    async def change(self, ctx, suggest_id, status):
        alias = {"ir": "in_review", "i": "in_review", "v": "verified", "p": "pass", "np": "not_pass", "n": "not_pass", "d": "done"}
        if status in alias: status = alias[status]
        if status not in ("in_review", "verified", "pass", "not_pass", "done"):
            await ctx.send("`EN0004`: The status was invalid.")
            return
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT status FROM \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" WHERE suggestion_id = {}".format(suggest_id))
            if not cursor:
                await ctx.send("`EN0006`: The suggestion id was invalid.")
                return
            if status == cursor.fetchone()[0]:
                await ctx.send("`EN0004`: The status of the suggestion was already `{}`".format(status))
                return
            cursor.execute("UPDATE \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" SET status = \'{}\' WHERE suggestion_id = {}; UPDATE \"BenChueng0422/IdleCorp-Profit\".\"last_update log\" SET datetime = \'{}\' WHERE tables = \'suggestions\'".format(status, suggest_id, datetime.datetime.now()))
        await ctx.send("Changed the suggestion into `{}`".format(status))

    @suggest.command(aliases=als["cogs"]["suggestions"]["suggest"][1]["remove"])
    @commands.has_any_role(801052590389329930, 801052697498746920)
    async def remove(self, ctx, suggest_id):
        with db.get_connection().cursor() as cursor:
            cursor.execute("SELECT user_id FROM \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" WHERE suggestion_id = {}".format(suggest_id))
            if not cursor:
                await ctx.send("`EN0006`: The suggestion id was invalid.")
                return
            cursor.execute("DELETE FROM \"BenChueng0422/IdleCorp-Profit\".\"suggestions\" WHERE suggestion_id = {}".format(suggest_id))
        await ctx.send("Deleted the suggestion `{}`".format(suggest_id))

def setup(bot):
    bot.add_cog(suggestions(bot))