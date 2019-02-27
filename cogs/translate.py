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

import traceback
import discord

from discord.ext import commands
from mtranslate import translate


dev_list = [
    ('WebKide', 323578534763298816)
]


conv = {
    "ab": "Abkhaz",
    "aa": "Afar",
    "af": "Afrikaans",
    "ak": "Akan",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "an": "Aragonese",
    "hy": "Armenian",
    "as": "Assamese",
    "av": "Avaric",
    "ae": "Avestan",
    "ay": "Aymara",
    "az": "Azerbaijani",
    "bm": "Bambara",
    "ba": "Bashkir",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bh": "Bihari",
    "bi": "Bislama",
    "bs": "Bosnian",
    "br": "Breton",
    "bg": "Bulgarian",
    "my": "Burmese",
    "ca": "Catalan",
    "ch": "Chamorro",
    "ce": "Chechen",
    "ny": "Nyanja",
    "zh": "Chinese",
    "cv": "Chuvash",
    "kw": "Cornish",
    "co": "Corsican",
    "cr": "Cree",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "dv": "Divehi",
    "nl": "Dutch",
    "dz": "Dzongkha",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "ee": "Ewe",
    "fo": "Faroese",
    "fj": "Fijian",
    "fi": "Finnish",
    "fr": "French",
    "ff": "Fula",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gn": "Guarani",
    "gu": "Gujarati",
    "ht": "Haitian",
    "ha": "Hausa",
    "he": "Hebrew",
    "hz": "Herero",
    "hi": "Hindi",
    "ho": "Hiri-Motu",
    "hu": "Hungarian",
    "ia": "Interlingua",
    "id": "Indonesian",
    "ie": "Interlingue",
    "ga": "Irish",
    "ig": "Igbo",
    "ik": "Inupiaq",
    "io": "Ido",
    "is": "Icelandic",
    "it": "Italian",
    "iu": "Inuktitut",
    "ja": "Japanese",
    "jv": "Javanese",
    "kl": "Kalaallisut",
    "kn": "Kannada",
    "kr": "Kanuri",
    "ks": "Kashmiri",
    "kk": "Kazakh",
    "km": "Khmer",
    "ki": "Kikuyu",
    "rw": "Kinyarwanda",
    "ky": "Kyrgyz",
    "kv": "Komi",
    "kg": "Kongo",
    "ko": "Korean",
    "ku": "Kurdish",
    "kj": "Kwanyama",
    "la": "Latin",
    "lb": "Luxembourgish",
    "lg": "Luganda",
    "li": "Limburgish",
    "ln": "Lingala",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lu": "Luba-Katanga",
    "lv": "Latvian",
    "gv": "Manx",
    "mk": "Macedonian",
    "mg": "Malagasy",
    "ms": "Malay",
    "ml": "Malayalam",
    "mt": "Maltese",
    "mi": "M\u0101ori",
    "mr": "Marathi",
    "mh": "Marshallese",
    "mn": "Mongolian",
    "na": "Nauru",
    "nv": "Navajo",
    "nb": "Norwegian Bokm\u00e5l",
    "nd": "North-Ndebele",
    "ne": "Nepali",
    "ng": "Ndonga",
    "nn": "Norwegian-Nynorsk",
    "no": "Norwegian",
    "ii": "Nuosu",
    "nr": "South-Ndebele",
    "oc": "Occitan",
    "oj": "Ojibwe",
    "cu": "Old-Church-Slavonic",
    "om": "Oromo",
    "or": "Oriya",
    "os": "Ossetian",
    "pa": "Panjabi",
    "pi": "P\u0101li",
    "fa": "Persian",
    "pl": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "qu": "Quechua",
    "rm": "Romansh",
    "rn": "Kirundi",
    "ro": "Romanian",
    "ru": "Russian",
    "sa": "Sanskrit",
    "sc": "Sardinian",
    "sd": "Sindhi",
    "se": "Northern-Sami",
    "sm": "Samoan",
    "sg": "Sango",
    "sr": "Serbian",
    "gd": "Scottish-Gaelic",
    "sn": "Shona",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovene",
    "so": "Somali",
    "st": "Southern-Sotho",
    "es": "Spanish",
    "su": "Sundanese",
    "sw": "Swahili",
    "ss": "Swati",
    "sv": "Swedish",
    "ta": "Tamil",
    "te": "Telugu",
    "tg": "Tajik",
    "th": "Thai",
    "ti": "Tigrinya",
    "bo": "Tibetan",
    "tk": "Turkmen",
    "tl": "Tagalog",
    "tn": "Tswana",
    "to": "Tonga",
    "tr": "Turkish",
    "ts": "Tsonga",
    "tt": "Tatar",
    "tw": "Twi",
    "ty": "Tahitian",
    "ug": "Uighur",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "ve": "Venda",
    "vi": "Vietnamese",
    "vo": "Volapuk",
    "wa": "Walloon",
    "cy": "Welsh",
    "wo": "Wolof",
    "fy": "Western-Frisian",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "za": "Zhuang",
    "zu": "Zulu"
}

