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

import asyncio
import json
import datetime
import discord
import textwrap
import time
import random


chosen_guilds = [
    ('ssevana', 328341202103435264),
    ('Modbot Dev Support', 540072370527010841)
]
bot_channel = 375179500604096512
rolename1 = 'Listener'
rolename2 = 'Member'


class OnJoinLeave:
    """
    Automatic message deletion, blaclisted words, server invites
    """

    def __init__(self, bot):
        self.bot = bot
        self.user_color = discord.Colour(0xed791d)

    # +------------------------------------------------------------+
    # |          Modbot sends dm to guild owner                    |
    # +------------------------------------------------------------+
    async def on_guild_join(self, guild):
        """ Bot sends a couple of messages upon joining """
        bot = self.bot
        msg = textwrap.dedent(f"""Hello {guild.owner.display_name} :)
        Thanks for inviting me to your guild **{guild.name}**!
        If you did not invite me, then someone with enough permissions did.
        Regardless, it is good to be part of {guild.name}.\n
        For a list of my commands, please use:
        ```css\n.help```*OR:*```{bot.user} help```""")
        mes = f'{guild.owner.display_name} | {guild.owner.id} invited me to ' \
              f'{guild.name} | {guild.id}'
        try:
            await guild.owner.send(msg)
        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
            await bot.get_channel(546770598177800212).send(mes)

        # We also send it to log, so that it is easy to leave guild if required
        try:
            await self.bot.get_channel(546770598177800212).send(mes)
        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
            pass

    async def on_guild_remove(self, guild):
        """ When the bot is removed it messages """
        support = '<https://discord.gg/HDJZnEj>'
        botid = self.bot.user.id
        bot_invite = f'<https://discordapp.com/oauth2/authorize?client_id={botid}&scope=bot&permissions=8>'
        msg = textwrap.dedent(f"""I'm really sorry that you weren't pleased by *me* in {guild.name}.
        ```Please let me know how I can improve.```
            To send any feedback, just reply in here, and I'll let my devs know 
        so that they can fix me.
            If you want to join my support server to interact with my devs or 
        other users, please click the invite below.\n
            To invite me again, just click my bot invite link: {bot_invite}
            And if you wish to follow my updates, please join: {support}""")
        try:
            await guild.owner.send(msg)

        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
            pass

    # +------------------------------------------------------------+
    # |     New member receives dm upon joining guild              |
    # +------------------------------------------------------------+
    async def on_member_join(self, member):
        bot = self.bot
        guild = member.guild

        if guild.id not in (x[1] for x in chosen_guilds):
            return

        if guild.id == 328341202103435264:  # ssevana
            u = [s.name for s in bot.guilds]

            # +------------------------------------------------------------+
            # |           New member receives auto role                    |
            # +------------------------------------------------------------+
            role = discord.utils.find(lambda m: rolename1.lower() in m.name.lower(), member.guild.roles)
            try:
                await bot.get_channel(358429353966698500).send(f'Hi **{member.mention}** '
                                                               f'\N{WAVING HAND SIGN}​ | `{member.id}`')
                await member.add_roles(role)
                await asyncio.sleep(369)
                await bot.get_channel(358429353966698500).send(f'**​`{rolename1}​`** role added '
                                                               f'to: *{member.display_name}*')

            except Exception as e:
                await bot.get_channel(bot_channel).send(f'yo, need perms to add {rolename1} role '
                                                        f'to {member.mention}\n{e}', delete_after=69)

        # +------------------------------------------------------------+
        # |      Modbot Development Support                            |
        # +------------------------------------------------------------+
        if guild.id == 540072370527010841:
            try:
                await bot.get_channel(540072370979864577).send(f'Valar dohaeris **{member.mention}** '
                                                               f'\N{WAVING HAND SIGN}​\n`{member.id}`')
            except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                pass

            # +------------------------------------------------------------+
            # |           New member receives auto role                    |
            # +------------------------------------------------------------+
            role = discord.utils.find(lambda m: rolename2.lower() in m.name.lower(), member.guild.roles)
            try:
                await bot.get_channel(540072370979864577).send(f'Hi **{member.mention}** '
                                                               f'\N{WAVING HAND SIGN}​ | `{member.id}`')
                await member.add_roles(role)
                await asyncio.sleep(369)
                await bot.get_channel(540072370979864577).send(f'**​`{rolename2}​`** role added '
                                                               f'to: *{member.display_name}*')

            except Exception as e:
                await bot.get_channel(bot_channel).send(f'yo, need perms to add {rolename2} role '
                                                        f'to {member.mention}\n{e}', delete_after=69)

    # +------------------------------------------------------------+
    # |      When member leaves or is kicked/banned                |
    # +------------------------------------------------------------+
    async def on_member_remove(self, member):
        """ Auto message when a member leaves """
        bot = self.bot
        g = member.guild

        if g.id not in (x[1] for x in chosen_guilds):
            return

        # +------------------------------------------------------------+
        # |      ssevana                                               |
        # +------------------------------------------------------------+
        if g.id == 328341202103435264:  # ssevana
            try:
                avy = member.avatar_url
            except discord.Forbidden:
                avy = 'https://cdn.discordapp.com/embed/avatars/0.png'

            try:
                fooid = g.id
                foo = g.name
            except discord.Forbidden:
                fooid = 'guild_id'
                foo = 'guild_name'

            try:
                gav = g.icon_url
            except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                gav = 'https://cdn.discordapp.com/embed/avatars/0.png'

            e = discord.Embed(colour = discord.Colour(0xed791d)) # purple 0x423098
            e.description = f'Another one bites the dust...'
            e.set_author(name=f'Guild: {foo} | {fooid}', icon_url=gav)
            e.set_thumbnail(url=avy)
            e.timestamp = datetime.datetime.utcnow()
            e.set_footer(text=f'{member.display_name} | {member.id}', icon_url=avy)
            
            await bot.get_channel(bot_channel).send(embed=e) # Temporary channel for testing purposes only! status

            try:
                await bot.get_channel(358429353966698500).send(f'Bye **{member.mention}** '
                                                            f'\N{WAVING HAND SIGN}​ | `{member.id}`')
            except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                pass

        # +------------------------------------------------------------+
        # |      Modbot Development Support                            |
        # +------------------------------------------------------------+
        if member.guild.id == 540072370527010841:
            try:
                await bot.get_channel(540072370979864577).send(f'*For the night is long, and full of terrors...*\n'
                                                               f'Valar morghulis **{member.display_name}** '
                                                               f'| `{member.id}`')
            except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                pass


def setup(bot):
    bot.add_cog(OnJoinLeave(bot))
