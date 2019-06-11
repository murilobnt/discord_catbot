import discord
import asyncio
import random

from queue import Queue
from enum import Enum

from discord.ext import commands
from discord.errors import Forbidden

class Operator(Enum):
    minus = 0
    plus = 1

class MathQuestion:
    def __init__(self):
        self.text_channel_converter = commands.TextChannelConverter()
        self.solved = { "result" : -1, "expression" : -1 }
        self.in_loop = False
        self.available = False

    def solve(self, operators, operands):
        result = operands.get()
        expression = ""
        expression += str(result)
        while not operators.empty():
            op = operators.get()
            n2 = operands.get()
            if op == Operator.minus:
                result -= n2
                expression += " - "
            elif op == Operator.plus:
                result += n2
                expression += " + "
            expression += str(n2)
        return {
            "result" : result,
            "expression" : expression
        }

    def user_is_not_admin(self, permission):
        if not permission.administrator:
            return True
        else:
            return False

    async def sleep(self, time):
        elapsed_time = 0
        while self.in_loop:
            await asyncio.sleep(1)
            elapsed_time += 1
            if elapsed_time >= time:
                return

    async def spawn_math_question(self, ctx, channel):
        chan = await self.text_channel_converter.convert(ctx, channel)
        self.available = True
        number_of_ints = random.randint(2, 4)
        operators = Queue()
        operands = Queue()

        for operand in range(number_of_ints):
            operands.put(random.randint(0, 25))

        for operator in range(number_of_ints - 1):
            operators.put(random.choice(list(Operator)))

        self.solved = self.solve(operators, operands)
        await chan.send("Math question: " + self.solved["expression"] + ". Use !ans to answer.")

    @commands.command(pass_context=True)
    async def ans(self, ctx, arg):
        m_arg = None

        try:
            m_arg = int(arg)
        except ValueError:
            return

        if self.available:
            if m_arg == self.solved["result"]:
                await ctx.send("Correct.")
                self.available = False
            else:
                await ctx.send("Wrong answer.")
        else:
            await ctx.send("No math questions available.")

    @commands.command(pass_context=True)
    async def mq_spawn(self, ctx, channel, sleep_lower_range, sleep_upper_range):
        if not ctx.message.author.guild_permissions.administrator or self.in_loop:
            await ctx.send("Admin only. Only 1 spawn allowed.")
            return
        self.in_loop = True
        await ctx.send("Spawn set.")
        while self.in_loop:
            await self.spawn_math_question(ctx, channel)
            await self.sleep(random.randint(int(sleep_lower_range), int(sleep_upper_range)))

    @commands.command(pass_context=True)
    async def mq_sstop(self, ctx):
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send("You need to be an administrator to run this command.")
            return
        self.in_loop = False
        await ctx.send("Math spawn has been stopped.")

    @commands.command(pass_context=True)
    async def set_callback(self, ctx, callback):
        self.callback = callback
