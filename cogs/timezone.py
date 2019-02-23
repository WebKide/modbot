"""
MIT License
Copyright (c) 2019 WebKide [d.id @323578534763298816]
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import traceback
import discord
import asyncio

from datetime import datetime
from pytz import timezone
from discord.ext import commands

dev_list = [
    ('WebKide', 323578534763298816)
]


class TimeZone:
    """
    Timezone list of places
    https://gist.github.com/mjrulesamrat/0c1f7de951d3c508fb3a20b4b0b33a98
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Command to get time across the world', aliases=['timezone'])
    async def tz(self, ctx, *, flag_country: str = None):
        """ ✔ Return current time for a particular timezone

        Use <tz> [:flag_country_gb: / :flag_country_it:] or available name:

        Argentina, Australia, Brazil, China,
        India, Ireland, Israel, Italy,
        Mexico, Nepal, New Zealand, Panama,
        Peru, Philippines, Sri Lanka,
        GMT, PST, MST, CST, EST, HST, IST
        """
        countries = ['argentina', 'australia', 'brazil', 'china', 'india', 'ireland', 'israel', 'italy',
                     'mexico', 'nepal', 'new zealand', 'panama', 'peru', 'philippines', 'sri lanka',
                     'ist', 'gmt', 'england', 'london', 'est', 'hst', 'pst', 'mst', 'cst']
        m = ctx.message

        if flag_country is None:
            msg = f'**Usage:** `{ctx.prefix}{ctx.invoked_with} [:flag_gb: / country]`\n\n' \
                  f'**Available countries:** Argentina, Australia, Brasil, China, India, Ireland, Israel, Italy, ' \
                  f'Mexico, Nepal, New Zealand, Panama, Peru, Philippines, Sri Lanka'
            return await ctx.send(msg, delete_after=23)

        else:
            if any(x in m.content.lower() for x in countries):
                try:
                    flag_country = flag_country.lower()
                    place = flag_country.replace('australia', 'Australia/Sydney') \
                                        .replace('brazil', 'America/Sao_Paulo') \
                                        .replace('china', 'Asia/Shanghai') \
                                        .replace('india', 'Asia/Calcutta') \
                                        .replace('ist', 'Asia/Calcutta') \
                                        .replace('sri lanka', 'Asia/Colombo') \
                                        .replace('ireland', 'Europe/Dublin') \
                                        .replace('israel', 'Asia/Jerusalem') \
                                        .replace('gmt', 'Europe/London') \
                                        .replace('england', 'Europe/London') \
                                        .replace('london', 'Europe/London') \
                                        .replace('nepal', 'Asia/Katmandu') \
                                        .replace('new zealand', 'Pacific/Auckland') \
                                        .replace('panama', 'America/Panama') \
                                        .replace('est', 'America/New_York') \
                                        .replace('hst', 'Pacific/Honolulu') \
                                        .replace('pst', 'America/Los_Angeles') \
                                        .replace('mst', 'America/Denver') \
                                        .replace('cst', 'America/Chicago') \
                                        .replace('peru', 'America/Lima') \
                                        .replace('philippines', 'Asia/Manila') \
                                        .replace('argentina', 'America/Argentina/Buenos_Aires')
                    k = place.split()
                    zone_c = str(k).strip('[').strip(']').strip('\'').strip(' ')
                    title_c = zone_c.replace('/', ', ').replace('_', ' ')
                    z_1 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                    try:
                        flag_title = flag_country.title()
                        e_1 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_1, color=0x7289da)
                        s = await ctx.send(embed=e_1)
                        await asyncio.sleep(1)
                        z_2 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                        e_2 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_2, color=0xed791d)
                        await s.edit(embed=e_2)
                        await asyncio.sleep(2)
                        z_3 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                        e_3 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_3, color=0x7289da)
                        await s.edit(embed=e_3)
                        await asyncio.sleep(3)
                        z_4 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                        e_4 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_4, color=0xed791d)
                        await s.edit(embed=e_4)
                        await asyncio.sleep(5)
                        z_5 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                        e_5 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_5, color=0x7289da)
                        return await s.edit(embed=e_5)

                    except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                        return await ctx.send(f'{title_c}\n{z_1}')

                except Exception as e:
                    if ctx.author.id in (dev[1] for dev in dev_list):
                        if m.guild.id == 540072370527010841:
                            tb = traceback.format_exc()
                            return await ctx.send(f'```py\n[Error: 001] {e}\n!------------>\n{tb}```')
                        else:
                            pass
                    else:
                        pass

            else:
                try:
                    m_fl = m.content
                    place = m_fl.replace('🇦🇺', 'Australia/Sydney') \
                                .replace('🇧🇷', 'America/Sao_Paulo') \
                                .replace('🇨🇳', 'Asia/Shanghai') \
                                .replace('🇨🇷', 'America/Costa_Rica') \
                                .replace('cr', 'America/Costa_Rica') \
                                .replace('🇩🇪', 'Europe/Berlin') \
                                .replace('🇪🇸', 'Europe/Madrid') \
                                .replace('es', 'Europe/Madrid') \
                                .replace('🇫🇷', 'Europe/Paris') \
                                .replace('fr', 'Europe/Paris') \
                                .replace('🇬🇧', 'Europe/London') \
                                .replace('gb', 'Europe/London') \
                                .replace('uk', 'Europe/London') \
                                .replace('🇮🇳', 'Asia/Calcutta') \
                                .replace('in', 'Asia/Calcutta') \
                                .replace('🇮🇹', 'Europe/Rome') \
                                .replace('🇱🇰', 'Asia/Colombo') \
                                .replace('🇮🇪', 'Europe/Dublin') \
                                .replace('🇫🇮', 'Europe/Helsinki') \
                                .replace('🇮🇱', 'Asia/Jerusalem') \
                                .replace('🇲🇽', 'America/Mexico_City') \
                                .replace('🇳🇵', 'Asia/Katmandu') \
                                .replace('🇳🇿', 'Pacific/Auckland') \
                                .replace('🇵🇦', 'America/Panama') \
                                .replace('🇵🇪', 'America/Lima') \
                                .replace('🇵🇭', 'Asia/Manila') \
                                .replace('🇵🇱', 'Europe/Warsaw') \
                                .replace('🇷🇴', 'Europe/Bucharest') \
                                .replace('🇸🇬', 'Asia/Singapore') \
                                .replace('🇿🇦', 'Africa/Johannesburg') \
                                .replace('🇦🇷', 'America/Argentina/Buenos_Aires')
                    k = place.split('tz ')
                    zone_c = str(k[1:]).strip('[').strip(']').strip('\'').strip(' ')
                    title_c = zone_c.replace('/', ', ').replace('_', ' ')
                    z_1 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                    try:
                        flag_title = flag_country.title()
                        e_1 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_1, color=0x7289da)
                        s = await ctx.send(embed=e_1)
                        await asyncio.sleep(1)
                        z_2 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                        e_2 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_2, color=0xed791d)
                        await s.edit(embed=e_2)
                        await asyncio.sleep(2)
                        z_3 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                        e_3 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_3, color=0x7289da)
                        await s.edit(embed=e_3)
                        await asyncio.sleep(3)
                        z_4 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                        e_4 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_4, color=0xed791d)
                        await s.edit(embed=e_4)
                        await asyncio.sleep(5)
                        z_5 = datetime.now(timezone(zone_c)).strftime(f'%a %d %b, **%H:**%M:%S')
                        e_5 = discord.Embed(title=f'{flag_title} | {title_c}', description=z_5, color=0x7289da)
                        return await s.edit(embed=e_5)

                    except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                        return await ctx.send(f'{title_c}\n{z_1}')

                except Exception as e:
                    if ctx.author.id in (dev[1] for dev in dev_list):
                        if m.guild.id == 540072370527010841:
                            tb = traceback.format_exc()
                            return await ctx.send(f'```py\n[Error: 002] {e}\n!------------>\n{tb}```')
                        else:
                            pass
                    else:
                        pass


def setup(bot):
    bot.add_cog(TimeZone(bot))
