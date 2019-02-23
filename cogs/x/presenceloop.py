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
import random
import traceback

from discord.ext import commands
from aiohttp import ClientSession

status_loop_channel = 545719518903926807  # status-loop channel in dev-server
activity_list = ['you', 'this server', 'everything', 'new members', 'Anime', 'hentai', 'yo mama']
dev_list = [('WebKide', 323578534763298816)]

class PresenceLoop:
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session
        # self.loop.create_task(self.periodic_presence_change())  # create presence-loop
        self.mod_color = discord.Colour(0x7289da)  # Blurple
        self.user_color = discord.Colour(0xed791d)  # Orange
        self.loop.create_task(self.periodic_presence_change())
        # self.session = None or aiohttp.ClientSession(loop=self.loop, headers={'User-Agent' : 'ModBot Discord'})

    @property
    def session(self):
        if self.session is None:
            self.session = ClientSession(loop=self.loop)
        return self.session

    # +------------------------------------------------------------+
    # |             Activity Presence-loop task                    |
    # +------------------------------------------------------------+
    @staticmethod
    def periodic_presence_change(self):
        """ ✔ Loop task for rotating presence """
        # ###await self.wait_until_ready()
        while True:
            for status in activity_list:
                # To avoid RATE LIMIT:
                # --> WebSocket connection is closed: code = 4008 (private use), reason = Rate limited.
                # --> Task was destroyed but it is pending!
                timer = 69  # random.randint(123, 369)
                await asyncio.sleep(timer)

                try:
                    if random.randint(1, 2) != 1:
                        await self.change_presence(status=discord.Status.dnd,
                                                          activity=discord.Activity(type=discord.ActivityType.watching,
                                                                                    name=status))
                        try:
                            watchin = f'\N{FILM FRAMES} `Status set to:` Watching **{status}** | `after: {timer} sec`'
                            await self.get_channel(status_loop_channel).send(watchin)  # to track time gap

                        except discord.HTTPException:
                            pass

                    else:
                        await self.change_presence(status=discord.Status.online,
                                                   activity=discord.Activity(type=discord.ActivityType.listening,
                                                                             name=status))
                        listen = f'\N{HEADPHONE} `Status set to:` Listening to **{status}** | `after: {timer} sec`'
                        try:
                            await self.get_channel(status_loop_channel).send(listen)  # to track time gap between changes

                        except discord.HTTPException:
                            pass

                except Exception as e:
                    tb = traceback.format_exc()
                    error = f'```py\n[ERROR: 001] {e}\n!------------>\n{tb}```'
                    await self.get_channel(status_loop_channel).send(error)

    @commands.group(name='presence', aliases=['pre'], invoke_without_subcommand=True)
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def _presence(self, ctx, *, status: str = None):
        """ Find that video you want to share """
        if ctx.message.author.id not in (dev[1] for dev in dev_list):
            return
        else:
            await ctx.send(f'Wrong {status}')

    @_presence.command(aliases=['listening', 'l'])
    async def listen(self, ctx, *, music: str = None):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.listening,
                                                                 name=music))
        await ctx.send(f'Listening to: {music}')

    @_presence.command(aliases=['watching', 'w'])
    async def watch(self, ctx, *, video: str = None):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.listening,
                                                                 name=video))
        await ctx.send(f'Watching: {video}')

    @_presence.command(aliases=['streaming', 's'])
    async def stream(self, ctx, *, stream: str = None):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Activity(type=discord.ActivityType.listening,
                                                                 name=stream))
        await ctx.send(f'Listening to: {stream}')


def setup(bot):
    bot.add_cog(PresenceLoop(bot))
