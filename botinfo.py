import discord
from discord.ext import commands
import platform, psutil, time
from datetime import datetime

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(name="botinfo", aliases=["stats", "bot"])
    async def botinfo(self, ctx):
        # Calculate uptime
        current_time = time.time()
        uptime_seconds = int(current_time - self.start_time)
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{days}d {hours}h {minutes}m {seconds}s"

        # Gradient color scheme
        gradient_colors = [0xff7eb3, 0x8b5cf6, 0x4ade80]
        color = gradient_colors[ctx.author.id % len(gradient_colors)]

        embed = discord.Embed(
            title="🤖 AI HOSHINO | Bot Information",
            description="✨ Get to know your digital assistant in detail!",
            color=color,
            timestamp=datetime.utcnow()
        )

        # Avatar + footer
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name} • {ctx.guild.name}",
            icon_url=ctx.author.display_avatar.url
        )

        # Basic info
        embed.add_field(name="💡 Bot Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="🆔 Bot ID", value=f"`{self.bot.user.id}`", inline=True)
        embed.add_field(name="🌐 Prefix", value="`!`", inline=True)

        # Stats
        embed.add_field(name="📡 Ping", value=f"{round(self.bot.latency * 1000)} ms", inline=True)
        embed.add_field(name="🕐 Uptime", value=uptime, inline=True)
        embed.add_field(name="🧠 Servers", value=f"{len(self.bot.guilds)}", inline=True)

        # System info
        embed.add_field(name="⚙️ Python Version", value=platform.python_version(), inline=True)
        embed.add_field(name="🔧 discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="💻 OS", value=platform.system(), inline=True)

        # Resource usage
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        embed.add_field(name="🧩 CPU Usage", value=f"{cpu_percent}%", inline=True)
        embed.add_field(name="💾 RAM Usage", value=f"{memory_info.percent}%", inline=True)

        # Fancy divider
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            value="🌸 *Powered by AI HOSHINO*",
            inline=False
        )

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(BotInfo(bot))
