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
    # Load the configuration from the config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Directories
    initial_directory = config.get('Filepaths', 'initial_directory', fallback='~')
    artist_directory = config.get('Filepaths', 'artist_directory', fallback='~')
    double_check_directory = config.get('Filepaths', 'double_check_directory', fallback='~')
    categories_file = config.get('Filepaths', 'categories_file', fallback='~')

    # Variables and window geometry
    reset_output_directory_var = config.getboolean("Settings", "reset_output_directory_var", fallback=False)
    suggest_output_var = config.getboolean("Settings", "suggest_output_var", fallback=False)
    move_text_var = config.getboolean('Settings', 'move_text_var', fallback=True)
    move_up_var = config.getboolean("Settings", "move_up_var", fallback=False)
    open_on_file_drop_var = config.getboolean("Settings", "open_on_file_drop_var", fallback=False)
    remove_duplicates_var = config.getboolean("Settings", "remove_duplicates_var", fallback=True)
    double_check_var = config.getboolean("Settings", "double_check_var", fallback=False)
    geometry = config.get('Settings', 'geometry', fallback='1280x750+0+0')
    ocd_file_renamer_log = config.get('Logs', 'ocd_file_renamer_log')
    default_placement_var = config.get("Settings", "default_placement_var", fallback="first_dash")

    # Initialize logging
    logging.basicConfig(filename=ocd_file_renamer_log, level=logging.INFO, filemode='a',
                        format='%(asctime)s - %(levelname)s: %(message)s')

    return (move_text_var, initial_directory, artist_directory, double_check_directory, categories_file,
            geometry,
            reset_output_directory_var, suggest_output_var, move_up_var, open_on_file_drop_var, remove_duplicates_var,
            default_placement_var, double_check_var, ocd_file_renamer_log)


"""
File Operations
"""


def move_file_to_trash(self):
    try:
        if self.selected_file:
            confirmation = messagebox.askyesno("Confirm Action",
                                               "Are you sure you want to move this file to the trash?")
            logging.info(f"'{self.selected_file}' selected for deletion.")
            if confirmation:
                send2trash.send2trash(self.selected_file)
                self.selected_file = ""
                self.queue = []
                self.file_display.configure(text="")
                self.custom_text_entry.delete(0, ctk.END)
                logging.info(f"File moved to trash.")
                self.show_message("File moved to trash successfully")
        else:
            logging.error("No file selected. Cannot move to trash.")
            self.show_message("No file selected. Cannot move to trash.", error=True)
    except OSError as e:
        # Construct the error message and truncate after x characters
        error_message = f"Error: {str(e)}"
        logging.error(error_message)
        if len(error_message) > 115:
            error_message = error_message[:115]
        self.show_message(error_message, error=True)


def load_last_used_file(self):
    if self.last_used_file:
        self.selected_file = self.last_used_file
        self.file_display.configure(text=os.path.basename(self.selected_file))
        self.queue = []
        self.update_file_display()

        message = os.path.basename(self.selected_file)
        logging.info(f"Last used file selected: {message}")
        if len(message) > 127:
            message = message[:127] + "..."

        self.show_message(f"Last used file selected: {message}")
    else:
        logging.error("No last used file found.")
        self.show_message("Error: No last used file found.", error=True)


def on_file_drop(self, event):
    self.selected_file = event.data.strip('{}')
    self.file_display.configure(text=os.path.basename(self.selected_file))  # Display only the filename
    self.queue = []
    self.update_file_display()

    # Get the base file name and truncate after x characters
    message = os.path.basename(self.selected_file)
    logging.info(f"File selected: {message}")
    if len(message) > 127:
        message = message[:127] + "..."

    self.show_message(f"File selected via drop: {message}")

    if self.open_on_file_drop_var.get():
        try:
            subprocess.Popen(['xdg-open', self.selected_file])  # I use Arch, btw.
            logging.info(f"File opened: {self.selected_file}")
        except OSError as e:
            # Construct the error message and truncate after x characters
            error_message = f"Error: {str(e)}"
            logging.error(error_message)
            if len(error_message) > 115:
                error_message = error_message[:115]
            self.show_message(error_message, error=True)


