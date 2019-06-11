import discord
import base64

from discord.ext import commands
from discord.errors import Forbidden
from Crypto.Cipher import AES

from src.database.catbot_database import CatbotDatabase

class AnonymousMessage:
    def encrypt(self, content):
        enc_secret = AES.new(self.master_key[:32])
        tag_string = (str(content) +
                      (AES.block_size -
                       len(str(content)) % AES.block_size) * "\0")
        cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))

        return str(cipher_text.decode("utf-8"))

    def __init__(self, bot):
        self.cb_d = CatbotDatabase()
        self.bot = bot
        self.text_channel_converter = commands.TextChannelConverter()
        #self.master_key = "master-key-taken-away-;)"

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def set_guild(self, ctx):
        self.cb_d.connect()
        self.cb_d.cursor.execute("SELECT guildid FROM guild")
        d_guildid = self.cb_d.cursor.fetchone()
        if d_guildid is None:
            self.cb_d.cursor.execute("INSERT INTO guild (guildid) VALUES (%s)", (ctx.guild.id,))
            self.cb_d.commit()
            await ctx.send("Inserted.")
        else:
            await ctx.send("Guild already inserted.")

        self.cb_d.close()

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def set_anon_channels(self, ctx, channel, l_channel):
        self.cb_d.connect()

        channel = await self.text_channel_converter.convert(ctx, channel)
        l_channel = await self.text_channel_converter.convert(ctx, l_channel)

        c_id = channel.id
        lc_id = l_channel.id

        self.cb_d.cursor.execute("SELECT channel FROM srecords WHERE module='anonymousmessage'")
        db_channel = self.cb_d.cursor.fetchone()
        self.cb_d.cursor.execute("SELECT channel FROM srecords WHERE module='anonymousmessagelog'")
        db_l_channel = self.cb_d.cursor.fetchone()

        if db_channel is None or db_l_channel is None:
            self.cb_d.cursor.execute("INSERT INTO srecords (module, channel) VALUES ('anonymousmessage', %s)", (c_id,))
            self.cb_d.cursor.execute("INSERT INTO srecords (module, channel) VALUES ('anonymousmessagelog', %s)", (lc_id,))
        else:
            self.cb_d.cursor.execute("UPDATE srecords SET channel=%s WHERE module='anonymousmessage'", (c_id,))
            self.cb_d.cursor.execute("UPDATE srecords SET channel=%s WHERE module='anonymousmessagelog'", (lc_id,))

        self.cb_d.commit()
        self.cb_d.close()

        await ctx.send("OK.")

    async def on_message(self, message):
        if type(message.channel) is discord.DMChannel:
            self.cb_d.connect()

            self.cb_d.cursor.execute("SELECT guildid FROM guild")
            guildid = int(self.cb_d.cursor.fetchone()[0])
            self.cb_d.cursor.execute("SELECT channel FROM srecords WHERE module='anonymousmessage'")
            db_channel = int(self.cb_d.cursor.fetchone()[0])
            self.cb_d.cursor.execute("SELECT channel FROM srecords WHERE module='anonymousmessagelog'")
            db_l_channel = int(self.cb_d.cursor.fetchone()[0])

            self.cb_d.close()

            if db_channel is None or db_l_channel is None:
                return

            channel = self.bot.get_guild(guildid).get_channel(db_channel)
            l_channel = self.bot.get_guild(guildid).get_channel(db_l_channel)

            await channel.send("**New message:**\n" + message.content + "\n---")
            author_name_enc = self.encrypt(str(message.author).encode("utf-8"))
            author_id_enc = self.encrypt(str(message.author.id).encode("utf-8"))
            await l_channel.send("**--- MESSAGE ---**\n" + message.content + "\nAuthor: ||" + author_name_enc + "||\nAuthor ID: ||" + author_id_enc + "||\n---")
