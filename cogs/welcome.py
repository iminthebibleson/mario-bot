import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1513730041849319475

        channel = member.guild.get_channel(channel_id)

        if not channel:
            return

        embed = discord.Embed(
            title="Welcome!",
            description=f"Welcome to **{member.guild.name}**, {member.mention}!",
            color=0xec5800
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.set_footer(
            text=f"You are member #{member.guild.member_count}"
        )

        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))