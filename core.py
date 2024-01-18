import os
import re
import json
from tkinter import filedialog, messagebox
import send2trash
import subprocess
import customtkinter as ctk
import logging
import configparser
import shutil
from moviepy.editor import VideoFileClip

"""
Configuration
"""


def load_configuration():
    # Check if config.ini file exists
    config_file_path = 'config.ini'
    if not os.path.exists(config_file_path):
        print(f"Error: {config_file_path} not found. Please create the config file and try again.")
        quit()

    # Load the configuration from the config.ini file
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Filepaths/Directories
    initial_directory = config.get('Filepaths', 'initial_directory', fallback='~')
    initial_output_directory = config.get('Filepaths', 'initial_output_directory', fallback='~')
    double_check_directory = config.get('Filepaths', 'double_check_directory', fallback='~')
    artist_directory = config.get('Filepaths', 'artist_directory', fallback='~')
    artist_file = config.get('Filepaths', 'artist_file', fallback='list_of_artists.txt')
    file_path_list_file = config.get('Filepaths', 'file_path_list_file', fallback='temp.txt')
    categories_file = config.get('Filepaths', 'categories_file', fallback='categories.json')

    # Variables and window geometry
    geometry = config.get('Settings', 'geometry', fallback='1280x850')
    column_numbers = config.get('Settings', 'column_numbers', fallback=7)
    default_weight = config.get('Settings', 'default_weight', fallback=9)
    default_decibel = config.get('Settings', 'default_decibel', fallback=0.0)
    default_audio_normalization = config.get('Settings', 'default_audio_normalization', fallback=0.0)
    default_frame = config.get('Settings', 'default_frame', fallback="file_renamer_window")
    ocd_file_renamer_log = config.get('Logs', 'ocd_file_renamer_log', fallback="ocd_file_renamer.log")
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

    # Name Normalizer
    remove_all_symbols_var = config.getboolean("Settings", "remove_all_symbols_var", fallback=False)
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
    deep_walk_var = config.getboolean("Settings", "deep_walk_var", fallback=False)

    # Video Editor
    remove_successful_lines_var = config.getboolean("Settings", "remove_successful_lines_var", fallback=False)
    default_rotation_var = config.get("Settings", "default_rotation_var", fallback="none")

    # File extensions
    file_extensions = config.get('Settings', 'file_extensions',
                                 fallback='.mp3, .wav, .ogg, .flac, .aac, .wma, .m4a, .aiff, .alac, .opus, .mp4, '
                                          '.mkv, .flv, .avi, .mov, .wmv, .mpeg, .mpg, .m4v')
    file_extensions_tuple = tuple(ext.strip() for ext in file_extensions.split(','))

    # Return the loaded configuration values as a tuple
    return (move_text_var, initial_directory, artist_directory, double_check_directory, categories_file,
            geometry, reset_output_directory_var, suggest_output_directory_var, move_up_directory_var,
            open_on_file_drop_var, remove_duplicates_var, default_placement_var, special_character_var,
            double_check_var, activate_logging_var, ocd_file_renamer_log, column_numbers, default_weight,
            file_extensions_tuple, remove_all_symbols_var, tail_var, remove_parenthesis_trail_var,
            remove_hashtag_trail_var, remove_new_var, remove_dash_var, remove_endash_var, remove_emdash_var,
            remove_ampersand_var, remove_at_var, remove_underscore_var, remove_comma_var, remove_single_quote_var,
            remove_double_quote_var,
            title_var, reset_var, initial_output_directory, artist_file, file_path_list_file, default_frame,
            artist_file_search_var, deep_walk_var, default_decibel, default_audio_normalization,
            remove_successful_lines_var, default_rotation_var, remove_double_space_var, remove_colon_var,
            remove_semicolon_var, remove_percent_var, remove_caret_var, remove_dollar_var, remove_asterisk_var,
            remove_plus_var, remove_equal_var, remove_curly_brace_var, remove_square_bracket_var, remove_pipe_var,
            remove_backslash_var, remove_angle_bracket_var, remove_question_mark_var, remove_parenthesis_var,
            remove_hashtag_var)


def logging_setup(self):
    # Create the log file if it doesn't exist
    if not os.path.exists(self.ocd_file_renamer_log):
        with open(self.ocd_file_renamer_log, 'w'):
            pass

    # Initialize logging
    logging.basicConfig(filename=self.ocd_file_renamer_log, level=logging.INFO, filemode='a',
                        format='%(asctime)s - %(levelname)s: %(message)s')

    logging.info("Logging started.")


"""
File Operations
"""


