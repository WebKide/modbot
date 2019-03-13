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
import random
import asyncio
import aiohttp
import traceback
import os
import re
import datetime
try:
    import psutil
except ModuleNotFoundError:
    pass

from datetime import datetime
from pytz import timezone
from discord.ext import commands
from pathlib import Path

__version__ = '0.05.1'  # first int is main, second is stable, third is working release [0.00.0]
dev_list = [
    ('WebKide', 323578534763298816),
    ('Kybre', 325012556940836864)
]
status_loop_channel = 545719518903926807  # status-loop channel in dev-server
activity_list = ['you', 'this server', 'everything', 'new members', 'Anime', 'hentai', 'yo mama']
__notes__ = "BETA version, official stable release. \n✔ commands are available to all " \
            "members. \nᗣ commands are restricted to Mod, Admin, and Owner roles. \n" \
            "✯ commands are only for Modbot Developer. \nWe're working to fix bugs " \
            "and add more functionality, thanks for your patience."


# +------------------------------------------------------------+
# |               ModBot has its own class!                    |
# +------------------------------------------------------------+
class ModBot(commands.Bot):
    """ a moderation bot for Discord guilds """
    _mentions_transforms = {
        '@everyone': '@\u200beveryone',
        '@here': '@\u200bhere'
    }

    _mention_pattern = re.compile('|'.join(_mentions_transforms.keys()))

    # +------------------------------------------------------------+
    # |             Here starts the actual bot                     |
    # +------------------------------------------------------------+
    def __init__(self, **attrs):
        self.description = f'|⌄| _  _||_  _ |_ ™\n| |(_)(_||_)(_)⎩_ v.{__version__}\n\n{__notes__}'
        self.ownerID = 323578534763298816
        super().__init__(command_prefix=commands.when_mentioned_or('botto ', '.', 'modbot '),
                         description=self.description, owner_id=self.ownerID, **attrs)
        self.add_command(self.ping)
        self.add_command(self.about)
        self.add_command(self.restart)  # hidden cmd
        self.add_command(self.load)
        self.add_command(self.reload)
        self.add_command(self.unload)
        self.startup_ext = [x.stem for x in Path('cogs').glob('*.py')]
        self._extensions = [x.replace('.py', '') for x in os.listdir('cogs') if x.endswith('.py')]
        self.run(os.getenv('TOKEN').strip('\"'))
        self.version = __version__
        self.load_extensions()  # automatically loads plugins inside /cogs/
        self.loop.create_task(self.periodic_presence_change())  # create presence-loop
        self.mod_color = discord.Colour(0x7289da)  # Blurple
        self.user_color = discord.Colour(0xed791d)  # Orange
        # self.process = psutil.Process()  # to monitor RAM and space
        self.session = None or aiohttp.ClientSession(loop=self.loop, headers={'User-Agent' : 'ModBot Discord'})
        # self.session = aiohttp.ClientSession(loop=self.loop, headers={'User-Agent' : 'ModBot Discord'})

    # +------------------------------------------------------------+
    # |         Here we load the cogs onto the bot                 |
    # +------------------------------------------------------------+
    def load_extensions(self, cogs=None, path='cogs.'):
        """ Start loading plugins from /cogs/ """
        print('\n\n\n┌─────────▿▿▿▿▿▿──────────┐')
        print('│✧ Created by: webKide    │')
        print(f'│        v.{__version__}         │')
        print('│           ◜◝            │')

        for plugin in cogs or self._extensions:
            try:
                self.load_extension(f'{path}{plugin}')
            # except Exception:
            except plugin is None:  # if it cannot find them, it passes silently
                pass

    # +------------------------------------------------------------+
    # |         Here is where the prefix is defined                |
    # |         need to fix heroku variable feature                |
    # +------------------------------------------------------------+
    '''
    @property
    def guild_id(self):
        from_heroku = os.environ.get('GUILD_ID')
        return int(from_heroku) if from_heroku else GUILD_ID

    @property
    def log_chan_id(self):
        from_heroku = os.environ.get('LOG_CHAN_ID')
        return int(from_heroku) if from_heroku else LOG_CHAN_ID
    '''
    # +------------------------------------------------------------+
    # |             Here we get the bot's TOKEN                    |
    # +------------------------------------------------------------+
    @property
    def heroku_token(self):
        """ Return Modbot's token from Heroku """
        return os.environ.get('TOKEN') or None

    @classmethod
    def init(bot):
        """ ModBot, get ready! """
        bot = bot()
        heroku_token = TOKEN or None
        if heroku_token is None:
            return print(Exception)
        else:
            try:
                bot.run(heroku_token, reconnect=True)
            except Exception as e:
                print(f'├ !-- Missing TOKEN in Heroku')
                print(e)

    # +------------------------------------------------------------+
    # |            Here the bot connects and loads cogs            |
    # +------------------------------------------------------------+
    async def on_connect(self):
        """ If you see this in the logs, modbot is alive """
        print('│   |⌵| _  _||_  _ |_ ™   │\n'
              '│   | |(_)(_||_)(_)⎩_     │\n'
              '│                         │\n'
              '│          ᶠᵒʳ ᵈⁱˢᶜᵒʳᵈ    │\n'
              '│                         └\n'
              '├ ✔ Loaded Modbot: main.py')

        for ext in self.startup_ext:
            try:
                self.load_extension(f'cogs.{ext}')
            except Exception as e:
                print(f'├ ✖ E R R O R  w/: {ext}.py\n'
                      f'├  {e}')
            else:
                print(f'├ ✔ Loaded Plugin: {ext}')

    # +------------------------------------------------------------+
    # |    For the time being, Modbot works on single guild only   |
    # +------------------------------------------------------------+
    @property
    def guild(self):
        """ Guild monitored by Modbot """
        return discord.utils.get(self.guilds)

    # +------------------------------------------------------------+
    # |            If everything went well...                      |
    # +------------------------------------------------------------+
    async def on_ready(self):
        """ If everything is fine, then... """
        print('│                         ┌\n'
              '│  (∩｀-´)⊃━✧｀｀｀｀｀｀ ♡ │\n'
              '│                         │\n'
              '│ Your instance of ModBot │\n'
              '│ is ready to watch over  │\n'
              '│ your Discord guild and  │\n'
              '│ its active members!     │\n'
              '│                         │\n'
              '├─────────────────────────┤\n'
              f'  ID: {self.user.id}\n'
              f'  Logged as: {self.user}\n'
              f'  Monitoring: {self.guild.name}\n'
              '├─────────────────────────┤\n'
              '│██████████████████░░ 93% │\n'
              '└─────────────────────────┘\n')

        status = "@Mod help | Massachusetts Live by Slipknot 🔂"
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(type=discord.ActivityType.listening,
                                                             name=status))
        msg = f'<:thonkingcool:540582184306606113> `Status set to:` Listening to **{status}** | `{self.ws.latency * 1000:.2f} ms`'
        await self.get_channel(status_loop_channel).send(msg)
        # ==================================================
        #            Waking up message!
        # ==================================================
        result = datetime.now(timezone('Europe/London')).strftime(f'**%a** %d %b, **%H**:%M:%S')
        txt = f'Websocket: `{self.ws.latency * 1000:.2f}` ms\n{result}'
        try:
            await self.get_channel(540600062217158666).send(txt)
        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
            gen_chan = os.environ.get('CHAN')
            try:
                await self.get_channel(gen_chan).send(txt)
            except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                pass

    # +------------------------------------------------------------+
    # |                Cliché commands                             |
    # +------------------------------------------------------------+
    @commands.command(description='Websocket latency')
    async def ping(self, ctx):
        """ ✔ Websocket latency, Pong! """
        pong = f'Latency: **`{self.ws.latency * 1000:.2f}`** ms ᕙ(⇀‸↼‶)ᕗ'

        e = discord.Embed(color=0x7289da)
        e.description = pong

        try:
            await ctx.message.add_reaction('\N{TABLE TENNIS PADDLE AND BALL}')
            await ctx.send(embed=e)
        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
            await ctx.send(pong)

    @commands.command(description='Modbot, a bot developed by WebKide', aliases=['bot', 'botto', 'info', 'invite'])
    async def about(self, ctx):
        """ ✔ Modbot info page """
        g = ctx.guild
        b = ctx.bot
        avy = 'https://cdn.discordapp.com/avatars/341645136981393409/a012ded302fa014b32302fed9724cde6.webp'

        # total_members = sum(1 for _ in b.get_all_members())
        total_online = len({m.id for m in b.get_all_members() if m.status is discord.Status.online})
        total_idle = len({m.id for m in b.get_all_members() if m.status is discord.Status.idle})
        total_dnd = len({m.id for m in b.get_all_members() if m.status is discord.Status.dnd})
        total_offline = len({m.id for m in b.get_all_members() if m.status is discord.Status.offline})
        total_unique = len(b.users)

        join_number = sorted(g.members, key=lambda m: m.joined_at).index(self.user) + 1
        # memory_usage = self.process.memory_full_info().uss / 1024 ** 2 or '0.0'
        # cpu_usage = f'{self.process.cpu_percent() / psutil.cpu_count():.2}%' or 'Unkwown'

        voice_channels = []
        text_channels = []
        for guild in b.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)
        text = len(text_channels)
        voice = len(voice_channels)

        try:
            now = datetime.utcnow()
            delta = now - datetime.fromisoformat('2019-02-04 06:15:23.496541')
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            weeks, days = divmod(days, 7)
            fmt = '{h}h:{m}m:{s}s'
            if days:
                fmt = '{d}d ' + fmt
            if weeks:
                fmt = '{w}w ' + fmt
            up_time = fmt.format(w=weeks, d=days, h=hours, m=minutes, s=seconds)
        except Exception:
            up_time = 'datetime error'

        d = f'```css\n|⌄| _  _||_  _ |_ ™\n| |(_)(_||_)(_)⎩_ v.{__version__}\n\n[Changelog]: {__notes__}```'
        tnx = '```bf\nThank you for using Modbot, please report any issues or request features in Github```'
        z = f'```py\n|⌄| _  _||_  _ |_ ™\n| |(_)(_||_)(_)⎩_ v.{__version__}```' \
            f'**Bot Instance**: {self.user} | `{self.user.id}`\n' \
            f'**Bot Author**: WebKide | `323578534763298816`\n' \
            f'**Bot Source**: <https://github.com/webkide/modbot/>\n' \
            f'**Protecting**: `{text}` text channels and `{voice}` voice channels in `{len(b.guilds)}` guild(s)\n' \
            f'**Serving**: a total of `{total_unique}` members of which `{total_online}` are actively online, ' \
            f'`{total_idle}` are chilling idly, `{total_dnd}` are busy, and `{total_offline}` are asleep\n' \
            f'**Geek Stats**: `memory_usage:.2f` MiB | `cpu_usage` CPU | `{up_time}` online\n' \
            f'◖|⌣ ‿ ⌣|◗˳♪⁎˚♫˳ Powered by `discord.py {discord.__version__} | Made with ❤`'

        try:
            e = discord.Embed(color=discord.Colour(0xed791d))
            e.url = 'http://discord.gg/HDJZnEj'
            e.set_author(name=f'{self.user} | {self.user.id}', icon_url=avy)
            e.set_footer(text=f'Powered by discord.py {discord.__version__} | Made with ❤')

            e.description = d

            e.add_field(name='<:evilmorty:540582117307056147> Bot Author',
                        value='[WebKide](https://github.com/webkide)')

            e.add_field(name='<:Heart:525716509830414347> Bot Uptime',
                        value=f'`{up_time}`')

            e.add_field(name='<:Terminal:527401285754814474> Bot Source',
                        value='[Github](https://github.com/webkide/modbot/) | [GitLab](https://gitlab.com/webkide)')

            e.add_field(name='<:zoomeyes:492155933263396865> Protecting',
                        value=f'`{len(b.guilds)}` guild(s)\n`{total_unique}` members\n'
                              f'`{text}` text channels\n`{voice}` voice channels')

            e.add_field(name='<:4stars:540582116090445825> Current Guild',
                        value=f'Position: `{join_number}`\nName: {g.name}\nDoB: {str(g.created_at)[:-16]}\n'
                              f'Owner: {g.owner.display_name}\nPrefix: `botto ` OR `@{self.user.display_name}`')

            e.add_field(name='\N{BUSTS IN SILHOUETTE} Members',
                        value=f'`{total_online}` online\n'
                              f'`{total_idle}` idle\n`{total_dnd}` dnd\n `{total_offline}` offline')

            # e.add_field(name='<:geekpengu:540582046486102027> Geek stats',
            #                      value=f'Processes: `{memory_usage:.2}` MiB | `{cpu_usage}` CPU\n'
            #                                  f'{tnx}')
            e.add_field(name='<:geekpengu:540582046486102027> Geek stats', value=f'Processes: currently unavailable')

            return await ctx.send(embed=e)

        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
            return await ctx.send(z)

    # +------------------------------------------------------------+
    # |                Bot Owner commands!                         |
    # +------------------------------------------------------------+
    @commands.command(description='Command for bot owner', hidden=True, no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def restart(self, ctx):
        """ ᗣ Restart Heroku """
        if ctx.message.author.id in (dev[1] for dev in dev_list):
            try:
                await ctx.channel.trigger_typing()
                await self.change_presence(status=discord.Status.offline)
                await ctx.send('Restarting Heroku . . .')
                self.session.close()
                await self.logout()

            except Exception as e:
                if ctx.message.guild.id == 540072370527010841:
                    tb = traceback.format_exc()
                    await ctx.send(f'```py\n{e}\n!------------>\n{tb}```')
                else:
                    pass

        else:
            if random.randint(1, 3) != 1:
                warn = '(ง •̀•́)ง fite me!'
                return await ctx.channel.send(warn, delete_after=60)
            else:
                pass

    @commands.command(description='Command for bot owner', no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def load(self, ctx, *, cog: str = None):
        """ ᗣ Load a mod plugin """
        if ctx.author.id not in (dev[1] for dev in dev_list):
            return

        else:
            cog = f'cogs.{cog}'

            if str is None:
                try:
                    await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')
                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    return

            if str is not None:
                try:
                    self.load_extension(cog)
                    try:
                        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                    except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                        return await ctx.send(f'Loaded plugin **{cog}.py** successfully')

                except Exception as e:
                    if ctx.message.guild.id == 540072370527010841:
                        await ctx.channel.trigger_typing()
                        tb = traceback.format_exc()
                        await ctx.send(f'```py\nError loading plugin: {cog}.py\n{e}\n!------------>\n{tb}```')

                    try:
                        await ctx.message.add_reaction('\N{LARGE RED CIRCLE}')
                    except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                        pass

    @commands.command(description='Command for bot owner', no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def reload(self, ctx, *, cog: str = None):
        """ ᗣ Reload any mod plugin """
        if ctx.author.id not in (dev[1] for dev in dev_list):
            return

        else:
            if str is None:
                try:
                    return await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')

                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    msg = 'sorry m8, I cannot read your mind\nwhat plugin do u want to reload?'
                    return await ctx.send(msg, delete_after=9)

            if str is not None:
                try:
                    cog = f"cogs.{cog}"
                    self.unload_extension(cog)
                    self.load_extension(cog)

                    try:
                        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

                    except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                        msg = f'Successfully reloaded cogs/{cog}.py'
                        return await ctx.send(msg, delete_after=9)

                except Exception as e:
                    if ctx.message.guild.id == 540072370527010841:
                        await ctx.channel.trigger_typing()
                        tb = traceback.format_exc()
                        await ctx.send(f'```py\nError loading plugin: {cog}.py\n{e}\n!------------>\n{tb}```')

                    try:
                        await ctx.message.add_reaction('\N{LARGE RED CIRCLE}')

                    except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                        pass

    @commands.command(description='Command for bot owner', no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def unload(self, ctx, *, cog: str = None):
        """ ᗣ Unload any mod plugin """
        if ctx.author.id not in (dev[1] for dev in dev_list):
            return

        else:
            if str is None:
                try:
                    await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')

                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    msg = 'sorry m8, I cannot read your mind\nwhat plugin do u want to unload?'
                    return await ctx.send(msg, delete_after=9)

            if str is not None:
                await ctx.channel.trigger_typing()
                try:
                    self.unload_extension(cog)
                    await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    msg = f'Plugin **cogs/{cog}.py** unloaded'
                    await ctx.send(msg, delete_after=9)


if __name__ == '__main__':
    ModBot.init()
