import asyncio, discord, json, urllib.request, re

from discord.ext import commands


class Search:
    def __init__(self, bot):
        self.bot = bot
        #  self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
                          '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8; '
                          'InfoPath.3; .NET4.0C; .NET4.0E) chromeframe/8.0.552.224',
            'Accept-Language': 'en-us',
            'Cache-Control': 'no-cache'
            }

    @commands.command(aliases=['g', 'sp', 'startpage'])
    async def search(self, ctx, *, query: str=None):
        """ Search the public web for a query """

        if query is None:
            return await ctx.send('You are supposed to enter a query after this command, smh', delete_after=5)

        splt = query.split()[1:]
        ms = ' '.join(splt)
        regex = re.compile('<div class="g">')
        addr = urllib.request.quote(ms)
        addr = 'https://www.startpage.com/do/search?q=' + addr
        req = urllib.request.Request(addr, None, self.headers)
        response = urllib.request.urlopen(req)
        htm = response.read().decode('utf8')
        try:
            result_page = htm.split('<ol class="list-flat">')[1].split('</ol>')[0]
        except IndexError:
            return await ctx.send('oops! try later', delete_after=23)

        result_page = re.sub('<a[\s\S]*?>', '<a>', result_page).replace('<li><a>Anonymous View</a></li>', '').split('</li>')
        for m in range(len(result_page)): result_page[m] = re.sub('<[\s\S]*?>', ' ', result_page[m].replace('<br>', '\n'))
        search_result = []
        for m in result_page[:3]:
            m = html.unescape(m)
            _header, li = m.strip().split('  \n \n ')
            t = li.split(' \n \n\n \n \n ')
            if len(t) == 1:
                desc = '[**StartPage:**]'
                link = t[0]
            else:
                link, desc = t
            if link[:4] != 'http': link = 'http://' + link
            search_result.append([_header, desc, '<' + link + '>'])
        await ctx.send(search_result)

def setup(bot):
    bot.add_cog(Search(bot))

    
