import os
import re
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, END
from tkinterdnd2 import DND_FILES, TkinterDnD
import send2trash
import subprocess
import platform
import core


class OCDFileRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("OCD File Renamer")

        self.selected_file = ""
        self.queue = []

        # Define weights for categories
        self.weights = {
            "Lo-fi": 1,
            "Acoustic": 2,
            "Tropical": 3,
        }

        # Variable to track whether to enable the text moving feature
        self.move_text_var = tk.BooleanVar()
        self.move_text_var.set(True)  # Default to disabled

        # Add a checkbox for moving the file up one folder
        self.move_up_var = tk.BooleanVar(value=False)

        # Variable to track whether to enable the reset output directory feature.
        self.reset_output_directory_var = tk.BooleanVar(value=False)  # Default state is not to reset

        # Initialize output directory
        self.output_directory = ""

        # Variable to track the user's placement choice (prefix or suffix)
        self.placement_choice = tk.StringVar()
        self.placement_choice.set("suffix")  # Default to suffix

        # Add a checkbox to enable/disable open on drop behavior
        self.open_on_drop_var = tk.BooleanVar(value=False)

        # Error message label
        self.message_label = tk.Label(self.root, text="", fg="red")
        self.message_label.pack()

        self.create_gui()

    def create_gui(self):
        # File Label
        self.file_label = tk.Label(self.root, text="Selected File:")
        self.file_label.pack()

        # Selected File Display
        self.file_display = tk.Label(self.root, text="")
        self.file_display.pack()

        # Browse Button
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        # Rename Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.categories = core.load_categories()  # Load categories from a configuration file
        self.categories.sort(key=lambda x: x.lower())

        self.buttons = []
        row = 0
        col = 0
        for category in self.categories:
            button = tk.Button(self.button_frame, text=category, command=lambda c=category: self.add_to_queue(c))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)
            col += 1
            if col == 8:
                col = 0
                row += 1
        # Create a frame for the category-related elements
        category_frame = ttk.Frame(self.root)
        category_frame.pack(pady=5)

        # Add Category Button
        self.add_category_button = tk.Button(category_frame, text="Add Category", command=self.add_category)
        self.add_category_button.grid(row=0, column=0, padx=5)

        # Add Category Entry
        self.category_entry = tk.Entry(category_frame)
        self.category_entry.grid(row=0, column=1, padx=5)

        # Remove Category Button
        self.remove_category_button = tk.Button(category_frame, text="Remove Category", command=self.remove_category)
        self.remove_category_button.grid(row=0, column=2, padx=5)

        # Remove Category Entry
        self.remove_category_entry = tk.Entry(category_frame)
        self.remove_category_entry.grid(row=0, column=3, padx=5)

        # Add a separator line underneath the category section
        category_separator = ttk.Separator(self.root, orient="horizontal")
        category_separator.pack(fill="x", pady=10)

        # Create a frame to group the custom text entry and Rename button
        custom_text_frame = ttk.Frame(self.root)
        custom_text_frame.pack(pady=5)

        # Output Directory Label
        output_directory_label = tk.Label(custom_text_frame, text="Output Directory:")
        output_directory_label.pack(side="left")

        # Output Directory Entry
        self.output_directory_entry = tk.Entry(custom_text_frame, width=40)
        self.output_directory_entry.pack(side="left")

        # Output Directory Browse Button
        output_directory_browse_button = tk.Button(custom_text_frame, text="Browse",
                                                   command=self.browse_output_directory)
        output_directory_browse_button.pack(side="left")

        # Custom Text Entry Label
        self.custom_text_label = tk.Label(custom_text_frame, text="Custom text entry:")
        self.custom_text_label.pack(side="left")

        # Custom Text Entry
        self.custom_text_entry = tk.Entry(custom_text_frame, width=40)
        self.custom_text_entry.pack(side="left")

        # Create a frame for the "Rename File" button
        rename_button_frame = ttk.Frame(self.root)
        rename_button_frame.pack(pady=5)

        # Add a frame for the placement choice and the new feature checkbox
        placement_feature_frame = ttk.Frame(self.root)
        placement_feature_frame.pack(pady=5)

        # Add a checkbox to enable/disable resetting the Output Directory
        self.reset_output_directory_checkbox = tk.Checkbutton(placement_feature_frame, text="Reset Output Directory",
                                                              variable=self.reset_output_directory_var)
        self.reset_output_directory_checkbox.pack(side="left")

        # Placement Label
        placement_label = tk.Label(placement_feature_frame, text="Placement:")
        placement_label.pack(side="left")

        # Radio button for Prefix
        prefix_radio = tk.Radiobutton(placement_feature_frame, text="Prefix", variable=self.placement_choice,
                                      value="prefix")
        prefix_radio.pack(side="left")

        # Radio button for Suffix
        suffix_radio = tk.Radiobutton(placement_feature_frame, text="Suffix", variable=self.placement_choice,
                                      value="suffix")
        suffix_radio.pack(side="left")

        # Rename File Button
        self.rename_button = tk.Button(placement_feature_frame, text="Rename File", command=self.rename_files)
        self.rename_button.pack(side="right")

        self.open_on_drop_checkbox = tk.Checkbutton(placement_feature_frame, text="Open on Drop",
                                                    variable=self.open_on_drop_var)
        self.open_on_drop_checkbox.pack(side="left", padx=5)

        # Checkbox for duplicate removal
        self.remove_duplicates_var = tk.BooleanVar(value=True)
        remove_duplicates_checkbox = tk.Checkbutton(placement_feature_frame, text="Remove Duplicates",
                                                    variable=self.remove_duplicates_var)
        remove_duplicates_checkbox.pack(side="left")

        # Checkbox for moving the file up one folder
        self.move_up_checkbox = tk.Checkbutton(placement_feature_frame, text="Move Up One Folder",
                                               variable=self.move_up_var)
        self.move_up_checkbox.pack(side="left", padx=5)

        # Checkbox for the new feature
        self.move_text_checkbox = tk.Checkbutton(placement_feature_frame, text="Move Text", variable=self.move_text_var,
                                                 onvalue=True, offvalue=False)
        self.move_text_checkbox.pack(side="right")

        # Add a separator line underneath the custom text section
        custom_text_separator = ttk.Separator(self.root, orient="horizontal")
        custom_text_separator.pack(fill="x", pady=10)

        # Create a frame to group the buttons
        button_group_frame = ttk.Frame(self.root)
        button_group_frame.pack()

        # Undo Button
        self.undo_button = tk.Button(button_group_frame, text="Undo", command=self.undo_last)
        self.undo_button.pack(side="left", padx=5)

        # Clear Button
        self.clear_button = tk.Button(button_group_frame, text="Clear", command=self.clear_selection)
        self.clear_button.pack(side="left", padx=5)

        # Move to Trash Button
        self.trash_button = tk.Button(button_group_frame, text="Move to Trash", command=self.move_to_trash)
        self.trash_button.pack(side="left", padx=5)

        # Create a frame to display the last used file
        last_used_frame = ttk.Frame(self.root)
        last_used_frame.pack(pady=5)

        # Select Last Used File Button
        self.last_used_file_button = tk.Button(last_used_frame, text="Select Last Used File",
                                               command=self.load_last_used_file)
        self.last_used_file_button.pack(side="left", padx=5)

        # Last Used File Display
        self.last_used_display = tk.Label(last_used_frame, text="")
        self.last_used_display.pack(side="left", padx=5)

        # Message Label
        self.message_label = tk.Label(self.root, text="")
        self.message_label.pack()

        # Bind file drop event
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def browse_output_directory(self):
        core.browse_output_directory(self)

    def move_to_trash(self):
        core.move_to_trash(self)

    def load_last_used_file(self):
        core.load_last_used_file(self)

    def on_drop(self, event):
        core.on_drop(self, event)

    def add_to_queue(self, category):
        core.add_to_queue(self, category)

    def update_file_display(self):
        core.update_file_display(self)

    def undo_last(self):
        core.undo_last(self)

    def clear_selection(self):
        core.clear_selection(self)

    def add_category(self):
        core.add_category(self)

    def remove_category(self):
        core.remove_category(self)

    def refresh_category_buttons(self):
        core.refresh_category_buttons(self)

    def load_categories(self):
        core.load_categories(self)

    def save_categories(self):
        core.save_categories(self)

    def rename_files(self):
        core.rename_files(self)

    def handle_rename_success(self, new_path):
        core.handle_rename_success(self, new_path)

    def browse_file(self):
        core.browse_file(self)

    def construct_new_name(self, base_name, weighted_categories, custom_text, extension):
        # Construct the new name based on placement choice (prefix or suffix)
        if self.placement_choice.get() == "prefix":
            new_name = f"{custom_text} {base_name} {' '.join(weighted_categories)} {' '.join(self.queue)}"
        else:  # Default to suffix
            new_name = f"{base_name} {' '.join(weighted_categories)} {' '.join(self.queue)} {custom_text}"
        return new_name + extension

    def move_text(self, name):
        match = re.match(r"^(.*) - (.*?)__-__ (.*)\.(\w+)$", name)
        if match:
            prefix, moved_text, suffix, extension = match.groups()
            name = f"{prefix} {suffix} {moved_text}.{extension}"
        return name

    def sanitize_file_name(self, name):
        # Remove double spaces and trailing spaces
        return " ".join(name.split()).strip()

    def show_message(self, message, error=False):
        if error:
            self.message_label.config(text=message, fg="red")
        else:
            self.message_label.config(text=message, fg="black")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = OCDFileRenamer(root)
    root.mainloop()
