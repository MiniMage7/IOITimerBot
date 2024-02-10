import discord
from discord.ext import tasks, commands
import datetime
import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

acceptedAreas = ["Verdant Glen", "Lucent Waters", "Autumn Falls", "Shady Wildwood", "Serene Deluge"]
acceptedPuzzles = ["Matchbox", "Light Motif", "Sightseer", "Sentinel Stones", "Hidden Ring", "Hidden Cube",
                   "Hidden Archway", "Hidden Pentad", "Logic Grid", "Memory Grid", "Pattern Grid", "Wandering Echo",
                   "Glide Rings", "Flow Orbs", "Crystal Labyrinth", "Morphic Fractal"]

# Times are UTC - 6
puzzleTimes = {
    "Verdant Glen Matchbox": "7:29",
    "Verdant Glen Light Motif": "20:18",
    "Verdant Glen Sightseer": "16:25",
    "Verdant Glen Sentinel Stones": "20:06",
    "Verdant Glen Hidden Ring": "9:47",
    "Verdant Glen Hidden Cube": "20:52",
    "Verdant Glen Hidden Archway": "7:20",
    "Verdant Glen Hidden Pentad": "13:12",
    "Verdant Glen Logic Grid": "5:17",
    "Verdant Glen Memory Grid": "13:34",
    "Verdant Glen Pattern Grid": "10:12",
    "Verdant Glen Wandering Echo": "12:05",
    "Verdant Glen Glide Rings": "5:52",
    "Verdant Glen Flow Orbs": "23:32",
    "Verdant Glen Crystal Labyrinth": "5:28",
    "Verdant Glen Morphic Fractal": "9:55"
}

with open("channels.json", "r") as read_file:
    channelsJSON = json.load(read_file)

channelIds = {
    "Verdant Glen": channelsJSON["Verdant Glen"],
    "Lucent Waters": channelsJSON["Lucent Waters"],
    "Autumn Falls": channelsJSON["Autumn Falls"],
    "Shady Wildwood": channelsJSON["Shady Wildwood"],
    "Serene Deluge": channelsJSON["Serene Deluge"]
}


@bot.check
async def globally_block_non_IOI(ctx):  # Second one is for testing
    return ctx.guild.id == 1193697387827437598 or ctx.guild.id == 1205261316818731029


async def isAdmin(ctx):
    return ctx.author.id == 461268548229136395 or await bot.is_owner(ctx.author)


@tasks.loop(seconds=60.0)
async def checkTime():
    time = datetime.datetime.utcnow() - datetime.timedelta(hours=6)
    timeString = "{:d}:{:02d}".format(time.hour, time.minute)
    for area in acceptedAreas:
        for puzzle in acceptedPuzzles:
            try:
                currentPuzzle = area + " " + puzzle
                if puzzleTimes[currentPuzzle] == timeString:
                    botChannel = bot.get_channel(channelIds[area])
                    await botChannel.send(currentPuzzle + " have refreshed!")
            except KeyError:
                pass


@bot.event
async def on_ready():
    checkTime.start()

bot.run(os.environ['TOKEN'])
