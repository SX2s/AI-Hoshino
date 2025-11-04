import discord
from discord.ext import commands
import time
from datetime import datetime

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases=["latency", "speed"])
    async def ping(self, ctx):
        # Measure API latency + round-trip time
        start = time.perf_counter()
        message = await ctx.send("🏓 Pinging...")
        end = time.perf_counter()
        api_latency = round(self.bot.latency * 1000)
        message_latency = round((end - start) * 1000)

        # Dynamic gradient color
        gradient_colors = [0xff7eb3, 0x8b5cf6, 0x4ade80]
        color = gradient_colors[ctx.author.id % len(gradient_colors)]

        # Determine latency status
        if api_latency <= 100:
            status_emoji, status_text = "🟢", "Excellent"
        elif api_latency <= 200:
            status_emoji, status_text = "🟡", "Good"
        elif api_latency <= 300:
            status_emoji, status_text = "🟠", "Moderate"
        else:
            status_emoji, status_text = "🔴", "Poor"

        # Create embed
        embed = discord.Embed(
            title=f"🏓 AI HOSHINO | Ping Status",
            description=f"{status_emoji} **Connection Status:** {status_text}",
            color=color,
            timestamp=datetime.utcnow()
        )

        embed.add_field(name="📡 WebSocket Latency", value=f"`{api_latency} ms`", inline=True)
        embed.add_field(name="⚙️ Message Latency", value=f"`{message_latency} ms`", inline=True)
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            value="🌸 *Latency check completed successfully!*",
            inline=False
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.display_name} • {ctx.guild.name}",
            icon_url=ctx.author.display_avatar.url
        )

        await message.edit(content=None, embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))
