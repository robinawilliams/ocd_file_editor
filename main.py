import os
import json
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
import send2trash
from tkinter import ttk
import re
import subprocess
import platform


class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer")

        self.selected_file = ""
        self.queue = []

        # Load categories from a configuration file
        self.categories = self.load_categories()

        # Initialize output directory
        self.output_directory = ""

        # Variable to track the user's placement choice (prefix or suffix)
        self.placement_choice = tk.StringVar()
        self.placement_choice.set("suffix")  # Default to suffix

        # Add a checkbox to enable/disable open on drop behavior
        self.open_on_drop_var = tk.BooleanVar(value=True)

        # Define weights for categories
        self.weights = {
            "Lo-fi": 1,
            "Acoustic": 2,
            "Tropical": 3,
        }

        # Variable to track whether to enable the text moving feature
        self.move_text_var = tk.BooleanVar()
        self.move_text_var.set(False)  # Default to disabled

        # Add a checkbox for moving the file up one folder
        self.move_up_var = tk.BooleanVar(value=False)

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

        self.categories = self.load_categories()  # Load categories from a configuration file
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

        # Inside the create_gui method, add the checkbox for duplicate removal
        self.remove_duplicates_var = tk.BooleanVar(value=False)
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
        output_directory = filedialog.askdirectory()
        if output_directory:
            self.output_directory = output_directory
            self.output_directory_entry.delete(0, tk.END)
            self.output_directory_entry.insert(0, self.output_directory)

    def move_to_trash(self):
        if self.selected_file:
            confirmation = messagebox.askyesno("Confirm Action",
                                               "Are you sure you want to move this file to the trash?")
            if confirmation:
                send2trash.send2trash(self.selected_file)
                self.selected_file = ""
                self.queue = []
                self.file_display.config(text="")
                self.custom_text_entry.delete(0, tk.END)
                self.show_message("File moved to trash successfully")

    def load_last_used_file(self):
        if self.last_used_file:
            self.selected_file = self.last_used_file
            self.file_display.config(text=os.path.basename(self.selected_file))
            self.queue = []
            self.update_file_display()
            self.show_message("Last used file selected: " + os.path.basename(self.selected_file))

    def on_drop(self, event):
        self.selected_file = event.data.strip('{}')
        self.file_display.config(text=os.path.basename(self.selected_file))  # Display only the filename
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
            self.show_message("Category added: " + category)

    def update_file_display(self):
        if self.selected_file:
            custom_text = self.custom_text_entry.get().strip()
            new_name = os.path.splitext(self.selected_file)[0] + " " + custom_text + " " + " ".join(self.queue) + \
                       os.path.splitext(self.selected_file)[1]

            # Remove double spaces and trailing spaces
            new_name = " ".join(new_name.split())  # Remove double spaces
            new_name = new_name.strip()  # Remove trailing spaces

            self.file_display.config(text=os.path.basename(new_name))

    def undo_last(self):
        if self.queue:
            self.queue.pop()
            self.update_file_display()
            self.show_message("Last category removed")

    def clear_selection(self):
        self.selected_file = ""
        self.queue = []
        self.file_display.config(text="")
        self.show_message("Selection cleared")

    def add_category(self):
        new_category = self.category_entry.get().strip()
        if new_category:
            self.categories.append(new_category)
            self.categories.sort()  # Sort the categories alphabetically
            self.save_categories()
            self.refresh_category_buttons()
            self.category_entry.delete(0, tk.END)
            self.show_message("Category added: " + new_category)

    def remove_category(self):
        category_to_remove = self.remove_category_entry.get().strip()
        if category_to_remove in self.categories:
            self.categories.remove(category_to_remove)
            self.save_categories()
            self.refresh_category_buttons()
            self.remove_category_entry.delete(0, tk.END)
            self.show_message("Category removed: " + category_to_remove)

    def refresh_category_buttons(self):
        for button in self.buttons:
            button.destroy()

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

    def load_categories(self):
        try:
            with open("categories.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_categories(self):
        with open("categories.json", "w") as file:
            json.dump(self.categories, file)

    def rename_files(self):
        if self.selected_file and (self.queue or self.custom_text_entry.get().strip()):
            custom_text = self.custom_text_entry.get().strip()
            base_name, extension = os.path.splitext(os.path.basename(self.selected_file))

            # Remove duplicate entries in the queue if the checkbox is selected
            if self.remove_duplicates_var.get():
                self.queue = list(dict.fromkeys(self.queue))

            weighted_categories = [category for category in self.queue if category in self.weights]

            # Sort weighted categories based on their weights
            weighted_categories.sort(key=lambda category: self.weights[category])

            # Construct the new name based on placement choice (prefix or suffix)
            if self.placement_choice.get() == "prefix":
                new_name = base_name
                for category in weighted_categories:
                    new_name = new_name + " " + category
                for category in self.queue:
                    if category not in weighted_categories:
                        new_name = new_name + " " + category
                new_name = custom_text + " " + new_name
            else:  # Default to suffix
                new_name = base_name
                for category in weighted_categories:
                    new_name = new_name + " " + category
                for category in self.queue:
                    if category not in weighted_categories:
                        new_name = new_name + " " + category
                new_name = new_name + " " + custom_text
                new_name = new_name.strip()

            new_name = new_name + extension

            if self.move_text_var.get():
                # Apply the feature if the checkbox is selected
                match = re.match(r"^(.*) - (.*?)__-__ (.*)\.(\w+)$", new_name)
                if match:
                    prefix, moved_text, suffix, extension = match.groups()
                    new_name = f"{prefix} {suffix} {moved_text}.{extension}"

            # Remove double spaces and trailing spaces
            new_name = " ".join(new_name.split())  # Remove double spaces
            new_name = new_name.strip()  # Remove trailing spaces

            # If the output directory is not explicitly set, use the file's current location
            if not self.output_directory:
                self.output_directory = os.path.dirname(self.selected_file)

            # Save the renamed file to the output directory
            new_path = os.path.join(self.output_directory, os.path.basename(new_name))
            try:
                os.rename(self.selected_file, new_path)
                self.selected_file = ""
                self.queue = []
                self.file_display.config(text="")
                self.custom_text_entry.delete(0, tk.END)
                self.last_used_file = new_path
                self.last_used_display.config(text=os.path.basename(new_path))
                self.show_message("File renamed and saved successfully")

                if self.move_up_var.get():
                    # Move the file up one folder
                    parent_directory = os.path.dirname(os.path.dirname(new_path))
                    new_location = os.path.join(parent_directory, os.path.basename(new_path))
                    os.rename(new_path, new_location)
                    self.selected_file = new_location
            except OSError as e:
                self.show_message("Error: " + str(e), error=True)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            self.file_display.config(text=self.selected_file)
            self.queue = []  # Clear the queue when a new file is selected
            self.update_file_display()
            self.show_message("File selected: " + os.path.basename(self.selected_file))

    def show_message(self, message, error=False):
        if error:
            self.message_label.config(text=message, fg="red")
        else:
            self.message_label.config(text=message, fg="black")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