# Function to move the selected file to the trash
def move_file_to_trash(self):
    try:
        if self.selected_file:
            # Ask for confirmation before moving to trash
            confirmation = messagebox.askyesno("Confirm Action",
                                               "Are you sure you want to move this file to the trash?")
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.info(f"'{self.selected_file}' selected for deletion.")
            if confirmation:
                # Move the file to trash using send2trash library
                send2trash.send2trash(self.selected_file)
                # Reset selected file, queue, and clear display elements
                self.selected_file = ""
                self.queue = []
                self.file_display_text.set("")
                self.custom_text_entry.delete(0, ctk.END)
                self.output_directory = ""
                self.output_directory_entry.delete(0, ctk.END)
                if self.activate_logging_var.get():
                    # Log the action if logging is enabled
                    logging.info("File moved to trash successfully")
                self.show_message("File moved to trash successfully", frame_name="file_renamer_window")
        else:
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error("No file selected. Cannot move to trash.")
            self.show_message("No file selected. Cannot move to trash.", error=True, frame_name="file_renamer_window")
    except OSError as e:
        # Construct the error message
        error_message = f"Error: {str(e)}"
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.error(error_message)
        self.show_message(error_message, error=True, frame_name="file_renamer_window")


# Function to load the last used file
def load_last_used_file(self):
    if self.last_used_file:
        # Set the selected file to the last used file and update display
        self.selected_file = self.last_used_file
        filename = os.path.basename(self.selected_file)

        # Display only the filename in the file display widget
        self.file_display_text.set(filename)

        self.queue = []
        self.update_file_display()

        message = filename
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.info(f"Last used file selected: {message}")

        self.show_message(f"Last used file selected: {message}", frame_name="file_renamer_window")
    else:
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.error("No last used file found.")
        self.show_message("Error: No last used file found.", error=True, frame_name="file_renamer_window")


# Function to handle a file being dropped onto the application window
def on_file_drop(self, event):
    # Remove the default custom text entry text
    self.custom_text_entry.delete(0, ctk.END)

    self.selected_file = event.data.strip('{}')
    filename = os.path.basename(self.selected_file)

    # Display only the filename in the file display widget
    self.file_display_text.set(filename)

    self.queue = []
    self.update_file_display()

    # Log the error and display the error in the gui
    message = filename
    if self.activate_logging_var.get():
        # Log the action if logging is enabled
        logging.info(f"File selected via drop: {message}")

    self.show_message(f"File selected via drop: {message}", frame_name="file_renamer_window")

    # Open the file if the corresponding option is set
    if self.open_on_file_drop_var.get():
        try:
            subprocess.Popen(['xdg-open', self.selected_file])  # I use Arch, btw.
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.info(f"File opened: {self.selected_file}")
        except OSError as e:
            # Construct the error message
            error_message = f"Error: {str(e)}"
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error(error_message)
            self.show_message(error_message, error=True, frame_name="file_renamer_window")


# Function to add a category to the queue
def add_to_queue(self, category):
    if self.selected_file:
        # Check if the category is not already in the queue
        if category not in self.queue:
            self.queue.append(category)

        # Update file display and show a message
        self.update_file_display()
        self.show_message(f"Word added: {category}", frame_name="file_renamer_window")


# Function to update the file display based on selected options
def update_file_display(self):
    if self.selected_file:
        custom_text = self.custom_text_entry.get().strip()

        # Use only the base name of the file, not the full path
        base_file_name = os.path.basename(self.selected_file)

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
            messagebox.showerror("Length Exceeded", "The proposed file name exceeds 250 characters. Please consider "
                                                    "shortening it to comply with operating system limitations.")
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
        self.show_message("Last category removed", frame_name="file_renamer_window")
    else:
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.error("Nothing in the queue. Nothing to undo.")
        self.show_message("Error: Nothing in the queue. Nothing to undo.", error=True, frame_name="file_renamer_window")


# Function to clear the selection and reset related elements
def clear_selection(self):
    self.selected_file = ""
    self.queue = []
    self.file_display_text.set("")
    self.show_message("Selection cleared", frame_name="file_renamer_window")

    # Clear custom text entry and reset output directory
    self.custom_text_entry.delete(0, ctk.END)
    self.output_directory = os.path.dirname(self.selected_file)
    self.output_directory_entry.delete(0, ctk.END)
    self.output_directory_entry.insert(0, self.output_directory)


# Function to browse and select a file
def browse_file(self):
    # Remove the default custom text entry text
    self.custom_text_entry.delete(0, ctk.END)

    file_path = filedialog.askopenfilename(initialdir=self.initial_directory)
    if file_path:
        # Set the selected file, update display, and log the action
        self.selected_file = file_path
        filename = os.path.basename(self.selected_file)

        # Display only the filename in the file display widget
        self.file_display_text.set(filename)

        self.queue = []
        self.update_file_display()

        # Log the error and display the error in the gui
        message = filename
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.info(f"File selected via Browse: {message}")

        self.show_message(f"File selected via Browse: {message}", frame_name="file_renamer_window")


