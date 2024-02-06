import os  # Operating System module for interacting with the operating system
import re  # Regular expression module for pattern matching in strings
import json  # JSON module for working with JSON data
from tkinter import filedialog, messagebox  # Tkinter modules for GUI file dialogs and message boxes
import send2trash  # Module for sending files to the trash instead of permanently deleting them
import subprocess  # Module for running external processes
import customtkinter as ctk  # Custom Tkinter module for enhanced GUI components
import logging  # Logging module for capturing log messages
import configparser  # Module for working with configuration files
import shutil  # Module for high-level file operations (copying, moving, etc.)
import sys  # System-specific parameters and functions
import string  # Module for various string manipulation functions and constants
from unidecode import unidecode  # Method that transliterates Unicode characters to their closest ASCII equivalents
from moviepy.editor import VideoFileClip  # Video editing module for working with video files

"""
Messaging
"""


def ask_confirmation(self, title, message):
    """
    Display a yes/no messagebox for confirmation.

    Parameters:
    - title (str): The title of the messagebox.
    - message (str): The message to be displayed in the messagebox.

    Returns:
    - bool: True if 'Yes' is selected, False otherwise.
    """
    # Check confirmation messagebox state and display messageboxes if applicable
    if self.show_confirmation_messageboxes_var.get():
        confirmation = messagebox.askyesno(title, message)
        return confirmation
    else:
        if self.fallback_confirmation_var.get():
            # Automatically choose Yes if fallback state is True.
            return True
        else:
            # Automatically choose No if fallback state is False.
            return False


"""
Configuration
"""


def load_configuration(self):
    # Check if configuration file exists
    self.config_file_path = 'config.ini'
    if not os.path.exists(self.config_file_path):
        # Display a message to the console if the configuration file does not exist
        print(f"Error: {self.config_file_path} not found. Please create the config file and try again.")
        # Quit the program
        quit()

    # Load the configuration from the config.ini file
    config = configparser.ConfigParser()
    config.read(self.config_file_path)

    # Filepaths/Directories
    initial_directory = config.get('Filepaths', 'initial_directory', fallback='/path/to/folder')
    initial_output_directory = config.get('Filepaths', 'initial_output_directory', fallback='/path/to/folder')
    double_check_directory = config.get('Filepaths', 'double_check_directory', fallback='double_check_reminders')
    no_go_directory = config.get('Filepaths', 'no_go_directory', fallback='no_go_reminders')
    artist_directory = config.get('Filepaths', 'artist_directory', fallback='artist_directory')
    artist_file = config.get('Filepaths', 'artist_file', fallback='list_of_artists.txt')
    no_go_artist_file = config.get('Filepaths', 'no_go_artist_file', fallback='list_of_no_go_artists.txt')
    excluded_file = config.get('Filepaths', 'excluded_file', fallback='excluded.json')
    categories_file = config.get('Filepaths', 'categories_file', fallback='categories.json')

    # Variables and window geometry
    geometry = config.get('Settings', 'geometry', fallback='1280x850')
    column_numbers = config.get('Settings', 'column_numbers', fallback=7)
    default_weight = config.get('Settings', 'default_weight', fallback=9)
    default_decibel = config.get('Settings', 'default_decibel', fallback=0.0)
    default_audio_normalization = config.get('Settings', 'default_audio_normalization', fallback=0.0)
    default_minute = config.get('Settings', 'default_minute', fallback=0)
    default_second = config.get('Settings', 'default_second', fallback=0)
    default_frame = config.get('Settings', 'default_frame', fallback="file_renamer_window")
    file_renamer_log = config.get('Logs', 'file_renamer_log', fallback="file_renamer.log")
    default_placement_var = config.get("Settings", "default_placement_var", fallback="special_character")
    special_character_var = config.get("Settings", "special_character_var", fallback="-")
    reset_output_directory_var = config.getboolean("Settings", "reset_output_directory_var", fallback=False)
    suggest_output_directory_var = config.getboolean("Settings", "suggest_output_directory_var", fallback=False)
    move_up_directory_var = config.getboolean("Settings", "move_up_directory_var", fallback=False)
    move_text_var = config.getboolean('Settings', 'move_text_var', fallback=False)
    open_on_file_drop_var = config.getboolean("Settings", "open_on_file_drop_var", fallback=False)
    remove_duplicates_var = config.getboolean("Settings", "remove_duplicates_var", fallback=True)
    double_check_var = config.getboolean("Settings", "double_check_var", fallback=False)
    activate_logging_var = config.getboolean("Settings", "activate_logging_var", fallback=False)
    suppress_var = config.getboolean("Settings", "suppress_var", fallback=True)
    show_messageboxes_var = config.getboolean("Settings", "show_messageboxes_var", fallback=True)
    show_confirmation_messageboxes_var = config.getboolean("Settings", "show_confirmation_messageboxes_var",
                                                           fallback=True)
    fallback_confirmation_var = config.getboolean("Settings", "fallback_confirmation_var", fallback=False)

    # Name Normalizer
    remove_all_symbols_var = config.getboolean("Settings", "remove_all_symbols_var", fallback=False)
    remove_most_symbols_var = config.getboolean("Settings", "remove_most_symbols_var", fallback=False)
    remove_non_ascii_symbols_var = config.getboolean("Settings", "remove_non_ascii_symbols_var", fallback=False)
    remove_number_var = config.getboolean("Settings", "remove_number_var", fallback=False)
    tail_var = config.getboolean("Settings", "tail_var", fallback=False)
    remove_parenthesis_trail_var = config.getboolean("Settings", "remove_parenthesis_trail_var", fallback=False)
    remove_parenthesis_var = config.getboolean("Settings", "remove_parenthesis_var", fallback=False)
    remove_hashtag_trail_var = config.getboolean("Settings", "remove_hashtag_trail_var", fallback=False)
    remove_hashtag_var = config.getboolean("Settings", "remove_hashtag_var", fallback=False)
    remove_new_var = config.getboolean("Settings", "remove_new_var", fallback=False)
    remove_dash_var = config.getboolean("Settings", "remove_dash_var", fallback=False)
    remove_endash_var = config.getboolean("Settings", "remove_endash_var", fallback=False)
    remove_emdash_var = config.getboolean("Settings", "remove_emdash_var", fallback=False)
    remove_ampersand_var = config.getboolean("Settings", "remove_ampersand_var", fallback=False)
    remove_at_var = config.getboolean("Settings", "remove_at_var", fallback=False)
    remove_underscore_var = config.getboolean("Settings", "remove_underscore_var", fallback=False)
    remove_comma_var = config.getboolean("Settings", "remove_comma_var", fallback=False)
    remove_single_quote_var = config.getboolean("Settings", "remove_single_quote_var", fallback=False)
    remove_double_quote_var = config.getboolean("Settings", "remove_double_quote_var", fallback=False)
    remove_colon_var = config.getboolean("Settings", "remove_colon_var", fallback=False)
    remove_semicolon_var = config.getboolean("Settings", "remove_semicolon_var", fallback=False)
    remove_percent_var = config.getboolean("Settings", "remove_percent_var", fallback=False)
    remove_caret_var = config.getboolean("Settings", "remove_caret_var", fallback=False)
    remove_dollar_var = config.getboolean("Settings", "remove_dollar_var", fallback=False)
    remove_asterisk_var = config.getboolean("Settings", "remove_asterisk_var", fallback=False)
    remove_plus_var = config.getboolean("Settings", "remove_plus_var", fallback=False)
    remove_equal_var = config.getboolean("Settings", "remove_equal_var", fallback=False)
    remove_curly_brace_var = config.getboolean("Settings", "remove_curly_brace_var", fallback=False)
    remove_square_bracket_var = config.getboolean("Settings", "remove_square_bracket_var", fallback=False)
    remove_pipe_var = config.getboolean("Settings", "remove_pipe_var", fallback=False)
    remove_backslash_var = config.getboolean("Settings", "remove_backslash_var", fallback=False)
    remove_angle_bracket_var = config.getboolean("Settings", "remove_angle_bracket_var", fallback=False)
    remove_question_mark_var = config.getboolean("Settings", "remove_question_mark_var", fallback=False)
    remove_double_space_var = config.getboolean("Settings", "remove_double_space_var", fallback=False)
    title_var = config.getboolean("Settings", "title_var", fallback=False)
    artist_file_search_var = config.getboolean("Settings", "artist_file_search_var", fallback=False)
    reset_var = config.getboolean("Settings", "reset_var", fallback=False)
    reset_video_entries_var = config.getboolean("Settings", "reset_video_entries_var", fallback=False)
    reset_artist_entries_var = config.getboolean("Settings", "reset_artist_entries_var", fallback=True)
    deep_walk_var = config.getboolean("Settings", "deep_walk_var", fallback=False)

    # Video Editor
    remove_successful_lines_var = config.getboolean("Settings", "remove_successful_lines_var", fallback=False)
    default_rotation_var = config.get("Settings", "default_rotation_var", fallback="none")

    # File extensions
    file_extensions_str = config.get('Settings', 'file_extensions',
                                     fallback='.mp3, .wav, .ogg, .flac, .aac, .wma, .m4a, .aiff, .alac, .opus, .mp4, '
                                              '.mkv, .flv, .avi, .mov, .wmv, .mpeg, .mpg, .m4v')
    file_extensions = tuple(ext.strip() for ext in file_extensions_str.split(','))

    valid_extensions_str = config.get('Settings', 'valid_extensions',
                                      fallback='.mp4, .mkv, .flv, .avi, .mov, .wmv, .mpeg, .mpg, .m4v')
    valid_extensions = [ext.strip() for ext in valid_extensions_str.split(',')]

    # Return the loaded configuration values as a tuple
    return (move_text_var, initial_directory, artist_directory, double_check_directory, categories_file,
            geometry, reset_output_directory_var, suggest_output_directory_var, move_up_directory_var,
            open_on_file_drop_var, remove_duplicates_var, default_placement_var, special_character_var,
            double_check_var, activate_logging_var, file_renamer_log, column_numbers, default_weight,
            file_extensions, remove_all_symbols_var, tail_var, remove_parenthesis_trail_var,
            remove_hashtag_trail_var, remove_new_var, remove_dash_var, remove_endash_var, remove_emdash_var,
            remove_ampersand_var, remove_at_var, remove_underscore_var, remove_comma_var, remove_single_quote_var,
            remove_double_quote_var, title_var, reset_var, initial_output_directory, artist_file, default_frame,
            artist_file_search_var, deep_walk_var, default_decibel, default_audio_normalization,
            remove_successful_lines_var, default_rotation_var, remove_double_space_var, remove_colon_var,
            remove_semicolon_var, remove_percent_var, remove_caret_var, remove_dollar_var, remove_asterisk_var,
            remove_plus_var, remove_equal_var, remove_curly_brace_var, remove_square_bracket_var, remove_pipe_var,
            remove_backslash_var, remove_angle_bracket_var, remove_question_mark_var, remove_parenthesis_var,
            remove_hashtag_var, show_messageboxes_var, show_confirmation_messageboxes_var, fallback_confirmation_var,
            valid_extensions, suppress_var, reset_video_entries_var, reset_artist_entries_var, remove_most_symbols_var,
            remove_number_var, default_minute, default_second, no_go_directory, no_go_artist_file, excluded_file,
            remove_non_ascii_symbols_var)


