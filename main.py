'''
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
'''

import discord
import asyncio
import aiohttp
import datetime
import time
import json
import sys
import os
import re
import traceback
import textwrap
## import psutil

from discord.ext import commands
from pathlib import Path

dev_list = [('WebKide', 323578534763298816),
            ('Kybre', 325012556940836864),
            ('4JR', 180314310298304512)
]
# +------------------------------------------------------------+
# |               ModBot has its own class!                    |
# +------------------------------------------------------------+
class ModBot(commands.Bot):
    """
    a moderation bot for cool Discord guilds
    """
    _mentions_transforms = {
        '@everyone': '@\u200beveryone',
        '@here': '@\u200bhere'
    }

    _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

    # +------------------------------------------------------------+
    # |             Here starts the actual bot                     |
    # +------------------------------------------------------------+
    def __init__(self, **attrs):
        super().__init__(command_prefix=None)
        self.startup_ext = [x.stem for x in Path('cogs').glob('*.py')]
        self._extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
        self.run(os.getenv('TOKEN').strip('\"'))
        self.add_command(self.ping)
        self.add_command(self.shutdown)
        self.add_command(self.load)
        self.add_command(self.reloadcog)
        self.add_command(self.unload)
        self.load_extensions()

    # +------------------------------------------------------------+
    # |         Here we load the cogs onto the env                 |
    # +------------------------------------------------------------+
    def load_extensions(self, cogs=None, path='cogs.'):
        """ Load extensions from ./cogs/ """
        print('\n\n+----------▿▿▿▿▿----------+\n'
              '|                         |\n'
              '|   |V| _  _||_  _ |_ ™   |\n'
              '|   | |(_)(_||_)(_)|_     |\n'
              '|                         |\n'
              '|          ᶠᵒʳ ᵈⁱˢᶜᵒʳᵈ    |\n'
              '|                         |')
        for extension in cogs or self._extensions:
            try:
                self.load_extension(f'{path}{extension}')
                print(f'|✧Loading extension: {extension} |')
            except Exception as e:
                print(f'|✧ERROR loading file!     |\n'
                      f'| {e}')

    # +------------------------------------------------------------+
    # |             Here we get the bot's TOKEN                    |
    # +------------------------------------------------------------+
    @classmethod
    def init(bot):
        """ ModBot, get ready! """
        bot = bot()
        heroku_token = TOKEN or None
        if None:
            return print(Exception, '!-- Missing TOKEN in Heroku')
        else:
            try:
                bot.run(heroku_token, reconnect=True)
            except Exception as e:
                print(e, '\n!-- Missing TOKEN in Heroku')

    async def get_prefix(self, message):
        return commands.when_mentioned_or('..', 'modbot ')(self, message)

    # +------------------------------------------------------------+
    # |     Here modbot loads cogs and shows errors, if any        |
    # +------------------------------------------------------------+
    async def on_connect(self):
        """ If you see this in the logs, congrats """
        print('|✧Loaded bot: main.py     |')

        for ext in self.startup_ext:
            try:
                self.load_extension(f'cogs.{ext}')
            except Exception as e:
                print(f'|✧Failed to load: {ext}    |\n'
                      f'| {e}')
            else:
                print(f'|✧Loaded extension: {ext}  |')

    # +------------------------------------------------------------+
    # |             If everything went well...                     |
    # +------------------------------------------------------------+
    async def on_ready(self):
        """ Modbot is online! """
        print(f'|                         |\n'
              f'|  (∩｀-´)⊃━☆ﾟ.*･｡ﾟ~[ ♡ ] |\n'
              f'|                         |\n'
              f'| Your instance of ModBot |\n'
              f'| is ready to watch over  |\n'
              f'| your Discord guild and  |\n'
              f'| its active members!     |\n'
              f'|                         |\n'
              f'+-------- (｡◝‿◜｡) --------+\n'
              f'  Logged in as: {self.user}\n'
              f'  ID: {self.user.id}\n'
              f'+-------------------------+\n'
              f' ██░░░░░░░░░░░░░░░░░░░░ 10%\n'
              f'+-------------------------+\n')

        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, 
                                                             name='over you'))

    async def process_commands(self, message):
        """ Members might mention by mistake """
        if message is None:
            return
    # +------------------------------------------------------------+
    # |   Still have to work this out to: ignore correctly,
    # |   to listen for commands invoqued by assigned role,
    # |   and to delete messages that need to be purged
    # |   automatically, and to respond to available cmds
    # +------------------------------------------------------------+
    async def on_message(self, message):
        """ Guild messages monitoring system """
        if message.author.bot:
            return

    # +------------------------------------------------------------+
    # |               Cliché commands                              |
    # +------------------------------------------------------------+
    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        pong = f'{self.bot.ws.latency * 1000:.4f} ms'
        e = discord.Embed(color=0x7289da)
        e.title = 'Pong! Websocket Latency:'
        e.description = pong
        x = ctx.message.author.id or message.author.id
        if x not in (dev[1] for dev in dev_list):
            return
        if x in (dev[1] for dev in dev_list):
            try:
                await ctx.send(embed=e)
            except discord.HTTPException:
                await ctx.send('ᕙ(⇀‸↼‶)ᕗ ', pong)
        else:
            return

# +------------------------------------------------------------+
# |       Dictionary of blacklisted words for test             |
# +------------------------------------------------------------+
blacklisted_words = ['nope', 'kms', 'go die', 'fuck off']

if __name__ == '__main__':
    ModBot.init()

