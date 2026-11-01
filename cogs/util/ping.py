from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="ping",
        description="Check bot latency"
    )
    async def ping(self, ctx):
        await ctx.respond(
            f"Pong! {round(self.bot.latency * 1000)}ms"
        )


def setup(bot):
    bot.add_cog(Ping(bot))