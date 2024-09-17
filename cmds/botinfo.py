import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.repeating_decimal_sol import repeating_dec_sol
from cmds.function_handler import function_handler
import decimal

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

class botinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["botinfo"]["botinfo"])
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot info", color=discord.Colour.dark_blue(), timestamp= datetime.datetime.now())
        embed.add_field(name="Bot Information", value="This bot is used to help players in IdleCorp can easier.```md\n<Language: Python>\n<Library: discord.py>\n<Version: v.{}>```".format(jdata["version"]), inline=False)
        embed.add_field(name="Server Information", value="Any bugs or typos can be reported in <#828810972902457415> or DM/PM the Developer/Owner.\nAny suggections can send in <#801067404759007292>.\nThe wiki can see in <#820210762123051089>.\nAny questions or want to get help about IdleCorp or IdleCorp Profit, can send in <#801067628802080798> or DM\PM the Owner.", inline=False)
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(botinfo(bot))