# Function to load the exclude_file
def initialize_exclude(self):
    # Load excluded_folders from the excluded_file or create an empty dictionary
    try:
        if not os.path.isfile(self.excluded_file):
            # Return early if the file doesn't exist
            return

        with open(self.excluded_file, 'r') as json_file:
            data = json.load(json_file)
            self.excluded_folders = data.get("excluded_folders", [])

    except FileNotFoundError:
        # Log that the file is not found (this might not necessarily be an error)
        self.log_and_show(f"Exclusion file not found: {self.excluded_file}")

    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        self.log_and_show(f"Error decoding JSON in exclusion file: {self.excluded_file}, {str(e)}", error=True)

    except Exception as e:
        self.log_and_show(f"Initialize exclusion_file failed: {self.excluded_file}, {str(e)}", error=True)


def logging_setup(self):
    # Create the log file if it doesn't exist
    if not os.path.exists(self.file_renamer_log):
        with open(self.file_renamer_log, 'w'):
            pass

    # Initialize logging
    logging.basicConfig(filename=self.file_renamer_log, level=logging.INFO, filemode='a',
                        format='%(asctime)s - %(levelname)s: %(message)s')

    logging.info("Logging started.")


def stop_logging(self):
    # Notate that logging stopped if the log file exists
    if os.path.exists(self.file_renamer_log):
        logging.info("Logging stopped.")


# Redirect output (Fix for MoviePy overriding user's logging choice)
def redirect_output(self):
    # If logging state is active, redirect the outputs to the log file instead of the console
    if self.activate_logging_var.get():
        # Redirect standard output and error to the log file
        sys.stdout = open(self.file_renamer_log, 'a')
        sys.stderr = open(self.file_renamer_log, 'a')
    # If inactive, either suppress the output completely or revert behavior
    else:
        if self.suppress_var.get():
            # Redirect standard output and error to /dev/null (discard)
            sys.stdout = open(os.devnull, 'w')
            sys.stderr = open(os.devnull, 'w')
        else:
            # Restore the original standard output and error
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr


"""
File Operations
"""


# Function to move the selected input to the trash
def move_file_to_trash(self):
    try:
        if self.file_renamer_selected_file:
            # Ask for confirmation before moving to trash
            confirmation = ask_confirmation(self, "Confirm Action",
                                            "Are you sure you want to move this file to the trash?")
            # Log the action if logging is enabled
            self.log_and_show(f"'{self.file_renamer_selected_file}' selected for deletion.")

            if confirmation:
                # Move the input to trash using send2trash library
                send2trash.send2trash(self.file_renamer_selected_file)
                # Reset selected file, queue, and clear display elements
                self.file_renamer_selected_file = ""
                self.queue = []
                self.file_display_text.set("")
                self.custom_text_entry.delete(0, ctk.END)
                self.output_directory = ""
                self.output_directory_entry.delete(0, ctk.END)
                # Log the action if logging is enabled
                self.log_and_show("File moved to trash successfully")
        else:
            # Log the action if logging is enabled
            self.log_and_show("No input selected. Cannot move to trash.",
                              create_messagebox=True,
                              error=True)
    except OSError as e:
        self.log_and_show(f"{str(e)}",
                          create_messagebox=True,
                          error=True)


# Function to create double check reminders
def double_check_reminder(self, new_path):
    try:
        # Get the name of the folder immediately above the current location
        folder_name = os.path.basename(os.path.dirname(new_path))

        # Ask for confirmation of the double check reminder
        confirmation = ask_confirmation(self, "Double Check Reminder",
                                        f"Do you want to create a double check reminder for: "
                                        f"{folder_name}?")
        if confirmation:
            # Expand the user's home directory in the output directory path
            double_check_directory = os.path.expanduser(self.double_check_directory)

            # Ensure the output directory exists, create it if not
            if not os.path.exists(double_check_directory):
                os.makedirs(double_check_directory)

            # Create an empty file with the specified naming scheme
            file_name = f"Double check {folder_name}"
            file_path = os.path.join(double_check_directory, file_name)

            # Empty file
            with open(file_path, 'w'):
                pass

            # Log the action if logging is enabled
            self.log_and_show(f"Double check reminder created successfully for {folder_name} in \n"
                              f"{self.double_check_directory}")
        else:
            # If the user declines, then do not create the double check reminder
            self.log_and_show(f"User declined double check reminder for: {folder_name}")

    except Exception as e:
        # Handle any errors that may occur
        self.log_and_show(f"Double check reminder was not created successfully: {str(e)}",
                          create_messagebox=True,
                          error=True)


# Function to load the last used file
def load_last_used_file(self):
    if self.frame_name == "file_renamer_window":
        # Check if the file_renamer_last_used_file variable is provided and the input exists
        if self.file_renamer_last_used_file and os.path.exists(self.file_renamer_last_used_file):
            # Set the selected file to the file renamer last used file and update display
            self.file_renamer_selected_file = self.file_renamer_last_used_file

            self.queue = []
            self.update_file_display()

            # Log the action if logging is enabled
            self.log_and_show(f"Input selected via Reload Last File: "
                              f"{os.path.basename(self.file_renamer_selected_file)}")
        else:
            self.log_and_show("No last used File Renamer input found.",
                              create_messagebox=True,
                              error=True)
    elif self.frame_name == "name_normalizer_window":
        # Check if the name_normalizer_last_used_file variable is provided and the input exists
        if self.name_normalizer_last_used_file and os.path.exists(self.name_normalizer_last_used_file):
            # Set the name normalizer selected input to the name normalizer last used input and update display
            self.name_normalizer_selected_file = self.name_normalizer_last_used_file
            filename = os.path.basename(self.name_normalizer_selected_file)

            # Set the selected input to the input entry widget
            self.nn_path_entry.delete(0, ctk.END)
            self.nn_path_entry.insert(0, filename)

            # Log the action if logging is enabled
            self.log_and_show(f"Last used Name Normalizer input selected: {filename}")
        else:
            self.log_and_show("No last used Name Normalizer input found.",
                              create_messagebox=True,
                              error=True)
    elif self.frame_name == "video_editor_window":
        # Check if the video_editor_last_used_file variable is provided and the input exists
        if self.video_editor_last_used_file and os.path.exists(self.video_editor_last_used_file):
            # Set the video editor selected file to the video editor last used file and update display
            self.video_editor_selected_file = self.video_editor_last_used_file
            filename = os.path.basename(self.video_editor_selected_file)

            # Set the selected input to the input entry widget
            self.input_method_entry.delete(0, ctk.END)
            self.input_method_entry.insert(0, filename)

            # Log the action if logging is enabled
            self.log_and_show(f"Last used Video Editor input selected: {filename}")
        else:
            self.log_and_show("No last used Video Editor input found.",
                              create_messagebox=True,
                              error=True)


