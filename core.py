import logging
from logging.handlers import RotatingFileHandler
import discord
from discord.ext import commands
from discord import app_commands
import config

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = RotatingFileHandler("logs/bot.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    fh.setFormatter(fmt)
    fh.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        setup_logging()
        logging.getLogger(__name__).info("Logged in as %s (%s)", self.bot.user, self.bot.user.id if self.bot.user else "n/a")
        if config.SYNC_ON_READY:
            try:
                if config.GUILD_IDS:
                    for gid in config.GUILD_IDS:
                        guild = discord.Object(id=gid)
                        await self.bot.tree.sync(guild=guild)
                    logging.info("Slash commands synced to guilds: %s", config.GUILD_IDS)
                else:
                    await self.bot.tree.sync()
                    logging.info("Slash commands synced globally")
            except Exception as e:
                logging.exception("Slash sync failed: %s", e)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Missing argument: {error.param.name}", mention_author=False)
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You lack required permissions.", mention_author=False)
            return
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.reply("I lack required permissions to do that.", mention_author=False)
            return
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Slow down! Try again in {error.retry_after:.1f}s.", mention_author=False)
            return

        logging.exception("Unhandled command error", exc_info=error)
        await ctx.reply("An unexpected error occurred.", mention_author=False)

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        logging.exception("App command error", exc_info=error)
        if interaction.response.is_done():
            await interaction.followup.send("An error occurred.", ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred.", ephemeral=True)

async def setup(bot: commands.Bot):
    import os
    os.makedirs("logs", exist_ok=True)
    await bot.add_cog(Core(bot))
