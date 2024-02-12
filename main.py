import discord
from discord.ext import tasks, commands
import datetime
import json
import os
from asyncio import sleep

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

puzzleAreas = ["Verdant Glen", "Lucent Waters", "Autumn Falls", "Shady Wildwood", "Serene Deluge"]

# TODO: This and puzzleTimes will need to be updated on release
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

    "Shady Wildwood": ["Matchboxes", "Light Motifs", "Sightseers", "Sentinel Stones", "Hidden Cubes", "Hidden Rings",
                       "Hidden Pentads", "Hidden Archways", "Logic Grids", "Memory Grids", "Pattern Grids",
                       "Wandering Echos", "Flow Orbs", "Glide Rings", "Crystal Labyrinths"],

    "Serene Deluge": ["Light Motifs", "Matchboxes", "Sightseers", "Sentinel Stones", "Hidden Pentads", "Hidden Cubes",
                      "Hidden Rings", "Hidden Archways", "Logic Grids", "Memory Grids", "Pattern Grids",
                      "Flow Orbs", "Glide Rings", "Wandering Echos", "Crystal Labyrinths"]
}

# Times are UTC - 6
puzzleTimes = {
    "Verdant Glen Matchboxes": "7:29:18",
    "Verdant Glen Light Motifs": "21:17:55",
    "Verdant Glen Sightseers": "17:25:11",
    "Verdant Glen Sentinel Stones": "20:06:03",
    "Verdant Glen Hidden Rings": "9:47:04",
    "Verdant Glen Hidden Cubes": "20:52:52",
    "Verdant Glen Hidden Archways": "7:21:13",
    "Verdant Glen Hidden Pentads": "13:12:52",
    "Verdant Glen Logic Grids": "5:17:06",
    "Verdant Glen Memory Grids": "13:34:42",
    "Verdant Glen Pattern Grids": "10:12:33",
    "Verdant Glen Wandering Echos": "12:05:38",
    "Verdant Glen Glide Rings": "5:52:48",
    "Verdant Glen Flow Orbs": "23:33:00",
    "Verdant Glen Crystal Labyrinths": "5:27:53",
    "Verdant Glen Morphic Fractals": "9:55:51",

    "Lucent Waters Sightseers": "6:44:23",
    "Lucent Waters Matchboxes": "21:48:32",
    "Lucent Waters Light Motifs": "10:37:06",
    "Lucent Waters Hidden Cubes": "11:12:05",
    "Lucent Waters Hidden Archways": "21:40:27",
    "Lucent Waters Hidden Rings": "0:06:17",
    "Lucent Waters Hidden Pentads": "3:32:06",
    "Lucent Waters Logic Grids": "19:36:18",
    "Lucent Waters Pattern Grids": "0:31:47",
    "Lucent Waters Memory Grids": "3:53:55",
    "Lucent Waters Wandering Echos": "2:24:51",
    "Lucent Waters Glide Rings": "20:12:01",
    "Lucent Waters Flow Orbs": "13:52:13",
    "Lucent Waters Morphic Fractals": "0:15:05",

    "Autumn Falls Matchboxes": "12:37:15",
    "Autumn Falls Sightseers": "21:33:08",
    "Autumn Falls Light Motifs": "1:25:51",
    "Autumn Falls Sentinel Stones": "1:13:00",
    "Autumn Falls Hidden Cubes": "2:00:49",
    "Autumn Falls Hidden Archways": "12:29:11",
    "Autumn Falls Hidden Rings": "14:55:01",
    "Autumn Falls Hidden Pentads": "18:20:49",
    "Autumn Falls Logic Grids": "10:25:02",
    "Autumn Falls Memory Grids": "18:42:39",
    "Autumn Falls Pattern Grids": "15:20:30",
    "Autumn Falls Flow Orbs": "4:40:58",
    "Autumn Falls Wandering Echos": "17:13:35",
    "Autumn Falls Glide Rings": "11:00:44",
    "Autumn Falls Morphic Fractals": "15:03:48",
    "Autumn Falls Crystal Labyrinths": "10:35:49",

    "Shady Wildwood Matchboxes": "14:13:24",
    "Shady Wildwood Light Motifs": "3:02:00",
    "Shady Wildwood Sightseers": "23:09:17",
    "Shady Wildwood Sentinel Stones": "2:50:09",
    "Shady Wildwood Hidden Cubes": "3:36:58",
    "Shady Wildwood Hidden Rings": "16:31:10",
    "Shady Wildwood Hidden Pentads": "19:56:58",
    "Shady Wildwood Hidden Archways": "14:05:20",
    "Shady Wildwood Logic Grids": "12:01:11",
    "Shady Wildwood Memory Grids": "20:18:48",
    "Shady Wildwood Pattern Grids": "16:56:39",
    "Shady Wildwood Wandering Echos": "18:49:44",
    "Shady Wildwood Flow Orbs": "6:17:05",
    "Shady Wildwood Glide Rings": "12:36:53",
    "Shady Wildwood Crystal Labyrinths": "12:11:58",

    "Serene Deluge Light Motifs": "18:55:43",
    "Serene Deluge Matchboxes": "6:07:08",
    "Serene Deluge Sightseers": "15:03:00",
    "Serene Deluge Sentinel Stones": "18:43:53",
    "Serene Deluge Hidden Pentads": "11:50:42",
    "Serene Deluge Hidden Cubes": "19:30:42",
    "Serene Deluge Hidden Rings": "8:24:53",
    "Serene Deluge Hidden Archways": "5:59:04",
    "Serene Deluge Logic Grids": "3:54:55",
    "Serene Deluge Memory Grids": "12:12:32",
    "Serene Deluge Pattern Grids": "8:50:23",
    "Serene Deluge Flow Orbs": "22:10:50",
    "Serene Deluge Glide Rings": "4:30:36",
    "Serene Deluge Wandering Echos": "10:43:27",
    "Serene Deluge Crystal Labyrinths": "4:05:42"
}

