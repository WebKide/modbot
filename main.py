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
import traceback
import textwrap
import aiohttp
import asyncio
import time
import os
import random
import json

from discord.ext import commands


# watch = discord.Activity(type=2, name='this guild'))
dev_list = [
    323578534763298816,
    180314310298304512,
    325012556940836864
]
# for the time being, blacklist is here,
# later has to be implemented in bot's db
blacklisted_words = [
    'kms',
    'go die',
    'fuck off'
]

class ModBot(commands.Bot):
    """
    a moderation bot for Discord guilds
    """
    _mentions_transforms = {
        '@everyone': '@\u200beveryone',
        '@here': '@\u200bhere'
    }
 
    _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))
 
    def __init__(self, **attrs):
        super().__init__(command_prefix=commands.when_mentioned_or(self.get_pre))
        self._extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
        self.run(os.getenv('TOKEN').strip('\"'))
        self.add_command(self.ping)
        self.add_command(self.shutdown)
        self.add_command(self.load)
        self.add_command(self.reloadcog)
        self.add_command(self.unload)
        self.load_extensions()
        

    def load_extensions(self, cogs=None, path='cogs.'):
        """ Load extensions from cogs folder """
        for extension in cogs or self._extensions:
            try:
                self.load_extension(f'{path}{extension}')
                print(f'Loaded extension: {extension}')
            except Exception as e:
                traceback.print_exc()

    @classmethod
    def init(bot):
        """ ModBot, get ready! """
        bot = bot()
        heroku_token = TOKEN or None
        if None:
            print(e, '\n!-- Missing TOKEN in Heroku')
        else:
            try:
                bot.run(heroku_token, reconnect=True)
            except Exception as e:
                print(e, '\n!-- Missing TOKEN in Heroku')

    @staticmethod
    async def get_pre(bot, message):
        """ Get the prefix from Heroku, 
        default prefix is mention """
        try:
          return os.environ.get('PREFIX') or 'modbot '
        except Exception as e:
            print(e, '\n!-- Missing PREFIX in Heroku')

    async def on_connect(self):
        """ If you see this in the logs, congrats """
        print('>+---------------------+<\n\n'
              '|V| _  _||_  _ |_'
              '| |(_)(_||_)(_)|_'
              '\nmain.py loaded')
 
    async def on_ready(self):
        """ If everything is fine, then... """
        print(textwrap.dedent(f"""
        Your instance of ModBot
        is ready to watch over
        your Discord guild and
        its active members!

        -------- (｡◝‿◜｡) --------
        Logged in as: {self.user}
        User ID: {self.user.id}
        >+---------------------+<
        """))
 
        watch = discord.Activity(type=discord.ActivityType.watching, name='this guild')
		await self.change_presence(activity=watch)

    async def process_commands(self, message):
        """ Members might mention by mistake """
        if message is None:
            return

    # Still have to work this out to: ignore correctly, 
    # to listen for commands invoqued by assigned role, 
    # and to delete messages that need to be purged 
    # automatically, and to respond to available cmds
    async def on_message(self, message):
        """ Guild messages monitoring system """
        if message.author.bot:
            return

        # Needs more work for blacklist words per guild, role, and channel in db
        if blacklisted_words in message.content:
            await message.delete()
 
        if message.content.startswith('Lol'):
            await message.delete()
 
        if message.author.bot:
            return
 
    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        result = self.ws.latency * 1000:.4f
        em = discord.Embed(color = 0x7289da)
        em.title ='Pong! Websocket Latency:'
        em.description = f'{result} ms'
        if ctx.author.id in dev_list:
            try:
                await ctx.send(embed=em)
            except discord.HTTPException:
                await ctx.send('ᕙ(⇀‸↼‶)ᕗ ', result)
        else:
            return


if __name__ == '__main__':
    ModBot.init()
    
