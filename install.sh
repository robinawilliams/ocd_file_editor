#!/usr/bin/env bash

# Script to setup and run the application

# Function to handle errors
handle_error() {
    echo "Error: $1" >&2
    exit 1
}

# Copy template files
copy_template() {
    if [ ! -f "$1" ]; then
        cp "$2" "$1" || handle_error "Unable to copy $2 to $1."
    fi
}

# Check for Python3 and venv
command -v python3 >/dev/null 2>&1 || handle_error "Error: Python3 is not installed."
command -v python3 -m venv >/dev/null 2>&1 || handle_error "Error: Python3 venv module is not installed."

# Check if in the directory of the git repository
if [ ! -d ".git" ]; then
    handle_error "Error: Not in the directory of the git repository."
fi

# Change directories if not already there
cd "$(dirname "$0")" || handle_error "Error: Unable to change to script directory."

# Git pull
if ! git pull; then
    handle_error "Error: Unable to pull from the git repository."
fi

# Check if venv already exists
if [ ! -d "venv" ]; then
    # Set up Python virtual environment
    python3 -m venv venv || handle_error "Error: Unable to create Python virtual environment."
fi

# Activate virtual environment
if ! source venv/bin/activate; then
    handle_error "Error: Unable to activate virtual environment."
fi

# Install requirements
if ! pip install -r requirements.txt; then
    handle_error "Error: Unable to install Python requirements."
fi

# Check for dependencies
if ! command -v sudo >/dev/null 2>&1; then
    handle_error "Error: sudo command not found. This script requires sudo to install Tkinter."
fi

# Check if Tkinter is installed
if ! python3 -c 'import tkinter' 2>/dev/null; then
    # Check Linux flavor
    if [ -f "/etc/arch-release" ]; then
        # Arch Linux (pacman)
        sudo pacman -S tk || handle_error "Error: Unable to install Tkinter."
    elif [ -f "/etc/debian_version" ]; then
        # Debian-based (apt-get)
        sudo apt-get install -y tk || handle_error "Error: Unable to install Tkinter."
    elif [ -f "/etc/fedora-release" ]; then
        # Fedora (dnf)
        sudo dnf install -y tk || handle_error "Error: Unable to install Tkinter."
    else
        handle_error "Error: Unsupported Linux distribution."
    fi
fi

copy_template "config.ini" "config.ini.template"
copy_template "list_of_artists.txt" "list_of_artists.txt.template"

# Run GUI
if ! python gui.py; then
    handle_error "Error: Unable to run GUI."
fi

# Deactivate virtual environment when done
if ! deactivate; then
    handle_error "Error: Unable to deactivate virtual environment."
fi