# Function to browse and select an output directory
def browse_output_directory(self):
    # Check if a file is selected
    if self.selected_file:
        # Determine the initial directory based on options
        if self.suggest_output_directory_var.get():
            base_name = os.path.basename(self.selected_file)

            # Extract the artist from the filename (before the dash)
            artist_match = re.match(r"^(.*?)\s*-\s*.*$", base_name)
            if artist_match:
                artist = artist_match.group(1).strip()

                # Construct the artist folder path
                artist_folder_path = os.path.join(self.artist_directory, artist)

                # Use artist folder if it exists, otherwise use default initial directory
                if os.path.exists(artist_folder_path):
                    initial_directory = artist_folder_path
                else:
                    initial_directory = self.initial_directory
            else:
                # If the filename doesn't match the expected pattern, use the default initial directory
                initial_directory = self.initial_directory
        else:
            initial_directory = self.initial_directory
    else:
        # If no file is selected, use the default initial directory
        initial_directory = self.initial_directory

    # Ask for the output directory
    output_directory = filedialog.askdirectory(initialdir=initial_directory)

    if output_directory:
        # Set the output directory and update the entry field
        self.output_directory = output_directory
        self.output_directory_entry.delete(0, ctk.END)
        self.output_directory_entry.insert(0, self.output_directory)


# Function to handle actions after successful file renaming
def handle_rename_success(self, new_path):
    if self.double_check_var.get():
        try:
            # Get the name of the folder immediately above the current location
            folder_name = os.path.basename(os.path.dirname(new_path))

            # Expand the user's home directory in the output directory path
            double_check_directory = os.path.expanduser(self.double_check_directory)

            # Ensure the output directory exists, create it if not
            if not os.path.exists(double_check_directory):
                os.makedirs(double_check_directory)

            # Create an empty file with the specified naming scheme
            file_name = f"Double check {folder_name}"
            file_path = os.path.join(double_check_directory, file_name)

            with open(file_path, 'w'):
                pass

            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.info(f"Empty file created successfully for {folder_name}")
            self.show_message(f"Empty file created successfully for {folder_name}", frame_name="file_renamer_window")

        except Exception as e:
            # Handle any errors that may occur
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error(f"Error creating empty file: {str(e)}")
            self.show_message(f"Error creating empty file: {str(e)}", frame_name="file_renamer_window")

    # Reset selected file, queue, and update last used file
    self.selected_file = ""
    self.queue = []
    self.file_display_text.set("")
    self.custom_text_entry.delete(0, ctk.END)
    self.last_used_file = new_path

    # Get the base name and truncate after x characters
    last_used_name = os.path.basename(new_path)
    if len(last_used_name) > 115:
        last_used_name = last_used_name[:115]
    self.last_used_display.configure(text=last_used_name)

    if self.reset_output_directory_var.get():
        # Clear and reset the Output Directory to the current directory
        self.output_directory = os.path.dirname(self.selected_file)
        self.output_directory_entry.delete(0, ctk.END)
        self.output_directory_entry.insert(0, self.output_directory)

    if self.activate_logging_var.get():
        # Log the action if logging is enabled
        logging.info("File renamed and saved successfully")

    # Show a success message
    self.show_message("File renamed and saved successfully", frame_name="file_renamer_window")


"""
Category Management
"""


def add_category(self):
    # Get the new category from the add category entry widget
    new_category = self.category_entry.get().strip()
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
                if self.activate_logging_var.get():
                    # Log the action if logging is enabled
                    logging.error("Error: Weight must be an integer. Using default weight.")
                # Handle the case where the provided weight is not an integer
                self.show_message("Error: Weight must be an integer. Using default weight.", error=True,
                                  frame_name="file_renamer_window")
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
            self.weight_entry.insert(0, self.default_weight)  # Reset to default weight

            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.info(f"Category added: '{new_category}' with weight({weight})")
            # Show a success message
            self.show_message(f"Category added: '{new_category}' with weight({weight})",
                              frame_name="file_renamer_window")
        else:
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error(f"'{new_category}' already exists. Skipping.")
            # Show an error message if the category already exists
            self.show_message(f"Error: '{new_category}' already exists. Skipping.", error=True,
                              frame_name="file_renamer_window")
            # Clear the category entry and weight entry fields
            self.category_entry.delete(0, ctk.END)
            self.weight_entry.delete(0, ctk.END)
            self.weight_entry.insert(0, self.default_weight)  # Reset to default weight


