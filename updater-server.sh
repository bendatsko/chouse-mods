#!/bin/bash

# Function to check for updates and update mods folder
check_for_updates() {
    # Get the latest commit hash from the repository
    latest_commit=$(git ls-remote https://github.com/bendatsko/chouse-mods.git HEAD | cut -f1)

    # If the latest commit hash is different from the stored one, update mods folder
    if [ "$latest_commit" != "$last_commit" ]; then
        echo "Detected update. Updating mods folder..."

        # Remove the existing chouse-mods directory if it exists
        if [ -d "$SCRIPT_DIR/chouse-mods" ]; then
            rm -rf "$SCRIPT_DIR/chouse-mods"
        fi

        # Clone the repository to the same directory as the script
        git clone https://github.com/bendatsko/chouse-mods.git "$SCRIPT_DIR/chouse-mods"

        # Clear the mods folder
        rm -rf "$SCRIPT_DIR/mods"/*

        # Move the contents of chouse-mods/mods to the mods folder in the same directory as the script
        mv "$SCRIPT_DIR/chouse-mods/mods"/* "$SCRIPT_DIR/mods"

        echo "Mods updated."
        
        # Update the stored commit hash
        last_commit="$latest_commit"
    fi
}

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Initialize the last_commit variable with an empty string
last_commit=""

# Infinite loop to continuously check for updates every 5 seconds
while true; do
    # Call the function to check for updates
    check_for_updates

    # Wait for 5 seconds before checking again
    sleep 5
done
