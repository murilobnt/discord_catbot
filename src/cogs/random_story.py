import discord
import random
import asyncio

from src.random_story.template_container import TemplateContainer
from src.database.catbot_database import CatbotDatabase

from discord.ext import commands
from discord.errors import Forbidden

class RandomStory:
    def __init__(self, bot):
        self.in_loop = False
        self.bot = bot
        self.cb_d = CatbotDatabase()
        self.text_channel_converter = commands.TextChannelConverter()
        self.m_template_container = TemplateContainer()

    async def sleep(self, time):
        elapsed_time = 0
        while self.in_loop:
            await asyncio.sleep(1)
            elapsed_time += 1
            if elapsed_time >= time:
                return

    async def spawn(self):
        self.cb_d.connect()
        cursor = self.cb_d.cursor

        cursor.execute("SELECT startup FROM srecords WHERE module='randomstory'")
        startup = cursor.fetchone()

        if startup is None or startup[0] is None or not startup[0]:
            self.cb_d.close()
            return

        cursor.execute("SELECT guildid FROM guild")
        guildid = int(cursor.fetchone()[0])

        cursor.execute("SELECT channel, timeinterval FROM srecords WHERE module='randomstory'")
        fetch = cursor.fetchone()

        if fetch is None:
            print("No records for random story.")
            self.cb_d.close()
            return

        d_channel = fetch[0]
        await_time = int(fetch[1])

        self.cb_d.close()

        guild = self.bot.get_guild(guildid)
        channel = guild.get_channel(d_channel)

        self.in_loop = True
        while self.in_loop:
            mention = random.choice(guild.members).display_name
            result = self.m_template_container.generate_random_story(mention)
            await channel.send(result)
            await self.sleep(int(await_time))

    @commands.command(pass_context=True)
    async def random_story(self, ctx):
        mention = random.choice(ctx.guild.members).display_name
        result = ""
        if random.randint(1, 1031) == 320:
            result = "June is...... Oh, sorry. This probably won't happen again... anytime soon..."
        else:
            result = self.m_template_container.generate_random_story(mention)
        await ctx.send(result)

    @commands.command(pass_context=True)
    async def build_story(self, ctx, *, mention):
        result = self.m_template_container.generate_random_story(mention)
        await ctx.send(result)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def get_from_template(self, ctx, template_id):
        mention = random.choice(ctx.guild.members).display_name
        await ctx.send(self.m_template_container.random_story(mention, template_id))

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def rs_spawn(self, ctx, channel, await_time):
        if self.in_loop:
            await ctx.send("Only 1 spawn allowed.")
            return

        self.cb_d.connect()
        cursor = self.cb_d.cursor

        channel = await self.text_channel_converter.convert(ctx, channel)
        c_id = channel.id

        cursor.execute("SELECT channel FROM srecords WHERE module='randomstory'")
        db_channel = cursor.fetchone()

        if db_channel is None:
            cursor.execute("INSERT INTO srecords (module, channel, timeinterval, startup) VALUES ('randomstory', %s, %s, 'true')", (c_id, await_time))
        else:
            cursor.execute("UPDATE srecords SET channel=%s, timeinterval=%s, startup='true' WHERE module='randomstory'", (c_id, await_time))

        self.cb_d.commit()
        self.cb_d.close()

        await ctx.send("OK.")
        await self.spawn()

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def rs_sstop(self, ctx):
        self.cb_d.connect()
        cursor = self.cb_d.cursor
        self.in_loop = False

        cursor.execute("UPDATE srecords SET startup='false' WHERE module='randomstory'")

        self.cb_d.commit()
        self.cb_d.close()

        await ctx.send("OK.")

    async def on_ready(self):
        await self.spawn()