def remove_category(self):
    # Get the category to be removed from the remove category entry widget
    category_to_remove = self.remove_category_entry.get().strip()

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

        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.info(f"Category removed: {category_to_remove}")
        # Show a success message
        self.show_message(f"Category removed: {category_to_remove}", frame_name="file_renamer_window")
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

            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.info(f"Category removed: {category_to_remove}")
            # Show a success message
            self.show_message(f"Category removed: {matching_category}", frame_name="file_renamer_window")
        else:
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error(f"'{category_to_remove}' not found in dictionary. Skipping.")
            # Show an error message if no matching category is found
            self.show_message(f"Error: '{category_to_remove}' not found in dictionary. Skipping.", error=True,
                              frame_name="file_renamer_window")


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
    # Check if a file is selected and either the queue is not empty or custom text is provided
    if self.selected_file and (self.queue or self.custom_text_entry.get().strip()):

        # Get custom text and file extension
        custom_text = self.custom_text_entry.get().strip()
        base_name, extension = os.path.splitext(os.path.basename(self.selected_file))

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
            self.output_directory = os.path.dirname(self.selected_file)

        # Determine the new path based on user preferences
        if self.move_up_directory_var.get():
            # Ignore the provided output directory and move the file up one folder
            parent_directory = os.path.dirname(os.path.dirname(self.selected_file))
            new_path = os.path.join(parent_directory, os.path.basename(name))
        else:
            # Use the specified output directory
            new_path = os.path.join(self.output_directory, os.path.basename(name))

        # TODO: Include logic for suggest_output_directory_var here
        # if self.suggest_output_directory_var.get():
        #     pass

        # Attempt to rename the file and handle success or errors
        try:
            os.rename(self.selected_file, new_path)
            if self.activate_logging_var.get():
                # Log the renaming action if logging is enabled
                logging.info(f"\nFile: '{os.path.basename(self.selected_file)}' renamed successfully. "
                             f"\nSaved to: \n{new_path}")
            self.handle_rename_success(new_path)
        except OSError as e:
            # Construct the error message
            error_message = f"Error: {str(e)}"
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error(error_message)
            self.show_message(error_message, error=True, frame_name="file_renamer_window")


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
                # Construct the error message
                error_message = f"Error: {str(e)}"
                if self.activate_logging_var.get():
                    # Log the action if logging is enabled
                    logging.error(error_message)
                self.show_message(error_message, error=True, frame_name="file_renamer_window")
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


# Function to remove duplicate artists from the filename. Requires artist_file
def remove_artist_duplicates_from_filename(file_name, artist_file):
    # Read the list of artists from the artist_file
    with open(artist_file, 'r') as artist_list_file:
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


# Function to process and rename files and moving files to a specified directory
def rename_and_move_file(self, file_path, move_directory, artist_file):
    # Split the file path into directory path and filename
    dir_path, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)

    # Check if the file has one of the video file extensions
    if ext.lower() in self.file_extensions_tuple:
        # Remove specified characters from the filename if remove_all_symbols_var is True
        if self.remove_all_symbols_var.get():
            # Define the characters to be removed
            remove_chars = ",;:@$%^&*+={}[]|\\<>\"?-–—"

            # Replace each unwanted character with an empty string
            for char in remove_chars:
                name = name.replace(char, "")

        # Remove new if remove_new_var is True
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
            # Make file name a title
            name = name.title()

        if self.remove_double_space_var.get():
            # Sanitize the filename by removing double spaces
            name = ' '.join(name.split())

        # Process artist names if artist_file_search_var is True
        if self.artist_file_search_var.get():
            # Read the list of artists from the artist_file
            with open(artist_file, 'r') as artist_list_file:
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
                name = remove_artist_duplicates_from_filename(name, artist_file)

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
            if self.activate_logging_var.get():
                logging.info(f"Skipped renaming: {filename} (no changes needed)")
            return

        # Construct the new file path
        new_path = os.path.join(dir_path, name)

        # Check if the new filename already exists
        if os.path.exists(new_path):
            if self.activate_logging_var.get():
                logging.warning(f"Conflict detected on: \n{name}.")

            # Extract the base name (excluding extension) and check for existing counter
            base_name, _ = os.path.splitext(name)
            counter_match = re.search(r" \((\d+)\)$", base_name)

            if counter_match:
                if self.activate_logging_var.get():
                    logging.info(f"Counter match on: \n{name}.")
                counter = int(counter_match.group(1)) + 1
                base_name = re.sub(r" \(\d+\)$", "", base_name)  # Remove existing counter
            else:
                if self.activate_logging_var.get():
                    logging.info(f"No counter match on: \n{name}.")
                counter = 1

            # Generate name with incremented counter until a unique name is found
            new_path = os.path.join(move_directory if move_directory else dir_path, name)
            while os.path.exists(new_path):
                new_name_with_counter = f"{base_name} ({counter}){ext}"
                name = new_name_with_counter
                new_path = os.path.join(move_directory if move_directory else dir_path, name)
                counter += 1
        try:
            # Rename the file
            os.rename(file_path, new_path)

            # Log the renaming operation if logging is activated
            if self.activate_logging_var.get():
                logging.info(f"Renamed: {filename} -> {os.path.basename(new_path)}")

            # Move the renamed file to the specified directory if move_directory is provided
            if move_directory:
                move_file_with_overwrite_check(self, new_path, move_directory)
        except OSError as e:
            # Log an error if renaming fails
            if self.activate_logging_var.get():
                logging.error(f"Error renaming {filename}: {e}")
    else:
        # Log that the file is ignored if not on the file extensions list
        if self.activate_logging_var.get():
            logging.info(f"Ignored: {filename} (not on file extensions list)")