def add_to_queue(self, category):
    if self.selected_file:
        # Check if the category is not already in the queue
        if category not in self.queue:
            self.queue.append(category)

        self.update_file_display()
        self.show_message(f"Word added: {category}")


def update_file_display(self):
    if self.selected_file:
        custom_text = self.custom_text_entry.get().strip()

        # Use only the base name of the file, not the full path
        base_file_name = os.path.basename(self.selected_file)

        # Construct the new name
        new_name = os.path.splitext(base_file_name)[0] + " " + custom_text + " " + " ".join(self.queue) + \
            os.path.splitext(base_file_name)[1]

        # Remove double spaces and trailing spaces
        new_name = " ".join(new_name.split())  # Remove double spaces
        new_name = new_name.strip()  # Remove trailing spaces

        if len(new_name) > 250:
            messagebox.showinfo("Length Exceeded", "The new file name exceeds 250 characters. Please shorten it.")
            new_name = "..." + new_name[180:]
        elif len(new_name) > 120:
            new_name = new_name[:120] + "..."

        # Set the new name to the file display
        self.file_display.configure(text=new_name)


def undo_last(self):
    if self.queue:
        self.queue.pop()
        self.update_file_display()
        self.show_message("Last category removed")
    else:
        logging.error("Nothing in the queue. Nothing to undo.")
        self.show_message("Error: Nothing in the queue. Nothing to undo.", error=True)


def clear_selection(self):
    self.selected_file = ""
    self.queue = []
    self.file_display.configure(text="")
    self.show_message("Selection cleared")

    self.custom_text_entry.delete(0, ctk.END)
    self.output_directory = os.path.dirname(self.selected_file)
    self.output_directory_entry.delete(0, ctk.END)
    self.output_directory_entry.insert(0, self.output_directory)


def browse_file(self):
    file_path = filedialog.askopenfilename(initialdir=self.initial_directory)
    if file_path:
        self.selected_file = file_path
        self.file_display.configure(text=self.selected_file)
        self.queue = []
        self.update_file_display()

        # Get the base file name and truncate after x characters
        message = os.path.basename(self.selected_file)
        logging.info(f"File selected via Browse: {message}")
        if len(message) > 127:
            message = message[:127] + "..."

        self.show_message(f"File selected: {message}")


def browse_output_directory(self):
    # Check if a file is selected
    if self.selected_file:
        if self.suggest_output_var.get():
            base_name = os.path.basename(self.selected_file)

            # Extract the artist from the filename (before the dash)
            artist_match = re.match(r"^(.*?)\s*-\s*.*$", base_name)
            if artist_match:
                artist = artist_match.group(1).strip()

                # Construct the artist folder path
                artist_folder_path = os.path.join(self.artist_directory, artist)

                # Check if the artist folder exists
                if os.path.exists(artist_folder_path):
                    initial_directory = artist_folder_path
                else:
                    # If the artist folder doesn't exist, use the default initial directory
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
        self.output_directory = output_directory
        self.output_directory_entry.delete(0, ctk.END)
        self.output_directory_entry.insert(0, self.output_directory)


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

            logging.info(f"Empty file created successfully for {folder_name}")
            self.show_message(f"Empty file created successfully for {folder_name}")

        except Exception as e:
            # Handle any errors that may occur
            logging.error(f"Error creating empty file: {str(e)}")
            self.show_message(f"Error creating empty file: {str(e)}")

    self.selected_file = ""
    self.queue = []
    self.file_display.configure(text="")
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

    self.show_message("File renamed and saved successfully")


"""
Category Management
"""


