"""
MIT License
Copyright (c) 2019-2021 WebKide [d.id @323578534763298816]
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

import discord, random, asyncio, aiohttp, traceback, os, re, datetime
try:
    import psutil
except ModuleNotFoundError:
    pass

from datetime import datetime
from pytz import timezone
from discord.ext import commands
from pathlib import Path

__version__ = '0.06.8'  # first int is main, second is stable, third is working release [0.00.0]
dev_list = [
    ('WebKide', 323578534763298816),
    ('Ara', 324040201225633794)
]
_token = os.getenv('TOKEN')
__notes__ = "BETA version, official stable release. \n✔ commands are available to all " \
            "members. \nᗣ commands are restricted to Mod, Admin, and Owner roles. \n" \
            "✯ commands are only for Modbot Developer. \nWe're working to fix bugs " \
            "and add more functionality, thanks for your patience."


# +------------------------------------------------------------+
# |               ModBot has its own class!                    |
# +------------------------------------------------------------+
class ModBot(commands.Bot):
    """ a moderation bot for Discord guilds """
    # +------------------------------------------------------------+
    # |             Here starts the actual bot                     |
    # +------------------------------------------------------------+
    def __init__(self, **attrs):
        self.description = f'|⌄| _  _||_  _ |_ ™\n| |(_)(_||_)(_)⎩_ v.{__version__}\n\n{__notes__}'
        self.ownerID = 323578534763298816
        super().__init__(command_prefix=commands.when_mentioned_or('botto ', '.', 'modbot '),
                         case_insensitive=True, owner_id=self.ownerID, description=self.description, **attrs)
        self.add_command(self.ping)
        self.add_command(self.about)

        self.version = __version__
        try:    self.process = psutil.Process()  # to monitor RAM and space
        except Exception:    pass

    # +------------------------------------------------------------+
    # |            Here the bot connects and loads cogs            |
    # +------------------------------------------------------------+
    async def on_connect(self):
        """ Once you see this in the logs, modbot is alive """
        print(f'│ ╔╦╗ ┌─┐ ┬─╮ ╔╗  ┌─┐ ┌┬┐™ │\n'
              f'│ ║║║ │ │ │ │ ╠╩╗ │ │  │   │\n'
              f'│ ╩ ╩ └─┘ ┴─┘ ╚═╝ └─┘  ┴   │\n'
              f'│            ᶠᵒʳ ᵈⁱˢᶜᵒʳᵈ   │\n'
              f'│                          └─→\n'
              f'├ ✔ Loaded Modbot: main.py')

    # +------------------------------------------------------------+
    # |            If everything went well...                      |
    # +------------------------------------------------------------+
    async def on_ready(self):
        """ If everything is fine, then... """
        print('│                          ┌─→\n'
              '│  (∩｀-´)⊃━✧｀｀｀｀｀｀ ♡  │\n'
              '│                          │\n'
              '│ Your instance of ModBot  │\n'
              '│ is ready to watch over   │\n'
              '│ your Discord guild and   │\n'
              '│ its active members!      │\n'
              '│                          │\n'
              '├──────────────────────────┤\n'
              f'  ID: {self.user.id}\n'
              f'  Logged as: {self.user}\n'
              f'  Monitoring: {self.guild.name}\n'
              '├──────────────────────────┤\n'
              '│ ██████████████████░░ 95% │\n'
              '└──────────────────────────┘\n')

        status = "@Mod help | Spotify"
        await self.change_presence(status=discord.Status.online,
                                   activity=discord.Activity(type=discord.ActivityType.listening,
                                                             name=status))

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
        try:    memory_usage = self.process.memory_full_info().uss / 1024 ** 2 or '0.0'
        except Exception:    pass
        try:    cpu_usage = f'{self.process.cpu_percent() / psutil.cpu_count():.2}%' or 'Unkwown'
        except Exception:    pass
        
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

            try:    e.add_field(name='<:geekpengu:540582046486102027> Geek stats',
                                value=f'Processes: `{memory_usage:.2}` MiB | `{cpu_usage}` CPU\n{tnx}')
            except Exception:    pass
            
            e.add_field(name='<:geekpengu:540582046486102027> Geek stats', value=f'Processes: currently unavailable')

            return await ctx.send(embed=e)

        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
            return await ctx.send(z)

# +------------------------------------------------------------+
# |             Here we get the bot's TOKEN                    |
# +------------------------------------------------------------+
def main(bot):
    """ ModBot, get ready! """
    bot = ModBot()
    bot.run(_token)
    
    
if __name__ == '__main__':
    ModBot.main()

