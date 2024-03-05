import os  # Operating System module for interacting with the operating system
import sys  # Handling standard error and output redirects
import re  # Regular expression module for pattern matching in strings
import json  # JSON module for working with JSON data
import send2trash  # Module for sending files to the trash instead of permanently deleting them
import subprocess  # Module for running external processes
import configparser  # Module for working with configuration files
import shutil  # Module for high-level file operations (copying, moving, etc.)
import string  # Module for various string manipulation functions and constants
import customtkinter as ctk  # Customtkinter for a modern gui
import threading  # Importing threading module for concurrent execution
import queue  # Importing queue module for implementing a simple FIFO queue
import time  # Import the time module for handling time-related functionality
import logging  # Logging module for capturing log messages
import atexit  # Module for registering functions to be called when the program is closing
from tkinter import filedialog, messagebox  # Tkinter modules for GUI file dialogs and message boxes
from tkinterdnd2 import DND_FILES, TkinterDnD  # Drag-and-drop functionality
from unidecode import unidecode  # Method that transliterates Unicode characters to their closest ASCII equivalents
from moviepy.editor import VideoFileClip  # Video editing module for working with video files
from moviepy.video.fx import all as vfx  # Importing all video effects (vfx) from the moviepy library


# Create a custom window class named SelectOptionWindow, inheriting from ctk.CTkToplevel
class SelectOptionWindow(ctk.CTkToplevel):
    def __init__(self, title, prompt, label_text, item_list, item_text=None, *args, **kwargs):
        """
        Initialize the SelectOptionWindow.

        Parameters:
        - title (str): The title of the window.
        - prompt (str): The text to be displayed as a prompt in the window.
        - label_text (str): Text to be displayed as a label for the radiobutton frame.
        - item_list (list): List of items for the scrollable radiobutton frame.
        - item_text (list, optional): GUI-friendly list of items for the scrollable radiobutton frame.
        - *args, **kwargs: Additional arguments that can be passed to the parent class constructor.
        """
        super().__init__(*args, **kwargs)

        # Set Window geometry
        self.geometry("500x450")

        # Set the window title
        self.title(title)

        # Prompt Label to display the provided prompt text
        self.prompt_label = ctk.CTkLabel(self, text=prompt)
        self.prompt_label.pack(pady=5)

        # If the gui-friendly text is provided, then use it, else use the item_list
        item_text = item_text if item_text else item_list

        # Create scrollable radiobutton frame
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500,
                                                                       item_list=item_list,
                                                                       item_text=item_text,
                                                                       label_text=label_text)
        self.scrollable_radiobutton_frame.pack(padx=10, pady=10)

        self.dialog_button_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.dialog_button_frame.pack(padx=10, pady=10)

        # Ok Button to confirm the selection
        self.ok_button = ctk.CTkButton(self.dialog_button_frame, text="Ok", command=self.ok_clicked)
        self.ok_button.pack(side=ctk.LEFT, padx=10)

        # Cancel Button to cancel the selection
        self.cancel_button = ctk.CTkButton(self.dialog_button_frame, text="Cancel", command=self.cancel_clicked)
        self.cancel_button.pack(side=ctk.RIGHT, padx=10)

        # Variable to store the selected option
        self.selected_option = None

    # Method to be executed when the Ok Button is clicked
    def ok_clicked(self):
        # Set the selected option to the selected item
        self.selected_option = self.scrollable_radiobutton_frame.get_selected_item()
        # Close the window
        self.destroy()

    # Method to be executed when the Cancel Button is clicked
    def cancel_clicked(self):
        # Close the window
        self.destroy()

    # Method to get the selected option from the window
    def get_selected_option(self):
        # Return the selected option
        return self.selected_option


# Create a scrollable radio button frame
class ScrollableRadiobuttonFrame(ctk.CTkScrollableFrame):
    """A scrollable frame containing radio buttons.

    Args:
        master (tk.Widget): The parent widget.
        item_list (list): A list of items to be used as variables for the radio buttons.
        item_text (list): A GUI-friendly list of items to be used as options for the radio buttons.
        command (callable, optional): A function to be called when a radio button is selected.
        **kwargs: Additional keyword arguments to be passed to the superclass constructor.
    """

    def __init__(self, master, item_list: list, item_text: list, command=None, **kwargs):
        # Initialize the ScrollableRadiobuttonFrame with a list of items and an optional command
        super().__init__(master, **kwargs)

        # Set the command to be executed on radio button selection
        self.command = command

        # Create a StringVar to track the selected radio button value
        self.radiobutton_variable = ctk.StringVar()

        # List to store radio button instances
        self.radiobutton_list = []

        # Iterate through the item list and add each item as a radio button
        for i, item in enumerate(item_list):
            # GUI-friendly formatting
            text = item_text[i] if i < len(
                item_text) else item  # Use the corresponding text if provided or fallback to the item itself
            self.add_item(item, text)

        # Set the default radio button
        if item_list:
            # Set the variable to the value of the first item
            self.radiobutton_variable.set(item_list[0])

    def add_item(self, value: str, text: str):
        """Add a new radio button with the specified item.

        Args:
            value (str): The variable for the radio button.
            text (str): The text for the radio button.
        """
        # Create a radio button with the specified text, value, and variable
        radiobutton = ctk.CTkRadioButton(self, text=text, value=value, variable=self.radiobutton_variable)

        # Configure the radio button to execute a command on selection, if provided
        if self.command is not None:
            radiobutton.configure(command=self.command)

        # Place the radio button in the grid with appropriate row and column settings
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))

        # Add the radio button to the list for tracking
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item: str) -> None:
        """Remove the specified item from the list of radio buttons.

        Args:
            item (str): The text of the item to be removed.
        """
        # Iterate through the radio buttons to find and remove the specified item
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_selected_item(self) -> str:
        """Get the value of the selected radio button.

        Returns:
            str: The value of the selected radio button.
        """
        # Retrieve the value of the selected radio button
        return self.radiobutton_variable.get()


