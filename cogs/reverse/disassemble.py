from discord.ext import commands


class Disassemble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="disassemble")
    async def disassemble(self, ctx, hex_bytes: str):
        await ctx.respond(f"Hex:\n```{hex_bytes}```")


def setup(bot):
    bot.add_cog(Disassemble(bot))