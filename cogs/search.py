import asyncio
import discord
import json

from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from urllib.parse import urlparse
from urllib.parse import parse_qs


class Search:
    def __init__(self, bot):
        self.bot = bot
        self.session = bot.session
        self.url = 'https://google.com/search'
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
                          '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; '
                          'InfoPath.3; .NET4.0C; .NET4.0E) chromeframe/8.0.552.224',
            'Accept-Language': 'en-us',
            'Cache-Control': 'no-cache'
            }
        self.image_headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235"
                          "7.134 Safari/537.36",
            'Accept-Language': 'en-us',
            'Cache-Control': 'no-cache'
            }
        self.reaction_emojis = ['1⃣', '2⃣', '3⃣', '4⃣']

    @commands.group(invoke_without_command=True, aliases=['g', 'find'])
    async def search(self, ctx, *, query: str=None):
        """ Search the public web for a query """

        if query is None:
            return await ctx.send('You are supposed to enter a query after the command, smh', delete_after=5)

        google_embed = False
        params = {'q': quote_plus(query), 'source': 'hp'}
        results_num = 3

        async with self.session.get(self.url, params=params, headers=self.headers) as r:
            html = await r.text()

        soup = BeautifulSoup(html, 'lxml')

        result_links = [parse_qs(urlparse(x.attrs['href'])[4])['url'][0] for x in soup.select('div.g h3.r a')[:4] if
                        '/search' not in x.attrs['href'] and not x.text == '']
        result_desc = [x.text for x in soup.select('div#ires div.g div.s span.st')[:4] if
                       '/search' not in x.text and not x.text == '']

        if soup.select('div.hp-xpdbox div._tXc'):
            google_embed = True
            embed_title = [a.text for a in soup.select('div._B5d')][0]
            try:
                embed_type = [a.text for a in soup.select('div._Pxg')][0]
            except IndexError:
                embed_type = None
            embed_details = [a.text for a in soup.select('div._tXc span')][0]
            results_num -= 1

            img = None
            try:
                img = [img.attrs.get('src') for img in soup.select('div._i8d img')][0]
            except IndexError:
                pass

        if google_embed:
            em = discord.Embed(title=embed_title, description=embed_type, color=self.bot.user_color)
            em.add_field(name="Info", value=embed_details)
            if img:
                em.set_thumbnail(url=img)

        results = "\n\n".join([f'<{link}>\n{desc}' for link, desc in list(zip(result_links, result_desc))[:results_num]])

        if google_embed:
            await ctx.send(embed=em, content=f"\n**I found {query} on the private web**\n{results}")
        else:
            await ctx.send(content=f"\n**I found {query} on the private web**\n{results}")

    @search.command(name="images", aliases=['img', 'image'])
    async def images(self, ctx, *, query: str=None):
        """ Search the public web for Images """

        if query is None:
            return await ctx.send('You are supposed to enter a query after the command, smh', delete_after=5)

        params = {'q': quote_plus(query), 'source': 'lmns', 'tbm': 'isch'}
        async with self.session.get(self.url, params=params, headers=self.image_headers) as r:
            html = await r.text()

        soup = BeautifulSoup(html, 'lxml')

        images = []
        for item in soup.select('div.rg_meta')[:4]:
            images.append(json.loads(item.text)["ou"])

        em = discord.Embed(title="Link", url=images[0])
        em.set_author(name=f"I found {query}")
        em.set_image(url=images[0])

        image_result = await ctx.send(embed=em)

        # needs more work
        for emoji in self.reaction_emojis:
            await image_result.add_reaction(emoji)

        while 1:
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in self.reaction_emojis\
                       and reaction.message == ctx.message
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await image_result.delete()
                break
            for emoji in self.reaction_emojis:
                await image_result.remove_reaction(emoji, ctx.author)

            # update the embed with a new image and link, idealy
            selected_item = self.reaction_emojis.index(str(reaction.emoji))
            em.set_image(url=images[selected_item])
            em.url = images[selected_item]
            await image_result.edit(embed=em)


def setup(bot):
    bot.add_cog(Search(bot))
