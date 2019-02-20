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

import datetime
import traceback

from pytz import timezone
from discord.ext import commands

dev_list = [
    ('WebKide', 323578534763298816)
]


class TimeZone:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Command to get time across world', aliases=['timezone'])
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def tz(self, ctx, flag: str = None):
        """ Return current time for a particular timezone """
        if flag is None:
            return await ctx.send('smh, include a flag for the timezone you want to know')

        if flag is not None:
            try:
                place = flag.replace(':flag_ar:', 'America/Argentina/Buenos_Aires')\
                            .replace(':flag_au:', 'Australia/Sydney')\
                            .replace(':flag_br:', 'America/Sao_Paulo')\
                            .replace(':flag_cn:', 'Asia/Shanghai')\
                            .replace(':flag_cr:', 'America/Costa_Rica')\
                            .replace(':flag_de:', 'Europe/Berlin')\
                            .replace(':flag_es:', 'Europe/Madrid')\
                            .replace(':flag_fr:', 'Europe/Paris')\
                            .replace(':flag_gb:', 'Europe/London')\
                            .replace(':flag_it:', 'Europe/Rome')\
                            .replace(':flag_lk:', 'Asia/Colombo')\
                            .replace(':flag_mx:', 'America/Mexico_City')\
                            .replace(':flag_np:', 'Asia/Katmandu')\
                            .replace(':flag_nz:', 'Pacific/Auckland')\
                            .replace(':flag_pa:', 'America/Panama')\
                            .replace(':flag_pe:', 'America/Lima')\
                            .replace(':flag_ph:', 'Asia/Manila')\
                            .replace(':flag_pl:', 'Europe/Warsaw')\
                            .replace(':flag_ro:', 'Europe/Bucharest')\
                            .replace(':flag_sg:', 'Asia/Singapore')\
                            .replace(':flag_za:', 'Africa/Johannesburg')
                result = datetime.now(timezone(place)).strftime(f'{flag} %a %d %b, **%H:**%M:%S')
                await ctx.send(result)

            except Exception as e:
                tb = traceback.format_exc()
                await ctx.send(f'```py\n{e}\n!------------>\n{tb}```')

        else:
            msg = f'**Usage:** `{ctx.prefix}{ctx.invoked_with} :flag_gb:`'
            return await ctx.send(msg, delete_after=23)


def setup(bot):
    bot.add_cog(TimeZone(bot))
