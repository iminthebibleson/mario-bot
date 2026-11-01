from discord.ext import commands


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="calc")
    async def calc(self, ctx, expression: str):
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            await ctx.respond(f"{result} (0x{result:X})")
        except Exception as e:
            await ctx.respond(f"Error: {e}")


def setup(bot):
    bot.add_cog(Calc(bot))