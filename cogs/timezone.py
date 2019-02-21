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

    @commands.command(description='Command to get time across world', aliases=['timezone'])
    async def tz(self, ctx, flag: str = None):
        """ ✔ Return current time for a particular timezone """
        if flag is None:
            msg = f'**Usage:** `{ctx.prefix}{ctx.invoked_with} :flag_gb:`'
            return await ctx.send(msg, delete_after=23)

        if flag is not None:
            try:
                m_fl = ctx.message.content.lower() or message.content.lower()
                if m_fl is not str:
                    place = m_fl.replace(':flag_ar:', 'America/Argentina/Buenos_Aires')\
                                .replace(':flag_au:', 'Australia/Sydney')\
                                .replace(':flag_br:', 'America/Sao_Paulo')\
                                .replace(':flag_cn:', 'Asia/Shanghai')\
                                .replace(':flag_in:', 'Asia/Calcutta')\
                                .replace(':flag_it:', 'Europe/Rome')\
                                .replace(':flag_lk:', 'Asia/Colombo')\
                                .replace(':flag_ie:', 'Europe/Dublin')\
                                .replace(':flag_il:', 'Asia/Jerusalem')\
                                .replace(':flag_mx:', 'America/Mexico_City')\
                                .replace(':flag_np:', 'Asia/Katmandu')\
                                .replace(':flag_nz:', 'Pacific/Auckland')\
                                .replace(':flag_pa:', 'America/Panama')\
                                .replace(':flag_pe:', 'America/Lima')\
                                .replace(':flag_ph:', 'Asia/Manila')\
                                .replace(':flag_za:', 'Africa/Johannesburg')
                    partial = place.split()
                    converted = str(partial[1:]).strip('[').strip(']').strip('\'').strip(' ')
                    result = datetime.now(timezone(converted)).strftime(f'{flag} | %a %d %b, **%H:**%M:%S')
                else:
                    place = m_fl.replace(':flag_ar:', 'America/Argentina/Buenos_Aires')\
                                .replace(':flag_au:', 'Australia/Sydney')\
                                .replace(':flag_br:', 'America/Sao_Paulo')\
                                .replace(':flag_cn:', 'Asia/Shanghai')\
                                .replace(':flag_in:', 'Asia/Calcutta')\
                                .replace(':flag_it:', 'Europe/Rome')\
                                .replace(':flag_lk:', 'Asia/Colombo')\
                                .replace(':flag_ie:', 'Europe/Dublin')\
                                .replace(':flag_il:', 'Asia/Jerusalem')\
                                .replace(':flag_mx:', 'America/Mexico_City')\
                                .replace(':flag_np:', 'Asia/Katmandu')\
                                .replace(':flag_nz:', 'Pacific/Auckland')\
                                .replace(':flag_pa:', 'America/Panama')\
                                .replace(':flag_pe:', 'America/Lima')\
                                .replace(':flag_ph:', 'Asia/Manila')\
                                .replace(':flag_za:', 'Africa/Johannesburg')
                    result = 'working on country initials as argument'  # datetime.now(timezone(place[1:])).strftime(f'{flag} | %a %d %b, **%H:**%M:%S')

                await ctx.send(result)

            except Exception as e:
                if ctx.author.id in (dev[1] for dev in dev_list):
                    tb = traceback.format_exc()
                    await ctx.send(f'```py\n{e}\n!------------>\n{tb}```')

                else:
                    pass


def setup(bot):
    bot.add_cog(TimeZone(bot))
