import discord
from discord.ext import commands
from pymongo import MongoClient
from extension import Extension

db = MongoClient('mongodb://syntony666:tony738294@ds027519.mlab.com:27519/heroku_vfz6lbdq').heroku_vfz6lbdq
keywords = db['keywords']

class Command(Extension):
    @commands.command()
    async def status(self, ctx):
        embed=discord.Embed(title="樂高", description="不要踩會痛", color=0xff2600)
        embed.set_author(name="沒有沒有名字(nononame)")
        embed.add_field(name="ping", value= str(round(self.bot.latency*1000))+' ms', inline=False)
        await ctx.send(mbed=embed)
     
    @commands.command()
    async def list(self, ctx):
        msg = '```\n'
        for x in keywords.find({"server" : str(ctx.message.guild.id)},{'_id' : 0, 'receive' : 1, 'send' : 1}):
            msg+=str(x)+'\n'
        await ctx.send(f'{msg}```')
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num:int):
        await ctx.channel.purge(limit = num+1)
        await ctx.send(f'<@{ctx.author.id}> 刪除了 {num} 則訊息')


    @commands.command()
    async def teach(self, ctx, keyword, *,msg):
        await ctx.send(keyword)
         

def setup(bot):
    bot.add_cog(Command(bot))