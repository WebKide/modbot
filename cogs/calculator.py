from __future__ import division
import discord
import math
import operator

from discord.ext import commands
from pyparsing import (Literal,CaselessLiteral,Word,Combine,Group,Optional,
                    ZeroOrMore,Forward,nums,alphas,oneOf)

__author__='Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__ = """http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
"""
__note__ = """
This is a re-wrap of Paul McGuire's fourFn.py as a class, so it can 
be used easily in other places of the code. Most of the work wad done 
by corpnewt, all I did was clean it and create the results in embeds.
Also, the messages are deleted after, except for the correct answer.
"""


class NumericStringParserForPython3(object):
    """
    Most of this code comes from the fourFn.py pyparsing example

    """
    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])
    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0]=='-':
            self.exprStack.append('unary -')
    def __init__(self):
        """
        Please use any of the following symbols:
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        """
        point = Literal(".")
        e     = CaselessLiteral("E")
        fnumber = Combine(Word("+-"+nums, nums) +
                        Optional(point + Optional(Word(nums))) +
                        Optional(e + Word("+-"+nums, nums)))
        ident = Word(alphas, alphas+nums+"_$")
        plus  = Literal("+")
        minus = Literal("-")
        mult  = Literal("*")
        div   = Literal("/")
        lpar  = Literal("(").suppress()
        rpar  = Literal(")").suppress()
        addop  = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi    = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                (pi|e|fnumber|ident+lpar+expr+rpar).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar+expr+rpar)
               ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        # addop_term = (addop + term).setParseAction(self.pushFirst)
        # general_term = term + ZeroOrMore(addop_term) | OneOrMore(addop_term)
        # expr <<  general_term
        self.bnf = expr
        # this will map operator symbols to their corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {
                "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv,
                "^" : operator.pow }
        self.fn  = {
                "sin" : math.sin,
                "cos" : math.cos,
                "tan" : math.tan,
                "abs" : abs,
                "trunc" : lambda a: int(a),
                "round" : round,
                "sgn" : lambda a: abs(a)>epsilon and cmp(a,0) or 0}
    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)
    def eval(self,num_string,parseAll=True):
        self.exprStack=[]
        results=self.bnf.parseString(num_string,parseAll)
        val=self.evaluateStack(self.exprStack[:])
        return val

class Calculator:

    # Init with the bot reference, and a reference to the settings var
    def __init__(self, bot):
        self.bot = bot
        self.nsp=NumericStringParserForPython3()
        self.user_color = discord.Colour(0xed791d) ## orange
        self.mod_color = discord.Colour(0x7289da) ## blurple

    @commands.command(description='Scientific calculator', aliases=['calculate', 'maths'])
    async def calc(self, ctx, *, formula = None):
        """ ✔ Do some math
        thanks to Paul McGuire's fourFn.py. """
        person = ctx.message.author
        formula = formula.replace('x', '*').replace(' minus ', '-').replace(' plus ', '+').replace(' into ', '/') \
                         .replace(' sub ', '-').replace(' pi ', 'PI').replace(' divide ', '/').replace(' multiply ', '*') \
                         .replace(' add ', '+').replace(' div ', '/').replace(' multi ', '*').replace(' mul ', '*') \
                         .replace('π', 'PI').replace('÷', '/')

        if formula == None:
            # How can it calculate an empty message? Reee!
            msg = f'\u200BUsage: `{ctx.prefix}{ctx.invoked_with} [any maths formula]`'
            e = discord.Embed(color=self.user_color)
            e.description = msg

            try:
                await ctx.send(embed=e, delete_after=23)
            except discord.HTTPException:
                await ctx.send(msg, delete_after=23)
            return

        try:
            answer=self.nsp.eval(formula)
        except:
            # If there's a problem in the input, show examples
            msg = f'\N{THINKING FACE} wrong `{formula}` input.\n\nTry any of these:'
            e = discord.Embed(color=self.user_color)
            e.description = f'\u200B{msg}'
            e.add_field(name='multiply', value='`2 * 3 x 5 multiply 7`')
            e.add_field(name='divide', value='`91 / 5 divide 3 into 2 ÷ 4`')
            e.add_field(name='add', value='`1 + 4 plus 8 add 23`')
            e.add_field(name='substract', value='`91 - 35 minus 3 sub 12`')
            e.add_field(name='exponential', value="`7 ^ 5`")
            e.add_field(name='Supported formulas', 
                        value='```py\nround((cos(45) + (3+7^2)*2 + tan(369.18)) / π - 3)```')

            try:
                await ctx.send(embed=e, delete_after=23)
            except discord.HTTPException:
                error = f'\N{THINKING FACE} wrong `{formula}` input.\n\n ' \
                        f'Try any of these:```py\nround((cos(45) + (3+7^2)*2 + tan(369.18)) / π - 3)```'
                await ctx.send(error, delete_after=23)
            return

        # Correct input prints correct answer
        distance = self.bot or self.bot.message
        duration = f'Calculated in {distance.ws.latency * 1000:.2f} ms'
        success = round(answer, 2)

        e = discord.Embed(color=self.user_color)
        e.add_field(name='Input:', value=f'```py\n{formula}```', inline=True)
        e.add_field(name='Result:', value=f'```css\n{success}```', inline=True)
        e.set_footer(text=duration)

        try:
            await ctx.send(embed=e)
        except discord.Forbidden:  # FORBIDDEN (status code: 403): Missing Permissions
            await ctx.send(f'```rust\n>Input: {formula}\nResult: {success}```')


def setup(bot):
    bot.add_cog(Calculator(bot))
