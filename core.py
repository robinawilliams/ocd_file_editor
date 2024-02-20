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
from moviepy.video.fx import all as vfx  # Importing all video effects (vfx) from the moviepy library
from gui import SelectOptionWindow  # Import the SelectOptionWindow for Ask Confirmation purposes

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
    dictionary_file = config.get('Filepaths', 'dictionary_file', fallback='dictionary.json')

    # Variables and window geometry
    geometry = config.get('Settings', 'geometry', fallback='1280x850')
    scaling = config.get('Settings', 'scaling', fallback='100')
    column_numbers = config.get('Settings', 'column_numbers', fallback=7)
    default_weight = config.get('Settings', 'default_weight', fallback=9)
    default_ctn_weight = config.get('Settings', 'default_ctn_weight', fallback=1)
    default_decibel = config.get('Settings', 'default_decibel', fallback=0.0)
    default_audio_normalization = config.get('Settings', 'default_audio_normalization', fallback=0.0)
    default_minute = config.get('Settings', 'default_minute', fallback=0)
    default_second = config.get('Settings', 'default_second', fallback=0)
    default_most_number = config.get('Settings', 'default_most_number', fallback=9)
    default_frame = config.get('Settings', 'default_frame', fallback="file_renamer_window")
    default_tab = config.get('Settings', 'default_tab', fallback="All")
    default_add_remove_tab = config.get('Settings', 'default_add_remove_tab', fallback="Artist")
    file_renamer_log = config.get('Logs', 'file_renamer_log', fallback="file_renamer.log")
    default_placement_var = config.get("Settings", "default_placement_var", fallback="special_character")
    special_character_var = config.get("Settings", "special_character_var", fallback="-")
    keyword_var = config.get("Settings", "keyword_var", fallback="Sort")
    reset_output_directory_var = config.getboolean("Settings", "reset_output_directory_var", fallback=False)
    use_custom_tab_names_var = config.getboolean("Settings", "use_custom_tab_names_var", fallback=False)
    sort_tab_names_var = config.getboolean("Settings", "sort_tab_names_var", fallback=False)
    sort_reverse_order_var = config.getboolean("Settings", "sort_reverse_order_var", fallback=False)
    suggest_output_directory_var = config.getboolean("Settings", "suggest_output_directory_var", fallback=False)
    artist_identifier_var = config.getboolean("Settings", "artist_identifier_var", fallback=False)
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
    remove_custom_text_var = config.getboolean("Settings", "remove_custom_text_var", fallback=False)
    replace_mode_var = config.getboolean("Settings", "replace_mode_var", fallback=False)
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
    reset_add_remove_var = config.getboolean("Settings", "reset_add_remove_var", fallback=True)
    deep_walk_var = config.getboolean("Settings", "deep_walk_var", fallback=False)

    # Video Editor
    remove_successful_lines_var = config.getboolean("Settings", "remove_successful_lines_var", fallback=False)
    default_rotation_var = config.get("Settings", "default_rotation_var", fallback="none")

    # Return the loaded configuration values as a tuple
    return (move_text_var, initial_directory, artist_directory, double_check_directory, keyword_var,
            geometry, reset_output_directory_var, suggest_output_directory_var, move_up_directory_var,
            open_on_file_drop_var, remove_duplicates_var, default_placement_var, special_character_var,
            double_check_var, activate_logging_var, file_renamer_log, column_numbers, default_weight,
            use_custom_tab_names_var, remove_all_symbols_var, tail_var, remove_parenthesis_trail_var,
            remove_hashtag_trail_var, remove_new_var, remove_dash_var, remove_endash_var, remove_emdash_var,
            remove_ampersand_var, remove_at_var, remove_underscore_var, remove_comma_var, remove_single_quote_var,
            remove_double_quote_var, title_var, reset_var, initial_output_directory, artist_file, default_frame,
            artist_file_search_var, deep_walk_var, default_decibel, default_audio_normalization,
            remove_successful_lines_var, default_rotation_var, remove_double_space_var, remove_colon_var,
            remove_semicolon_var, remove_percent_var, remove_caret_var, remove_dollar_var, remove_asterisk_var,
            remove_plus_var, remove_equal_var, remove_curly_brace_var, remove_square_bracket_var, remove_pipe_var,
            remove_backslash_var, remove_angle_bracket_var, remove_question_mark_var, remove_parenthesis_var,
            remove_hashtag_var, show_messageboxes_var, show_confirmation_messageboxes_var, fallback_confirmation_var,
            default_tab, suppress_var, reset_video_entries_var, reset_add_remove_var, remove_most_symbols_var,
            remove_number_var, default_minute, default_second, no_go_directory, no_go_artist_file, dictionary_file,
            remove_non_ascii_symbols_var, artist_identifier_var, sort_tab_names_var, sort_reverse_order_var,
            default_most_number, scaling, default_ctn_weight, remove_custom_text_var, replace_mode_var,
            default_add_remove_tab)


# Function to load the json file (exclude_file and weight_to_tab_name dictionaries)
def initialize_json(self):
    # Load data from the dictionary_file
    try:
        if not os.path.isfile(self.dictionary_file):
            # Return early if the file doesn't exist
            return

        with open(self.dictionary_file, "r") as json_file:
            data = json.load(json_file)

            # Get categories dictionary
            self.categories = data.get("categories", {})

            # Get custom_text_to_remove dictionary
            self.custom_text_to_remove = data.get("custom_text_to_remove", [])

            # Get excluded_folders dictionary
            self.excluded_folders = data.get("excluded_folders", [])

            # Get file_extensions dictionary
            self.file_extensions = data.get("file_extensions", [])

            # Get valid_extensions dictionary
            self.valid_extensions = data.get("valid_extensions", [])

            # Get weight_to_tab_name dictionary
            weight_to_tab_name = data.get("weight_to_tab_name", {})
            # Make sure the keys are integers
            self.weight_to_tab_name = {int(key): value for key, value in weight_to_tab_name.items()}

    except FileNotFoundError:
        # Log that the file is not found
        self.log_and_show(f"Exclusion file not found: {self.dictionary_file}")

    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        self.log_and_show(f"Error decoding JSON in exclusion file: {self.dictionary_file}, {str(e)}", error=True)

    except Exception as e:
        self.log_and_show(f"Initialize exclusion_file failed: {self.dictionary_file}, {str(e)}", error=True)


# Function to update the json dictionary
def update_json(self, file_to_update, dictionary_name, updated_data):
    try:
        if not os.path.isfile(file_to_update):
            # Return early if the file doesn't exist
            raise FileNotFoundError

        # Read existing JSON data
        with open(file_to_update, 'r') as json_file:
            data = json.load(json_file)

        # Update the dictionary key
        data[dictionary_name] = updated_data

        # Sort the dictionary alphabetically
        sorted_data = {key: value for key, value in sorted(data.items())}

        # Write the sorted data back to the JSON file
        with open(file_to_update, 'w') as json_file:
            json.dump(sorted_data, json_file, indent=2)

    except FileNotFoundError:
        # Log that the file is not found
        self.log_and_show(f"JSON file not found: {file_to_update}", create_messagebox=True, error=True)

    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        self.log_and_show(f"Decoding JSON in JSON file failed: {file_to_update}, {str(e)}", error=True)

    except Exception as e:
        self.log_and_show(f"Updating JSON failed: {file_to_update}, {str(e)}", error=True)


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
            confirmation = self.ask_confirmation("Confirm Action",
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
            self.log_and_show("No input selected. Cannot move to trash.", create_messagebox=True, error=True)
    except OSError as e:
        self.log_and_show(f"{str(e)}", create_messagebox=True, error=True)


# Function to create double check reminders
def double_check_reminder(self, new_path):
    try:
        # Get the name of the folder immediately above the current location
        folder_name = os.path.basename(os.path.dirname(new_path))

        # Ask for confirmation of the double check reminder
        confirmation = self.ask_confirmation("Double Check Reminder",
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
                          create_messagebox=True, error=True)


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
                              create_messagebox=True, error=True)
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
                              create_messagebox=True, error=True)
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
                              create_messagebox=True, error=True)


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
                              create_messagebox=True, error=True)

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
                              create_messagebox=True, error=True)

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
                                  create_messagebox=True, error=True)
        else:
            # Input not selected
            self.log_and_show("No input selected. Cannot send to module",
                              create_messagebox=True, error=True)
    else:
        # Invalid frame name
        self.log_and_show("Invalid frame name for send to module",
                          create_messagebox=True, error=True)
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
                          create_messagebox=True, error=True)
        return

    # If the input path is not empty, try to open the input using the default system program
    if file_to_open:
        try:
            subprocess.Popen(['xdg-open', file_to_open])

            # Log a success message if the input is opened successfully
            self.log_and_show(f"Input opened: {filename}")
        except OSError as e:
            # If an error occurs while opening the file, log the error
            self.log_and_show(f"{str(e)}", create_messagebox=True, error=True)


