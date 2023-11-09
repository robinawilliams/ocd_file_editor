import os
from tkinterdnd2 import DND_FILES, TkinterDnD
import core
import customtkinter as ctk
from PIL import Image


class OCDFileRenamer(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

        self.title("OCD File Renamer")
        self.geometry(f"{1280}x{750}")

        self.selected_file = ""
        self.queue = []

        # Define weights for categories
        self.weights = {
            "Lo-fi": 1,
            "Acoustic": 2,
            "Tropical": 3,
        }

        # Initialize output directory
        self.output_directory = ""

        # Drag and drop
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_file_drop)

        self.create_gui()

    def create_gui(self):
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                       size=(26, 26))
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")),
                                             size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                             size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                       dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                       size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                       dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                       size=(20, 20))
        self.add_user_image = ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="OCD File Renamer",
                                                   compound="left",
                                                   font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="Home",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.add_remove_categories = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                   border_spacing=10, text="Categories",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.chat_image, anchor="w",
                                                   command=self.add_remove_categories_event)
        self.add_remove_categories.grid(row=2, column=0, sticky="ew")

        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                             text="Settings",
                                             fg_color="transparent", text_color=("gray10", "gray90"),
                                             hover_color=("gray70", "gray30"),
                                             image=self.add_user_image, anchor="w",
                                             command=self.settings_button_event)
        self.settings_button.grid(row=4, column=0, sticky="ew")

        # home_window ###
        # Create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=1)

        # Create a canvas and a scrollbar
        # TODO Include logic to adjust the background (bg) color depending on what mode is selected.
        self.home_canvas = ctk.CTkCanvas(self.home_frame, bg='#2B2B2B', highlightthickness=0)
        self.home_scrollbar = ctk.CTkScrollbar(self.home_frame, command=self.home_canvas.yview)
        self.home_canvas.configure(yscrollcommand=self.home_scrollbar.set)

        # Place the canvas and the scrollbar in the grid
        self.home_canvas.grid(row=0, column=0, sticky="nsew")
        self.home_scrollbar.grid(row=0, column=1, sticky="ns")

        # Create a frame inside the canvas which will be scrolled
        self.home_scrollable_frame = ctk.CTkFrame(self.home_canvas, corner_radius=0)
        self.home_scrollable_frame_window = self.home_canvas.create_window((0, 0), window=self.home_scrollable_frame,
                                                                           anchor="nw")

        # Bind the canvas and frame to configure scroll region and canvas scrolling
        self.home_canvas.bind('<Configure>', self.on_canvas_configure)
        self.home_scrollable_frame.bind('<Configure>', self.on_frame_configure)

        # Top frame
        self.home_top_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.home_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Browse Button
        self.browse_button = ctk.CTkButton(self.home_top_frame, text="Browse", image=self.image_icon_image,
                                           command=self.browse_file)
        self.browse_button.grid(row=0, column=0, padx=5, pady=5)

        # Selected File Display
        self.file_display = ctk.CTkLabel(self.home_top_frame, text="")
        self.file_display.grid(row=0, column=1, padx=5, pady=5)

        # Categories button frame
        self.button_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)

        self.categories_buttons_initialize()

        # Create a frame for the category-related elements
        self.category_frame = ctk.CTkFrame(self.home_scrollable_frame)
        self.category_frame.grid(row=2, column=0, padx=10, pady=10)

        # Add Category Button
        self.add_category_button = ctk.CTkButton(self.category_frame, text="Add Category", command=self.add_category)
        self.add_category_button.grid(row=0, column=0, padx=5)

        # Add Category Entry
        self.category_entry = ctk.CTkEntry(self.category_frame, width=250)
        self.category_entry.grid(row=0, column=1, padx=5)

        # Remove Category Button
        self.remove_category_button = ctk.CTkButton(self.category_frame, text="Remove Category",
                                                    command=self.remove_category)
        self.remove_category_button.grid(row=0, column=2, padx=5)

        # Remove Category Entry
        self.remove_category_entry = ctk.CTkEntry(self.category_frame, width=250)
        self.remove_category_entry.grid(row=0, column=3, padx=5)

        # Create a frame to group the custom text entry and output directory
        self.custom_text_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.custom_text_frame.grid(row=3, column=0, padx=10, pady=10)

        # Output Directory Browse Button
        self.output_directory_browse_button = ctk.CTkButton(self.custom_text_frame, text="Output Directory",
                                                            image=self.image_icon_image,
                                                            command=self.browse_output_directory)
        self.output_directory_browse_button.grid(row=0, column=0, padx=5, pady=5)

        # Output Directory Entry
        self.output_directory_entry = ctk.CTkEntry(self.custom_text_frame, width=150)
        self.output_directory_entry.grid(row=0, column=1, padx=5, pady=5)

        # Custom Text Entry Label
        self.custom_text_label = ctk.CTkLabel(self.custom_text_frame, text="Custom text entry: ")
        self.custom_text_label.grid(row=0, column=2, padx=5, pady=5)

        # Custom Text Entry
        self.custom_text_entry = ctk.CTkEntry(self.custom_text_frame, width=350)
        self.custom_text_entry.grid(row=0, column=3, padx=10, pady=10)

        # Rename File Button
        self.rename_button = ctk.CTkButton(self.custom_text_frame, text="Rename File",
                                           command=self.rename_files)
        self.rename_button.grid(row=0, column=4, padx=5, pady=5)

        # Create a frame to group the folder operations frame
        self.folder_operations_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.folder_operations_frame.grid(row=8, column=0, padx=10, pady=10)

        # Placement Label
        self.placement_label = ctk.CTkLabel(self.folder_operations_frame, text="Placement:")
        self.placement_label.grid(row=0, column=3, padx=10, pady=5)

        # Variable to track the user's placement choice (prefix or suffix)
        self.placement_choice = ctk.StringVar()
        self.placement_choice.set("suffix")  # Default to suffix

        # Radio button for prefix
        self.prefix_radio = ctk.CTkRadioButton(self.folder_operations_frame, text="Prefix",
                                               variable=self.placement_choice,
                                               value="prefix")
        self.prefix_radio.grid(row=0, column=4, padx=5, pady=5)

        # Radio button for suffix
        self.suffix_radio = ctk.CTkRadioButton(self.folder_operations_frame, text="Suffix",
                                               variable=self.placement_choice,
                                               value="suffix")
        self.suffix_radio.grid(row=0, column=5, padx=5, pady=5)

        # Create a frame to group the misc. buttons
        self.button_group_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.button_group_frame.grid(row=4, column=0, padx=10, pady=10)

        # Undo Button
        self.undo_button = ctk.CTkButton(self.button_group_frame, text="Undo", command=self.undo_last)
        self.undo_button.grid(row=0, column=0, padx=10, pady=10)

        # Clear Button
        self.clear_button = ctk.CTkButton(self.button_group_frame, text="Clear", command=self.clear_selection)
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)

        # Move to Trash Button
        self.trash_button = ctk.CTkButton(self.button_group_frame, text="Move to Trash",
                                          command=self.move_file_to_trash)
        self.trash_button.grid(row=0, column=2, padx=10, pady=10)

        # Select Last Used File Button
        self.last_used_file_button = ctk.CTkButton(self.button_group_frame, text="Select Last Used File",
                                                   command=self.load_last_used_file)
        self.last_used_file_button.grid(row=0, column=3, padx=10, pady=10)

        # Create a frame to display the last used file
        self.last_used_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.last_used_frame.grid(row=6, column=0, padx=5, pady=5)

        # Last Used File Label
        self.last_used_display_label = ctk.CTkLabel(self.last_used_frame, text="Last used file:")
        self.last_used_display_label.grid(row=0, column=0, padx=5, pady=5)

        # Last Used File Display
        self.last_used_display = ctk.CTkLabel(self.last_used_frame, text="")
        self.last_used_display.grid(row=0, column=1, padx=5, pady=5)

        # Create a frame to display messages
        self.message_label_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.message_label_frame.grid(row=7, column=0, padx=10, pady=10)

        # Message Label
        self.message_label = ctk.CTkLabel(self.message_label_frame, text="")
        self.message_label.grid(row=0, column=0, padx=10, pady=10)

        # category_window ###
        # Create add/remove categories frame
        self.category_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.category_frame.grid_columnconfigure(0, weight=1)

        # Top frame
        self.cat_top_frame = ctk.CTkFrame(self.category_frame, corner_radius=0, fg_color="transparent")
        self.cat_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Add/Remove Categories Label
        self.file_label = ctk.CTkLabel(self.cat_top_frame, text="Add/Remove Categories",
                                       font=ctk.CTkFont(size=15, weight="bold"))
        self.file_label.grid(row=0, column=0, padx=5, pady=5)

        # TODO work on fix
        # # Categories button frame
        # self.button_frame = ctk.CTkFrame(self.cat_top_frame, corner_radius=0, fg_color="transparent")
        # self.button_frame.grid(row=1, column=0, padx=10, pady=10)

        # self.categories_buttons_initialize()
        #
        # # Cat frame
        # self.cat_frame = ctk.CTkFrame(self.cat_top_frame, corner_radius=0, fg_color="transparent")
        # self.cat_frame.grid(row=2, column=0, padx=10, pady=10)

        # # Add Category Entry
        # self.category_entry = ctk.CTkEntry(self.cat_frame, width=705)
        # self.category_entry.grid(row=0, column=0, padx=20, pady=10)
        #
        # # Add Category Button
        # self.add_category_button = ctk.CTkButton(self.cat_frame, text="Add Category",
        #                                          command=self.add_category)
        # self.add_category_button.grid(row=0, column=1, padx=20, pady=10)
        #
        # # Remove Category Entry
        # self.remove_category_entry = ctk.CTkEntry(self.cat_frame, width=705)
        # self.remove_category_entry.grid(row=1, column=0, padx=20, pady=10)
        #
        # # Remove Category Button
        # self.remove_category_button = ctk.CTkButton(self.cat_frame, text="Remove Category",
        #                                             command=self.remove_category)
        # self.remove_category_button.grid(row=1, column=1, padx=20, pady=10)

        # # Create a frame to display messages
        # self.message_label_frame = ctk.CTkFrame(self.cat_frame, corner_radius=0, fg_color="transparent")
        # self.message_label_frame.grid(row=3, column=0, padx=10, pady=10)
        #
        # # Message Label
        # self.message_label = ctk.CTkLabel(self.message_label_frame, text="")
        # self.message_label.grid(row=0, column=0, padx=10, pady=10)

        # settings_window ###
        # Create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # Top frame
        self.settings_top_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.settings_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Settings label
        self.settings_label = ctk.CTkLabel(self.settings_top_frame, text="Settings",
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.settings_label.grid(row=0, column=0, padx=5, pady=5)

        # Select light or dark label
        self.appearance_mode_label = ctk.CTkLabel(self.settings_top_frame, text="Appearance:")
        self.appearance_mode_label.grid(row=2, column=0, padx=10, pady=10)

        # Select light or dark mode
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.settings_top_frame,
                                                      values=["Light", "Dark", "System"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=2, column=1, padx=10, pady=10)

        # Select scaling label
        self.scaling_label = ctk.CTkLabel(self.settings_top_frame, text="UI Scaling:")
        self.scaling_label.grid(row=3, column=0, padx=10, pady=10)

        # Select scaling level
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.settings_top_frame,
                                                     values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=3, column=1, padx=10, pady=10)

        # Misc ###
        # Set default value for scaling
        self.scaling_optionemenu.set("100%")

        # Select default frame
        self.select_frame_by_name("home")

    def on_frame_configure(self, event=None):
        # Reset the scroll region to encompass the inner frame
        self.home_canvas.configure(scrollregion=self.home_canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Set the scrollable frame's width to match the canvas
        canvas_width = event.width - self.home_scrollbar.winfo_width()
        self.home_canvas.itemconfig(self.home_scrollable_frame_window, width=canvas_width)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.add_remove_categories.configure(
            fg_color=("gray75", "gray25") if name == "add_remove_categories" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "add_remove_categories":
            self.category_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.category_frame.grid_forget()
        if name == "settings":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def add_remove_categories_event(self):
        self.select_frame_by_name("add_remove_categories")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def show_message(self, message, error=False):
        if error:
            self.message_label.configure(text=message, text_color="red")
        else:
            self.message_label.configure(text=message, text_color="white")

    # Configuration and Initialization ###
    def load_configuration(self):
        return core.load_configuration()

    # FileOperations ###
    def move_file_to_trash(self):
        core.move_file_to_trash(self)

    def load_last_used_file(self):
        core.load_last_used_file(self)

    def on_file_drop(self, event):
        core.on_file_drop(self, event)

    def add_to_queue(self, category):
        core.add_to_queue(self, category)

    def update_file_display(self):
        core.update_file_display(self)

    def undo_last(self):
        core.undo_last(self)

    def clear_selection(self):
        core.clear_selection(self)

    def browse_file(self):
        core.browse_file(self)

    def browse_output_directory(self):
        core.browse_output_directory(self)

    def handle_rename_success(self, new_path):
        core.handle_rename_success(self, new_path)

    # CategoryManagement ###
    def add_category(self):
        core.add_category(self)

    def remove_category(self):
        core.remove_category(self)

    def categories_buttons_initialize(self):
        core.categories_buttons_initialize(self)

    def refresh_category_buttons(self):
        core.refresh_category_buttons(self)

    def save_categories(self):
        core.save_categories(self)

    # File Renaming ###
    def rename_files(self):
        core.rename_files(self)

    def construct_new_name(self, base_name, weighted_categories, custom_text, extension):
        return core.construct_new_name(self, base_name, weighted_categories, custom_text, extension)

    def move_text(self, name):
        return core.move_text(name)

    def sanitize_file_name(self, name):
        return core.sanitize_file_name(name)


if __name__ == "__main__":
    app = OCDFileRenamer()

    # Read settings from the configuration file
    move_text_var, initial_directory, categories_file, geometry, reset_output_directory_var, move_up_var, \
        open_on_file_drop_var, remove_duplicates_var = app.load_configuration()

    app.move_text_var = move_text_var  # Set the move_text_var attribute
    app.initial_directory = initial_directory  # Set the initial_directory attribute
    app.categories_file = categories_file  # Set the categories_file attribute
    app.geometry(geometry)
    app.reset_output_directory_var = reset_output_directory_var
    app.move_up_var = move_up_var
    app.open_on_file_drop_var = open_on_file_drop_var
    app.remove_duplicates_var = remove_duplicates_var

    # TODO Housekeeping
    # Create the "Move Text" checkbox with the initial state
    app.move_text_var = ctk.BooleanVar(value=move_text_var)
    app.move_text_checkbox = ctk.CTkCheckBox(app.folder_operations_frame, text="Move Text",
                                             variable=app.move_text_var,
                                             onvalue=True, offvalue=False)
    app.move_text_checkbox.grid(row=0, column=2, padx=5, pady=5)

    # Checkbox to enable/disable resetting the Output Directory
    app.reset_output_directory_var = ctk.BooleanVar(value=reset_output_directory_var)  # Default not to reset
    app.reset_output_directory_checkbox = ctk.CTkCheckBox(app.folder_operations_frame,
                                                          text="Reset Output Directory",
                                                          variable=app.reset_output_directory_var)
    app.reset_output_directory_checkbox.grid(row=0, column=0, padx=10, pady=10)

    # Checkbox to enable/disable moving the file up one folder
    app.move_up_var = ctk.BooleanVar(value=move_up_var)
    app.move_up_checkbox = ctk.CTkCheckBox(app.folder_operations_frame, text="Move Up One Folder",
                                           variable=app.move_up_var)
    app.move_up_checkbox.grid(row=0, column=1, padx=5, pady=5)

    # Checkbox to enable/disable open on drop behavior
    app.open_on_file_drop_var = ctk.BooleanVar(value=open_on_file_drop_var)
    app.open_on_file_drop_switch = ctk.CTkSwitch(app.settings_top_frame, text="Open File on Drag and Drop",
                                            variable=app.open_on_file_drop_var)
    app.open_on_file_drop_switch.grid(row=1, column=0, padx=10, pady=10)

    # Checkbox to enable/disable for duplicate removal
    app.remove_duplicates_var = ctk.BooleanVar(value=remove_duplicates_var)
    app.remove_duplicates_switch = ctk.CTkSwitch(app.settings_top_frame,
                                                 text="Remove Duplicates",
                                                 variable=app.remove_duplicates_var)
    app.remove_duplicates_switch.grid(row=1, column=1, padx=10, pady=10)


    app.mainloop()