class OCDFileRenamer(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        # Call the __init__ method of the parent class (TkinterDnD) with the given arguments
        super().__init__(*args, **kwargs)

        # Determine TkinterDnD version and store it in the TkdndVersion attribute
        # noinspection PyProtectedMember
        self.TkdndVersion = TkinterDnD._require(self)

        # Set the window title
        self.title("O.C.D. File Editor")

        """Load Configuration"""
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
        self.initial_directory = config.get('Filepaths', 'initial_directory', fallback='/path/to/folder')
        self.initial_output_directory = config.get('Filepaths', 'initial_output_directory', fallback='/path/to/folder')
        self.double_check_directory = config.get('Filepaths', 'double_check_directory',
                                                 fallback='double_check_reminders')
        self.no_go_directory = config.get('Filepaths', 'no_go_directory', fallback='no_go_reminders')
        self.artist_directory = config.get('Filepaths', 'artist_directory', fallback='artist_directory')
        self.artist_file = config.get('Filepaths', 'artist_file', fallback='list_of_artists.txt')
        self.no_go_artist_file = config.get('Filepaths', 'no_go_artist_file', fallback='list_of_no_go_artists.txt')
        self.dictionary_file = config.get('Filepaths', 'dictionary_file', fallback='dictionary.json')

        # Variables and window geometry
        self.scaling = config.get('Settings', 'scaling', fallback='100')
        self.default_weight = config.get('Settings', 'default_weight', fallback=9)
        self.default_ctn_weight = config.get('Settings', 'default_ctn_weight', fallback=1)
        self.default_decibel = config.get('Settings', 'default_decibel', fallback=0.0)
        self.default_audio_normalization = config.get('Settings', 'default_audio_normalization', fallback=0.0)
        self.default_minute = config.get('Settings', 'default_minute', fallback=0)
        self.default_second = config.get('Settings', 'default_second', fallback=0)
        self.default_frame = config.get('Settings', 'default_frame', fallback="file_renamer_window")
        self.default_cat_tab = config.get('Settings', 'default_cat_tab', fallback="All")
        self.default_add_remove_tab = config.get('Settings', 'default_add_remove_tab', fallback="Artist")
        self.file_renamer_log = config.get('Logs', 'file_renamer_log', fallback="file_renamer.log")
        self.default_placement_var = config.get("Settings", "default_placement_var", fallback="special_character")
        self.special_character_var = config.get("Settings", "special_character_var", fallback="-")

        self.geometry(config.get('Settings', 'geometry', fallback='1280x850'))
        self.column_numbers = int(config.get('Settings', 'column_numbers', fallback=7))
        self.default_most_number = int(config.get('Settings', 'default_most_number', fallback=9))
        self.reset_output_directory_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "reset_output_directory_var", fallback=False))
        self.use_custom_tab_names_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "use_custom_tab_names_var", fallback=False))
        self.sort_tab_names_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "sort_tab_names_var", fallback=False))
        self.sort_reverse_order_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "sort_reverse_order_var", fallback=False))
        self.suggest_output_directory_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "suggest_output_directory_var", fallback=False))
        self.artist_search_var = ctk.BooleanVar(value=config.getboolean("Settings", "artist_search_var",
                                                                        fallback=False))
        self.ignore_known_artists_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "ignore_known_artists_var", fallback=False))
        self.artist_common_categories_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "artist_common_categories_var", fallback=False))
        self.remove_artist_duplicates_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "remove_artist_duplicates_var", fallback=True))
        self.move_up_directory_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "move_up_directory_var", fallback=False))
        self.move_text_var = ctk.BooleanVar(value=config.getboolean('Settings', 'move_text_var', fallback=False))
        self.open_on_file_drop_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "open_on_file_drop_var", fallback=False))
        self.double_check_var = ctk.BooleanVar(value=config.getboolean("Settings", "double_check_var", fallback=False))
        self.activate_logging_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "activate_logging_var", fallback=False))
        self.suppress_var = ctk.BooleanVar(value=config.getboolean("Settings", "suppress_var", fallback=True))
        self.show_messageboxes_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "show_messageboxes_var", fallback=True))
        self.show_confirmation_messageboxes_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "show_confirmation_messageboxes_var",
                                    fallback=True))
        self.fallback_confirmation_var = ctk.BooleanVar(value=config.getboolean("Settings", "fallback_confirmation_var",
                                                                                fallback=False))
        self.truncate_var = ctk.BooleanVar(value=config.getboolean("Settings", "truncate_var", fallback=True))

        # Name Normalizer
        self.remove_all_symbols_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_all_symbols_var",
                                                                             fallback=False))

        self.remove_most_symbols_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_most_symbols_var",
                                                                              fallback=False))

        self.remove_non_ascii_symbols_var = ctk.BooleanVar(value=config.getboolean("Settings",
                                                                                   "remove_non_ascii_symbols_var",
                                                                                   fallback=False))

        self.remove_number_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_number_var",
                                                                        fallback=False))

        self.tail_var = ctk.BooleanVar(value=config.getboolean("Settings", "tail_var", fallback=False))

        self.remove_parenthesis_trail_var = ctk.BooleanVar(value=config.getboolean("Settings",
                                                                                   "remove_parenthesis_trail_var",
                                                                                   fallback=False))

        self.remove_parenthesis_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_parenthesis_var",
                                                                             fallback=False))

        self.remove_hashtag_trail_var = ctk.BooleanVar(value=config.getboolean("Settings",
                                                                               "remove_hashtag_trail_var",
                                                                               fallback=False))

        self.remove_hashtag_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_hashtag_var",
                                                                         fallback=False))

        self.remove_custom_text_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_custom_text_var",
                                                                             fallback=False))

        self.replace_mode_var = ctk.BooleanVar(value=config.getboolean("Settings", "replace_mode_var", fallback=False))

        self.remove_dash_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_dash_var", fallback=False))

        self.remove_endash_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_endash_var",
                                                                        fallback=False))

        self.remove_emdash_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_emdash_var",
                                                                        fallback=False))

        self.remove_ampersand_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_ampersand_var",
                                                                           fallback=False))

        self.remove_at_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_at_var", fallback=False))

        self.remove_underscore_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_underscore_var",
                                                                            fallback=False))

        self.remove_comma_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_comma_var", fallback=False))

        self.remove_single_quote_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_single_quote_var",
                                                                              fallback=False))

        self.remove_double_quote_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_double_quote_var",
                                                                              fallback=False))

        self.remove_colon_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_colon_var", fallback=False))

        self.remove_semicolon_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_semicolon_var",
                                                                           fallback=False))

        self.remove_percent_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_percent_var",
                                                                         fallback=False))

        self.remove_caret_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_caret_var", fallback=False))

        self.remove_dollar_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_dollar_var",
                                                                        fallback=False))

        self.remove_asterisk_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_asterisk_var",
                                                                          fallback=False))

        self.remove_plus_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_plus_var", fallback=False))

        self.remove_equal_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_equal_var", fallback=False))

        self.remove_curly_brace_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_curly_brace_var",
                                                                             fallback=False))

        self.remove_square_bracket_var = ctk.BooleanVar(value=config.getboolean("Settings",
                                                                                "remove_square_bracket_var",
                                                                                fallback=False))

        self.remove_pipe_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_pipe_var", fallback=False))

        self.remove_backslash_var = ctk.BooleanVar(value=config.getboolean("Settings", "remove_backslash_var",
                                                                           fallback=False))

        self.remove_angle_bracket_var = ctk.BooleanVar(value=config.getboolean("Settings",
                                                                               "remove_angle_bracket_var",
                                                                               fallback=False))

        self.remove_question_mark_var = ctk.BooleanVar(value=config.getboolean("Settings",
                                                                               "remove_question_mark_var",
                                                                               fallback=False))

        self.remove_extra_whitespace_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "remove_extra_whitespace_var", fallback=False))

        self.title_var = ctk.BooleanVar(value=config.getboolean("Settings", "title_var", fallback=False))

        self.artist_identifier_var = ctk.BooleanVar(
            value=config.getboolean("Settings", "artist_identifier_var", fallback=False))

        self.reset_var = ctk.BooleanVar(value=config.getboolean("Settings", "reset_var", fallback=False))

        self.reset_video_entries_var = ctk.BooleanVar(value=config.getboolean("Settings", "reset_video_entries_var",
                                                                              fallback=True))

        self.reset_add_remove_var = ctk.BooleanVar(value=config.getboolean("Settings", "reset_add_remove_var",
                                                                           fallback=True))
        self.auto_add_acc_record_var = ctk.BooleanVar(value=config.getboolean("Settings", "auto_add_acc_record_var",
                                                                              fallback=False))

        self.deep_walk_var = ctk.BooleanVar(value=config.getboolean("Settings", "deep_walk_var", fallback=False))

        # Video Editor
        self.remove_successful_lines_var = ctk.BooleanVar(value=config.getboolean("Settings",
                                                                                  "remove_successful_lines_var",
                                                                                  fallback=False))
        self.default_rotation_var = config.get("Settings", "default_rotation_var", fallback="none")
        """End Load Configuration"""

        """Cache"""
        # Set the cache duration to 10 minutes (600 seconds)
        self.cache_duration = 600
        self.last_cache_update = 0
        self.cached_artist_files = []
        """End Cache"""

        # Initialize instance variables for selected files, output directories, queue, and last used files
        self.file_renamer_selected_file = ""
        self.file_renamer_last_used_file = ""
        self.output_directory = ""
        self.history = []
        self.nn_history = []
        self.file_renamer_queue = []
        self.cat_tabs = {}
        self.add_remove_tabs = {}
        self.settings_tabs = {}
        self.excluded_folders = []
        self.custom_text_to_replace = {}
        self.file_extensions = []
        self.valid_extensions = []
        self.weight_to_tab_name = {}
        self.categories = {}
        self.artist_common_categories = {}
        self.name_normalizer_selected_file = ""
        self.name_normalizer_last_used_file = ""
        self.name_normalizer_output_directory = ""
        self.video_editor_selected_file = ""
        self.video_editor_last_used_file = ""
        self.video_editor_output_directory = ""
        self.acc_selected_artist = ""

        # Initialize the queue for FIFO queue module functionality
        self.queue = queue.Queue()

        """Threading"""
        self.name_processing_thread_single = ""
        self.name_processing_thread_multiple = ""
        self.video_processing_thread = ""

        # Flag to indicate whether processing should be interrupted
        self.interrupt_name_processing_thread_var = False
        self.interrupt_video_processing_thread_var = False

        """Tab Names"""
        # List of tab names for the add_remove_tabview
        self.add_remove_tab_names = ["Artist", "Category", "Custom Tab Name", "Custom Text to Replace", "Exclude",
                                     "File Extensions", "NO GO", "Valid Extensions"]

        # List of tab names for the settings_tabview
        self.settings_tab_names = ["Appearance", "Artist", "File Operations", "Logging", "Messaging", "Reminders",
                                   "Tabs"]

        # Initialize the standard output and error variables (Fix for MoviePy overriding user's logging choice)
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # Initialize buttons
        self.cat_tabview = None
        self.buttons = None
        self.most_buttons = None
        self.all_buttons = None

        # Initialize Main GUI elements
        # Housekeeping Note: Some attributes are initialized as None and later assigned specific GUI elements
        self.navigation_frame = None
        self.navigation_frame_label = None
        self.file_renamer_button = None
        self.name_normalizer_button = None
        self.video_editor_button = None
        self.add_remove_button = None
        self.settings_button = None

        # Initialize File Renamer GUI elements
        self.file_renamer_frame = None
        self.file_renamer_canvas = None
        self.file_renamer_scrollbar = None
        self.file_renamer_scrollable_frame = None
        self.file_renamer_scrollable_frame_window = None
        self.file_renamer_top_frame = None
        self.browse_file_button = None
        self.file_display_text = None
        self.file_display_entry = None
        self.name_length_text = None
        self.name_length_label = None
        self.cat_button_frame = None
        self.custom_text_frame = None

        self.output_directory_browse_button = None
        self.output_directory_entry = None
        self.prefix_text_entry = None
        self.custom_text_entry = None
        self.rename_button = None
        self.button_group_frame = None
        self.undo_button = None
        self.undo_file_rename_button = None
        self.clear_button = None
        self.trash_button = None
        self.file_renamer_last_used_file_button = None
        self.last_used_frame = None
        self.last_used_display_label = None
        self.last_used_display = None
        self.file_renamer_message_label_frame = None
        self.file_renamer_message_label = None
        self.folder_operations_frame = None
        self.reset_output_directory_checkbox = None
        self.suggest_output_directory_checkbox = None
        self.move_up_directory_checkbox = None
        self.move_text_checkbox = None
        self.artist_common_categories_checkbox = None
        self.send_to_module_frame = None
        self.send_to_video_editor_button = None
        self.send_to_name_normalizer_button = None
        self.placement_frame = None
        self.placement_label = None
        self.placement_choice = None
        self.prefix_radio = None
        self.special_character_radio = None
        self.suffix_radio = None

        # Initialize Name Normalizer GUI elements
        self.name_normalizer_frame = None
        self.name_normalizer_top_frame = None
        self.name_normalizer_label = None
        self.checkbox_frame1 = None
        self.nn_browse_button = None
        self.nn_path_entry = None
        self.tail_checkbox = None
        self.remove_all_symbols_checkbox = None
        self.remove_most_symbols_checkbox = None
        self.remove_non_ascii_symbols_checkbox = None
        self.remove_numbers_checkbox = None
        self.checkbox_frame2 = None
        self.remove_dash_checkbox = None
        self.remove_endash_checkbox = None
        self.remove_emdash_checkbox = None
        self.remove_hashtag_checkbox = None
        self.checkbox_frame3 = None
        self.remove_ampersand_checkbox = None
        self.remove_at_checkbox = None
        self.remove_underscore_checkbox = None
        self.remove_comma_checkbox = None
        self.remove_dollar_checkbox = None
        self.checkbox_frame4 = None
        self.title_checkbox = None
        self.remove_single_quote_checkbox = None
        self.remove_double_quote_checkbox = None
        self.remove_colon_checkbox = None
        self.remove_semicolon_checkbox = None
        self.remove_percent_checkbox = None
        self.remove_caret_checkbox = None
        self.checkbox_frame5 = None
        self.remove_asterisk_checkbox = None
        self.remove_parenthesis_checkbox = None
        self.remove_plus_checkbox = None
        self.remove_equal_checkbox = None
        self.remove_curly_brace_checkbox = None
        self.remove_square_bracket_checkbox = None
        self.checkbox_frame6 = None
        self.remove_pipe_checkbox = None
        self.remove_backslash_checkbox = None
        self.remove_angle_bracket_checkbox = None
        self.remove_question_mark_checkbox = None
        self.checkbox_frame7 = None
        self.remove_parenthesis_trail_checkbox = None
        self.remove_hashtag_trail_checkbox = None
        self.remove_custom_text_checkbox = None
        self.replace_mode_switch = None
        self.remove_extra_whitespace_checkbox = None
        self.artist_identifier_checkbox = None
        self.deep_walk_checkbox = None
        self.reset_checkbox = None
        self.string_frame = None
        self.prefix_label = None
        self.prefix_entry = None
        self.suffix_label = None
        self.suffix_entry = None
        self.replace_label = None
        self.original_entry = None
        self.replace_entry = None
        self.output_directory_frame = None
        self.browse_move_directory_button = None
        self.move_directory_entry = None
        self.custom_text_label = None
        self.custom_text_removal_entry = None
        self.normalize_folder_frame = None
        self.normalize_preview_button = None
        self.interrupt_button = None
        self.normalize_button = None
        self.send_to_module_frame1 = None
        self.send_to_file_renamer_button1 = None
        self.send_to_video_editor_button1 = None
        self.clear_name_normalizer_selection_button = None
        self.undo_nn_button = None
        self.name_normalizer_last_used_file_button = None
        self.name_normalizer_message_label_frame = None
        self.name_normalizer_message_label = None
        self.slider_progressbar_frame = None
        self.progressbar = ""

        # Initialize Video Editor GUI elements
        self.video_editor_frame = None
        self.video_editor_top_frame = None
        self.video_editor_label = None
        self.browse_input_method_button = None
        self.input_method_entry = None
        self.rotation_frame = None
        self.rotation_label = None
        self.rotation_var = None
        self.left_radio = None
        self.right_radio = None
        self.flip_radio = None
        self.mirror_radio = None
        self.no_rotation_radio = None
        self.decibel_frame = None
        self.decibel_label = None
        self.decibel_var = None
        self.decibel_entry = None
        self.audio_normalization_frame = None
        self.audio_normalization_label = None
        self.audio_normalization_var = None
        self.audio_normalization_entry = None
        self.trim_frame = None
        self.trim_label = None
        self.minute_var = None
        self.minute_entry = None
        self.colon_label = None
        self.second_var = None
        self.second_entry = None
        self.trim_label1 = None
        self.minute_var1 = None
        self.minute_entry1 = None
        self.colon_label1 = None
        self.second_var1 = None
        self.second_entry1 = None
        self.video_editor_output_directory_frame = None
        self.browse_video_editor_output_directory_button = None
        self.video_editor_output_directory_entry = None
        self.process_video_editor_frame = None
        self.clear_video_editor_selection_button = None
        self.video_editor_last_used_file_button = None
        self.interrupt_button1 = None
        self.process_video_edits_button = None
        self.video_editor_checkbox_frame = None
        self.remove_successful_lines_checkbox = None
        self.reset_video_checkbox = None
        self.video_editor_message_label_frame = None
        self.video_editor_message_label = None
        self.send_to_module_frame2 = None
        self.send_to_file_renamer_button = None
        self.send_to_name_normalizer_button1 = None
        self.slider_progressbar_frame1 = None
        self.progressbar1 = ""

        # Initialize Add/Remove GUI elements
        self.add_remove_frame = None
        self.add_remove_label = None
        self.add_remove_tabview = None
        self.add_remove_artist_top_frame = None
        self.add_remove_artist_label_frame = None
        self.add_remove_artist_label = None
        self.add_remove_artist_entry_frame = None
        self.add_artist_button = None
        self.add_artist_entry = None
        self.remove_artist_button = None
        self.remove_artist_entry = None
        self.auto_add_acc_record_frame = None
        self.auto_add_acc_record_checkbox = None
        self.add_remove_acc_record_label_frame = None
        self.add_remove_acc_record_label = None
        self.add_remove_acc_record_entry_frame = None
        self.add_acc_record_button = None
        self.add_acc_record_entry = None
        self.remove_acc_record_button = None
        self.remove_acc_record_entry = None
        self.add_remove_acc_label_frame = None
        self.add_remove_acc_label = None
        self.acc_browse_frame = None
        self.browse_artist_button = None
        self.acc_display_text = None
        self.acc_display_entry = None
        self.detect_artist_button = None
        self.add_remove_acc_entry_frame = None
        self.add_acc_button = None
        self.add_acc_entry = None
        self.remove_acc_button = None
        self.remove_acc_entry = None
        self.category_frame = None
        self.add_category_button = None
        self.category_entry = None
        self.weight_label = None
        self.weight_var = None
        self.weight_entry = None
        self.remove_category_button = None
        self.remove_category_entry = None
        self.ctn_frame = None
        self.add_ctn_button = None
        self.custom_tab_name_entry = None
        self.weight_label1 = None
        self.weight_var1 = None
        self.weight_entry1 = None
        self.remove_ctn_button = None
        self.remove_custom_tab_name_entry = None
        self.ctr_entry_frame = None
        self.add_ctr_button = None
        self.add_ctr_name_entry = None
        self.replacement_label = None
        self.replacement_text_entry = None
        self.remove_ctr_button = None
        self.remove_ctr_name_entry = None
        self.exclude_entry_frame = None
        self.add_exclude_button = None
        self.add_exclude_name_entry = None
        self.remove_exclude_button = None
        self.remove_exclude_name_entry = None
        self.file_extension_entry_frame = None
        self.add_file_extension_button = None
        self.add_file_extension_entry = None
        self.remove_file_extension_button = None
        self.remove_file_extension_entry = None
        self.no_go_entry_frame = None
        self.add_no_go_button = None
        self.add_no_go_name_entry = None
        self.remove_no_go_button = None
        self.remove_no_go_name_entry = None
        self.valid_extension_entry_frame = None
        self.add_valid_extension_button = None
        self.add_valid_extension_entry = None
        self.remove_valid_extension_button = None
        self.remove_valid_extension_entry = None
        self.clear_add_remove_frame = None
        self.clear_add_remove_button = None
        self.reset_add_remove_frame = None
        self.reset_add_remove_checkbox = None
        self.add_remove_message_label_frame = None
        self.add_remove_message_label = None

        # Initialize Settings GUI elements
        self.settings_frame = None
        self.settings_label = None
        self.settings_tabview = None
        self.remove_duplicates_switch = None
        self.artist_switch_frame = None
        self.artist_search_label = None
        self.artist_search_switch = None
        self.ignore_known_artists_switch = None
        self.artist_identifier_label = None
        self.file_ops_frame = None
        self.file_ops_switch_frame = None
        self.open_on_file_drop_switch = None
        self.reminders_frame = None
        self.double_check_switch = None
        self.logging_switch_frame = None
        self.activate_logging_switch = None
        self.suppress_switch = None
        self.show_messageboxes_switch = None
        self.confirmation_frame = None
        self.show_confirmation_messageboxes_switch = None
        self.fallback_confirmation_label = None
        self.true_radio = None
        self.false_radio = None
        self.truncate_text_switch = None
        self.tab_name_frame = None
        self.use_custom_tab_names_switch = None
        self.sort_tab_names_switch = None
        self.sort_tab_names_reverse_switch = None
        self.gui_settings_frame = None
        self.appearance_mode_label = None
        self.appearance_mode_menu = None
        self.scaling_label = None
        self.scaling_optionemenu = None
        self.master_entry_frame = None
        self.initial_directory_frame = None
        self.browse_initial_directory_button = None
        self.initial_directory_entry = None
        self.browse_initial_output_directory_button = None
        self.initial_output_directory_entry = None
        self.double_check_reminder_directory_frame = None
        self.browse_reminder_directory_button = None
        self.double_check_reminder_directory_entry = None
        self.browse_no_go_directory_button = None
        self.no_go_reminder_directory_entry = None
        self.open_artist_file_button = None
        self.artist_directory_frame = None
        self.browse_artist_directory_button = None
        self.artist_directory_entry = None
        self.browse_artist_file_button = None
        self.artist_file_entry = None
        self.configuration_file_frame = None
        self.open_configuration_file_button = None
        self.configuration_file_entry = None
        self.dictionary_file_frame = None
        self.open_dictionary_file_button = None
        self.dictionary_file_entry = None
        self.open_log_file_button = None
        self.log_file_entry = None
        self.logging_browse_frame = None
        self.logging_frame = None
        self.artist_frame = None
        self.artist_browse_frame = None

        # Enable drag-and-drop functionality for files
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_file_drop)

        # Initial check for activate logging state prior to application launch
        self.handle_logging_activation()

        # Register the cleanup method to be called on program exit
        atexit.register(self.cleanup_on_exit)

        # Initialize frame name to default frame
        self.frame_name = self.default_frame

        # Initialize the json file dictionaries
        self.initialize_json()

        # Create the GUI elements
        self.create_gui()

        # Select default frame
        self.select_frame_by_name(self.default_frame)

        # Set scaling at the start
        self.change_scaling_event(self.scaling)

    def create_gui(self):
        # Set up grid layout with 1 row and 2 columns, configuring weights for resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation frame (Buttons on the left hand side)
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)  # Index number is responsible for floating

        # Create label for the navigation frame
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  O.C.D. \nFile Editor",
                                                   compound="left",
                                                   font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=5, pady=5)

        # Create file renamer button with specific styling and command
        self.file_renamer_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                 text="File Renamer",
                                                 fg_color="transparent", text_color=("gray10", "gray90"),
                                                 hover_color=("gray70", "gray30"),
                                                 anchor="w", command=self.file_renamer_button_event)
        self.file_renamer_button.grid(row=1, column=0, sticky="ew")

        # Create button for Name Normalizer with specific styling and command
        self.name_normalizer_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                    border_spacing=10, text="Name Normalizer",
                                                    fg_color="transparent", text_color=("gray10", "gray90"),
                                                    hover_color=("gray70", "gray30"),
                                                    anchor="w",
                                                    command=self.name_normalizer_button_event)
        self.name_normalizer_button.grid(row=2, column=0, sticky="ew")

        # Create button for Video Editor with specific styling and command
        self.video_editor_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                 border_spacing=10, text="Video Editor",
                                                 fg_color="transparent", text_color=("gray10", "gray90"),
                                                 hover_color=("gray70", "gray30"),
                                                 anchor="w",
                                                 command=self.video_editor_button_event)
        self.video_editor_button.grid(row=3, column=0, sticky="ew")

        # Create Add/Remove button with specific styling and command
        self.add_remove_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                               text="Add/Remove",
                                               fg_color="transparent", text_color=("gray10", "gray90"),
                                               hover_color=("gray70", "gray30"),
                                               anchor="w",
                                               command=self.add_remove_button_event)
        self.add_remove_button.grid(row=4, column=0, sticky="ew")

        # Create Settings button with specific styling and command
        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                             text="Settings",
                                             fg_color="transparent", text_color=("gray10", "gray90"),
                                             hover_color=("gray70", "gray30"),
                                             anchor="w",
                                             command=self.settings_button_event)
        self.settings_button.grid(row=5, column=0, sticky="ew")

        """
        file_renamer_window
        """
        # Create file renamer frame
        self.file_renamer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.file_renamer_frame.grid(row=0, column=1, sticky="nsew")
        self.file_renamer_frame.grid_columnconfigure(0, weight=1)
        self.file_renamer_frame.grid_rowconfigure(0, weight=1)

        # Create a canvas and a scrollbar
        self.file_renamer_canvas = ctk.CTkCanvas(self.file_renamer_frame, highlightthickness=0)
        self.file_renamer_scrollbar = ctk.CTkScrollbar(self.file_renamer_frame, command=self.file_renamer_canvas.yview)
        self.file_renamer_canvas.configure(yscrollcommand=self.file_renamer_scrollbar.set)

        # Set default background color based on system mode
        self.update_background_color()

        # Place the canvas and the scrollbar in the grid
        self.file_renamer_canvas.grid(row=0, column=0, sticky="nsew")
        self.file_renamer_scrollbar.grid(row=0, column=1, sticky="ns")

        # Create a frame inside the canvas for scrollable content
        self.file_renamer_scrollable_frame = ctk.CTkFrame(self.file_renamer_canvas, corner_radius=0,
                                                          bg_color="transparent")
        self.file_renamer_scrollable_frame_window = (self.file_renamer_canvas.create_window(
            (0, 0),
            window=self.file_renamer_scrollable_frame,
            anchor="nw"))

        # Bind canvas and frame for scrolling functionality
        self.file_renamer_canvas.bind('<Configure>', self.on_canvas_configure)
        self.file_renamer_scrollable_frame.bind('<Configure>', self.on_frame_configure)

        # Top frame in the file renamer window
        self.file_renamer_top_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.file_renamer_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Browse file button
        self.browse_file_button = ctk.CTkButton(self.file_renamer_top_frame, text="Browse File",
                                                command=self.browse_input)
        self.browse_file_button.grid(row=0, column=0, padx=5)

        # Selected File Display
        self.file_display_text = ctk.StringVar()
        self.file_display_text.set("Select a file using the 'Browse File' button or drag and drop it into the "
                                   "program...")
        self.file_display_entry = ctk.CTkEntry(self.file_renamer_top_frame, width=850,
                                               textvariable=self.file_display_text)
        self.file_display_entry.grid(row=0, column=1, padx=5)

        # Name Length Display
        self.name_length_text = ctk.IntVar()
        self.name_length_label = ctk.CTkLabel(self.file_renamer_top_frame, textvariable=self.name_length_text)
        self.name_length_label.grid(row=0, column=2, padx=5)

        # Categories button frame
        self.cat_button_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame,
                                             corner_radius=0, fg_color="transparent")
        self.cat_button_frame.grid(row=1, column=0, padx=10, pady=5)

        # Create a cat_tabview and initialize category buttons on cat_button_frame
        self.create_cat_tabview()

        # Frame to group custom text entry and output directory
        self.custom_text_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                              fg_color="transparent")
        self.custom_text_frame.grid(row=2, column=0, padx=10)

        # Output Directory Browse Button
        self.output_directory_browse_button = ctk.CTkButton(self.custom_text_frame,
                                                            text="Output Directory",
                                                            command=self.browse_output_directory)
        self.output_directory_browse_button.grid(row=0, column=0, padx=5, pady=5)

        # Output Directory Entry
        self.output_directory_entry = ctk.CTkEntry(self.custom_text_frame, width=340)
        self.output_directory_entry.grid(row=0, column=1, padx=5, pady=5)

        # Prefix Text Entry
        self.prefix_text_entry = ctk.CTkEntry(self.custom_text_frame, width=70)
        self.prefix_text_entry.insert(0, "Prefix...")
        self.prefix_text_entry.grid(row=0, column=2, padx=10, pady=10)

        # Bind the update_file_display function to the prefix text entry change event
        self.prefix_text_entry.bind("<KeyRelease>", self.update_file_display)

        # Custom Text Entry
        self.custom_text_entry = ctk.CTkEntry(self.custom_text_frame, width=290)
        self.custom_text_entry.insert(0, "Enter your custom text here...")
        self.custom_text_entry.grid(row=0, column=3, padx=10, pady=10)

        # Bind the update_file_display function to the custom text entry change event
        self.custom_text_entry.bind("<KeyRelease>", self.update_file_display)

        # Rename File Button
        self.rename_button = ctk.CTkButton(self.custom_text_frame, text="Rename",
                                           command=self.rename_files)
        self.rename_button.grid(row=0, column=4, padx=5, pady=5)

        # Frame to group miscellaneous buttons
        self.button_group_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                               fg_color="transparent")
        self.button_group_frame.grid(row=3, column=0, padx=10)

        # Undo Button
        self.undo_button = ctk.CTkButton(self.button_group_frame, text="Undo", command=self.undo_last)
        self.undo_button.grid(row=0, column=0, padx=10, pady=10)

        # Undo File Rename Button
        self.undo_file_rename_button = ctk.CTkButton(self.button_group_frame,
                                                     text="Undo File Rename",
                                                     command=self.undo_file_rename)
        self.undo_file_rename_button.grid(row=0, column=1, padx=10, pady=10)

        # Clear Button
        self.clear_button = ctk.CTkButton(self.button_group_frame, text="Clear",
                                          command=lambda: self.clear_selection(frame_name="file_renamer_window"))
        self.clear_button.grid(row=0, column=2, padx=10, pady=10)

        # Move to Trash Button
        self.trash_button = ctk.CTkButton(self.button_group_frame, text="Move to Trash",
                                          command=self.move_file_to_trash)
        self.trash_button.grid(row=0, column=3, padx=10, pady=10)

        # Select File Renamer Last Used File Button
        self.file_renamer_last_used_file_button = ctk.CTkButton(self.button_group_frame, text="Reload Last File",
                                                                command=self.load_last_used_file)
        self.file_renamer_last_used_file_button.grid(row=0, column=4, padx=10, pady=10)

        # Frame to display the last used file
        self.last_used_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.last_used_frame.grid(row=4, column=0, padx=5)

        # Last Used File Label
        self.last_used_display_label = ctk.CTkLabel(self.last_used_frame, text="Last used file:")
        self.last_used_display_label.grid(row=0, column=0, padx=5, pady=5)

        # Last Used File Display
        self.last_used_display = ctk.CTkLabel(self.last_used_frame, text="")
        self.last_used_display.grid(row=0, column=1, padx=5, pady=5)

        # Frame to display messages
        self.file_renamer_message_label_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                                             fg_color="transparent")
        self.file_renamer_message_label_frame.grid(row=5, column=0, padx=10)

        # Message Label
        self.file_renamer_message_label = ctk.CTkLabel(self.file_renamer_message_label_frame, text="")
        self.file_renamer_message_label.grid(row=0, column=0, padx=10, pady=10)

        # Frame to group placement frame
        self.placement_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.placement_frame.grid(row=6, column=0, padx=10, pady=10)

        # Placement Label
        self.placement_label = ctk.CTkLabel(self.placement_frame, text="Placement:")
        self.placement_label.grid(row=0, column=0, padx=10)

        # Variable to track the user's placement choice (prefix, suffix, or special_character)
        self.placement_choice = ctk.StringVar()
        self.placement_choice.set(self.default_placement_var)

        # Trace the changes in the StringVar
        self.placement_choice.trace_add("write", self.update_file_display)

        # Radio button for prefix
        self.prefix_radio = ctk.CTkRadioButton(self.placement_frame, text="Prefix",
                                               variable=self.placement_choice,
                                               value="prefix")
        self.prefix_radio.grid(row=0, column=1, padx=10)

        # Radio button for special_character
        self.special_character_radio = ctk.CTkRadioButton(self.placement_frame,
                                                          text=f"Special Character: {self.special_character_var}",
                                                          variable=self.placement_choice,
                                                          value="special_character")
        self.special_character_radio.grid(row=0, column=2, padx=10)

        # Radio button for suffix
        self.suffix_radio = ctk.CTkRadioButton(self.placement_frame, text="Suffix",
                                               variable=self.placement_choice,
                                               value="suffix")
        self.suffix_radio.grid(row=0, column=3, padx=10)

        # Frame to group folder operations
        self.folder_operations_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                                    fg_color="transparent")
        self.folder_operations_frame.grid(row=7, column=0, padx=10)

        # Checkbox to enable/disable resetting the Output Directory
        self.reset_output_directory_checkbox = ctk.CTkCheckBox(self.folder_operations_frame,
                                                               text="Reset Output Dir.",
                                                               variable=self.reset_output_directory_var)
        self.reset_output_directory_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable suggesting an output directory
        self.suggest_output_directory_checkbox = ctk.CTkCheckBox(self.folder_operations_frame, text="Suggest Output "
                                                                                                    "Dir.",
                                                                 variable=self.suggest_output_directory_var)
        self.suggest_output_directory_checkbox.grid(row=0, column=1, padx=5, pady=5)

        # Checkbox to enable/disable moving the file up one folder
        self.move_up_directory_checkbox = ctk.CTkCheckBox(self.folder_operations_frame, text="Move Up One Dir.",
                                                          variable=self.move_up_directory_var)
        self.move_up_directory_checkbox.grid(row=0, column=2, padx=5, pady=5)

        # Checkbox to enable/disable move text between - and __-__
        self.move_text_checkbox = ctk.CTkCheckBox(self.folder_operations_frame, text="Move Text",
                                                  variable=self.move_text_var)
        self.move_text_checkbox.grid(row=0, column=3, padx=5, pady=5)

        # Checkbox to enable/disable add artist common categories
        self.artist_common_categories_checkbox = ctk.CTkCheckBox(self.folder_operations_frame,
                                                                 text="Add Artist Common Categories",
                                                                 variable=self.artist_common_categories_var)
        self.artist_common_categories_checkbox.grid(row=0, column=4, padx=5, pady=5)

        # Bind the callback function to the artist_common_categories_var variable
        self.artist_common_categories_var.trace_add("write", self.handle_common_categories_state)

        # Send to Module frame
        self.send_to_module_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame,
                                                 corner_radius=0,
                                                 fg_color="transparent")
        self.send_to_module_frame.grid(row=8, column=0, padx=5)

        # Send to Video Editor button
        self.send_to_video_editor_button = ctk.CTkButton(self.send_to_module_frame, text="Send to Video Editor",
                                                         command=lambda: self.send_to_module(
                                                             destination="video_editor_module"))
        self.send_to_video_editor_button.grid(row=0, column=0, padx=10, pady=10)

        # Send to Name Normalizer button
        self.send_to_name_normalizer_button = ctk.CTkButton(self.send_to_module_frame,
                                                            text="Send to Name Normalizer",
                                                            command=lambda: self.send_to_module(
                                                                destination="name_normalizer_module"))
        self.send_to_name_normalizer_button.grid(row=0, column=1, padx=10, pady=10)

        """
        name_normalizer_window
        """
        # Create Name Normalizer frame
        self.name_normalizer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.name_normalizer_frame.grid_columnconfigure(0, weight=1)

        # Name Normalizer Label
        self.name_normalizer_label = ctk.CTkLabel(self.name_normalizer_frame, text="Name Normalizer",
                                                  font=ctk.CTkFont(size=15, weight="bold"))
        self.name_normalizer_label.grid(row=0, column=0, padx=10, pady=10)

        # Name Normalizer Top frame
        self.name_normalizer_top_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                                      fg_color="transparent")
        self.name_normalizer_top_frame.grid(row=1, column=0, padx=10, pady=5)

        # Browse button
        self.nn_browse_button = ctk.CTkButton(self.name_normalizer_top_frame, text="Browse",
                                              command=self.browse_input)
        self.nn_browse_button.grid(row=0, column=0, padx=5, pady=5)

        # Path Entry
        self.nn_path_entry = ctk.CTkEntry(self.name_normalizer_top_frame, width=890)
        self.nn_path_entry.insert(0, "Select a folder or file to normalize using the 'Browse' button...")
        self.nn_path_entry.grid(row=0, column=1, padx=10, pady=10)

        # Button Frame 1
        self.checkbox_frame1 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame1.grid(row=2, column=0, padx=10, pady=5)

        # Checkbox to enable/disable Append '__-__ ' to the file name
        self.tail_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                             text="Append '__-__ '",
                                             variable=self.tail_var)
        self.tail_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove all symbols ,;:@$%^&#*+=(){}[]|\<>'"?_-–—
        self.remove_all_symbols_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                                           text="Remove all symbols",
                                                           variable=self.remove_all_symbols_var)
        self.remove_all_symbols_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove most symbols ,;:@$%^&*+={}[]|\<>"?-–—
        self.remove_most_symbols_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                                            text="Remove most symbols",
                                                            variable=self.remove_most_symbols_var)
        self.remove_most_symbols_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove non-ascii symbols
        self.remove_non_ascii_symbols_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                                                 text="Remove non-ASCII symbols",
                                                                 variable=self.remove_non_ascii_symbols_var)
        self.remove_non_ascii_symbols_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove numbers
        self.remove_numbers_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                                       text="Remove numbers",
                                                       variable=self.remove_number_var)
        self.remove_numbers_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Button Frame 2
        self.checkbox_frame2 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame2.grid(row=3, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove dashes
        self.remove_dash_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                    text="Remove dashes",
                                                    variable=self.remove_dash_var)
        self.remove_dash_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove endashes
        self.remove_endash_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                      text="Remove endashes",
                                                      variable=self.remove_endash_var)
        self.remove_endash_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove emdashes
        self.remove_emdash_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                      text="Remove emdashes",
                                                      variable=self.remove_emdash_var)
        self.remove_emdash_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove hashtags
        self.remove_hashtag_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                       text="Remove hashtags",
                                                       variable=self.remove_hashtag_var)
        self.remove_hashtag_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove commas
        self.remove_comma_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                     text="Remove commas",
                                                     variable=self.remove_comma_var)
        self.remove_comma_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Checkbox to enable/disable remove parenthesis and trailing text
        self.remove_parenthesis_trail_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                                 text="( onward",
                                                                 variable=self.remove_parenthesis_trail_var)
        self.remove_parenthesis_trail_checkbox.grid(row=0, column=5, padx=10, pady=10)

        # Button Frame 3
        self.checkbox_frame3 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame3.grid(row=4, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove ampersands
        self.remove_ampersand_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                         text="Remove &",
                                                         variable=self.remove_ampersand_var)
        self.remove_ampersand_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove @
        self.remove_at_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                  text="Remove @",
                                                  variable=self.remove_at_var)
        self.remove_at_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove underscores
        self.remove_underscore_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                          text="Remove underscores",
                                                          variable=self.remove_underscore_var)
        self.remove_underscore_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove single quotes
        self.remove_single_quote_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                            text="Remove single quotes",
                                                            variable=self.remove_single_quote_var)
        self.remove_single_quote_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove double quotes
        self.remove_double_quote_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                            text="Remove double quotes",
                                                            variable=self.remove_double_quote_var)
        self.remove_double_quote_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Checkbox to enable/disable remove hashtag and trailing text
        self.remove_hashtag_trail_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                             text="# onward",
                                                             variable=self.remove_hashtag_trail_var)
        self.remove_hashtag_trail_checkbox.grid(row=0, column=5, padx=10, pady=10)

        # Button Frame 4
        self.checkbox_frame4 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame4.grid(row=5, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove dollars
        self.remove_dollar_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                      text="Remove dollars",
                                                      variable=self.remove_dollar_var)
        self.remove_dollar_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove colons
        self.remove_colon_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                     text="Remove colons",
                                                     variable=self.remove_colon_var)
        self.remove_colon_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable semicolons
        self.remove_semicolon_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                         text="Remove semicolons",
                                                         variable=self.remove_semicolon_var)
        self.remove_semicolon_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove percents
        self.remove_percent_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                       text="Remove percents",
                                                       variable=self.remove_percent_var)
        self.remove_percent_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove carets
        self.remove_caret_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                     text="Remove carets",
                                                     variable=self.remove_caret_var)
        self.remove_caret_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Checkbox to enable/disable remove plus signs
        self.remove_plus_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                    text="Remove plus signs",
                                                    variable=self.remove_plus_var)
        self.remove_plus_checkbox.grid(row=0, column=5, padx=10, pady=10)

        # Button Frame 5
        self.checkbox_frame5 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame5.grid(row=6, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove asterisks
        self.remove_asterisk_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                        text="Remove asterisks",
                                                        variable=self.remove_asterisk_var)
        self.remove_asterisk_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove parenthesis
        self.remove_parenthesis_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                           text="Remove parenthesis",
                                                           variable=self.remove_parenthesis_var)
        self.remove_parenthesis_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove angle brackets
        self.remove_angle_bracket_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                             text="Remove angle brackets",
                                                             variable=self.remove_angle_bracket_var)
        self.remove_angle_bracket_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove curly braces
        self.remove_curly_brace_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                           text="Remove curly braces",
                                                           variable=self.remove_curly_brace_var)
        self.remove_curly_brace_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove square brackets
        self.remove_square_bracket_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                              text="Remove square brackets",
                                                              variable=self.remove_square_bracket_var)
        self.remove_square_bracket_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Button Frame 6
        self.checkbox_frame6 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame6.grid(row=7, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove pipes
        self.remove_pipe_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                    text="Remove pipes",
                                                    variable=self.remove_pipe_var)
        self.remove_pipe_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove backslashes
        self.remove_backslash_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                         text="Remove backslashes",
                                                         variable=self.remove_backslash_var)
        self.remove_backslash_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove equal signs
        self.remove_equal_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                     text="Remove equal signs",
                                                     variable=self.remove_equal_var)
        self.remove_equal_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove question marks
        self.remove_question_mark_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                             text="Remove question marks",
                                                             variable=self.remove_question_mark_var)
        self.remove_question_mark_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove custom text
        self.remove_custom_text_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                           text="Replace custom text",
                                                           variable=self.remove_custom_text_var)
        self.remove_custom_text_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Button Frame 7
        self.checkbox_frame7 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame7.grid(row=8, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove extra whitespace
        self.remove_extra_whitespace_checkbox = ctk.CTkCheckBox(self.checkbox_frame7,
                                                                text="Remove extra spaces",
                                                                variable=self.remove_extra_whitespace_var)
        self.remove_extra_whitespace_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable Titlefy the name
        self.title_checkbox = ctk.CTkCheckBox(self.checkbox_frame7,
                                              text="Titlefy",
                                              variable=self.title_var)
        self.title_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable Artist Identifier
        self.artist_identifier_checkbox = ctk.CTkCheckBox(self.checkbox_frame7,
                                                          text="Artist Identifier",
                                                          variable=self.artist_identifier_var)
        self.artist_identifier_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable include subdirectories
        self.deep_walk_checkbox = ctk.CTkCheckBox(self.checkbox_frame7,
                                                  text="Subdirectories",
                                                  variable=self.deep_walk_var)
        self.deep_walk_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable reset entries
        self.reset_checkbox = ctk.CTkCheckBox(self.checkbox_frame7,
                                              text="Reset entries",
                                              variable=self.reset_var)
        self.reset_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Switch to enable/disable replace mode (case-sensitive vs case-insensitive)
        self.replace_mode_switch = ctk.CTkSwitch(self.checkbox_frame7, text="Case sensitive/insensitive",
                                                 variable=self.replace_mode_var)
        self.replace_mode_switch.grid(row=0, column=5, padx=10)

        # String frame
        self.string_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                         fg_color="transparent")
        self.string_frame.grid(row=9, column=0, padx=10, pady=5)

        # Prefix Label
        self.prefix_label = ctk.CTkLabel(self.string_frame, text="Prefix:")
        self.prefix_label.grid(row=1, column=0, padx=10, pady=10)

        # Prefix Entry
        self.prefix_entry = ctk.CTkEntry(self.string_frame, width=140)
        self.prefix_entry.grid(row=1, column=1, padx=10, pady=10)

        # Suffix Label
        self.suffix_label = ctk.CTkLabel(self.string_frame, text="Suffix:")
        self.suffix_label.grid(row=1, column=2, padx=10, pady=10)

        # Suffix Entry
        self.suffix_entry = ctk.CTkEntry(self.string_frame, width=140)
        self.suffix_entry.grid(row=1, column=3, padx=10, pady=10)

        # Replace Label
        self.replace_label = ctk.CTkLabel(self.string_frame, text="Replace (Original, Replacement):")
        self.replace_label.grid(row=1, column=4, padx=10, pady=10)

        # Original Entry
        self.original_entry = ctk.CTkEntry(self.string_frame, width=150)
        self.original_entry.grid(row=1, column=5, padx=10, pady=10)

        # Replace Entry
        self.replace_entry = ctk.CTkEntry(self.string_frame, width=150)
        self.replace_entry.grid(row=1, column=10, pady=10)

        # Output directory move frame
        self.output_directory_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.output_directory_frame.grid(row=10, column=0, padx=10, pady=5)

        # Browse move directory folder button
        self.browse_move_directory_button = ctk.CTkButton(self.output_directory_frame, text="Output Directory",
                                                          command=self.browse_output_directory)
        self.browse_move_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Move directory entry
        self.move_directory_entry = ctk.CTkEntry(self.output_directory_frame, width=400)
        self.move_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Custom Text Removal Label
        self.custom_text_label = ctk.CTkLabel(self.output_directory_frame, text="Remove:")
        self.custom_text_label.grid(row=0, column=2, padx=10, pady=10)

        # Custom Text Removal Entry
        self.custom_text_removal_entry = ctk.CTkEntry(self.output_directory_frame, width=385)
        self.custom_text_removal_entry.grid(row=0, column=3, padx=10, pady=10)

        # Normalize Folder frame
        self.normalize_folder_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.normalize_folder_frame.grid(row=11, column=0, padx=10, pady=5)

        # Clear Name Normalizer Selection Button
        self.clear_name_normalizer_selection_button = ctk.CTkButton(self.normalize_folder_frame,
                                                                    text="Clear",
                                                                    command=lambda: self.clear_selection(
                                                                        frame_name="name_normalizer_window"))
        self.clear_name_normalizer_selection_button.grid(row=0, column=0, padx=10, pady=10)

        # Undo Name Normalizer Button
        self.undo_nn_button = ctk.CTkButton(self.normalize_folder_frame,
                                            text="Undo Name Normalizer",
                                            command=self.undo_file_rename)
        self.undo_nn_button.grid(row=0, column=1, padx=10, pady=10)

        # Select Name Normalizer Last Used File Button
        self.name_normalizer_last_used_file_button = ctk.CTkButton(self.normalize_folder_frame,
                                                                   text="Reload Last File",
                                                                   command=self.load_last_used_file)
        self.name_normalizer_last_used_file_button.grid(row=0, column=2, padx=10, pady=10)

        # Normalize Preview button
        self.normalize_preview_button = ctk.CTkButton(self.normalize_folder_frame, text="Preview",
                                                      command=lambda: self.process_name_normalizer(mode="preview"))
        self.normalize_preview_button.grid(row=0, column=3, padx=5, pady=5)

        # Interrupt button
        self.interrupt_button = ctk.CTkButton(self.normalize_folder_frame, text="Interrupt",
                                              command=lambda: self.interrupt_processing("name_processing_thread"))
        self.interrupt_button.grid(row=0, column=4, padx=5, pady=5)

        # Normalize button
        self.normalize_button = ctk.CTkButton(self.normalize_folder_frame, text="Normalize",
                                              command=lambda: self.process_name_normalizer(mode="action"))
        self.normalize_button.grid(row=0, column=5, padx=5, pady=5)

        # Send to Module frame
        self.send_to_module_frame1 = ctk.CTkFrame(self.name_normalizer_frame,
                                                  corner_radius=0,
                                                  fg_color="transparent")
        self.send_to_module_frame1.grid(row=12, column=0, padx=5)

        # Send to File Renamer button
        self.send_to_file_renamer_button1 = ctk.CTkButton(self.send_to_module_frame1, text="Send to File Renamer",
                                                          command=lambda: self.send_to_module(
                                                              destination="file_renamer_module"))
        self.send_to_file_renamer_button1.grid(row=0, column=0, padx=10, pady=10)

        # Send to Video Editor button
        self.send_to_video_editor_button1 = ctk.CTkButton(self.send_to_module_frame1, text="Send to Video Editor",
                                                          command=lambda: self.send_to_module(
                                                              destination="video_editor_module"))
        self.send_to_video_editor_button1.grid(row=0, column=1, padx=10, pady=10)

        # Frame to display messages on the Name Normalizer frame
        self.name_normalizer_message_label_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                                                fg_color="transparent")
        self.name_normalizer_message_label_frame.grid(row=13, column=0, padx=10)

        # Name Normalizer message Label
        self.name_normalizer_message_label = ctk.CTkLabel(self.name_normalizer_message_label_frame, text="")
        self.name_normalizer_message_label.grid(row=0, column=0, padx=10, pady=10)

        # Progressbar frame
        self.slider_progressbar_frame = ctk.CTkFrame(self.name_normalizer_message_label_frame,
                                                     corner_radius=0,
                                                     fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=0, padx=10)
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)

        """
        video_editor_window
        """
        # Create Video Editor frame
        self.video_editor_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.video_editor_frame.grid_columnconfigure(0, weight=1)

        # Video Editor Label
        self.video_editor_label = ctk.CTkLabel(self.video_editor_frame, text="Video Editor",
                                               font=ctk.CTkFont(size=15, weight="bold"))
        self.video_editor_label.grid(row=0, column=0, padx=10, pady=10)

        # Video Editor Top frame
        self.video_editor_top_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.video_editor_top_frame.grid(row=1, column=0, padx=10, pady=5)

        # Video Editor browse input method button
        self.browse_input_method_button = ctk.CTkButton(self.video_editor_top_frame, text="Browse",
                                                        command=self.browse_input)
        self.browse_input_method_button.grid(row=0, column=0, padx=5, pady=5)

        # Input method entry for a file, directory, or .txt containing a line delimited list of files to process
        self.input_method_entry = ctk.CTkEntry(self.video_editor_top_frame, width=890)
        self.input_method_entry.insert(0, "Select a video to edit using the 'Browse' button...")
        self.input_method_entry.grid(row=0, column=1, padx=10, pady=10)

        # Rotation frame
        self.rotation_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                           fg_color="transparent")
        self.rotation_frame.grid(row=3, column=0, padx=10, pady=5)

        # Rotate Video label
        self.rotation_label = ctk.CTkLabel(self.rotation_frame, text="Rotate Video:")
        self.rotation_label.grid(row=0, column=0, padx=10, pady=5)

        # Variable to store rotation option
        self.rotation_var = ctk.StringVar()
        self.rotation_var.set(self.default_rotation_var)

        # Left rotation radio button
        self.left_radio = ctk.CTkRadioButton(self.rotation_frame, text="Left", variable=self.rotation_var, value="left")
        self.left_radio.grid(row=0, column=1, padx=10, pady=5)

        # Right rotation radio button
        self.right_radio = ctk.CTkRadioButton(self.rotation_frame, text="Right", variable=self.rotation_var,
                                              value="right")
        self.right_radio.grid(row=0, column=2, padx=10, pady=5)

        # Flip rotation radio button
        self.flip_radio = ctk.CTkRadioButton(self.rotation_frame, text="Flip", variable=self.rotation_var,
                                             value="flip")
        self.flip_radio.grid(row=0, column=3, padx=10, pady=5)

        # Mirror rotation radio button
        self.mirror_radio = ctk.CTkRadioButton(self.rotation_frame, text="Mirror", variable=self.rotation_var,
                                               value="mirror")
        self.mirror_radio.grid(row=0, column=4, padx=10, pady=5)

        # None rotation radio button
        self.no_rotation_radio = ctk.CTkRadioButton(self.rotation_frame, text="None", variable=self.rotation_var,
                                                    value="none")
        self.no_rotation_radio.grid(row=0, column=5, padx=10, pady=5)

        # Decibel frame
        self.decibel_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                          fg_color="transparent")
        self.decibel_frame.grid(row=4, column=0, padx=10, pady=5)

        # Increase Audio (dB) label
        self.decibel_label = ctk.CTkLabel(self.decibel_frame, text="Increase Audio (dB):")
        self.decibel_label.grid(row=0, column=0, padx=10, pady=5)

        # Initialize decibel variable
        self.decibel_var = ctk.StringVar()
        self.decibel_var.set(self.default_decibel)

        # Trace the changes in the StringVar
        self.decibel_var.trace_add("write",
                                   lambda name, index, mode, var=self.decibel_var, default=self.default_decibel,
                                          desired_type=float: self.validate_entry(var, default, desired_type))

        # Decibel entry
        self.decibel_entry = ctk.CTkEntry(self.decibel_frame, textvariable=self.decibel_var, width=50)
        self.decibel_entry.grid(row=0, column=1, padx=10, pady=10)

        # Audio Normalization frame
        self.audio_normalization_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                      fg_color="transparent")
        self.audio_normalization_frame.grid(row=5, column=0, padx=10, pady=5)

        # Normalize Audio label
        self.audio_normalization_label = ctk.CTkLabel(self.audio_normalization_frame, text="Normalize Audio:")
        self.audio_normalization_label.grid(row=0, column=0, padx=10, pady=5)

        # Initialize audio normalization variable
        self.audio_normalization_var = ctk.StringVar()
        self.audio_normalization_var.set(self.default_audio_normalization)

        # Trace the changes in the StringVar
        self.audio_normalization_var.trace_add("write",
                                               lambda name, index, mode, var=self.audio_normalization_var,
                                                      default=self.default_audio_normalization,
                                                      desired_type=float: self.validate_entry(var, default,
                                                                                              desired_type))

        # Audio Normalization entry
        self.audio_normalization_entry = ctk.CTkEntry(self.audio_normalization_frame,
                                                      textvariable=self.audio_normalization_var,
                                                      width=50)
        self.audio_normalization_entry.grid(row=0, column=1, padx=10, pady=10)

        # Trim frame
        self.trim_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                       fg_color="transparent")
        self.trim_frame.grid(row=6, column=0, padx=10, pady=5)

        # Trim label
        self.trim_label = ctk.CTkLabel(self.trim_frame, text="Trim (Minutes:Seconds):")
        self.trim_label.grid(row=0, column=0, padx=10, pady=5)

        # Initialize minute variable
        self.minute_var = ctk.StringVar()
        self.minute_var.set(self.default_minute)

        # Trace the changes in the StringVar
        self.minute_var.trace_add("write",
                                  lambda name, index, mode, var=self.minute_var, default=self.default_minute,
                                         desired_type=int: self.validate_entry(var, default, desired_type))

        # Minute entry
        self.minute_entry = ctk.CTkEntry(self.trim_frame, textvariable=self.minute_var, width=50)
        self.minute_entry.grid(row=0, column=1, padx=10, pady=10)

        # Trim label
        self.colon_label = ctk.CTkLabel(self.trim_frame, text=":")
        self.colon_label.grid(row=0, column=2)

        # Initialize second variable
        self.second_var = ctk.StringVar()
        self.second_var.set(self.default_second)

        # Trace the changes in the StringVar
        self.second_var.trace_add("write",
                                  lambda name, index, mode, var=self.second_var, default=self.default_second,
                                         desired_type=int: self.validate_entry(var, default, desired_type))

        # Second entry
        self.second_entry = ctk.CTkEntry(self.trim_frame, textvariable=self.second_var, width=50)
        self.second_entry.grid(row=0, column=3, padx=10, pady=10)

        # Trim label
        self.trim_label1 = ctk.CTkLabel(self.trim_frame, text="-")
        self.trim_label1.grid(row=0, column=4, padx=10, pady=5)

        # Initialize minute variable1
        self.minute_var1 = ctk.StringVar()
        self.minute_var1.set(self.default_minute)

        # Trace the changes in the StringVar
        self.minute_var1.trace_add("write",
                                   lambda name, index, mode, var=self.minute_var1, default=self.default_minute,
                                          desired_type=int: self.validate_entry(var, default, desired_type))

        # Minute entry1
        self.minute_entry1 = ctk.CTkEntry(self.trim_frame, textvariable=self.minute_var1, width=50)
        self.minute_entry1.grid(row=0, column=5, padx=10, pady=10)

        # Trim label1
        self.colon_label1 = ctk.CTkLabel(self.trim_frame, text=":")
        self.colon_label1.grid(row=0, column=6)

        # Initialize second variable
        self.second_var1 = ctk.StringVar()
        self.second_var1.set(self.default_second)

        # Trace the changes in the StringVar
        self.second_var1.trace_add("write",
                                   lambda name, index, mode, var=self.second_var1, default=self.default_second,
                                          desired_type=int: self.validate_entry(var, default, desired_type))

        # Second entry1
        self.second_entry1 = ctk.CTkEntry(self.trim_frame, textvariable=self.second_var1, width=50)
        self.second_entry1.grid(row=0, column=7, padx=10, pady=10)

        # Video Editor Output directory frame
        self.video_editor_output_directory_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                                fg_color="transparent")
        self.video_editor_output_directory_frame.grid(row=8, column=0, padx=10, pady=5)

        # Browse video editor output directory folder button
        self.browse_video_editor_output_directory_button = ctk.CTkButton(self.video_editor_output_directory_frame,
                                                                         text="Output Directory",
                                                                         command=self.browse_output_directory)
        self.browse_video_editor_output_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Video editor output directory entry
        self.video_editor_output_directory_entry = ctk.CTkEntry(self.video_editor_output_directory_frame, width=890)
        self.video_editor_output_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Process video editor frame
        self.process_video_editor_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                       fg_color="transparent")
        self.process_video_editor_frame.grid(row=9, column=0, padx=10, pady=5)

        # Clear process video editor Button
        self.clear_video_editor_selection_button = ctk.CTkButton(self.process_video_editor_frame,
                                                                 text="Clear",
                                                                 command=lambda: self.clear_selection(
                                                                     frame_name="video_editor_window"))
        self.clear_video_editor_selection_button.grid(row=0, column=0, padx=10, pady=10)

        # Select Video Editor Last Used File Button
        self.video_editor_last_used_file_button = ctk.CTkButton(self.process_video_editor_frame,
                                                                text="Reload Last File",
                                                                command=self.load_last_used_file)
        self.video_editor_last_used_file_button.grid(row=0, column=1, padx=10, pady=10)

        # Interrupt button1
        self.interrupt_button1 = ctk.CTkButton(self.process_video_editor_frame, text="Interrupt",
                                               command=lambda: self.interrupt_processing("video_processing_thread"))
        self.interrupt_button1.grid(row=0, column=2, padx=5, pady=5)

        # Process video button
        self.process_video_edits_button = ctk.CTkButton(self.process_video_editor_frame, text="Process video(s)",
                                                        command=self.gather_and_validate_entries)
        self.process_video_edits_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame to display messages on the video editor frame
        self.send_to_module_frame2 = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                  fg_color="transparent")
        self.send_to_module_frame2.grid(row=10, column=0, padx=10)

        # Send to File Renamer button
        self.send_to_file_renamer_button = ctk.CTkButton(self.send_to_module_frame2, text="Send to File Renamer",
                                                         command=lambda: self.send_to_module(
                                                             destination="file_renamer_module"))
        self.send_to_file_renamer_button.grid(row=0, column=0, padx=10, pady=10)

        # Send to Name Normalizer button
        self.send_to_name_normalizer_button1 = ctk.CTkButton(self.send_to_module_frame2,
                                                             text="Send to Name Normalizer",
                                                             command=lambda: self.send_to_module(
                                                                 destination="name_normalizer_module"))
        self.send_to_name_normalizer_button1.grid(row=0, column=1, padx=10, pady=10)

        # Video editor checkbox frame
        self.video_editor_checkbox_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                        fg_color="transparent")
        self.video_editor_checkbox_frame.grid(row=11, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove successful lines
        self.remove_successful_lines_checkbox = ctk.CTkCheckBox(self.video_editor_checkbox_frame,
                                                                text="Remove successful lines from input file",
                                                                variable=self.remove_successful_lines_var)
        self.remove_successful_lines_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable reset video editor entries
        self.reset_video_checkbox = ctk.CTkCheckBox(self.video_editor_checkbox_frame,
                                                    text="Reset entries",
                                                    variable=self.reset_video_entries_var)
        self.reset_video_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Frame to display messages on the video editor frame
        self.video_editor_message_label_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                             fg_color="transparent")
        self.video_editor_message_label_frame.grid(row=12, column=0, padx=10)

        # Video editor message Label
        self.video_editor_message_label = ctk.CTkLabel(self.video_editor_message_label_frame, text="")
        self.video_editor_message_label.grid(row=0, column=0, padx=10, pady=10)

        # Progressbar frame1
        self.slider_progressbar_frame1 = ctk.CTkFrame(self.video_editor_message_label_frame,
                                                      corner_radius=0,
                                                      fg_color="transparent")
        self.slider_progressbar_frame1.grid(row=1, column=0, padx=10)
        self.slider_progressbar_frame1.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame1.grid_rowconfigure(4, weight=1)

        """
        add_remove_window
        """
        # Create Add/Remove frame
        self.add_remove_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.add_remove_frame.grid_columnconfigure(0, weight=1)

        # Add/Remove Label
        self.add_remove_label = ctk.CTkLabel(self.add_remove_frame, text="Add/Remove",
                                             font=ctk.CTkFont(size=15, weight="bold"))
        self.add_remove_label.grid(row=0, column=0, padx=10, pady=10)

        # Create an add_remove_tabview on add_remove_frame row 1
        self.add_remove_tabview, self.add_remove_tabs = self.create_tabview(self.add_remove_frame,
                                                                            self.add_remove_tab_names,
                                                                            self.default_add_remove_tab)

        """Artist Tab"""
        # Add and remove artist top frame
        self.add_remove_artist_top_frame = ctk.CTkFrame(self.add_remove_tabs.get("Artist"), corner_radius=0,
                                                        fg_color="transparent")
        self.add_remove_artist_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Add and remove artist label frame
        self.add_remove_artist_label_frame = ctk.CTkFrame(self.add_remove_artist_top_frame, corner_radius=0,
                                                          fg_color="transparent")
        self.add_remove_artist_label_frame.grid(row=0, column=0, padx=10, pady=10)

        # Add/Remove Artist Label
        self.add_remove_artist_label = ctk.CTkLabel(self.add_remove_artist_label_frame, text="Add/Remove Artist",
                                                    font=ctk.CTkFont(size=15, weight="bold"))
        self.add_remove_artist_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Add and remove artist entry frame
        self.add_remove_artist_entry_frame = ctk.CTkFrame(self.add_remove_artist_top_frame, corner_radius=0,
                                                          fg_color="transparent")
        self.add_remove_artist_entry_frame.grid(row=1, column=0, padx=10, pady=10)

        # Add artist button
        self.add_artist_button = ctk.CTkButton(self.add_remove_artist_entry_frame, text="Add Artist",
                                               command=self.add_artist_to_file)
        self.add_artist_button.grid(row=0, column=0, padx=5)

        # Add artist entry
        self.add_artist_entry = ctk.CTkEntry(self.add_remove_artist_entry_frame, width=370)
        self.add_artist_entry.grid(row=0, column=1, padx=5)

        # Remove artist button
        self.remove_artist_button = ctk.CTkButton(self.add_remove_artist_entry_frame, text="Remove Artist",
                                                  command=self.remove_artist_from_file)
        self.remove_artist_button.grid(row=0, column=2, padx=5, pady=5)

        # Remove artist entry
        self.remove_artist_entry = ctk.CTkEntry(self.add_remove_artist_entry_frame, width=370)
        self.remove_artist_entry.grid(row=0, column=3, padx=5)

        # Add and remove artist checkbox frame
        self.auto_add_acc_record_frame = ctk.CTkFrame(self.add_remove_artist_top_frame, corner_radius=0,
                                                      fg_color="transparent")
        self.auto_add_acc_record_frame.grid(row=2, column=0, padx=10, pady=10)

        # Checkbox to enable/disable automatically add artist record for common categories
        self.auto_add_acc_record_checkbox = ctk.CTkCheckBox(self.auto_add_acc_record_frame,
                                                            text="Automatically add record for Common Categories",
                                                            variable=self.auto_add_acc_record_var)
        self.auto_add_acc_record_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Add and remove artist label frame
        self.add_remove_acc_record_label_frame = ctk.CTkFrame(self.add_remove_artist_top_frame, corner_radius=0,
                                                              fg_color="transparent")
        self.add_remove_acc_record_label_frame.grid(row=3, column=0, padx=10, pady=10)

        # Add/Remove Artist Label
        self.add_remove_acc_record_label = ctk.CTkLabel(self.add_remove_acc_record_label_frame,
                                                        text="Add/Remove Artist "
                                                             "Common Categories "
                                                             "Record",
                                                        font=ctk.CTkFont(size=15, weight="bold"))
        self.add_remove_acc_record_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Add and remove artist entry frame
        self.add_remove_acc_record_entry_frame = ctk.CTkFrame(self.add_remove_artist_top_frame, corner_radius=0,
                                                              fg_color="transparent")
        self.add_remove_acc_record_entry_frame.grid(row=4, column=0, padx=10, pady=10)

        # Add artist button
        self.add_acc_record_button = ctk.CTkButton(self.add_remove_acc_record_entry_frame, text="Add Artist C.C.",
                                                   command=self.add_artist_to_common_categories_dictionary)
        self.add_acc_record_button.grid(row=0, column=0, padx=5)

        # Add artist entry
        self.add_acc_record_entry = ctk.CTkEntry(self.add_remove_acc_record_entry_frame, width=370)
        self.add_acc_record_entry.grid(row=0, column=1, padx=5)

        # Remove artist button
        self.remove_acc_record_button = ctk.CTkButton(self.add_remove_acc_record_entry_frame, text="Remove Artist C.C.",
                                                      command=self.remove_artist_from_common_categories_dictionary)
        self.remove_acc_record_button.grid(row=0, column=2, padx=5, pady=5)

        # Remove artist entry
        self.remove_acc_record_entry = ctk.CTkEntry(self.add_remove_acc_record_entry_frame, width=370)
        self.remove_acc_record_entry.grid(row=0, column=3, padx=5)

        # Add/Remove artist common categories label frame
        self.add_remove_acc_label_frame = ctk.CTkFrame(self.add_remove_artist_top_frame, corner_radius=0,
                                                       fg_color="transparent")
        self.add_remove_acc_label_frame.grid(row=5, column=0, padx=10, pady=10)

        # Add/Remove artist common categories Label
        self.add_remove_acc_label = ctk.CTkLabel(self.add_remove_acc_label_frame, text="Add/Remove Artist "
                                                                                       "Common Categories",
                                                 font=ctk.CTkFont(size=15, weight="bold"))
        self.add_remove_acc_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Browse frame for artist common categories
        self.acc_browse_frame = ctk.CTkFrame(self.add_remove_artist_top_frame, corner_radius=0,
                                             fg_color="transparent")
        self.acc_browse_frame.grid(row=6, column=0, padx=10, pady=10)

        # Browse artist common categories button
        self.browse_artist_button = ctk.CTkButton(self.acc_browse_frame, text="Browse Artist",
                                                  command=lambda: self.browse_artist(mode="Browse"))
        self.browse_artist_button.grid(row=0, column=0, padx=5)

        # Artist Common Categories Display
        self.acc_display_text = ctk.StringVar()
        self.acc_display_text.set("Select an Artist using the 'Browse Artist' button...")
        self.acc_display_entry = ctk.CTkEntry(self.acc_browse_frame, width=900,
                                              textvariable=self.acc_display_text)
        self.acc_display_entry.grid(row=0, column=1, padx=5)

        # Detect artist button
        self.detect_artist_button = ctk.CTkButton(self.acc_browse_frame, text="Detect Artist",
                                                  command=lambda: self.browse_artist(mode="Detect"))
        self.detect_artist_button.grid(row=1, column=0, padx=5, pady=10)

        # Add and remove artist common categories entry frame
        self.add_remove_acc_entry_frame = ctk.CTkFrame(self.add_remove_artist_top_frame, corner_radius=0,
                                                       fg_color="transparent")
        self.add_remove_acc_entry_frame.grid(row=7, column=0, padx=10, pady=10)

        # Add artist common categories button
        self.add_acc_button = ctk.CTkButton(self.add_remove_acc_entry_frame, text="Add A.C.C.",
                                            command=self.add_artist_common_category)
        self.add_acc_button.grid(row=0, column=0, padx=5)

        # Add artist common categories entry
        self.add_acc_entry = ctk.CTkEntry(self.add_remove_acc_entry_frame, width=370)
        self.add_acc_entry.grid(row=0, column=1, padx=5)

        # Remove artist common categories button
        self.remove_acc_button = ctk.CTkButton(self.add_remove_acc_entry_frame, text="Remove A.C.C.",
                                               command=self.remove_artist_common_category)
        self.remove_acc_button.grid(row=0, column=2, padx=5, pady=5)

        # Remove artist common categories entry
        self.remove_acc_entry = ctk.CTkEntry(self.add_remove_acc_entry_frame, width=370)
        self.remove_acc_entry.grid(row=0, column=3, padx=5)

        """Category Tab"""
        self.category_frame = ctk.CTkFrame(self.add_remove_tabs.get("Category"), corner_radius=0,
                                           fg_color="transparent")
        self.category_frame.grid(row=3, column=0, padx=10, pady=10)

        # Add Category Button
        self.add_category_button = ctk.CTkButton(self.category_frame, text="Add Category", command=self.add_category)
        self.add_category_button.grid(row=0, column=0, padx=5)

        # Add Category Entry
        self.category_entry = ctk.CTkEntry(self.category_frame, width=310)
        self.category_entry.grid(row=0, column=1, padx=5)

        # Weight Label
        self.weight_label = ctk.CTkLabel(self.category_frame, text="Weight:")
        self.weight_label.grid(row=0, column=2, padx=5)

        # Initialize weight variable
        self.weight_var = ctk.StringVar()
        self.weight_var.set(self.default_weight)

        # Trace the changes in the StringVar
        self.weight_var.trace_add("write",
                                  lambda name, index, mode, var=self.weight_var, default=self.default_weight,
                                         desired_type=int: self.validate_entry(var, default, desired_type))

        # Weight Entry
        self.weight_entry = ctk.CTkEntry(self.category_frame, textvariable=self.weight_var, width=35)
        self.weight_entry.grid(row=0, column=3, padx=5)

        # Remove Category Button
        self.remove_category_button = ctk.CTkButton(self.category_frame, text="Remove Category",
                                                    command=self.remove_category)
        self.remove_category_button.grid(row=0, column=4, padx=5)

        # Remove Category Entry
        self.remove_category_entry = ctk.CTkEntry(self.category_frame, width=310)
        self.remove_category_entry.grid(row=0, column=5, padx=5)

        """Custom Tab Name Tab"""
        self.ctn_frame = ctk.CTkFrame(self.add_remove_tabs.get("Custom Tab Name"), corner_radius=0,
                                      fg_color="transparent")
        self.ctn_frame.grid(row=6, column=0, padx=10, pady=10)

        # Add Custom Tab Name Button
        self.add_ctn_button = ctk.CTkButton(self.ctn_frame, text="Add Custom Tab", command=self.add_custom_tab_name)
        self.add_ctn_button.grid(row=0, column=0, padx=5)

        # Add Custom Tab Name Entry
        self.custom_tab_name_entry = ctk.CTkEntry(self.ctn_frame, width=310)
        self.custom_tab_name_entry.grid(row=0, column=1, padx=5)

        # Weight1 Label
        self.weight_label1 = ctk.CTkLabel(self.ctn_frame, text="Weight:")
        self.weight_label1.grid(row=0, column=2, padx=5)

        # Initialize weight variable
        self.weight_var1 = ctk.StringVar()
        self.weight_var1.set(self.default_ctn_weight)

        # Trace the changes in the StringVar
        self.weight_var1.trace_add("write",
                                   lambda name, index, mode, var=self.weight_var1, default=self.default_ctn_weight,
                                          desired_type=int: self.validate_entry(var, default, desired_type))

        # Weight Entry1
        self.weight_entry1 = ctk.CTkEntry(self.ctn_frame, textvariable=self.weight_var1, width=35)
        self.weight_entry1.grid(row=0, column=3, padx=5)

        # Remove Custom Tab Name Button
        self.remove_ctn_button = ctk.CTkButton(self.ctn_frame, text="Remove Custom Tab",
                                               command=self.remove_custom_tab_name)
        self.remove_ctn_button.grid(row=0, column=4, padx=5)

        # Remove Custom Tab Name Entry
        self.remove_custom_tab_name_entry = ctk.CTkEntry(self.ctn_frame, width=310)
        self.remove_custom_tab_name_entry.grid(row=0, column=5, padx=5)

        """Custom Text to Replace Tab"""
        # Custom Text to Replace frame
        self.ctr_entry_frame = ctk.CTkFrame(self.add_remove_tabs.get("Custom Text to Replace"), corner_radius=0,
                                            fg_color="transparent")
        self.ctr_entry_frame.grid(row=12, column=0, padx=10, pady=10)

        # Add ctr button
        self.add_ctr_button = ctk.CTkButton(self.ctr_entry_frame, text="Add CTR",
                                            command=self.add_custom_text_to_replace)
        self.add_ctr_button.grid(row=0, column=0, padx=5)

        # Add ctr entry
        self.add_ctr_name_entry = ctk.CTkEntry(self.ctr_entry_frame, width=370)
        self.add_ctr_name_entry.grid(row=0, column=1, padx=5, pady=10)

        # Replacement Label
        self.replacement_label = ctk.CTkLabel(self.ctr_entry_frame, text="Replace with:")
        self.replacement_label.grid(row=0, column=2, padx=5, pady=10)

        # Replacement text entry
        self.replacement_text_entry = ctk.CTkEntry(self.ctr_entry_frame, width=100)
        self.replacement_text_entry.grid(row=0, column=3, padx=5, pady=10)

        # Remove ctr button
        self.remove_ctr_button = ctk.CTkButton(self.ctr_entry_frame, text="Remove CTR",
                                               command=self.remove_custom_text_to_replace)
        self.remove_ctr_button.grid(row=1, column=0, padx=5)

        # Remove ctr entry
        self.remove_ctr_name_entry = ctk.CTkEntry(self.ctr_entry_frame, width=370)
        self.remove_ctr_name_entry.grid(row=1, column=1, padx=5)

        """Exclude Tab"""
        # Exclude frame
        self.exclude_entry_frame = ctk.CTkFrame(self.add_remove_tabs.get("Exclude"), corner_radius=0,
                                                fg_color="transparent")
        self.exclude_entry_frame.grid(row=10, column=0, padx=10, pady=10)

        # Add Exclude button
        self.add_exclude_button = ctk.CTkButton(self.exclude_entry_frame, text="Add Exclude",
                                                command=self.add_folder_to_excluded_folders)
        self.add_exclude_button.grid(row=0, column=0, padx=5)

        # Add Exclude entry
        self.add_exclude_name_entry = ctk.CTkEntry(self.exclude_entry_frame, width=370)
        self.add_exclude_name_entry.grid(row=0, column=1, padx=5)

        # Remove Exclude button
        self.remove_exclude_button = ctk.CTkButton(self.exclude_entry_frame, text="Remove Exclude",
                                                   command=self.remove_folder_from_excluded_folders)
        self.remove_exclude_button.grid(row=0, column=3, padx=5)

        # Remove Exclude entry
        self.remove_exclude_name_entry = ctk.CTkEntry(self.exclude_entry_frame, width=370)
        self.remove_exclude_name_entry.grid(row=0, column=4, padx=5)

        """File Extensions Tab"""
        # File Extension frame
        self.file_extension_entry_frame = ctk.CTkFrame(self.add_remove_tabs.get("File Extensions"), corner_radius=0,
                                                       fg_color="transparent")
        self.file_extension_entry_frame.grid(row=8, column=0, padx=10, pady=10)

        # Add File Extension button
        self.add_file_extension_button = ctk.CTkButton(self.file_extension_entry_frame, text="Add File Ext.",
                                                       command=self.add_file_extension)
        self.add_file_extension_button.grid(row=0, column=0, padx=5)

        # Add File Extension entry
        self.add_file_extension_entry = ctk.CTkEntry(self.file_extension_entry_frame, width=370)
        self.add_file_extension_entry.grid(row=0, column=1, padx=5)

        # Remove File Extension button
        self.remove_file_extension_button = ctk.CTkButton(self.file_extension_entry_frame, text="Remove File Ext.",
                                                          command=self.remove_file_extension)
        self.remove_file_extension_button.grid(row=0, column=3, padx=5)

        # Remove File Extension entry
        self.remove_file_extension_entry = ctk.CTkEntry(self.file_extension_entry_frame, width=370)
        self.remove_file_extension_entry.grid(row=0, column=4, padx=5)

        """NO-GO Tab"""
        # NO-GO frame
        self.no_go_entry_frame = ctk.CTkFrame(self.add_remove_tabs.get("NO GO"), corner_radius=0,
                                              fg_color="transparent")
        self.no_go_entry_frame.grid(row=8, column=0, padx=10, pady=10)

        # Add NO-GO button
        self.add_no_go_button = ctk.CTkButton(self.no_go_entry_frame, text="Add NO GO",
                                              command=self.no_go_creation)
        self.add_no_go_button.grid(row=0, column=0, padx=5)

        # Add NO-GO entry
        self.add_no_go_name_entry = ctk.CTkEntry(self.no_go_entry_frame, width=370)
        self.add_no_go_name_entry.grid(row=0, column=1, padx=5)

        # Remove NO-GO button
        self.remove_no_go_button = ctk.CTkButton(self.no_go_entry_frame, text="Remove NO GO",
                                                 command=self.no_go_removal)
        self.remove_no_go_button.grid(row=0, column=3, padx=5)

        # Remove NO-GO entry
        self.remove_no_go_name_entry = ctk.CTkEntry(self.no_go_entry_frame, width=370)
        self.remove_no_go_name_entry.grid(row=0, column=4, padx=5)

        """Valid Extensions Tab"""
        # Valid Extension frame
        self.valid_extension_entry_frame = ctk.CTkFrame(self.add_remove_tabs.get("Valid Extensions"), corner_radius=0,
                                                        fg_color="transparent")
        self.valid_extension_entry_frame.grid(row=8, column=0, padx=10, pady=10)

        # Add Valid Extension button
        self.add_valid_extension_button = ctk.CTkButton(self.valid_extension_entry_frame, text="Add Valid Ext.",
                                                        command=self.add_valid_extension)
        self.add_valid_extension_button.grid(row=0, column=0, padx=5)

        # Add Valid Extension entry
        self.add_valid_extension_entry = ctk.CTkEntry(self.valid_extension_entry_frame, width=370)
        self.add_valid_extension_entry.grid(row=0, column=1, padx=5)

        # Remove Valid Extension button
        self.remove_valid_extension_button = ctk.CTkButton(self.valid_extension_entry_frame, text="Remove Valid Ext.",
                                                           command=self.remove_valid_extension)
        self.remove_valid_extension_button.grid(row=0, column=3, padx=5)

        # Remove Valid Extension entry
        self.remove_valid_extension_entry = ctk.CTkEntry(self.valid_extension_entry_frame, width=370)
        self.remove_valid_extension_entry.grid(row=0, column=4, padx=5)

        # Frame for clear add/remove button
        self.clear_add_remove_frame = ctk.CTkFrame(self.add_remove_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.clear_add_remove_frame.grid(row=2, column=0, padx=10)

        # Clear add/remove Button
        self.clear_add_remove_button = ctk.CTkButton(self.clear_add_remove_frame,
                                                     text="Clear",
                                                     command=lambda: self.clear_selection(
                                                         frame_name="add_remove_window"))
        self.clear_add_remove_button.grid(row=0, column=0, padx=10, pady=10)

        # Frame for reset add/remove checkbox
        self.reset_add_remove_frame = ctk.CTkFrame(self.add_remove_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.reset_add_remove_frame.grid(row=3, column=0, padx=10, pady=10)

        # Checkbox to enable/disable reset add/remove entries
        self.reset_add_remove_checkbox = ctk.CTkCheckBox(self.reset_add_remove_frame,
                                                         text="Reset entries",
                                                         variable=self.reset_add_remove_var)
        self.reset_add_remove_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Frame to display messages on the add/remove frame
        self.add_remove_message_label_frame = ctk.CTkFrame(self.add_remove_frame, corner_radius=0,
                                                           fg_color="transparent")
        self.add_remove_message_label_frame.grid(row=13, column=0, padx=10)

        # Add/Remove Message Label
        self.add_remove_message_label = ctk.CTkLabel(self.add_remove_message_label_frame, text="")
        self.add_remove_message_label.grid(row=0, column=0, padx=10, pady=10)

        """
        settings_window
        """
        # Create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # Settings label
        self.settings_label = ctk.CTkLabel(self.settings_frame, text="Settings",
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.settings_label.grid(row=0, column=0, padx=5, pady=5, columnspan=5)

        # Create a settings_tabview on settings_frame row 1
        self.settings_tabview, self.settings_tabs = self.create_tabview(self.settings_frame,
                                                                        self.settings_tab_names)

        """Appearance Tab"""
        # GUI settings frame
        self.gui_settings_frame = ctk.CTkFrame(self.settings_tabs.get("Appearance"), corner_radius=0,
                                               fg_color="transparent")
        self.gui_settings_frame.grid(row=0, column=0, padx=10, pady=10)

        # Select light or dark label
        self.appearance_mode_label = ctk.CTkLabel(self.gui_settings_frame, text="Appearance:")
        self.appearance_mode_label.grid(row=0, column=0, padx=10, pady=10)

        # Select light or dark mode
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.gui_settings_frame,
                                                      values=["Light", "Dark"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=0, column=1, padx=10, pady=10)

        # Set default value for appearance
        self.appearance_mode_menu.set("Dark")

        # Select scaling label
        self.scaling_label = ctk.CTkLabel(self.gui_settings_frame, text="UI Scaling:")
        self.scaling_label.grid(row=1, column=0, padx=10, pady=10)

        # Select scaling level
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.gui_settings_frame,
                                                     values=["70%", "80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=1, column=1, padx=10, pady=10)

        # Set default value for scaling
        self.scaling_optionemenu.set(f"{self.scaling}%")

        """Artist Tab"""
        # Artist frame
        self.artist_frame = ctk.CTkFrame(self.settings_tabs.get("Artist"), corner_radius=0,
                                         fg_color="transparent")
        self.artist_frame.grid(row=0, column=0, padx=10, pady=10)

        # Artist switch frame
        self.artist_switch_frame = ctk.CTkFrame(self.artist_frame, corner_radius=0,
                                                fg_color="transparent")
        self.artist_switch_frame.grid(row=0, column=0, padx=10, pady=10)

        # Artist Search label
        self.artist_search_label = ctk.CTkLabel(self.artist_switch_frame, text="Artist Search")
        self.artist_search_label.grid(row=0, column=0, padx=10, pady=5)

        # Switch to enable/disable artist search
        self.artist_search_switch = ctk.CTkSwitch(self.artist_switch_frame, text="Artist Search",
                                                  variable=self.artist_search_var)
        self.artist_search_switch.grid(row=1, column=0, padx=10, pady=10)

        # Switch to enable/disable ignore known artists for artist search
        self.ignore_known_artists_switch = ctk.CTkSwitch(self.artist_switch_frame, text="Ignore Known Artists",
                                                         variable=self.ignore_known_artists_var)
        self.ignore_known_artists_switch.grid(row=1, column=1, padx=10, pady=10)

        # Artist Identifier label
        self.artist_identifier_label = ctk.CTkLabel(self.artist_switch_frame, text="Artist Identifier")
        self.artist_identifier_label.grid(row=2, column=0, padx=10, pady=5)

        # Switch to enable/disable remove duplicates
        self.remove_duplicates_switch = ctk.CTkSwitch(self.artist_switch_frame,
                                                      text="Remove Artist Duplicates From Filename",
                                                      variable=self.remove_artist_duplicates_var)
        self.remove_duplicates_switch.grid(row=3, column=0, padx=10, pady=10)

        # Artist browse frame
        self.artist_browse_frame = ctk.CTkFrame(self.artist_frame, corner_radius=0,
                                                fg_color="transparent")
        self.artist_browse_frame.grid(row=1, column=0, padx=10, pady=10)

        # Browse Artist Directory button
        self.browse_artist_directory_button = ctk.CTkButton(self.artist_browse_frame, text="Artist Directory",
                                                            command=lambda: self.browse_directory(
                                                                self.artist_directory_entry, 'artist_directory'))
        self.browse_artist_directory_button.grid(row=0, column=0, padx=10, pady=5)

        # Artist Directory entry
        self.artist_directory_entry = ctk.CTkEntry(self.artist_browse_frame, width=890)
        self.artist_directory_entry.insert(0, self.artist_directory)
        self.artist_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browse Artist File button
        self.browse_artist_file_button = ctk.CTkButton(self.artist_browse_frame, text="Artist File",
                                                       command=self.browse_artist_file)
        self.browse_artist_file_button.grid(row=1, column=0, padx=5, pady=5)

        # Artist File entry
        self.artist_file_entry = ctk.CTkEntry(self.artist_browse_frame, width=890)
        self.artist_file_entry.insert(0, self.artist_file)
        self.artist_file_entry.grid(row=1, column=1, padx=10, pady=10)

        # Open Artist File button
        self.open_artist_file_button = ctk.CTkButton(self.artist_browse_frame, text="Open Artist File",
                                                     command=lambda: self.open_file(
                                                         self.artist_file))
        self.open_artist_file_button.grid(row=2, column=0, padx=5)

        """File Operations Tab"""
        # File Operations frame
        self.file_ops_frame = ctk.CTkFrame(self.settings_tabs.get("File Operations"), corner_radius=0,
                                           fg_color="transparent")
        self.file_ops_frame.grid(row=0, column=0, padx=10)

        # File Operations switch frame
        self.file_ops_switch_frame = ctk.CTkFrame(self.file_ops_frame, corner_radius=0,
                                                  fg_color="transparent")
        self.file_ops_switch_frame.grid(row=0, column=0, padx=10)

        # Switch to enable/disable open on drop behavior
        self.open_on_file_drop_switch = ctk.CTkSwitch(self.file_ops_switch_frame, text="Open File on Drag and Drop",
                                                      variable=self.open_on_file_drop_var)
        self.open_on_file_drop_switch.grid(row=0, column=0, padx=10, pady=10)

        # Master Entry frame
        self.master_entry_frame = ctk.CTkFrame(self.file_ops_frame, corner_radius=0, fg_color="transparent")
        self.master_entry_frame.grid(row=1, column=0, padx=10, pady=10)

        # Initial Directory frame
        self.initial_directory_frame = ctk.CTkFrame(self.master_entry_frame, corner_radius=0, fg_color="transparent")
        self.initial_directory_frame.grid(row=0, column=0, padx=10, pady=10)

        # Browse Initial Directory button
        self.browse_initial_directory_button = ctk.CTkButton(self.initial_directory_frame, text="Initial Directory",
                                                             command=lambda: self.browse_directory(
                                                                 self.initial_directory_entry, 'initial_directory'))
        self.browse_initial_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Initial Directory entry
        self.initial_directory_entry = ctk.CTkEntry(self.initial_directory_frame, width=855)
        self.initial_directory_entry.insert(0, self.initial_directory)
        self.initial_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browse Initial Output Directory button
        self.browse_initial_output_directory_button = ctk.CTkButton(self.initial_directory_frame,
                                                                    text="Initial Output Directory",
                                                                    command=lambda:
                                                                    self.browse_directory(
                                                                        self.initial_output_directory_entry,
                                                                        'initial_output_directory')
                                                                    )
        self.browse_initial_output_directory_button.grid(row=1, column=0, padx=5, pady=5)

        # Initial Directory entry
        self.initial_output_directory_entry = ctk.CTkEntry(self.initial_directory_frame, width=855)
        self.initial_output_directory_entry.insert(0, self.initial_output_directory)
        self.initial_output_directory_entry.grid(row=1, column=1, padx=10, pady=10)

        # Configuration File Frame
        self.configuration_file_frame = ctk.CTkFrame(self.master_entry_frame, corner_radius=0,
                                                     fg_color="transparent")
        self.configuration_file_frame.grid(row=1, column=0, padx=10, pady=10)

        # Browse Configuration File button
        self.open_configuration_file_button = ctk.CTkButton(self.configuration_file_frame, text="Open Config File",
                                                            command=lambda: self.open_file(
                                                                self.config_file_path))
        self.open_configuration_file_button.grid(row=0, column=0, padx=5)

        # Configuration File entry
        self.configuration_file_entry = ctk.CTkEntry(self.configuration_file_frame, width=890)
        self.configuration_file_entry.insert(0, self.config_file_path)
        self.configuration_file_entry.grid(row=0, column=1, padx=10, pady=10)

        # Dictionary File Frame
        self.dictionary_file_frame = ctk.CTkFrame(self.master_entry_frame, corner_radius=0,
                                                  fg_color="transparent")
        self.dictionary_file_frame.grid(row=2, column=0, padx=10, pady=10)

        # Browse Dictionary File button
        self.open_dictionary_file_button = ctk.CTkButton(self.dictionary_file_frame, text="Open Dictionary File",
                                                         command=lambda: self.open_file(
                                                             self.dictionary_file))
        self.open_dictionary_file_button.grid(row=0, column=0, padx=5)

        # Dictionary File entry
        self.dictionary_file_entry = ctk.CTkEntry(self.dictionary_file_frame, width=890)
        self.dictionary_file_entry.insert(0, self.dictionary_file)
        self.dictionary_file_entry.grid(row=0, column=1, padx=10, pady=10)

        """Logging Tab"""
        # Logging frame
        self.logging_frame = ctk.CTkFrame(self.settings_tabs.get("Logging"), corner_radius=0,
                                          fg_color="transparent")
        self.logging_frame.grid(row=0, column=0, padx=10, pady=10)

        # Logging switch frame
        self.logging_switch_frame = ctk.CTkFrame(self.logging_frame, corner_radius=0,
                                                 fg_color="transparent")
        self.logging_switch_frame.grid(row=0, column=0, padx=10, pady=10)

        # Switch to enable/disable activate logging
        self.activate_logging_switch = ctk.CTkSwitch(self.logging_switch_frame, text="Activate Logging",
                                                     variable=self.activate_logging_var)
        self.activate_logging_switch.grid(row=0, column=0, padx=10, pady=10)

        # Bind the callback function to the activate logging variable
        self.activate_logging_var.trace_add("write", self.handle_logging_activation)

        # Switch to enable/disable suppress standard outputs/errors
        self.suppress_switch = ctk.CTkSwitch(self.logging_switch_frame, text="Suppress Standard Output/Error",
                                             variable=self.suppress_var)
        self.suppress_switch.grid(row=0, column=1, padx=10, pady=10)

        # Logging browse frame
        self.logging_browse_frame = ctk.CTkFrame(self.logging_frame, corner_radius=0,
                                                 fg_color="transparent")
        self.logging_browse_frame.grid(row=1, column=0, padx=10, pady=10)

        # Browse Log button
        self.open_log_file_button = ctk.CTkButton(self.logging_browse_frame, text="Open Log File",
                                                  command=lambda: self.open_file(
                                                      self.file_renamer_log))
        self.open_log_file_button.grid(row=0, column=0, padx=5)

        # log File entry
        self.log_file_entry = ctk.CTkEntry(self.logging_browse_frame, width=890)
        self.log_file_entry.insert(0, self.file_renamer_log)
        self.log_file_entry.grid(row=0, column=1, padx=10, pady=10)

        """Messaging Tab"""
        # Confirmation frame
        self.confirmation_frame = ctk.CTkFrame(self.settings_tabs.get("Messaging"), corner_radius=0,
                                               fg_color="transparent")
        self.confirmation_frame.grid(row=0, column=0, padx=10)

        # Switch to enable/disable show messageboxes
        self.show_messageboxes_switch = ctk.CTkSwitch(self.confirmation_frame, text="Show Messageboxes",
                                                      variable=self.show_messageboxes_var)
        self.show_messageboxes_switch.grid(row=0, column=0, padx=10, pady=10)

        # Switch to enable/disable show confirmation messageboxes
        self.show_confirmation_messageboxes_switch = ctk.CTkSwitch(self.confirmation_frame,
                                                                   text="Show Confirmation Messageboxes",
                                                                   variable=self.show_confirmation_messageboxes_var)
        self.show_confirmation_messageboxes_switch.grid(row=0, column=1, padx=10, pady=10)

        # Fallback confirmation state when confirmation messageboxes are suppressed
        self.fallback_confirmation_label = ctk.CTkLabel(self.confirmation_frame, text="Fallback confirmation state:")
        self.fallback_confirmation_label.grid(row=1, column=0, padx=10, pady=5)

        # Fallback true radio button
        self.true_radio = ctk.CTkRadioButton(self.confirmation_frame, text="True",
                                             variable=self.fallback_confirmation_var, value=True)
        self.true_radio.grid(row=1, column=1, padx=10, pady=5)

        # Fallback false radio button
        self.false_radio = ctk.CTkRadioButton(self.confirmation_frame, text="False",
                                              variable=self.fallback_confirmation_var,
                                              value=False)
        self.false_radio.grid(row=1, column=2, padx=10, pady=5)

        # Switch to enable/disable truncate text
        self.truncate_text_switch = ctk.CTkSwitch(self.confirmation_frame, text="Truncate Text",
                                                  variable=self.truncate_var)
        self.truncate_text_switch.grid(row=2, column=0, padx=10, pady=5)

        """Reminders Tab"""
        # Reminders frame
        self.reminders_frame = ctk.CTkFrame(self.settings_tabs.get("Reminders"), corner_radius=0,
                                            fg_color="transparent")
        self.reminders_frame.grid(row=3, column=0, padx=10, pady=10)

        # Switch to enable/disable create double check reminder
        self.double_check_switch = ctk.CTkSwitch(self.reminders_frame, text="Create Double Check Reminder",
                                                 variable=self.double_check_var)
        self.double_check_switch.grid(row=0, column=0, padx=10, pady=10)

        # Double Check Directory frame
        self.double_check_reminder_directory_frame = ctk.CTkFrame(self.reminders_frame, corner_radius=0,
                                                                  fg_color="transparent")
        self.double_check_reminder_directory_frame.grid(row=1, column=0, padx=10, pady=10)

        # Browse Double Check Directory button
        self.browse_reminder_directory_button = ctk.CTkButton(self.double_check_reminder_directory_frame,
                                                              text="Double Check Reminder Directory",
                                                              command=lambda: self.browse_directory(
                                                                  self.double_check_reminder_directory_entry,
                                                                  'double_check_directory'))
        self.browse_reminder_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Double Check Reminder entry
        self.double_check_reminder_directory_entry = ctk.CTkEntry(self.double_check_reminder_directory_frame, width=775)
        self.double_check_reminder_directory_entry.insert(0, self.double_check_directory)
        self.double_check_reminder_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browse NO GO Directory button
        self.browse_no_go_directory_button = ctk.CTkButton(self.double_check_reminder_directory_frame,
                                                           text="NO GO Directory",
                                                           command=lambda: self.browse_directory(
                                                               self.no_go_reminder_directory_entry, 'no_go_directory'))
        self.browse_no_go_directory_button.grid(row=1, column=0, padx=5, pady=5)

        # NO GO Reminder entry
        self.no_go_reminder_directory_entry = ctk.CTkEntry(self.double_check_reminder_directory_frame, width=775)
        self.no_go_reminder_directory_entry.insert(0, self.no_go_directory)
        self.no_go_reminder_directory_entry.grid(row=1, column=1, padx=10, pady=10)

        # Open NO GO Artist File button
        self.open_artist_file_button = ctk.CTkButton(self.double_check_reminder_directory_frame,
                                                     text="Open NO GO Artist File",
                                                     command=lambda: self.open_file(
                                                         self.no_go_artist_file))
        self.open_artist_file_button.grid(row=2, column=0, padx=10)

        """Tabs"""
        # Tab name frame
        self.tab_name_frame = ctk.CTkFrame(self.settings_tabs.get("Tabs"), corner_radius=0, fg_color="transparent")
        self.tab_name_frame.grid(row=3, column=0, padx=10, pady=10)

        # Switch to enable/disable use_custom_tab_names_var
        self.use_custom_tab_names_switch = ctk.CTkSwitch(self.tab_name_frame, text="Use Custom Tab Names",
                                                         variable=self.use_custom_tab_names_var)
        self.use_custom_tab_names_switch.grid(row=0, column=0, padx=10)

        # Bind the callback function to use_custom_tab_names_var
        self.use_custom_tab_names_var.trace_add("write", self.refresh_category_buttons)

        # Switch to enable/disable sort tab names
        self.sort_tab_names_switch = ctk.CTkSwitch(self.tab_name_frame, text="Sort Tab Names",
                                                   variable=self.sort_tab_names_var)
        self.sort_tab_names_switch.grid(row=0, column=1, padx=10)

        # Bind the callback function to sort_tab_names_var
        self.sort_tab_names_var.trace_add("write", self.refresh_buttons_and_tabs)

        # Switch to enable/disable sort_reverse_order_var
        self.sort_tab_names_reverse_switch = ctk.CTkSwitch(self.tab_name_frame, text="Sort Tab Names (A-Z / Z-A)",
                                                           variable=self.sort_reverse_order_var)
        self.sort_tab_names_reverse_switch.grid(row=0, column=2, padx=10)

        # Bind the callback function to sort_reverse_order_var
        self.sort_reverse_order_var.trace_add("write", self.refresh_buttons_and_tabs)

    def on_frame_configure(self, *_):
        """
        Callback function to handle the frame configuration for scrolling.

        Args:
        *_: Variable number of arguments. Ignored in the implementation.
        """
        # Reset the scroll region to encompass the inner frame
        self.file_renamer_canvas.configure(scrollregion=self.file_renamer_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """
        Callback function to handle the canvas configuration.

        Adjusts the width of the scrollable frame to match the canvas width.

        Args:
        event (tk.Event): The event object containing information about the canvas configuration change.
        """
        # Set the scrollable frame's width to match the canvas
        canvas_width = event.width - self.file_renamer_scrollbar.winfo_width()
        self.file_renamer_canvas.itemconfig(self.file_renamer_scrollable_frame_window, width=canvas_width)

    def handle_logging_activation(self, *_):
        """
        Callback function to handle logging activation.

        Activates or deactivates logging based on the value of the activate_logging_var variable.

        Args:
        *_: Variable number of arguments. Ignored in the implementation.
        """
        # If logging is true, call the logging_setup function
        if self.activate_logging_var.get():
            try:
                self.logging_setup()
            except OSError as e:
                print(f"Logging failed. Error: {e}")
        else:
            # If logging is false, call the stop_logging function
            self.stop_logging()

    def cleanup_on_exit(self):
        """
        Cleanup method to be called on program exit.

        Stops logging if it is currently running. Interrupt processing if threads are running.

        Note: Ensure this method is appropriately connected to an exit event or cleanup routine.
        """
        # Interrupt threads that are processing
        self.interrupt_processing("all")

        # Stop logging if currently running
        if self.activate_logging_var.get():
            self.stop_logging()

    def select_frame_by_name(self, frame_name: str):
        """
        Switches between frames based on the provided frame_name and sets button colors accordingly.

        Args:
        frame_name (str): The name of the frame to be selected.

        Note: Ensure this method is connected to a button press or navigation event.
        """
        # Set button color for the selected button
        self.file_renamer_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "file_renamer_window" else "transparent")
        self.name_normalizer_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "name_normalizer_window" else "transparent")
        self.video_editor_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "video_editor_window" else "transparent")
        self.add_remove_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "add_remove_window" else "transparent")
        self.settings_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "settings_window" else "transparent")

        # Show the selected frame and hide others, set the active frame_name
        if frame_name == "file_renamer_window":
            self.file_renamer_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.file_renamer_frame.grid_forget()
        if frame_name == "name_normalizer_window":
            self.name_normalizer_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.name_normalizer_frame.grid_forget()
        if frame_name == "video_editor_window":
            self.video_editor_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.video_editor_frame.grid_forget()
        if frame_name == "add_remove_window":
            self.add_remove_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.add_remove_frame.grid_forget()
        if frame_name == "settings_window":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.settings_frame.grid_forget()

    """
    Event handlers for button clicks to switch frames
    """

    def file_renamer_button_event(self):
        """
        Event handler for the file renamer button.

        Calls the select_frame_by_name method to switch to the 'file_renamer_window' frame.
        """
        self.select_frame_by_name("file_renamer_window")

    def name_normalizer_button_event(self):
        """
        Event handler for the name normalizer button.

        Calls the select_frame_by_name method to switch to the 'name_normalizer_window' frame.
        """
        self.select_frame_by_name("name_normalizer_window")

    def video_editor_button_event(self):
        """
        Event handler for the video editor button.

        Calls the select_frame_by_name method to switch to the 'video_editor_window' frame.
        """
        self.select_frame_by_name("video_editor_window")

    def add_remove_button_event(self):
        """
        Event handler for the add/remove button.

        Calls the select_frame_by_name method to switch to the 'add_remove_window' frame.
        """
        self.select_frame_by_name("add_remove_window")

    def settings_button_event(self):
        """
        Event handler for the settings button.

        Calls the select_frame_by_name method to switch to the 'settings_window' frame.
        """
        self.select_frame_by_name("settings_window")

    def update_background_color(self):
        """
        Updates the canvas background color based on the current appearance mode.

        Note: Ensure this method is called appropriately, such as in response to a mode change event.
        """
        # Update canvas background color based on the current appearance mode
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            self.file_renamer_canvas.configure(bg='#dbdbdb')
        elif current_mode == "Dark":
            self.file_renamer_canvas.configure(bg='#2B2B2B')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
        Event handler for changing the appearance mode.

        Updates the appearance mode using ctk.set_appearance_mode() and calls update_background_color()
        to adjust the background color based on the new appearance mode.

        Args:
        new_appearance_mode (str): The new appearance mode ('Light' or 'Dark').
        """
        # Update background color when appearance mode changes
        ctk.set_appearance_mode(new_appearance_mode)
        self.update_background_color()

    @staticmethod
    def change_scaling_event(new_scaling: str):
        """
        Event handler for changing widget scaling.

        Converts the new_scaling percentage to a float, sets the widget scaling using ctk.set_widget_scaling().

        Args:
        new_scaling (str): The new widget scaling percentage.
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    """
    Messaging
    """

    def update_text_color(self):
        """
        Updates text color based on the current appearance mode.

        Note: Ensure this method is called appropriately, such as in response to a mode change event.
        """
        # Update text color based on the current appearance mode
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            self.file_renamer_message_label.configure(text_color="#000000")
            self.name_normalizer_message_label.configure(text_color="#000000")
            self.video_editor_message_label.configure(text_color="#000000")
            self.add_remove_message_label.configure(text_color="#000000")
        elif current_mode == "Dark":
            self.file_renamer_message_label.configure(text_color="#FFFFFF")
            self.name_normalizer_message_label.configure(text_color="#FFFFFF")
            self.video_editor_message_label.configure(text_color="#FFFFFF")
            self.add_remove_message_label.configure(text_color="#FFFFFF")

    def show_message(self, message, error=False, frame_name=None):
        """
        Displays a message on the actively selected frame or all frames.

        Args:
        message (str): The message to be displayed.
        error (bool): If True, formats the message with red text for error indication. Default is False.
        frame_name (str or None): The name of the frame to display the message on. If None, displays on all frames.

        Note: Ensure this method is called appropriately to show messages in your GUI.
        """
        # Update text color when displaying a message
        self.update_text_color()

        # Display the message with optional error formatting on the actively selected frame
        if frame_name == "file_renamer_window":
            labels = [self.file_renamer_message_label]
        elif frame_name == "name_normalizer_window":
            labels = [self.name_normalizer_message_label]
        elif frame_name == "video_editor_window":
            labels = [self.video_editor_message_label]
        elif frame_name == "add_remove_window":
            labels = [self.add_remove_message_label]
        else:
            # Default to all frame labels if no frame name is passed
            labels = [self.file_renamer_message_label, self.name_normalizer_message_label,
                      self.video_editor_message_label, self.add_remove_message_label]

        # Truncate the message after x characters for GUI-friendly formatting.
        truncated_message = f"{message[:115]}..." if len(message) > 115 else message

        for label in labels:
            if error:
                label.configure(text=truncated_message, text_color="#FF0000")  # Red text for errors
            else:
                label.configure(text=truncated_message)

    @staticmethod
    def validate_entry(var, default_value, desired_type):
        """
        Validates and updates the value of a Tkinter variable based on the desired type.

        Args:
        var (tkinter.Variable): The Tkinter variable to be validated and updated.
        default_value: The default value to set if validation fails.
        desired_type (type): The desired type for the variable (int or float).

        Note: Ensure this method is used to validate and update Tkinter variable values.
        """
        # Ensure the value is of the desired type
        current_value = var.get()

        if desired_type == int:
            # Check if the value is an integer
            if not current_value.isdigit():
                try:
                    # Try to convert the value to an integer
                    int_value = int(current_value)
                    var.set(int_value)
                except ValueError:
                    # If conversion to integer fails, set it to the default value
                    var.set(default_value)
        elif desired_type == float:
            # Check if the value is a float
            try:
                float_value = float(current_value)
                var.set(float_value)
            except ValueError:
                # If conversion to float fails, set it to the default value
                var.set(default_value)
        else:
            # If the desired type is neither int nor float, set it to the default value
            var.set(default_value)

    @staticmethod
    def get_basenames(file_paths: list) -> list:
        """
        Get the basenames of a list of file paths.

        Parameters:
        - file_paths (list): A list of file paths.

        Returns:
        - list: A list containing the basenames of the input file paths.
        """
        basenames = [os.path.basename(path) for path in file_paths]
        return basenames

    @staticmethod
    def get_lengths(input_list: list) -> list:
        """
        Get the lengths of each item in the input list, add one to account for the whitespace, and append it to the
        item.

        Parameters:
        - input_list (list): A list of items.

        Returns:
        - list: A new list with each item appended by its length.
        """
        processed_list = [f"{item} (frees {(len(str(item)) + 1)} characters)" for item in
                          input_list]
        return processed_list

    def start_progress(self, progress_bar_name: str, frame: str):
        """
        Start a progress bar.

        Args:
        - progress_bar_name (str): The name of the progress bar attribute.
        - frame (str): The name of the frame to which the progress bar will be added.

        """
        # Create a progress bar
        setattr(self, progress_bar_name, ctk.CTkProgressBar(frame, orientation="horizontal", mode="indeterminate"))
        getattr(self, progress_bar_name).grid(row=0, column=0, padx=10, pady=10)

        # Start the progress bar
        getattr(self, progress_bar_name).start()

    def stop_progress(self, progress_bar_name: str):
        """
        Stop and destroy a progress bar.

        Args:
        - progress_bar_name (str): The name of the progress bar attribute to stop and destroy.

        """
        try:
            # Stop the progress bar
            getattr(self, progress_bar_name).stop()

            # Destroy the progress bar widget
            getattr(self, progress_bar_name).destroy()
        except AttributeError:
            # Handle the case where the progress bar attribute does not exist
            self.log_and_show(f"Progress bar '{progress_bar_name}' not found.", create_messagebox=True, error=True)

    def log_and_show(self, message, create_messagebox=False, error=False, not_logging=False):
        """
        Method to check logging state, log if applicable, and show a messagebox.

        Parameters:
        - message: The message to be logged and displayed.
        - create_messagebox: Boolean indicating whether to create and display a messagebox.
        - error: Boolean indicating whether the message is an error message.
        - not_logging: Boolean indicating whether to skip logging.
        """
        # Check logging state and log message if applicable
        if not not_logging and self.activate_logging_var.get():
            logging_function = logging.error if error else logging.info
            logging_function(message)

        # Check messagebox state and display messageboxes if applicable
        if self.show_messageboxes_var.get():
            messagebox_function = messagebox.showerror if error else messagebox.showinfo
            if create_messagebox:
                messagebox_function("Error" if error else "Info", message)
            else:
                # Display the message on the applicable frame if messageboxes are enabled but none were created
                self.show_message(message, error=error, frame_name=self.frame_name)
        else:
            # Display the message on the applicable frame if messageboxes are disabled
            self.show_message(message, error=error, frame_name=self.frame_name)

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

    @staticmethod
    def selection_window(title: str, prompt: str, label_text: str, item_list: list, item_text=None) -> str:
        """
        Display a selection window prompting the user to choose from a list of options.

        Args:
        - title (str): Title of the selection window.
        - prompt (str): Prompt message displayed in the window.
        - label_text (str): Label text for the selection.
        - item_list (list): List of items to choose from.
        - item_text (list, optional): GUI-friendly list of items to choose from.

        Returns:
        - str: The selected option from the user.

        """
        # If the gui-friendly text is provided, then use it, else use the item_list
        item_text = item_text if item_text else item_list

        # Prompt the user to choose from the list using SelectOptionWindow
        selection_window = SelectOptionWindow(title=title,
                                              prompt=prompt,
                                              label_text=label_text,
                                              item_list=item_list,
                                              item_text=item_text)

        # Wait for the user to respond before proceeding
        selection_window.wait_window()

        # Retrieve the selected directory
        selected_option = selection_window.get_selected_option()

        return selected_option

    """
    Json Handling
    """

    def initialize_json(self):
        """
        Initializes class attributes by loading data from the specified JSON file.

        Note: Ensure this method is called appropriately during the initialization of your class.
        """
        # Load data from the dictionary_file
        try:
            if not os.path.isfile(self.dictionary_file):
                # Return early if the file doesn't exist
                return

            with open(self.dictionary_file, "r") as json_file:
                data = json.load(json_file)

                # Get artist_common_categories dictionary
                self.artist_common_categories = data.get("artist_common_categories", {})

                # Get categories dictionary
                self.categories = data.get("categories", {})

                # Get custom_text_to_replace list
                self.custom_text_to_replace = data.get("custom_text_to_replace", {})

                # Get excluded_folders list
                self.excluded_folders = data.get("excluded_folders", [])

                # Get file_extensions list
                self.file_extensions = data.get("file_extensions", [])

                # Get valid_extensions list
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

    def update_json(self, file_to_update, dictionary_name, updated_data):
        """
        Updates a specific dictionary in a JSON file with new data.

        Args:
        file_to_update (str): The path to the JSON file to be updated.
        dictionary_name (str): The name of the dictionary key to be updated.
        updated_data: The new data to be assigned to the specified dictionary key.

        Note: Ensure this method is called appropriately to update JSON files in your application.
        """
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

    """
    Logging
    """

    def logging_setup(self):
        """
        Set up logging for the File Renamer application.

        Note: Ensure this method is called appropriately during the initialization of your application.
        """
        # Create the log file if it doesn't exist
        if not os.path.exists(self.file_renamer_log):
            with open(self.file_renamer_log, 'w'):
                pass

        # Initialize logging
        logging.basicConfig(filename=self.file_renamer_log, level=logging.INFO, filemode='a',
                            format='%(asctime)s - %(levelname)s: %(message)s')

        logging.info("Logging started.")

    def stop_logging(self):
        """
        Stop logging for the File Renamer application.

        Note: Ensure this method is called appropriately during the cleanup or termination of your application.
        """
        # Notate that logging stopped if the log file exists
        if os.path.exists(self.file_renamer_log):
            logging.info("Logging stopped.")

    def redirect_output(self):
        """
        Redirects standard output and error based on logging and suppression settings.

        Note: Ensure this method is called appropriately to manage the redirection of output.
        """
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

    def remove_successful_line_from_file(self, file_path: str, line_to_remove: str):
        """
        Removes a specified line from a text file.

        Args:
        file_path (str): The path to the text file.
        line_to_remove (str): The line to be removed from the file.

        Note: Ensure this method is called appropriately to remove a line from the specified text file.
        """
        try:
            if not file_path.lower().endswith('.txt'):
                # If the file does not have a .txt extension, return without performing any operation.
                self.log_and_show("The provided file is not a txt file. Skipping removal of successful line.",
                                  error=True)
                return

            # Read all lines from the file.
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Open the file in write mode to remove the specified line.
            with open(file_path, 'w') as file:
                # Write lines back to the file, excluding the successful line to remove.
                for line in lines:
                    if line.strip() != line_to_remove:
                        file.write(line)

            self.log_and_show(f"Successful line removed from {file_path}")

        except Exception as e:
            # Log the exception using the logging module.
            self.log_and_show(f"An error occurred while removing line from file: {e}", create_messagebox=True,
                              error=True)

    def move_file_to_trash(self):
        """
        Move the selected file to the system's trash.

        Note: Ensure this method is called appropriately to move the selected file to the trash.
        """
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
                    self.file_renamer_queue = []
                    self.file_display_text.set("")
                    self.name_length_text.set("")
                    self.prefix_text_entry.delete(0, ctk.END)
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

    def double_check_reminder(self, new_path: str):
        """
        Create a double-check reminder for the folder immediately above the specified location.

        Args:
        new_path (str): The path for which the double-check reminder is to be created.

        Note: Ensure this method is called appropriately to create double-check reminders.
        """
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

    def load_last_used_file(self):
        """
        Load the last used file based on the current frame and update the display accordingly.

        Notes:
        - Handles last used file loading for different frames (file_renamer, name_normalizer, video_editor).
        - Logs the action if logging is enabled.
        """
        if self.frame_name == "file_renamer_window":
            # Check if the file_renamer_last_used_file variable is provided and the input exists
            if self.file_renamer_last_used_file and os.path.exists(self.file_renamer_last_used_file):
                # Set the selected file to the file renamer last used file and update display
                self.file_renamer_selected_file = self.file_renamer_last_used_file

                self.file_renamer_queue = []
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

    def send_to_module(self, destination: str):
        """
        Send the selected file to the specified module and perform necessary updates.

        Args:
        - destination (str): The name of the destination module ("file_renamer_module", "name_normalizer_module",
        "video_editor_module").

        Notes:
        - Clears the selection for the source module.
        - Updates the display based on the selected file and the destination module.
        - Logs the action if logging is enabled.
        - Switches frames to the specified destination module.

        """
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

    def on_file_drop(self, event):
        """
        Handle the event when a file is dropped onto the application window.

        Args:
        - event (Event): The event object representing the file drop.

        Notes:
        - Initializes the selected file variable to the dropped file.
        - Extracts the file name from the path for GUI-friendly presentation.
        - Assigns the selected file variable to the correct file depending on the active frame.
        - Clears and updates the corresponding entry widgets and variables.
        - Opens the input file if the corresponding option is set.
        - Adds artist common categories to the queue if the option is set.
        - Logs the action and displays the message in the GUI.

        """
        # Initialize the selected file variable to the dropped file
        selected_file = event.data.strip('{}')

        # Extract the file name from the path for GUI-friendly presentation
        filename = os.path.basename(selected_file)

        # Assign the selected file variable to the correct file depending on the active frame
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

            # Remove the default entries text
            self.prefix_text_entry.delete(0, ctk.END)
            self.custom_text_entry.delete(0, ctk.END)

            self.file_renamer_queue = []
            self.update_file_display()

            # Open the input if the corresponding option is set
            if self.open_on_file_drop_var.get():
                self.open_file(selected_file)

            # Add artist common categories to the queue
            if self.artist_common_categories_var.get():
                self.add_remove_common_categories_to_queue()

        # Log the action and display the message in the GUI
        self.log_and_show(f"Input selected via drop: {filename}")

    def open_file(self, file_to_open: str):
        """
        Opens the specified file using the default system program.

        Parameters:
        - file_to_open (str): The path of the file to be opened.

        Returns:
        - None
        """
        # Check if the input exists
        if not os.path.exists(file_to_open):
            # If the provided input does not exist, log an error and return
            self.log_and_show(f"Cannot open input as it does not exist: {file_to_open}",
                              create_messagebox=True, error=True)
            return

        # Get the filename from the file path
        filename = os.path.basename(file_to_open)

        # If the input path is not empty, try to open the input using the default system program
        if file_to_open:
            try:
                subprocess.Popen(['xdg-open', file_to_open])

                # Log a success message if the input is opened successfully
                self.log_and_show(f"Input opened: {filename}")
            except OSError as e:
                # If an error occurs while opening the file, log the error
                self.log_and_show(f"{str(e)}", create_messagebox=True, error=True)

    def update_file_display(self, *_):
        """
        Update the file display based on the selected file and user input.

        Args:
        - *_: Variable number of arguments (unused in this method).

        Notes:
        - Gathers data from the GUI including base name, weighted categories, prefix text, custom text, and extension.
        - Constructs the proposed name using gathered information.
        - Sets the proposed name to the char_length variable.
        - Sets the proposed name to the display text.
        - Handles name length constraints, truncating if necessary.
        - Updates the file display and name length variables.

        """
        if self.file_renamer_selected_file:
            # Gather the data from the GUI
            (base_name, weighted_categories, prefix_text, custom_text, extension) = self.gather_and_sort()

            # Construct the name
            (proposed_name, char_length) = self.construct_new_name(base_name, weighted_categories, prefix_text,
                                                                   custom_text, extension)

            # Set the proposed name to the file display
            self.file_display_text.set(proposed_name)

            # Set the length of the name to the name_length_text
            self.name_length_text.set(char_length)

            # Handle name length constraints
            if char_length > 255:
                self.name_length_handler(char_length)

    def name_length_handler(self, char_length: int):
        """
        Handle name length constraints for the proposed file name.

        Args:
        - char_length (int): Length of the proposed file name.

        """
        if char_length > 255:
            # Check if there is an entry in the queue list
            if len(self.file_renamer_queue) == 0:
                self.log_and_show("The proposed file name exceeds 255 characters. "
                                  "Operating system limitations prohibit this. Please remove some of your custom text"
                                  " and try again.",
                                  create_messagebox=True, error=True)
            elif len(self.file_renamer_queue) > 0:
                # Display the length of the category word + 1
                categories_with_lengths = self.get_lengths(self.file_renamer_queue)

                # Prompt the user to choose from the list using SelectOptionWindow
                chosen_category = self.selection_window(title="Name Length Error",
                                                        prompt="The proposed file name exceeds 255 characters. "
                                                               "\nOperating system limitations prohibit this. "
                                                               "\nPlease choose a category to remove:",
                                                        label_text="Choose Category",
                                                        item_list=self.file_renamer_queue,
                                                        item_text=categories_with_lengths)

                if chosen_category:
                    # Remove the category from the queue
                    self.remove_from_queue(chosen_category)

    def undo_last(self):
        """
        Undo the last category added to the file renamer queue.

        Notes:
        - Removes the last category from the queue and updates the file display.
        - Logs the action if logging is enabled.

        """
        if self.file_renamer_queue:
            # Remove the last category from the queue and update display
            self.file_renamer_queue.pop()
            self.update_file_display()
            self.log_and_show("Last category removed", not_logging=True)
        else:
            # Log the action if logging is enabled
            self.log_and_show("Nothing in the queue. Nothing to undo.",
                              create_messagebox=True, error=True)

    def undo_file_rename(self):
        """
        Undo the last file renaming or name normalization operation.

        This method checks the current frame and attempts to revert the changes made
        in the last file renaming or name normalization operation. It provides a confirmation
        prompt before performing the undo operation.

        Returns:
            None
        """
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
                self.log_and_show("No previous file rename operation. Nothing to undo.", create_messagebox=True,
                                  error=True)

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

    def clear_selection(self, frame_name: str) -> None:
        """
        Clear the selected options and input fields based on the provided frame name.

        Parameters:
            frame_name (str): The name of the frame for which to clear the selection.

        Returns:
            None
        """
        if frame_name == "file_renamer_window":
            self.file_renamer_selected_file = ""
            self.file_renamer_queue = []
            self.file_display_text.set("")
            self.name_length_text.set("")

            # Clear text entries and reset output directory
            self.prefix_text_entry.delete(0, ctk.END)
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

            # Clear minute entries
            self.minute_entry.delete(0, ctk.END)
            self.minute_entry1.delete(0, ctk.END)

            # Clear second entries
            self.second_entry.delete(0, ctk.END)
            self.second_entry1.delete(0, ctk.END)

        elif frame_name == "add_remove_window":
            # Get the active tab from the add_remove_tabview
            active_tag = self.add_remove_tabview.get()

            if active_tag == "Artist":
                # Clear add artist entry
                self.add_artist_entry.delete(0, ctk.END)

                # Clear remove artist entry
                self.remove_artist_entry.delete(0, ctk.END)

                # Clear add acc artist record entry
                self.add_acc_record_entry.delete(0, ctk.END)

                # Clear remove acc artist record entry
                self.remove_acc_record_entry.delete(0, ctk.END)

                # Clear acc artist
                self.acc_selected_artist = ""
                self.acc_display_text.set("")

                # Clear add acc entry
                self.add_acc_entry.delete(0, ctk.END)

                # Clear remove acc entry
                self.remove_acc_entry.delete(0, ctk.END)

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

            elif active_tag == "Custom Text to Replace":
                # Clear add custom text to replace entry
                self.add_ctr_name_entry.delete(0, ctk.END)

                # Clear replacement text to replace entry
                self.replacement_text_entry.delete(0, ctk.END)

                # Clear remove custom text to replace entry
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

    def browse_artist_file(self):
        """
        Open a file dialog to browse and select an artist-related file.

        Updates:
        - Sets the selected file path to the artist_file variable.
        - Clears the entry and sets it to the artist file path in the GUI.
        """
        artist_file = filedialog.askopenfilename(
            initialdir=self.initial_directory,
            filetypes=[("Text Files", "*.txt")])

        if artist_file:
            # Set the file to the artist file variable
            self.artist_file = artist_file

            # Clear the entry and set it to the artist file
            self.artist_file_entry.delete(0, ctk.END)
            self.artist_file_entry.insert(0, self.artist_file)

    def browse_directory(self, entry_widget, target_attribute):
        """
        Open a directory dialog to browse and select a directory.

        Updates:
        - Clears the entry in the GUI and sets it to the selected directory.
        - Updates the corresponding attribute in the class with the selected directory path.

        Parameters:
        - entry_widget: The entry widget in the GUI where the selected directory path will be displayed.
        - target_attribute: The attribute in the class to be updated with the selected directory path.
        """
        selected_directory = filedialog.askdirectory(initialdir=getattr(self, target_attribute))

        if selected_directory:
            # Clear the entry and set it to the selected directory
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, selected_directory)
            # Update the corresponding attribute in your class
            setattr(self, target_attribute, selected_directory)

    def browse_input(self) -> None:
        """
        Browse and select input files or directories based on the frame context.

        Returns:
            None
        """
        if self.frame_name == "file_renamer_window":
            # Remove the default prefix text entry text
            self.prefix_text_entry.delete(0, ctk.END)
            # Remove the default custom text entry text
            self.custom_text_entry.delete(0, ctk.END)

            file_path = filedialog.askopenfilename(initialdir=self.initial_directory)
            if file_path:
                # Set the selected file
                self.file_renamer_selected_file = file_path

                # Clear the queue
                self.file_renamer_queue = []
                # Update display
                self.update_file_display()

                # Add artist common categories to the queue
                if self.artist_common_categories_var.get():
                    self.add_remove_common_categories_to_queue()

                # Log the action if logging is enabled
                self.log_and_show(f"Input selected via Browse: "
                                  f"{os.path.basename(self.file_renamer_selected_file)}")

        elif self.frame_name == "name_normalizer_window":
            # Method to browse and select a folder to normalize files
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

    def browse_output_directory(self) -> None:
        """
        Browse and select an output directory based on the frame context.

        Returns:
            None
        """
        if self.frame_name == "file_renamer_window":
            # Check if an input is selected
            if self.file_renamer_selected_file:
                # Check if suggest output directory is true
                if self.suggest_output_directory_var.get():
                    # Call the suggest output directory function to determine initial directory
                    initial_directory_check = self.suggest_output_directory()

                    # If suggest output directory returns a single result, set it to initial_directory
                    if initial_directory_check and not isinstance(initial_directory_check, list):
                        initial_directory = initial_directory_check

                    # If suggest output directory returns a list, then use SelectOptionWindow
                    elif isinstance(initial_directory_check, list):
                        # Sanitize the list for display in the GUI
                        basename_list = self.get_basenames(initial_directory_check)

                        # Prompt the user to choose from the list using SelectOptionWindow
                        chosen_artist = self.selection_window(title="Suggest Output Directory",
                                                              prompt="Multiple matching artists found. Choose "
                                                                     "an artist:",
                                                              label_text="Choose Artist",
                                                              item_list=initial_directory_check,
                                                              item_text=basename_list)

                        if chosen_artist in initial_directory_check:
                            initial_directory = chosen_artist
                            self.log_and_show(f"User chose the suggested output directory: {chosen_artist}")
                        else:
                            # If the choice is not in the matching_artists, use the default initial output directory
                            initial_directory = self.initial_output_directory

                    # If suggest output directory returns None, set initial_directory to self.initial_output_directory
                    elif initial_directory_check is None:
                        initial_directory = self.initial_output_directory

                    # Catchall, use the default initial output directory
                    else:
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
        """
        Suggests an output directory based on the selected file's artist.

        Returns:
        - If there is a single match, return the matching artist folder.
        - If matches, returns the list of matching artist folder(s).
        - If no matching artist folder is found or encountered an error, returns None.
        """
        # Check if an input is selected
        if not self.file_renamer_selected_file:
            # If no input is selected, return None
            self.log_and_show("No input selected. Using default initial directory.")
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
                # If multiple matches, return the list
                return matching_artists

            elif len(matching_artists) == 1:
                # If only one match found, return that
                return matching_artists[0]

            else:
                # If no matching artist folder is found, return none
                self.log_and_show("Cannot suggest output directory. Falling back to default output directory.")
                return None

        except Exception as e:
            # Handle any unexpected exceptions and log an error message
            self.log_and_show(f"Unexpected error suggesting an output directory: {e}",
                              create_messagebox=True, error=True)
            return None

    def handle_rename_success(self, new_path: str):
        """
        Handles the success of a file renaming operation.

        Parameters:
        - new_path (str): The new path after the file renaming operation.
        """
        # Store information about the rename operation in the history
        self.history.append({
            'original_path': self.file_renamer_selected_file,
            'new_path': new_path
        })

        # Reset selected file, queue and update file renamer last used file
        self.file_renamer_selected_file = ""
        self.file_renamer_queue = []
        self.file_display_text.set("")
        self.name_length_text.set("")
        self.prefix_text_entry.delete(0, ctk.END)
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
        """
        Add a new category to the dictionary with the specified weight,
        save the updated categories to the file, and refresh the category buttons in the GUI.

        Returns:
            None
        """
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
        """
        Remove a category from the dictionary, save the updated categories to the file,
        and refresh the category buttons in the GUI.

        Returns:
            None
        """
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
            matching_category = next((key for key in self.categories if key.lower() == category_to_remove.lower()),
                                     None)
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
        """
        Create a category button within a specified tab.

        Parameters:
            tab: The tab in which the button will be created.
            category (str): The category for which the button is created.

        Returns:
            ctk.CTkButton: The created category button.
        """
        # Set the category to the button text variable for potential formatting
        button_text = category

        if self.truncate_var.get():
            # Truncate the text after x characters for GUI friendly formatting.
            button_text = f"{category[:13]}..." if len(button_text) > 16 else category

        return ctk.CTkButton(tab, text=button_text, command=lambda c=category: self.add_to_queue(c))

    def refresh_category_buttons(self, *_):
        """
        Refresh the category buttons by destroying existing tabs and buttons,
        loading categories, and creating new tabs and buttons.

        Parameters:
            *_: Variable number of positional arguments (ignored in the function)

        Returns:
            None
        """
        # Destroy existing tabs and buttons
        if hasattr(self, 'cat_tabview') and self.cat_tabview:
            self.cat_tabview.destroy()
        for button in getattr(self, 'buttons', []):
            button.destroy()

        # Load categories from the file or create an empty dictionary
        self.initialize_json()

        # Create the cat_tabview and buttons
        self.create_cat_tabview()

    def create_cat_tabview(self):
        """
        Create the category tabview and populate it with buttons based on category weights.

        Returns:
            None
        """
        # Create cat_tabview
        self.cat_tabview = ctk.CTkTabview(self.cat_button_frame)
        self.cat_tabview.grid(row=0, column=0)

        # Create a tab for all categories
        all_cat_tab = self.cat_tabview.add("All")
        self.cat_tabs["All"] = all_cat_tab  # Store the reference to the tab

        # Create a tab for "Most Categories" with weights 1-9
        most_cat_tab = self.cat_tabview.add("Most")
        self.cat_tabs["Most"] = most_cat_tab  # Store the reference to the tab

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

            self.cat_tabs[weight] = tab  # Store the reference to the tab

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
            # Check if self.default_cat_tab is in the tab names
            if self.default_cat_tab and self.cat_tabview.index(self.default_cat_tab) is not None:
                self.cat_tabview.set(self.default_cat_tab)
        except ValueError:
            return

    def add_to_queue(self, category):
        """
        Add a category to the processing queue.

        Parameters:
            category (str): The category to be added to the queue.

        Returns:
            None
        """
        if not self.file_renamer_selected_file:
            # If no input selected, log the action and display a message in the GUI
            self.log_and_show("Please select an input first and then add a word to the queue.",
                              create_messagebox=True, error=True)
            return

        # Check if the category is not already in the queue
        if category not in self.file_renamer_queue:
            # Add the category to the queue
            self.file_renamer_queue.append(category)
            self.log_and_show(f"Word added to queue: {category}", not_logging=True)

        # Check if the category is already in the queue
        elif category in self.file_renamer_queue:
            # Ask for confirmation of removing the category from the queue
            confirmation = self.ask_confirmation("Queue Conflict",
                                                 f"{category} is already in the queue. Do you want to remove it?")

            if confirmation:
                # Remove the category from the queue
                self.remove_from_queue(category)

        # Update file display
        self.update_file_display()

    def remove_from_queue(self, category, suppress=False):
        """
        remove_from_queue(category, suppress=False)

        Removes a word from the queue based on the specified category.

        Parameters:
        - category (str): The category of the word to be removed from the queue.
        - suppress (bool): If True, suppresses log and show messages when the word is not in the queue.

        Returns:
        None

        If no input file is selected, logs an error and shows a message in the GUI.

        If the specified category is not in the queue, logs an error and shows a message unless suppress is True.

        Updates the file display after removing the word from the queue.
        """
        if not self.file_renamer_selected_file:
            # If no input selected, log the action and display a message in the GUI
            self.log_and_show("Please select an input first and then remove a word from the queue.",
                              create_messagebox=True, error=True)
            return

        # Check if the category is not already in the queue
        if category not in self.file_renamer_queue:
            # Check if the message is suppressed
            if not suppress:
                # If not suppressed, log and show the message
                self.log_and_show(f"Word not in queue: {category}",
                                  create_messagebox=True, error=True, not_logging=True)
            return

        # Remove the category from the queue
        self.file_renamer_queue.remove(category)
        self.log_and_show(f"Word removed from queue: {category}", not_logging=True)

        # Update file display
        self.update_file_display()

    def handle_common_categories_state(self, *_):
        """
        Handle the state change of the artist common categories variable.

        Parameters:
            *_: Variable number of positional arguments (ignored in the function)

        Returns:
            None
        """
        # Check if the artist common categories variable is true
        if self.artist_common_categories_var.get():
            # Call the add_remove_common_categories_to_queue method
            self.add_remove_common_categories_to_queue()
        else:
            # Call the add_remove_common_categories_to_queue method with the remove parameter
            self.add_remove_common_categories_to_queue(remove=True)

    def add_remove_common_categories_to_queue(self, remove=False):
        """
        Add or remove common categories to/from the processing queue based on the selected file.

        Parameters:
            remove (bool): Flag indicating whether to remove common categories from the queue. Default is False.

        Returns:
            None
        """
        # Check if the selected file is set
        if not self.file_renamer_selected_file:
            return  # Do nothing if the selected file is not set

        # Extract the base name from the selected file
        base_name = os.path.basename(self.file_renamer_selected_file)
        base_name_lower = base_name.lower()  # Convert to lowercase for case-insensitive comparison

        # Check if there is a '-' in the name
        if '-' not in base_name_lower:
            # If no '-', return
            self.log_and_show("No '-' found in the file name. Cannot identify artist for Artist Common Categories "
                              "functionality.")
            return

        # Extract the artist from the text before '-'
        artist = base_name_lower.split('-')[0].strip()

        # Iterate through common categories and associated values
        for key, values in self.artist_common_categories.items():
            # Check if the lowercase key is present in the lowercase base name
            if artist.find(key.lower()) != -1:
                # Iterate through the values associated with the matching key
                for value in values:
                    if remove:
                        self.remove_from_queue(value, suppress=True)  # Remove each value from the processing queue
                    else:
                        self.add_to_queue(value)  # Add each value to the processing queue
                return  # Stop processing after the first match

    """
    File Renaming
    """

    def rename_files(self):
        """
        Rename selected files based on user preferences.

        - Gathers data from the GUI, constructs a new name, and handles name length constraints.
        - Moves text between '-' and '__-__' if the move_text_var is set.
        - Determines the new path based on user preferences for output directory.
        - Attempts to rename the file and handles success or errors.

        Raises:
            OSError: If an error occurs during the file renaming process.

        """
        # Check if an input is selected and either the queue is not empty or custom text is provided
        if self.file_renamer_selected_file and (
                self.file_renamer_queue or self.prefix_text_entry.get().strip() or
                self.custom_text_entry.get().strip()):
            # Gather the data from the gui
            (base_name, weighted_categories, prefix_text, custom_text, extension) = self.gather_and_sort()

            # Construct the name
            (name, char_length) = self.construct_new_name(base_name, weighted_categories, prefix_text, custom_text,
                                                          extension)

            # Handle name length constraints
            if char_length > 255:
                self.name_length_handler(char_length)
                return

            # If move_text_var is set, move the text between - and __-__
            if self.move_text_var.get():
                name = self.move_text(name)

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

                    # If suggest output directory returns a result, use SelectOptionWindow to determine output directory
                    if suggested_output_directory:
                        # If suggest output directory is a single result, convert it to a list (sanitize)
                        if suggested_output_directory and not isinstance(suggested_output_directory, list):
                            suggested_output_directory = [suggested_output_directory]
                        # Sanitize the list for display in the GUI
                        basename_list = self.get_basenames(suggested_output_directory)

                        # Prompt the user to choose from the list using SelectOptionWindow
                        chosen_directory = self.selection_window(title="Suggest Output Directory",
                                                                 prompt="Suggested output directory found."
                                                                        "\nDo you want use the suggested output "
                                                                        "directory?"
                                                                        "\nCancel to use default output "
                                                                        "directory.",
                                                                 label_text="Choose Directory",
                                                                 item_list=suggested_output_directory,
                                                                 item_text=basename_list)

                        if chosen_directory in suggested_output_directory:
                            self.output_directory = chosen_directory
                            self.log_and_show(f"User chose the suggested output directory: {chosen_directory}")
                        else:
                            # If the user did not select the suggested directory, use the previously set output
                            # directory
                            self.log_and_show(
                                "User did not choose the suggested output directory. Falling back to default "
                                "directory.")

                    elif suggested_output_directory is None:
                        # If suggest output directory returns none, use the previously set output directory
                        # Log the result and update the GUI
                        self.log_and_show(f"Suggest output directory returned no result. Using {self.output_directory}")

                    # Catchall, use the previously set output directory
                    else:
                        # Log the result and update the GUI
                        self.log_and_show(f"Suggest output directory could not function due to invalid return"
                                          f" '{suggested_output_directory}'."
                                          f"\nUsing {self.output_directory}")

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

                # Check if Artist Search is true
                if self.artist_search_var.get():
                    # Use artist search to find other instances of artists in files outside the current folder
                    identified = self.artist_search()

                    if identified:
                        # Unpack the tuple
                        (artist, artist_file_path) = identified

                        # Log the result and display a messagebox to the user
                        self.log_and_show(f"Artist Search identified {artist} outside the current folder: "
                                          f"\n\nFile name: {artist}"
                                          f"\n{os.path.basename(artist_file_path)} "
                                          f"\n\nFile path: "
                                          f"\n{artist_file_path}",
                                          create_messagebox=True)
                    else:
                        # Log the action
                        self.log_and_show(f"No Artist Search result")

                # Rename the file
                os.rename(self.file_renamer_selected_file, str(new_path))
                self.log_and_show(f"File: '{os.path.basename(self.file_renamer_selected_file)}' renamed successfully. "
                                  f"\nSaved to: \n{new_path}")
                self.handle_rename_success(new_path)

            except OSError as e:
                if "Invalid cross-device link" in str(e):
                    # Attempt to use shutil.move if "Invalid cross-device link" error
                    try:
                        shutil.move(self.file_renamer_selected_file, str(new_path))
                        self.log_and_show(
                            f"File: '{os.path.basename(self.file_renamer_selected_file)}' renamed and moved "
                            f"successfully."
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
        elif self.file_renamer_selected_file and not (
                self.file_renamer_queue or self.prefix_text_entry.get().strip() or
                self.custom_text_entry.get().strip()):
            # Log the action if logging is enabled
            self.log_and_show("Input selected but nothing added to the queue. Nothing to rename.",
                              create_messagebox=True, error=True)
        # If no input is selected, show error
        elif not self.file_renamer_selected_file:
            # Log the action if logging is enabled
            self.log_and_show("No input selected. Nothing to rename.", create_messagebox=True, error=True)

    def gather_and_sort(self) -> tuple:
        """
        Gather information from the gui and sort categories based on weights.

        Returns:
        tuple: A tuple containing base_name, categories_text, prefix_text, custom_text, and extension.
        """

        # Get custom text, prefix_text, basename, and file extension
        prefix_text = self.prefix_text_entry.get().strip()
        custom_text = self.custom_text_entry.get().strip()
        base_name, extension = os.path.splitext(os.path.basename(self.file_renamer_selected_file))

        # Filter categories that are both in file_renamer_queue and categories
        weighted_categories = [category for category in self.file_renamer_queue if category in self.categories]

        # Sort the weighted_categories based on their weights in the categories dictionary
        # Use default weight if one isn't present
        weighted_categories.sort(key=lambda category: self.categories.get(category, self.default_weight))

        # Create a new list containing non-weighted categories from file_renamer_queue
        categories = weighted_categories + [category for category in self.file_renamer_queue if
                                            category not in weighted_categories]

        # Join the categories list into a space-separated string and strip any leading or trailing whitespaces
        categories_text = ' '.join(categories).strip()

        # Return a tuple containing the data
        return base_name, categories_text, prefix_text, custom_text, extension

    def construct_new_name(self, base_name: str, categories_text: str, prefix_text: str, custom_text: str,
                           extension: str) -> tuple:
        """
        Construct a new file name based on specified parameters.

        Args:
        base_name (str): The original base name of the file.
        categories_text (str): Space-separated string containing categories sorted based on weights.
        prefix_text (str): Custom prefix text.
        custom_text (str): Custom text.
        extension (str): File extension.

        Returns:
        tuple: A tuple containing the constructed new file name and its length.
        """
        # Place the queue at the beginning of the name
        if self.placement_choice.get() == "prefix":
            name = f"{prefix_text} {custom_text} {categories_text} {base_name}".strip()
        # Place the queue at the first instance of the special character
        elif self.placement_choice.get() == "special_character":
            parts = base_name.split(self.special_character_var, 1)
            if len(parts) == 2:
                name = f"{prefix_text} {parts[0].rstrip()} {categories_text} {custom_text} {parts[1].lstrip()}".strip()
                try:
                    # Remove the tail __-__ if found
                    name = name.replace("__-__", "")
                except OSError as e:
                    # Log the action if logging is enabled
                    self.log_and_show(f"{str(e)}", create_messagebox=True, error=True)
            else:
                # If there's no special character found, fallback to edge case custom formatting
                name = f"{prefix_text} {categories_text} {custom_text} {base_name}".strip()
        else:  # Default to suffix
            name = f"{prefix_text} {base_name} {categories_text} {custom_text}".strip()

        # Remove extra whitespaces from the name
        name = " ".join(name.split()).strip()

        # Construct the name by adding the base_name and extension
        name = name + extension

        # Get the length of the name
        name_length = len(name)

        return name, name_length

    def get_non_conflicting_filename(self, path):
        """
        Get a non-conflicting filename by appending a counter to the base filename if conflicts are detected.

        Args:
        - path (str): The original file path.

        Returns:
        - str: The non-conflicting filename or None if an error occurs.

        Raises:
        - OSError: If an error occurs while checking for file existence or constructing the new filename.

        Examples:
        self.get_non_conflicting_filename("/path/to/file.txt")
        '/path/to/file (1).txt'

        self.get_non_conflicting_filename("/path/to/file (1).txt")
        '/path/to/file (2).txt'
        """
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
            self.log_and_show(f"Getting non-conflicting file name failed: {str(e)}", create_messagebox=True,
                              error=True)

            # Return None in case of an error.
            return None

    @staticmethod
    def move_text(name: str) -> str:
        """
        Move the text between '-' and '__-__' in the given name.

        Args:
        - name (str): The original name containing the text to be moved.

        Returns:
        - str: The modified name with the text moved.

        Example:
        self.move_text("Artist - words to move__-__file.mp3")
        'Artist file words to move.mp3'
        """
        # Move the text between - and __-__ in the name
        match = re.match(r"^(.*) - (.*?)__-__ (.*)\.(\w+)$", name)
        if match:
            prefix, moved_text, suffix, extension = match.groups()
            name = f"{prefix} {suffix} {moved_text}.{extension}"
        return name

    """
    Name Normalizer
    """

    def remove_custom_user_text(self, name: str) -> str:
        """
        Remove custom user-specified text from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with custom user text removed.
        """
        try:
            # Get the text to remove from the entry
            text_to_remove = self.custom_text_removal_entry.get().strip()
        except Exception as e:
            self.log_and_show(f"An error occurred getting the custom text to remove: {str(e)}",
                              create_messagebox=True,
                              error=True)
            return name

        # Check if text to remove is provided
        if text_to_remove:
            if self.replace_mode_var.get():
                # Check if the text to remove is present in name (case-insensitive)
                pattern = re.compile(re.escape(text_to_remove), re.IGNORECASE)

                # Remove all instances of the text to remove from name
                name = pattern.sub('', name)

                # Replace consecutive spaces with a single space when custom text is removed
                name = re.sub(r'\s+', ' ', name)
            else:
                # Check if the text to remove is present in name (case-sensitive)
                if text_to_remove in name:
                    # Remove all instances of the text to remove from name
                    name = name.replace(text_to_remove, '')

                    # Replace consecutive spaces with a single space when custom text is removed
                    name = re.sub(r'\s+', ' ', name)

        return name

    def remove_custom_text(self, name: str) -> str:
        """
        Remove custom text from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with custom text removed or replaced.
        """
        # Remove custom text from the custom_text_to_replace dictionary
        if self.replace_mode_var.get():
            for text_to_replace, replacement in self.custom_text_to_replace.items():
                # Check if the text to remove is present in name (case-insensitive)
                pattern = re.compile(re.escape(text_to_replace), re.IGNORECASE)

                # Replace the text with the specified replacement or remove if replacement is an empty string
                name = pattern.sub(replacement, name) if replacement != "" else pattern.sub('', name)
        else:
            # Check if the text to remove is present in name (case-sensitive)
            for text_to_replace, replacement in self.custom_text_to_replace.items():
                # Replace the text with the specified replacement or remove if replacement is an empty string
                name = name.replace(text_to_replace, replacement) if replacement != "" else name.replace(
                    text_to_replace, '')

        # Replace consecutive spaces with a single space when custom text is removed
        name = re.sub(r'\s+', ' ', name)

        return name

    @staticmethod
    def remove_non_ascii_symbols(name: str) -> str:
        """
        Remove non-ASCII symbols from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with non-ASCII symbols removed.
        """
        # Get all printable ASCII characters
        standard_chars = set(string.printable)

        # Replace non-ASCII characters with their ASCII equivalents (ignore slashes)
        name = ''.join(unidecode(char) if char not in standard_chars and char not in ['⁄', '／']
                       else char if char not in ['⁄', '／'] else ' ' for char in name)
        return name

    @staticmethod
    def remove_symbols(name, remove_chars):
        """
        Remove specified symbols from the provided name.

        Args:
        name (str): The original name.
        remove_chars (str): The characters to be removed from the name.

        Returns:
        str: The modified name with specified symbols removed.
        """
        for char in remove_chars:
            name = name.replace(char, "")
        return name

    @staticmethod
    def remove_numbers(name: str) -> str:
        """
        Remove all numbers from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with numbers removed.
        """
        name = ''.join(char for char in name if not char.isdigit())
        return name

    @staticmethod
    def remove_text_trailing(name, symbol):
        """
        Remove text in parentheses and trailing text.

        Args:
        name (str): The original name.
        symbol (str): The symbol indicating the beginning of the trailing text.

        Returns:
        str: The modified name with trailing text removed.
        """
        index = name.find(symbol)
        if index != -1:
            name = name[:index].strip()
        return name

    @staticmethod
    def remove_dashes(name: str) -> str:
        """
        Remove dashes from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with dashes removed.
        """
        name = re.sub(r'-', '', name)
        return name

    @staticmethod
    def remove_endashes(name: str) -> str:
        """
        Remove endashes from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with endashes removed.
        """
        name = re.sub(r'–', '', name)
        return name

    @staticmethod
    def remove_emdashes(name: str) -> str:
        """
        Remove emdashes from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with emdashes removed.
        """
        name = re.sub(r'—', '', name)
        return name

    @staticmethod
    def remove_ampersands(name: str) -> str:
        """
        Remove ampersands from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with ampersands removed.
        """
        name = re.sub(r'&', '', name)
        return name

    @staticmethod
    def remove_at_symbols(name: str) -> str:
        """
        Remove at symbols from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with at symbols removed.
        """
        name = re.sub(r'@', '', name)
        return name

    @staticmethod
    def remove_underscores(name: str) -> str:
        """
        Remove underscores from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with underscores replaced by spaces.
        """
        name = name.replace('_', ' ')
        return name

    @staticmethod
    def remove_commas(name: str) -> str:
        """
        Remove commas from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with commas removed.
        """
        name = name.replace(',', '')
        return name

    @staticmethod
    def remove_single_quotes(name: str) -> str:
        """
        Remove single quotes from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with single quotes removed.
        """
        name = name.replace('\'', '')
        return name

    @staticmethod
    def remove_double_quotes(name: str) -> str:
        """
        Remove double quotes from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with double quotes removed.
        """
        name = name.replace('\"', '')
        return name

    @staticmethod
    def remove_colons(name: str) -> str:
        """
        Remove colons from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with colons removed.
        """
        name = name.replace(':', '')
        return name

    @staticmethod
    def remove_semicolons(name: str) -> str:
        """
        Remove semicolons from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with semicolons removed.
        """
        name = name.replace(';', '')
        return name

    @staticmethod
    def remove_percents(name: str) -> str:
        """
        Remove percents from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with percents removed.
        """
        name = name.replace('%', '')
        return name

    @staticmethod
    def remove_carets(name: str) -> str:
        """
        Remove carets from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with carets removed.
        """
        name = name.replace('^', '')
        return name

    @staticmethod
    def remove_parenthesis(name: str) -> str:
        """
        Remove parenthesis from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with parenthesis removed.
        """
        name = name.replace('(', '').replace(')', '')
        return name

    @staticmethod
    def remove_hashtags(name: str) -> str:
        """
        Remove hashtags from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with hashtags removed.
        """
        name = name.replace('#', '')
        return name

    @staticmethod
    def remove_dollar_signs(name: str) -> str:
        """
        Remove dollar signs from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with dollar signs removed.
        """
        name = name.replace('$', '')
        return name

    @staticmethod
    def remove_asterisks(name: str) -> str:
        """
        Remove asterisks from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with asterisks removed.
        """
        name = name.replace('*', '')
        return name

    @staticmethod
    def remove_plus_signs(name: str) -> str:
        """
        Remove plus signs from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with plus signs removed.
        """
        name = name.replace('+', '')
        return name

    @staticmethod
    def remove_equal_signs(name: str) -> str:
        """
        Remove equal signs from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with equal signs removed.
        """
        name = name.replace('=', '')
        return name

    @staticmethod
    def remove_curly_braces(name: str) -> str:
        """
        Remove curly braces from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with curly braces removed.
        """
        name = name.replace('{', '').replace('}', '')
        return name

    @staticmethod
    def remove_square_brackets(name: str) -> str:
        """
        Remove square brackets from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with square brackets removed.
        """
        name = name.replace('[', '').replace(']', '')
        return name

    @staticmethod
    def remove_pipes(name: str) -> str:
        """
        Remove pipes from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with pipes removed.
        """
        name = name.replace('|', '')
        return name

    @staticmethod
    def remove_backslashes(name: str) -> str:
        """
        Remove backslashes from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with backslashes removed.
        """
        name = name.replace('\\', '')
        return name

    @staticmethod
    def remove_angle_brackets(name: str) -> str:
        """
        Remove angle brackets from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with angle brackets removed.
        """
        name = name.replace('<', '').replace('>', '')
        return name

    @staticmethod
    def remove_question_marks(name: str) -> str:
        """
        Remove question marks from the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with question marks removed.
        """
        name = name.replace('?', '')
        return name

    @staticmethod
    def title_the_name(name: str) -> str:
        """
        Make the file name a title while preserving lowercase letters after apostrophes in contractions.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with title case.
        """
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
        return name

    @staticmethod
    def remove_extra_whitespace(name: str) -> str:
        """
        Sanitize the filename by removing extra whitespaces.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with extra whitespaces removed.
        """
        name = ' '.join(name.split())
        return name

    def artist_identifier(self, name: str) -> str:
        """
        Identify artists in the given filename and modify the filename accordingly.

        Args:
            name (str): The original filename to be processed.

        Returns:
            str: The modified filename with artist information.

        Raises:
            FileNotFoundError: If the artist file specified is not found.
            Exception: For any other unexpected errors during the artist identification process.

        """
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

            # Check if remove_artist_duplicates_var is set
            if self.remove_artist_duplicates_var.get():
                # Call the remove_artist_duplicates_from_filename function to modify name
                name = self.remove_artist_duplicates_from_filename(str(name))
        except FileNotFoundError:
            self.log_and_show(f"File not found: {self.artist_file}", create_messagebox=True, error=True)
        except Exception as e:
            self.log_and_show(f"Artist Identifier failed {self.artist_file}: {e}", create_messagebox=True,
                              error=True)
        return name

    @staticmethod
    def add_tail(name: str) -> str:
        """
        Add a tail to the end of the provided name.

        Args:
        name (str): The original name.

        Returns:
        str: The modified name with the added tail.
        """
        # Add tail to the end of the name
        name += "__-__ "

        # Catchall for situations where only "artist -__-__" is present after operation
        name = re.sub(r' -__-__', '', name).strip()

        # Catchall for situations where the tail is already present "__-____-__"
        name = re.sub(r'__-____-__', '__-__', name).strip()
        return name

    def remove_artist_duplicates_from_filename(self, file_name: str) -> str:
        """
        Remove artist names from the given file name by processing the list of artists
        read from the artist_file and modifying the file name accordingly. The intent is to give the user the option
        to maintain the rest of the original file name after the Artist Identifier, or remove the now duplicate entries
        for a clean file name.

        Parameters:
            file_name (str): The original file name.

        Returns:
            str: The modified file name with artist names removed.

        Example:
            self.remove_artist_duplicates_from_filename('Artist - A Title Artist - Album Version Artist')
            'Artist - A Title - Album Version'
        """
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

        # Sanitize file name. Remove extra whitespace.
        new_file_name = ' '.join(new_file_name.split()).strip()

        # Check for double dashes and remove the second dash
        if ' - - ' in new_file_name:
            new_file_name = new_file_name.replace(' - - ', ' - ', 1)

        return new_file_name

    def preview_name(self, file_path):
        """
        Preview the modified file name based on various user settings.

        Parameters:
            file_path (str): The path of the file.

        Returns:
            str: The modified file name.
        """
        # Split the file path into directory path and filename
        dir_path, filename = os.path.split(file_path)
        name, ext = os.path.splitext(filename)

        if ext.lower() not in self.file_extensions:
            # Log that the input is ignored if not on the file extensions list
            self.log_and_show(f"Ignored: {filename} (not on file extensions list)")

        # Check if the input has one of the video file extensions
        if ext.lower() in self.file_extensions:
            # Remove custom text provided by the user
            name = self.remove_custom_user_text(name)

            if self.remove_non_ascii_symbols_var.get():
                # Remove non-ASCII characters
                name = self.remove_non_ascii_symbols(name)

            if self.remove_all_symbols_var.get():
                # Define the characters to be removed
                all_symbols = ",;:@$%^&#*+=(){}[]|\\<>\'\"?_-–—"

                # Remove the symbols
                name = self.remove_symbols(name, all_symbols)

            if self.remove_most_symbols_var.get():
                # Define the characters to be removed
                most_symbols = ",;:@$%^&*+={}[]|\\<>\"?-–—"

                # Remove the symbols
                name = self.remove_symbols(name, most_symbols)

            if self.remove_number_var.get():
                # Remove all numbers from the name
                name = self.remove_numbers(name)

            if self.remove_hashtag_trail_var.get():
                # Remove the # and trailing text
                name = self.remove_text_trailing(name, "#")

            if self.remove_parenthesis_trail_var.get():
                # Remove the ( and trailing text
                name = self.remove_text_trailing(name, "(")

            if self.remove_dash_var.get():
                # Remove dashes
                name = self.remove_dashes(name)

            if self.remove_endash_var.get():
                # Remove endashes
                name = self.remove_endashes(name)

            if self.remove_emdash_var.get():
                # Remove emdashes
                name = self.remove_emdashes(name)

            if self.remove_ampersand_var.get():
                # Remove ampersands
                name = self.remove_ampersands(name)

            if self.remove_at_var.get():
                # Remove at symbols
                name = self.remove_at_symbols(name)

            if self.remove_underscore_var.get():
                # Remove underscores
                name = self.remove_underscores(name)

            if self.remove_comma_var.get():
                # Remove commas
                name = self.remove_commas(name)

            if self.remove_single_quote_var.get():
                # Remove single quotes
                name = self.remove_single_quotes(name)

            if self.remove_double_quote_var.get():
                # Remove double quotes
                name = self.remove_double_quotes(name)

            if self.remove_colon_var.get():
                # Remove colons
                name = self.remove_colons(name)

            if self.remove_semicolon_var.get():
                # Remove semicolons
                name = self.remove_semicolons(name)

            if self.remove_percent_var.get():
                # Remove percents
                name = self.remove_percents(name)

            if self.remove_caret_var.get():
                # Remove carets
                name = self.remove_carets(name)

            if self.remove_parenthesis_var.get():
                # Remove parenthesis
                name = self.remove_parenthesis(name)

            if self.remove_hashtag_var.get():
                # Remove hashtags
                name = self.remove_hashtags(name)

            if self.remove_dollar_var.get():
                # Remove dollars
                name = self.remove_dollar_signs(name)

            if self.remove_asterisk_var.get():
                # Remove asterisks
                name = self.remove_asterisks(name)

            if self.remove_plus_var.get():
                # Remove plus signs
                name = self.remove_plus_signs(name)

            if self.remove_equal_var.get():
                # Remove equal signs
                name = self.remove_equal_signs(name)

            if self.remove_curly_brace_var.get():
                # Remove curly braces
                name = self.remove_curly_braces(name)

            if self.remove_square_bracket_var.get():
                # Remove square brackets
                name = self.remove_square_brackets(name)

            if self.remove_pipe_var.get():
                # Remove pipes
                name = self.remove_pipes(name)

            if self.remove_backslash_var.get():
                # Remove backslashes
                name = self.remove_backslashes(name)

            if self.remove_angle_bracket_var.get():
                # Remove angle brackets
                name = self.remove_angle_brackets(name)

            if self.remove_question_mark_var.get():
                # Remove question marks
                name = self.remove_question_marks(name)

            if self.title_var.get():
                # Make file name a title while preserving lowercase letters after apostrophes in contractions
                name = self.title_the_name(name)

            if self.remove_custom_text_var.get():
                # Remove custom text from the custom_text_to_replace dictionary
                name = self.remove_custom_text(name)

            if self.artist_identifier_var.get():
                # Process artist names to place identified artist(s) at the beginning
                name = self.artist_identifier(name)

            if self.remove_extra_whitespace_var.get():
                # Remove extra white space
                name = self.remove_extra_whitespace(name)

            if self.tail_var.get():
                # Add tail
                name = self.add_tail(name)

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

    def rename_and_move_file(self, file_path):
        """
        Rename the given file based on the user-defined settings and move it to a specified directory if provided.

        Parameters:
            file_path (str): The path of the file to be renamed.

        Returns:
            tuple: A tuple containing the original file path and the final file path after renaming and, if applicable,
            moving.
        """
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
                        self.log_and_show(
                            f"Moved: {os.path.basename(new_path)} -> {os.path.basename(destination_file)}")
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

    def process_name_normalizer(self, mode):
        """
        Process the name normalization based on the specified mode.

        Parameters:
            mode (str): The mode indicating whether to preview or take action on the file(s).

        Returns:
            None
        """
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

        # Check if artist identifier is enabled
        if self.artist_identifier_var.get():
            # Check if artist file is not provided
            if not self.artist_file:
                # Log and display an error message
                self.log_and_show(
                    "No artist file provided. Please provide one and try again, or turn off Artist Identifier.",
                    create_messagebox=True, error=True)
                return
            # Check if artist file does not exist
            elif not os.path.exists(self.artist_file):
                # Log and display an error message
                self.log_and_show(f"The artist file does not exist: '{self.artist_file}'"
                                  f"\nPlease ensure the provided Artist File exists, "
                                  f"\nor turn off Artist Identifier to proceed.\nSee FAQ",
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
                # If a single file is provided, use threading to directly process it
                self.name_processing_thread_single = threading.Thread(target=self.process_single_file,
                                                                      args=(self.name_normalizer_selected_file,)
                                                                      ).start()
            else:
                # Get folder contents and use threading to process the files
                self.name_processing_thread_multiple = threading.Thread(target=self.process_folder,
                                                                        args=(self.name_normalizer_selected_file,)
                                                                        ).start()

        except Exception as e:
            # Display error message if an exception occurs
            self.log_and_show(f"An error occurred: {e}", create_messagebox=True, error=True)

    def process_single_file(self, file_path):
        """
        Process a single file using the Name Normalizer function.

        Args:
            file_path (str): The path of the file to be processed.

        Returns:
            None

        """
        try:
            # Start the progress bar for the Name Normalizer function
            self.start_progress(self.progressbar, self.slider_progressbar_frame)

            # Rename and move the file, obtaining original and new paths
            original_path, new_path = self.rename_and_move_file(file_path)

            # Check if the tuple is the same to prevent no operations from being added to history
            if original_path != new_path:
                # Append the operation to the history
                self.queue.put({
                    'original_paths': [original_path],
                    'new_paths': [new_path]
                })

            # Log the action if logging is enabled
            self.log_and_show("File has been processed successfully.")

            # Stop the progress bar for the Name Normalizer function
            self.stop_progress(self.progressbar)

            # Reset GUI input fields if reset is True
            if self.reset_var.get():
                # Clear selection for the name_normalizer_window
                self.clear_selection(frame_name="name_normalizer_window")

            # Schedule the next check after 100 milliseconds
            self.after(100, self.check_queue)

        except Exception as e:
            # Handle unexpected exceptions and log an error message
            self.log_and_show(f"Error processing file {file_path}: {e}", create_messagebox=True, error=True)
            # Stop the progress bar in case of an error
            self.stop_progress(self.progressbar)

    def process_folder(self, folder_path: str) -> None:
        """
        Process all files in a folder using the Name Normalizer function.

        Args:
            folder_path (str): The path of the folder to be processed.

        Returns:
            None

        """
        try:
            # Start the progress bar for the Name Normalizer function
            self.start_progress(self.progressbar, self.slider_progressbar_frame)

            # Initialize an empty list to store file paths
            file_paths = []
            original_paths = []
            new_paths = []

            # Log the os.walk state
            if self.deep_walk_var.get():
                deep_walk_status = "including subdirectories"
            else:
                deep_walk_status = "excluding subdirectories"

            self.log_and_show(
                f"Info: os.walk, {deep_walk_status}, started on '{folder_path}'")

            # Traverse through the folder using os.walk
            for root, dirs, files in os.walk(folder_path):
                # Include subdirectories if the deep_walk_var is True or the root folder is selected
                if self.deep_walk_var.get() or root == folder_path:
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

                        # Check if processing should be interrupted
                        if self.interrupt_name_processing_thread_var:
                            break  # Break out of the loop

                    # Append the batch operation to the name normalizer history
                    self.queue.put({
                        'original_paths': original_paths,
                        'new_paths': new_paths
                    })

            if self.interrupt_name_processing_thread_var:
                # Log the action if logging is enabled
                self.log_and_show("User interrupted the process. File(s) have not been processed successfully.",
                                  error=True)
            else:
                # Log the action if logging is enabled
                self.log_and_show("File(s) have been processed successfully.")

            # Stop the progress bar for the Name Normalizer function
            self.stop_progress(self.progressbar)

            # Reset GUI input fields if reset is True
            if self.reset_var.get():
                # Clear selection for the name_normalizer_window
                self.clear_selection(frame_name="name_normalizer_window")

            # Reset the variable back to false
            self.interrupt_name_processing_thread_var = False

            # Schedule the next check after 100 milliseconds
            self.after(100, self.check_queue)

        except Exception as e:
            # Handle unexpected exceptions and log an error message
            self.log_and_show(f"Error processing folder {folder_path}: {e}", create_messagebox=True, error=True)
            # Stop the progress bar in case of an error
            self.stop_progress(self.progressbar)

    def check_queue(self):
        """
        Check the queue for results from the Name Normalizer process.

        This method is responsible for continuously checking the queue for results from the Name Normalizer process.
        It retrieves results from the queue and appends them to the `nn_history` list.

        Returns:
            None

        """
        try:
            while True:
                result = self.queue.get_nowait()
                self.nn_history.append(result)
        except queue.Empty:
            pass

        # Schedule the next check after 100 milliseconds
        self.after(100, self.check_queue)

    # Method to interrupt processing
    def interrupt_processing(self, thread_name: str):
        """
        Set interruption flags to stop processing for the specified thread.

        Args:
        - thread_name (str): The name of the thread to interrupt.
        """
        if thread_name == "name_processing_thread":
            self.interrupt_name_processing_thread_var = True
        elif thread_name == "video_processing_thread":
            self.interrupt_video_processing_thread_var = True
        elif thread_name == "all":
            self.interrupt_name_processing_thread_var = True
            self.interrupt_video_processing_thread_var = True
        else:
            self.log_and_show(f"Thread {thread_name} is not running, cannot interrupt.",
                              create_messagebox=True, error=True)

    """
    Video Editor
    """

    def rotate_video(self, clip, rotation_angle):
        """
        Rotate or mirror a video clip.

        Parameters:
            clip (VideoClip): The input video clip to be rotated or mirrored.
            rotation_angle (Union[int, str]): The angle by which to rotate the video
                (e.g., 90, 180, 270) or "mirror" to mirror the video along the horizontal axis.

        Returns:
            VideoClip or None: The rotated or mirrored video clip if successful, or None in case of an error.
        """
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

    def increase_volume(self, clip, increase_db):
        """
        Increase the volume of a video clip.

        Parameters:
            clip (VideoClip): The input video clip to be modified.
            increase_db (float): The amount by which to increase the volume in decibels.

        Returns:
            VideoClip or None: The modified video clip with increased volume if successful,
            or None in case of an error.
        """
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

    def normalize_audio(self, clip, volume_multiplier):
        """
        Normalize the audio of a video clip.

        Parameters:
            clip (VideoClip): The input video clip with audio to be normalized.
            volume_multiplier (float): The multiplier to adjust the audio volume.

        Returns:
            VideoClip or None: The video clip with normalized audio if successful,
            or None in case of an error.
        """
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

    def trim_video(self, clip, front_trim=0, back_trim=0):
        """
        Trim a video clip by removing specified durations from the front and/or back.

        Parameters:
            clip (VideoClip): The input video clip to be trimmed.
            front_trim (float): Duration to trim from the front in seconds.
            back_trim (float): Time to start the end trim in seconds.

        Returns:
            VideoClip or None: The trimmed video clip if successful, or None in case of an error.
        """
        try:
            # Calculate the start and end times for trimming
            start_time = front_trim
            end_time = back_trim if back_trim > 0 else None

            # Trim the clip
            trimmed_clip = clip.subclip(start_time, end_time)

            # Log normalization success if logging is activated.
            self.log_and_show(f"Trimming successful. Front: {front_trim} seconds, Back: {back_trim} seconds")

            # Return the trimmed video clip.
            return trimmed_clip

        except Exception as e:
            # Log error and display an error message if trimming fails.
            self.log_and_show(f"Trimming failed: {str(e)}", create_messagebox=True, error=True)

            # Return None in case of an error.
            return None

    def gather_and_validate_entries(self):
        """
        Gather and validate user inputs for video editing operations.

        This function retrieves input parameters from the user interface, such as rotation, decibel,
        audio normalization, minutes, and seconds. It then checks the provided input file or directory,
        validates parameters, and performs video edits based on the selected operations.

        Returns:
            None
        """
        try:
            # Get input parameters from user interface.
            rotation = str(self.rotation_var.get())
            decibel = float(self.decibel_entry.get().strip())
            audio_normalization = float(self.audio_normalization_entry.get().strip())
            minutes = int(self.minute_entry.get().strip())
            seconds = int(self.second_entry.get().strip())
            minutes1 = int(self.minute_entry1.get().strip())
            seconds1 = int(self.second_entry1.get().strip())
        except ValueError as e:
            self.log_and_show(
                f"Value error: Please enter a valid value (integer or float) into the entry field. {str(e)}",
                create_messagebox=True, error=True)
            return

        # Adjust minutes and seconds
        adjusted_minutes = minutes if minutes != 0 else 0
        adjusted_seconds = seconds if seconds != 0 else 0

        # Convert time to seconds
        total_start_time = adjusted_minutes * 60 + adjusted_seconds

        # Adjust minutes1 and seconds1
        adjusted_minutes1 = minutes1 if minutes1 != 0 else 0
        adjusted_seconds1 = seconds1 if seconds1 != 0 else 0

        # Convert time to seconds
        total_end_time = adjusted_minutes1 * 60 + adjusted_seconds1

        total_time = total_start_time + total_end_time

        # If there is nothing to trim, set trim to False
        trim = total_time != 0
        rotation = None if rotation == "none" else rotation
        decibel = None if decibel == 0.0 else decibel
        audio_normalization = None if audio_normalization == 0.0 else audio_normalization

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

        # Input validation
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
        if not any((decibel, rotation, audio_normalization, minutes, seconds, minutes1, seconds1)):
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
            if os.path.isfile(self.video_editor_selected_file) and self.video_editor_selected_file.lower().endswith(
                    tuple(self.valid_extensions)):
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
                                                     "Are you sure you want edit ALL video files in the provided "
                                                     "directory?"
                                                     "\nThis option may be computer intensive.")
                if confirmation:
                    self.log_and_show(f"User confirmed the directory for {self.video_editor_selected_file}.")

                    # Get the absolute file paths of all files within the directory with valid extensions
                    input_paths = [os.path.join(root, file) for root, _, files in
                                   os.walk(self.video_editor_selected_file)
                                   for file in files if os.path.splitext(file)[1].lower() in self.valid_extensions]
                else:
                    # If the user does not confirm the directory, return
                    return

            else:
                raise ValueError("Invalid input detected. Please select a video file, .txt file with video file paths, "
                                 "or a directory with video files")
        except Exception as e:
            self.log_and_show(f"Processing input failed: {str(e)}", create_messagebox=True, error=True)
            return

        # Process the input(s)
        self.video_processing_thread = threading.Thread(target=self.process_video_paths,
                                                        args=(audio_normalization, decibel, input_paths, rotation_angle,
                                                              total_start_time, total_end_time, trim,)).start()

    def process_video_paths(self, audio_normalization: float, decibel: float, input_paths: list,
                            rotation_angle, total_start_time: int, total_end_time: int, trim: bool):
        """
        Process a list of video paths with specified video editing operations.

        Args:
        - audio_normalization (float): Audio normalization adjustment in decibels.
        - decibel (float): Audio volume adjustment in decibels.
        - input_paths (list): List of input video file paths to be processed.
        - rotation_angle (float): Rotation angle in degrees.
        - total_start_time (int): Total time duration for video trimming from the start.
        - total_end_time (int): Total time duration for video trimming from the end.
        - trim (bool): Flag indicating whether to trim the video.

        Notes:
        - Redirects MoviePy output for video edits.
        - Applies specified video editing operations to each input video.
        - Logs the outcome of each operation.
        - Resets redirect MoviePy output for video edits after processing.
        - If a temporary copy is created due to filename length constraints, it is deleted after 
        processing.
        """
        # Redirect MoviePy output for video edits
        self.redirect_output()

        # Start the progress bar for the Name Normalizer function
        self.start_progress(self.progressbar1, self.slider_progressbar_frame1)

        # Process each input path
        for input_path in input_paths:
            # Check if processing should be interrupted
            if self.interrupt_video_processing_thread_var:
                # Log the action if logging is enabled
                self.log_and_show("User interrupted the process. Video(s) have not been processed successfully.",
                                  error=True)
                # Reset the variable to false
                self.interrupt_video_processing_thread_var = False
                break  # Break out of the loop

            try:
                # Initialize the temp copy exists variable to False
                temp_copy_exists = False

                # Check if the file name length exceeds the upper limit of characters
                if len(os.path.basename(input_path)) > 228:
                    self.log_and_show(f"Long file name length detected. Video will be saved as 'temp_EDITED'."
                                      f"\nOriginal File: {input_path}", error=True)

                    # Create a temporary copy of the file
                    temp_dir = os.path.dirname(input_path)
                    temp_copy_path = os.path.join(temp_dir, 'temp.mp4')
                    shutil.copyfile(input_path, temp_copy_path)
                    temp_copy_exists = True
                else:
                    temp_copy_path = input_path

                # Extract filename, extension, and output directory
                filename, extension = os.path.splitext(os.path.basename(temp_copy_path))
                output_dir = os.path.dirname(temp_copy_path)

                # Create the output path with the operation suffix
                output_path = os.path.join(output_dir, f"{filename}_EDITED{extension}")

                # Adjust output path if a video output directory is specified
                if self.video_editor_output_directory:
                    output_path = os.path.join(self.video_editor_output_directory, os.path.basename(output_path))

                # Get a non-conflicting name for the output path if it exists
                if os.path.exists(output_path):
                    output_path = self.get_non_conflicting_filename(output_path)

                # Load the original video clip
                original_clip = VideoFileClip(temp_copy_path)
                successful_operations = True

                # Apply operations in sequence, checking for success
                if rotation_angle is not None and successful_operations:
                    processed_clip = self.rotate_video(original_clip, rotation_angle)
                    successful_operations = processed_clip is not None
                    original_clip = processed_clip if successful_operations else original_clip

                if decibel and successful_operations:
                    processed_clip = self.increase_volume(original_clip, decibel)
                    successful_operations = processed_clip is not None
                    original_clip = processed_clip if successful_operations else original_clip

                if audio_normalization and successful_operations:
                    processed_clip = self.normalize_audio(original_clip, audio_normalization)
                    successful_operations = processed_clip is not None
                    original_clip = processed_clip if successful_operations else original_clip

                if trim and successful_operations:
                    if total_start_time and not total_end_time:
                        processed_clip = self.trim_video(original_clip, front_trim=total_start_time)
                    elif not total_start_time and total_end_time:
                        processed_clip = self.trim_video(original_clip, back_trim=total_end_time)
                    elif total_start_time and total_end_time:
                        processed_clip = self.trim_video(original_clip, front_trim=total_start_time,
                                                         back_trim=total_end_time)
                    else:
                        processed_clip = None

                    successful_operations = processed_clip is not None
                    original_clip = processed_clip if successful_operations else original_clip

                # Write the final modified clip to the output path if all operations were successful
                if successful_operations:
                    original_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

                    # Set the video editor last used file upon success
                    self.video_editor_last_used_file = output_path

                    if self.reset_video_entries_var.get():
                        # Clear selection for the video_editor_window
                        self.clear_selection(frame_name="video_editor_window")

                    # Check if remove successful lines is true and the input is a txt file
                    if (self.remove_successful_lines_var.get() and
                            self.video_editor_selected_file.lower().endswith('.txt')):
                        # Remove the successfully processed line from the input file
                        self.remove_successful_line_from_file(self.video_editor_selected_file, input_path)

                    # Log the action if logging is enabled
                    self.log_and_show(f"Video saved as {os.path.basename(output_path)}"
                                      f"\nPath: {output_path}")
                else:
                    self.log_and_show(f"Operations failed for video {os.path.basename(input_path)}",
                                      create_messagebox=True, error=True)

                # Close the original clip to free resources
                original_clip.close()

                # Delete the temporary copy if it was created
                if temp_copy_exists:
                    os.remove(temp_copy_path)

            except OSError as e:
                # Log error and skip to the next file in case of OSError
                self.log_and_show(f"OSError: {str(e)} Skipping this file and moving to the next one.",
                                  create_messagebox=True, error=True)
                continue

        # Reset redirect MoviePy output for video edits
        self.redirect_output()

        # Stop the progress bar for the Name Normalizer function
        self.stop_progress(self.progressbar1)

    """
    add_remove_window
    """

    def add_artist_to_file(self):
        """
        Add an artist to the artist file and, if enabled, to the artist_common_categories dictionary.

        This method reads the list of artists from the artist file, checks if the provided artist is already in the
        list, adds the artist to the list, writes the updated list back to the artist file, and optionally adds the
        artist to the artist_common_categories dictionary.

        Returns:
            None

        """
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

            # Write the updated list back to the artist_file and artist_common_categories dictionary
            try:
                with open(self.artist_file, 'w') as artist_list_file:
                    artist_list_file.write('\n'.join(artist_list))

                # Check if the auto add acc record variable is set
                if self.auto_add_acc_record_var.get():
                    # Create a record for the artist in the common categories dictionary
                    self.add_artist_to_common_categories_dictionary(add_artist)

                # Log the message and display to the GUI
                self.log_and_show(f"Added artist to the Artist File: '{add_artist}'")

            except IOError:
                self.log_and_show(f"Writing to Artist File failed: '{self.artist_file}'.",
                                  create_messagebox=True, error=True)

        # Reset the artist entries if the action is successful
        if self.reset_add_remove_var.get():
            # Clear add artist entry
            self.add_artist_entry.delete(0, ctk.END)

    def remove_artist_from_file(self):
        """
        Remove an artist from the artist file and, if found, from the artist_common_categories dictionary.

        This method reads the list of artists from the artist file, checks if the provided artist is in the list,
        removes the artist from the list, writes the updated list back to the artist file, and optionally removes the
        artist from the artist_common_categories dictionary.

        Returns:
            None

        """
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

            # Write the updated list back to the artist_file and artist_common_categories dictionary
            try:
                # Check if the artist is in the common categories dictionary (case-insensitive)
                if any(artist.lower() == remove_artist.lower() for artist in self.artist_common_categories):
                    # Remove the artist record in the common categories dictionary
                    self.remove_artist_from_common_categories_dictionary(remove_artist)

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

    def add_artist_to_common_categories_dictionary(self, add_artist=None):
        """
        Add an artist to the artist_common_categories dictionary.

        This method adds an artist as a key to the artist_common_categories dictionary with an empty list as the value.
        It updates the JSON file with the modified artist_common_categories dictionary.

        Args: add_artist (str, optional): The artist to be added. If not provided, it retrieves the artist from the
        entry widget.

        Returns:
            None

        """
        try:
            # Set the artist to be added from the entry widget
            add_artist = add_artist if add_artist else self.add_acc_record_entry.get().strip()

            # Check if no artist is provided
            if not add_artist:
                self.log_and_show("Add Artist cannot be empty.", create_messagebox=True, error=True)
                return  # Exit the function if no artist is provided

            # Check if the add_artist is already in the list (case-insensitive)
            if any(artist.lower() == add_artist.lower() for artist in self.artist_common_categories):
                self.log_and_show(f"Dictionary record already exists for: '{add_artist}'",
                                  create_messagebox=True, error=True)
            else:
                # Add the artist as a key to the artist_common_categories dictionary with an empty list as the value
                self.artist_common_categories[add_artist] = []

                # Update the JSON file with the modified artist_common_categories dictionary
                self.update_json(self.dictionary_file, "artist_common_categories", self.artist_common_categories)
                self.log_and_show(f"Created dictionary record for: '{add_artist}'")
        except Exception as e:
            self.log_and_show(f"Creating dictionary record failed: '{str(e)}'.", create_messagebox=True, error=True)

        # Reset the artist entries
        if self.reset_add_remove_var.get():
            # Clear add acc record entry
            self.add_acc_record_entry.delete(0, ctk.END)

    def remove_artist_from_common_categories_dictionary(self, remove_artist=None):
        """
        Remove an artist from the artist_common_categories dictionary.

        This method removes the specified artist from the artist_common_categories dictionary.
        It updates the JSON file with the modified artist_common_categories dictionary.

        Args: remove_artist (str, optional): The artist to be removed. If not provided, it retrieves the artist from
        the entry widget.

        Returns:
            None

        """
        try:
            # Set the artist to be added from the entry widget
            remove_artist = remove_artist if remove_artist else self.remove_acc_record_entry.get().strip()

            # Check if no artist is provided
            if not remove_artist:
                self.log_and_show("Remove Artist cannot be empty.", create_messagebox=True, error=True)
                return  # Exit the function if no artist is provided

            # Check if the remove_artist is in the list (case-insensitive)
            if any(artist.lower() == remove_artist.lower() for artist in self.artist_common_categories):
                del self.artist_common_categories[remove_artist]
                # Update the JSON file with the modified artist_common_categories dictionary
                self.update_json(self.dictionary_file, "artist_common_categories", self.artist_common_categories)

                self.log_and_show(f"Dictionary record removed for: '{remove_artist}'")
            else:
                self.log_and_show(f"Artist not found in artist_common_categories: '{remove_artist}'", error=True)
        except Exception as e:
            self.log_and_show(f"Removing dictionary record failed: '{str(e)}'.", create_messagebox=True, error=True)

        # Reset the artist entries
        if self.reset_add_remove_var.get():
            # Clear remove acc record entry
            self.remove_acc_record_entry.delete(0, ctk.END)

    def no_go_creation(self):
        """
        Create a NO-GO file and update the Tampermonkey Script text file.

        This method creates a NO-GO file using the provided name. It also updates the Tampermonkey Script text file
        to include the new NO-GO entry. If the NO-GO file or entry already exists, it logs the action and skips
        creation.

        Returns:
            None

        """
        try:
            # Attempt to get the contents from self.add_no_go_name_entry
            no_go_name = self.add_no_go_name_entry.get().strip()

            # Check if no_go_name is provided
            if not no_go_name:
                self.log_and_show("Add NO GO cannot be empty.", create_messagebox=True, error=True)
                return  # Exit the function if no artist is provided

            # Expand the user's home directory in the NO-GO path
            no_go_directory = os.path.expanduser(self.no_go_directory)

            # Ensure the NO-GO directory exists, create it if not
            if not os.path.exists(no_go_directory):
                os.makedirs(no_go_directory)

            # Create a file for the NO-GO
            no_go_file_name = f"NO GO - {no_go_name}"
            no_go_file_path = os.path.join(no_go_directory, no_go_file_name)

            # Check if the file already exists case-insensitively to prevent overwriting
            if any(filename.lower() == no_go_file_name.lower() for filename in os.listdir(no_go_directory)):
                # Log the action and display a message
                self.log_and_show(f"'{no_go_file_name}' already exists. Skipping creation.", create_messagebox=True,
                                  error=True)

                # Reset the no-go entries if the action is successful
                if self.reset_add_remove_var.get():
                    # Clear add no-go name entry and reset
                    self.add_no_go_name_entry.delete(0, ctk.END)
                return

            # Create NO-GO empty file
            with open(no_go_file_path, 'w'):
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
        """
        Remove a NO-GO file and update the Tampermonkey Script text file.

        This method removes a specified NO-GO file and updates the Tampermonkey Script text file to remove the
        corresponding entry. If the NO-GO file or entry does not exist, it logs the action and skips removal.

        Returns:
            None

        """
        try:
            # Attempt to get the contents from self.remove_no_go_name_entry
            remove_no_go_name = self.remove_no_go_name_entry.get().strip()

            # Expand the user's home directory in the NO-GO path
            no_go_directory = os.path.expanduser(self.no_go_directory)

            # Check if the NO-GO file exists
            no_go_file_name = f"NO GO - {remove_no_go_name}"

            # Check if remove_no_go_name is provided
            if not remove_no_go_name:
                self.log_and_show("Remove NO GO cannot be empty.", create_messagebox=True, error=True)
                return  # Exit the function if no artist is provided

            # Ensure the NO-GO directory exists
            if not os.path.exists(no_go_directory):
                self.log_and_show("NO GO directory does not exist.", create_messagebox=True, error=True)
                return  # Exit the function if NO GO directory does not exist

            # Ensure the NO-GO artist file exists
            if not os.path.exists(self.no_go_artist_file):
                self.log_and_show(f"{self.no_go_artist_file} does not exist. Skipping NO GO removal from the text "
                                  f"file.", error=True)

                # Set the remove variable to false
                remove = False
            else:
                # Set the remove variable to true
                remove = True

            # Check if the file exists case-insensitively
            matching_files = [filename for filename in os.listdir(no_go_directory) if
                              filename.lower() == no_go_file_name.lower()]

            if matching_files:
                # Get the first match and construct the filepath
                matched_filename = matching_files[0]
                matched_file_path = os.path.join(no_go_directory, matched_filename)

                # Remove the matched filepath
                os.remove(matched_file_path)
                self.log_and_show(f"NO GO file '{matched_filename}' removed successfully.")
            else:
                self.log_and_show(f"NO GO file '{no_go_file_name}' not found.", create_messagebox=True, error=True)

            if remove:
                # Check and remove the entry from self.no_go_artist_file tampermonkey (case-insensitive)
                with open(self.no_go_artist_file, "r") as file:
                    lines = file.readlines()

                with open(self.no_go_artist_file, "w") as file:
                    for line in lines:
                        if line.strip().lower() != remove_no_go_name.lower():
                            file.write(line)

                self.log_and_show(f"NO GO entry '{remove_no_go_name}' removed from {self.no_go_artist_file}"
                                  f" successfully.")

        except Exception as e:
            self.log_and_show(f"Removing NO GO failed: '{str(e)}'.", create_messagebox=True, error=True)

        # Reset the no-go entries if the action is successful
        if self.reset_add_remove_var.get():
            # Clear remove no-go name entry and reset
            self.remove_no_go_name_entry.delete(0, ctk.END)

    def add_folder_to_excluded_folders(self):
        """
        Add a folder to the list of excluded folders and update the settings.

        This method takes the folder name from the entry widget, checks if it's already in the excluded folders list
        case-insensitively, and adds it to the list if not. It then updates the JSON file with the new excluded
        folders list.

        Returns:
            None

        """
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

    def remove_folder_from_excluded_folders(self):
        """
        Remove a folder from the list of excluded folders and update the settings.

        This method takes the folder name from the entry widget, checks if it's in the excluded folders list
        case-insensitively, and removes it from the list if found. It then updates the JSON file with the new
        excluded folders list.

        Returns:
            None

        """
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

    def add_custom_text_to_replace(self):
        """
        Add custom text to the list of text replacements and update the settings.

        This method retrieves custom text and replacement text from entry widgets, checks if the custom text is
        already in the list case-insensitively, and adds it to the list with the specified replacement text. It then
        updates the JSON file with the new custom text to replace dictionary.

        Returns:
            None

        """
        # Get the custom text to be added from the entry widget
        custom_text = self.add_ctr_name_entry.get().strip()

        # Get the custom text to be replaced from the entry widget
        replacement_text = self.replacement_text_entry.get().strip()

        # Check if no custom text is provided
        if not custom_text:
            self.log_and_show("Add CTR cannot be empty.", create_messagebox=True, error=True)
            return  # Exit the function if no custom_text is provided

        # Convert both the input custom text and existing custom texts to lowercase
        custom_text_lower = custom_text.lower()
        custom_texts_lower = [text.lower() for text in self.custom_text_to_replace]

        # Check if the custom_text is already in the custom_text_to_replace dictionary (case-insensitive)
        if custom_text_lower in custom_texts_lower:
            self.log_and_show(f"Custom Text '{custom_text}' is already in the custom text to replace dictionary.",
                              create_messagebox=True, error=True)

            # Reset the custom text entries if the action is successful
            if self.reset_add_remove_var.get():
                # Reset the add custom text to replace entry
                self.add_ctr_name_entry.delete(0, ctk.END)

                # Clear replacement text to replace entry
                self.replacement_text_entry.delete(0, ctk.END)

            return  # Exit the function if the custom_text is already in the dictionary

        try:
            # Check if the user did not specify replacement text
            if not replacement_text:
                # Add the custom_text to the custom_text_to_replace dictionary with an empty string as the value
                self.custom_text_to_replace[custom_text] = ""
            else:
                # Add the custom_text to the custom_text_to_replace dictionary with the replacement text as the value
                self.custom_text_to_replace[custom_text] = replacement_text

            # Update the JSON file with the new custom_text_to_replace dictionary
            self.update_json(self.dictionary_file, "custom_text_to_replace", self.custom_text_to_replace)

            # Log and show success message
            self.log_and_show(f"Custom Text '{custom_text}' added to custom text to replace list with "
                              f"'{replacement_text}'.")

        except Exception as e:
            # Log and show error message if an exception occurs
            self.log_and_show(f"Adding Custom Text '{custom_text}' to custom text to replace dictionary failed:"
                              f" {str(e)}",
                              create_messagebox=True, error=True)

        # Reset the custom text entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the custom text to replace entry if the action is successful
            self.add_ctr_name_entry.delete(0, ctk.END)

            # Clear replacement text to replace entry
            self.replacement_text_entry.delete(0, ctk.END)

    def remove_custom_text_to_replace(self):
        """
        Remove custom text from the list of text replacements and update the settings.

        This method retrieves custom text from the entry widget, checks if the custom text is in the dictionary
        case-insensitively, and removes the corresponding key from the custom_text_to_replace dictionary. It then
        updates the JSON file with the new custom text to replace dictionary.

        Returns:
            None

        """
        # Get the custom text to be removed from the entry widget
        custom_text = self.remove_ctr_name_entry.get().strip()

        # Check if no custom text is provided
        if not custom_text:
            self.log_and_show("Remove CTR cannot be empty.", create_messagebox=True, error=True)
            return  # Exit the function if no custom_text is provided

        # Convert the input custom text and existing keys in the dictionary to lowercase
        custom_text_lower = custom_text.lower()
        custom_texts_lower = [text.lower() for text in self.custom_text_to_replace.keys()]

        # Check if the custom_text is in the custom_text_to_replace dictionary (case-insensitive)
        if custom_text_lower not in custom_texts_lower:
            self.log_and_show(f"Custom Text '{custom_text}' is not in the custom text to replace dictionary.",
                              create_messagebox=True, error=True)

            # Reset the custom text entry if the action is successful
            if self.reset_add_remove_var.get():
                # Reset the remove custom_text_to_replace entry
                self.remove_ctr_name_entry.delete(0, ctk.END)

            return  # Exit the function if the custom_text is not in the dictionary

        try:
            # Remove the custom_text key from the custom_text_to_replace dictionary (case-insensitive)
            for key in list(self.custom_text_to_replace.keys()):
                if key.lower() == custom_text_lower:
                    del self.custom_text_to_replace[key]

            # Update the JSON file with the new custom_text_to_replace dictionary
            self.update_json(self.dictionary_file, "custom_text_to_replace", self.custom_text_to_replace)

            # Log and show success message
            self.log_and_show(f"Custom Text '{custom_text}' removed from custom text to replace dictionary.")

        except Exception as e:
            # Log and show error message if an exception occurs
            self.log_and_show(f"Removing Custom Text '{custom_text}' from custom text to replace dictionary failed: "
                              f"{str(e)}",
                              create_messagebox=True, error=True)

        # Reset the custom text entry if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the remove custom_text_to_replace entry if the action is successful
            self.remove_ctr_name_entry.delete(0, ctk.END)

    def add_file_extension(self):
        """
        Add a file extension to the list of allowed file extensions and update the settings.

        This method retrieves a file extension from the entry widget, checks if the file extension is in the list
        case-insensitively, and appends it to the list of file extensions. It then updates the JSON file with the new
        file extensions list.

        Returns:
            None

        """
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

    def remove_file_extension(self):
        """
        Remove a file extension from the list of allowed file extensions and update the settings.

        This method retrieves a file extension from the entry widget, checks if the file extension is in the list
        case-insensitively, and removes it from the list of file extensions. It then updates the JSON file with the new
        file extensions list.

        Returns:
            None

        """
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

    def add_valid_extension(self):
        """
        Add a valid file extension to the list of allowed valid file extensions and update the settings.

        This method retrieves a valid file extension from the entry widget, checks if the file extension is in the list
        case-insensitively, and adds it to the list of valid file extensions. It then updates the JSON file with the new
        valid file extensions list.

        Returns:
            None

        """
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

    def remove_valid_extension(self):
        """
        Remove a valid file extension from the list of allowed valid file extensions and update the settings.

        This method retrieves a valid file extension from the entry widget, checks if the file extension is in the
        list case-insensitively, and removes it from the list of valid file extensions. It then updates the JSON file
        with the new valid file extensions list.

        Returns:
            None

        """
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
            self.log_and_show(
                f"Removing File Extension '{valid_extension}' from valid extensions list failed: {str(e)}",
                create_messagebox=True, error=True)

        # Reset the valid extension entries if the action is successful
        if self.reset_add_remove_var.get():
            # Reset the remove valid_extensions entry if the action is successful
            self.remove_valid_extension_entry.delete(0, ctk.END)

    def add_custom_tab_name(self):
        """
        Add a new custom tab name with a specified weight to the dictionary and update the settings.

        This method retrieves a new custom tab name and weight from the entry widgets, checks for duplicates
        case-insensitively, and adds the new custom tab name to the dictionary under the specified weight. The updated
        dictionary is then saved to the JSON file, and the category buttons in the GUI are refreshed.

        Returns:
            None

        """
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

    def remove_custom_tab_name(self):
        """
        Remove a custom tab name from the dictionary and update the settings.

        This method retrieves the custom tab name to be removed from the entry widget, checks for a case-sensitive
        match in values, and removes the custom tab name from the dictionary. The updated dictionary is then saved to
        the JSON file, and the category buttons in the GUI are refreshed. If no case-sensitive match is found,
        it checks for a case-insensitive match, and if found, removes the case-insensitive matched custom tab name
        from the dictionary.

        Returns:
            None

        """
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

    def browse_artist(self, mode: str) -> None:
        """
        Browse and select an artist using either the "Detect" or "Browse" mode.

        Parameters:
            mode (str): The mode for artist selection. Should be either "Detect" or "Browse".

        Returns:
            None

        Raises:
            ValueError: If an invalid mode is provided or if "Detect" mode is selected without a file renamer input.

        """
        try:
            # Clear the artist display entry widget
            self.acc_display_entry.delete(0, ctk.END)

            # Retrieve the list of artist names from common categories
            artist_list = list(self.artist_common_categories.keys())

            if mode == "Detect":
                # Check if a file renamer input is selected for detection
                if not self.file_renamer_selected_file:
                    raise ValueError("No file renamer input selected. Cannot detect artist without it.")

                # Create a set of excluded folders in lowercase for case-insensitive comparison
                excluded_folders_lower = set(folder.lower() for folder in self.excluded_folders)

                # Filter out excluded folders from the artist list
                sanitized_artist_list = [folder for folder in artist_list if
                                         folder.lower() not in excluded_folders_lower]

                # Get the lowercase base name of the selected file
                base_name_lower = os.path.basename(self.file_renamer_selected_file).lower()

                # Iterate through sanitized artist list to find a match in the file name
                for artist in sanitized_artist_list:
                    if artist.lower() in base_name_lower:
                        self.acc_selected_artist = artist
                        break

                # Update the artist display and log the selected artist
                self.update_acc_display()
                self.log_and_show(f"Artist selected via {mode}: {self.acc_selected_artist}")

            elif mode == "Browse":
                # Create a window to allow the user to select an artist from the list
                artist = self.selection_window(
                    title="Artist Selection",
                    prompt="Which artist would you like to modify?:",
                    label_text="Choose Artist",
                    item_list=artist_list
                )

                # Update the selected artist if a valid choice is made, otherwise, return
                if artist in artist_list:
                    # Set the acc selected artist
                    self.acc_selected_artist = artist

                    # Update acc display
                    self.update_acc_display()

                    # Log the action if logging is enabled
                    self.log_and_show(f"Artist selected via {mode}: {self.acc_selected_artist}")
                else:
                    return

            else:
                # Raise an error for invalid mode
                raise ValueError(f"Invalid mode for browse artist: {mode}")

        except ValueError as e:
            # Handle ValueError exceptions by logging and showing the error
            self.log_and_show(str(e), create_messagebox=True, error=True)
        except Exception as e:
            # Handle unexpected exceptions by logging and showing the error
            self.log_and_show(f"An unexpected error occurred: {str(e)}", create_messagebox=True, error=True)

    def update_acc_display(self):
        """
        Update the Artist Category Customization (ACC) display with the selected artist and their common categories.

        This method sets the artist's name and their common categories in the ACC display.

        Returns:
            None
        """
        if self.acc_selected_artist:
            common_categories = self.artist_common_categories.get(self.acc_selected_artist, [])

            # Set the artist and artist's common categories to the acc display
            self.acc_display_text.set(f"{self.acc_selected_artist}: {common_categories}")

    def add_artist_common_category(self):
        """
        Add a new common category for the selected artist in the Artist Category Customization (ACC).

        This method retrieves the selected artist and a new common category from the GUI entry widget,
        checks for duplicates, appends the new common category to the selected artist's list of common categories,
        updates the JSON file with the modified dictionary, logs the action, updates the artist display,
        and resets the entry if the action is successful.

        Raises:
            ValueError: If no artist is selected, the new common category is empty, or if the new common category
                        already exists for the selected artist.

        Returns:
            None
        """
        try:
            if not self.acc_selected_artist:
                raise ValueError("No artist selected. Please select an artist and try again.")

            # Get the new common category from the add_acc_entry widget
            new_common_category = self.add_acc_entry.get().strip()

            if not new_common_category:
                raise ValueError("Add A.C.C. cannot be empty.")

            # Convert all items to lower case
            lower_artist_common_categories = map(lambda x: x.lower(),
                                                 self.artist_common_categories.get(self.acc_selected_artist, []))

            # Check for case-insensitive duplicates
            if new_common_category.lower() in lower_artist_common_categories:
                raise ValueError(f"'{new_common_category}' already exists for {self.acc_selected_artist}.")

            # Append the new_common_category to the selected artist's list
            self.artist_common_categories[self.acc_selected_artist].append(new_common_category)

            # Update the JSON file with the modified dictionary
            self.update_json(self.dictionary_file, "artist_common_categories", self.artist_common_categories)

            # Log the action if logging is enabled
            self.log_and_show(f"A.C.C. added: '{new_common_category}'")

            # Update the artist display
            self.update_acc_display()

            # Reset the acc entry if the action is successful
            if self.reset_add_remove_var.get():
                # Clear the add_acc_entry entry
                self.add_acc_entry.delete(0, ctk.END)

        except ValueError as ve:
            # Log an error message and display it using messagebox
            self.log_and_show(str(ve), create_messagebox=True, error=True)
        except Exception as e:
            # Handle unexpected errors
            self.log_and_show(f"An unexpected error occurred: {str(e)}", create_messagebox=True, error=True)

    def remove_artist_common_category(self):
        """
        Remove a common category for the selected artist in the Artist Category Customization (ACC).

        This method retrieves the selected artist and the common category to be removed from the GUI entry widget,
        checks for empty inputs and the existence of the common category in the selected artist's list,
        removes the common category from the list, updates the JSON file with the modified dictionary,
        updates the artist display, and resets the entry if the action is successful.

        Raises:
            ValueError: If no artist is selected, the common category to be removed is empty,
                        or if the common category is not found for the selected artist.

        Returns:
            None
        """
        try:
            if not self.acc_selected_artist:
                raise ValueError("No artist selected. Please select an artist and try again.")

            # Get the common category from the remove_acc_entry widget
            remove_common_category = self.remove_acc_entry.get().strip()

            if not remove_common_category:
                raise ValueError("Remove A.C.C. cannot be empty.")

            # Case-insensitive check for the common category in the selected artist's list
            common_categories = self.artist_common_categories.get(self.acc_selected_artist, [])

            # Convert all items to lowercase for case-insensitive comparison
            lower_common_categories = [category.lower() for category in common_categories]

            if remove_common_category.lower() not in lower_common_categories:
                raise ValueError(f"'{remove_common_category}' not found for {self.acc_selected_artist}.")

            # Remove the common category from the selected artist's list
            self.artist_common_categories[self.acc_selected_artist] = [
                category for category in common_categories if category.lower() != remove_common_category.lower()]

            # Update the JSON file with the modified dictionary
            self.update_json(self.dictionary_file, "artist_common_categories", self.artist_common_categories)

            # Update the artist display
            self.update_acc_display()

            # Reset the remove_acc entry if the action is successful
            if self.reset_add_remove_var.get():
                # Clear the remove_acc_entry entry
                self.remove_acc_entry.delete(0, ctk.END)

        except ValueError as ve:
            # Log an error message and display it using messagebox
            self.log_and_show(str(ve), create_messagebox=True, error=True)
        except Exception as e:
            # Handle unexpected errors
            self.log_and_show(f"An unexpected error occurred: {str(e)}", create_messagebox=True, error=True)

    def create_tabview(self, parent_frame, tab_names, default_tab=None):
        """
        Create a tabview with customizable parameters.

        Parameters:
        - parent_frame: The parent frame to which the tabview will be added.
        - tab_names: List of tab names to be displayed in the tabview.
        - default_tab: Optional. The default tab to be set after creating the new tabview.

        Returns:
        - tabview: The created tabview.
        - tabs: Dictionary containing references to the created tabs.
        """
        # Create tabview
        tabview = ctk.CTkTabview(parent_frame)
        tabview.grid(row=1, column=0)

        # Sort the tab_names
        if self.sort_tab_names_var.get():
            # Determine the order to sort (forward or backward)
            sort_reverse_order_var = True if self.sort_reverse_order_var.get() else False

            # Determine the order to sort (forward or backward)
            tab_names = sorted(list(set(tab_names)), reverse=sort_reverse_order_var)
        else:
            tab_names = list(set(tab_names))

        tabs = {}  # Dictionary to store tab references

        for tab_name in tab_names:
            # Use the tab_name naming scheme
            tab_name = f"{tab_name}"

            # Create the tab
            tab = tabview.add(tab_name)

            # Store the reference to the tab
            tabs[tab_name] = tab

        if default_tab:
            # Set the default tab
            tabview.set(default_tab)

        return tabview, tabs

    def refresh_buttons_and_tabs(self, *_):
        """
        Refreshes the category buttons and tabs in the user interface.

        This method serves as a wrapper around the refresh_category_buttons method,
        triggering an update of the buttons and tabs based on changes or events.

        Parameters:
            *_: Accepts any number of positional arguments (unused in the method).

        Returns:
            None
        """
        self.refresh_category_buttons()

    def update_cache(self):
        """
        Update the cache with the list of artist files in the artist directory using os.walk.

        Notes:
            - If the cache is older than the specified duration (self.cache_duration), a periodic update is triggered.
            - The updated cache is stored in the 'self.cached_artist_files' variable.
        """
        # Update the cache if it's older than the specified duration
        current_time = time.time()
        if current_time - self.last_cache_update > self.cache_duration:
            self.log_and_show("Periodic os.walk for Artist Search functionality started")

            # Reset the cached artist files list
            self.cached_artist_files = []

            # Traverse the artist directory using os.walk to collect artist file paths
            for root, dirs, files in os.walk(self.artist_directory):
                for file_name in files:
                    artist_file_path = os.path.join(root, file_name)
                    # Append each artist file path to the cache
                    self.cached_artist_files.append(artist_file_path)

            # Update the last_cache_update timestamp to the current time
            self.last_cache_update = current_time

    def artist_search(self):
        """
        Perform an artist search based on the selected input and artist directory.

        Notes:
        - Requires file name with a dash (-) in it to help reduce false positives with common words. Place the
        artist on the left hand side of the dash to be considered for use with this function.

        Returns:
            tuple or None: If a matching artist is found, returns a tuple (artist, artist_file_path), else returns None.
        """
        # Check if an input is selected
        if not self.file_renamer_selected_file:
            # If no input is selected, return none
            self.log_and_show("No input selected.")
            return None

        # Check if self.artist_directory exists
        if not os.path.exists(self.artist_directory):
            # If artist directory does not exist, display an error message and return none
            self.log_and_show(f"Artist Search cannot function as intended since the Artist Directory"
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
                self.log_and_show("No '-' found in the file name. Cannot identify artist for Artist Search "
                                  "functionality.")
                return None

            # Extract the artist from the text before '-'
            artist = base_name.split('-')[0].strip()

            if self.ignore_known_artists_var.get():
                # Perform case-insensitive matching for known artists in the artist_directory
                matching_artists = [directory for directory in os.listdir(self.artist_directory) if
                                    re.match(artist, directory, re.IGNORECASE)]

                # Remove matching known artists from the artist variable
                for matching_artist in matching_artists:
                    artist = artist.replace(matching_artist, '').strip()

                # Check if there is anything left in artist variable
                if not artist:
                    self.log_and_show(f"Artist Search: All matching artists removed. No artist left after ignoring "
                                      f"known artists.")
                    return None

            # Update the cache
            self.update_cache()

            # Search for a case-insensitive match for the artist in the cached artist files
            for artist_file_path in self.cached_artist_files:
                # Check if the artist is present in the file name
                if artist.lower() in os.path.basename(artist_file_path).lower():
                    # Skip the current file being compared
                    if artist_file_path == self.file_renamer_selected_file:
                        continue

                    # Verify the file exists and artist's name is not part of the directory path
                    if os.path.exists(artist_file_path) and os.path.isfile(artist_file_path) \
                            and artist.lower() not in os.path.dirname(artist_file_path).lower():
                        # Return the artist and result as a tuple
                        return artist, artist_file_path

            # If no matching artist is found, return none
            self.log_and_show("No matching artist file found.")
            return None

        except Exception as e:
            # Handle any unexpected exceptions and log an error message
            self.log_and_show(f"Unexpected error identifying artist for Artist Search: {e}",
                              create_messagebox=True, error=True)
            return None


if __name__ == "__main__":
    # Create an instance of the OCDFileRenamer application and start the main loop
    app = OCDFileRenamer()
    app.mainloop()