# Function to retrieve the contents of a folder, including all files in subdirectories, and saves the full file paths
# to a specified file
def get_folder_contents_and_save_to_file(self, folder_path, file_list_file):
    # Initialize an empty list to store file paths
    file_paths = []

    # Traverse through the folder using os.walk
    for root, dirs, files in os.walk(folder_path):
        # Log the shallow os.walk operation if logging is activated
        if self.activate_logging_var.get():
            logging.info(f"Info: {self.deep_walk_var.get()} os.walk started on '{folder_path}'")
        # Include subdirectories if the deep_walk_var is True or the foot folder is selected
        if self.deep_walk_var.get() or root == folder_path:
            for file in files:
                # Append the full file path to the list
                file_paths.append(str(os.path.join(root, file)))

    # Write the file paths to the specified file
    with open(file_list_file, 'w') as f:
        f.write('\n'.join(file_paths))


# Function to move a file from a source path to a destination directory with overwrite protection
def move_file_with_overwrite_check(self, source_path, destination_directory):
    # Create the destination file path by joining the destination directory and the source file name
    destination_file = os.path.join(destination_directory, os.path.basename(source_path))

    # Check if the destination file already exists
    if os.path.exists(destination_file):
        # Rename the source file to avoid overwriting by appending a counter
        name, ext = os.path.splitext(os.path.basename(source_path))
        counter = 1
        while os.path.exists(destination_file):
            name = f"{name} ({counter})"
            destination_file = os.path.join(destination_directory, name + ext)
            counter += 1

    # Perform the move now that we're sure it won't overwrite
    try:
        shutil.move(str(source_path), str(destination_file))

        # Log the move operation if logging is activated
        if self.activate_logging_var.get():
            logging.info(f"Moved: {os.path.basename(source_path)} -> {os.path.basename(destination_file)}")
    except OSError as e:
        # Log error if logging is activated
        if self.activate_logging_var.get():
            logging.error(f"Error renaming {os.path.basename(source_path)}: {e}")


# TODO Optimize this
# Function to performing various name normalization operations on certain files within a specified folder
def process_folder(self):
    # Retrieve values from GUI input fields
    folder_path = self.folder_path_entry.get()
    move_directory = self.move_directory_entry.get()
    artist_file = self.artist_file_entry.get()

    # Check if the specified folder path exists
    if not os.path.exists(folder_path):
        messagebox.showerror("Error", "Folder path does not exist or was not specified.\nPlease try again.")
        return

    # Check if move_directory is specified and exists
    if move_directory and not os.path.exists(move_directory):
        messagebox.showerror("Error", "Output directory does not exist or was not specified.\nPlease try again.")
        return

    # Check artist file conditions if artist_file_search_var is True
    if self.artist_file_search_var.get():
        if not artist_file:
            # If artist file wasn't specified, try falling back to the default
            artist_file = self.artist_file
            # If fallback artist file doesn't exist return so elif portion fires
            if not os.path.exists(artist_file):
                return
        elif not os.path.exists(artist_file):
            messagebox.showerror("Error", "Artist file does not exist.\nPlease create it from the template and try "
                                          "again\nor turn off Artist Search.\nSee FAQ")
            return

    # Set move_directory to None if not specified
    if not move_directory:
        move_directory = None

    try:
        # Get folder contents and save to a temporary file
        get_folder_contents_and_save_to_file(self, folder_path, self.file_path_list_file)
        try:
            # Read file paths from the temporary file
            with open(self.file_path_list_file, 'r') as file:
                file_paths = file.read().splitlines()

            # Iterate through file paths and rename/move files
            for file_path in file_paths:
                rename_and_move_file(
                    self,
                    file_path,
                    move_directory,
                    artist_file
                )
        except OSError as e:
            # Log error if logging is activated
            if self.activate_logging_var.get():
                logging.error(f"Error: {str(e)}")
        try:
            # Remove the temporary file
            os.remove(self.file_path_list_file)

            # Log deletion of temp file if logging is activated
            if self.activate_logging_var.get():
                logging.info("Deleting temp file.")
        except OSError as e:
            # Log error if logging is activated
            if self.activate_logging_var.get():
                logging.error(f"Error: {str(e)}")

        # Reset GUI input fields if reset is True
        if self.reset_var.get():
            # Clear the entry fields
            self.folder_path_entry.delete(0, ctk.END)
            self.move_directory_entry.delete(0, ctk.END)
            self.artist_file_entry.delete(0, ctk.END)

        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.info("Files have been processed successfully.")

        # Display success message
        self.show_message("Files have been processed successfully.", frame_name="name_normalizer_window")
    except Exception as e:
        # Display error message if an exception occurs
        messagebox.showerror("Error", f"An error occurred: {e}")