class Translate:
    """
    Cog to translate text from any available language
    """
    def __init__(self, bot):
        self.bot = bot
        self.user_color = discord.Colour(0xed791d) ## orange
        self.mod_color = discord.Colour(0x7289da) ## blurple


    @commands.group(description='Command to translate across languages', aliases=['tr'],  invoke_without_command=True)
    async def translate(self, ctx, lang: str = None, *, text: str = None):
        """
        ✔ Translate text between languages

        Use subcommand to show short list of languages:
        translate langs
        """
        available = ', '.join(conv.values())
        languages = 'Albanian, Arabic, Aymara, Belarusian, Bulgarian, Catalan, Chinese, Croatian, Czech, ' \
                    'Danish, Dutch, English, Estonian, Fijian, Finnish, French, Georgian, German, Greek, ' \
                    'Hebrew, Hindi, Irish, Icelandic, Italian, Japanese, Kannada, Kashmiri, Korean, Latin, ' \
                    'Lithuanian, Malayalam, Marathi, Norwegian, Panjabi, Persian, Polish, Portuguese, ' \
                    'Quechua, Romanian, Russian, Sanskrit, Scottish-Gaelic, Spanish, Swahili, Swedish, ' \
                    'Tamil, Telugu, Tagalog, Turkish, Urdu, Welsh, Yiddish, Zulu \n\nFor full list: \n' \
                    'https://github.com/WebKide/modbot/data/langs.json'
        m = f'{ctx.message.author.display_name} | {ctx.message.author.id}'
        msg = f'**Usage:** {ctx.prefix}{ctx.invoked_with} <language_from_list> <message>\n\n```bf\n{languages}```'
        distance = self.bot or self.bot.message
        duration = f'Translated in {distance.ws.latency * 990:.2f} ms'

        try:
            em = discord.Embed(color=self.mod_color)
            em.set_author(name='Available Languages:', icon_url=ctx.message.author.avatar_url),
            em.description = f'```bf\n{available}```'
            em.set_footer(text=duration, icon_url='https://i.imgur.com/yeHFKgl.png')

            if lang in conv:
                t = f'{translate(text, lang)}'
                e = discord.Embed(color=self.user_color)
                e.set_author(name=m, icon_url=ctx.message.author.avatar_url),
                e.add_field(name='Original', value=f'*```css\n{text}```*', inline=False)
                e.add_field(name='Translation', value=f'```css\n{t}```', inline=False)
                e.set_footer(text=duration, icon_url='https://i.imgur.com/yeHFKgl.png')
                try:
                    await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    pass
                return await ctx.send(embed=e)

            lang = dict(zip(conv.values(), conv.keys())).get(lang.lower().title())
            if lang:
                tn = f'{translate(text, lang)}'
                em = discord.Embed(color=self.user_color)
                em.set_author(name=m, icon_url=ctx.message.author.avatar_url),
                em.add_field(name='Original', value=f'*```css\n{text}```*', inline=False)
                em.add_field(name='Translation', value=f'```css\n{tn}```', inline=False)
                em.set_footer(text=duration, icon_url='https://i.imgur.com/yeHFKgl.png')
                try:
                    await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    pass
                await ctx.send(embed=em)

            else:
                # await ctx.send(f'​`Language not available.​`\n\n{traceback.format_exc()}', delete_after=69)
                await ctx.send(msg, delete_after=23)

        except discord.Forbidden:
            if lang in conv:
                trans = f'{ctx.message.author.mention} | *{translate(text, lang)}*'
                return await ctx.send(trans)

            lang = dict(zip(conv.values(), conv.keys())).get(lang.lower().title())
            if lang:
                trans = f'{ctx.message.author.mention} | *{translate(text, lang)}*'
                await ctx.send(trans)
                try:
                    await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    pass

            else:
                # await ctx.send(f'​`Language not available.​`\n\n{traceback.format_exc()}', delete_after=69)
                await ctx.send(msg, delete_after=23)
                try:
                    await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')
                except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
                    pass

    @translate.command()
    async def langs(self, ctx):
        """ ✔ List available languages """
        available = ', '.join(conv.values())
        foo = 'Full list in https://github.com/WebKide/modbot/data/langs.json'

        em = discord.Embed(color=discord.Color.blue())
        em.set_author(name='Available Languages:', icon_url=ctx.message.author.avatar_url),
        em.description = f'```bf\n{available}```'
        em.set_footer(text=foo, icon_url='https://i.imgur.com/yeHFKgl.png')

        try:
            await ctx.send(embed=em, delete_after=123)

        except discord.Forbidden:
            msg = f'Available languages:\n```bf\n{available}```\n{foo}'
            await ctx.send(msg, delete_after=123)


def setup(bot):
    bot.add_cog(Translate(bot))
