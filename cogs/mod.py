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

from discord.ext import commands


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.mod_color = discord.Colour(0x7289da)  # Blurple
        self.user_color = discord.Colour(0xed791d)  # Orange

    async def format_mod_embed(self, ctx, user, success, method):
        """ Helper func to format an embed to prevent extra code """
        e = discord.Embed(color=self.mod_color)
        e.set_author(name=method.title(), icon_url=user.avatar_url)
        e.set_footer(text=f'User ID: {user.id}')
        if success:
            if method == 'ban':
                e.description = f'{user} was just {method}ned.'
            else:
                e.description = f'{user} was just {method}ed.'
        else:
            e.description = f"You do not have the permissions to {method} users."

        return e

    # +------------------------------------------------------------+
    # |                    KICK THEM OUT!                          |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def kick(self, ctx, member: discord.Member, *, reason='Please write a reason!'):
        """ ᗣ Kick someone from the server """
        if not member:
            return await ctx.send('ヽ( ･∀･)ﾉ┌┛Σ(ノ `Д´)ノ')

        if not reason:
            return await ctx.send(f'Gimme a good reason to ヽ( ･∀･)ﾉ┌┛Σ(ノ `Д´)ノ {member}')

        else:
            try:
                await ctx.guild.kick(member, reason=reason)
            except:
                success = False
            else:
                success = True

            e = await self.format_mod_embed(ctx, member, success, 'kick', reason)
            await ctx.send(embed=e)

    # +------------------------------------------------------------+
    # |                  BAN HAMMER!                               |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def ban(self, ctx, member: discord.Member, *, reason='Please write a reason!'):
        """ ᗣ Ban someone from the server """
        if not member:
            return await ctx.send('(•̆ꈊ•̆;;)▁▂▃▅▆▓▒░')

        if not reason:
            return await ctx.send(f'Gimme a good reason to (•̆ꈊ•̆;;)▁▂▃▅▆▓▒░ {member}')

        else:
            try:
                await ctx.guild.ban(member, reason=reason)
            except:
                success = False
            else:
                success = True

            e = await self.format_mod_embed(ctx, member, success, 'ban', reason)
            await ctx.send(embed=e)

    # +------------------------------------------------------------+
    # |                    REMOVE A BAN!                           |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def unban(self, ctx, name_or_id, *, reason=None):
        """ ᗣ Unban someone from the server """
        if not name_or_id:
            return await ctx.send('、ヽ｀、ヽ｀个o(･･｡)｀ヽ、｀ヽ、')

        if not reason:
            return await ctx.send(f'Gimme a good reason to 、ヽ｀、ヽ｀个o(･･｡)｀ヽ、｀ヽ、 {name_or_id}')

        else:
            ban = await ctx.get_ban(name_or_id)

            try:
                await ctx.guild.unban(ban.user, reason=reason)
            except:
                success = False
            else:
                success = True

            e = await self.format_mod_embed(ctx, ban.user, success, 'unban')
            await ctx.send(embed=e)

    # +------------------------------------------------------------+
    # |              BAN PEOPLE NOT IN SERVER!                     |
    # +------------------------------------------------------------+
    @commands.command(description='Ban using ID if they are no longer in server', no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def hackban(self, ctx, userid, *, reason='Please write a reason!'):
        """ ᗣ Ban user, even if not in server """
        if not userid:
            return await ctx.send('To use this command, use User ID, and give a reason for ban.')

        if not reason:
            return await ctx.send(f'Gimme a good reason to (•̆ꈊ•̆;;)▁▂▃▅▆▓▒░ {member}')

        else:
            try:
                userid = int(userid)
            except:
                return await ctx.send(f'`{userid}` is an invalid Discord ID!', delete_after=5)

            try:
                await ctx.guild.ban(discord.Object(userid), reason=reason)
            except:
                success = False
            else:
                success = True

            if success:
                async for entry in ctx.guild.audit_logs(limit=1, user=ctx.guild.me, action=discord.AuditLogAction.ban):
                    e = await self.format_mod_embed(ctx, entry.target, success, 'hackban')
            else:
                e = await self.format_mod_embed(ctx, userid, success, 'hackban')
            try:
                return await ctx.send(embed=e)
            except discord.Forbidden:
                pass

    # +------------------------------------------------------------+
    # |              CLEAN THAT CHAT!                              |
    # +------------------------------------------------------------+
    @commands.command(aliases=['del', 'p', 'prune'], bulk=True, no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def purge(self, ctx, limit: int):
        """ ᗣ Clean messages from chat """
        if not limit:
            return await ctx.send('Enter the number of messages you want me to delete.')

        if limit < 99:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit)
            succ = f'₍₍◝(°꒳°)◜₎₎ Successfully deleted {len(deleted)} message(s)'
            await ctx.channel.send(succ, delete_after=6)

        else:
            await ctx.send(f'Cannot delete `{limit}`, try with less than 100.', delete_after=23)

    # +------------------------------------------------------------+
    # |             CLEAN CHAT FROM BOT MESSAGES!                  |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def clean(self, ctx, limit: int = 15):
        """ ᗣ Clean a only Bot's messages """
        if not limit:
            return await ctx.send('Enter the number of messages you want me to delete. ˛˛(⊙﹏⊙ ) ̉ ̉')

        if limit < 99:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=limit, check=lambda m: m.author == self.bot.user)
            await ctx.channel.send(f'Successfully deleted {len(deleted)} message(s)', delete_after=5)

        else:
            await ctx.send(f'Cannot delete `{limit}`, try fewer messages.')

    # +------------------------------------------------------------+
    # |              GET A LIST OF BANNED USERS!                   |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def bans(self, ctx):
        """ ᗣ See a list of banned users """
        try:
            bans = await ctx.guild.bans()
        except:
            return await ctx.send("You don't have the perms to see bans. (｡◝‿◜｡)")
        e = discord.Embed(color=self.mod_color)
        e.set_author(name=f'List of Banned Members ({len(bans)}):', icon_url=ctx.guild.icon_url)        
        result = ',\n'.join(["[" + (str(b.user.id) + "] " + str(b.user)) for b in bans])
        if len(result) < 1990:
            total = result
        else:
            total = result[:1990]
            e.set_footer(text=f'Too many bans to show here!')
        e.description = f'```bf\n{total}```'
        await ctx.send(embed=e)

    # +------------------------------------------------------------+
    # |         CHECK THE REASON FOR THAT BAN!                     |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def baninfo(self, ctx, *, name_or_id):
        """ ᗣ Check the reason of a ban """
        ban = await ctx.get_ban(name_or_id)
        e = discord.Embed(color=self.mod_color)
        e.set_author(name=str(ban.user), icon_url=ban.user.avatar_url)
        e.add_field(name='Reason', value=ban.reason or 'None')
        e.set_thumbnail(url=ban.user.avatar_url)
        e.set_footer(text=f'User ID: {ban.user.id}')
        await ctx.send(embed=e)

    # +------------------------------------------------------------+
    # |                GIVE THEM ROLES!                            |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def addrole(self, ctx, member: discord.Member, *, rolename: str = None):
        """
        ᗣ Add a role to someone else
        Usage:
        addrole @name Listener
        """
        if not member and rolename is None:
            return await ctx.send('To whom do I add which role? ╰(⇀ᗣ↼‶)╯')

        if rolename is not None:
            role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
            if not role:
                return await ctx.send('That role does not exist. ╰(⇀ᗣ↼‶)╯')
            try:
                await member.add_roles(role)
                await ctx.message.delete()
                await ctx.send(f'Added: **`{role.name}`** role to *{member.display_name}*')
            except:
                await ctx.send("I don't have the perms to add that role. ╰(⇀ᗣ↼‶)╯")

        else:
            return await ctx.send('Please mention the member and role to give them. ╰(⇀ᗣ↼‶)╯')

    # +------------------------------------------------------------+
    # |                 REMOVE THAT ROLE!                          |
    # +------------------------------------------------------------+
    @commands.command(no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Journalist', 'Owner')
    async def removerole(self, ctx, member: discord.Member, *, rolename: str):
        """ ᗣ Remove a role from someone """
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist. ╰(⇀ᗣ↼‶)╯')
        try:
            await member.remove_roles(role)
            await ctx.message.delete()
            await ctx.send(f'Removed: `{role.name}` role from *{member.display_name}*')
        except:
            await ctx.send("I don't have the perms to remove that role. ╰(⇀ᗣ↼‶)╯")


def setup(bot):
    bot.add_cog(Moderation(bot))
