import discord
import requests
import asyncio

from discord.ext import commands
from discord.errors import Forbidden

from psycopg2.extensions import AsIs
from src.database.catbot_database import CatbotDatabase
from src.common.common_publisher_cog import CommonPublisherCog

class WyrGenerator(CommonPublisherCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.filters = ['gay', 'sex',
        'hot girls', 'hot guys',
        'hot', 'sex', 'sexual',
        'nude', 'nudity', 'naked',
        'cheating', 'cheat', 'dating',
        'people', 'gross', 'love',
        'politics', 'religion', 'relationships',
        'drugs', 'meth']

    async def loop_operation(self, guild, channel):
        data = await self.get_random_wyr()
        msg = await channel.send(data['title'] + "\n:regional_indicator_a: `"+data['choicea']+"`\n:b: `" + data['choiceb'] + "`\n:fast_forward: `I rather not answer`")
        await msg.add_reaction("\U0001F1E6")
        await msg.add_reaction("\U0001F171")
        await msg.add_reaction("\U000023E9")

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
        self.start_spawn(ctx, 'wyrgenerator', channel, await_time)

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def wyr_sstop(self, ctx):
        self.stop_spawn(ctx, 'wyrgenerator')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.spawn('wyrgenerator')
