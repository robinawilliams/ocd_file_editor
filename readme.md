# O.C.D. File Editor

## Overview
Introducing the O.C.D. File Editor, a powerful Python tool crafted for dynamic file editing. Boasting a user-friendly graphical interface (GUI), this tool simplifies file manipulation and renaming, making the process effortless and efficient.

## Installation
1. **Clone the Repository:**
    ```
    git clone https://github.com/robinawilliams/ocd_file_editor.git
    ```

2. **Change Directories:**
    ```
    cd ocd_file_editor
    ```
   
3. **Install Method (Automatic Install):**
   1. **Run Install Script:**
       ```
       ./install.sh
       ```
   
4. **Install Method (Manual Install):**
   1. **Install Dependencies:**
       ```
       pip install -r requirements.txt
       ``` 
   2. **Install Tkinter:**
      - Arch: `sudo pacman -S tk`
      - Debian: `sudo apt-get install tk`
      - Fedora: `sudo dnf install tk`

   3. **Configure the template files:**
      - Customize the configuration file "config.ini.template" as needed and remove the .template extension.
      - Customize the list of artists file "list_of_artists.txt.template" as needed and remove the .template extension.

## Usage
### Running the Project
- Execute the command:
    ```
    python gui.py
    ```
## Modules
### File Renamer
Rename files (or folders)
- Drag and drop a file into the window or choose "Browse File" to select one.
- Categories:
  - Use tabs to separate the categories by weight or show all categories.
  - Use category buttons to add words to the renaming queue.
  - Click the same category button again to remove words from the renaming queue.
- Choose "Output Directory" to select the output folder. Leave blank to default to current directory.
- Type in the custom text entry field to add custom text to the renaming queue.
- Click "Rename File" to rename the file with the changes in the queue.
- Use "Undo" to revert the last category added to the queue.
- Use "Clear" to remove everything.
- "Move to Trash" sends the selected file to the trash.
- "Reload Last File" reloads the last used file.
- "Send to Video Editor" sends the selected file to the Video Editor module.
- "Send to Name Normalizer" sends the selected file to the Name Normalizer module.

Checkboxes/Radio Buttons
- "Placement" determines where to place words in the renaming process.
   - Prefix: At the beginning of the file name.
   - Special Character: At the first special character found in the file name.
     - Special Character is set to - by default. See special_character_var in config.ini to change.
     - This will revert to Suffix if no special character is found.
   - Suffix: At the end of the file name.
- "Reset Output Dir." resets the output directory on each run.
- "Suggest Output Dir." attempts to find an artist in the file and matching folder in the Artist Directory.
- "Move Up One Dir." moves the file up one directory.
  - This overrides "Suggest Output Dir."
- "Move Text" moves text within special characters to the end of the file.
   - Use " - " and "\_\_-\_\_" in the preprocessed file name. For example, "Artist - WORDS TO MOVE__-__ .mp3"

### Name Normalizer 
Name Normalize a file or folder containing files for easy use with File Renamer. You can include certain file types by changing file_extensions in the dictionary.json file.
  - Drag and drop a file/folder into the window or choose "Browse" to select one.
  - "Append "\_\_-\_\_ " to the file name"
  - "Artist Search"
  - "Include subdirectories"
  - "Remove @"
  - "Remove all symbols"
  - "Remove most symbols"
  - "Remove ampersands"
  - "Remove angle brackets"
  - "Remove asterisks"
  - "Remove backslashes"
  - "Remove carets"
  - "Remove colons"
  - "Remove commas"
  - "Remove curly braces"
  - "Remove dashes"
  - "Remove dollars"
  - "Remove double quotes"
  - "Remove double spaces"
  - "Remove emdashes"
  - "Remove endashes"
  - "Remove equal signs"
  - "Remove hashtags"
  - "Remove new"
  - "Remove non-ASCII symbols"
  - "Remove numbers"
  - "Remove parenthesis"
  - "Remove percents"
  - "Remove pipes"
  - "Remove plus signs"
  - "Remove question marks"
  - "Remove semicolons"
  - "Remove single quotes"
  - "Remove square brackets"
  - "Remove text following the first '#'"
  - "Remove text following the first '('"
  - "Remove underscores"
  - "Reset entries"
  - "Titlefy the name"
  - "Output Directory"
  - "Clear"
  - "Reload Last File"
  - "Preview"
  - "Normalize"
  - "Send to File Renamer" sends the selected file to the File Renamer module.
  - "Send to Video Editor" sends the selected file to the Video Editor module.

