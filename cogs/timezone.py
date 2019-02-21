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
                place = m_fl.replace('🇦🇷', 'America/Argentina/Buenos_Aires')\
                            .replace('ar', 'America/Argentina/Buenos_Aires')\
                            .replace('🇦🇺', 'Australia/Sydney')\
                            .replace('au', 'Australia/Sydney')\
                            .replace('🇧🇷', 'America/Sao_Paulo')\
                            .replace('🇨🇳', 'Asia/Shanghai')\
                            .replace('cn', 'Asia/Shanghai')\
                            .replace('🇨🇷', 'America/Costa_Rica')\
                            .replace('cr', 'America/Costa_Rica')\
                            .replace('🇩🇪', 'Europe/Berlin')\
                            .replace('🇪🇸', 'Europe/Madrid')\
                            .replace('es', 'Europe/Madrid')\
                            .replace('🇫🇷', 'Europe/Paris')\
                            .replace('fr', 'Europe/Paris')\
                            .replace('🇬🇧', 'Europe/London')\
                            .replace('gb', 'Europe/London')\
                            .replace('uk', 'Europe/London')\
                            .replace('🇮🇳', 'Asia/Calcutta')\
                            .replace('in', 'Asia/Calcutta')\
                            .replace('🇮🇹', 'Europe/Rome')\
                            .replace('it', 'Europe/Rome')\
                            .replace('🇱🇰', 'Asia/Colombo')\
                            .replace('🇮🇪', 'Europe/Dublin')\
                            .replace('🇫🇮', 'Europe/Helsinki')\
                            .replace('fi', 'Europe/Helsinki')\
                            .replace('🇮🇱', 'Asia/Jerusalem')\
                            .replace('🇲🇽', 'America/Mexico_City')\
                            .replace('🇳🇵', 'Asia/Katmandu')\
                            .replace('🇳🇿', 'Pacific/Auckland')\
                            .replace('nz', 'Pacific/Auckland')\
                            .replace('🇵🇦', 'America/Panama')\
                            .replace('🇵🇪', 'America/Lima')\
                            .replace('🇵🇭', 'Asia/Manila')\
                            .replace('🇵🇱', 'Europe/Warsaw')\
                            .replace('🇷🇴', 'Europe/Bucharest')\
                            .replace('🇸🇬', 'Asia/Singapore')\
                            .replace('🇿🇦', 'Africa/Johannesburg')
                converted = place.split(' ')
                # result = datetime.now(timezone(converted[1:])).strftime(f'{flag} | %a %d %b, **%H:**%M:%S')
                result = datetime.now(timezone(str(converted[1:]).replace('[', '').replace(']', '')\
                                                                 .replace('\'', '').replace(' ', '')))\
                                                                 .strftime(f'{flag} | %a %d %b, **%H:**%M:%S')
                await ctx.send(result)

            except Exception as e:
                if ctx.author.id in (dev[1] for dev in dev_list):
                    tb = traceback.format_exc()
                    await ctx.send(f'```py\n{e}\n!------------>\n{tb}```')

                else:
                    pass


def setup(bot):
    bot.add_cog(TimeZone(bot))
