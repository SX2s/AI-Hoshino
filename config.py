PREFIX = "!"
OWNER_IDS = set()  # e.g., {123456789012345678}
GUILD_IDS = []  # e.g., [123456789012345678] for faster slash sync; leave empty for global
COG_AUTOLOAD_DIR = "cogs"
LOG_CHANNEL_ID = 0  # set to a channel ID for moderation/logging events, or 0 to disable
LOG_LEVEL = "INFO"  # DEBUG / INFO / WARNING / ERROR
SYNC_ON_READY = True  # auto sync slash commands on_ready
