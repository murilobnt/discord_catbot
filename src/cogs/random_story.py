import discord
import random
import asyncio

from src.operational.rs_template_applier import RSTemplateApplier
from src.common.common_publisher_cog import CommonPublisherCog

from discord.ext import commands
from discord.errors import Forbidden

class RandomStory(CommonPublisherCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.m_rs_template_applier = RSTemplateApplier()

    def get_story(self, mention):
        if random.randint(1, 120) == 120:
            return "June is...... Oh, sorry. This probably won't happen again... anytime soon..."
        else:
            return self.m_rs_template_applier.generate_random_story(mention)

    async def loop_operation(self, guild, channel):
        mention = random.choice(guild.members).display_name
        await channel.send(self.get_story(mention))

    @commands.command(pass_context=True)
    async def random_story(self, ctx):
        mention = random.choice(ctx.guild.members).display_name
        await ctx.send(self.get_story(mention))

    @commands.command(pass_context=True)
    async def build_story(self, ctx, *, mention):
        await ctx.send(self.get_story(mention))

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def get_from_template(self, ctx, template_id):
        mention = random.choice(ctx.guild.members).display_name
        await ctx.send(self.m_rs_template_applier.random_story(mention, template_id))

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def rs_spawn(self, ctx, channel, await_time):
        await self.start_spawn(ctx, 'randomstory', channel, await_time)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def rs_sstop(self, ctx):
        await self.stop_spawn(ctx, 'randomstory')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.spawn('randomstory')