# Read all the json files for initialization information
with open("channels.json", "r") as read_file:
    channelIds = json.load(read_file)

with open("embedMessages.json", "r") as read_file:
    embedMessageIds = json.load(read_file)

with open("roles.json", "r") as read_file:
    roleIds = json.load(read_file)

# Dictionaries for containing the processed channels and embed messages
# These will be filled in the bot ready function
channels = {}
embedMessages = {}


# Checks for commands
@bot.check
async def globally_block_non_IOI(ctx):  # Second one is for testing
    return ctx.guild.id == 1193697387827437598 or ctx.guild.id == 1205261316818731029


async def isAdmin(ctx):
    return ctx.author.guild_permissions.administrator or await bot.is_owner(ctx.author)


# Commands for setting up the embed messages
@bot.command()
@commands.check(isAdmin)
async def set_verdant_glen(ctx):
    await create_embed_timer(ctx, "Verdant Glen")


@bot.command()
@commands.check(isAdmin)
async def set_lucent_waters(ctx):
    await create_embed_timer(ctx, "Lucent Waters")


@bot.command()
@commands.check(isAdmin)
async def set_autumn_falls(ctx):
    await create_embed_timer(ctx, "Autumn Falls")


@bot.command()
@commands.check(isAdmin)
async def set_shady_wildwood(ctx):
    await create_embed_timer(ctx, "Shady Wildwood")


@bot.command()
@commands.check(isAdmin)
async def set_serene_deluge(ctx):
    await create_embed_timer(ctx, "Serene Deluge")


# Creates an embedded timer for an area
async def create_embed_timer(ctx, area):
    # Delete the message that called this function
    await ctx.message.delete()

    # Create the embed message and get the current time
    embedVar = discord.Embed(title=area + " Timers", color=0x336EFF)
    currentTime = datetime.datetime.utcnow() - datetime.timedelta(hours=6)

    # For each puzzle, calculate the time left til update and add it to the embed
    for puzzle in acceptedPuzzles[area]:
        seconds = (datetime.datetime.strptime(puzzleTimes[area + " " + puzzle], '%H:%M:%S')
                   - currentTime).seconds

        timeString = convertSecondsToString(seconds)

        embedVar.add_field(name=puzzle, value=timeString, inline=True)

    # Fix weird spacing
    # TODO: This will need to be changed on release
    if area == "Lucent Waters":
        embedVar.add_field(name="", value="", inline=True)

    # Send the embedded message
    embeddedMessage = await ctx.channel.send(embed=embedVar)

    # Get the embedded message's channel id and message id to retrieve it later
    embedMessageIds[area + " Channel"] = ctx.channel.id
    embedMessageIds[area] = embeddedMessage.id

    # Update the embedMessages dictionary too
    channel = bot.get_channel(embedMessageIds[area + " Channel"])
    embedMessages[area] = await channel.fetch_message(embedMessageIds[area])

    # Save it to a json
    with open("embedMessages.json", "w") as write_file:
        json.dump(embedMessageIds, write_file)