# Function to add a category to the queue
def add_to_queue(self, category):
    if self.file_renamer_selected_file:
        # Check if the category is not already in the queue
        if category not in self.queue:
            # Add the category to the queue
            self.queue.append(category)
            self.log_and_show(f"Word added to queue: {category}", not_logging=True)

        # Check if the category is already in the queue
        elif category in self.queue:
            # Ask for confirmation of removing the category from the queue
            confirmation = self.ask_confirmation("Queue Conflict",
                                                 f"{category} is already in the queue. Do you want to remove it?")

            if confirmation:
                # Remove the category from the queue
                self.queue.remove(category)
                self.log_and_show(f"Word removed from queue: {category}", not_logging=True)

        # Update file display
        self.update_file_display()
    else:
        # If no input selected, log the action and display a message in the GUI
        self.log_and_show("Please select an input first and then add a word to the queue.",
                          create_messagebox=True, error=True)


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
        if len(name) > 255:
            self.log_and_show("The proposed file name exceeds 255 characters. "
                              "Operating system limitations prohibit this.",
                              create_messagebox=True, error=True)
            # Truncate the name
            name = f"...{name[180:]}"

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
        self.log_and_show("Last category removed", not_logging=True)
    else:
        # Log the action if logging is enabled
        self.log_and_show("Nothing in the queue. Nothing to undo.",
                          create_messagebox=True, error=True)


# Function to undo the last file rename operation
def undo_file_rename(self):
    if self.frame_name == "file_renamer_window":
        if self.history:
            # Get the last operation from the history
            last_operation = self.history.pop()

            # Extract the information needed to revert the changes
            original_path, new_path = last_operation['original_path'], last_operation['new_path']

            # Ask for confirmation of the undo file rename operation
            confirmation = self.ask_confirmation("Undo File Rename",
                                                 f"Do you want to undo the file rename operation?: "
                                                 f"\n{os.path.basename(new_path)}"
                                                 f"\nOriginal name: "
                                                 f"\n{os.path.basename(original_path)}")

            if confirmation:
                try:
                    # Attempt to revert the changes by renaming the file back to the original path
                    os.rename(new_path, original_path)

                    # Log and display a message
                    self.log_and_show(f"Undo successful. File reverted to: \n{original_path}")

                    # Set the last used file
                    self.file_renamer_last_used_file = original_path
                except OSError as e:
                    if "Invalid cross-device link" in str(e):
                        # Attempt to use shutil.move if "Invalid cross-device link" error
                        try:
                            shutil.move(new_path, original_path)
                            self.log_and_show(
                                f"File: '{os.path.basename(new_path)}' renamed and moved successfully. "
                                f"\nSaved to: \n{original_path}")
                            # Set the last used file
                            self.file_renamer_last_used_file = original_path
                        except Exception as move_error:
                            # Log the action if shutil.move also fails
                            self.log_and_show(f"Renaming and moving file failed: {str(move_error)}",
                                              create_messagebox=True, error=True)
                    else:
                        # Log the action for other OSError
                        self.log_and_show(f"{str(e)}", create_messagebox=True, error=True)

            else:
                # If the user declines, re-add the operation to the history
                self.history.append(last_operation)
                return
        else:
            # Log the action if logging is enabled
            self.log_and_show("No previous file rename operation. Nothing to undo.", create_messagebox=True, error=True)

    elif self.frame_name == "name_normalizer_window":
        if self.nn_history:
            # Get the last operation from the nn_history
            last_operation = self.nn_history.pop()

            # Extract the information needed to revert the changes
            original_paths, new_paths = last_operation['original_paths'], last_operation['new_paths']

            # Filter out None values from new_paths
            new_paths = [path for path in new_paths if path is not None]

            # Truncate paths if they exceed a certain limit (Beautify the data for the gui)
            max_display_paths = 3
            truncated_original_paths = original_paths[:max_display_paths]
            truncated_new_paths = new_paths[:max_display_paths]
            truncated_original_paths_str = ', '.join(os.path.basename(path) for path in truncated_original_paths)
            truncated_new_paths_str = ', '.join(os.path.basename(path) for path in truncated_new_paths)
            if len(original_paths) > max_display_paths:
                truncated_original_paths_str += f", and {len(original_paths) - max_display_paths} more..."
            if len(new_paths) > max_display_paths:
                truncated_new_paths_str += f", and {len(new_paths) - max_display_paths} more..."

            # Ask for confirmation of the undo name normalizer operation
            confirmation = self.ask_confirmation("Undo Name Normalizer",
                                                 f"Do you want to undo the name normalizer operation?: "
                                                 f"\n{truncated_new_paths_str}"
                                                 f"\n\nOriginal names: "
                                                 f"\n{truncated_original_paths_str}")

            if confirmation:
                try:
                    # Attempt to revert the changes by renaming/moving the files back to their original paths
                    for original_path, new_path in zip(original_paths, new_paths):
                        # Check if new path is provided and skip if the there is no change
                        if new_path is not None and (original_path != new_path):
                            try:
                                # Check if the file exists
                                if not os.path.isfile(new_path):
                                    # Raise error if not found
                                    raise FileNotFoundError

                                # Rename the file
                                os.rename(new_path, original_path)
                            except FileNotFoundError:
                                # Handle the file not found error and log an error message
                                self.log_and_show(f"File not found: "
                                                  f"\n{new_path}",
                                                  create_messagebox=True, error=True)
                                continue
                            except OSError as e:
                                # Use shutil as a fallback
                                if "Invalid cross-device link" in str(e):
                                    try:
                                        # Rename the file and move it across devices
                                        shutil.move(new_path, original_path)
                                    except Exception as e:
                                        # Handle any exceptions and log an error message
                                        self.log_and_show(f"Unexpected error renaming: "
                                                          f"\n{new_path}"
                                                          f"\n{original_path} "
                                                          f"\n{e}",
                                                          create_messagebox=True, error=True)
                                        continue

                    # Log and display a message
                    self.log_and_show(f"Undo successful. Files reverted to: \n{', '.join(original_paths)}")

                    # Set the last used file
                    self.name_normalizer_last_used_file = original_paths[-1]
                except OSError as e:
                    # Log the action for other OSError
                    self.log_and_show(f"{str(e)}", create_messagebox=True, error=True)

            else:
                # If the user declines, re-add the operation to the nn_history
                self.nn_history.append(last_operation)
                return
        else:
            # Log the action if logging is enabled
            self.log_and_show("No previous name normalizer operation. Nothing to undo.", create_messagebox=True,
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
        self.custom_text_removal_entry.delete(0, ctk.END)

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
        # Get the active tab from the add_remove_tabview
        active_tag = self.add_remove_tabview.get()

        if active_tag == "Artist":
            # Clear add artist entry
            self.add_artist_entry.delete(0, ctk.END)

            # Clear remove artist entry
            self.remove_artist_entry.delete(0, ctk.END)

        elif active_tag == "Category":
            # Clear add category entry
            self.category_entry.delete(0, ctk.END)

            self.weight_entry.delete(0, ctk.END)

            # Clear remove category entry
            self.remove_category_entry.delete(0, ctk.END)

        elif active_tag == "Custom Tab Name":
            # Clear add custom tab name entry
            self.custom_tab_name_entry.delete(0, ctk.END)

            self.weight_entry1.delete(0, ctk.END)

            # Clear remove custom tab name entry
            self.remove_custom_tab_name_entry.delete(0, ctk.END)

        elif active_tag == "Custom Text to Remove":
            # Clear add custom text to remove entry
            self.add_ctr_name_entry.delete(0, ctk.END)

            # Clear remove custom text to remove entry
            self.remove_ctr_name_entry.delete(0, ctk.END)

        elif active_tag == "Exclude":
            # Clear add exclude entry
            self.add_exclude_name_entry.delete(0, ctk.END)

            # Clear remove exclude entry
            self.remove_exclude_name_entry.delete(0, ctk.END)

        elif active_tag == "File Extensions":
            # Clear add extension entry
            self.add_file_extension_entry.delete(0, ctk.END)

            # Clear remove extension entry
            self.remove_file_extension_entry.delete(0, ctk.END)

        elif active_tag == "NO GO":
            # Clear add NO-GO entry
            self.add_no_go_name_entry.delete(0, ctk.END)

            # Clear remove NO-GO entry
            self.remove_no_go_name_entry.delete(0, ctk.END)

        elif active_tag == "Valid Extensions":
            # Clear add extension entry
            self.add_valid_extension_entry.delete(0, ctk.END)

            # Clear remove extension entry
            self.remove_valid_extension_entry.delete(0, ctk.END)
        else:
            # Invalid tab name
            return
    else:
        # Invalid frame name
        return

    # Log action and display message on the applicable frame
    self.log_and_show("Selection cleared", not_logging=True)


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
            # Set the name normalizer selected file
            self.name_normalizer_selected_file = nn_input_method

            # Extract just the file name, not the absolute file path
            filename = os.path.basename(nn_input_method)

            # Reset the entry and insert the filename
            self.nn_path_entry.delete(0, ctk.END)
            self.nn_path_entry.insert(0, filename)

            # Log the action if logging is enabled
            self.log_and_show(f"Input selected via Browse: {filename}")

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
            filename = os.path.basename(input_method)

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
                          create_messagebox=True, error=True)
        return None

    try:
        # Create a list from self.artist_directory
        artist_folders = os.listdir(self.artist_directory)

        # Use self.excluded_folders to remove any matches (case-insensitive) from the list
        excluded_folders_lower = [folder.lower() for folder in self.excluded_folders]
        artist_folders = [folder for folder in artist_folders if folder.lower() not in excluded_folders_lower]

        # Extract the base name from the selected file
        base_name = os.path.basename(self.file_renamer_selected_file)
        base_name_lower = base_name.lower()  # Case insensitive comparison

        # Extract the artist from the filename
        matching_artists = []

        # Use the filtered list to match the artist_folder
        for artist_folder in artist_folders:
            if artist_folder.lower() in base_name_lower:
                # Construct the artist folder path
                artist_folder_path = os.path.join(self.artist_directory, artist_folder)

                # Verify the folder exists
                if os.path.exists(artist_folder_path) and os.path.isdir(artist_folder_path):
                    matching_artists.append(artist_folder_path)

        # Check if there are multiple matches
        if len(matching_artists) > 1:
            # Prompt the user to choose from the list using SelectOptionWindow
            artist_selection_window = SelectOptionWindow(title="Choose Artist",
                                                         prompt="Multiple matching artists found. Choose an artist:",
                                                         item_list=matching_artists,
                                                         label_text="Select Artist")

            # Wait for the user to respond before proceeding
            artist_selection_window.wait_window()

            # Retrieve the selected artist
            chosen_artist = artist_selection_window.get_selected_option()

            if chosen_artist in matching_artists:
                self.log_and_show(f"User chose the suggested output directory: {chosen_artist}")
                return chosen_artist
            else:
                self.log_and_show("Invalid choice. Falling back to default location.")
                return None

        elif len(matching_artists) == 1:
            # If only one match found, return that
            artist_folder_path = matching_artists[0]
            return artist_folder_path

        else:
            # If no matching artist folder is found, return none
            self.log_and_show("Cannot suggest output directory. Falling back to default output directory.")
            return None

    except Exception as e:
        # Handle any unexpected exceptions and log an error message
        self.log_and_show(f"Unexpected error suggesting an output directory: {e}",
                          create_messagebox=True, error=True)
        return None


