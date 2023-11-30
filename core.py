import os
import re
import json
from tkinter import filedialog, messagebox
import send2trash
import subprocess
import customtkinter as ctk
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

"""
Configuration
"""


def load_configuration():
    # Read the settings
    move_text_var = config.getboolean('Settings', 'move_text_var', fallback=True)
    initial_directory = config.get('Filepaths', 'initial_directory')
    categories_file = config.get('Filepaths', 'categories_file')
    weighted_categories_file = config.get('Filepaths', 'weighted_categories_file')
    geometry = config.get('Settings', 'geometry', fallback='1280x750+0+0')
    reset_output_directory_var = config.get("Settings", "reset_output_directory_var", fallback=False)
    move_up_var = config.getboolean("Settings", "move_up_var", fallback=False)
    open_on_file_drop_var = config.get("Settings", "open_on_file_drop_var", fallback=False)
    remove_duplicates_var = config.getboolean("Settings", "remove_duplicates_var", fallback=True)
    default_placement_var = config.get("Settings", "default_placement_var", fallback="first_dash")

    return (move_text_var, initial_directory, categories_file, weighted_categories_file, geometry,
            reset_output_directory_var, move_up_var, open_on_file_drop_var, remove_duplicates_var,
            default_placement_var)


"""
File Operations
"""


def move_file_to_trash(self):
    try:
        if self.selected_file:
            confirmation = messagebox.askyesno("Confirm Action",
                                               "Are you sure you want to move this file to the trash?")
            if confirmation:
                send2trash.send2trash(self.selected_file)
                self.selected_file = ""
                self.queue = []
                self.file_display.configure(text="")
                self.custom_text_entry.delete(0, ctk.END)
                self.show_message("File moved to trash successfully")
    except OSError as e:
        # Construct the error message and truncate after 50 characters
        error_message = "Error: " + str(e)
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
        if len(message) > 127:
            message = message[:127]

        self.show_message("Last used file selected: " + message + "...")


def on_file_drop(self, event):
    self.selected_file = event.data.strip('{}')
    self.file_display.configure(text=os.path.basename(self.selected_file))  # Display only the filename
    self.queue = []
    self.update_file_display()
    # Get the base file name and truncate if longer than 50 characters
    message = os.path.basename(self.selected_file)
    if len(message) > 127:
        message = message[:127]

    self.show_message("File selected: " + message + "...")

    if self.open_on_file_drop_var.get():
        try:
            subprocess.Popen(['xdg-open', self.selected_file])  # I use Arch, btw.
        except OSError as e:
            # Construct the error message and truncate after 50 characters
            error_message = "Error: " + str(e)
            if len(error_message) > 115:
                error_message = error_message[:115]
            self.show_message(error_message, error=True)


def add_to_queue(self, category):
    if self.selected_file:
        if category in self.weights:
            # Check if the category is not already in the queue
            if category not in self.queue:
                self.queue.insert(self.weights[category] - 1, category)
        else:
            # Check if the category is not already in the queue
            if category not in self.queue:
                self.queue.append(category)

        self.update_file_display()
        self.show_message("Word added: " + category)


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


def clear_selection(self):
    self.selected_file = ""
    self.queue = []
    self.file_display.configure(text="")
    self.show_message("Selection cleared")

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

        # Get the base file name and truncate if longer than 127 characters
        message = os.path.basename(self.selected_file)
        if len(message) > 127:
            message = message[:127]

        self.show_message("File selected: " + message + "...")


def browse_output_directory(self):
    output_directory = filedialog.askdirectory(initialdir=self.initial_directory)

    if output_directory:
        self.output_directory = output_directory
        self.output_directory_entry.delete(0, ctk.END)
        self.output_directory_entry.insert(0, self.output_directory)


