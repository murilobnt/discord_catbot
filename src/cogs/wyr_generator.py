import discord
import requests
import asyncio

from discord.ext import commands
from discord.errors import Forbidden

from psycopg2.extensions import AsIs
from src.database.catbot_database import CatbotDatabase

class WyrGenerator:
    def __init__(self, bot):
        self.in_loop = False
        self.bot = bot
        self.text_channel_converter = commands.TextChannelConverter()
        self.cb_d = CatbotDatabase()
        self.filters = ['gay', 'sex',
        'hot girls', 'hot guys',
        'hot', 'sex', 'sexual',
        'nude', 'nudity', 'naked',
        'cheating', 'cheat', 'dating',
        'people', 'gross', 'love',
        'politics', 'religion', 'relationships',
        'drugs', 'meth']

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

        cursor.execute("SELECT startup FROM srecords WHERE module='wyrgenerator'")
        startup = cursor.fetchone()

        if startup is None or startup[0] is None or not startup[0]:
            self.cb_d.close()
            return

        cursor.execute("SELECT guildid FROM guild")
        guildid = int(cursor.fetchone()[0])

        cursor.execute("SELECT channel, timeinterval FROM srecords WHERE module='wyrgenerator'")
        fetch = cursor.fetchone()

        if fetch is None:
            print("No records for would you rather.")
            self.cb_d.close()
            return

        d_channel = fetch[0]
        await_time = int(fetch[1])

        self.cb_d.close()

        channel = self.bot.get_guild(guildid).get_channel(d_channel)

        self.in_loop = True
        while self.in_loop:
            data = await self.get_random_wyr()
            msg = await channel.send(data['title'] + "\n:regional_indicator_a: `"+data['choicea']+"`\n:b: `" + data['choiceb'] + "`\n:fast_forward: `I rather not answer`")
            await msg.add_reaction("\U0001F1E6")
            await msg.add_reaction("\U0001F171")
            await msg.add_reaction("\U000023E9")
            await self.sleep(int(await_time))

    async def get_random_wyr(self):
        self.cb_d.connect()
        cursor = self.cb_d.cursor
        while True:
            req = requests.get('https://www.rrrather.com/botapi')
            data = req.json()
            cursor.execute("SELECT * FROM question WHERE choicea=%s", (data['choicea'],))
            if data['nsfw'] == True or (data['tags'] != False and [i for i in self.filters if i in data['tags']]) or (cursor.fetchone() is not None):
                continue

            cursor.execute("INSERT INTO question (choicea) VALUES (%s)", (data['choicea'],))
            self.cb_d.commit()
            self.cb_d.close()
            return data

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def wyr_spawn(self, ctx, channel, await_time):
        if self.in_loop:
            await ctx.send("Only 1 spawn allowed.")
            return

        self.cb_d.connect()
        cursor = self.cb_d.cursor

        channel = await self.text_channel_converter.convert(ctx, channel)
        c_id = channel.id

        cursor.execute("SELECT channel FROM srecords WHERE module='wyrgenerator'")
        db_channel = cursor.fetchone()

        if db_channel is None:
            cursor.execute("INSERT INTO srecords (module, channel, timeinterval, startup) VALUES ('wyrgenerator', %s, %s, 'true')", (c_id, await_time))
        else:
            cursor.execute("UPDATE srecords SET channel=%s, timeinterval=%s, startup='true' WHERE module='wyrgenerator'", (c_id, await_time))

        self.cb_d.commit()
        self.cb_d.close()

        await ctx.send("OK.")
        await self.spawn()

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def wyr_sstop(self, ctx):
        self.cb_d.connect()
        cursor = self.cb_d.cursor
        self.in_loop = False

        cursor.execute("UPDATE srecords SET startup='false' WHERE module='wyrgenerator'")

        self.cb_d.commit()
        self.cb_d.close()

        await ctx.send("OK.")

    async def on_ready(self):
        await self.spawn()
