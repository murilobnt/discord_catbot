from discord.ext import commands
import os

from src.cogs.random_story import RandomStory
from src.cogs.wyr_generator import WyrGenerator
from src.cogs.anonymous_message import AnonymousMessage
from src.cogs.random_wyr import RandomWyr

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.add_cog(RandomStory(bot))
bot.add_cog(RandomWyr(bot))
bot.add_cog(WyrGenerator(bot))
bot.add_cog(AnonymousMessage(bot))
bot.run(os.environ['DISCORD_BOT_KEY'])
