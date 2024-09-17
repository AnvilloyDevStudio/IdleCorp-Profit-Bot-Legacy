import discord
from discord.ext import commands
import json
import datetime
import asyncio

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)

class main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["main"]["send"])
    async def send(self, ctx, channel:discord.TextChannel):
        await channel.send("This is Message")

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if self.bot.user in message.mentions:
    #         await message.channel.send(f"The bot prefix is: `{self.bot.command_prefix}`")

def setup(bot):
    bot.add_cog(main(bot))