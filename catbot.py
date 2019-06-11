from discord.ext import commands

from src.cogs.math_question import MathQuestion
from src.cogs.random_story import RandomStory
from src.cogs.wyr_generator import WyrGenerator
from src.cogs.anonymous_message import AnonymousMessage

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#bot.add_cog(MathQuestion())
bot.add_cog(RandomStory(bot))
bot.add_cog(WyrGenerator(bot))
bot.add_cog(AnonymousMessage(bot))
#bot.run('secret-taken-away-because-my-bot-is-currently-online-;)')
