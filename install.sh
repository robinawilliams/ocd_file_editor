#!/usr/bin/env bash

# Logging function
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1"
}

# Function to handle errors
handle_error() {
    log "Error: $1" >&2
    exit 1
}

# Check for Python3 and venv
if ! command -v python3 >/dev/null 2>&1; then
    handle_error "Python3 is not installed."
fi

if ! command -v python3 -m venv >/dev/null 2>&1; then
    handle_error "Python3 venv module is not installed."
fi

# Check for dependencies
if ! command -v sudo >/dev/null 2>&1 || [ "$(id -u)" -eq 0 ]; then
    handle_error "This script requires sudo or elevated permissions."
fi

# Check if in the directory of the git repository
if [ ! -d ".git" ]; then
    handle_error "Not in the directory of the git repository."
fi

# Change directories if not already there
cd "$(dirname "$0")" || handle_error "Unable to change to script directory."

# Git pull
if git diff-index --quiet HEAD --; then
    if ! git pull; then
        handle_error "Unable to pull from the git repository."
    fi
else
    log "Local changes exist. Skipping git pull."
fi

# Check if venv already exists
if [ ! -d "venv" ]; then
    # Set up Python virtual environment
    python3 -m venv venv || handle_error "Unable to create Python virtual environment."
fi

# Check if the environment is already activated
if [ -z "${VIRTUAL_ENV}" ]; then
    # Activate virtual environment
    if ! source venv/bin/activate; then
        handle_error "Unable to activate virtual environment."
    fi
fi

# Install requirements
if ! pip install -r requirements.txt; then
    handle_error "Unable to install Python requirements."
fi

# Check if Tkinter is installed
if ! python3 -c 'import tkinter' 2>/dev/null; then
    # Check Linux flavor
    if [ -f "/etc/arch-release" ]; then
        # Arch Linux (pacman)
        sudo pacman -S tk || handle_error "Unable to install Tkinter."
    elif [ -f "/etc/debian_version" ]; then
        # Debian-based (apt-get)
        sudo apt-get install -y tk || handle_error "Unable to install Tkinter."
    elif [ -f "/etc/fedora-release" ]; then
        # Fedora (dnf)
        sudo dnf install -y tk || handle_error "Unable to install Tkinter."
    else
        handle_error "Unsupported Linux distribution."
    fi
fi

# Copy template files
copy_template() {
    if [ ! -e "$1" ]; then
        cp "$2" "$1" || handle_error "Unable to copy $2 to $1."
    fi
}

copy_template "config.ini" "config.ini.template"
copy_template "list_of_artists.txt" "list_of_artists.txt.template"

# Run GUI in the background
if ! python gui.py & disown; then
    handle_error "Unable to run GUI."
fi

# Deactivate virtual environment when done
if ! deactivate; then
    handle_error "Unable to deactivate virtual environment."
fi

log "Script execution completed successfully."
