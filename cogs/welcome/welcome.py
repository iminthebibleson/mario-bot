import io
import discord
from discord.ext import commands

from utils.welcome_renderer import generate_welcome

#test 1523564054952677396
#main 1513730041849319475

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        channel_id = 1523564054952677396

        channel = member.guild.get_channel(channel_id)

        if not channel:
            return

        image_bytes = await generate_welcome(
            username=member.display_name,
            avatar=member.display_avatar.url,
            guild_name=member.guild.name,
            member_count=member.guild.member_count
        )

        file = discord.File(
            fp=io.BytesIO(image_bytes),
            filename="welcome.png"
        )

        await channel.send(member.mention ,file=file)


def setup(bot):
    bot.add_cog(Welcome(bot))