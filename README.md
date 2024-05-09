# CHouse Client-Server Mod-Sync


To install mods on the server notify clients of an update. To update the modpack, commit your updated `mods` folder (aka the modpack) to the `master` branch. 

# ALL MODS MUST BE COMPATIBLE WITH FORGE 14.23.5.2860

## Client
1. Go into Curseforge and click on and "open folder".
2. Place `updater-client.py` in the folder it takes you to. There should already be a mods folder in there.
3. Whenever someone says they've updated the modpack, run `updater-client.py` with python.
4. Now press play in your minecraft launcher and press "play game". If something is wrong, that's probably not good. 


## Server stuff
Start server
`sudo screen -dm bash ServerStart.bat`

Start server mod updater
`sudo screen -dm bash updater-server.sh`