def send_to_module(self, destination):
    if self.frame_name == "file_renamer_window":
        selected_file = self.file_renamer_selected_file
    elif self.frame_name == "name_normalizer_window":
        selected_file = self.name_normalizer_selected_file
    elif self.frame_name == "video_editor_window":
        selected_file = self.video_editor_selected_file
    else:
        # Invalid frame name
        return

    # Send to File Renamer
    if destination == "file_renamer_module":
        if selected_file:
            # Clear selection for the file_renamer_window
            self.clear_selection(frame_name="file_renamer_window")

            # Set the name normalizer selected file to the file renamer selected file and update display
            self.file_renamer_selected_file = selected_file

            self.update_file_display()

            # Log the action if logging is enabled
            self.log_and_show(f"Input selected via send to module: "
                              f"{os.path.basename(self.file_renamer_selected_file)}")

            # Clear selection for the source module
            self.clear_selection(frame_name=self.frame_name)

            # Switch frames to the File Renamer
            self.file_renamer_button_event()
        else:
            # Input not selected
            self.log_and_show("No input selected. Cannot send to module",
                              create_messagebox=True,
                              error=True)

    # Send to Name Normalizer
    elif destination == "name_normalizer_module":
        if selected_file:
            # Clear selection for the name_normalizer_window
            self.clear_selection(frame_name="name_normalizer_window")

            # Set the source selected file to the Name Normalizer selected file
            self.name_normalizer_selected_file = selected_file

            # Log the action if logging is enabled
            self.log_and_show(f"Input selected via send to module: "
                              f"{os.path.basename(self.name_normalizer_selected_file)}")

            # Clear selection for the source module
            self.clear_selection(frame_name=self.frame_name)

            # Set the Name Normalizer selected file to the nn_path_entry
            self.nn_path_entry.insert(0, self.name_normalizer_selected_file)

            # Switch frames to the File Renamer
            self.name_normalizer_button_event()
        else:
            # Input not selected
            self.log_and_show("No input selected. Cannot send to module",
                              create_messagebox=True,
                              error=True)

    # Send to Video Editor
    elif destination == "video_editor_module":
        # Check if there is an input selected
        if selected_file:
            # Confirm if the input is a valid file for the video editor window
            if any(selected_file.lower().endswith(ext) for ext in self.valid_extensions):
                # Clear selection for the video_editor_window
                self.clear_selection(frame_name="video_editor_window")

                # Initialize video editor selected file to selected file from source module
                self.video_editor_selected_file = selected_file
                filename = os.path.basename(self.video_editor_selected_file)

                # Clear selection for the source module
                self.clear_selection(frame_name=self.frame_name)

                # Set the video editor selected file to the input_method_entry
                self.input_method_entry.insert(0, filename)

                # Log the action and display the message in the GUI
                self.log_and_show(f"Input selected via send to module: {filename}")

                # Switch frames to the video editor
                self.video_editor_button_event()
            else:
                # Input not selected
                self.log_and_show("Non-video input detected. Cannot send to Video Editor",
                                  create_messagebox=True,
                                  error=True)
        else:
            # Input not selected
            self.log_and_show("No input selected. Cannot send to module",
                              create_messagebox=True,
                              error=True)
    else:
        # Invalid frame name
        self.log_and_show("Invalid frame name for send to module",
                          create_messagebox=True,
                          error=True)
        return


# Function to handle an input being dropped onto the application window
def on_file_drop(self, event):
    # Initialize the selected file variable to the dropped file
    selected_file = event.data.strip('{}')

    # Extract the file name from the path for gui friendly presentation
    filename = os.path.basename(selected_file)

    # Assign the selected file variable to the correct file depending on active frame
    if self.frame_name == "name_normalizer_window":
        self.name_normalizer_selected_file = selected_file

        self.nn_path_entry.delete(0, ctk.END)
        self.nn_path_entry.insert(0, filename)
    elif self.frame_name == "video_editor_window":
        self.video_editor_selected_file = selected_file

        # Set the selected file to the input entry widget
        self.input_method_entry.delete(0, ctk.END)
        self.input_method_entry.insert(0, filename)
    # Default to File Renamer module (file_renamer_window)
    else:
        self.file_renamer_selected_file = selected_file

        # Remove the default custom text entry text
        self.custom_text_entry.delete(0, ctk.END)

        self.queue = []
        self.update_file_display()

    # Open the input if the corresponding option is set
    if self.open_on_file_drop_var.get():
        self.open_file(selected_file)

    # Log the action and display the message in the gui
    self.log_and_show(f"Input selected via drop: {filename}")


def open_file(self, file_to_open):
    # Get the filename from the file path
    filename = os.path.basename(file_to_open)

    # Check if the input exists
    if not os.path.exists(file_to_open):
        # If the provided input does not exist, log an error and return
        self.log_and_show(f"Cannot open input as it does not exist: {filename}",
                          create_messagebox=True,
                          error=True)
        return

    # If the input path is not empty, try to open the input using the default system program
    if file_to_open:
        try:
            subprocess.Popen(['xdg-open', file_to_open])

            # Log a success message if the input is opened successfully
            self.log_and_show(f"Input opened: {filename}")
        except OSError as e:
            # If an error occurs while opening the file, log the error
            self.log_and_show(f"{str(e)}",
                              create_messagebox=True,
                              error=True)


# Function to add a category to the queue
def add_to_queue(self, category):
    if self.file_renamer_selected_file:
        # Check if the category is not already in the queue
        if category not in self.queue:
            self.queue.append(category)

        # Update file display and show a message
        self.update_file_display()
        self.log_and_show(f"Word added to queue: {category}",
                          not_logging=True)
    else:
        # If no input selected, log the action and display a message in the GUI
        self.log_and_show("Please select an input first and then add a word to the queue.",
                          create_messagebox=True,
                          error=True)


# Function to update the file display based on selected options
def update_file_display(self):
    if self.file_renamer_selected_file:
        custom_text = self.custom_text_entry.get().strip()

        # Use only the base name of the file, not the full path
        base_file_name = os.path.basename(self.file_renamer_selected_file)

        # Construct the name
        new_name_parts = [
            os.path.splitext(base_file_name)[0],
            custom_text,
            " ".join(self.queue),
            os.path.splitext(base_file_name)[1]
        ]

        # Join the parts and remove double spaces and trailing spaces
        name = " ".join(part for part in new_name_parts if part).strip()

        # Handle name length constraints
        if len(name) > 250:
            self.log_and_show("The proposed file name exceeds 250 characters. Please consider "
                              "shortening it to comply with operating system limitations.",
                              create_messagebox=True)
            # Truncate the name
            name = f"...{name[180:]}"

        # Set the name to the file display
        self.file_display_text.set(name)


# Function to undo the last category added to the queue
def undo_last(self):
    if self.queue:
        # Remove the last category from the queue and update display
        self.queue.pop()
        self.update_file_display()
        self.log_and_show("Last category removed",
                          not_logging=True)
    else:
        # Log the action if logging is enabled
        self.log_and_show("Nothing in the queue. Nothing to undo.",
                          create_messagebox=True,
                          error=True)


# Function to clear the selection and reset related elements
def clear_selection(self, frame_name):
    if frame_name == "file_renamer_window":
        self.file_renamer_selected_file = ""
        self.queue = []
        self.file_display_text.set("")

        # Clear custom text entry and reset output directory
        self.custom_text_entry.delete(0, ctk.END)
        self.output_directory = ""
        self.output_directory_entry.delete(0, ctk.END)

    elif frame_name == "name_normalizer_window":
        self.name_normalizer_selected_file = ""
        self.name_normalizer_output_directory = ""

        self.nn_path_entry.delete(0, ctk.END)
        self.move_directory_entry.delete(0, ctk.END)

    elif frame_name == "video_editor_window":
        self.video_editor_selected_file = ""

        self.input_method_entry.delete(0, ctk.END)
        self.video_editor_output_directory_entry.delete(0, ctk.END)

        # Clear decibel entry
        self.decibel_entry.delete(0, ctk.END)

        # Clear audio normalization entry
        self.audio_normalization_entry.delete(0, ctk.END)

        # Clear minute entry
        self.minute_entry.delete(0, ctk.END)

        # Clear second entry
        self.second_entry.delete(0, ctk.END)

    elif frame_name == "add_remove_window":
        # Clear add artist entry
        self.add_artist_entry.delete(0, ctk.END)

        # Clear remove artist entry
        self.remove_artist_entry.delete(0, ctk.END)
    else:
        # Invalid frame name
        return

    # Log action and display message on the applicable frame
    self.log_and_show("Selection cleared",
                      not_logging=True)


# Open a dialog to browse and select an input containing a line delimited list of artists
def browse_artist_file(self):
    self.artist_file = filedialog.askopenfilename(
        initialdir=self.initial_directory,
        filetypes=[("Text Files", "*.txt")])

    if self.artist_file:
        # Clear the entry and set it to the artist file
        self.artist_file_entry.delete(0, ctk.END)
        self.artist_file_entry.insert(0, self.artist_file)


# Function to browse and select a directory to use for the artist search
def browse_artist_directory(self):
    self.artist_directory = filedialog.askdirectory(initialdir=self.initial_directory)

    if self.artist_directory:
        # Clear the entry and set it to the artist directory
        self.artist_directory_entry.delete(0, ctk.END)
        self.artist_directory_entry.insert(0, self.artist_directory)


# Function to browse and select the initial directory when the user browses location
def browse_initial_directory(self):
    self.initial_directory = filedialog.askdirectory(initialdir=self.initial_directory)

    if self.initial_directory:
        # Clear the entry and set it to the initial directory when the user browses location
        self.initial_directory_entry.delete(0, ctk.END)
        self.initial_directory_entry.insert(0, self.initial_directory)


# Function to browse and select the initial directory when the user browses output location
def browse_initial_output_directory(self):
    self.initial_output_directory = filedialog.askdirectory(initialdir=self.initial_output_directory)

    if self.initial_output_directory:
        # Clear the entry and set it to the initial directory when the user browses output location
        self.initial_output_directory_entry.delete(0, ctk.END)
        self.initial_output_directory_entry.insert(0, self.initial_output_directory)


# Function to browse and select a directory to save double check reminders in
def browse_double_check_reminder_directory(self):
    self.double_check_directory = filedialog.askdirectory(initialdir=self.initial_directory)

    if self.double_check_directory:
        # Clear the entry and set it to the artist directory
        self.double_check_reminder_directory_entry.delete(0, ctk.END)
        self.double_check_reminder_directory_entry.insert(0, self.double_check_directory)


# Function to browse and select a directory to save NO GO reminders in
def browse_no_go_directory(self):
    self.no_go_directory = filedialog.askdirectory(initialdir=self.initial_directory)

    if self.no_go_directory:
        # Clear the entry and set it to the artist directory
        self.no_go_reminder_directory_entry.delete(0, ctk.END)
        self.no_go_reminder_directory_entry.insert(0, self.no_go_directory)