# Open a dialog to browse and select a folder to normalize files
def browse_folder_path(self):
    # Function to browse and select a folder to normalize files
    self.folder_path = filedialog.askdirectory(initialdir=self.initial_directory)
    self.folder_path_entry.delete(0, ctk.END)
    self.folder_path_entry.insert(0, self.folder_path)


# Function to browse and select a folder to move the normalized files
def browse_move_directory(self):
    move_directory = filedialog.askdirectory(initialdir=self.initial_output_directory)
    self.move_directory_entry.delete(0, ctk.END)
    self.move_directory_entry.insert(0, move_directory)


# Open a dialog to browse and select a file containing a line delimited list of artists
def browse_artist_file(self):
    artist_file = filedialog.askopenfilename(
        initialdir=self.initial_directory,
        filetypes=[("Text Files", "*.txt")])
    self.artist_file_entry.delete(0, ctk.END)
    self.artist_file_entry.insert(0, artist_file)


# Function to clear the selection and update the GUI
def clear_name_normalizer_selection(self):
    self.folder_path_entry.delete(0, ctk.END)
    self.move_directory_entry.delete(0, ctk.END)
    self.artist_file_entry.delete(0, ctk.END)


"""
Video Editor
"""


# Function to generate a non-conflicting filename
def get_non_conflicting_filename(self, path):
    try:
        # Split the given path into the base filename and its extension.
        base, ext = os.path.splitext(path)

        # Initialize a counter to keep track of the uniqueness of the filename.
        counter = 1

        # Initialize the new path with the original path.
        new_path = path

        # Check if the file already exists at the given path.
        while os.path.exists(new_path):
            # If the file exists, modify the new path by appending the counter and extension to the base filename.
            new_path = f"{base}_{counter}{ext}"

            # Increment the counter for the next iteration.
            counter += 1

        # Return the generated non-conflicting filename.
        return new_path
    except Exception as e:
        # Log error and display an error message when get non-conflicting file name fails.
        if self.activate_logging_var.get():
            logging.error(f"Error getting non-conflicting file name: {str(e)}")
        messagebox.showerror("Error", f"Error getting non-conflicting file name: {str(e)}")

        # Return None in case of an error.
        return None


# Method to rotate a video clip by a specified angle.
def rotate_video(self, clip, rotation_angle):
    try:
        # Rotate the video clip by the specified angle.
        rotated_clip = clip.rotate(rotation_angle)

        # Log rotation success if logging is activated.
        if self.activate_logging_var.get():
            logging.info(f"Rotation successful {clip} {rotation_angle}")

        # Return the rotated video clip.
        return rotated_clip
    except Exception as e:
        # Log error and display an error message if rotation fails.
        if self.activate_logging_var.get():
            logging.error(f"Error rotating video: {str(e)}")
        messagebox.showerror("Error", f"Error rotating video: {str(e)}")

        # Return None in case of an error.
        return None


# Method to increase the volume of a video clip by a specified dB value.
def increase_volume(self, clip, increase_db):
    try:
        # Modify the volume of the video clip by converting dB to linear scale.
        modified_clip = clip.volumex(10 ** (increase_db / 20.0))

        # Return the modified video clip.
        return modified_clip

    except Exception as e:
        # Log error and display an error message if volume increase fails.
        if self.activate_logging_var.get():
            logging.error(f"Error increasing volume: {str(e)}")
        messagebox.showerror("Error", f"Error increasing volume: {str(e)}")

        # Return None in case of an error.
        return None


# Method to normalize the audio of a video clip by applying a volume multiplier.
def normalize_audio(self, clip, volume_multiplier):
    try:
        # Normalize the audio of the video clip by applying the specified volume multiplier.
        normalized_clip = clip.volumex(volume_multiplier)

        # Return the normalized video clip.
        return normalized_clip

    except Exception as e:
        # Log error and display an error message if audio normalization fails.
        if self.activate_logging_var.get():
            logging.error(f"Error normalizing audio: {str(e)}")
        messagebox.showerror("Error", f"Error normalizing audio: {str(e)}")

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
        if self.activate_logging_var.get():
            logging.error(f"An error occurred while removing line from file: {e}")


