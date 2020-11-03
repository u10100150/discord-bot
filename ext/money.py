import random
import time
from datetime import datetime

from discord.ext import commands

from core.extension import Extension
from core.member import Member


class Money(Extension):

    @commands.command()
    async def dice(self, ctx, num):
        member = Member(ctx.author.id, ctx.author.id)
        random.seed(time.clock())
        if member.get_cash() < 100:
            dice = random.randint(1, 6)
            if dice == num:
                member.set_cash(member.get_cash() + 100)
                await ctx.send(f'你骰到{dice} 獲得現金 100 你還有現金{member.get_cash()}')
            else:
                member.set_cash(member.get_cash() - 100)
                await ctx.send(f'你骰到{dice} 損失現金 100， 你還有現金 {member.get_cash()}')

    @commands.command(aliases=['daily'])
    async def daily_cash(self, ctx):
        member_info = Member(ctx.guild.id, ctx.author.id)
        if datetime.now() > member_info.get_daily_cash_time():
            member_info.set_cash(member_info.get_cash() + member_info.get_daily_cash())
            member_info.set_daily_cash_now_time()
            await ctx.send(f'這是你今天的薪資 {member_info.get_daily_cash()}')
        else:
            time_sec = (member_info.get_daily_cash_time() - datetime.now()).seconds
            time_parser = f'{time_sec // 3600}小時' if time_sec > 3600 else f'{time_sec // 60}分鐘'
            await ctx.send(f'你今天領過了，你還要等 {time_parser} 才能再領')

    @commands.command(aliases=['cash'])
    async def get_cash_command(self, ctx):
        member_info = Member(ctx.guild.id, ctx.author.id)
        await ctx.send(f'你現在有現金 {member_info.get_cash()} 元')


def setup(bot):
    bot.add_cog(Money(bot))