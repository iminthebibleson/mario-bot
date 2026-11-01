import io
import discord
from discord.ext import commands

from utils.welcome_renderer import generate_welcome

# test 1523564054952677396
# main 1513730041849319475

CHANNEL_ID = 1513730041849319475


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_welcome(self, member):

        channel = member.guild.get_channel(CHANNEL_ID)
        if not channel:
            return

        try:
            image_bytes = await generate_welcome(
                username=member.display_name,
                avatar=member.display_avatar.url,
                guild_name=member.guild.name,
                member_count=member.guild.member_count
            )
        except Exception as e:
            print(f"[welcome] Image generation failed: {e!r}", flush=True)
            await channel.send(f"Welcome to {member.guild.name}, {member.mention}!")
            return

        file = discord.File(fp=io.BytesIO(image_bytes), filename="welcome.png")
        await channel.send(member.mention, file=file)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.send_welcome(member)

    # Temporary: run !testwelcome to trigger it without a real join
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def testwelcome(self, ctx):
        await self.send_welcome(ctx.author)


def setup(bot):
    bot.add_cog(Welcome(bot))