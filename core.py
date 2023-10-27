import os
import re
import json
from tkinter import filedialog, messagebox
import send2trash
import subprocess
import platform
import customtkinter as ctk
import configparser

# Create a configuration parser
config = configparser.ConfigParser()
config.read('config.ini')

# Read configuration options
INITIAL_DIRECTORY = config.get('Paths', 'INITIAL_DIRECTORY')
CATEGORIES_FILE = config.get('Files', 'CATEGORIES_FILE')


def browse_output_directory(self):
    output_directory = filedialog.askdirectory(initialdir=INITIAL_DIRECTORY)

    if output_directory:
        self.output_directory = output_directory
        self.output_directory_entry.delete(0, ctk.END)
        self.output_directory_entry.insert(0, self.output_directory)


def move_to_trash(self):
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


def load_last_used_file(self):
    if self.last_used_file:
        self.selected_file = self.last_used_file
        self.file_display.configure(text=os.path.basename(self.selected_file))
        self.queue = []
        self.update_file_display()
        self.show_message("Last used file selected: " + os.path.basename(self.selected_file))


def on_drop(self, event):
    self.selected_file = event.data.strip('{}')
    self.file_display.configure(text=os.path.basename(self.selected_file))  # Display only the filename
    self.queue = []
    self.update_file_display()
    self.show_message("File selected: " + os.path.basename(self.selected_file))  # Update the message

    if self.open_on_drop_var.get():
        if platform.system() == "Linux":
            # Open the dropped file using xdg-open on Linux
            subprocess.Popen(['xdg-open', self.selected_file])
        elif platform.system() == "Windows":
            # Open the dropped file using the Windows start command. shell=True
            subprocess.Popen(['start', self.selected_file])
        else:
            # Use 'open' command on macOS, you can customize this as needed
            subprocess.Popen(['open', self.selected_file])


def add_to_queue(self, category):
    if self.selected_file:
        if category in self.weights:
            self.queue.insert(self.weights[category] - 1, category)
        else:
            self.queue.append(category)

        self.update_file_display()
        self.show_message("Word added: " + category)


def update_file_display(self):
    if self.selected_file:
        custom_text = self.custom_text_entry.get().strip()
        new_name = os.path.splitext(self.selected_file)[0] + " " + custom_text + " " + " ".join(self.queue) + \
            os.path.splitext(self.selected_file)[1]

        # Remove double spaces and trailing spaces
        new_name = " ".join(new_name.split())  # Remove double spaces
        new_name = new_name.strip()  # Remove trailing spaces

        self.file_display.configure(text=os.path.basename(new_name))


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
        if col == 6:
            col = 0
            row += 1


def load_categories():
    try:
        with open(CATEGORIES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_categories(self):
    with open(CATEGORIES_FILE, "w") as file:
        json.dump(self.categories, file)


def rename_files(self):
    if self.selected_file and (self.queue or self.custom_text_entry.get().strip()):
        custom_text = self.custom_text_entry.get().strip()
        base_name, extension = os.path.splitext(os.path.basename(self.selected_file))

        if self.remove_duplicates_var.get():
            self.queue = list(dict.fromkeys(self.queue))

        weighted_categories = [category for category in self.queue if category in self.weights]
        weighted_categories.sort(key=lambda category: self.weights[category])

        new_name = self.construct_new_name(base_name, custom_text, extension)

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
            self.show_message("Error: " + str(e), error=True)


def construct_new_name(self, base_name, custom_text, extension):
    # Construct the new name based on placement choice (prepend or append)
    if self.placement_choice.get() == "prepend":
        new_name = f"{custom_text} {base_name} {' '.join(self.queue)}"
    else:  # Default to append
        new_name = f"{base_name} {' '.join(self.queue)} {custom_text}"
    return new_name + extension


def move_text(name):
    match = re.match(r"^(.*) - (.*?)__-__ (.*)\.(\w+)$", name)
    if match:
        prepend, moved_text, append, extension = match.groups()
        name = f"{prepend} {append} {moved_text}.{extension}"
    return name


def sanitize_file_name(name):
    # Remove double spaces and trailing spaces
    return " ".join(name.split()).strip()


def handle_rename_success(self, new_path):
    self.selected_file = ""
    self.queue = []
    self.file_display.configure(text="")
    self.custom_text_entry.delete(0, ctk.END)
    self.last_used_file = new_path
    self.last_used_display.configure(text=os.path.basename(new_path))
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


def browse_file(self):
    file_path = filedialog.askopenfilename(initialdir=INITIAL_DIRECTORY)
    if file_path:
        self.selected_file = file_path
        self.file_display.configure(text=self.selected_file)
        self.queue = []  # Clear the queue when a new file is selected
        self.update_file_display()
        self.show_message("File selected: " + os.path.basename(self.selected_file))


def show_message(self, message, error=False):
    if error:
        self.message_label.configure(text=message, text_color="red")
    else:
        self.message_label.configure(text=message, text_color="white")