# Function to handle actions after successful input renaming
def handle_rename_success(self, new_path):
    # Store information about the rename operation in the history
    self.history.append({
        'original_path': self.file_renamer_selected_file,
        'new_path': new_path
    })

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

    # Check if the double check reminder variable is true
    if self.double_check_var.get():
        # Call the double check reminder function
        self.double_check_reminder(new_path)

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
                          create_messagebox=True, error=True)
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
                                  create_messagebox=True, error=True)
                weight = self.default_weight

            # Add the new category to the dictionary with the specified weight
            self.categories[new_category] = weight
            # Save the updated categories to the file
            self.update_json(self.dictionary_file, "categories", self.categories)
            # Refresh the category buttons in the GUI
            self.refresh_category_buttons()

            # Log the action if logging is enabled
            self.log_and_show(f"Category added: '{new_category}' with weight({weight})")
        else:
            # Log the action if logging is enabled
            self.log_and_show(f"'{new_category}' already exists. Skipping.",
                              create_messagebox=True, error=True)

    # Reset the category entries
    if self.reset_add_remove_var.get():
        # Clear the category entry and weight entry fields
        self.category_entry.delete(0, ctk.END)
        self.weight_entry.delete(0, ctk.END)


def remove_category(self):
    # Get the category to be removed from the remove category entry widget
    category_to_remove = self.remove_category_entry.get().strip()

    if not category_to_remove:
        # If the category to be removed is an empty string, log an error message and return
        self.log_and_show("Remove Category cannot be empty.", create_messagebox=True, error=True)
        return

    # Check for a case-sensitive match
    if category_to_remove in self.categories:
        # Remove the category from the dictionary
        del self.categories[category_to_remove]
        # Save the updated categories to the file
        self.update_json(self.dictionary_file, "categories", self.categories)
        # Refresh the category buttons in the GUI
        self.refresh_category_buttons()

        # Log the action if logging is enabled
        self.log_and_show(f"Category removed: {category_to_remove}")
    else:
        # Check for a case-insensitive match
        matching_category = next((key for key in self.categories if key.lower() == category_to_remove.lower()), None)
        if matching_category:
            # Remove the case-insensitive matched category from the dictionary
            del self.categories[matching_category]
            # Save the updated categories to the file
            self.update_json(self.dictionary_file, "categories", self.categories)
            # Refresh the category buttons in the GUI
            self.refresh_category_buttons()

            # Log the action if logging is enabled
            self.log_and_show(f"Category removed: {matching_category}")
        else:
            # Log the action if logging is enabled
            self.log_and_show(f"'{category_to_remove}' not found in dictionary. Skipping.",
                              create_messagebox=True, error=True)

    # Reset the category entries
    if self.reset_add_remove_var.get():
        # Clear the remove category entry field
        self.remove_category_entry.delete(0, ctk.END)


def create_category_button(self, tab, category):
    return ctk.CTkButton(tab, text=category, command=lambda c=category: self.add_to_queue(c))


def refresh_category_buttons(self):
    # Destroy existing tabs and buttons
    if hasattr(self, 'cat_tabview') and self.cat_tabview:
        self.cat_tabview.destroy()
    for button in getattr(self, 'buttons', []):
        button.destroy()

    # Load categories from the file or create an empty dictionary
    self.initialize_json()

    # Create the cat_tabview and buttons
    self.create_cat_tabview()


