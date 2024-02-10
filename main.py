import discord
from discord.ext import tasks, commands
import datetime
import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

puzzleAreas = ["Verdant Glen", "Lucent Waters", "Autumn Falls", "Shady Wildwood", "Serene Deluge"]

acceptedPuzzles = {
    "Verdant Glen": ["Matchboxes", "Light Motifs", "Sightseers", "Sentinel Stones", "Hidden Rings", "Hidden Cubes",
                     "Hidden Archways", "Hidden Pentads", "Logic Grids", "Memory Grids", "Pattern Grids",
                     "Wandering Echos", "Glide Rings", "Flow Orbs", "Crystal Labyrinths", "Morphic Fractals"],

    "Lucent Waters": ["Sightseers", "Matchboxes", "Light Motifs", "Hidden Cubes", "Hidden Archways", "Hidden Rings",
                      "Hidden Pentads", "Logic Grids", "Pattern Grids", "Memory Grids",
                      "Wandering Echos", "Glide Rings", "Flow Orbs", "Morphic Fractals"],

    "Autumn Falls": ["Matchboxes", "Sightseers", "Light Motifs", "Sentinel Stones", "Hidden Cubes", "Hidden Archways",
                     "Hidden Rings", "Hidden Pentads", "Logic Grids", "Memory Grids", "Pattern Grids",
                     "Flow Orbs", "Wandering Echos", "Glide Rings", "Morphic Fractals", "Crystal Labyrinths"],

    "Shady Wildwood": ["Matchboxes", "Light Motifs", "Sightseers", "Sentinel Stones", "Hidden Cubes",  "Hidden Rings",
                       "Hidden Pentads", "Hidden Archways", "Logic Grids", "Memory Grids", "Pattern Grids",
                       "Wandering Echos", "Flow Orbs", "Glide Rings", "Crystal Labyrinths"],

    "Serene Deluge": ["Light Motifs", "Matchboxes", "Sightseers", "Sentinel Stones", "Hidden Pentads", "Hidden Cubes",
                      "Hidden Rings", "Hidden Archways", "Logic Grids", "Memory Grids", "Pattern Grids",
                      "Flow Orbs", "Glide Rings", "Wandering Echos", "Crystal Labyrinths"]
}

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
    "Verdant Glen Morphic Fractals": "9:56",

    "Lucent Waters Sightseers": "6:44",
    "Lucent Waters Matchboxes": "21:48",
    "Lucent Waters Light Motifs": "10:37",
    "Lucent Waters Hidden Cubes": "11:12",
    "Lucent Waters Hidden Archways": "21:40",
    "Lucent Waters Hidden Rings": "0:06",
    "Lucent Waters Hidden Pentads": "3:32",
    "Lucent Waters Logic Grids": "19:36",
    "Lucent Waters Pattern Grids": "0:31",
    "Lucent Waters Memory Grids": "3:53",
    "Lucent Waters Wandering Echos": "2:24",
    "Lucent Waters Glide Rings": "20:12",
    "Lucent Waters Flow Orbs": "13:52",
    "Lucent Waters Morphic Fractals": "0:15",

    "Autumn Falls Matchboxes": "12:37",
    "Autumn Falls Sightseers": "21:33",
    "Autumn Falls Light Motifs": "1:25",
    "Autumn Falls Sentinel Stones": "1:14",
    "Autumn Falls Hidden Cubes": "2:00",
    "Autumn Falls Hidden Archways": "12:29",
    "Autumn Falls Hidden Rings": "14:55",
    "Autumn Falls Hidden Pentads": "19:20",
    "Autumn Falls Logic Grids": "10:25",
    "Autumn Falls Memory Grids": "18:42",
    "Autumn Falls Pattern Grids": "15:20",
    "Autumn Falls Flow Orbs": "4:40",
    "Autumn Falls Wandering Echos": "17:13",
    "Autumn Falls Glide Rings": "11:00",
    "Autumn Falls Morphic Fractals": "15:03",
    "Autumn Falls Crystal Labyrinths": "10:35",

    "Shady Wildwood Matchboxes": "14:13",
    "Shady Wildwood Light Motifs": "3:02",
    "Shady Wildwood Sightseers": "23:09",
    "Shady Wildwood Sentinel Stones": "2:50",
    "Shady Wildwood Hidden Cubes": "3:36",
    "Shady Wildwood Hidden Rings": "16:31",
    "Shady Wildwood Hidden Pentads": "19:56",
    "Shady Wildwood Hidden Archways": "14:05",
    "Shady Wildwood Logic Grids": "12:01",
    "Shady Wildwood Memory Grids": "20:18",
    "Shady Wildwood Pattern Grids": "16:56",
    "Shady Wildwood Wandering Echos": "18:49",
    "Shady Wildwood Flow Orbs": "6:17",
    "Shady Wildwood Glide Rings": "12:36",
    "Shady Wildwood Crystal Labyrinths": "12:11",

    "Serene Deluge Light Motifs": "18:55",
    "Serene Deluge Matchboxes": "6:06",
    "Serene Deluge Sightseers": "15:03",
    "Serene Deluge Sentinel Stones": "18:43",
    "Serene Deluge Hidden Pentads": "11:50",
    "Serene Deluge Hidden Cubes": "19:30",
    "Serene Deluge Hidden Rings": "8:24",
    "Serene Deluge Hidden Archways": "5:59",
    "Serene Deluge Logic Grids": "3:54",
    "Serene Deluge Memory Grids": "12:12",
    "Serene Deluge Pattern Grids": "8:50",
    "Serene Deluge Flow Orbs": "22:10",
    "Serene Deluge Glide Rings": "4:30",
    "Serene Deluge Wandering Echos": "10:43",
    "Serene Deluge Crystal Labyrinths": "4:05"
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

