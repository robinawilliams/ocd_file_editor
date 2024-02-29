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
      - Customize the json file "dictionary.json.template" as needed and remove the .template extension.
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
- Type in the prefix text entry field to add custom text as a prefix to the renaming queue.
- Type in the custom text entry field to add custom text to the renaming queue.
- Click "Rename" to rename the file with the changes in the queue.
- Use "Undo" to revert the last category added to the queue.
- Use "Undo File Rename" to revert the last file rename operation.
- Use "Clear" to remove everything.
- "Move to Trash" sends the selected file to the trash.
- "Reload Last File" reloads the last used file.
- "Send to Video Editor" sends the selected file to the Video Editor module.
- "Send to Name Normalizer" sends the selected file to the Name Normalizer module.

Checkboxes/Radio Buttons
- "Placement" determines where to place words in the renaming process.
    - Prefix: At the beginning of the file name {prefix_text} {custom_text} {categories_text} {base_name}.
    - Special Character: At the first special character found in the file name {prefix_text} {left side of -}
      {categories_text} {custom_text} {right side of -}
     - Special Character is set to - by default. See special_character_var in config.ini to change.
    - This will revert to {prefix_text} {categories_text} {custom_text} {base_name} if no special character is found.
    - Suffix: At the end of the file name {prefix_text} {base_name} {categories_text} {custom_text}.
- "Reset Output Dir." resets the output directory on each run.
- "Suggest Output Dir." attempts to find an artist in the file and matching folder in the Artist Directory.
- "Move Up One Dir." moves the file up one directory.
  - This overrides "Suggest Output Dir."
- "Move Text" moves text within special characters to the end of the file.
   - Use " - " and "\_\_-\_\_" in the preprocessed file name. For example, "Artist - WORDS TO MOVE__-__ .mp3"
- "Add Artist Common Categories" common categories for the artist to the queue, e.g. Taylor Swift (Country, Pop).

### Name Normalizer 
Name Normalize a file or folder containing files for easy use with File Renamer. You can include certain file types by changing file_extensions in the dictionary.json file.
  - Drag and drop a file/folder into the window or choose "Browse" to select one.
- "Append \_\_-\_\_"
- "Artist Identifier"
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
- "Remove custom text"
  - "Remove dashes"
  - "Remove dollars"
  - "Remove double quotes"
  - "Remove emdashes"
  - "Remove endashes"
  - "Remove equal signs"
- "Remove extra whitespaces"
  - "Remove hashtags"
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
- "Remove text following the first '('"
  - "Remove text following the first '#'"
  - "Remove underscores"
  - "Reset entries"
  - "Titlefy the name"
  - "Output Directory"
- "Remove Text"
  - "Clear"
- "Undo Name Normalizer"
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

Artist
- "Add Artist" to add artists to the Artist File.
- "Remove Artist" to remove artists to the Artist File.
- "Browse Artist" to select the artist to add/remove common categories to.
- "Detect Artist" to detect the artist in the selected file in the File Renamer module.
- "Add A.C.C." to add a common category to the artist's list.
- "Remove A.C.C." to remove a common category from the artist's list.

Category
- Manage categories with "Add Category" and "Remove Category" fields. Add a weight to the category to influence position. The lower weight, the higher the precedence.

Custom Tab Name

- "Add Custom Tab" to add a custom tab name for the corresponding weight.
- "Remove Custom Tab" to remove a custom tab name.

Custom Text to Replace

- "Add CTR" to add a custom text to replace record in the dictionary.
- "Replace with" to provide text to replace. If left empty, the text is replaced with an empty string.
- "Remove CTR" to remove the custom text to replace record in the dictionary.

Exclude

- "Add Exclude" to add a folder to be excluded from the Suggest Output Directory search.
- "Remove Exclude" to remove a folder to be excluded from the Suggest Output Directory search.

File Extensions

- "Add File Ext." to add a file extension to the list of file extensions for the Name Normalizer to operate on.
- "Remove File Ext." to remove a file extension from the list of file extensions for the Name Normalizer to operate on.

NO-GO

- "Add NO-GO" to create a no-go file for the artist and optionally add it to the txt file for use with tampermonkey.
- "Remove NO-GO" to remove the no-go file for the artist and the txt file.

Valid Extensions

- "Add Valid Ext." to add a file extension to the list of valid extensions for the Video Editor to operate on.
- "Remove Valid Ext." to remove a file extension from the list of valid extensions for the Video Editor to operate on.

"Clear" to clear all entries in the tab.

"Reset entries" resets the entries after operations.

### Settings

Appearance

- "Appearance" switches between light and dark mode.
- "UI Scaling" switches between different scaling sizes for the user interface.

Artist

- "Artist Search" attempts to identify the artist in other folders while conducting file renaming operations.
- "Ignore Known Artists" ignores known artists (ones with directories in the Artist Directory) when conducting the
  Artist Search.
- "Remove Artist Duplicates From Filename" removes duplicate entries of the artist when the Artist Identifier is used.
- "Artist Directory" sets the directory that Suggest Output Directory and Artist Search uses to find a match for an
  artist.
- "Artist File" set the line delimited list of artists file that "Artist Identifier" uses to find a match for an artist.
- "Open Artist File" to open the Artist file for editing in the default system program.

File Operations

- "Open File on Drag and Drop" (Linux only).
- "Initial Directory" sets the initial directory when the user browses for an input.
- "Initial Output Directory" sets the initial directory when the user browses for an output directory.
    - This may be overridden by "Suggest Output Dir."
- "Open Config File" to open the configuration file for editing in the default system program.
- "Open Dictionary File" to open the Dictionary file for editing in the default system program.

Logging

- "Activate Logging" logs actions taken within the program.
- "Suppress Standard Output/Error" will supress the outputs to the console and redirect them to the log file.
- "Open Log File" to open the Log file for editing in the default system program.

Messaging

- "Show Messageboxes" displays messagebox notifications. False defaults to standard messaging in the frame.
- "Show Confirmation Messageboxes" displays confirmation messagebox notifications. False defaults to standard messaging
  in the frame. Confirmation messageboxes will always be displayed.
- "Fallback confirmation state" sets what the response is when confirmation messagebox notifications are suppressed.
- "Truncate Text" to truncate text excessively long text in the file display on the File Renamer.

Reminders

- "Create Double Check Reminder" creates an empty file for double-checking.
- "Double Check Reminder Directory" sets the directory that reminders are saved to, if enabled.
- "Open NO GO Artist File" to open the no-go artist file for editing in the default system program.
- "Use Custom Tab Names" sets the tab names you set in the Dictionary.json file.

Tabs

- "Use Custom Tab Names" to use the tab names that were specified in the Custom Tab Name add/remove tab.
- "Sort Tab Names" sorts the standard tab names.
- "Sort Tab Names (A-Z / Z-A)" sorts the standard tab names alphabetically or reverse alphabetically.


### Files
- Use "config.ini.template" as a template for configuring the tool. Remove the .template extension to use.
- Use "dictionary.json.template" as a template for configuring the dictionaries/lists. Remove the .template extension to
  use.
- Use "list_of_artists.txt.template" as a template for the various Artist features. Remove the .template extension to
  use.

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