# Function to create the cat_tabview and buttons
def create_cat_tabview(self):
    # Create cat_tabview
    self.cat_tabview = ctk.CTkTabview(self.button_frame)
    self.cat_tabview.grid(row=0, column=0)

    # Create a tab for all categories
    all_cat_tab = self.cat_tabview.add("All")
    self.tabs["All"] = all_cat_tab  # Store the reference to the tab

    # Create a tab for "Most Categories" with weights 1-9
    most_cat_tab = self.cat_tabview.add("Most")
    self.tabs["Most"] = most_cat_tab  # Store the reference to the tab

    # Sort the weight tab_names
    if self.sort_tab_names_var.get():
        # Determine the order to sort (forward or backward)
        sort_reverse_order_var = True if self.sort_reverse_order_var.get() else False

        # Create a tab for each sorted weight
        weights = sorted(list(set(self.categories.values())), reverse=sort_reverse_order_var)
    else:
        # Create a tab for each weight
        weights = set(self.categories.values())

    for weight in weights:
        # Set either custom names or use the default weight naming scheme
        if self.use_custom_tab_names_var.get() and weight in self.weight_to_tab_name:
            tab_name = self.weight_to_tab_name[weight]
        else:
            tab_name = f"Weight {weight}"

        tab = self.cat_tabview.add(tab_name)

        self.tabs[weight] = tab  # Store the reference to the tab

        # Filter categories based on weight and sort case-insensitively
        weight_categories = sorted([category for category, w in self.categories.items() if w == weight],
                                   key=lambda x: x.lower())

        # Batch processing for button creation
        buttons = [self.create_category_button(tab, category) for category in weight_categories]

        for i, button in enumerate(buttons):
            button.grid(row=i // self.column_numbers, column=i % self.column_numbers, padx=5, pady=5)

        self.buttons = buttons

    # Create buttons for all categories in the "All Categories" tab
    all_categories = sorted(self.categories.keys(), key=lambda x: x.lower())
    all_buttons = [self.create_category_button(all_cat_tab, category) for category in all_categories]

    for i, button in enumerate(all_buttons):
        button.grid(row=i // self.column_numbers, column=i % self.column_numbers, padx=5, pady=5)

    self.all_buttons = all_buttons

    # Create buttons for categories with weights 1-default_most_number in the "Most Categories" tab
    most_categories = [category for category, w in self.categories.items() if 1 <= w <= self.default_most_number]
    # Sort the categories alphabetically and ignore case
    most_categories_sorted = sorted(most_categories, key=lambda x: x.lower())
    # Create buttons for the sorted categories
    most_buttons = [self.create_category_button(most_cat_tab, category) for category in most_categories_sorted]

    for i, button in enumerate(most_buttons):
        button.grid(row=i // self.column_numbers, column=i % self.column_numbers, padx=5, pady=5)

    self.most_buttons = most_buttons

    # Attempt to set the default tab
    try:
        # Check if self.default_tab is in the tab names
        if self.default_tab and self.cat_tabview.index(self.default_tab) is not None:
            self.cat_tabview.set(self.default_tab)
    except ValueError:
        return


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
                    confirmation = self.ask_confirmation("Suggest Output Directory",
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

            # Check if Artist Identifier is true
            if self.artist_identifier_var.get():
                # Use artist identifier to find other instances of artists
                identified = self.artist_identifier()

                if identified:
                    # Log the result and display a messagebox to the user
                    self.log_and_show(f"Artist Identifier: "
                                      f"\nFile name: "
                                      f"\n{os.path.basename(identified)} "
                                      f"\nFile path: "
                                      f"\n{identified}",
                                      create_messagebox=True)
                else:
                    # Log the action
                    self.log_and_show(f"No Artist Identifier result")

            # Rename the file
            os.rename(self.file_renamer_selected_file, new_path)
            self.log_and_show(f"File: '{os.path.basename(self.file_renamer_selected_file)}' renamed successfully. "
                              f"\nSaved to: \n{new_path}")
            self.handle_rename_success(new_path)

        except OSError as e:
            if "Invalid cross-device link" in str(e):
                # Attempt to use shutil.move if "Invalid cross-device link" error
                try:
                    shutil.move(self.file_renamer_selected_file, new_path)
                    self.log_and_show(
                        f"File: '{os.path.basename(self.file_renamer_selected_file)}' renamed and moved successfully. "
                        f"\nSaved to: \n{new_path}")
                    self.handle_rename_success(new_path)
                except Exception as move_error:
                    # Log the action if shutil.move also fails
                    self.log_and_show(f"Renaming and moving file failed: {str(move_error)}",
                                      create_messagebox=True, error=True)
            else:
                # Log the action for other OSError
                self.log_and_show(f"{str(e)}", create_messagebox=True, error=True)

    # If an input is selected and either the queue is empty or no custom text is provided show error
    elif self.file_renamer_selected_file and not (self.queue or self.custom_text_entry.get().strip()):
        # Log the action if logging is enabled
        self.log_and_show("Input selected but nothing added to the queue. Nothing to rename.",
                          create_messagebox=True, error=True)
    # If no input is selected, show error
    elif not self.file_renamer_selected_file:
        # Log the action if logging is enabled
        self.log_and_show("No input selected. Nothing to rename.", create_messagebox=True, error=True)


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
                self.log_and_show(f"{str(e)}", create_messagebox=True, error=True)
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
        # No dash found, return the original filename
        return file_name

    # Sanitize file name. Remove double spaces.
    new_file_name = ' '.join(new_file_name.split()).strip()

    # Check for double dashes and remove the second dash
    if ' - - ' in new_file_name:
        new_file_name = new_file_name.replace(' - - ', ' - ', 1)

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
        # Remove custom text
        try:
            # Get the text to remove from the entry
            text_to_remove = self.custom_text_removal_entry.get().strip()
        except Exception as e:
            self.log_and_show(f"An error occurred getting the custom text to remove: {str(e)}",
                              create_messagebox=True,
                              error=True)
            text_to_remove = None

        # Check if text to remove is provided
        if text_to_remove:
            if self.replace_mode_var.get():
                # Check if the text to remove is present in name (case-insensitive)
                pattern = re.compile(re.escape(text_to_remove), re.IGNORECASE)

                # Remove all instances of the text to remove from name
                name = pattern.sub('', name)
            else:
                # Check if the text to remove is present in name (case-sensitive)
                if text_to_remove in name:
                    # Remove all instances of the text to remove from name
                    name = name.replace(text_to_remove, '')

        if self.remove_custom_text_var.get():
            # Remove custom text from the custom_text_to_remove list
            if self.replace_mode_var.get():
                for text_to_remove in self.custom_text_to_remove:
                    # Check if the text to remove is present in name (case-insensitive)
                    pattern = re.compile(re.escape(text_to_remove), re.IGNORECASE)

                    # Remove all instances of the text to remove from name
                    name = pattern.sub('', name)
            else:
                # Check if the text to remove is present in name (case-sensitive)
                for text_to_remove in self.custom_text_to_remove:
                    # Remove all instances of the text to remove from name
                    name = name.replace(text_to_remove, '')

        if self.remove_custom_text_var.get() or text_to_remove:
            # Replace consecutive spaces with a single space when custom text is removed
            name = re.sub(r'\s+', ' ', name)

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
                    name = self.remove_artist_duplicates_from_filename(name)
            except FileNotFoundError:
                self.log_and_show(f"File not found: {self.artist_file}", create_messagebox=True, error=True)
            except Exception as e:
                self.log_and_show(f"Artist search failed {self.artist_file}: {e}", create_messagebox=True, error=True)

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
                    self.log_and_show(f"Moving failed for {os.path.basename(new_path)}: {e}", error=True)

            # Return a tuple with file path and name normalizer last used file
            return file_path, self.name_normalizer_last_used_file

        except OSError as e:
            # Log an error if renaming fails
            self.log_and_show(f"Renaming failed for {os.path.basename(file_path)}: {e}", error=True)
            # Return a tuple with file path and file path if error
            return file_path, file_path
    else:
        # Return a tuple with file path and file path if no result
        return file_path, file_path


# Function to performing various name normalization operations on certain files within a specified folder
def process_name_normalizer(self, mode):
    # Check if the specified input exists
    if (not os.path.exists(self.name_normalizer_selected_file)
            and not os.path.isfile(self.name_normalizer_selected_file)):
        self.log_and_show("Path does not exist or was not specified.\nPlease try again.",
                          create_messagebox=True, error=True)
        return

    # Check if name_normalizer_output_directory is specified and exists
    if self.name_normalizer_output_directory and not os.path.exists(self.name_normalizer_output_directory):
        self.log_and_show("Output directory does not exist or was not specified.\nPlease try again.",
                          create_messagebox=True, error=True)
        return

    # Check if artist file search is enabled
    if self.artist_file_search_var.get():
        # Check if artist file is not provided
        if not self.artist_file:
            # Log and display an error message
            self.log_and_show("No artist file provided. Please provide one and try again, or turn off Artist Search.",
                              create_messagebox=True, error=True)
            return
        # Check if artist file does not exist
        elif not os.path.exists(self.artist_file):
            # Log and display an error message
            self.log_and_show(f"The artist file does not exist: '{self.artist_file}'"
                              f"\nPlease ensure the provided Artist File exists, "
                              f"\nor turn off Artist Search to proceed.\nSee FAQ",
                              create_messagebox=True, error=True)
            return

    if mode == "preview":
        preview_result = self.preview_name(self.name_normalizer_selected_file)
        if preview_result:
            self.log_and_show(f"Preview: \n{os.path.basename(preview_result)}", create_messagebox=True)
        return
    elif mode == "action":
        # Ask for confirmation before normalizing files
        confirmation = self.ask_confirmation("Confirm Action",
                                             "Are you sure you want normalize the file(s)? You may not be able "
                                             "to undo this operation.")
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
            original_path, new_path = self.rename_and_move_file(self.name_normalizer_selected_file)

            # Check if the tuple is the same to prevent no operations from being added to history
            if original_path != new_path:
                # Append the operation to the history
                self.nn_history.append({
                    'original_paths': [original_path],
                    'new_paths': [new_path]
                })
        else:
            # Get folder contents and save to memory

            # Initialize an empty list to store file paths
            file_paths = []
            original_paths = []
            new_paths = []

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
                        original_path, new_path = self.rename_and_move_file(file_path)
                        # Check if the tuple is the same to prevent no operations from being added to history
                        if original_path != new_path:
                            original_paths.append(original_path)
                            new_paths.append(new_path)

                    # Append the batch operation to the name normalizer history
                    self.nn_history.append({
                        'original_paths': original_paths,
                        'new_paths': new_paths
                    })

        # Log the action if logging is enabled
        self.log_and_show("File(s) have been processed successfully.")

        # Reset GUI input fields if reset is True
        if self.reset_var.get():
            # Clear selection for the name_normalizer_window
            self.clear_selection(frame_name="name_normalizer_window")

    except Exception as e:
        # Display error message if an exception occurs
        self.log_and_show(f"An error occurred: {e}", create_messagebox=True, error=True)


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
        self.log_and_show(f"Getting non-conflicting file name failed: {str(e)}", create_messagebox=True, error=True)

        # Return None in case of an error.
        return None


# Function to remove a successful line from a file.
def remove_successful_line_from_file(self, file_path, line_to_remove):
    try:
        if not file_path.lower().endswith('.txt'):
            # If the file does not have a .txt extension, return without performing any operation.
            self.log_and_show("The provided file is not a txt file.", error=True)
            return

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
        self.log_and_show(f"An error occurred while removing line from file: {e}", create_messagebox=True, error=True)


# Method to rotate/mirror a video clip by a specified angle.
def rotate_video(self, clip, rotation_angle):
    try:
        if rotation_angle == "mirror":
            # Mirror the video clip along the horizontal axis.
            # noinspection PyUnresolvedReferences
            rotated_clip = clip.fx(vfx.mirror_x)

        else:
            # Rotate the video clip by the specified angle.
            rotated_clip = clip.rotate(rotation_angle)

        # Log rotation success if logging is activated.
        self.log_and_show(f"Rotation successful {rotation_angle}")

        # Return the rotated video clip.
        return rotated_clip

    except Exception as e:
        # Log error and display an error message if rotation fails.
        self.log_and_show(f"Rotating video failed: {str(e)}", create_messagebox=True, error=True)

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
        self.log_and_show(f"Increasing volume failed: {str(e)}", create_messagebox=True, error=True)

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
        self.log_and_show(f"Normalizing audio failed: {str(e)}", create_messagebox=True, error=True)

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
        self.log_and_show(f"Trimming failed: {str(e)}", create_messagebox=True, error=True)

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
        self.log_and_show(f"Value error: Please enter a valid value (integer or float) into the entry field. {str(e)}",
                          create_messagebox=True, error=True)
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

    # Check if rotation is 0.0 and set variable to None
    if audio_normalization == 0.0:
        audio_normalization = None

    # Check if an input source is provided
    if not self.video_editor_selected_file:
        self.log_and_show("Input must be specified (video file, line separated txt, or directory.",
                          create_messagebox=True, error=True)
        return

    # Check if the provided input exists
    if self.video_editor_selected_file and not os.path.exists(self.video_editor_selected_file):
        self.log_and_show("The input does not exist or cannot be found. Please try again.",
                          create_messagebox=True, error=True)
        return

    # Check if the necessary parameters for video editing are provided
    if (self.video_editor_selected_file and decibel is None and rotation is None and audio_normalization is None
            and minutes is None and seconds is None):
        self.log_and_show("You need to specify an operation (audio increase, video rotation, "
                          "audio normalization, trim, or some combination of them)",
                          create_messagebox=True, error=True)
        return

    # Check if the provided output directory exists
    if self.video_editor_output_directory and not os.path.exists(self.video_editor_output_directory):
        self.log_and_show("The output directory does not exist or cannot be found. Please try again.",
                          create_messagebox=True, error=True)
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
            confirmation = self.ask_confirmation("Confirm Action",
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
        self.log_and_show(f"Processing input failed: {str(e)}", create_messagebox=True, error=True)
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
                    rotation_angle = 180
                elif rotation == "mirror":
                    rotation_angle = "mirror"

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
                processed_clip = self.rotate_video(original_clip, rotation_angle)
                if processed_clip:
                    original_clip = processed_clip
                else:
                    successful_operations = False

            if decibel and successful_operations:
                processed_clip = self.increase_volume(original_clip, decibel)
                if processed_clip:
                    original_clip = processed_clip
                else:
                    successful_operations = False

            if audio_normalization and successful_operations:
                processed_clip = self.normalize_audio(original_clip, audio_normalization)
                if processed_clip:
                    original_clip = processed_clip
                else:
                    successful_operations = False

            if trim and successful_operations:
                processed_clip = self.trim_video(original_clip, total_time)
                if processed_clip:
                    original_clip = processed_clip
                else:
                    successful_operations = False

            # Write the final modified clip to the output path if all operations were successful
            if successful_operations:
                original_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

                # Set the video editor last used file upon success
                self.video_editor_last_used_file = output_path

                if self.reset_video_entries_var.get():
                    # Clear selection for the video_editor_window
                    self.clear_selection(frame_name="video_editor_window")

                # Remove the successfully processed line from the input file
                if self.video_editor_selected_file:
                    self.remove_successful_line_from_file(self.video_editor_selected_file, input_path)

                # Log the action if logging is enabled
                self.log_and_show(f"Video saved as {os.path.basename(output_path)}"
                                  f"\nPath: {output_path}")
            else:
                self.log_and_show(f"Operations failed for video {os.path.basename(input_path)}",
                                  create_messagebox=True, error=True)

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
                              create_messagebox=True, error=True)
            continue


"""
add_remove_window
"""


# Function to add artists to the artist file
def add_artist_to_file(self):
    # Get the artist to be added from the entry widget
    add_artist = self.add_artist_entry.get().strip()

    # Check if no artist is provided
    if not add_artist:
        self.log_and_show("Add Artist cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no artist is provided

    # Read the list of artists from the artist_file
    try:
        with open(self.artist_file, 'r') as artist_list_file:
            artist_list = [artist.strip() for artist in artist_list_file]
    except FileNotFoundError:
        self.log_and_show(f"Artist File '{self.artist_file}' not found.", create_messagebox=True, error=True)
        return  # Exit the function if the artist_file is not found

    # Check if the add_artist is already in the list (case-insensitive)
    if any(artist.lower() == add_artist.lower() for artist in artist_list):
        self.log_and_show(f"Artist is already in the Artist File: '{add_artist}'",
                          create_messagebox=True, error=True)
    else:
        # Add the add_artist to the list
        artist_list.append(add_artist)

        # Write the updated list back to the artist_file
        try:
            with open(self.artist_file, 'w') as artist_list_file:
                artist_list_file.write('\n'.join(artist_list))

            # Log the message and display to the gui
            self.log_and_show(f"Added artist to the Artist File: '{add_artist}'")

        except IOError:
            self.log_and_show(f"Writing to Artist File failed: '{self.artist_file}'.",
                              create_messagebox=True, error=True)

    # Reset the artist entries if the action is successful
    if self.reset_add_remove_var.get():
        # Clear add artist entry
        self.add_artist_entry.delete(0, ctk.END)


# Function to remove artists from the artist file
def remove_artist_from_file(self):
    # Get the artist to be removed from the entry widget
    remove_artist = self.remove_artist_entry.get().strip()

    # Check if no artist is provided
    if not remove_artist:
        self.log_and_show("Remove Artist cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no artist is provided

    try:
        # Read the list of artists from the artist_file
        with open(self.artist_file, 'r') as artist_list_file:
            artist_list = [artist.strip() for artist in artist_list_file]
    except FileNotFoundError:
        self.log_and_show(f"Artist File '{self.artist_file}' not found.", create_messagebox=True, error=True)
        return  # Exit the function if the artist_file is not found

    # Check if the remove_artist is in the list (case-insensitive)
    if any(artist.lower() == remove_artist.lower() for artist in artist_list):
        # Remove the remove_artist from the list
        artist_list = [artist for artist in artist_list if artist.lower() != remove_artist.lower()]

        # Write the updated list back to the artist_file
        try:
            with open(self.artist_file, 'w') as artist_list_file:
                artist_list_file.write('\n'.join(artist_list))
            self.log_and_show(f"Removed artist from the Artist File: '{remove_artist}'")

        except IOError:
            self.log_and_show(f"Writing to Artist File failed: '{self.artist_file}'.",
                              create_messagebox=True, error=True)
    else:
        self.log_and_show(f"Artist is not in the Artist File: '{remove_artist}'",
                          create_messagebox=True, error=True)

    # Reset the artist entries
    if self.reset_add_remove_var.get():
        # Clear remove artist entry
        self.remove_artist_entry.delete(0, ctk.END)


# Function to create a NO-GO file
def no_go_creation(self):
    # Attempt to get the contents from self.add_no_go_name_entry
    no_go_name = self.add_no_go_name_entry.get().strip()

    # Check if no_go_name is provided
    if not no_go_name:
        self.log_and_show("Add NO GO cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no artist is provided

    try:
        # Expand the user's home directory in the NO-GO path
        no_go_directory = os.path.expanduser(self.no_go_directory)

        # Ensure the NO-GO directory exists, create it if not
        if not os.path.exists(no_go_directory):
            os.makedirs(no_go_directory)

        # Create a file for the NO-GO
        file_name = f"NO GO - {no_go_name}"
        file_path = os.path.join(no_go_directory, file_name)

        # Check if the file already exists case-insensitively to prevent overwriting
        if any(filename.lower() == file_name.lower() for filename in os.listdir(no_go_directory)):
            # Log the action and display a message
            self.log_and_show(f"'{file_name}' already exists. Skipping creation.", create_messagebox=True, error=True)

            # Reset the no-go entries if the action is successful
            if self.reset_add_remove_var.get():
                # Clear add no-go name entry and reset
                self.add_no_go_name_entry.delete(0, ctk.END)
            return

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
            file.write("\n" + no_go_name)

        # Log the action if logging is enabled
        self.log_and_show(f"NO GO created successfully for '{no_go_name}' in \n"
                          f"{no_go_directory}")

    except Exception as e:
        self.log_and_show(f"Creating NO GO failed: '{str(e)}'.", create_messagebox=True, error=True)

    # Reset the no-go entries if the action is successful
    if self.reset_add_remove_var.get():
        # Clear add no-go name entry and reset
        self.add_no_go_name_entry.delete(0, ctk.END)


def no_go_removal(self):
    # Attempt to get the contents from self.remove_no_go_name_entry
    remove_no_go_name = self.remove_no_go_name_entry.get().strip()

    # Check if remove_no_go_name is provided
    if not remove_no_go_name:
        self.log_and_show("Remove NO GO cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no artist is provided

    try:
        # Expand the user's home directory in the NO-GO path
        no_go_directory = os.path.expanduser(self.no_go_directory)

        # Ensure the NO-GO directory exists
        if not os.path.exists(no_go_directory):
            self.log_and_show("NO GO directory does not exist.", create_messagebox=True, error=True)
            return  # Exit the function if NO GO directory does not exist

        # Check if the NO-GO file exists 
        # TODO Compare case-insensitively
        no_go_file_name = f"NO GO - {remove_no_go_name}"
        no_go_file_path = os.path.join(no_go_directory, no_go_file_name)
        if os.path.isfile(no_go_file_path):
            os.remove(no_go_file_path)
            self.log_and_show(f"NO GO file '{no_go_file_name}' removed successfully.")
        else:
            self.log_and_show(f"NO GO file '{no_go_file_name}' not found.", create_messagebox=True, error=True)

        # Check and remove the entry from self.no_go_artist_file tampermonkey (case-insensitive)
        with open(self.no_go_artist_file, "r") as file:
            lines = file.readlines()

        with open(self.no_go_artist_file, "w") as file:
            for line in lines:
                if line.strip().lower() != remove_no_go_name.lower():
                    file.write(line)

        self.log_and_show(f"NO GO entry '{remove_no_go_name}' removed from {self.no_go_artist_file} successfully.")

    except Exception as e:
        self.log_and_show(f"Removing NO GO failed: '{str(e)}'.", create_messagebox=True, error=True)

    # Reset the no-go entries if the action is successful
    if self.reset_add_remove_var.get():
        # Clear remove no-go name entry and reset
        self.remove_no_go_name_entry.delete(0, ctk.END)


# Function to exclude folder from Artist Directory search
def add_folder_to_excluded_folders(self):
    # Get the exclude name to be added from the entry widget
    exclude_name = self.add_exclude_name_entry.get().strip()

    # Check if no exclude name is provided
    if not exclude_name:
        self.log_and_show("Add Exclude cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no exclude_name is provided

    # Convert both the input exclude name and existing excluded folders to lowercase
    exclude_name_lower = exclude_name.lower()
    excluded_folders_lower = [folder.lower() for folder in self.excluded_folders]

    # Check if the exclude_name is already in the excluded_folders list (case-insensitive)
    if exclude_name_lower in excluded_folders_lower:
        self.log_and_show(f"Folder '{exclude_name}' is already in the excluded folders list.",
                          create_messagebox=True, error=True)

        # Reset the exclude entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the exclude entry
            self.add_exclude_name_entry.delete(0, ctk.END)

        return  # Exit the function if the exclude_name is already in the list

    try:
        # Add the exclude_name to the excluded_folders list
        self.excluded_folders.append(exclude_name)

        # Update the JSON file with the new excluded_folders list
        self.update_json(self.dictionary_file, "excluded_folders", self.excluded_folders)

        # Log and show success message
        self.log_and_show(f"Folder '{exclude_name}' added to excluded folders list.")

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Adding folder '{exclude_name}' to excluded folders list failed: {str(e)}",
                          create_messagebox=True, error=True)

    # Reset the exclude entry if the action is successful
    if self.reset_add_remove_var.get():
        # Reset the exclude entry
        self.add_exclude_name_entry.delete(0, ctk.END)


# Function to include folder in Artist Directory search
def remove_folder_from_excluded_folders(self):
    # Get the exclude name to be removed from the entry widget
    exclude_name = self.remove_exclude_name_entry.get().strip()

    # Check if no exclude name is provided
    if not exclude_name:
        self.log_and_show("Remove Exclude cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no exclude_name is provided

    # Convert both the input exclude name and existing excluded folders to lowercase
    exclude_name_lower = exclude_name.lower()
    excluded_folders_lower = [folder.lower() for folder in self.excluded_folders]

    # Check if the exclude_name is in the excluded_folders list (case-insensitive)
    if exclude_name_lower not in excluded_folders_lower:
        self.log_and_show(f"Folder '{exclude_name}' is not in the excluded folders list.",
                          create_messagebox=True, error=True)

        # Reset the exclude entry if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the remove entry
            self.remove_exclude_name_entry.delete(0, ctk.END)

        return  # Exit the function if the exclude_name is not in the list

    try:
        # Remove the folder from the excluded_folders list (case-insensitive)
        self.excluded_folders = [folder for folder in self.excluded_folders if folder.lower() != exclude_name_lower]

        # Update the JSON file with the new excluded_folders list
        self.update_json(self.dictionary_file, "excluded_folders", self.excluded_folders)

        # Log and show success message
        self.log_and_show(f"Folder '{exclude_name}' removed from excluded folders list.")

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Removing folder '{exclude_name}' from excluded folders list failed: {str(e)}",
                          create_messagebox=True, error=True)

    # Reset the exclude entries if the action is successful
    if self.reset_add_remove_var.get():

        # Reset the remove entry if the action is successful
        self.remove_exclude_name_entry.delete(0, ctk.END)


# Function to add text to custom_text_to_remove list
def add_custom_text_to_remove(self):
    # Get the custom text to be added from the entry widget
    custom_text = self.add_ctr_name_entry.get().strip()

    # Check if no custom text is provided
    if not custom_text:
        self.log_and_show("Add CTR cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no custom_text is provided

    # Convert both the input custom text and existing custom texts to lowercase
    custom_text_lower = custom_text.lower()
    custom_texts_lower = [text.lower() for text in self.custom_text_to_remove]

    # Check if the custom_text is already in the custom_text_to_remove list (case-insensitive)
    if custom_text_lower in custom_texts_lower:
        self.log_and_show(f"Custom Text '{custom_text}' is already in the custom text to remove list.",
                          create_messagebox=True, error=True)

        # Reset the custom text entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the add custom text to remove entry
            self.add_ctr_name_entry.delete(0, ctk.END)

        return  # Exit the function if the custom_text is already in the list

    try:
        # Add the custom_text to the custom_text_to_remove list
        self.custom_text_to_remove.append(custom_text)

        # Update the JSON file with the new custom_text_to_remove list
        self.update_json(self.dictionary_file, "custom_text_to_remove", self.custom_text_to_remove)

        # Log and show success message
        self.log_and_show(f"Custom Text '{custom_text}' added to custom text to remove list.")

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Adding Custom Text '{custom_text}' to custom text to remove list failed: {str(e)}",
                          create_messagebox=True, error=True)

    # Reset the custom text entries if the action is successful
    if self.reset_add_remove_var.get():
        # Reset the custom text to remove entry if the action is successful
        self.add_ctr_name_entry.delete(0, ctk.END)


# Function to remove text from custom_text_to_remove list
def remove_custom_text_to_remove(self):
    # Get the custom text to be removed from the entry widget
    custom_text = self.remove_ctr_name_entry.get().strip()

    # Check if no custom text is provided
    if not custom_text:
        self.log_and_show("Remove CTR cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no custom_text is provided

    # Convert both the input custom text and existing custom texts to lowercase
    custom_text_lower = custom_text.lower()
    custom_texts_lower = [text.lower() for text in self.custom_text_to_remove]

    # Check if the custom_text is in the custom_text_to_remove list (case-insensitive)
    if custom_text_lower not in custom_texts_lower:
        self.log_and_show(f"Custom Text '{custom_text}' is not in the custom text to remove list.",
                          create_messagebox=True, error=True)

        # Reset the custom text entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the remove custom_text_to_remove entry
            self.remove_ctr_name_entry.delete(0, ctk.END)

        return  # Exit the function if the custom_text is not in the list

    try:
        # Remove the custom_text from the custom_text_to_remove list (case-insensitive)
        self.custom_text_to_remove = [text for text in self.custom_text_to_remove if
                                      text.lower() != custom_text_lower]

        # Update the JSON file with the new custom_text_to_remove list
        self.update_json(self.dictionary_file, "custom_text_to_remove", self.custom_text_to_remove)

        # Log and show success message
        self.log_and_show(f"Custom Text '{custom_text}' removed from custom text to remove list.")

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Removing Custom Text '{custom_text}' from custom text to remove list failed: {str(e)}",
                          create_messagebox=True, error=True)

    # Reset the custom text entries if the action is successful
    if self.reset_add_remove_var.get():
        # Reset the remove custom_text_to_remove entry if the action is successful
        self.remove_ctr_name_entry.delete(0, ctk.END)


# Function to add extension to file_extensions list
def add_file_extension(self):
    # Get the extension to be added from the entry widget
    file_extension = self.add_file_extension_entry.get().strip()

    # Check if no extension is provided
    if not file_extension:
        self.log_and_show("Add File Ext. cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no file_extension is provided

    # Check if the extension starts with a period; if not, add one
    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    # Convert both the input file extension and existing file extensions to lowercase
    file_extension_lower = file_extension.lower()
    file_extensions_lower = [ext.lower() for ext in self.file_extensions]

    # Check if the extension is already in the file_extensions list (case-insensitive)
    if file_extension_lower in file_extensions_lower:
        self.log_and_show(f"File Extension '{file_extension}' is already in the file extensions list.",
                          create_messagebox=True, error=True)

        # Reset the file extension entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the add extension to remove entry
            self.add_file_extension_entry.delete(0, ctk.END)

        return  # Exit the function if the file_extension is already in the list

    try:
        # Add the extension to the file_extensions list
        self.file_extensions.append(file_extension)

        # Update the JSON file with the new file_extensions list
        self.update_json(self.dictionary_file, "file_extensions", self.file_extensions)

        # Log and show success message
        self.log_and_show(f"File Extension '{file_extension}' added to file extensions list.")

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Adding File Extension '{file_extension}' to file extensions list failed: {str(e)}",
                          create_messagebox=True, error=True)

    # Reset the file extension entries if the action is successful
    if self.reset_add_remove_var.get():
        # Reset the file extensions entry if the action is successful
        self.add_file_extension_entry.delete(0, ctk.END)


# Function to remove extension from file_extensions list
def remove_file_extension(self):
    # Get the extension to be removed from the entry widget
    file_extension = self.remove_file_extension_entry.get().strip()

    # Check if no extension is provided
    if not file_extension:
        self.log_and_show("Remove File Ext. cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no file_extension is provided

    # Check if the extension starts with a period; if not, add one
    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    # Convert both the input file extension and existing file extensions to lowercase
    file_extension_lower = file_extension.lower()
    file_extensions_lower = [ext.lower() for ext in self.file_extensions]

    # Check if the file_extension is in the file_extensions list (case-insensitive)
    if file_extension_lower not in file_extensions_lower:
        self.log_and_show(f"File Extension '{file_extension}' is not in the file extensions list.",
                          create_messagebox=True, error=True)

        # Reset the file extension entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the remove file_extensions entry
            self.remove_file_extension_entry.delete(0, ctk.END)

        return  # Exit the function if the file_extension is not in the list

    try:
        # Remove the file_extension from the file_extensions list (case-insensitive)
        self.file_extensions = [ext for ext in self.file_extensions if
                                ext.lower() != file_extension_lower]

        # Update the JSON file with the new file_extensions list
        self.update_json(self.dictionary_file, "file_extensions", self.file_extensions)

        # Log and show success message
        self.log_and_show(f"File Extension '{file_extension}' removed from file extensions list.")

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Removing File Extension '{file_extension}' from file extensions list failed: {str(e)}",
                          create_messagebox=True, error=True)

    # Reset the file extension entries if the action is successful
    if self.reset_add_remove_var.get():
        # Reset the remove file_extensions entry if the action is successful
        self.remove_file_extension_entry.delete(0, ctk.END)


# Function to add extension to valid_extensions list
def add_valid_extension(self):
    # Get the extension to be added from the entry widget
    valid_extension = self.add_valid_extension_entry.get().strip()

    # Check if no extension is provided
    if not valid_extension:
        self.log_and_show("Add Valid Ext. cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no valid_extension is provided

    # Check if the extension starts with a period; if not, add one
    if not valid_extension.startswith('.'):
        valid_extension = '.' + valid_extension

    # Convert both the input valid extension and existing valid extensions to lowercase
    valid_extension_lower = valid_extension.lower()
    valid_extensions_lower = [ext.lower() for ext in self.valid_extensions]

    # Check if the extension is already in the valid_extensions list (case-insensitive)
    if valid_extension_lower in valid_extensions_lower:
        self.log_and_show(f"File Extension '{valid_extension}' is already in the valid extensions list.",
                          create_messagebox=True, error=True)

        # Reset the valid extension entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the add extension to remove entry
            self.add_valid_extension_entry.delete(0, ctk.END)

        return  # Exit the function if the valid_extension is already in the list

    try:
        # Add the extension to the valid_extensions list
        self.valid_extensions.append(valid_extension)

        # Update the JSON file with the new valid_extensions list
        self.update_json(self.dictionary_file, "valid_extensions", self.valid_extensions)

        # Log and show success message
        self.log_and_show(f"File Extension '{valid_extension}' added to valid extensions list.")

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Adding File Extension '{valid_extension}' to valid extensions list failed: {str(e)}",
                          create_messagebox=True, error=True)

    # Reset the valid extension entries if the action is successful
    if self.reset_add_remove_var.get():
        # Reset the valid extensions entry if the action is successful
        self.add_valid_extension_entry.delete(0, ctk.END)


# Function to remove extension from valid_extensions list
def remove_valid_extension(self):
    # Get the extension to be removed from the entry widget
    valid_extension = self.remove_valid_extension_entry.get().strip()

    # Check if no extension is provided
    if not valid_extension:
        self.log_and_show("Remove Valid Ext. cannot be empty.", create_messagebox=True, error=True)
        return  # Exit the function if no valid_extension is provided

    # Check if the extension starts with a period; if not, add one
    if not valid_extension.startswith('.'):
        valid_extension = '.' + valid_extension

    # Convert both the input valid extension and existing valid extensions to lowercase
    valid_extension_lower = valid_extension.lower()
    valid_extensions_lower = [ext.lower() for ext in self.valid_extensions]

    # Check if the valid_extension is in the valid_extensions list (case-insensitive)
    if valid_extension_lower not in valid_extensions_lower:
        self.log_and_show(f"File Extension '{valid_extension}' is not in the valid extensions list.",
                          create_messagebox=True, error=True)

        # Reset the valid extension entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the remove valid_extensions entry
            self.remove_valid_extension_entry.delete(0, ctk.END)

        return  # Exit the function if the valid_extension is not in the list

    try:
        # Remove the valid_extension from the valid_extensions list (case-insensitive)
        self.valid_extensions = [ext for ext in self.valid_extensions if
                                 ext.lower() != valid_extension_lower]

        # Update the JSON file with the new valid_extensions list
        self.update_json(self.dictionary_file, "valid_extensions", self.valid_extensions)

        # Log and show success message
        self.log_and_show(f"File Extension '{valid_extension}' removed from valid extensions list.")

    except Exception as e:
        # Log and show error message if an exception occurs
        self.log_and_show(f"Removing File Extension '{valid_extension}' from valid extensions list failed: {str(e)}",
                          create_messagebox=True, error=True)

    # Reset the valid extension entries if the action is successful
    if self.reset_add_remove_var.get():
        # Reset the remove valid_extensions entry if the action is successful
        self.remove_valid_extension_entry.delete(0, ctk.END)


# Function to add a custom tab name to the dictionary
def add_custom_tab_name(self):
    # Get the new custom tab name from the add custom tab name entry widget
    new_custom_tab_name = self.custom_tab_name_entry.get().strip()

    if not new_custom_tab_name:
        # If the new custom tab name is an empty string, log an error message and return
        self.log_and_show("New Custom Tab cannot be empty.",
                          create_messagebox=True, error=True)
        return

    if new_custom_tab_name:
        # Convert to lowercase for case-insensitive check
        new_custom_tab_name_lower = new_custom_tab_name.lower()
        # Prevent duplicate entries in the json file
        if new_custom_tab_name_lower not in map(lambda x: x.lower(), self.weight_to_tab_name.values()):
            # Get the weight from the GUI entry field
            weight_entry_value = self.weight_entry1.get().strip()

            try:
                # Use the provided weight if it's an integer, otherwise use the default custom tab name weight
                weight = int(weight_entry_value) if weight_entry_value else self.default_ctn_weight
            except ValueError:
                self.log_and_show("Weight must be an integer. Using default weight.",
                                  create_messagebox=True, error=True)
                weight = self.default_ctn_weight

            # Add the new custom tab name to the dictionary under the specified weight
            self.weight_to_tab_name[weight] = new_custom_tab_name
            # Save the updated custom tab names to the file
            self.update_json(self.dictionary_file, "weight_to_tab_name", self.weight_to_tab_name)
            # Refresh the category buttons in the GUI
            self.refresh_category_buttons()

            # Log the action if logging is enabled
            self.log_and_show(f"Custom Tab Name added: '{new_custom_tab_name}' for weight({weight})")
        else:
            # Log the action if logging is enabled
            self.log_and_show(f"'{new_custom_tab_name}' already exists. Skipping.",
                              create_messagebox=True, error=True)

        # Reset the custom tab name entries if the action is successful
        if self.reset_add_remove_var.get():
            # Clear the custom_tab_name entry and weight entry fields
            self.custom_tab_name_entry.delete(0, ctk.END)
            self.weight_entry1.delete(0, ctk.END)


# Remove a  custom tab name to the dictionary
def remove_custom_tab_name(self):
    # Get the custom tab name to be removed from the remove custom tab name entry widget
    ctn_to_remove = self.remove_custom_tab_name_entry.get().strip()

    if not ctn_to_remove:
        # If the custom tab name to be removed is an empty string, log an error message and return
        self.log_and_show("Remove Custom Tab cannot be empty.", create_messagebox=True, error=True)
        return

    # Check for a case-sensitive match in values
    if ctn_to_remove in self.weight_to_tab_name.values():
        # Remove the custom tab name from the dictionary
        keys_to_remove = [key for key, value in self.weight_to_tab_name.items() if value == ctn_to_remove]
        for key in keys_to_remove:
            del self.weight_to_tab_name[key]

        # Save the updated custom tab names to the file
        self.update_json(self.dictionary_file, "weight_to_tab_name", self.weight_to_tab_name)
        # Refresh the category buttons in the GUI
        self.refresh_category_buttons()

        # Log the action if logging is enabled
        self.log_and_show(f"Custom Tab Name removed: {ctn_to_remove}")
    else:
        # Check for a case-insensitive match for a custom tab name in values
        matching_ctn = next(
            (key for key, value in self.weight_to_tab_name.items() if value.lower() == ctn_to_remove.lower()), None)
        if matching_ctn:
            # Remove the case-insensitive matched custom tab name from the dictionary
            del self.weight_to_tab_name[matching_ctn]
            # Save the updated custom tab names to the file
            self.update_json(self.dictionary_file, "weight_to_tab_name", self.weight_to_tab_name)
            # Refresh the category buttons in the GUI
            self.refresh_category_buttons()

            # Log the action if logging is enabled
            self.log_and_show(f"Custom Tab Name removed: {matching_ctn}")
        else:
            # Log the action if logging is enabled
            self.log_and_show(f"'{ctn_to_remove}' not found in dictionary. Skipping.",
                              create_messagebox=True, error=True)

    # Reset the custom tab name entries if the action is successful
    if self.reset_add_remove_var.get():
        # Clear the remove custom tab name entry field
        self.remove_custom_tab_name_entry.delete(0, ctk.END)


# Function to refresh the add/remove tabview
def refresh_add_remove_tabview(self):
    # Destroy existing tabs
    if hasattr(self, 'add_remove_tabview') and self.add_remove_tabview:
        self.add_remove_tabview.destroy()

    # Create the add_remove_tabview
    self.create_add_remove_tabview()


# Function to create add/remove tabview
def create_add_remove_tabview(self):
    # Create add_remove_tabview
    self.add_remove_tabview = ctk.CTkTabview(self.add_remove_frame)
    self.add_remove_tabview.grid(row=1, column=0)

    # Sort the add/remove tab_names
    if self.sort_tab_names_var.get():
        # Determine the order to sort (forward or backward)
        sort_reverse_order_var = True if self.sort_reverse_order_var.get() else False

        # Create a tab for each sorted tab_name
        tab_names = sorted(list(set(self.tab_names)), reverse=sort_reverse_order_var)
    else:
        # Create a tab for each tab_name
        tab_names = list(set(self.tab_names))

    for tab_name in tab_names:
        # Use the tab_name naming scheme
        tab_name = f"{tab_name}"

        # Create the tab
        tab = self.add_remove_tabview.add(tab_name)

        # Store the reference to the tab
        self.tabs[tab_name] = tab

    # Set the default tab
    self.add_remove_tabview.set(self.default_add_remove_tab)


# Function to attempt to identify Artists
def artist_identifier(self):
    # Check if an input is selected
    if not self.file_renamer_selected_file:
        # If no input is selected, return none
        self.log_and_show("No input selected.")
        return None

    # Check if the artist_identifier_var is True
    if not self.artist_identifier_var.get():
        # If artist_identifier_var is False, return none
        self.log_and_show("Artist Identifier disabled.")
        return None

    # Check if self.artist_directory exists
    if not os.path.exists(self.artist_directory):
        # If artist directory does not exist, display an error message and return none
        self.log_and_show(f"Artist Identifier cannot function as intended since the Artist Directory"
                          f" does not exist."
                          f"\nPlease ensure Artist Directory: '{self.artist_directory}' exists.",
                          create_messagebox=True, error=True)
        return None

    try:
        # Extract the base name from the selected file
        base_name = os.path.basename(self.file_renamer_selected_file)

        # Check if there is a '-' in the name
        if '-' not in base_name:
            # If no '-', return none
            self.log_and_show("No '-' found in the file name. Cannot identify artist.")
            return None

        # Extract the artist from the text before '-'
        artist = base_name.split('-')[0].strip()

        # Search for a case-insensitive match for the artist in self.artist_directory
        for root, dirs, files in os.walk(self.artist_directory):
            for file_name in files:
                # Check if the artist is present in the file name
                if artist.lower() in file_name.lower():
                    # Construct the artist file path
                    artist_file_path = os.path.join(root, file_name)

                    # Skip the current file being compared
                    if artist_file_path == self.file_renamer_selected_file:
                        continue

                    # Verify the file exists and the keyword is in the absolute path
                    if os.path.exists(artist_file_path) and os.path.isfile(artist_file_path) \
                            and self.keyword_var.lower() in artist_file_path.lower():
                        # Check if the artist's name is not part of the directory path
                        if artist.lower() not in os.path.dirname(artist_file_path).lower():
                            # Return the result
                            return artist_file_path

        # If no matching artist is found, return none
        self.log_and_show("No matching artist file found.")
        return None

    except Exception as e:
        # Handle any unexpected exceptions and log an error message
        self.log_and_show(f"Unexpected error identifying artist: {e}",
                          create_messagebox=True, error=True)
        return None
