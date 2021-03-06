import random
import time
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from core.extension import Extension
from core.member import Member
from core.util import get_member_rank, invoked_no_subcommand


class MemberInfo(Extension):
    @commands.command(aliases=['level'])
    async def get_level(self, ctx):
        member = ctx.author if len(ctx.message.mentions) == 0 else ctx.message.mentions[0]
        level = Member(ctx.author.id, ctx.guild.id).get_level()
        await ctx.send(f'{member.mention} 目前為等級 {level}')

    @commands.command(aliases=['exp'])
    async def get_exp(self, ctx):
        member = ctx.author if len(ctx.message.mentions) == 0 else ctx.message.mentions[0]
        member_info = Member(ctx.author.id, ctx.guild.id)
        msg_count, level, exp = member_info.get_msg_count(), member_info.get_level(), member_info.get_exp()
        await ctx.send(f'{member.mention} 目前說了 {msg_count} 句話\n' +
                       f'共獲得 {member_info.get_all_exp()} 經驗值\n' +
                       f'再獲得 {member_info.get_need_exp()} 經驗值就能升級')

    @commands.command(aliases=['info'])
    async def get_info(self, ctx):
        member = ctx.author if len(ctx.message.mentions) == 0 else ctx.message.mentions[0]
        member_info = Member(ctx.author.id, ctx.guild.id)
        embed = discord.Embed(title=member.name, color=member.color.value)
        embed.add_field(name='等級', value=member_info.get_level(), inline=False)
        embed.add_field(name='已獲得經驗', value=member_info.get_exp(), inline=True)
        embed.add_field(name='升級所需經驗值', value=member_info.get_need_exp(), inline=True)
        embed.add_field(name='已傳送對話數量', value=member_info.get_msg_count(), inline=False)
        embed.add_field(name='現金', value=member_info.get_cash(), inline=False)
        await ctx.send(embed=embed)

    @commands.group()
    async def rank(self, ctx):
        invoked_no_subcommand(ctx)

    @rank.command(aliases=['level'])
    async def get_level_rank(self, ctx):
        members = get_member_rank(ctx.guild.id, [('level', -1)])
        embed = discord.Embed(title='幹話排行', color=0xff2600)
        for x in range(5):
            member_id = members[x].get('user')
            if x >= len(members) or ctx.guild.get_member(member_id) is None:
                break
            embed_str = f'等級: {members[x].get("level")}\n已傳送對話數量: {members[x].get("msg-count")}'
            embed.add_field(name=f'__第{x + 1}名__',value='~~  ~~', inline=False)
            embed.add_field(name=ctx.guild.get_member(member_id).display_name, value=embed_str, inline=False)
        await ctx.send(embed=embed)

    @rank.command(aliases=['cash'])
    async def get_cash_rank(self, ctx):
        members = get_member_rank(ctx.guild.id, [('cash', -1)])
        embed = discord.Embed(title='富豪排行', color=0xff2600)
        for x in range(5):
            member_id = members[x].get('user')
            if x >= len(members) or ctx.guild.get_member(member_id) is None:
                break
            embed_str = f'持有現金: {members[x].get("cash")}'
            embed.add_field(name=f'__第{x + 1}名__', value='~~  ~~', inline=False)
            embed.add_field(name=ctx.guild.get_member(member_id).display_name, value=embed_str, inline=False)
        await ctx.send(embed=embed)


def message_count(member: discord.Member):
    member_info = Member(member.id, member.guild.id)
    member_info.set_msg_count(member_info.get_msg_count() + 1)
    member_info.update()


def message_exp(member: discord.Member):
    random.seed(time.process_time())
    member_info = Member(member.id, member.guild.id)
    if datetime.now() > member_info.get_msg_time() + timedelta(minutes=1):
        member_info.add_exp(random.randint(10, 30))
    member_info.update()


def setup(bot):
    bot.add_cog(MemberInfo(bot))
