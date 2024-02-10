import discord
from discord.ext import tasks, commands
import datetime
import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

acceptedAreas = ["Verdant Glen", "Lucent Waters", "Autumn Falls", "Shady Wildwood", "Serene Deluge"]
acceptedPuzzles = ["Matchboxes", "Light Motifs", "Sightseers", "Sentinel Stones", "Hidden Rings", "Hidden Cubes",
                   "Hidden Archways", "Hidden Pentads", "Logic Grids", "Memory Grids", "Pattern Grids",
                   "Wandering Echos", "Glide Rings", "Flow Orbs", "Crystal Labyrinths", "Morphic Fractals"]

# Times are UTC - 6
puzzleTimes = {
    "Verdant Glen Matchboxes": "7:29",
    "Verdant Glen Light Motifs": "20:18",
    "Verdant Glen Sightseers": "16:25",
    "Verdant Glen Sentinel Stones": "20:06",
    "Verdant Glen Hidden Rings": "9:47",
    "Verdant Glen Hidden Cubes": "20:52",
    "Verdant Glen Hidden Archways": "7:20",
    "Verdant Glen Hidden Pentads": "13:12",
    "Verdant Glen Logic Grids": "5:17",
    "Verdant Glen Memory Grids": "13:34",
    "Verdant Glen Pattern Grids": "10:12",
    "Verdant Glen Wandering Echos": "12:05",
    "Verdant Glen Glide Rings": "5:52",
    "Verdant Glen Flow Orbs": "23:32",
    "Verdant Glen Crystal Labyrinths": "5:28",
    "Verdant Glen Morphic Fractals": "9:55"
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


@bot.hybrid_command()
@commands.check(isAdmin)
async def set_verdant_glen(ctx):
    await ctx.message.delete()

    embedVar = discord.Embed(title="Verdant Glen Timers", color=0x336EFF)
    currentTime = datetime.datetime.utcnow() - datetime.timedelta(hours=6)

    for puzzle in acceptedPuzzles:
        try:
            seconds = (datetime.datetime.strptime(puzzleTimes["Verdant Glen " + puzzle], '%H:%M')
                       - currentTime).seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            timeString = ""

            if hours != 0:
                timeString += "{:d} hour".format(hours)
                if hours != 1:
                    timeString += "s"

                if minutes != 0:
                    timeString += " and "

            if minutes != 0:
                timeString += "{:d} minute".format(minutes)
                if minutes != 1:
                    timeString += "s"

            if timeString == "":
                timeString = "Refreshing Now!"

            embedVar.add_field(name=puzzle, value=timeString, inline=True)
        except KeyError:
            pass

    await ctx.channel.send(embed=embedVar)


@tasks.loop(seconds=60.0)
async def checkTime():
    # Send messages for each ready puzzle
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
