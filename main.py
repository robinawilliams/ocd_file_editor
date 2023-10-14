import os
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
import json
import send2trash  # Import the send2trash library


class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer")

        self.selected_file = ""
        self.queue = []

        self.create_gui()

        # Add the last used file tracking variable
        self.last_used_file = ""

        self.categories = self.load_categories()

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
            if col == 6:
                col = 0
                row += 1

        # Add Category Entry and Button
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()
        self.add_category_button = tk.Button(self.root, text="Add Category", command=self.add_category)
        self.add_category_button.pack()

        # Remove Category Entry and Button
        self.remove_category_entry = tk.Entry(self.root)
        self.remove_category_entry.pack()
        self.remove_category_button = tk.Button(self.root, text="Remove Category", command=self.remove_category)
        self.remove_category_button.pack()

        # Custom Text Entry Label
        self.custom_text_label = tk.Label(self.root, text="Custom text entry:")
        self.custom_text_label.pack()

        # Custom Text Entry
        self.custom_text_entry = tk.Entry(self.root)
        self.custom_text_entry.pack()

        # Rename Button
        self.rename_button = tk.Button(self.root, text="Rename Files", command=self.rename_files)
        self.rename_button.pack()

        # Undo Button
        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_last)
        self.undo_button.pack()

        # Clear Button
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_selection)
        self.clear_button.pack()

        # Message Label
        self.message_label = tk.Label(self.root, text="")
        self.message_label.pack()

        # DnD Label
        self.dnd_label = tk.Label(self.root, text="Drag and Drop files here:")
        self.dnd_label.pack()

        # Bind file drop event
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

        self.trash_button = tk.Button(self.root, text="Move to Trash", command=self.move_to_trash)
        self.trash_button.pack()

        # Last Used File Button
        self.last_used_file_button = tk.Button(self.root, text="Select Last Used File",
                                               command=self.load_last_used_file)
        self.last_used_file_button.pack()

    def move_to_trash(self):
        if self.selected_file:
            confirmation = tk.messagebox.askyesno("Confirm Action",
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
            self.file_display.config(text=self.selected_file)
            self.queue = []
            self.update_file_display()
            self.show_message("Last used file selected: " + self.selected_file)

    def on_drop(self, event):
        # Get the dropped file path without curly braces
        self.selected_file = event.data.strip('{}')
        self.file_display.config(text=self.selected_file)
        self.queue = []  # Clear the queue when a new file is selected
        self.update_file_display()
        self.show_message("File selected: " + self.selected_file)

    def add_to_queue(self, category):
        if self.selected_file:
            self.queue.append(category)
            self.update_file_display()
            self.show_message("Category added: " + category)

    def update_file_display(self):
        if self.selected_file:
            custom_text = self.custom_text_entry.get().strip()
            new_name = os.path.splitext(self.selected_file)[0] + " " + custom_text + " " + " ".join(self.queue) + \
                       os.path.splitext(self.selected_file)[1]
            self.file_display.config(text=new_name)

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
            if col == 6:
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
            new_name = os.path.splitext(self.selected_file)[0] + " " + custom_text + " " + " ".join(self.queue) + \
                       os.path.splitext(self.selected_file)[1]
            try:
                os.rename(self.selected_file, new_name)
                self.selected_file = ""
                self.queue = []
                self.file_display.config(text="")
                self.custom_text_entry.delete(0, tk.END)
                self.last_used_file = new_name  # Set the last used file
                self.show_message("File renamed successfully")
            except OSError as e:
                self.show_message("Error: " + str(e), error=True)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            self.file_display.config(text=self.selected_file)
            self.queue = []  # Clear the queue when a new file is selected
            self.update_file_display()
            self.show_message("File selected: " + self.selected_file)

    def show_message(self, message, error=False):
        if error:
            self.message_label.config(text=message, fg="red")
        else:
            self.message_label.config(text=message, fg="black")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