# Function to browse and select an input
def browse_input(self):
    if self.frame_name == "file_renamer_window":
        # Remove the default custom text entry text
        self.custom_text_entry.delete(0, ctk.END)

        file_path = filedialog.askopenfilename(initialdir=self.initial_directory)
        if file_path:
            # Set the selected file
            self.file_renamer_selected_file = file_path

            # Clear the queue
            self.queue = []
            # Update display
            self.update_file_display()

            # Log the action if logging is enabled
            self.log_and_show(f"Input selected via Browse: "
                              f"{os.path.basename(self.file_renamer_selected_file)}")

    elif self.frame_name == "name_normalizer_window":
        # Function to browse and select a folder to normalize files
        nn_input_method = filedialog.askdirectory(initialdir=self.initial_directory,
                                                  title="Browse a directory. Close to select a file instead")

        if not nn_input_method:
            nn_input_method = filedialog.askopenfilename(
                initialdir=self.initial_directory,
                title="Browse a file.",
                filetypes=[("All Files", "*.*")]
            )

        if nn_input_method:
            self.name_normalizer_selected_file = nn_input_method
            self.nn_path_entry.delete(0, ctk.END)
            self.nn_path_entry.insert(0, self.name_normalizer_selected_file)

            # Log the action if logging is enabled
            self.log_and_show(f"Input selected via Browse: "
                              f"{os.path.basename(self.name_normalizer_selected_file)}")

    elif self.frame_name == "video_editor_window":
        # Initially ask for a file
        input_method = filedialog.askopenfilename(
            initialdir=self.initial_directory,
            title="Browse a file. Close to select a directory instead",
            filetypes=[("All Files", "*.*")]
        )
        if not input_method:
            # If no file is selected, try to get a directory
            input_method = filedialog.askdirectory(initialdir=self.initial_directory, title="Browse a directory")

        if input_method:
            # Set the video editor selected file
            self.video_editor_selected_file = input_method
            # Extract just the file name, not the absolute file path
            filename = os.path.basename(self.video_editor_selected_file)

            # Set the selected file to the input entry widget
            self.input_method_entry.delete(0, ctk.END)
            self.input_method_entry.insert(0, filename)

            # Log the action and display the message in the gui
            self.log_and_show(f"Input selected via Browse: {filename}")


# Function to browse and select an output directory
def browse_output_directory(self):
    if self.frame_name == "file_renamer_window":
        # Check if an input is selected
        if self.file_renamer_selected_file:
            # Check if suggest output directory is true
            if self.suggest_output_directory_var.get():
                # Call the suggest output directory function to determine initial directory
                initial_directory = self.suggest_output_directory()

                # If suggest output directory returns none, use the default initial output directory
                if not initial_directory:
                    initial_directory = self.initial_output_directory
            else:
                # If suggest output directory is false, use the default initial directory
                initial_directory = self.initial_directory
        else:
            # If no input is selected, use the default initial output directory
            initial_directory = self.initial_output_directory

        # Ask for the output directory
        self.output_directory = filedialog.askdirectory(initialdir=initial_directory)

        # If output directory, update the entry field in the gui
        if self.output_directory:
            self.output_directory_entry.delete(0, ctk.END)
            self.output_directory_entry.insert(0, self.output_directory)

    elif self.frame_name == "name_normalizer_window":
        # Ask for the output directory
        self.name_normalizer_output_directory = filedialog.askdirectory(initialdir=self.initial_output_directory)

        # If name normalizer output directory, update the entry field in the GUI
        if self.name_normalizer_output_directory:
            self.move_directory_entry.delete(0, ctk.END)
            self.move_directory_entry.insert(0, self.name_normalizer_output_directory)

    elif self.frame_name == "video_editor_window":
        # Ask for the output directory
        self.video_editor_output_directory = filedialog.askdirectory(initialdir=self.initial_output_directory)

        # If video editor output directory, update the entry field in the GUI
        if self.video_editor_output_directory:
            self.video_editor_output_directory_entry.delete(0, ctk.END)
            self.video_editor_output_directory_entry.insert(0, self.video_editor_output_directory)


def suggest_output_directory(self):
    # Check if an input is selected
    if not self.file_renamer_selected_file:
        # If no input is selected, return none
        self.log_and_show("No input selected. Using default initial directory.")
        return None

    # Check if the suggest_output_directory_var is True
    if not self.suggest_output_directory_var.get():
        # If suggest_output_directory is False, return none
        self.log_and_show("Suggest output directory disabled. Using default output directory.")
        return None

    # Check if self.artist_directory exists
    if not os.path.exists(self.artist_directory):
        # If artist directory does not exist, display an error message and return none
        self.log_and_show(f"Suggest Output Directory cannot function as intended since the Artist Directory"
                          f" does not exist."
                          f"\nUsing default output directory as the fallback."
                          f"\nPlease ensure Artist Directory: '{self.artist_directory}' exists.",
                          create_messagebox=True,
                          error=True)
        return None

    try:
        # Extract the base name from the selected file
        base_name = os.path.basename(self.file_renamer_selected_file)
        base_name_lower = base_name.lower()  # Case insensitive comparison

        # Extract the artist from the filename
        for artist_folder in os.listdir(self.artist_directory):
            if artist_folder.lower() in base_name_lower:
                if artist_folder in self.excluded_folders:
                    # Log and show message for excluded folder match
                    self.log_and_show(f"Artist folder '{artist_folder}' is on the excluded folders list. "
                                      f"Falling back to default output directory.")
                    return None

                # Construct the artist folder path
                artist_folder_path = os.path.join(self.artist_directory, artist_folder)

                # Verify the folder exists
                if os.path.exists(artist_folder_path) and os.path.isdir(artist_folder_path):
                    # Return the result
                    return artist_folder_path

        # If no matching artist folder is found, return none
        self.log_and_show("Cannot suggest output directory. Falling back to default output directory.")
        return None

    except Exception as e:
        # Handle any unexpected exceptions and log an error message
        self.log_and_show(f"Unexpected error suggesting an output directory: {e}",
                          create_messagebox=True,
                          error=True)
        return None


# Function to handle actions after successful input renaming
def handle_rename_success(self, new_path):
    # Check if the double check reminder variable is true
    if self.double_check_var.get():
        # Call the double check reminder function
        double_check_reminder(self, new_path)

    # Reset selected file, queue and update file renamer last used file
    self.file_renamer_selected_file = ""
    self.queue = []
    self.file_display_text.set("")
    self.custom_text_entry.delete(0, ctk.END)
    self.file_renamer_last_used_file = new_path

    # Get the base name and truncate after x characters
    last_used_name = os.path.basename(new_path)
    if len(last_used_name) > 115:
        last_used_name = last_used_name[:115]
    self.last_used_display.configure(text=last_used_name)

    if self.reset_output_directory_var.get():
        # Clear and reset the Output Directory
        self.output_directory = ""
        self.output_directory_entry.delete(0, ctk.END)

    # Log the action if logging is enabled
    self.log_and_show("File renamed and saved successfully")


"""
Category Management
"""


def add_category(self):
    # Get the new category from the add category entry widget
    new_category = self.category_entry.get().strip()

    if not new_category:
        # If the new category is an empty string, log an error message and return
        self.log_and_show("Add Category cannot be empty.",
                          create_messagebox=True,
                          error=True)
        return

    if new_category:
        # Convert to lowercase for case-insensitive check
        new_category_lower = new_category.lower()
        # Prevent duplicate entries in the json file
        if new_category_lower not in map(lambda x: x.lower(), self.categories.keys()):
            # Get the weight from the GUI entry field
            weight_entry_value = self.weight_entry.get().strip()

            try:
                # Use the provided weight if it's an integer, otherwise use the default weight
                weight = int(weight_entry_value) if weight_entry_value else self.default_weight
            except ValueError:
                self.log_and_show("Weight must be an integer. Using default weight.",
                                  create_messagebox=True,
                                  error=True)
                weight = self.default_weight

            # Add the new category to the dictionary with the specified weight
            self.categories[new_category] = weight
            # Sort categories alphabetically, case-insensitive
            sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())
            # Save the updated categories to the file
            self.save_categories()
            # Refresh the category buttons in the GUI
            self.refresh_category_buttons(sorted_categories)
            # Clear the category entry and weight entry fields
            self.category_entry.delete(0, ctk.END)
            self.weight_entry.delete(0, ctk.END)

            # Log the action if logging is enabled
            self.log_and_show(f"Category added: '{new_category}' with weight({weight})")
        else:
            # Log the action if logging is enabled
            self.log_and_show(f"'{new_category}' already exists. Skipping.",
                              create_messagebox=True,
                              error=True)
            # Clear the category entry and weight entry fields
            self.category_entry.delete(0, ctk.END)
            self.weight_entry.delete(0, ctk.END)


def remove_category(self):
    # Get the category to be removed from the remove category entry widget
    category_to_remove = self.remove_category_entry.get().strip()

    if not category_to_remove:
        # If the category to be removed is an empty string, log an error message and return
        self.log_and_show("Remove Category cannot be empty.",
                          create_messagebox=True,
                          error=True)
        return

    # Check for a case-sensitive match
    if category_to_remove in self.categories:
        # Remove the category from the dictionary
        del self.categories[category_to_remove]
        # Sort categories alphabetically, case-insensitive
        sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())
        # Save the updated categories to the file
        self.save_categories()
        # Refresh the category buttons in the GUI
        self.refresh_category_buttons(sorted_categories)
        # Clear the remove category entry field
        self.remove_category_entry.delete(0, ctk.END)

        # Log the action if logging is enabled
        self.log_and_show(f"Category removed: {category_to_remove}")
    else:
        # Check for a case-insensitive match
        matching_category = next((key for key in self.categories if key.lower() == category_to_remove.lower()), None)
        if matching_category:
            # Remove the case-insensitive matched category from the dictionary
            del self.categories[matching_category]
            # Sort categories alphabetically, case-insensitive
            sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())
            # Save the updated categories to the file
            self.save_categories()
            # Refresh the category buttons in the GUI
            self.refresh_category_buttons(sorted_categories)
            # Clear the remove category entry field
            self.remove_category_entry.delete(0, ctk.END)

            # Log the action if logging is enabled
            self.log_and_show(f"Category removed: {matching_category}")
        else:
            # Log the action if logging is enabled
            self.log_and_show(f"'{category_to_remove}' not found in dictionary. Skipping.",
                              create_messagebox=True,
                              error=True)


