from discord.ext import commands
from cpp_demangle import demangle


class Demangle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="demangle")
    async def demangle_cmd(self, ctx, symbol: str):

        try:
            result = demangle(symbol)
            await ctx.respond(f"```{result}```")

        except ValueError:
            await ctx.respond(
                "❌ Invalid mangled symbol.\n"
                "Make sure it's a full C++ mangled name (not truncated)."
            )

        except Exception as e:
            await ctx.respond(f"Error: {repr(e)}")


def setup(bot):
    bot.add_cog(Demangle(bot))