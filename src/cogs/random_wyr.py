import discord
import asyncio

from discord.ext import commands
from discord.errors import Forbidden

from src.database.catbot_database import CatbotDatabase
from src.operational.rwyr_template_applier import RWYRTemplateApplier
from src.common.common_publisher_cog import CommonPublisherCog

class RandomWyr(CommonPublisherCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.rwyr_template_applier = RWYRTemplateApplier()

    async def loop_operation(self, guild, channel):
        random_wyr = self.rwyr_template_applier.generate_random_wyr()
        msg = await channel.send(random_wyr)
        await msg.add_reaction("\U0001F1E6")
        await msg.add_reaction("\U0001F171")

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def random_wyr(self, ctx):
        random_wyr = self.rwyr_template_applier.generate_random_wyr()
        msg = await ctx.send(random_wyr)
        await msg.add_reaction("\U0001F1E6")
        await msg.add_reaction("\U0001F171")

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def rwyr_spawn(self, ctx, channel, await_time):
        await self.start_spawn(ctx, 'randomwyr', channel, await_time)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def rwyr_sstop(self, ctx):
        await self.stop_spawn(ctx, 'randomwyr')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.spawn('randomwyr')
