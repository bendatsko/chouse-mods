#!/bin/bash

#check for updates and update mods folder
check_for_updates() {
    # the latest commit hash from repository
    latest_commit=$(git ls-remote https://github.com/bendatsko/chouse-mods.git HEAD | cut -f1)

    # If latest commit hash is different from the stored one update mods folder
    if [ "$latest_commit" != "$last_commit" ]; then
        echo "Detected update. Updating mods folder..."

        # remove existing chouse-mods directory if exists
        if [ -d "$SCRIPT_DIR/chouse-mods" ]; then
            rm -rf "$SCRIPT_DIR/chouse-mods"
        fi

        git clone https://github.com/bendatsko/chouse-mods.git "$SCRIPT_DIR/chouse-mods"
        rm -rf "$SCRIPT_DIR/mods"/*
        mv "$SCRIPT_DIR/chouse-mods/mods"/* "$SCRIPT_DIR/mods"

        echo "Mods updated."
        
        # update stored commit hash
        last_commit="$latest_commit"
    fi
}

# get directory where script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# initialize last_commit with empty string
last_commit=""

# infinite loop to continuously check for updates every 5 seconds
while true; do
    # call the function to check for updates
    check_for_updates

    # wait for 5 seconds before checking again
    sleep 5
done
