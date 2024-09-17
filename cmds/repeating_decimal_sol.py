import discord
from discord.ext import commands, tasks
import json
import datetime
import asyncio
from pathlib import Path

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

class repeating_dec_sol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def repeating_dec_sol(numerator, denominator):
        negative = False
        if denominator == 0:
            return 'Undefined'
        if numerator == 0:
            return '0'
        if numerator*denominator < 0:
            negative = True
        if numerator % denominator == 0:
            return str(numerator/denominator)
        
        num = abs(numerator)
        den = abs(denominator)

        result = ""
        result += str(num // den)
        result += "."

        quotient_num = []
        while num:
            # In case the remainder is equal to zero, there are no repeating
            # decimals. Therefore, we don't need to add any parenthesis and we can
            # break the while loop and return the result.
            remainder = num % den
            if remainder == 0:
                for i in quotient_num:
                    result += str(i[-1])
                break
            num = remainder*10
            quotient = num // den

            # If the new numerator and quotient are not already in the list, we
            # append them to the list.
            if [num, quotient] not in quotient_num:
                quotient_num.append([num, quotient])
            # If the new numerator and quotient are instead already in the list, we 
            # break the execution and we prepare to return the final result.
            # We take track of the index position, in order to add the parenthesis 
            # at the output in the right place.
            elif [num, quotient] in quotient_num:
                index = quotient_num.index([num, quotient])
                for i in quotient_num[:index]:
                    result += str(i[-1])
                result += "("
                for i in quotient_num[index:]:
                    result += str(i[-1])
                result += ")"
                break
            if negative:
                if result[:1] == "-": continue#fixed in v.1.0
                result = "-" + result
        return result

def setup(bot):
    bot.add_cog(repeating_dec_sol(bot))