def add_category(self):
    new_category = self.category_entry.get().strip()
    if new_category:
        new_category_lower = new_category.lower()  # Convert to lowercase for case-insensitive check
        # Prevent duplicate entries in the json file
        if new_category_lower not in map(str.lower, self.categories.keys()):
            self.categories[new_category] = None
            sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())
            self.save_categories()
            self.refresh_category_buttons(sorted_categories)
            self.category_entry.delete(0, ctk.END)
            self.show_message(f"Category added: {new_category}")
        else:
            self.show_message(f"Error: '{new_category}' already exists. Skipping.", error=True)
            self.category_entry.delete(0, ctk.END)


def remove_category(self):
    category_to_remove = self.remove_category_entry.get().strip()
    if category_to_remove in self.categories:
        del self.categories[category_to_remove]
        sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())
        self.save_categories()
        self.refresh_category_buttons(sorted_categories)
        self.remove_category_entry.delete(0, ctk.END)
        self.show_message(f"Category removed: {category_to_remove}")


def categories_buttons_initialize(self):
    # Load categories
    try:
        with open(self.categories_file, "r") as file:
            self.categories = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        self.categories = {}

    # Sort the category keys alphabetically, case-insensitive
    sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())

    self.buttons = []
    row = 0
    col = 0
    for category in sorted_categories:
        button = ctk.CTkButton(self.button_frame, text=category,
                               command=lambda c=category: self.add_to_queue(c))
        button.grid(row=row, column=col, padx=5, pady=5)
        self.buttons.append(button)
        col += 1
        if col == 7:
            col = 0
            row += 1


def refresh_category_buttons(self, sorted_categories=None):
    if sorted_categories is None:
        sorted_categories = sorted(self.categories.keys(), key=lambda x: x.lower())

    for button in self.buttons:
        button.destroy()

    self.buttons = []
    row = 0
    col = 0
    for category in sorted_categories:
        button = ctk.CTkButton(self.button_frame, text=category, command=lambda c=category: self.add_to_queue(c))
        button.grid(row=row, column=col, padx=5, pady=5)
        self.buttons.append(button)
        col += 1
        if col == 7:
            col = 0
            row += 1


def save_categories(self):
    with open(self.categories_file, "w") as file:
        json.dump(self.categories, file)


"""
File Renaming
"""


def rename_files(self):
    if self.selected_file and (self.queue or self.custom_text_entry.get().strip()):
        custom_text = self.custom_text_entry.get().strip()
        base_name, extension = os.path.splitext(os.path.basename(self.selected_file))

        if self.remove_duplicates_var.get():
            self.queue = list(dict.fromkeys(self.queue))

        weighted_categories = [category for category in self.queue if category in self.categories]
        weighted_categories.sort(key=lambda category: self.categories.get(category, 0))  # Use 0 as default weight

        new_name = self.construct_new_name(base_name, weighted_categories, custom_text, extension)

        if self.move_text_var.get():
            new_name = self.move_text(new_name)

        new_name = " ".join(new_name.split()).strip()

        # If output directory is not explicitly set, then default to the same directory as the file
        if not self.output_directory:
            self.output_directory = os.path.dirname(self.selected_file)

        if self.move_up_var.get():
            # Ignore the provided output directory and move the file up one folder
            parent_directory = os.path.dirname(os.path.dirname(self.selected_file))
            new_path = os.path.join(parent_directory, os.path.basename(new_name))
        else:
            new_path = os.path.join(self.output_directory, os.path.basename(new_name))

        # TODO put suggest_output_var logic here
        # if self.suggest_output_var.get():
        #     pass

        try:
            os.rename(self.selected_file, new_path)
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
    match = re.match(r"^(.*) - (.*?)__-__ (.*)\.(\w+)$", name)
    if match:
        prefix, moved_text, suffix, extension = match.groups()
        name = f"{prefix} {suffix} {moved_text}.{extension}"
    return name
