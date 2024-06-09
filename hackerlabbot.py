import discord
import datetime
import pytz
from discord.ext import commands
import sys
import _creds_

tz = pytz.timezone('US/Pacific')
description = """Displays the current status of the HackerLab."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True


bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=_creds_.guild_id))
    print(f'Logged in as {bot.user} (ID: {_creds_.bot_id})')


@bot.tree.command(name="openlab", guild=discord.Object(id=_creds_.guild_id))
async def openlab(interaction: discord.Interaction) -> None:
    success = await openLab(name=interaction.user.name)
    await interaction.response.send_message("Command Executed: " + str(success))


@bot.tree.command(name="closelab", guild=discord.Object(id=_creds_.guild_id))
async def closelab(interaction: discord.Interaction):
    success = await closeLab(name=interaction.user.name)
    await interaction.response.send_message("Command Executed: " + str(success))


async def closeLab(name="") -> bool:
    """
    Updates the status to CLOSED

    Sends an embed that the HackerLab is CLOSED
    Changes the status to HackerLab CLOSED
    Changes the nickname to HackerLab CLOSED
    Changes the pfp of the bot to red
    """
    try:
        embed = discord.Embed(
            title="HackerLab Closed",
            description="The HackerLab is Closed :(" if name == "" else "The HackerLab was closed by " + name,
            color=discord.Color.red(),
            timestamp=datetime.datetime.now(tz)
        )
        await messenger(embed, "HackerLab CLOSED", "🔴 Lab CLOSED")
        return True
    except Exception as e:
        print("ERROR: ", str(e), file=sys.stderr)
        return False


async def openLab(name="") -> bool:
    """
        Updates the status to OPEN

        Sends an embed that the HackerLab is Open
        Changes the status to HackerLab OPEN
        Changes the nickname to HackerLab OPEN
        Changes the pfp of the bot to green
        """
    try:
        embed = discord.Embed(
            title="HackerLab Open",
            description="HackerLab is now Open" if name == "" else "The HackerLab was opened by " + name,
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(tz)
        )
        await messenger(embed, "HackerLab OPEN", "🟢 Lab OPEN")
    except Exception as e:
        print("ERROR: ", str(e), file=sys.stderr)
        return False
    return True


async def messenger(embed: discord.Embed, status: str, name: str) -> bool:
    try:
        await bot.change_presence(activity=discord.Game(status))
        await bot.get_guild(_creds_.guild_id).get_member(_creds_.bot_id).edit(nick=name)
        await bot.get_channel(_creds_.channel_id).send(embed=embed)  # discord will only update the name after message is sent
        return True
    except Exception as e:
        print("Error: " + str(e), file=sys.stderr)
        return False


async def startBot():
    await bot.login(_creds_.bot_token)
    await bot.connect()
