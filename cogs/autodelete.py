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

import discord
import asyncio
import aiohttp
import datetime
import time
import random
import json
import sys
import os
import re
import traceback
import textwrap

from datetime import timedelta
from discord.ext import commands
from pathlib import Path

dev_list = [('WebKide', 323578534763298816)]
bot_channel = 375179500604096512
guilds_spam = [('Mds', 540072370527010841),
               ('spam_log', 540600062217158666),
               ('invites', 541059392951418880),
               ('msg_log', 541061070907899905),
               ('default', 540072370979864577),
               ('ignored_chan', 540582467648749569),
               ('ssevana', 328341202103435264)]
# +------------------------------------------------------------+
# |       Dictionary of blacklisted words for test             |
# +------------------------------------------------------------+
url_list = ['discord.gg/', 'discord.io/', 'discord.me/', 'discordapp.com/invite/',
            'discordlisting.me', 'discordlist.me', 'invite/']


class AutoDelete:
    """
    Automatic message deletion, blaclisted words, server invites
    """

    def __init__(self, bot):
        self.bot = bot
        self.user_color = discord.Colour(0xed791d)

    # +------------------------------------------------------------+
    # |          Blacklist words command group                     |
    # |            it shows usage if no word str is given          |
    # +------------------------------------------------------------+
    @commands.group(invoke_without_command=True)
    async def blw(self, ctx):
        """ Blacklist words cmd """
        if 'include' not in ctx.message.content:
            usage = f'```css\n{ctx.prefix}{ctx.invoked_with} <add> [pacman]\n```'
            await ctx.send(usage)
    
    @blw.command(no_pm=True)
    async def include(self, ctx, *, _include: str = None):
        """ Blacklist word add """
        if _include is None:
            await ctx.message.add_reaction('\N{WAVING HAND SIGN}')
        
        if _include is not None:
            with open('data/blacklist_words.json', 'a') as f:
                json_words = f.write(_include)
                await ctx.send(f'added {json_words}')
                await ctx.message.add_reaction('\N{CHERRIES}')

    # Monitoring guild events and member messages
    async def on_message(self, message):
        if message.guild.id not in (x[1] for x in guilds_spam):
            return

        userinfo = f'**{message.author.display_name}** | `{message.author.id}`'
        msgLower = message.content.lower()
        msgs = []
        with open('data/blacklist_words.json') as f:  # json file that contains blacklisted words
            blacklisted_words = json.load(f)

        # +------------------------------------------------------------+
        # |          Needs more work for blacklist words to work       |
        # |          per guild, role, and channel in db                |
        # +------------------------------------------------------------+
        if any(x in message.content.lower() for x in blacklisted_words):
            try:
                await message.delete()
                await message.add_reaction('\N{WARNING SIGN}')

            except discord.Forbidden:
                pass

            finally:
                if random.randint(1, 3) != 1:
                    warn = f"{userinfo}\n" \
                           f"\N{WARNING SIGN} Watch your language!"
                    await message.channel.send(warn, delete_after=60)

        # +------------------------------------------------------------+
        # |          Server invite monitor and auto-deleter            |
        # |            it warns user and logs invite with author ID    |
        # +------------------------------------------------------------+
        if message.guild.id in (x[1] for x in guilds_spam):
            if message.channel.id in (x[1] for x in guilds_spam):
                return

            else:
                if '/HDJZnEj' in message.content:  # Modbot development support official invite
                    return
                if '/dvAq6Hm' in message.content:  # Ssevana official invite
                    return

                if any(x in msgLower for x in url_list):
                    warns = f"{userinfo}\n" \
                            f"\N{WARNING SIGN} Invites aren't allowed in this text channel!"

                    try:
                        # Invites are logged in deleted-invites channel
                        await message.delete()

                    except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                        await message.channel.send(warns, delete_after=69)

                        try:
                            await message.add_reaction('\N{AUBERGINE}')

                        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                            pass

                    finally:
                        # invite links and their message are logged if there's a channel for them
                        log_content = f'{userinfo} *spammed in:*\n' \
                                      f'```css\ntChan: {message.channel.name} | {message.channel.id}\n' \
                                      f'Guild: {message.guild.name} | {message.guild.id}```' \
                                      f'{message.content}'
                        return await self.bot.get_channel(541059392951418880).send(log_content)


def setup(bot):
    bot.add_cog(AutoDelete(bot))
