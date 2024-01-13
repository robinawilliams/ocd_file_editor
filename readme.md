# O.C.D. File Renamer

## Overview
Introducing the O.C.D. File Renamer, a powerful Python tool crafted for dynamic file renaming. Boasting a user-friendly graphical interface (GUI), this tool simplifies file manipulation and renaming, making the process effortless and efficient.

## Installation
1. **Clone the Repository:**
    ```
    git clone https://github.com/robinawilliams/ocd_file_renamer.git
    ```

2. **Change Directories:**
    ```
    cd ocd_file_renamer
    ```
   
3. **Install Method (Automatic Install):**
   1. **Run Install Script:**
       ```
       ./install.sh
       ```
   
2. **Install Method (Manual Install):**
   1. **Install Dependencies:**
       ```
       pip install -r requirements.txt
       ``` 
   3. **Install Tkinter:**
      - Arch: `sudo pacman -S tk`
      - Debian: `sudo apt-get install tk`
      - Fedora: `sudo dnf install tk`

   4. **Configure the template files:**
      - Customize the configuration file "config.ini.template" as needed and remove the .template extension.
      - Customize the list of artists file "list_of_artists.txt.template" as needed and remove the .template extension.

## Usage
### Running the Project
- Execute the command:
    ```
    python gui.py
    ```

### Quick Start
- Drag and drop a file into the window or choose "Browse File" to select one.
- Use category buttons to add words to the renaming queue.
- Manage categories with "Add Category" and "Remove Category" fields. Add a weight to the category to influence position. The lower weight, the highter the precedence.
- Choose "Output Directory" to select the output folder. Leave blank to default to current directory.
- Type in the custom text entry field to add custom text to the renaming queue.
- Click "Rename Files" to confirm changes.
- Use "Undo" to revert the last category added.
- Use "Clear" to remove everything.
- "Move to Trash" sends the selected file to the trash.
- "Reload Last File" reloads the last used file.

### Checkboxes/Radio Buttons
- "Reset Output Dir." resets the output directory on each run.
- "Suggest Output Dir." attempts to find an artist match in a provided directory.
- "Move Up One Dir." moves the file up one directory.
- "Move Text" moves text within special characters to the end of the file.
   - Use " - " and "\_\_-\_\_" in the preprocessed file name. For example, "Artist - WORDS TO MOVE__-__ .mp3"
- "Placement" determines where to place words in the renaming process.
   - Prefix: At the beginning of the file name.
   - Special Character: At the first special character found in the file name (Will revert to Suffix if no special character is found).
     - Special Character is set to - by default. See special_character_var in config.ini to change.
   - Suffix: At the end of the file name.

### Detailed Features
- Weight categories in the gui or "categories.json" file.
- "Open File on Drag and Drop" (Linux only).
- "Remove Duplicates" removes duplicate entries in the file name.
- "Create Double Check Reminder" creates an empty file for double-checking.
- "Activate Logging" logs actions taken within the program.
- Name Normalizer 
  - Name Normalize a folder containing files. You can include certain file types by changing file_extensions in the config.ini file.
  - "Remove symbols"
  - "Append "\_\_-\_\_ " to the file name"
  - "Remove text following the first '('"
  - "Remove text following the first '#'"
  - "Remove New"
  - "Remove dashes"
  - "Remove endashes"
  - "Remove emdashes"
  - "Remove ampersands"
  - "Remove @"
  - "Remove underscores"
  - "Remove commas"
  - "Remove quotes"
  - "Titlefy the name"
  - "Artist Search"
  - "Include subdirectories"
  - "Reset entries"
  - "Output Directory"
  - "Artist File"
  - "Clear"
  - "Normalize Folder"

### Files
- Use "config.ini.template" as a template for configuring the tool. Remove the .template extension to use.
- Use "list_of_artists.txt.template" as a template for the artist search feature. Remove the .template extension to use.

## Bug Reports and Contributions
If you encounter issues or want to contribute, use the "Issues" tab. For PRs, reference the related issue.

## Known Issues
This project is a work in progress. Check the issues section for known problems.

## Show Your Support
If you like this project, please share it.

## FAQ
**Q: I get the error "import _tkinter # If this fails, your Python may not be configured for Tk". How do I resolve this?**

A: Install tkinter.
   - Arch: `sudo pacman -S tk`
   - Debian: `sudo apt-get install tk`
   - Fedora: `sudo dnf install tk`

**Q: I get the error "import customtkinter as ctk  # Customtkinter for a modern gui
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'customtkinter'". How do I resolve this?**

A: The requirements haven't been installed. Install the requirements and try again.
   - `pip install -r requirements.txt`
