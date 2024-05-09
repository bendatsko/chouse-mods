# CHouse Client-Server Mod-Sync


To install mods on the server notify clients of an update, commit your updated `mods` folder to the `master` branch. 

## Client
Place `updater-client.py` in `.minecraft` folder. Double click before pressing "play game" in the launcher.


## Server stuff
Start server
`sudo screen -dm bash ServerStart.bat`

Start server mod updater
`sudo screen -dm bash updater-server.sh`