### Video Editor
Make basic edits to videos.
- Drag and drop a file/folder into the window or choose "Browse" to select an input method (video file, .txt file containing file paths, or a directory with video files to edit.)
- "Rotate Video" determines how much to rotate the video ("Left", "Right", "Flip"). Use "None" to disable rotation.
- "Increase Audio (dB)" determines how much to amplify the audio, e.g. "5.0" for 5 decibels.
- "Normalize Audio" determines how much to normalize the audio, e.g. "0.9" for 0.9 audio normalization.
- "Trim (Minutes:Seconds)" determines how much to trim the video, e.g. "01:05" to trim one minute and five seconds from the video.
- "Output Directory" to select the output directory for the file(s). Default is the initial directory of the file if none is explicitly provided.
- "Clear" to clear all entries in the frame.
- "Reload Last File" reloads the last used file.
- "Process video(s)" to process video files in the provided input method.
- "Send to File Renamer" sends the selected file to the File Renamer module.
- "Send to Name Normalizer" sends the selected file to the Name Normalizer module.
- "Remove successful lines from input file" to remove the successful lines from the input file.
- "Reset entries" after successful processing.

### Add/Remove
Add or remove artists from the Artist File in the GUI.
- "Add Artist" to add artists to the Artist File.
- "Remove Artist" to remove artists to the Artist File.
- "Clear" to clear all entries in the frame.
- "Reset entries" resets the entries after adding/removing artists.

Add or remove categories from the Dictionary file in the GUI.
- Manage categories with "Add Category" and "Remove Category" fields. Add a weight to the category to influence position. The lower weight, the higher the precedence.

Flag an artist as no-go in the GUI.
- Manage NO-GO with "Add NO-GO" field.

Add an excluded folder from the Artist Directory in the GUI.
- Manage Exclusions with "Add Exclude" field.

### Settings
Change basic settings for this session within the GUI. Change variables in the config.ini file to persist between sessions. 
- "Open File on Drag and Drop" (Linux only).
- "Remove Duplicates" removes duplicate entries in the file name.
- "Artist Identifier" attempts to identify the artist in other folders while conducting file renaming operations.
- "Create Double Check Reminder" creates an empty file for double-checking.
- "Activate Logging" logs actions taken within the program.
- "Suppress Standard Output/Error" will supress the outputs to the console and redirect them to the log file.
- "Show Messageboxes" displays messagebox notifications. False defaults to standard messaging in the frame.
- "Show Confirmation Messageboxes" displays confirmation messagebox notifications. False defaults to standard messaging in the frame. Confirmation messageboxes will always be displayed.
- "Fallback confirmation state" sets what the response is when confirmation messagebox notifications are suppressed.
- "Use Custom Tab Names" sets the tab names you set in the Dictionary.json file.
- "Sort Tab Names" sorts the tab names.
- "Sort Tab Names (A-Z / Z-A)" sorts the tab names alphabetically or reverse alphabetically.
- "Appearance" switches between light and dark mode. 
- "UI Scaling" switches between different scaling sizes for the user interface. 
- "Initial Directory" sets the initial directory when the user browses for an input.
- "Initial Output Directory" sets the initial directory when the user browses for an output directory. 
  - This may be overriden by "Suggest Output Dir."
- "Double Check Reminder Directory" sets the directory that reminders are saved to, if enabled.
- "Artist Directory" sets the directory that "Suggest Output Directory" uses to find a match for an artist.
- "Artist File" set the line delimited list of artists file that "Artist Search" uses to find a match for an artist.
- "Open Config File" open the configuration file for editing in the default system program.


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
