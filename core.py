import os
import re
import json
from tkinter import filedialog, messagebox
import send2trash
import subprocess
import customtkinter as ctk
import logging
import configparser

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

    # Directories
    initial_directory = config.get('Filepaths', 'initial_directory', fallback='~')
    artist_directory = config.get('Filepaths', 'artist_directory', fallback='~')
    double_check_directory = config.get('Filepaths', 'double_check_directory', fallback='~')
    categories_file = config.get('Filepaths', 'categories_file', fallback='~')

    # Variables and window geometry
    geometry = config.get('Settings', 'geometry', fallback='1280x800')
    column_numbers = config.get('Settings', 'column_numbers', fallback=7)
    default_weight = config.get('Settings', 'default_weight', fallback=9)
    ocd_file_renamer_log = config.get('Logs', 'ocd_file_renamer_log', fallback="ocd_file_renamer.log")
    default_placement_var = config.get("Settings", "default_placement_var", fallback="first_dash")
    reset_output_directory_var = config.getboolean("Settings", "reset_output_directory_var", fallback=False)
    suggest_output_directory_var = config.getboolean("Settings", "suggest_output_directory_var", fallback=False)
    move_up_directory_var = config.getboolean("Settings", "move_up_directory_var", fallback=False)
    move_text_var = config.getboolean('Settings', 'move_text_var', fallback=False)
    open_on_file_drop_var = config.getboolean("Settings", "open_on_file_drop_var", fallback=False)
    remove_duplicates_var = config.getboolean("Settings", "remove_duplicates_var", fallback=True)
    double_check_var = config.getboolean("Settings", "double_check_var", fallback=False)
    activate_logging_var = config.getboolean("Settings", "activate_logging_var", fallback=False)

    # Return the loaded configuration values as a tuple
    return (move_text_var, initial_directory, artist_directory, double_check_directory, categories_file,
            geometry, reset_output_directory_var, suggest_output_directory_var, move_up_directory_var,
            open_on_file_drop_var, remove_duplicates_var, default_placement_var, double_check_var,
            activate_logging_var, ocd_file_renamer_log, column_numbers, default_weight)


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
                    logging.info("File moved to trash.")
                self.show_message("File moved to trash successfully")
        else:
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error("No file selected. Cannot move to trash.")
            self.show_message("No file selected. Cannot move to trash.", error=True)
    except OSError as e:
        # Construct the error message and truncate after x characters
        error_message = f"Error: {str(e)}"
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.error(error_message)
        if len(error_message) > 115:
            error_message = error_message[:115]
        self.show_message(error_message, error=True)


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
        if len(message) > 127:
            message = message[:127] + "..."

        self.show_message(f"Last used file selected: {message}")
    else:
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.error("No last used file found.")
        self.show_message("Error: No last used file found.", error=True)


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

    # Log the error, truncate after x characters and display the error in the gui
    message = filename
    if self.activate_logging_var.get():
        # Log the action if logging is enabled
        logging.info(f"File selected: {message}")
    if len(message) > 127:
        message = message[:127] + "..."

    self.show_message(f"File selected via drop: {message}")

    # Open the file if the corresponding option is set
    if self.open_on_file_drop_var.get():
        try:
            subprocess.Popen(['xdg-open', self.selected_file])  # I use Arch, btw.
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.info(f"File opened: {self.selected_file}")
        except OSError as e:
            # Construct the error message and truncate after x characters
            error_message = f"Error: {str(e)}"
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error(error_message)
            if len(error_message) > 115:
                error_message = error_message[:115]
            self.show_message(error_message, error=True)


# Function to add a category to the queue
def add_to_queue(self, category):
    if self.selected_file:
        # Check if the category is not already in the queue
        if category not in self.queue:
            self.queue.append(category)

        # Update file display and show a message
        self.update_file_display()
        self.show_message(f"Word added: {category}")


# Function to update the file display based on selected options
def update_file_display(self):
    if self.selected_file:
        custom_text = self.custom_text_entry.get().strip()

        # Use only the base name of the file, not the full path
        base_file_name = os.path.basename(self.selected_file)

        # Construct the new name
        new_name_parts = [
            os.path.splitext(base_file_name)[0],
            custom_text,
            " ".join(self.queue),
            os.path.splitext(base_file_name)[1]
        ]

        # Join the parts and remove double spaces and trailing spaces
        new_name = " ".join(part for part in new_name_parts if part).strip()

        # Handle name length constraints
        if len(new_name) > 250:
            messagebox.showinfo("Length Exceeded", "The proposed file name exceeds 250 characters. Please consider "
                                                   "shortening it to comply with operating system limitations.")
            new_name = "..." + new_name[180:]

        # Set the new name to the file display
        self.file_display_text.set(new_name)


