import discord
import asyncio

from abc import ABC, ABCMeta, abstractmethod
from discord.ext import commands
from discord.errors import Forbidden
from src.database.catbot_database import CatbotDatabase

class CogABCMeta(commands.CogMeta, ABCMeta):
    pass

class CommonPublisherCog(ABC, commands.Cog, metaclass=CogABCMeta):
    def __init__(self, bot):
        self.in_loop = False
        self.bot = bot
        self.text_channel_converter = commands.TextChannelConverter()
        self.cb_d = CatbotDatabase()

    @abstractmethod
    async def loop_operation(self, guild, channel):
        pass

    async def sleep(self, time):
        elapsed_time = 0
        while self.in_loop:
            await asyncio.sleep(1)
            elapsed_time += 1
            if elapsed_time >= time:
                return

    async def spawn(self, module):
        self.cb_d.connect()
        cursor = self.cb_d.cursor

        cursor.execute("SELECT startup FROM srecords WHERE module=%s", (module,))
        startup = cursor.fetchone()

        if startup is None or startup[0] is None or not startup[0]:
            print("No startup set for the module: " + module + ".")
            self.cb_d.close()
            return

        cursor.execute("SELECT guildid FROM guild")
        guildid = int(cursor.fetchone()[0])

        cursor.execute("SELECT channel, timeinterval FROM srecords WHERE module=%s", (module,))
        fetch = cursor.fetchone()

        if fetch is None:
            print("No records for the module: " + module + ".")
            self.cb_d.close()
            return

        d_channel = fetch[0]
        await_time = int(fetch[1])

        self.cb_d.close()

        guild = self.bot.get_guild(guildid)
        channel = guild.get_channel(d_channel)

        self.in_loop = True
        while self.in_loop:
            await self.loop_operation(guild, channel)
            await self.sleep(int(await_time))

    async def start_spawn(self, ctx, module, channel, await_time):
        if self.in_loop:
            await ctx.send("Only 1 spawn allowed on module "+ module + ".")
            return

        self.cb_d.connect()
        cursor = self.cb_d.cursor

        channel = await self.text_channel_converter.convert(ctx, channel)
        c_id = channel.id

        cursor.execute("SELECT channel FROM srecords WHERE module=%s", (module,))
        db_channel = cursor.fetchone()

        if db_channel is None:
            cursor.execute("INSERT INTO srecords (module, channel, timeinterval, startup) VALUES (%s, %s, %s, 'true')", (module, c_id, await_time))
        else:
            cursor.execute("UPDATE srecords SET channel=%s, timeinterval=%s, startup='true' WHERE module=%s", (c_id, await_time, module))

        self.cb_d.commit()
        self.cb_d.close()

        await ctx.send("OK.")
        await self.spawn(module)

    async def stop_spawn(self, ctx, module):
        self.cb_d.connect()
        cursor = self.cb_d.cursor
        self.in_loop = False

        cursor.execute("UPDATE srecords SET startup='false' WHERE module=%s", (module,))

        self.cb_d.commit()
        self.cb_d.close()

        await ctx.send("OK.")
