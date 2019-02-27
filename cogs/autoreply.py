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
guilds_spam = [
    ('Mds', 540072370527010841),
    ('spam_log', 540600062217158666),
    ('invites', 541059392951418880),
    ('msg_log', 541061070907899905),
    ('default', 540072370979864577),
    ('ignored_chan', 540582467648749569),
    ('ssevana', 328341202103435264)
]
whitelisted_guilds = [('Modbot DS', 540072370527010841)]
blacklisted_users = [
    ('bv', 358433182304960513),
    ('4jr', 180314310298304512),
    ('kybre', 325012556940836864)
]


class AutoReply:
    """
    Automatically reply to users, or not
    """

    def __init__(self, bot):
        self.bot = bot
        # self.user_color = discord.Colour(0xed791d)

    # Monitoring guild events and member messages
    @staticmethod
    async def on_message(message):
        """ Process on_message content """
        if message.author.bot:  # avoid replying to other bots in an endless loop
            return  # avoid replying to other bots in an endless loop, oof

        if message is None:
            return

        if message.guild.id not in (x[1] for x in whitelisted_guilds):
            return

        if message.author.id in (x[1] for x in blacklisted_users):
            return

        userinfo = f'**{message.author.display_name}** | `{message.author.id}`'
        msgLower = message.content.lower()
        msgs = []

        # +------------------------------------------------------------+
        # |          I am Modbot, nice to meet you                     |
        # +------------------------------------------------------------+
        if message.content.startswith('I am '):

            if random.randint(1, 3) != 1:
                return

            else:
                try:
                    hello = ['Hello', 'nice to meet you', 'Hi there', 'Rādhe Rādhe', 'hello', 'henlo', 'Namasté',
                             'Ciao', 'Buon giorno', 'how is it going', 'long time no see', 'howdy', 'My pleasure',
                             'Shalom', 'Konnichiwa', 'how are things', 'good to see you', 'Bonjour', 'Guten Tag',
                             'Privet', 'Anyoung haseyo', 'Ahlan', 'Nǐ hǎo', 'Qué tal', 'Parev', 'Hallo', 'Aloha',
                             'Dia dhuit', 'Bunã ziua', 'Merhaba', 'Vitayu', 'Hei', 'Vaya vaya', 'Caramba']
                    i_am = ['I am', 'my name is', 'me llamo', 'you can call me', 'pleasure meeting you, I am',
                            'please call me', 'watashi wa', 'Io mi chiamo', 'Ich heiße']
                    rep = f'{random.choice(hello)} *{message.content[5:].title()}*, {random.choice(i_am)} Modbot'

                    await message.channel.send(rep)

                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    return

        # +------------------------------------------------------------+
        # |          Flipping tables, it might spam the chat           |
        # +------------------------------------------------------------+
        if message.content.startswith('(╯°□°）╯︵ ┻━┻'):

            if random.randint(1, 3) != 1:
                return

            else:
                with open('data/flipping_tables.json') as f:
                    kaomoji = json.load(f)

                try:
                    e = discord.Embed(color=0x7289da)
                    e.add_field(name=userinfo,
                                value=f'{random.choice(kaomoji)}')

                    if random.randint(1, 3) != 1:
                        await message.channel.send(f'{random.choice(kaomoji)}')
                    else:
                        await message.channel.send(embed=e)

                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    await message.channel.send(f'{random.choice(kaomoji)}')


def setup(bot):
    bot.add_cog(AutoReply(bot))
