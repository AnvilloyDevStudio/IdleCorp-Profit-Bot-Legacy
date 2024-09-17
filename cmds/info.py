import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.calculate import calculate
import random
from pathlib import Path

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
with open("aliases.json", mode="r", encoding="utf8") as f:
    als = json.load(f)
with open("icdetail.json", mode="r", encoding="utf8") as f:
    icd = json.load(f)

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=als["cogs"]["info"]["info"])
    async def info(self, ctx, *, req):
        icinfo = icd["info"]
        debug = []
        infoals = {}
        for a in als["ic"].values():
            infoals.update(a)
        for a, b in infoals.items():
            if not b == None and req in b:
                debug.append(a)
        if len(debug) > 1:
            await ctx.send("`EN0401`: Happened an unexpected or imposible thing, E1: Aliases")
            return
        elif debug:
            reqsl, = debug
        else:
            reqsl = req
        reqsl = "_".join(reqsl.split(" "))
        if reqsl.endswith("_u"): reqsl, techlv = reqsl[:-2], 1
        elif reqsl.endswith("_uu"): reqsl, techlv = reqsl[:-3], 2
        else: techlv = 0
        check = [b for a in icinfo.values() for b in a.keys()]
        if not reqsl in check:
            await ctx.send(f"`EN0004`: Cannot find info of: {req}, check your input")
            return
        for a in icinfo:
            if reqsl in icinfo[a]:
                infoclass = a
        theinfo = icinfo[infoclass][reqsl]
        embed = discord.Embed(title=f"Info -- {infoclass.capitalize()}", color=discord.Colour.greyple(), timestamp= datetime.datetime.now())
        embed.set_footer(text=self.bot.user.name+" | "+jdata["version"], icon_url=self.bot.user.avatar_url)
        embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="_ _", inline=False)
        ifimg = None
        output = []
        if infoclass == "assets":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            stuff = []
            if theinfo["market"] == True:
                stuff.append("It's tradable in market")
            elif theinfo["market"] == False:
                stuff.append("It's not tradable in market")
            if theinfo["retail"] == False:
                stuff.append("It cannot sold in retail store")
                stuff.append("It cannot be scrapped")
            else:
                stuff.append("It can sold in retail store")
                stuff.append("It can be scrapped into {} scraps".format(theinfo["retail"]))
            # output.append("\n".join(stuff))
            stuff2 = ["NPC market buy price(if valid): "+str(icd["assets"][reqsl]*2)]
            stuff2.append("NPC market sell price: "+str(icd["assets"][reqsl]))
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\n\n"+"\n".join(stuff)+"\n\n"+"\n".join(stuff2), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["assets"]:
                await ctx.send("`EN0402`: Cannot find assets -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["assets"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["assets"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if reqsl == "led": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Light-emitting_diode)")
            elif reqsl == "rubber": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/synthetic_rubber)")
            elif reqsl == "energy": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/electricity)")
            elif reqsl == "lamp": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/light_fixture)")
            elif reqsl == "ccd": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/charge-coupled_device)")
            elif reqsl == "hq": stuff.append("[Wikipedia](https://en.wikipedia.org/wiki/Headquarters)")
            elif theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            ifimg = rf"images/info/{reqsl}.png" if Path(f"images/info/{reqsl}.png").is_file() else r"images/info/box.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "facilities":
            # output.append("**IdleCorp Info(Examine):**\n"+theinfo["icinfo"])
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"], inline=False)
            stuff = []
            for a, b in theinfo["construct"].items():
                if not a == "money":
                    stuff.append(f"{b:,}"+" **"+a.capitalize()+"**")
                else:
                    stuff.append("$"+f"{b:,}")
            # output.append("**Construction materials:**\n"+"\n".join(stuff))
            embed.add_field(name="Construction materials:", value="\n".join(stuff), inline=False)
            # output.append("**IdleCorp Wiki:**\n"+theinfo["icwiki"])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            # output.append("**Wikipedia:**\n"+theinfo["wikipedia"])
            embed.add_field(name="Wikipedia:", value=theinfo["wikipedia"], inline=False)
            if reqsl in icd["facilities"]:
                stuff = "**Consumes**\n"
                facpro = icd["facilities"][reqsl]
                stuff += "None\n" if facpro["consumes"] == "None" else "\n".join([f"**{a.capitalize().replace('_', ' ')}** | {b:,}" for a, b in facpro["consumes"].items()])+"\n"
                stuff += "**Produces**\n"
                stuff += "None\n" if facpro["produces"] == "None" else "\n".join([f"**{a.capitalize().replace('_', ' ')}** | {b:,}" for a, b in facpro["produces"].items()])+"\n"
                stuff += "Speed: "+str(icd["facilities"][reqsl]["speed"])+" seconds"
                embed.add_field(name="Production:", value=stuff, inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["facilities"]:
                await ctx.send("`EN0402`: Cannot find facilities -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["facilities"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["facilities"][reqsl]))
            else: output.append("Aliases: None")
            if reqsl == "steel_mill":
                if random.randint(1, 50) == 1:
                    output.append("*I always typo this facility as \"still mill\"*")
            if reqsl == "furniture_factory":
                if random.randint(1, 5) == 1:
                    output.append("*Why the IdleCorp Wiki page has so many words...*")
                if random.randint(1, 10) == 1:
                    output.append("*Because the IdleCorp Wiki page has too many work, I had to change the layout of all...*")
            if reqsl.split("_")[-1] == "factory":
                if random.randint(1, 20) == 1:
                    output.append("*I really want to know who made this facility page...*")
            if reqsl == "research_chemical_factory":
                if random.randint(1, 3) == 1:
                    output.append("*Why this facility has so many aliases...*")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            if Path(f"images/info/{reqsl}.png").is_file(): ifimg = fr"images/info/{reqsl}.png"
            elif reqsl.endswith("mine"): ifimg = r"images/info/mine.png"
            elif reqsl in ("ccd_factory", "cpu_factory", "cell_phone_factory", "laptop_factory", "digital_camera_factory", "television_factory"): ifimg = "images/info/tech_facility.png"
            elif reqsl in ("retail_store", "research_facility", "customer_support_center", "hq"): ifimg = r"images/info/office_building.png"
            elif reqsl in ("research_chemical_factory", "prescription_drug_factory"): ifimg = r"images/info/chemical_plant.png"
            else: ifimg = r"images/info/facility.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "blueprints":
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\n\nRarity: {}".format(theinfo["rarity"])+"\n\nAll blueprints **cannot** trade and be sold in the market and the retail stores.", inline=False)
            stuff = []
            for a, b in theinfo["require"].items():
                stuff.append(f"{b:,}"+" **"+a.capitalize()+"**")
            embed.add_field(name="Requires:", value="\n".join(stuff), inline=False)
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            if theinfo.setdefault("icp"):
                embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["blueprints"]:
                await ctx.send("`EN0402`: Cannot find blueprints -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["blueprints"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["blueprints"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            output.append("\n".join(stuff))
            ifimg = r"images/info/blueprint.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "technologies":
            stuff = []
            if techlv == 2:
                if theinfo["upgrade"]["uu"] == "None":
                    await ctx.send("`EN0004`: The tech haven't \"uu\" upgrade")
                    return
                stuff.append(theinfo["upgrade"]["uu"]["icinfo"])
                stuff.append("Rarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["upgrade"]["uu"]["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
            elif techlv == 1:
                if theinfo["upgrade"]["u"] == "None":
                    await ctx.send("`EN0004`: The tech haven't \"u\" upgrade")
                    return
                stuff.append(theinfo["upgrade"]["u"]["icinfo"])
                stuff.append("Rarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["upgrade"]["u"]["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
                if theinfo["upgrade"]["uu"] != "None": stuff.append("\nNext upgrade: "+reqsl.replace("_", " ")+"uu")
            else:
                stuff.append(theinfo["icinfo"])
                stuff.append("\nRarity: "+theinfo["rarity"])
                stuff.append("It can be scrapped into {} scraps".format(theinfo["scrap"]))
                stuff.append("\nAll technologies **can** trade and **cannot** be sold in the market and the retail stores respectively.")
                if theinfo["upgrade"]["u"] != "None": stuff.append("\nNext upgrade: "+reqsl.replace("_", " ")+"u")
            stuff.append("The tech affected on "+theinfo["affect"].capitalize())
            embed.add_field(name="IdleCorp Info(Examine):", value="\n".join(stuff), inline=False)
            stuff = "\n".join(["Level {} boost: {}".format(a, theinfo["boost"][a].replace("+", "and")) for a in range(len(theinfo["boost"]))])
            embed.add_field(name="IdleCorp Wiki:", value=theinfo["icwiki"], inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["technologies"]:
                await ctx.send("`EN0402`: Cannot find blueprints -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["technologies"][reqsl+("_u" if techlv == 1 else ("_uu" if techlv == 2 else ""))] == None:
                output.append("Aliases: "+", ".join(als["ic"]["technologies"][reqsl+("_u" if techlv == 1 else ("_uu" if techlv == 2 else ""))]))
            else: output.append("Aliases: None")
            stuff = []
            stuff.append(f"\n[IdleCorp Wiki](https://wiki.idlecorp.xyz/index.php/{reqsl})")
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            output.append("\n".join(stuff))
            ifimg = r"images/info/technology.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "services":
            embed.add_field(name="IdleCorp Info(Examine):", value=theinfo["icinfo"]+"\nAffect: "+theinfo["effect"]+"\nCost: **${:,}**".format(theinfo["cost"]), inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["services"]:
                await ctx.send("`EN0402`: Cannot find services -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["services"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["services"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            if stuff: output.append("\n".join(stuff))
            ifimg = r"images/info/crane.png"
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        elif infoclass == "pollicies":
            embed.add_field(name="IdleCorp Info(Examine):", value="Affect: "+theinfo["affect"]+"\nCost: {} *Funding points*".format(theinfo["cost"]), inline=False)
            if theinfo.setdefault("icp"): embed.add_field(name="IdleCorp Profit:", value=theinfo["icp"], inline=False)
            if reqsl not in als["ic"]["services"]:
                await ctx.send("`EN0402`: Cannot find services -- {} aliases, an unexpect error".format(reqsl.replace("_", " ").capitalize()))
                return
            if not als["ic"]["policies"][reqsl] == None:
                output.append("Aliases: "+", ".join(als["ic"]["policies"][reqsl]))
            else: output.append("Aliases: None")
            stuff = []
            if theinfo["wikipedia"] != "None": stuff.append(f"[Wikipedia](https://en.wikipedia.org/wiki/{reqsl})")
            if stuff: output.append("\n".join(stuff))
            embed.add_field(name="_ _", value="\n\n".join(output), inline=False)
        # embed.add_field(name=reqsl.replace("_", " ").capitalize(), value="\n\n".join(output))
        if ifimg == None: await ctx.send(embed=embed)
        else:
            ifimg = discord.File(ifimg)
            embed.set_thumbnail(url=r"attachment://"+ifimg.filename)
            await ctx.send(embed=embed, file=ifimg)

def setup(bot):
    bot.add_cog(info(bot))