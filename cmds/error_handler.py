import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.custom_exception import custom_exception

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event):
        if isinstance(event, discord.DiscordException):
            print("Discord.py error")
        elif isinstance(event, discord.ClientException):
            print("Client fail")
        elif isinstance(event, discord.LoginFailure):
            print("Login fail")
        elif isinstance(event, discord.NoMoreItems):
            print("No more items")
        elif isinstance(event, discord.HTTPException):
            if isinstance(event, discord.Forbidden):
                print("HTTP status code 403 occurs")
            elif isinstance(event, discord.NotFound):
                print("HTTP status code 404 occurs")
            elif isinstance(event, discord.DiscordServerError):
                print("HTTP a 500 range status code occurs")
            else:
                print(f"HTTP request fail, response: {event.response}{f', error: {event.text}' if event.text != None else ''}, status: {event.status}, code: {event.code}")
        elif isinstance(event, discord.InvalidData):
            print("Encounters unknown or invalid data")
        elif isinstance(event, discord.InvalidArgument):
            print("Invalid argument")
        elif isinstance(event, discord.GatewayNotFound):
            print("Gateway not found")
        elif isinstance(event, discord.ConnectionClosed):
            print(f"Gateway connection is closed, code: {event.code}, reason: {event.reason}{f', shard id: {event.shard_id}' if event.shard_id != None else ''}")
        elif isinstance(event, discord.PrivilegedIntentsRequired):
            print(f"Not enabled intents{f', shard id: {event.shard_id}' if event.shard_id != None else ''}")
        elif isinstance(event, discord.opus.OpusError):
            print(f"Opus event, code: {event.code}")
        elif isinstance(event, discord.opus.OpusNotLoaded):
            print("Opus isn\'t loaded")
        print(event)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(error, "original"):
            original = getattr(error, "original")
            if isinstance(original, custom_exception.MissingRequiredArgument):
                await ctx.send(f"`EN0005`: Missing argument {original.arg}")
                return
        if isinstance(error, commands.errors.DiscordException):
            if isinstance(error, commands.errors.CommandError):
                if isinstance(error, commands.errors.ConversionError):
                    await ctx.send(f"Conversion {error.converter} Error ({error.original})")
                elif isinstance(error, commands.errors.UserInputError):
                    if isinstance(error, commands.errors.MissingRequiredArgument):
                        await ctx.send(f"Missing argument {error.param}")
                    elif isinstance(error, commands.errors.ArgumentParsingError):
                        if isinstance(error, commands.errors.UnexpectedQuoteError):
                            await ctx.send(f"Wrong usage in {error.quote}")
                        elif isinstance(error, commands.errors.InvalidEndOfQuotedStringError):
                            await ctx.send(f"Missing space after the closing quote in {error.char}")
                        elif isinstance(error, commands.errors.ExpectedClosingQuoteError):
                            await ctx.send(f"Missing the closing quote {error.close_quote}")
                        else:
                            await ctx.send("Wrong arg")
                    elif isinstance(error, commands.errors.BadArgument):
                        if isinstance(error, commands.errors.MessageNotFound):
                            await ctx.send(f"Can't found message {error.argument}")
                        elif isinstance(error, commands.errors.MemberNotFound):
                            await ctx.send(f"Can't found member {error.argument}")
                        elif isinstance(error, commands.errors.UserNotFound):
                            await ctx.send(f"Can't found user {error.argument}")
                        elif isinstance(error, commands.errors.ChannelNotFound):
                            await ctx.send(f"Can't find channel {error.argument}")
                        elif isinstance(error, commands.errors.ChannelNotReadable):
                            await ctx.send(f"Can't read channel {error.argument}")
                        elif isinstance(error, commands.errors.BadColourArgument):
                            await ctx.send(f"Invalid color {error.argument} was given")
                        elif isinstance(error, commands.errors.RoleNotFound):
                            await ctx.send(f"Can't find role {error.argument}")
                        elif isinstance(error, commands.errors.BadInviteArgument):
                            await ctx.send("Invalid invite")
                        elif isinstance(error, commands.errors.EmojiNotFound):
                            await ctx.send(f"Can't find emoji {error.argument}")
                        elif isinstance(error, commands.errors.PartialEmojiConversionFailure):
                            await ctx.send(f"Wrong emoji format {error.argument}")
                        elif isinstance(error, commands.errors.BadBoolArgument):
                            await ctx.send(f"Wrong bool argument {error.argument} was given")
                        else:
                            await ctx.send("Argument error")
                    elif isinstance(error, commands.errors.BadUnionArgument):
                        await ctx.send(f"Union error, {error.param}, {error.converters}, {error.errors}")
                    elif isinstance(error, commands.errors.TooManyArguments):
                        await ctx.send("Too many arguments")
                    else:
                        await ctx.send("Input error")
                elif isinstance(error, commands.errors.CheckFailure):
                    if isinstance(error, commands.errors.PrivateMessageOnly):
                        await ctx.send("It's private message only")
                    elif isinstance(error, commands.errors.NoPrivateMessage):
                        await ctx.send("Can't work in private message")
                    elif isinstance(error, commands.errors.CheckAnyFailure):
                        await ctx.send(f"Check_any fail, {error.errors}, c: {error.checks}")
                    elif isinstance(error, commands.errors.NotOwner):
                        await ctx.send("Is not owner")
                    elif isinstance(error, commands.errors.MissingPermissions):
                        a = ",".join(error.missing_perms)
                        await ctx.send(f"User haven't enough permission(s) ({a})")
                    elif isinstance(error, commands.errors.BotMissingPermissions):
                        a = ",".join(error.missing_perms)
                        await ctx.send(f"Bot not enough permission(s) ({a})")
                    elif isinstance(error, commands.errors.MissingRole):
                        await ctx.send(f"User missing role: {a}")
                    elif isinstance(error, commands.errors.BotMissingRole):
                        await ctx.send(f"Bot missing role: {a}")
                    elif isinstance(error, commands.errors.MissingAnyRole):
                        d = []
                        for a in error.missing_roles:
                            for b in a:
                                if type(b) == str:
                                    d.append(b)
                        await ctx.send(f"User missing either in roles: {d}")
                    elif isinstance(error, commands.errors.BotMissingAnyRole):
                        d = []
                        for a in error.missing_roles:
                            for b in a:
                                if type(b) == str:
                                    d.append(b)
                        await ctx.send(f"Bot missing either in roles: {d}")
                    elif isinstance(error, commands.errors.NSFWChannelRequired):
                        await ctx.send(f"Channel {error.channel} missing NSFW channel setting")
                    else:
                        await ctx.send("Check fail")
                elif isinstance(error, commands.errors.CommandNotFound):
                    await ctx.send("Haven't this command")
                elif isinstance(error, commands.errors.DisabledCommand):
                    await ctx.send("This command is disabled")
                elif isinstance(error, commands.errors.CommandInvokeError):
                    await ctx.send(f"Command has error, {error.original}")
                elif isinstance(error, commands.errors.CommandOnCooldown):
                    await ctx.send(f"Command is on cooldown, {error.cooldown}, wait {error.retry_after}")
                elif isinstance(error, commands.errors.MaxConcurrencyReached):
                    await ctx.send(f"In maximum concurrency, max {error.number}, per {error.per}")
                else:
                    await ctx.send("Command has error")
            elif isinstance(error, commands.errors.ExtensionError):
                if isinstance(error, commands.errors.ExtensionAlreadyLoaded):
                    await ctx.send(f"The extension {error.name} has already been loaded")
                elif isinstance(error, commands.errors.ExtensionNotLoaded):
                    await ctx.send(f"The extension {error.name} was not loaded")
                elif isinstance(error, commands.errors.NoEntryPointError):
                    await ctx.send(f"The extension {error.name} doesn't has a \"setup\" function")
                elif isinstance(error, commands.errors.ExtensionFailed):
                    await ctx.send(f"The extension {error.name} failed when loading, {error.original if error.original != None else ''}")
                elif isinstance(error, commands.errors.ExtensionNotFound):
                    await ctx.send(f"Can't found extension")
                else:
                    await ctx.send(f"Extension {error.name} had an error")
            else:
                await ctx.send("Discord error")
        elif isinstance(error, commands.errors.ClientException):
            if isinstance(error, commands.errors.CommandRegistrationError):
                await ctx.send(f"Can't add command {error.name}{', conflicts to an alias'if error.alias_conflict == True else ''}")
            else:
                await ctx.send("Client error")
        else:
            await ctx.send("Error")
        pass

def setup(bot):
    bot.add_cog(error_handler(bot))