# Function to undo the last category added to the queue
def undo_last(self):
    if self.queue:
        # Remove the last category from the queue and update display
        self.queue.pop()
        self.update_file_display()
        self.show_message("Last category removed")
    else:
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.error("Nothing in the queue. Nothing to undo.")
        self.show_message("Error: Nothing in the queue. Nothing to undo.", error=True)


# Function to clear the selection and reset related elements
def clear_selection(self):
    self.selected_file = ""
    self.queue = []
    self.file_display_text.set("")
    self.show_message("Selection cleared")

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

        # Log the error, truncate after x characters and display the error in the gui
        message = filename
        if self.activate_logging_var.get():
            # Log the action if logging is enabled
            logging.info(f"File selected via Browse: {message}")
        if len(message) > 127:
            message = message[:127] + "..."

        self.show_message(f"File selected: {message}")


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
            self.show_message(f"Empty file created successfully for {folder_name}")

        except Exception as e:
            # Handle any errors that may occur
            if self.activate_logging_var.get():
                # Log the action if logging is enabled
                logging.error(f"Error creating empty file: {str(e)}")
            self.show_message(f"Error creating empty file: {str(e)}")

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

    # Show a success message
    self.show_message("File renamed and saved successfully")


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
            # Add the new category to the dictionary with a default weight
            # TODO Add a dynamic prompt
            self.categories[new_category] = self.default_weight
            # Sort categories alphabetically, case-insensitive
            sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())
            # Save the updated categories to the file
            self.save_categories()
            # Refresh the category buttons in the GUI
            self.refresh_category_buttons(sorted_categories)
            # Clear the category entry field
            self.category_entry.delete(0, ctk.END)
            # Show a success message
            self.show_message(f"Category added: {new_category}")
        else:
            # Show an error message if the category already exists
            self.show_message(f"Error: '{new_category}' already exists. Skipping.", error=True)
            # Clear the category entry field
            self.category_entry.delete(0, ctk.END)


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
        # Show a success message
        self.show_message(f"Category removed: {category_to_remove}")
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
            # Show a success message
            self.show_message(f"Category removed: {matching_category}")
        else:
            # Show an error message if no matching category is found
            self.show_message(f"Error: '{category_to_remove}' not found in dictionary. Skipping.", error=True)


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

        # Construct a new name using base name, weighted categories, custom text, and extension
        new_name = self.construct_new_name(base_name, weighted_categories, custom_text, extension)

        # If move_text_var is set, move the text between - and __-__
        if self.move_text_var.get():
            new_name = self.move_text(new_name)

        # Remove extra whitespaces from the new name
        new_name = " ".join(new_name.split()).strip()

        # If output directory is not explicitly set, default to the same directory as the file
        if not self.output_directory:
            self.output_directory = os.path.dirname(self.selected_file)

        # Determine the new path based on user preferences
        if self.move_up_directory_var.get():
            # Ignore the provided output directory and move the file up one folder
            parent_directory = os.path.dirname(os.path.dirname(self.selected_file))
            new_path = os.path.join(parent_directory, os.path.basename(new_name))
        else:
            # Use the specified output directory
            new_path = os.path.join(self.output_directory, os.path.basename(new_name))

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
            # Construct the error message and truncate after x characters
            error_message = f"Error: {str(e)}"
            if len(error_message) > 115:
                error_message = error_message[:115]
            self.show_message(error_message, error=True)


def construct_new_name(self, base_name, weighted_categories, custom_text, extension):
    # Construct the new name based on placement choice (prefix, suffix, or first_dash)
    categories = weighted_categories + [category for category in self.queue if category not in weighted_categories]
    categories_text = ' '.join(categories).strip()

    if self.placement_choice.get() == "prefix":
        new_name = f"{custom_text} {categories_text} {base_name}".strip()
    elif self.placement_choice.get() == "first_dash":
        parts = base_name.split('-', 1)
        if len(parts) == 2:
            new_name = f"{parts[0].rstrip()} {categories_text} {custom_text} {parts[1].lstrip()}".strip()
            try:
                # Remove the tail __-__ if found
                new_name = new_name.replace("__-__", "")
            except OSError as e:
                # Construct the error message and truncate after x characters
                error_message = f"Error: {str(e)}"
                if len(error_message) > 115:
                    error_message = error_message[:115]
                self.show_message(error_message, error=True)
        else:
            # If there's no dash, default to suffix
            new_name = f"{base_name} {categories_text} {custom_text}".strip()
    else:  # Default to suffix
        new_name = f"{base_name} {categories_text} {custom_text}".strip()

    return new_name + extension


def move_text(name):
    # Move the text between - and __-__ in the name
    match = re.match(r"^(.*) - (.*?)__-__ (.*)\.(\w+)$", name)
    if match:
        prefix, moved_text, suffix, extension = match.groups()
        name = f"{prefix} {suffix} {moved_text}.{extension}"
    return name
