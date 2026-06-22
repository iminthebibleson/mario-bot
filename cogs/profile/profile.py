import discord
from discord.ext import commands
from utils.ida_loader import load_profiles


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profiles = load_profiles()

    @commands.slash_command(name="profile")
    async def profile(self, ctx, profile_id: int):

        profile = self.profiles.get(str(profile_id))

        if not profile:
            return await ctx.respond("Profile not found.")

        embed = discord.Embed(
            title=profile.get("name"),
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Build Function",
            value=profile.get("build_function", "Unknown")
        )

        embed.add_field(
            name="Type",
            value=profile.get("type", "Unknown")
        )

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Profile(bot))