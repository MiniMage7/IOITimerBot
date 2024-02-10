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
    "Verdant Glen Matchboxes": "7:30",
    "Verdant Glen Light Motifs": "20:18",
    "Verdant Glen Sightseers": "16:26",
    "Verdant Glen Sentinel Stones": "20:07",
    "Verdant Glen Hidden Rings": "9:48",
    "Verdant Glen Hidden Cubes": "20:53",
    "Verdant Glen Hidden Archways": "7:22",
    "Verdant Glen Hidden Pentads": "13:13",
    "Verdant Glen Logic Grids": "5:18",
    "Verdant Glen Memory Grids": "13:35",
    "Verdant Glen Pattern Grids": "10:13",
    "Verdant Glen Wandering Echos": "12:06",
    "Verdant Glen Glide Rings": "5:53",
    "Verdant Glen Flow Orbs": "23:33",
    "Verdant Glen Crystal Labyrinths": "5:28",
    "Verdant Glen Morphic Fractals": "9:56"
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
    await create_embed_timer(ctx, "Verdant Glen")


@bot.hybrid_command()
@commands.check(isAdmin)
async def set_lucent_waters(ctx):
    await create_embed_timer(ctx, "Lucent Waters")


@bot.hybrid_command()
@commands.check(isAdmin)
async def set_autumn_falls(ctx):
    await create_embed_timer(ctx, "Autumn Falls")


@bot.hybrid_command()
@commands.check(isAdmin)
async def set_shady_wildwood(ctx):
    await create_embed_timer(ctx, "Shady Wildwood")


@bot.hybrid_command()
@commands.check(isAdmin)
async def set_serene_deluge(ctx):
    await create_embed_timer(ctx, "Serene Deluge")


async def create_embed_timer(ctx, area):
    await ctx.message.delete()

    embedVar = discord.Embed(title=area + " Timers", color=0x336EFF)
    currentTime = datetime.datetime.utcnow() - datetime.timedelta(hours=6)

    for puzzle in acceptedPuzzles:
        try:
            seconds = (datetime.datetime.strptime(puzzleTimes[area + " " + puzzle], '%H:%M')
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

    # Update each embedded message


@bot.event
async def on_ready():
    checkTime.start()

bot.run(os.environ['TOKEN'])
