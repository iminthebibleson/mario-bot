from discord.ext import commands
from fuzzywuzzy import process
from utils.ida_loader import load_sprites


class FuzzySprite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sprites = load_sprites()

        # name -> id (FAST reverse lookup)
        self.reverse_map = {}
        for sid, sprite in self.sprites.items():
            name = sprite.get("name", "Unknown")
            self.reverse_map[name] = sid

        # id -> name (for display)
        self.name_map = {
            sid: sprite.get("name", "Unknown")
            for sid, sprite in self.sprites.items()
        }

        # IDA-style session memory (optional upgrade)
        self.sessions = {}

    @commands.slash_command(name="fuzzysprite")
    async def fuzzysprite(self, ctx, query: str):

        try:
            if not self.reverse_map:
                return await ctx.respond("❌ No sprite data loaded.")

            # fuzzy match
            matches = process.extract(
                query,
                list(self.reverse_map.keys()),
                limit=5
            )

            results = []
            ids = []

            for name, score in matches:
                sid = self.reverse_map.get(name)

                if sid:
                    results.append(f"`{sid}` — {name} ({score}%)")
                    ids.append(sid)

            if not results:
                return await ctx.respond("❌ No matches found.")

            # 🔥 store session (IDA-style result window)
            self.sessions[ctx.author.id] = {
                "results": ids,
                "index": 0
            }

            await ctx.respond(
                "**🔍 Sprite Search Results**\n" + "\n".join(results)
            )

        except Exception as e:
            await ctx.respond(f"Error: {repr(e)}")


def setup(bot):
    bot.add_cog(FuzzySprite(bot))