def create_category_button(self, category):
    return ctk.CTkButton(self.button_frame, text=category, command=lambda c=category: self.add_to_queue(c))


def categories_buttons_initialize(self):
    # Load categories from the file or create an empty dictionary
    try:
        with open(self.categories_file, "r") as file:
            self.categories = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        self.categories = {}

    # Sort the category keys alphabetically, case-insensitive
    sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())

    # Batch processing for button creation
    buttons = [self.create_category_button(category) for category in sorted_categories]

    for i, button in enumerate(buttons):
        button.grid(row=i // self.column_numbers, column=i % self.column_numbers, padx=5, pady=5)

    self.buttons = buttons


def refresh_category_buttons(self, sorted_categories=None):
    # If sorted_categories is not provided, sort the categories alphabetically, case-insensitive
    if sorted_categories is None:
        sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())

    # Remove existing buttons
    for button in self.buttons:
        button.destroy()

    # Batch processing for button creation
    buttons = [self.create_category_button(category) for category in sorted_categories]

    for i, button in enumerate(buttons):
        button.grid(row=i // self.column_numbers, column=i % self.column_numbers, padx=5, pady=5)

    self.buttons = buttons


def save_categories(self):
    # Save the current categories to the file
    with open(self.categories_file, "w") as file:
        json.dump(self.categories, file)


"""
File Renaming
"""


def rename_files(self):
    # Check if an input is selected and either the queue is not empty or custom text is provided
    if self.file_renamer_selected_file and (self.queue or self.custom_text_entry.get().strip()):

        # Get custom text and file extension
        custom_text = self.custom_text_entry.get().strip()
        base_name, extension = os.path.splitext(os.path.basename(self.file_renamer_selected_file))

        # Check if the remove_duplicates_var is set
        if self.remove_duplicates_var.get():
            # Remove duplicates from the queue
            self.queue = list(dict.fromkeys(self.queue))

        # Filter and sort categories based on weights
        weighted_categories = [category for category in self.queue if category in self.categories]
        weighted_categories.sort(key=lambda category: self.categories.get(category, 0))  # Use 0 as default weight

        # Construct a name using base name, weighted categories, custom text, and extension
        name = self.construct_new_name(base_name, weighted_categories, custom_text, extension)

        # If move_text_var is set, move the text between - and __-__
        if self.move_text_var.get():
            name = self.move_text(name)

        # Remove extra whitespaces from the name
        name = " ".join(name.split()).strip()

        # If output directory is not explicitly set, default to the same directory as the file
        if not self.output_directory:
            self.output_directory = os.path.dirname(self.file_renamer_selected_file)

        # Determine the new path based on user preferences
        if self.move_up_directory_var.get():
            # Ignore the provided output directory and move the input up one folder
            parent_directory = os.path.dirname(os.path.dirname(self.file_renamer_selected_file))
            new_path = os.path.join(parent_directory, os.path.basename(name))
        else:
            # Use the suggest output directory
            if self.suggest_output_directory_var.get():
                # Call the suggest output directory to get a suggested output directory
                suggested_output_directory = self.suggest_output_directory()

                # If suggest output directory returns a result, use that as the output directory
                if suggested_output_directory:
                    # Ask for confirmation of new output directory if match found
                    confirmation = ask_confirmation(self, "Suggest Output Directory",
                                                    f"Suggested output directory found. Do you want to use: "
                                                    f"{suggested_output_directory}?")
                    if confirmation:
                        self.output_directory = suggested_output_directory
                        self.log_and_show(f"User chose the suggested output directory: {self.output_directory}")
                    else:
                        # If the user did not select the suggested output directory, use the previously set output
                        # directory
                        self.log_and_show("User did not choose the suggested output directory. Falling back to default "
                                          "directory.")

                else:
                    # If suggest output directory does not return a result, use the previously set output directory
                    # Log the result and update the GUI
                    self.log_and_show(f"Suggest output directory returned no result. Using {self.output_directory}")

                new_path = os.path.join(self.output_directory, os.path.basename(name))

            else:
                # Use the specified output directory
                new_path = os.path.join(self.output_directory, os.path.basename(name))

        # Attempt to rename the input and handle success or errors
        try:
            # Check if the new_path exists
            if os.path.exists(new_path):
                # Get a non-conflicting filename
                new_path = self.get_non_conflicting_filename(new_path)

            # Rename the file
            os.rename(self.file_renamer_selected_file, new_path)
            self.log_and_show(f"File: '{os.path.basename(self.file_renamer_selected_file)}' renamed successfully. "
                              f"\nSaved to: \n{new_path}")
            self.handle_rename_success(new_path)
        except OSError as e:
            # Log the action if logging is enabled
            self.log_and_show(f"{str(e)}",
                              create_messagebox=True,
                              error=True)
    # If an input is selected and either the queue is empty or no custom text is provided show error
    elif self.file_renamer_selected_file and not (self.queue or self.custom_text_entry.get().strip()):
        # Log the action if logging is enabled
        self.log_and_show("Input selected but nothing added to the queue. Nothing to rename.",
                          create_messagebox=True,
                          error=True)
    # If no input is selected, show error
    elif not self.file_renamer_selected_file:
        # Log the action if logging is enabled
        self.log_and_show("No input selected. Nothing to rename.",
                          create_messagebox=True,
                          error=True)


def construct_new_name(self, base_name, weighted_categories, custom_text, extension):
    # Construct the name based on placement choice (prefix, suffix, or special_character)
    categories = weighted_categories + [category for category in self.queue if category not in weighted_categories]
    categories_text = ' '.join(categories).strip()

    if self.placement_choice.get() == "prefix":
        name = f"{custom_text} {categories_text} {base_name}".strip()
    # Place the queue at the first instance of the special character
    elif self.placement_choice.get() == "special_character":
        parts = base_name.split(self.special_character_var, 1)
        if len(parts) == 2:
            name = f"{parts[0].rstrip()} {categories_text} {custom_text} {parts[1].lstrip()}".strip()
            try:
                # Remove the tail __-__ if found
                name = name.replace("__-__", "")
            except OSError as e:
                # Log the action if logging is enabled
                self.log_and_show(f"{str(e)}",
                                  create_messagebox=True,
                                  error=True)
        else:
            # If there's no special character found, default to suffix
            name = f"{base_name} {categories_text} {custom_text}".strip()
    else:  # Default to suffix
        name = f"{base_name} {categories_text} {custom_text}".strip()

    return name + extension


def move_text(name):
    # Move the text between - and __-__ in the name
    match = re.match(r"^(.*) - (.*?)__-__ (.*)\.(\w+)$", name)
    if match:
        prefix, moved_text, suffix, extension = match.groups()
        name = f"{prefix} {suffix} {moved_text}.{extension}"
    return name


"""
Name Normalizer
"""


# Function to remove duplicate artists from the filename
def remove_artist_duplicates_from_filename(self, file_name):
    # Read the list of artists from the artist_file
    with open(self.artist_file, 'r') as artist_list_file:
        artist_list = [artist.strip() for artist in artist_list_file]

    # Extract the file name without the path
    file_name = os.path.basename(file_name)

    # Find the first occurrence of '-'
    index = file_name.find('-')

    if index != -1:
        # Temporary removal of everything before the dash
        temp_name = file_name[index + 1:]
        temp_name = temp_name.strip()

        # Search for artist names and remove them
        for artist in artist_list:
            # Make the search case-insensitive
            regex = re.compile(rf'\b{re.escape(artist)}\b', re.IGNORECASE)
            temp_name = regex.sub('', temp_name)

        # Reattach the dash and any remaining text
        new_file_name = f"{file_name[:index + 1]} {temp_name.strip()}"
    else:
        new_file_name = file_name

    # Sanitize file name. Remove double spaces.
    new_file_name = ' '.join(new_file_name.split()).strip()
    return new_file_name


def preview_name(self, file_path):
    # Split the file path into directory path and filename
    dir_path, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)

    if ext.lower() not in self.file_extensions:
        # Log that the input is ignored if not on the file extensions list
        self.log_and_show(f"Ignored: {filename} (not on file extensions list)")

    # Check if the input has one of the video file extensions
    if ext.lower() in self.file_extensions:
        if self.remove_non_ascii_symbols_var.get():
            # Get all printable ASCII characters
            standard_chars = set(string.printable)

            # Replace non-ASCII characters with their ASCII equivalents (ignore slashes)
            name = ''.join(unidecode(char) if char not in standard_chars and char not in ['⁄', '／']
                           else char if char not in ['⁄', '／'] else ' ' for char in name)

        if self.remove_all_symbols_var.get():
            # Define the characters to be removed
            remove_chars = ",;:@$%^&#*+=(){}[]|\\<>\'\"?_-–—"

            # Replace each unwanted character with an empty string
            for char in remove_chars:
                name = name.replace(char, "")

        if self.remove_most_symbols_var.get():
            # Define the characters to be removed
            remove_chars = ",;:@$%^&*+={}[]|\\<>\"?-–—"

            # Replace each unwanted character with an empty string
            for char in remove_chars:
                name = name.replace(char, "")

        if self.remove_number_var.get():
            # Remove all numbers from the name
            name = ''.join(char for char in name if not char.isdigit())

        if self.remove_new_var.get():
            if 'New_' in name:
                # Replace underscore with a space if it immediately trails the word "New". Catchall
                name = name.replace('New_', '', 1)
            else:
                # Remove the first occurrence of "New "
                name = name.replace('New ', '', 1)

        if self.remove_hashtag_trail_var.get():
            # Find the first occurrence of '#'
            index = name.find('#')

            # Remove the # and everything afterward
            if index != -1:
                name = name[:index].strip()

        if self.remove_parenthesis_trail_var.get():
            # Find the first occurrence of beginning parenthesis
            index = name.find('(')

            # Remove the ( and everything afterward
            if index != -1:
                name = name[:index].strip()

        if self.remove_dash_var.get():
            # Remove dashes
            name = re.sub(r'-', '', name)

        if self.remove_endash_var.get():
            # Remove endashes
            name = re.sub(r'–', '', name)

        if self.remove_emdash_var.get():
            # Remove emdashes
            name = re.sub(r'—', '', name)

        if self.remove_ampersand_var.get():
            # Remove ampersands
            name = re.sub(r'&', '', name)

        if self.remove_at_var.get():
            # Remove at symbols
            name = re.sub(r'@', '', name)

        if self.remove_underscore_var.get():
            # Remove underscores
            name = name.replace('_', ' ')

        if self.remove_comma_var.get():
            # Remove commas
            name = name.replace(',', '')

        if self.remove_single_quote_var.get():
            # Remove single quotes
            name = name.replace('\'', '')

        if self.remove_double_quote_var.get():
            # Remove double quotes
            name = name.replace('\"', '')

        if self.remove_colon_var.get():
            # Remove colons
            name = name.replace(':', '')

        if self.remove_semicolon_var.get():
            # Remove semicolons
            name = name.replace(';', '')

        if self.remove_percent_var.get():
            # Remove percents
            name = name.replace('%', '')

        if self.remove_caret_var.get():
            # Remove carets
            name = name.replace('^', '')

        if self.remove_parenthesis_var.get():
            # Remove parenthesis
            name = name.replace('(', '').replace(')', '')

        if self.remove_hashtag_var.get():
            # Remove hashtags
            name = name.replace('#', '')

        if self.remove_dollar_var.get():
            # Remove dollars
            name = name.replace('$', '')

        if self.remove_asterisk_var.get():
            # Remove asterisks
            name = name.replace('*', '')

        if self.remove_plus_var.get():
            # Remove plus signs
            name = name.replace('+', '')

        if self.remove_equal_var.get():
            # Remove equal signs
            name = name.replace('=', '')

        if self.remove_curly_brace_var.get():
            # Remove curly braces
            name = name.replace('{', '').replace('}', '')

        if self.remove_square_bracket_var.get():
            # Remove square brackets
            name = name.replace('[', '').replace(']', '')

        if self.remove_pipe_var.get():
            # Remove pipes
            name = name.replace('|', '')

        if self.remove_backslash_var.get():
            # Remove backslashes
            name = name.replace('\\', '')

        if self.remove_angle_bracket_var.get():
            # Remove angle brackets
            name = name.replace('<', '').replace('>', '')

        if self.remove_question_mark_var.get():
            # Remove question marks
            name = name.replace('?', '')

        if self.title_var.get():
            # Make file name a title while preserving lowercase letters after apostrophes in contractions
            words = name.split()
            formatted_words = []

            for word in words:
                if "'" in word:
                    # If the word is a contraction with ', capitalize the first part and keep the rest in lowercase
                    parts = word.split("'")
                    formatted_word = "'".join([parts[0].capitalize()] + [part.lower() for part in parts[1:]])
                else:
                    # Capitalize the word as usual
                    formatted_word = word.capitalize()

                formatted_words.append(formatted_word)

            # Join the words back into a formatted name
            name = ' '.join(formatted_words)

        if self.remove_double_space_var.get():
            # Sanitize the filename by removing double spaces
            name = ' '.join(name.split())

        # Process artist names if artist_file_search_var is True
        if self.artist_file_search_var.get():
            try:
                # Read the list of artists from the artist_file
                with open(self.artist_file, 'r') as artist_list_file:
                    artists = [artist.strip() for artist in artist_list_file]

                # Search for artist names and add them as prefixes
                artist_prefix = ''
                for artist in artists:
                    # Make the search case-insensitive
                    regex = re.compile(rf'\b{re.escape(artist)}\b', re.IGNORECASE)
                    if regex.search(name):
                        artist_prefix += f"{artist} "

                # Remove extra spaces and dashes at the beginning and end
                artist_prefix = artist_prefix.strip()
                name = name.strip("-")

                # Add artist prefix to the filename if artist_prefix is not empty
                name = f"{artist_prefix} - {name}" if artist_prefix else name

                # Check if remove_duplicates_var is set
                if self.remove_duplicates_var.get():
                    # Call the remove_artist_duplicates_from_filename function to modify name
                    name = remove_artist_duplicates_from_filename(self, name)
            except FileNotFoundError:
                self.log_and_show(f"File not found: {self.artist_file}",
                                  create_messagebox=True, error=True)
            except Exception as e:
                self.log_and_show(f"Artist search failed {self.artist_file}: {e}",
                                  create_messagebox=True, error=True)

        # Add tail if tail_var is True
        if self.tail_var.get():
            name += "__-__ "

            # Remove " -__-__" if present. Catchall for situations where only the artist name is left and -artist and
            # -tail are used.
            name = re.sub(r' -__-__', '', name).strip()

        # Add the file extension back to the name
        name += ext

        # Skip renaming if the name is the same as the original
        if name == filename:
            self.log_and_show(f"Skipped renaming: {filename} (no changes needed)")
            return

        # Construct the new file path
        new_path = os.path.join(dir_path, name)

        # Check if the new filename already exists
        if os.path.exists(new_path):
            # Get a non-conflicting name
            new_path = self.get_non_conflicting_filename(new_path)

        return new_path