# Takes a number of seconds and converts it to number of hours and minutes away in XXh XXm format
def convertSecondsToString(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    timeString = "{:d}h {:d}m".format(hours, minutes)

    if hours == 0 and minutes == 0:
        timeString = "Refreshing Now!"

    return timeString


# Adds the passed role to the user
# If the role doesn't exist yet, create it
@bot.command()
async def add_role(ctx, *args):
    # Make sure the correct number of arguments were passed
    if len(args) != 2:
        await ctx.channel.send(f"{ctx.author.mention}\n"
                               f"This command is used to add a pingable role to yourself for a specific puzzle.\n"
                               f"`$add_role \"area\" \"puzzle\"`\n"
                               f"The quotes and capitalization are necessary.")
        return

    # Assign the arguments
    area = args[0]
    puzzle = args[1]

    # Check that the area is valid
    if area not in puzzleAreas:
        await ctx.channel.send(f"{ctx.author.mention}\nThat is not a valid area. Valid areas are: \"Verdant Glen\", "
                               f"\"Lucent Waters\", \"Autumn Falls\", \"Shady Wildwood\", and \"Serene Deluge\"."
                               f"\nRemember quotes and capitalization.")
        return

    # Check that the puzzle is in the area
    if puzzle not in acceptedPuzzles[area]:
        await ctx.channel.send(f"{ctx.author.mention}\nThat is not a valid area.\n"
                               f"Valid areas for {area} are: {acceptedPuzzles[area]}\n"
                               f"Remember to use double quotes and capitalization.")
        return

    # Check if the role already exists
    try:
        roleId = roleIds[area + " " + puzzle]
        role = ctx.guild.get_role(roleId)
        await ctx.author.add_roles(role)
        await ctx.channel.send(f"Role Added! {ctx.author.mention}")
        return
    except KeyError:
        pass

    # If it doesn't exist, create it, add it to the user, and save its id
    role = await ctx.guild.create_role(name=area + " " + puzzle)
    roleId = role.id
    await ctx.author.add_roles(role)
    await ctx.channel.send(f"Role Added! {ctx.author.mention}")

    roleIds.update({area + " " + puzzle: roleId})
    with open("roles.json", "w") as write_file:
        json.dump(roleIds, write_file)


# Removes a passed role from the user
# If that user was the last user with the role, delete the role
@bot.command()
async def remove_role(ctx, *args):
    # Make sure the correct number of arguments were passed
    if len(args) != 2:
        await ctx.channel.send(f"{ctx.author.mention}\n"
                               f"This command is used to remove a pingable role from yourself.\n"
                               f"`$remove_role \"area\" \"puzzle\"`\n"
                               f"Quotes and capitalization are necessary.")
        return

    # Assign the arguments
    area = args[0]
    puzzle = args[1]

    # Check that the area is valid
    if area not in puzzleAreas:
        await ctx.channel.send(f"{ctx.author.mention}\nThat is not a valid area. Valid areas are: \"Verdant Glen\", "
                               f"\"Lucent Waters\", \"Autumn Falls\", \"Shady Wildwood\", and \"Serene Deluge\"."
                               f"\nRemember to use double quotes and capitalization.")
        return

    # Check that the puzzle is in that area
    if puzzle not in acceptedPuzzles[area]:
        await ctx.channel.send(f"{ctx.author.mention}\nThat is not a valid area.\n"
                               f"Valid areas for {area} are: {acceptedPuzzles[area]}\n"
                               f"Remember to use double quotes and capitalization.")
        return

    # Make sure the role exists
    try:
        roleId = roleIds[area + " " + puzzle]
        role = ctx.guild.get_role(roleId)
        try:
            # If it does, remove the role and continue past this try statement
            await ctx.author.remove_roles(role)
            await ctx.channel.send(f"Role Removed! {ctx.author.mention}")
        except discord.HTTPException:
            # If it doesn't, print a message and exit
            await ctx.channel.send(f"Role remove failed. {ctx.author.mention}")
            return

        # If that was the last user with the role, delete the role
        if len(role.members) == 0:
            await role.delete()

            # and remove it from the json / dictionary
            del roleIds[area + " " + puzzle]
            with open("roles.json", "w") as write_file:
                json.dump(roleIds, write_file)

    except KeyError:
        await ctx.channel.send(f"That role doesn't exist. {ctx.author.mention}")


# Sends generic help information to the chat
@bot.command()
async def help_me(ctx):
    embedVar = discord.Embed(title="Help", color=0x336EFF)
    messageContent = ("```I keep track of Islands of Insight puzzle timers!\n"
                      "My commands:\n"
                      "-- $add_role (type me in chat for how to use)\n"
                      "-- $remove_role (type me in chat for how to use)\n"
                      "If you have any suggestions to add to me, create a ticket to ask the server admins!\n"
                      "If you find any bugs, message seasonsveil on Discord.```")
    embedVar.add_field(name="", value=messageContent)
    await ctx.channel.send(embed=embedVar)


# Sends admin help information to the chat
@bot.command()
@commands.check(isAdmin)
async def help_admin(ctx):
    embedVar = discord.Embed(title="Help", color=0x336EFF)
    messageContent = ("```My commands only work in the official test server and the IOI Fan Server.\n"
                      "The following commands can only be used by people with administrator permissions.\n"
                      "Admin commands:\n"
                      "-- $set_verdant_glen\n"
                      "-- $set_lucent_waters\n"
                      "-- $set_autumn_falls\n"
                      "-- $set_shady_wildwood\n"
                      "-- $set_serene_deluge\n"
                      "Note: There can only be 1 of each area's embed message at a time. If you make a new one, "
                      "you probably want to delete the old one as it will no longer function.\n"
                      "If you want to move a 'spam' channel, ask seasonsveil as it would be more work than "
                      "it is worth to make that happen through commands.```")
    embedVar.add_field(name="", value=messageContent)
    await ctx.channel.send(embed=embedVar)


# Loop that checks to send out refresh messages
@tasks.loop(seconds=60.0)
async def checkTime():
    # Send messages for each ready puzzle
    # Get the current time and store it as a string
    time = datetime.datetime.utcnow() - datetime.timedelta(hours=6)
    timeString = "{:d}:{:02d}".format(time.hour, time.minute)

    # For each area and each puzzle in that area
    for area in puzzleAreas:
        # Get the channel to send the message
        botChannel = channels[area]
        for puzzle in acceptedPuzzles[area]:
            currentPuzzle = area + " " + puzzle
            # Check if it is time for this message to be sent
            if puzzleTimes[currentPuzzle][:-3] == timeString:  # TODO: Check to make sure this works for midnight to 1
                # Check if there is anyone with the role to ping
                try:
                    roleId = roleIds[area + " " + puzzle]
                    role = botChannel.guild.get_role(roleId)
                    await botChannel.send(f"{currentPuzzle} have refreshed! {role.mention}")
                except KeyError:
                    await botChannel.send(currentPuzzle + " have refreshed!")


# Updates stored embedded messages
@tasks.loop(seconds=30.0)
async def updateEmbeds():
    # Get the current time
    currentTime = datetime.datetime.utcnow() - datetime.timedelta(hours=6)

    # For each area
    for area in puzzleAreas:
        # Get the embedded message
        message = embedMessages[area]
        embed = message.embeds[0]

        index = 0

        # Update each puzzle in the message
        for puzzle in acceptedPuzzles[area]:
            seconds = (datetime.datetime.strptime(puzzleTimes[area + " " + puzzle], '%H:%M:%S')
                       - currentTime).seconds

            timeString = convertSecondsToString(seconds)

            embed.set_field_at(index=index, name=puzzle, value=timeString, inline=True)

            index += 1

        # Send the update
        await message.edit(embed=embed)
        await sleep(3.5)  # Only here to avoid the rate limit warning clogging the console; completely unnecessary


# When the bot is ready, start the main loop
@bot.event
async def on_ready():
    # Convert the channels and embed message ids into actual objects
    # The channels will only ever be defined here, so if you change the channel json,
    # you'll have to rerun the program for the changes to come into effect
    # The embed messages can be changed through the set commands
    for area in puzzleAreas:
        channels.update({area: bot.get_channel(channelIds[area])})

        channel = bot.get_channel(embedMessageIds[area + " Channel"])
        embedMessages.update({area: await channel.fetch_message(embedMessageIds[area])})

    updateEmbeds.start()
    await sleep(20)
    checkTime.start()


bot.run(os.environ['TOKEN'])
