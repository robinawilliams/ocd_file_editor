# O.C.D. File Renamer

## Overview
O.C.D. File Renamer is a Python tool designed to dynamically rename files. This tool provides a graphical user interface (GUI) for easy file manipulation and renaming.

## Installation
1. **Clone the Repository:**
    ```
    git clone https://github.com/robinawilliams/ocd_file_renamer.git
    ```

2. **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```

3. **Install Tkinter:**
   - Arch: `sudo pacman -S tk`
   - Debian: `sudo apt-get install tk`
   - Fedora: `sudo dnf install tk`

4. **Configure the Configuration File:**
   - Customize the configuration file "config.ini" as needed.

## Usage
### Running the Project
- Execute the command:
    ```
    python gui.py
    ```

### Quick Start
1. Drag and drop a file into the window or choose "Browse File" to select one.
2. Use category buttons to add words to the renaming queue.
3. Type in the custom text entry field to add custom words.
4. Click "Rename Files" to confirm changes.
5. Use "Undo" to revert the last category added.
6. Use "Clear" to remove everything **including the selected file.
7. Manage categories with "Add Category" and "Remove Category" fields.
8. "Move to Trash" sends the selected file to the trash.
9. "Select Last Used File" reloads the last used file.

### Checkboxes/Radio Buttons
- "Reset Output Dir." resets the output directory on each run.
- "Suggest Output Dir." attempts to find an artist match in a provided directory.
- "Move Up One Dir." moves the file up one directory.
- "Move Text" moves text within special characters to the end of the file.
   - Use " - " and "\_\_-\_\_" in the preprocessed file name. For example, "Artist - WORDS TO MOVE__-__ .mp3"
- "Placement" determines where to place words in the renaming process.
   - Prefix: At the beginning of the file name.
   - First Dash: At the first dash found in the file name (Will revert to Suffix if no dash is found).
   - Suffix: At the end of the file name.

### Detailed Features
- Weight categories in the "categories.json" file.
- "Open File on Drag and Drop" (Linux only).
- "Remove Duplicates" removes duplicate entries in the file name.
- "Create Double Check Reminder" creates an empty file for double-checking.
- "Activate Logging" logs actions taken within the program.

### Configuration File
- Use "config.ini.template" as a template for configuring the tool.

## Bug Reports and Contributions
If you encounter issues or want to contribute, use the "Issues" tab. For PRs, reference the related issue.

## Known Issues
This project is a work in progress. Check the issues section for known problems.

## Show Your Support
If you like this project, please share it.

## FAQ
**Q: I get the error "import _tkinter # If this fails, your Python may not be configured for Tk". How do I resolve this?

A: Install tkinter.
   - Arch: `sudo pacman -S tk`
   - Debian: `sudo apt-get install tk`
   - Fedora: `sudo dnf install tk`
