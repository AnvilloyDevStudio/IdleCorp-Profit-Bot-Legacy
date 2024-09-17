import discord
from discord.ext import commands
import json
import datetime
import asyncio
from cmds.repeating_decimal_sol import repeating_dec_sol
from cmds.function_handler import function_handler
import decimal, fractions
import re

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

with open("icdetail.json", mode="r", encoding="utf8") as f:
    icd = json.load(f)

class calculate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def product_speed(facility, types, num=1):
        fac = icd["facilities"][facility]
        if not types in ("consumes", "produces", "all"):
            return
        if types == "all":
            tya = fac["consumes"]
            tyb = fac["produces"]
        else:
            ty = fac[types]
            if ty == "None":
                return None
        speed = fac["speed"]
        con_spee = {}
        pro_spee = {}
        if types == "consumes":
            if type(speed) == list:
                for e in speed:
                    for a, b in ty.items():
                        c = b*int(num)
                        con_spe = repeating_dec_sol.repeating_dec_sol(c, e)
                        con_spee[a] = con_spe
                return con_spee
            for a, b in ty.items():
                c = b*int(num)
                con_spe = repeating_dec_sol.repeating_dec_sol(c, speed)
                con_spee[a] = con_spe
            return con_spee
        elif types == "produces":
            if type(speed) == list:
                for e in speed:
                    for a, b in ty.items():
                        c = b*int(num)
                        pro_spe = repeating_dec_sol.repeating_dec_sol(c, e)
                        pro_spee[a] = pro_spe
                return pro_spee
            for a, b in ty.items():
                c = b*int(num)
                pro_spe = repeating_dec_sol.repeating_dec_sol(c, speed)
                pro_spee[a] = pro_spe
            return pro_spee
        elif types == "all":
            if not tya == "None":
                if type(speed) == list:
                    i = 0
                    for e in speed:
                        for a, b in tya.items():
                            c = b*int(num)
                            con_spe = repeating_dec_sol.repeating_dec_sol(c, e)
                            if i == 0:
                                con_spee[a+f"_Max({e})"] = con_spe
                            elif i == 1:
                                con_spee[a+f"_Min({e})"] = con_spe
                        i += 1
                else:
                    for a, b in tya.items():
                        c = b*int(num)
                        con_spe = repeating_dec_sol.repeating_dec_sol(c, speed)
                        con_spee[a] = con_spe
            else:
                con_spee = "None"
            if not tyb == "None":
                if type(speed) == list:
                    i = 0
                    for e in speed:
                        for a, b in tyb.items():
                            c = b*int(num)
                            pro_spe = repeating_dec_sol.repeating_dec_sol(c, e)
                            if i == 0:
                                pro_spee[a+f"_Max({e})"] = pro_spe
                            elif i == 1:
                                pro_spee[a+f"_Min({e})"] = pro_spe
                        i += 1
                else:
                    for a, b in tyb.items():
                        c = b*int(num)
                        pro_spe = repeating_dec_sol.repeating_dec_sol(c, speed)
                        pro_spee[a] = pro_spe
            else:
                pro_spee = "None"
            return [con_spee, pro_spee]

    def product_profit(facility, types, num=1):
        fac = icd["facilities"][facility]
        if not types in ("consumes", "produces", "all"):
            return
        if types == "all":
            tya = fac["consumes"]
            tyb = fac["produces"]
        else:
            ty = fac[types]
            if ty == "None":
                return None
        speed = fac["speed"]
        con_pfr = {}
        pro_pfr = {}
        if types == "consumes":
            for a, b in ty.items():
                money = icd["assets"][a]
                c = b*int(num)*money
                con_pf = repeating_dec_sol.repeating_dec_sol(c*2, speed)
                con_pfr[a] = con_pf
            return con_pfr
        elif types == "produces":
            for a, b in ty.items():
                money = icd["assets"][a]
                c = b*int(num)*money
                pro_pf = repeating_dec_sol.repeating_dec_sol(c, speed)
                pro_pfr[a] = pro_pf
            return pro_pfr
        elif types == "all":
            if not tya == "None":
                for a, b in tya.items():
                    if type(speed) == list:
                        speed = fac["speed"]
                        count = 0
                        for d in speed:
                            if a == "money":
                                money = 1
                            else:
                                money = icd["assets"][a]
                            c = b*int(num)*money
                            if c == int(c):
                                c = int(c)
                            else:
                                while c != int(c):
                                    c *= 10
                                    d *= 10
                                c = int(c)
                            con_pf = repeating_dec_sol.repeating_dec_sol(c*2, d)
                            con_pfr[a+(("_Min("+str(d)+")") if count == 1 else ("_Max("+str(d)+")"))] = con_pf
                            count = 1
                    else:
                        if a == "money":
                            money = 1
                        else:
                            money = icd["assets"][a]
                        c = b*int(num)*money
                        if c == int(c):
                            c = int(c)
                        else:
                            while c != int(c):
                                c *= 10
                                speed *= 10
                            c = int(c)
                        con_pf = repeating_dec_sol.repeating_dec_sol(c*2, speed)
                        con_pfr[a] = con_pf
            else:
                con_pfr = "None"
            if not tyb == "None":
                for a, b in tyb.items():
                    speed = fac["speed"]
                    if type(speed) == list:
                        count = 0
                        for d in speed:
                            if a == "money":
                                money = 1
                            else:
                                money = icd["assets"][a]
                            c = b*int(num)*money
                            if c == int(c):
                                c = int(c)
                            else:
                                while c != int(c):
                                    c *= 10
                                    d *= 10
                                c = int(c)
                            pro_pf = repeating_dec_sol.repeating_dec_sol(c, d)
                            pro_pfr[a+(("_Min("+str(d)+")") if count == 1 else ("_Max("+str(d)+")"))] = pro_pf
                            count = 1
                    else:
                        speed = fac["speed"]
                        if a == "money":
                            money = 1
                        else:
                            money = icd["assets"][a]
                        c = b*int(num)*money
                        if c == int(c):
                            c = int(c)
                        else:
                            while c != int(c):
                                c *= 10
                                speed *= 10
                            c = int(c)
                        pro_pf = repeating_dec_sol.repeating_dec_sol(c, speed)
                        pro_pfr[a] = pro_pf
            else:
                pro_pfr = "None"
            if con_pfr == "None":
                if len(list(pro_pfr.values())) == 1:
                    for a in list(pro_pfr.values()):
                        pfs = a 
            else:
                speed = fac["speed"]
                assets = icd["assets"]
                if type(speed) == list:
                    i = 0
                    pfss = []
                    for r in speed:
                        for a, b in tyb.items():
                            if a == "money":
                                pdm = 1
                            else:
                                pdm = assets[a]
                            pdttm = b*pdm*int(num)
                        csttm = []
                        for a, b in tya.items():
                            csm = assets[a]
                            csttm.append(csm*b*int(num))
                        cstm = 0
                        for a in csttm:
                            cstm += a
                        pfbf = float(decimal.Decimal(str(pdttm))-decimal.Decimal(str(cstm*2)))
                        if pfbf == int(pfbf):
                            pfbf = int(pfbf)
                        else:
                            while pfbf != int(pfbf):
                                pfbf *= 10
                                r *= 10
                            pfbf = int(pfbf)
                        pfs = repeating_dec_sol.repeating_dec_sol(pfbf, r)
                        if i == 1:
                            pfss.append({"Min": pfs})
                        else:
                            pfss.append({"Max": pfs})
                        i += 1
                    return [con_pfr, pro_pfr, pfss]
                for a, b in tyb.items():
                    if a == "money":
                        pdm = 1
                    else:
                        pdm = assets[a]
                    pdttm = b*pdm*int(num)
                csttm = []
                for a, b in tya.items():
                    csm = assets[a]
                    csttm.append(csm*b*int(num))
                cstm = 0
                for a in csttm:
                    cstm += a
                pfbf = float(decimal.Decimal(str(pdttm))-decimal.Decimal(str(cstm*2)))
                if pfbf == int(pfbf):
                    pfbf = int(pfbf)
                else:
                    while pfbf != int(pfbf):
                        pfbf *= 10
                        speed *= 10
                    pfbf = int(pfbf)
                pfs = repeating_dec_sol.repeating_dec_sol(pfbf, speed)
            return [con_pfr, pro_pfr, pfs]

    def fraction_diff(a_a, a_b, b_a, b_b):
        args = [a_a, a_b, b_a, b_b]
        for a in args:
            if type(a) == int:
                pass
            elif type(a) == float:
                if a == int(a):
                    a = int(a)
                else:
                    print(f"ERROR \"{a}\"")
            elif type(a) == str:
                a = float(a)
                if a == int(a):
                    a = int(a)
                else:
                    print(f"ERROR \"{a}\"")
        stuff = a_b
        a_a *= b_b; a_b *= b_b
        b_a *= stuff; b_b *= stuff
        a_set = a_a-b_a
        if a_b == b_b:
            pass
        else:
            print("ERROR b_set")
        return [a_set, a_b]

    def facratio(fac, num=1):
        faclist = icd["facilities"]
        faccs = faclist[fac]["consumes"]
        facspeed = faclist[fac]["speed"]
        if faccs == "None":
            return [f"0:{num}", f"(0:{num}, 0:{num})", [("N/A", 0)]]
        facpd = []
        for a in faccs:
            for b in faclist:
                for c in faclist[b]["produces"].keys():
                    if c == a:
                        facpd.append((b, c))
        stuff = [b for a, b in facpd]
        rep = []
        for a in range(len(stuff)):
            for b in stuff:
                if stuff.count(b) > 1:
                    rep.append(b)
        energy = 0
        if "energy" in rep:
            energy = 1
        if energy:
            facpd.pop(0)
            facpd = [("solar_power_plant" if a == "coal_power_plant" else a, b) for a, b in facpd]
        stuff1 = []
        depfrac1 = []
        depfrac2 = []
        firstfacdt = []
        if type(faclist[fac]["speed"]) == list:
            for s in faclist[fac]["speed"]:
                for f, g in facpd:
                    ty = "_Max({})".format(s) if faclist[fac]["speed"].index(s) else "_Min({})".format(s)
                    # a = fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
                    b = fractions.Fraction(faccs[g], s)*num
                    count = 0
                    while b > 0:
                        b-=fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
                        count += 1
                    firstfacdt.append((f+ty, count))
                    stuff1.append(str(count)+ty)
                    frac1 = b/fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
                    afrac = [b, fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])]
                    if afrac.index(min(afrac)):
                        afrac = (max(afrac)/min(afrac), 1)
                    else:
                        afrac = (1, max(afrac)/min(afrac))
                    depfrac1.append((":".join((str(int(float(f))) if float(f).is_integer() else f) if re.fullmatch(r"[0-9]+[.][0-9]+", f) else f for f in [repeating_dec_sol.repeating_dec_sol(a.numerator, a.denominator) for a in calculate.simratio(afrac)]))+ty)
                    bfrac = []
                    for a in afrac:
                        if type(a) == fractions.Fraction:
                            b = repeating_dec_sol.repeating_dec_sol(a.numerator, a.denominator)
                            bfrac.append((str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b)
                        else: bfrac.append(str(a))
                    depfrac2.append(":".join(bfrac)+ty)
        else:
            for f, g in facpd:
                # a = fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
                b = fractions.Fraction(faccs[g], faclist[fac]["speed"])*num
                count = 0
                while b > 0:
                    b-=fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
                    count += 1
                firstfacdt.append((f, count))
                stuff1.append(str(count))
                frac1 = fractions.Fraction(faccs[g], facspeed)/fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])
                afrac = [fractions.Fraction(faccs[g], faclist[fac]["speed"]), fractions.Fraction(faclist[f]["produces"][g], faclist[f]["speed"])]
                if afrac.index(min(afrac)):
                    afrac = (max(afrac)/min(afrac), 1)
                else:
                    afrac = (1, max(afrac)/min(afrac))
                depfrac1.append(":".join((str(int(float(f))) if float(f).is_integer() else f) if re.fullmatch(r"[0-9]+[.][0-9]+", f) else f for f in [repeating_dec_sol.repeating_dec_sol(a.numerator, a.denominator) for a in calculate.simratio(afrac)]))
                bfrac = []
                for a in afrac:
                    if type(a) == fractions.Fraction:
                        b = repeating_dec_sol.repeating_dec_sol(a.numerator, a.denominator)
                        bfrac.append((str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b)
                    else: bfrac.append(str(a))
                depfrac2.append(":".join(bfrac))
        # a = True
        # b = [decimal.Decimal(str(1.2337)), decimal.Decimal(str(1.22)), decimal.Decimal(str(7.177))]
        # re = b
        # while a:
        #     bfr = []
        #     stuff = []
        #     for c in re:
        #         c*=10
        #         bfr.append(c)
        #         stuff.append(True if int(c)!=float(c) else False)
        #     if True in stuff: a = True
        #     if list(set(stuff)) == [False]: a = False
        #     re = bfr
        # for a, b in facpd:
        #     a, = faclist[f]["produces"].values()
        #     b = fractions.Fraction(faccs[g], facspeed)
        # intrat = calculate.simratio([fractions.Fraction(faclist[a]["produces"][b], faclist[a]["speed"]) for a, b in facpd]+[fractions.Fraction(faccs[], 1)])
        # print(intrat) # ":".join([repeating_dec_sol.repeating_dec_sol(a.numerator, a.denominator) for a in intrat])+":1", 
        return (":".join(stuff1)+":1", ", ".join([f"({a}, {b})" for a, b in zip(depfrac1, depfrac2)]), firstfacdt)

    def simratio(nums):
        re = []
        hcf = nums[0].numerator
        lcm = nums[0].denominator
        for a in nums:
            nu, de = a.numerator, a.denominator
            lcm = (de*lcm)/(calculate.gcd(de, lcm))
            hcf = calculate.gcd(nu, hcf)
        frac = fractions.Fraction(int(hcf), int(lcm))
        return [n / frac for n in nums]

    def gcd(*nums):#greatest common denominator
        if len(nums) > 2:
            c = gcd(*nums[1::])
            return gcd(nums[0], c)
        a, b = nums
        while b != 0:
            a, b = b, a % b
        return a

    def firstfac(fac, facdt, sp=False):
        if not sp: ff = "\n".join([f"**{a.capitalize().replace('_', ' ')}** | {b}" for a, b in facdt])
        else: ff = "\n".join([f"{a.capitalize().replace('_', ' ')} | {b}" for a, b in facdt])
        lds = "Land "+str(1+sum([b for a, b in facdt]))
        return [ff, lds, 1+sum([b for a, b in facdt])]

    def product_profitpland(facility, types, num=1, land=1):
        fac = icd["facilities"][facility]
        if not types in ("consumes", "produces", "all"):
            return
        if types == "all":
            tya = fac["consumes"]
            tyb = fac["produces"]
        else:
            ty = fac[types]
            if ty == "None":
                return None
        speed = fac["speed"]
        con_pfr = {}
        pro_pfr = {}
        if types == "consumes":
            for a, b in ty.items():
                money = icd["assets"][a]
                c = b*int(num)*money
                con_pf = repeating_dec_sol.repeating_dec_sol(c*2, speed)
                con_pfr[a] = con_pf
            return con_pfr
        elif types == "produces":
            for a, b in ty.items():
                money = icd["assets"][a]
                c = b*int(num)*money
                pro_pf = repeating_dec_sol.repeating_dec_sol(c, speed*land)
                pro_pfr[a] = pro_pf
            return pro_pfr
        elif types == "all":
            if not tya == "None":
                for a, b in tya.items():
                    if type(speed) == list:
                        speed = fac["speed"]
                        count = 0
                        for d in speed:
                            if a == "money":
                                money = 1
                            else:
                                money = icd["assets"][a]
                            c = b*int(num)*money
                            if c == int(c):
                                c = int(c)
                            else:
                                while c != int(c):
                                    c *= 10
                                    d *= 10
                                c = int(c)
                            con_pf = repeating_dec_sol.repeating_dec_sol(c*2, d)
                            con_pfr[a+(("_Min("+str(d)+")") if count == 1 else ("_Max("+str(d)+")"))] = con_pf
                            count = 1
                    else:
                        if a == "money":
                            money = 1
                        else:
                            money = icd["assets"][a]
                        c = b*int(num)*money
                        if c == int(c):
                            c = int(c)
                        else:
                            while c != int(c):
                                c *= 10
                                speed *= 10
                            c = int(c)
                        con_pf = repeating_dec_sol.repeating_dec_sol(c*2, speed)
                        con_pfr[a] = con_pf
            else:
                con_pfr = "None"
            if not tyb == "None":
                for a, b in tyb.items():
                    speed = fac["speed"]
                    if type(speed) == list:
                        count = 0
                        for d in speed:
                            if a == "money":
                                money = 1
                            else:
                                money = icd["assets"][a]
                            c = b*int(num)*money
                            if c == int(c):
                                c = int(c)
                            else:
                                while c != int(c):
                                    c *= 10
                                    d *= 10
                                c = int(c)
                            pro_pf = repeating_dec_sol.repeating_dec_sol(c, d*land)
                            pro_pfr[a+(("_Min("+str(d)+")") if count == 1 else ("_Max("+str(d)+")"))] = pro_pf
                            count = 1
                    else:
                        speed = fac["speed"]
                        if a == "money":
                            money = 1
                        else:
                            money = icd["assets"][a]
                        c = b*int(num)*money
                        if c == int(c):
                            c = int(c)
                        else:
                            while c != int(c):
                                c *= 10
                                speed *= 10
                            c = int(c)
                        pro_pf = repeating_dec_sol.repeating_dec_sol(c, speed*land)
                        pro_pfr[a] = pro_pf
            else:
                pro_pfr = "None"
            if con_pfr == "None":
                if len(list(pro_pfr.values())) == 1:
                    for a in list(pro_pfr.values()):
                        pfs = a 
            else:
                speed = fac["speed"]
                assets = icd["assets"]
                if type(speed) == list:
                    i = 0
                    pfss = []
                    for r in speed:
                        for a, b in tyb.items():
                            if a == "money":
                                pdm = 1
                            else:
                                pdm = assets[a]
                            pdttm = b*pdm*int(num)
                        csttm = []
                        for a, b in tya.items():
                            csm = assets[a]
                            csttm.append(csm*b*int(num))
                        cstm = 0
                        for a in csttm:
                            cstm += a
                        pfbf = float(decimal.Decimal(str(pdttm))-decimal.Decimal(str(cstm*2)))
                        if pfbf == int(pfbf):
                            pfbf = int(pfbf)
                        else:
                            while pfbf != int(pfbf):
                                pfbf *= 10
                                r *= 10
                            pfbf = int(pfbf)
                        pfs = repeating_dec_sol.repeating_dec_sol(pfbf, r*land)
                        if i == 1:
                            pfss.append({"Min": pfs})
                        else:
                            pfss.append({"Max": pfs})
                        i += 1
                    return [con_pfr, pro_pfr, pfss]
                for a, b in tyb.items():
                    if a == "money":
                        pdm = 1
                    else:
                        pdm = assets[a]
                    pdttm = b*pdm*int(num)
                csttm = []
                for a, b in tya.items():
                    csm = assets[a]
                    csttm.append(csm*b*int(num))
                cstm = 0
                for a in csttm:
                    cstm += a
                pfbf = float(decimal.Decimal(str(pdttm))-decimal.Decimal(str(cstm*2)))
                if pfbf == int(pfbf):
                    pfbf = int(pfbf)
                else:
                    while pfbf != int(pfbf):
                        pfbf *= 10
                        speed *= 10
                    pfbf = int(pfbf)
                pfs = repeating_dec_sol.repeating_dec_sol(pfbf, speed*land)
            return [con_pfr, pro_pfr, pfs]

    def produce_remain(fac, facdt, num=1, land=1):
        faclist = icd["facilities"]
        faccs = faclist[fac]["consumes"]
        facspeed = faclist[fac]["speed"]
        assets = icd["assets"]
        res1 = []
        res2 = []
        ld = []
        if type(facspeed) == list:
            for s in facspeed:
                for a, b in facdt:
                    ty = "_Max({})".format(a[-3:-1]) if re.search(r"_Max([0-9][0-9])$", a) else "_Min({})".format(a[-3:-1])
                    a = a[:-8]
                    if a == "N/A":
                        pd = a
                        sp = 1
                        b = "0"
                    else:
                        pd, = faclist[a]["produces"].keys()
                        f, = faclist[a]["produces"].values()
                        f = fractions.Fraction(f*b, faclist[a]["speed"])
                        sp = f-fractions.Fraction(faccs[pd]*int(num), s)
                        b = repeating_dec_sol.repeating_dec_sol(sp.numerator, sp.denominator)
                    res1.append((pd+ty, (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b))
                    if a == "N/A": b = fractions.Fraction(0)
                    else: b = sp*fractions.Fraction(str(assets[pd]))
                    ld.append(b)
                    if a == "N/A": b = "0"
                    else: b = repeating_dec_sol.repeating_dec_sol(b.numerator, b.denominator)
                    res2.append((pd+ty, (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b))
                pfld = sum(ld)/land
                res3 = repeating_dec_sol.repeating_dec_sol(pfld.numerator, pfld.denominator)
                res3 = (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b
                print(res1, res2, res3)
        else:
            for a, b in facdt:
                if a == "N/A":
                    pd = a
                    sp = 1
                    b = "0"
                else:
                    pd, = faclist[a]["produces"].keys()
                    f, = faclist[a]["produces"].values()
                    f = fractions.Fraction(f*b, faclist[a]["speed"])
                    sp = f-fractions.Fraction(faccs[pd]*int(num), facspeed)
                    b = repeating_dec_sol.repeating_dec_sol(sp.numerator, sp.denominator)
                res1.append((pd, (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b))
                if a == "N/A": b = fractions.Fraction(0)
                else: b = sp*fractions.Fraction(str(assets[pd]))
                ld.append(b)
                if a == "N/A": b = "0"
                else: b = repeating_dec_sol.repeating_dec_sol(b.numerator, b.denominator)
                res2.append((pd, (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b))
            pfld = sum(ld)/land
            res3 = repeating_dec_sol.repeating_dec_sol(pfld.numerator, pfld.denominator)
            res3 = (str(int(float(b))) if float(b).is_integer() else b) if re.fullmatch(r"[0-9]+[.][0-9]+", b) else b
        return [res1, res2, res3]

def setup(bot):
    bot.add_cog(calculate(bot))