with open("embedMessages.json", "r") as read_file:
    embedMessages = json.load(read_file)

embedMessageIds = {
    "Verdant Glen Channel": embedMessages["Verdant Glen Channel"],
    "Verdant Glen": embedMessages["Verdant Glen"],
    "Lucent Waters Channel": embedMessages["Lucent Waters Channel"],
    "Lucent Waters": embedMessages["Lucent Waters"],
    "Autumn Falls Channel": embedMessages["Autumn Falls Channel"],
    "Autumn Falls": embedMessages["Autumn Falls"],
    "Shady Wildwood Channel": embedMessages["Shady Wildwood Channel"],
    "Shady Wildwood": embedMessages["Shady Wildwood"],
    "Serene Deluge Channel": embedMessages["Serene Deluge Channel"],
    "Serene Deluge": embedMessages["Serene Deluge"]
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

    for puzzle in acceptedPuzzles[area]:
        seconds = (datetime.datetime.strptime(puzzleTimes[area + " " + puzzle], '%H:%M')
                   - currentTime).seconds

        timeString = convertSecondsToString(seconds)

        embedVar.add_field(name=puzzle, value=timeString, inline=True)

    # Fix weird spacing
    if area == "Lucent Waters":
        embedVar.add_field(name="", value="", inline=True)

    embeddedMessage = await ctx.channel.send(embed=embedVar)

    embedMessageIds[area + " Channel"] = ctx.channel.id
    embedMessageIds[area] = embeddedMessage.id

    with open("embedMessages.json", "w") as write_file:
        json.dump(embedMessageIds, write_file)


def convertSecondsToString(seconds):
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

    return timeString


@tasks.loop(seconds=60.0)
async def checkTime():
    # Send messages for each ready puzzle
    time = datetime.datetime.utcnow() - datetime.timedelta(hours=6)
    timeString = "{:d}:{:02d}".format(time.hour, time.minute)
    for area in puzzleAreas:
        for puzzle in acceptedPuzzles[area]:
            currentPuzzle = area + " " + puzzle
            if puzzleTimes[currentPuzzle] == timeString:
                botChannel = bot.get_channel(channelIds[area])
                await botChannel.send(currentPuzzle + " have refreshed!")

    # Update each embedded message
    await updateEmbeds()


async def updateEmbeds():
    currentTime = datetime.datetime.utcnow() - datetime.timedelta(hours=6)

    for area in puzzleAreas:
        channel = bot.get_channel(embedMessageIds[area + " Channel"])
        message = await channel.fetch_message(embedMessageIds[area])
        embed = message.embeds[0]

        index = 0

        for puzzle in acceptedPuzzles[area]:
            seconds = (datetime.datetime.strptime(puzzleTimes[area + " " + puzzle], '%H:%M')
                       - currentTime).seconds

            timeString = convertSecondsToString(seconds)

            embed.set_field_at(index=index, name=puzzle, value=timeString, inline=True)

            index += 1

        await message.edit(embed=embed)


@bot.event
async def on_ready():
    checkTime.start()


bot.run(os.environ['TOKEN'])
