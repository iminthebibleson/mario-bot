from discord.ext import commands


class Assemble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="assemble")
    async def assemble(self, ctx, code: str):
        await ctx.respond(f"Assembly:\n```{code}```")


def setup(bot):
    bot.add_cog(Assemble(bot))