# Function to process and rename files and moving files to a specified directory
def rename_and_move_file(self, file_path):
    # Call the preview name function to get the name
    new_path = self.preview_name(file_path)

    if new_path:
        try:
            # Rename the file
            os.rename(file_path, new_path)

            # Set self.name_normalizer_last_used_file to the new path
            self.name_normalizer_last_used_file = new_path

            # Log the renaming operation if logging is activated
            self.log_and_show(f"Renamed: {os.path.basename(file_path)} -> {os.path.basename(new_path)}")

            # Move the renamed input to the specified directory if name_normalizer_output_directory is provided
            if self.name_normalizer_output_directory:
                # Create the destination file path by joining the destination directory and the source file name
                destination_file = os.path.join(self.name_normalizer_output_directory, os.path.basename(new_path))

                # Check if the destination file already exists
                if os.path.exists(destination_file):
                    # Get a non-conflicting name
                    destination_file = self.get_non_conflicting_filename(destination_file)

                try:
                    # Perform the move to the provided directory
                    shutil.move(str(new_path), str(destination_file))

                    # Update self.name_normalizer_last_used_file to the new path
                    self.name_normalizer_last_used_file = destination_file

                    # Log the move operation if logging is activated
                    self.log_and_show(f"Moved: {os.path.basename(new_path)} -> {os.path.basename(destination_file)}")
                except OSError as e:
                    # Log error if logging is activated
                    self.log_and_show(f"Moving failed for {os.path.basename(new_path)}: {e}",
                                      error=True)

        except OSError as e:
            # Log an error if renaming fails
            self.log_and_show(f"Renaming failed for {os.path.basename(file_path)}: {e}",
                              error=True)
    else:
        return


# Function to performing various name normalization operations on certain files within a specified folder
def process_name_normalizer(self, mode):
    # Check if the specified input exists
    if (not os.path.exists(self.name_normalizer_selected_file)
            and not os.path.isfile(self.name_normalizer_selected_file)):
        self.log_and_show("Path does not exist or was not specified.\nPlease try again.",
                          create_messagebox=True,
                          error=True)
        return

    # Check if name_normalizer_output_directory is specified and exists
    if self.name_normalizer_output_directory and not os.path.exists(self.name_normalizer_output_directory):
        self.log_and_show("Output directory does not exist or was not specified.\nPlease try again.",
                          create_messagebox=True,
                          error=True)
        return

    # Check if artist file search is enabled
    if self.artist_file_search_var.get():
        # Check if artist file is not provided
        if not self.artist_file:
            # Log and display an error message
            self.log_and_show("No artist file provided. Please provide one and try again, or turn off Artist Search.",
                              create_messagebox=True,
                              error=True)
            return
        # Check if artist file does not exist
        elif not os.path.exists(self.artist_file):
            # Log and display an error message
            self.log_and_show(f"The artist file does not exist: '{self.artist_file}'"
                              f"\nPlease ensure the provided Artist File exists, "
                              f"\nor turn off Artist Search to proceed.\nSee FAQ",
                              create_messagebox=True,
                              error=True)
            return

    if mode == "preview":
        preview_result = preview_name(self, self.name_normalizer_selected_file)
        if preview_result:
            self.log_and_show(f"Preview: \n{os.path.basename(preview_result)}", create_messagebox=True)
        return
    elif mode == "action":
        # Ask for confirmation before normalizing files
        confirmation = ask_confirmation(self, "Confirm Action",
                                        "Are you sure you want normalize the file(s)? This cannot be undone.")
        if confirmation:
            self.log_and_show(f"User confirmed the name normalization process for "
                              f"{self.name_normalizer_selected_file}.")
        else:
            self.log_and_show(f"User cancelled the name normalization process for "
                              f"{self.name_normalizer_selected_file}.")
            return

    try:
        if os.path.isfile(self.name_normalizer_selected_file):
            # If a single file is provided, directly process it
            rename_and_move_file(self, self.name_normalizer_selected_file)
        else:
            # Get folder contents and save to memory

            # Initialize an empty list to store file paths
            file_paths = []

            # Log the os.walk state
            if self.deep_walk_var.get():
                deep_walk_status = "including subdirectories"
            else:
                deep_walk_status = "excluding subdirectories"
            self.log_and_show(f"Info: os.walk, {deep_walk_status}, started on '{self.name_normalizer_selected_file}'")

            # Traverse through the folder using os.walk
            for root, dirs, files in os.walk(self.name_normalizer_selected_file):
                # Include subdirectories if the deep_walk_var is True or the root folder is selected
                if self.deep_walk_var.get() or root == self.name_normalizer_selected_file:
                    for file in files:
                        # Append the full file path to the list
                        file_paths.append(str(os.path.join(root, file)))

            # Iterate through file paths and rename/move files
            for file_path in file_paths:
                rename_and_move_file(self, file_path)

        # Log the action if logging is enabled
        self.log_and_show("File(s) have been processed successfully.")

        # Reset GUI input fields if reset is True
        if self.reset_var.get():
            # Clear selection for the name_normalizer_window
            self.clear_selection(frame_name="name_normalizer_window")

    except Exception as e:
        # Display error message if an exception occurs
        self.log_and_show(f"An error occurred: {e}",
                          create_messagebox=True,
                          error=True)