# TODO Optimize this
# Method to process video edits based on user inputs.
def process_video_edits(self):
    # Get input parameters from user interface.
    input_video = self.video_editor_display_entry.get()
    input_file = self.input_file_entry.get()
    video_output_directory = self.video_output_directory_entry.get()
    rotation = str(self.rotation_var.get())
    decibel = float(self.decibel_entry.get())
    audio_normalization = float(self.audio_normalization_entry.get())

    if rotation == "none":
        rotation = None

    if decibel == 0.0:
        decibel = None

    if audio_normalization == 0.0:
        audio_normalization = None

    # TODO Put this in configuration file or json file
    # Create a list of valid video extensions
    valid_extensions = ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.mpeg', '.mpg', '.m4v']

    # Check if an input file containing a list of video file paths is provided
    if input_file:
        # Read the input file and filter out lines with non-video extensions
        with open(input_file, 'r') as file:
            input_paths = [line.strip() for line in file if
                           os.path.splitext(line.strip())[1].lower() in valid_extensions]

        # Overwrite the input file with the filtered paths
        with open(input_file, 'w') as file:
            file.write('\n'.join(input_paths))

    # Check if the necessary parameters for video editing are provided
    if (input_video or input_file) and decibel is None and rotation is None and audio_normalization is None:
        if self.activate_logging_var.get():
            logging.error("Error: You need to specify an operation (audio increase, video rotation, "
                          "audio normalization, or a combination of them")
        messagebox.showerror("Error", "Error: You need to specify an operation (audio increase, video rotation, "
                                      "audio normalization, or a combination of them")
        return

    # Check for conflicting input parameters
    if input_video and input_file:
        if self.activate_logging_var.get():
            logging.error("Error: Both input video and input file specified. Please choose one.")
        messagebox.showerror("Error", "Error: Both input video and input file specified. Please choose one.")
        return

    # Check if at least one input source (video or file) is provided
    if not input_video and not input_file:
        if self.activate_logging_var.get():
            logging.error("Error: Either input video or input file must be specified.")
        messagebox.showerror("Error", "Error: Either input video or input file must be specified.")
        return

    # Define the list of input paths based on user input
    if input_video:
        input_paths = [input_video]
    else:
        with open(input_file, 'r') as file:
            input_paths = [line.strip() for line in file]

    # Process each input path
    for input_path in input_paths:
        try:
            # Check if the file name length exceeds 260 characters
            if len(input_path) > 260:
                if self.activate_logging_var.get():
                    logging.warning(f"File over 260 warning!!! Fix: {input_path}")

                # Create a temporary copy of the file
                temp_dir = os.path.dirname(input_path)
                temp_copy_path = os.path.join(temp_dir, 'temp_EXCEPTION.mp4')
                shutil.copyfile(input_path, temp_copy_path)

                # Extract filename, extension, and output directory
                filename, extension = os.path.splitext(os.path.basename(temp_copy_path))
                output_dir = os.path.dirname(temp_copy_path)

                # Initialize a list to keep track of operations
                operation_tags = []

                # Determine the rotation operation tag
                rotation_angle = None  # Default rotation angle

                if rotation:
                    if rotation is not None:  # Check if rotation is not set to "none"
                        rotation_tag = "ROTATED_" + rotation.upper()
                        operation_tags.append(rotation_tag)  # Add to the operations list

                        if rotation == "left":
                            rotation_angle = 90
                        elif rotation == "right":
                            rotation_angle = -90
                        elif rotation == "flip":
                            rotation_angle = -180
                else:
                    rotation_angle = None  # Reset rotation angle

                # Determine the volume increase operation tag
                if decibel:
                    volume_tag = f"INCREASED_{decibel}DB"
                    operation_tags.append(volume_tag)  # Add to the operations list

                # Determine the audio normalization operation tag
                if audio_normalization:
                    normalization_tag = f"NORMALIZED_{audio_normalization}"
                    operation_tags.append(normalization_tag)  # Add to the operations list

                # Join operation tags to create a filename suffix
                operation_suffix = "_".join(operation_tags)

                # Create the output path with the operation suffix
                output_path = os.path.join(output_dir, f'{filename}_{operation_suffix}{extension}')

                # Adjust output path if a video output directory is specified
                if video_output_directory:
                    output_path = os.path.join(video_output_directory, os.path.basename(output_path))

                # Get a non-conflicting name for the output path
                output_path = get_non_conflicting_filename(self, output_path)

                # Load the original video clip
                original_clip = VideoFileClip(temp_copy_path)
                successful_operations = True

                # Apply operations in sequence, checking for success
                if rotation is not None and successful_operations:
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

                # Write the final modified clip to the output path if all operations were successful
                if successful_operations:
                    original_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                    if self.activate_logging_var.get():
                        logging.info(f"Video {operation_suffix.lower()} saved as {output_path}")
                    self.show_message(f"Video {operation_suffix.lower()} saved as {output_path}",
                                      frame_name="video_editor_window")

                    # Remove the successfully processed line from the input file
                    if input_file:
                        remove_successful_line_from_file(self, input_file, input_path)
                else:
                    if self.activate_logging_var.get():
                        logging.error(f"Error: Operations failed for video {input_path}")
                    messagebox.showerror("Error", f"Error: Operations failed for video {input_path}")

                # Close the original clip to free resources
                original_clip.close()

                # Delete the temporary copy
                os.remove(temp_copy_path)

            else:
                # Extract filename, extension, and output directory
                filename, extension = os.path.splitext(os.path.basename(input_path))
                output_dir = os.path.dirname(input_path)

                # Initialize a list to keep track of operations
                operation_tags = []

                # Determine the rotation operation tag
                rotation_angle = None  # Default rotation angle

                if rotation:
                    if rotation is not None:  # Check if rotation is not set to "none"
                        rotation_tag = "ROTATED_" + rotation.upper()
                        operation_tags.append(rotation_tag)  # Add to the operations list

                        if rotation == "left":
                            rotation_angle = 90
                        elif rotation == "right":
                            rotation_angle = -90
                        elif rotation == "flip":
                            rotation_angle = -180
                else:
                    rotation_angle = None  # Reset rotation angle

                # Determine the volume increase operation tag
                if decibel:
                    volume_tag = f"INCREASED_{decibel}DB"
                    operation_tags.append(volume_tag)  # Add to the operations list

                # Determine the audio normalization operation tag
                if audio_normalization:
                    normalization_tag = f"NORMALIZED_{audio_normalization}"
                    operation_tags.append(normalization_tag)  # Add to the operations list

                # Join operation tags to create a filename suffix
                operation_suffix = "_".join(operation_tags)

                # Create the output path with the operation suffix
                output_path = os.path.join(output_dir, f'{filename}_{operation_suffix}{extension}')

                # Adjust output path if a video output directory is specified
                if video_output_directory:
                    output_path = os.path.join(video_output_directory, os.path.basename(output_path))

                # Get a non-conflicting name for the output path
                output_path = get_non_conflicting_filename(self, output_path)

                # Load the original video clip
                original_clip = VideoFileClip(input_path)
                successful_operations = True

                # Apply operations in sequence, checking for success
                if rotation is not None and successful_operations:
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

                # Write the final modified clip to the output path if all operations were successful
                if successful_operations:
                    original_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
                    if self.activate_logging_var.get():
                        logging.info(f"Video {operation_suffix.lower()} saved as {output_path}")
                    self.show_message(f"Video {operation_suffix.lower()} saved as {output_path}",
                                      frame_name="video_editor_window")

                    # Remove the successfully processed line from the input file
                    if input_file:
                        remove_successful_line_from_file(self, input_file, input_path)
                else:
                    if self.activate_logging_var.get():
                        logging.error(f"Error: Operations failed for video {input_path}")
                    messagebox.showerror("Error", f"Error: Operations failed for video {input_path}")

                # Close the original clip to free resources
                original_clip.close()

        except OSError as e:
            # Log error and skip to the next file in case of OSError
            if self.activate_logging_var.get():
                logging.error(f"OSError: {str(e)} Skipping this file and moving to the next one.")
            messagebox.showerror("Error", f"OSError: {str(e)} Skipping this file and moving to the next one.")
            continue


