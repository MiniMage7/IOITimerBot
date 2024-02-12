# IOITimerBot
#### Discord bot that keeps track and notifies users when puzzles refresh

## Important Information
A few things of the bot are hard coded. The bot will only currently function in the IOI fan server and a test server. The channels that the bot sends it "Puzzle has refreshed!" are set whenever the bot starts from channels.json. The roles.json and embedMessages.json store the pingable role ids and embed messages so that if the bot turns off, all the information is stored, and it can restart without any issues. You should never have to mess with these.

## Normal Commands

### $help_me
Sends a message in chat that provides some information about the following commands.

### $add_role and $remove_role
Adds or removes a pingable role from the user. (If the user wants to be pinged for Verdant Glen Hidden Cubes, they would do `$add_role "Verdant Glen" "Hidden Cubes"`)  
Doing just `$add_role` or `$remove_role` will explain how to use the command.  
Doing `$add_role` with an invalid area i.e. `$add_role "test" "test"` will print out all the valid areas.  
Doing `$add_role` with a valid area but invalid puzzle will list all puzzles that can be done for the area. i.e. `$add_role "Verdant Glen" "test"`  
If there are no users with a pingable role after `$remove_role` is called, it is deleted. It will be remade if someone else calls `$add_role` for the role again.