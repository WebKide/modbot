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

import asyncio
import traceback
import textwrap
import io

from contextlib import redirect_stdout
from discord.ext import commands

dev_list = [
    ('WebKide', 323578534763298816)
]


class Evaluate:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    @staticmethod
    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @staticmethod
    def get_syntax_error(e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(name='evaluate', aliases=['eval', 'ev'], hidden=True)
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def _evaluate(self, ctx, *, body: str):
        """ ✯ Evaluate some python code """
        if ctx.author.id not in (dev[1] for dev in dev_list):
            return

        else:
            env = {
                'bot': self.bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                '_': self._last_result
            }

            env.update(globals())

            body = self.cleanup_code(body)
            stdout = io.StringIO()

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```', delete_after=369)
                await ctx.send(f'```py\n{e}```', delete_after=369)
            else:
                value = stdout.getvalue()

                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(name='pyval', hidden=True)
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def _pyval(self, ctx, *, body: str):
        """ Evaluates a code """
        if ctx.author.id not in (dev[1] for dev in dev_list):
            return

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        await self.edit_to_codeblock(ctx, body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await self.bot.say(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await self.bot.say(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await self.bot.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await self.bot.say(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await self.bot.say(f'```py\n{value}{ret}\n```')

    async def edit_to_codeblock(self, ctx, body):
        msg = f'```py\n{body}\n```'
        await self.bot.message.edit(content=msg)

    def cleanup_code(self, content):
        """ Automatically removes code blocks from the code """
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'

        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    @commands.command(description='Terminal access', name='modbot$', hidden=True, no_pm=True)
    @commands.has_any_role('Admin', 'Mod', 'Moderator', 'Owner')
    async def shell_access(self, ctx, *, cmd: str = None):
        """ ✯ Access commandline from text_channel """
        if ctx.author.id not in (dev[1] for dev in dev_list):
            return
        try:
            if cmd is None:
                return

            if cmd is not None:
                process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
                stdout, stderr = await process.communicate()

                try:
                    if stdout:
                        await ctx.send(f'`{cmd}`\n```{stdout.decode().strip()}```')
                    elif stderr:
                        await ctx.send(f'`{cmd}`\n```{stderr.decode().strip()}```')
                    else:
                        await ctx.send(f'`{cmd}` produced no output')

                except Exception as e:
                    await ctx.send(f'Unable to send output\n```py\n{e}```', delete_after=15.0)
        except Exception as e:
            return await ctx.send(f'```py\n{e}```')


def setup(bot):
    bot.add_cog(Evaluate(bot))
