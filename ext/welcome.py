from discord.ext import commands

from core.extension import Extension
from core.util import setEmbedList, isChannelInGuild, invokedNoSubcommand


class Welcome(Extension):

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        invokedNoSubcommand(ctx)

    @welcome.command(aliases=['l', 'list'])
    async def get_list(self, ctx):
        if ctx.invoked_subcommand is None:
            welcome = self.db['config'].find_one({'server': ctx.message.guild.id})
            title = '歡迎訊息'
            description = ''
            context = {
                '通知頻道': '未設定' if welcome["welcome"]["channel"] == 0 else f'<#{welcome["welcome"]["channel"]}>',
                '通知訊息': '未設定' if welcome["welcome"]["message"] == '' else welcome["welcome"]["message"]
            }
            await ctx.send(embed=setEmbedList(title, description, context))

    @welcome.command(aliases=['c', 'channel'])
    async def set_channel(self, ctx, channelId: int):
        server = ctx.message.guild.id
        await ctx.channel.purge(limit=1)
        if isChannelInGuild(channelId, ctx.message.guild):
            self.db['config'].find_one_and_update({'server': server}, {'$set': {'welcome.channel': channelId}})
            await ctx.send(f'**{ctx.message.guild}** 的歡迎訊息通知在 <#{channelId}>')
        elif channelId == 0:
            self.db['config'].find_one_and_update({'server': server}, {'$set': {'welcome.channel': channelId}})
            await ctx.send(f'**{ctx.message.guild}** 的歡迎訊息通知已取消')
        else:
            await ctx.send(f'頻道ID輸入錯誤')

    @welcome.command(aliases=['m', 'message'])
    async def set_message(self, ctx, *, msg):
        server = ctx.message.guild.id
        await ctx.channel.purge(limit=1)
        if self.db['config'].find_one({'server': server, 'welcome.channel': 0}) is not None:
            await ctx.send(f'**!!!尚未設定歡迎訊息頻道!!!**')
        self.db['config'].find_one_and_update({'server': server}, {'$set': {'welcome.message': msg}})
        await ctx.send(f'**{ctx.message.guild}** 的歡迎訊息通知為 {msg}')


def setup(bot):
    bot.add_cog(Welcome(bot))