# Method to browse and select a file for video editing.
def browse_video_editor_file_path(self):
    video_editor_folder_path = filedialog.askopenfilename(initialdir=self.initial_directory)
    self.video_editor_display_text = video_editor_folder_path
    self.video_editor_display_entry.delete(0, ctk.END)
    self.video_editor_display_entry.insert(0, self.video_editor_display_text)


# Method to browse and select a file containing a line delimited list of files to process
def browse_list_of_files_to_edit_file(self):
    input_file = filedialog.askopenfilename(
        initialdir=self.initial_directory,
        filetypes=[("Text Files", "*.txt")])
    self.input_file_entry.delete(0, ctk.END)
    self.input_file_entry.insert(0, input_file)


# Method to browse and select a folder to move the processed files
def browse_video_output_directory(self):
    video_output_directory = filedialog.askdirectory(initialdir=self.initial_output_directory)
    self.video_output_directory_entry.delete(0, ctk.END)
    self.video_output_directory_entry.insert(0, video_output_directory)


# Function to clear the selection and update the GUI
def clear_video_editor_selection(self):
    self.video_editor_display_entry.delete(0, ctk.END)
    self.input_file_entry.delete(0, ctk.END)
    self.video_output_directory_entry.delete(0, ctk.END)

    # Clear decibel entry and set default value
    self.decibel_entry.delete(0, ctk.END)
    self.decibel_entry.insert(0, self.default_decibel)

    # Clear audio normalization entry and set default value
    self.audio_normalization_entry.delete(0, ctk.END)
    self.audio_normalization_entry.insert(0, self.default_audio_normalization)