def handle_rename_success(self, new_path):
    self.selected_file = ""
    self.queue = []
    self.file_display.configure(text="")
    self.custom_text_entry.delete(0, ctk.END)
    self.last_used_file = new_path
    # Get the base name and truncate after 115 characters
    last_used_name = os.path.basename(new_path)
    if len(last_used_name) > 115:
        last_used_name = last_used_name[:115]
    self.last_used_display.configure(text=last_used_name)

    self.show_message("File renamed and saved successfully")

    if self.move_up_var.get():
        # Move the file up one folder
        parent_directory = os.path.dirname(os.path.dirname(new_path))
        new_location = os.path.join(parent_directory, os.path.basename(new_path))
        os.rename(new_path, new_location)
        self.selected_file = new_location

    if self.reset_output_directory_var.get():
        # Clear and reset the Output Directory to the current directory
        self.output_directory = os.path.dirname(self.selected_file)
        self.output_directory_entry.delete(0, ctk.END)
        self.output_directory_entry.insert(0, self.output_directory)


"""
Category Management
"""


def add_category(self):
    new_category = self.category_entry.get().strip()
    if new_category:
        self.categories.append(new_category)
        self.categories.sort(key=lambda x: x.lower())
        self.save_categories()
        self.refresh_category_buttons()
        self.category_entry.delete(0, ctk.END)
        self.show_message("Category added: " + new_category)


def remove_category(self):
    category_to_remove = self.remove_category_entry.get().strip()
    if category_to_remove in self.categories:
        self.categories.remove(category_to_remove)
        self.save_categories()
        self.refresh_category_buttons()
        self.remove_category_entry.delete(0, ctk.END)
        self.show_message("Category removed: " + category_to_remove)


def load_weights():
    weighted_categories_file = config.get("Filepaths", "weighted_categories_file")
    try:
        with open(weighted_categories_file, 'r') as f:
            weights = json.load(f)
        return weights
    except FileNotFoundError:
        print(f"Error: json file not found.")
        return {}  # Return an empty dictionary if the file is not found


def categories_buttons_initialize(self):
    # Load categories from a configuration file
    categories_file = config.get("Filepaths", "categories_file")
    try:
        with open(categories_file, "r") as file:
            self.categories = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        self.categories = []

    # Sort the categories alphabetically, case-insensitive
    self.categories.sort(key=lambda x: x.lower())

    self.buttons = []
    row = 0
    col = 0
    for category in self.categories:
        button = ctk.CTkButton(self.button_frame, text=category,
                               command=lambda c=category: self.add_to_queue(c))
        button.grid(row=row, column=col, padx=5, pady=5)
        self.buttons.append(button)
        col += 1
        if col == 7:
            col = 0
            row += 1


def refresh_category_buttons(self):
    for button in self.buttons:
        button.destroy()

    self.buttons = []
    row = 0
    col = 0
    for category in self.categories:
        button = ctk.CTkButton(self.button_frame, text=category, command=lambda c=category: self.add_to_queue(c))
        button.grid(row=row, column=col, padx=5, pady=5)
        self.buttons.append(button)
        col += 1
        if col == 7:
            col = 0
            row += 1


def save_categories(self):
    categories_file = config.get("Filepaths", "categories_file")
    with open(categories_file, "w") as file:
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

        weighted_categories = [category for category in self.queue if category in self.weights]
        weighted_categories.sort(key=lambda category: self.weights[category])

        new_name = self.construct_new_name(base_name, weighted_categories, custom_text, extension)

        if self.move_text_var.get():
            new_name = self.move_text(new_name)

        new_name = self.sanitize_file_name(new_name)

        if not self.output_directory:
            self.output_directory = os.path.dirname(self.selected_file)

        new_path = os.path.join(self.output_directory, os.path.basename(new_name))
        try:
            os.rename(self.selected_file, new_path)
            self.handle_rename_success(new_path)
        except OSError as e:
            # Construct the error message and truncate after 50 characters
            error_message = "Error: " + str(e)
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
                # Construct the error message and truncate after 50 characters
                error_message = "Error: " + str(e)
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


def sanitize_file_name(name):
    # Remove double spaces and trailing spaces
    return " ".join(name.split()).strip()