"""
Video Editor
"""


# Function to generate a non-conflicting filename
def get_non_conflicting_filename(self, path):
    # Log the action and display a message
    self.log_and_show(f"Conflict detected on: '{os.path.basename(path)}'")

    try:
        # Split the given path into the base filename and its extension.
        base, ext = os.path.splitext(os.path.basename(path))

        # Extract the counter from the original filename if it exists.
        counter = 1
        match = re.match(r'(.+) \((\d+)\)', base)
        if match:
            base, counter = match.groups()
            counter = int(counter)

        # Check if the file already exists at the given path.
        while os.path.exists(os.path.join(os.path.dirname(path), f"{base} ({counter}){ext}")):
            # If the file exists, update the counter.
            counter += 1

        # Construct the new base filename with the updated counter.
        new_base = f"{base} ({counter})"

        # Construct the new path by joining the directory and the new base filename.
        new_path = os.path.join(os.path.dirname(path), f"{new_base}{ext}")

        # Log action and display a message
        self.log_and_show(f"Using non-conflicting file name: {new_base}{ext}")

        # Return the generated non-conflicting filename.
        return new_path
    except Exception as e:
        # Log error and display an error message when get non-conflicting file name fails.
        self.log_and_show(f"Getting non-conflicting file name failed: {str(e)}",
                          create_messagebox=True,
                          error=True)

        # Return None in case of an error.
        return None


# Function to remove a successful line from a file.
def remove_successful_line_from_file(self, file_path, line_to_remove):
    try:
        if self.remove_successful_lines_var.get():
            # Read all lines from the file.
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Open the file in write mode to remove the specified line.
            with open(file_path, 'w') as file:
                # Write lines back to the file, excluding the successful line to remove.
                for line in lines:
                    if line.strip() != line_to_remove:
                        file.write(line)

    except Exception as e:
        # Log the exception using the logging module.
        self.log_and_show(f"An error occurred while removing line from file: {e}",
                          create_messagebox=True,
                          error=True)


# Method to rotate a video clip by a specified angle.
def rotate_video(self, clip, rotation_angle):
    try:
        # Rotate the video clip by the specified angle.
        rotated_clip = clip.rotate(rotation_angle)

        # Log rotation success if logging is activated.
        self.log_and_show(f"Rotation successful {rotation_angle}")

        # Return the rotated video clip.
        return rotated_clip

    except Exception as e:
        # Log error and display an error message if rotation fails.
        self.log_and_show(f"Rotating video failed: {str(e)}",
                          create_messagebox=True,
                          error=True)

        # Return None in case of an error.
        return None


# Method to increase the volume of a video clip by a specified dB value.
def increase_volume(self, clip, increase_db):
    try:
        # Modify the volume of the video clip by converting dB to linear scale.
        modified_clip = clip.volumex(10 ** (increase_db / 20.0))

        # Log amplification success if logging is activated.
        self.log_and_show(f"Amplification successful {increase_db}")

        # Return the modified video clip.
        return modified_clip

    except Exception as e:
        # Log error and display an error message if volume increase fails.
        self.log_and_show(f"Increasing volume failed: {str(e)}",
                          create_messagebox=True,
                          error=True)

        # Return None in case of an error.
        return None


# Method to normalize the audio of a video clip by applying a volume multiplier.
def normalize_audio(self, clip, volume_multiplier):
    try:
        # Normalize the audio of the video clip by applying the specified volume multiplier.
        normalized_clip = clip.volumex(volume_multiplier)

        # Log audio normalization success if logging is activated.
        self.log_and_show(f"Audio Normalization successful {volume_multiplier}")

        # Return the normalized video clip.
        return normalized_clip

    except Exception as e:
        # Log error and display an error message if audio normalization fails.
        self.log_and_show(f"Normalizing audio failed: {str(e)}",
                          create_messagebox=True,
                          error=True)

        # Return None in case of an error.
        return None


# Method to trim a video by a specified time value.
def trim_video(self, clip, total_time):
    try:
        # Trim the clip to remove the specified duration.
        trimmed_clip = clip.subclip(total_time)

        # Log normalization success if logging is activated.
        self.log_and_show(f"Trimming successful {total_time}")

        # Return the trimmed video clip.
        return trimmed_clip

    except Exception as e:
        # Log error and display an error message if trimming fails.
        self.log_and_show(f"Trimming failed: {str(e)}",
                          create_messagebox=True,
                          error=True)

        # Return None in case of an error.
        return None


# Method to process video edits based on user inputs.
# noinspection PyTypeChecker
def process_video_edits(self):
    try:
        # Get input parameters from user interface.
        rotation = str(self.rotation_var.get())
        decibel = float(self.decibel_entry.get().strip())
        audio_normalization = float(self.audio_normalization_entry.get().strip())
        minutes = int(self.minute_entry.get().strip())
        seconds = int(self.second_entry.get().strip())
    except ValueError as e:
        self.log_and_show(f"Value error: Please enter a valid value. {str(e)}",
                          create_messagebox=True,
                          error=True)
        return

    # Check if minutes is 00 and set variable to None
    if minutes == 0:
        minutes = None
        adjusted_minutes = 0
    else:
        adjusted_minutes = minutes

    # Check if seconds is 00 and set variable to None
    if seconds == 0:
        seconds = None
        adjusted_seconds = 0
    else:
        adjusted_seconds = seconds

    # Convert time to seconds
    total_time = adjusted_minutes * 60 + adjusted_seconds

    # If there is nothing to trim, set trim to False
    trim = total_time != 0

    # Check if rotation is none and set to variable to None
    if rotation == "none":
        rotation = None

    # Check if decibel is 0.0 and set to variable to None
    if decibel == 0.0:
        decibel = None

    # Check if rotation is none and set variable to None
    if audio_normalization == 0.0:
        audio_normalization = None

    # Check if an input source is provided
    if not self.video_editor_selected_file:
        self.log_and_show("Input must be specified (video file, line separated txt, or directory.",
                          create_messagebox=True,
                          error=True)
        return

    # Check if the provided input exists
    if self.video_editor_selected_file and not os.path.exists(self.video_editor_selected_file):
        self.log_and_show("The input does not exist or cannot be found. Please try again.",
                          create_messagebox=True,
                          error=True)
        return

    # Check if the necessary parameters for video editing are provided
    if (self.video_editor_selected_file and decibel is None and rotation is None and audio_normalization is None
            and minutes is None and seconds is None):
        self.log_and_show("You need to specify an operation (audio increase, video rotation, "
                          "audio normalization, trim, or some combination of them)",
                          create_messagebox=True,
                          error=True)
        return

    # Check if the provided output directory exists
    if self.video_editor_output_directory and not os.path.exists(self.video_editor_output_directory):
        self.log_and_show("The output directory does not exist or cannot be found. Please try again.",
                          create_messagebox=True,
                          error=True)
        return

    # Define which input paths based on user input (Video file, .txt file, or directory)
    try:
        # Video file
        if os.path.isfile(self.video_editor_selected_file) and any(self.video_editor_selected_file.lower().endswith(ext)
                                                                   for ext in self.valid_extensions):
            input_paths = [self.video_editor_selected_file]
        # .txt file
        elif os.path.isfile(self.video_editor_selected_file) and self.video_editor_selected_file.lower().endswith(
                '.txt'):
            with open(self.video_editor_selected_file, 'r') as file:
                input_paths = [line.strip() for line in file if
                               os.path.splitext(line.strip())[1].lower() in self.valid_extensions]
        # Directory
        elif os.path.isdir(self.video_editor_selected_file):
            # Ask for confirmation before normalizing files
            confirmation = ask_confirmation(self, "Confirm Action",
                                            "Are you sure you want edit ALL video files in the provided directory?"
                                            "\nThis option may be computer intensive.")
            if confirmation:
                self.log_and_show(f"User confirmed the directory for {self.video_editor_selected_file}.")

                # Get the absolute file paths of all files within the directory with valid extensions
                input_paths = []
                for root, dirs, files in os.walk(self.video_editor_selected_file):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.splitext(file_path)[1].lower() in self.valid_extensions:
                            input_paths.append(file_path)
            else:
                # If the user does not confirm the directory, return
                return

        else:
            raise ValueError("Invalid input detected. Please select a video file, .txt file with video file paths, "
                             "or a directory with video files")
    except Exception as e:
        self.log_and_show(f"Processing input failed: {str(e)}",
                          create_messagebox=True,
                          error=True)
        return

    # Redirect MoviePy output for video edits
    self.redirect_output()

    # Process each input path
    for input_path in input_paths:
        try:
            # Check if the file name length exceeds 255 characters
            if len(input_path) > 255:
                self.log_and_show(f"File over 255 warning!!! Fix: {input_path}", error=True)

                # Create a temporary copy of the file
                temp_dir = os.path.dirname(input_path)
                temp_copy_path = os.path.join(temp_dir, 'temp.mp4')
                shutil.copyfile(input_path, temp_copy_path)
            else:
                temp_copy_path = input_path

            # Extract filename, extension, and output directory
            filename, extension = os.path.splitext(os.path.basename(temp_copy_path))
            output_dir = os.path.dirname(temp_copy_path)

            # Determine the rotation operation tag
            rotation_angle = None  # Default rotation angle
            if rotation and rotation != "none":
                if rotation == "left":
                    rotation_angle = 90
                elif rotation == "right":
                    rotation_angle = -90
                elif rotation == "flip":
                    rotation_angle = -180

            # Create the output path with the operation suffix
            output_path = os.path.join(output_dir, f"{filename}_EDITED{extension}")

            # Adjust output path if a video output directory is specified
            if self.video_editor_output_directory:
                output_path = os.path.join(self.video_editor_output_directory, os.path.basename(output_path))

            # Check if the new_path exists
            if os.path.exists(output_path):
                # Get a non-conflicting name for the output path
                output_path = self.get_non_conflicting_filename(output_path)

            # Load the original video clip
            original_clip = VideoFileClip(temp_copy_path)
            successful_operations = True

            # Apply operations in sequence, checking for success
            if rotation_angle is not None and successful_operations:
                processed_clip = rotate_video(self, original_clip, rotation_angle)
                if processed_clip:
                    original_clip = processed_clip
                else:
                    successful_operations = False

            if decibel and successful_operations:
                processed_clip = increase_volume(self, original_clip, decibel)
                if processed_clip:
                    original_clip = processed_clip
                else:
                    successful_operations = False

            if audio_normalization and successful_operations:
                processed_clip = normalize_audio(self, original_clip, audio_normalization)
                if processed_clip:
                    original_clip = processed_clip
                else:
                    successful_operations = False

            if trim and successful_operations:
                processed_clip = trim_video(self, original_clip, total_time)
                if processed_clip:
                    original_clip = processed_clip
                else:
                    successful_operations = False

            # Write the final modified clip to the output path if all operations were successful
            if successful_operations:
                original_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

                # Log the action if logging is enabled
                self.log_and_show(f"Video saved as {os.path.basename(output_path)}"
                                  f"\nPath: {output_path}")

                # Set the video editor last used file upon success
                self.video_editor_last_used_file = output_path

                if self.reset_video_entries_var.get():
                    # Clear selection for the video_editor_window
                    self.clear_selection(frame_name="video_editor_window")

                # Remove the successfully processed line from the input file
                if self.video_editor_selected_file:
                    remove_successful_line_from_file(self, self.video_editor_selected_file, input_path)
            else:
                self.log_and_show(f"Operations failed for video {os.path.basename(input_path)}",
                                  create_messagebox=True,
                                  error=True)

            # Close the original clip to free resources
            original_clip.close()

            # Reset redirect MoviePy output for video edits
            self.redirect_output()

            if len(input_path) > 255:
                # Delete the temporary copy
                os.remove(temp_copy_path)

        except OSError as e:
            # Log error and skip to the next file in case of OSError
            self.log_and_show(f"OSError: {str(e)} Skipping this file and moving to the next one.",
                              create_messagebox=True,
                              error=True)
            continue


