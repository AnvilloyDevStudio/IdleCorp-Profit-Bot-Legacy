import discord
from discord.ext import commands, tasks
import json
import datetime
import asyncio
from pathlib import Path
import re

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class string_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def filter(arg, spec_digit=False):
        num = []
        string = []
        for a in arg.split(" "):
            if spec_digit == False:
                if a.isdigit():
                    num.append(int(a))
                else:
                    string.append(a)
            else:
                if a.endswith(('k', 'm', 'b')):
                    ad = a[:-1]
                    if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", ad):
                        num.append(a)
                    else:
                        string.append(a)
                elif re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", a):
                    num.append(a)
                else:
                    string.append(a)
        return [string, num]

    def location(first, second, arg, spec_digit=False):
        mark = []
        if first == str:
            mark.append("str")
        elif first == int:
            mark.append("int")
        if second == str:
            mark.append("str")
        elif second == int:
            mark.append("int")
        if mark[0]==mark[1]:
            return None
        sec = []
        for a in arg.split(" "):
            if len(sec) > 0:
                if sec[-1] == "str":
                    if spec_digit == False:
                        if not a.isdigit():
                            continue
                    else:
                        if a.endswith(('k', 'm', 'b')):
                            ad = a[:-1]
                            if not re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", ad):
                                continue
                        elif not re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", a):
                            continue
                else:
                    if spec_digit == False:
                        if a.isdigit():
                            continue
                    else:
                        if a.endswith(('k', 'm', 'b')):
                            ad = a[:-1]
                            if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", ad):
                                continue
                        else:
                            if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", a):
                                continue
            if spec_digit == False:
                if a.isdigit():
                    sec.append("int")
                else:
                    sec.append("str")
            else:
                if a.endswith(('k', 'm', 'b')):
                    ad = a[:-1]
                    if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", ad):
                        sec.append("int")
                    else:
                        sec.append("str")
                else:
                    if re.search(r"^(?:[0-9]{1,3})(?:[,][0-9]{3}){1,}(?:[.][0-9]{1,})?$|^(?:[0-9]{1,})(?:[.][0-9]{1,})?$", a):
                        sec.append("int")
                    else:
                        sec.append("str")
        if len(sec) == 1:
            for a in sec:
                return a
        if sec == mark:
            return True
        else:
            return [False, sec]

    def flags(arg):
        if type(arg) == list:
            pass
        else:
            arg = arg.split()
        flags = []
        flags_1 = []
        other = []
        for a in arg:
            if a.startswith("--"):
                flags.append(a)
            elif a.startswith("-"):
                flags_1.append(a)
            else:
                other.append(a)
        return [flags, flags_1, other]

    def numberToBase(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return digits[::-1]

def setup(bot):
    bot.add_cog(string_handler(bot))