"""
add_remove_window
"""


# Function to add artists to the artist file
def add_artist_to_file(self):
    # Check if self.add_artist is None
    if not self.add_artist:
        # Get the artist to be added from the entry widget
        self.add_artist = self.add_artist_entry.get().strip()

        # Check if no artist is provided
        if not self.add_artist:
            self.log_and_show("Add Artist cannot be empty.",
                              create_messagebox=True,
                              error=True)
            return  # Exit the function if no artist is provided

    # Read the list of artists from the artist_file
    try:
        with open(self.artist_file, 'r') as artist_list_file:
            artist_list = [artist.strip() for artist in artist_list_file]
    except FileNotFoundError:
        self.log_and_show(f"Artist File '{self.artist_file}' not found.",
                          create_messagebox=True,
                          error=True)
        return  # Exit the function if the artist_file is not found

    # Check if the add_artist is already in the list (case-insensitive)
    if any(artist.lower() == self.add_artist.lower() for artist in artist_list):
        self.log_and_show(f"Artist is already in the Artist File: '{self.add_artist}'",
                          create_messagebox=True,
                          error=True)
    else:
        # Add the add_artist to the list
        artist_list.append(self.add_artist)

        # Write the updated list back to the artist_file
        try:
            with open(self.artist_file, 'w') as artist_list_file:
                artist_list_file.write('\n'.join(artist_list))
            self.log_and_show(f"Added artist to the Artist File: '{self.add_artist}'")

        except IOError:
            self.log_and_show(f"Writing to Artist File failed: '{self.artist_file}'.",
                              create_messagebox=True,
                              error=True)

    # Reset the artist entries if the action is successful
    if self.reset_artist_entries_var.get():
        # Clear add artist entry
        self.add_artist = ""
        self.add_artist_entry.delete(0, ctk.END)


# Function to remove artists from the artist file
def remove_artist_from_file(self):
    # Check if self.remove_artist is None
    if not self.remove_artist:
        # Get the artist to be removed from the entry widget
        self.remove_artist = self.remove_artist_entry.get().strip()

        # Check if no artist is provided
        if not self.remove_artist:
            self.log_and_show("Remove Artist cannot be empty.",
                              create_messagebox=True,
                              error=True)
            return  # Exit the function if no artist is provided

    try:
        # Read the list of artists from the artist_file
        with open(self.artist_file, 'r') as artist_list_file:
            artist_list = [artist.strip() for artist in artist_list_file]
    except FileNotFoundError:
        self.log_and_show(f"Artist File '{self.artist_file}' not found.",
                          create_messagebox=True,
                          error=True)
        return  # Exit the function if the artist_file is not found

    # Check if the remove_artist is in the list (case-insensitive)
    if any(artist.lower() == self.remove_artist.lower() for artist in artist_list):
        # Remove the remove_artist from the list
        artist_list = [artist for artist in artist_list if artist.lower() != self.remove_artist.lower()]

        # Write the updated list back to the artist_file
        try:
            with open(self.artist_file, 'w') as artist_list_file:
                artist_list_file.write('\n'.join(artist_list))
            self.log_and_show(f"Removed artist from the Artist File: '{self.remove_artist}'")

        except IOError:
            self.log_and_show(f"Writing to Artist File failed: '{self.artist_file}'.",
                              create_messagebox=True,
                              error=True)
    else:
        self.log_and_show(f"Artist is not in the Artist File: '{self.remove_artist}'",
                          create_messagebox=True,
                          error=True)

    # Reset the artist entries if the action is successful
    if self.reset_artist_entries_var.get():
        # Clear remove artist entry
        self.remove_artist = ""
        self.remove_artist_entry.delete(0, ctk.END)


# Function to create a NO-GO file
def no_go_creation(self):
    # Check if self.no_go_name is None
    if not self.no_go_name:
        # Attempt to get the contents from self.add_no_go_name_entry
        self.no_go_name = self.add_no_go_name_entry.get().strip()

        # Check if self.no_go_name is provided
        if not self.no_go_name:
            self.log_and_show("Add NO GO cannot be empty.",
                              create_messagebox=True,
                              error=True)
            return  # Exit the function if no artist is provided

    try:
        # Expand the user's home directory in the NO-GO path
        no_go_directory = os.path.expanduser(self.no_go_directory)

        # Ensure the NO-GO directory exists, create it if not
        if not os.path.exists(no_go_directory):
            os.makedirs(no_go_directory)

        # Create a file for the NO-GO
        file_name = f"NO GO - {self.no_go_name}"
        file_path = os.path.join(no_go_directory, file_name)

        # Create NO-GO empty file
        with open(file_path, 'w'):
            pass

        # Add to text file for Tampermonkey Script use
        if not os.path.isfile(self.no_go_artist_file):
            # If the file does not exist, create it
            with open(self.no_go_artist_file, "w"):
                pass  # do nothing, just create an empty file

        # Write the no_go_name to the file
        with open(self.no_go_artist_file, "a") as file:
            file.write("\n" + self.no_go_name)

        # Log the action if logging is enabled
        self.log_and_show(f"NO GO created successfully for {self.no_go_name} in \n"
                          f"{no_go_directory}")

    except Exception as e:
        self.log_and_show(f"Creating NO GO failed: '{str(e)}'.",
                          create_messagebox=True,
                          error=True)

    # Clear add no-go name entry and reset self.no_go_name
    self.no_go_name = ""
    self.add_no_go_name_entry.delete(0, ctk.END)


# Function to exclude folder from Artist Directory search
def add_folder_to_excluded_folders(self):
    if not self.exclude_name:
        # Get the exclude name to be added from the entry widget
        self.exclude_name = self.add_exclude_name_entry.get().strip()

        # Check if no exclude name is provided
        if not self.exclude_name:
            self.log_and_show("Add Exclude cannot be empty.",
                              create_messagebox=True,
                              error=True)
            return  # Exit the function if no exclusion is provided

    # Check if the folder is already in the excluded_folders list
    if self.exclude_name in self.excluded_folders:
        self.log_and_show(f"Folder '{self.exclude_name}' is already in the excluded folders list.",
                          create_messagebox=True,
                          error=True)
        # Reset the exclude entry
        self.exclude_name = ""
        self.add_exclude_name_entry.delete(0, ctk.END)
        return  # Exit the function if the folder is already in the list

    try:
        # Add the folder to the excluded_folders list
        self.excluded_folders.append(self.exclude_name)

        # Update the JSON file with the new excluded_folders list
        with open(self.excluded_file, 'w') as json_file:
            json.dump({"excluded_folders": self.excluded_folders}, json_file, indent=2)

        # Log and show success message
        self.log_and_show(f"Folder '{self.exclude_name}' added to excluded folders list.")

        # Reset the exclude entry if the action is successful
        self.exclude_name = ""
        self.add_exclude_name_entry.delete(0, ctk.END)

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Error adding folder '{self.exclude_name}' to excluded folders list: {e}",
                          create_messagebox=True,
                          error=True)
