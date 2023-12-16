import customtkinter as ctk  # Customtkinter for a modern gui
from tkinterdnd2 import DND_FILES, TkinterDnD  # Drag-and-drop functionality
import core  # Main logic for the program


class OCDFileRenamer(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        # Call the __init__ method of the parent class (TkinterDnD) with the given arguments
        super().__init__(*args, **kwargs)

        # Determine TkinterDnD version and store it in the TkdndVersion attribute
        self.TkdndVersion = TkinterDnD._require(self)

        # Set the window title and geometry
        self.title("OCD File Renamer")

        # Initialize instance variables for selected file and queue
        self.selected_file = ""
        self.output_directory = ""
        self.queue = []

        # Initialize GUI elements (buttons, labels, frames, etc.)
        # Note: Some attributes are initialized as None and later assigned specific GUI elements
        # TODO Housekeeping
        self.browse_file_button = None
        self.custom_text_frame = None
        self.scaling_optionemenu = None
        self.message_label = None
        self.undo_button = None
        self.trash_button = None
        self.rename_button = None
        self.placement_label = None
        self.custom_text_label = None
        self.custom_text_entry = None
        self.output_directory_entry = None
        self.output_directory_browse_button = None
        self.remove_category_button = None
        self.remove_category_entry = None
        self.button_frame = None
        self.category_entry = None
        self.add_category_button = None
        self.file_display = None
        self.last_used_display = None
        self.last_used_display_label = None
        self.last_used_file_button = None
        self.last_used_file = None
        self.clear_button = None
        self.message_label_frame = None
        self.last_used_frame = None
        self.category_frame = None
        self.cat_top_frame = None
        self.settings_top_frame = None
        self.file_label = None
        self.coming_soon_label = None  # TODO Remove once add/remove categories window is running
        self.settings_frame = None
        self.settings_label = None
        self.scaling_label = None
        self.appearance_mode_menu = None
        self.appearance_mode_label = None
        self.button_group_frame = None
        self.folder_operations_frame = None
        self.home_top_frame = None
        self.home_scrollable_frame_window = None
        self.home_scrollable_frame = None
        self.home_scrollbar = None
        self.home_canvas = None
        self.home_frame = None
        self.settings_button = None
        self.add_remove_categories = None
        self.home_button = None
        self.navigation_frame_label = None
        self.navigation_frame = None
        self.open_on_file_drop_switch = None
        self.suffix_radio = None
        self.first_dash_radio = None
        self.prefix_radio = None
        self.placement_choice = None
        self.move_text_checkbox = None
        self.move_up_directory_checkbox = None
        self.suggest_output_directory_checkbox = None
        self.reset_output_directory_checkbox = None
        self.remove_duplicates_switch = None
        self.double_check_switch = None
        self.activate_logging_switch = None

        # Read settings from the configuration file and assign them to instance variables
        (move_text_var, initial_directory, artist_directory, double_check_directory, categories_file,
         geometry,
         reset_output_directory_var, suggest_output_directory_var, move_up_directory_var, open_on_file_drop_var,
         remove_duplicates_var,
         default_placement_var, double_check_var, activate_logging_var, ocd_file_renamer_log) = (
            self.load_configuration())

        # Set instance variables with the values from the configuration file
        self.initial_directory = initial_directory
        self.artist_directory = artist_directory
        self.double_check_directory = double_check_directory
        self.categories_file = categories_file
        self.geometry(geometry)
        self.move_text_var = ctk.BooleanVar(value=move_text_var)
        self.reset_output_directory_var = ctk.BooleanVar(value=reset_output_directory_var)
        self.suggest_output_directory_var = ctk.BooleanVar(value=suggest_output_directory_var)
        self.move_up_directory_var = ctk.BooleanVar(value=move_up_directory_var)
        self.open_on_file_drop_var = ctk.BooleanVar(value=open_on_file_drop_var)
        self.remove_duplicates_var = ctk.BooleanVar(value=remove_duplicates_var)
        self.double_check_var = ctk.BooleanVar(value=double_check_var)
        self.activate_logging_var = ctk.BooleanVar(value=activate_logging_var)
        self.default_placement_var = default_placement_var
        self.ocd_file_renamer_log = ocd_file_renamer_log

        # Enable drag-and-drop functionality for files
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_file_drop)

        # Create the GUI elements
        self.create_gui()

    def create_gui(self):
        # Set up grid layout with 1 row and 2 columns, configuring weights for resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        # Create label for the navigation frame
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="OCD \nFile \nRenamer",
                                                   compound="left",
                                                   font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=5, pady=5)

        # Create Home button with specific styling and command
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                         text="Home",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        # Create button for adding/removing categories with specific styling and command
        self.add_remove_categories = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                   border_spacing=10, text="Categories",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   anchor="w",
                                                   command=self.add_remove_categories_event)
        self.add_remove_categories.grid(row=2, column=0, sticky="ew")

        # Create Settings button with specific styling and command
        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                             text="Settings",
                                             fg_color="transparent", text_color=("gray10", "gray90"),
                                             hover_color=("gray70", "gray30"),
                                             anchor="w",
                                             command=self.settings_button_event)
        self.settings_button.grid(row=4, column=0, sticky="ew")

        """
        home_window
        """
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

        # Create a frame inside the canvas for scrollable content
        self.home_scrollable_frame = ctk.CTkFrame(self.home_canvas, corner_radius=0)
        self.home_scrollable_frame_window = self.home_canvas.create_window((0, 0), window=self.home_scrollable_frame,
                                                                           anchor="nw")

        # Bind canvas and frame for scrolling functionality
        self.home_canvas.bind('<Configure>', self.on_canvas_configure)
        self.home_scrollable_frame.bind('<Configure>', self.on_frame_configure)

        # Top frame in the home window
        self.home_top_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.home_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Browse file button
        self.browse_file_button = ctk.CTkButton(self.home_top_frame, text="Browse File",
                                                command=self.browse_file)
        self.browse_file_button.grid(row=0, column=0, padx=5, pady=5)

        # Selected File Display
        self.file_display = ctk.CTkLabel(self.home_top_frame, text="")
        self.file_display.grid(row=0, column=1, padx=5, pady=5)

        # Categories button frame
        self.button_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)

        # Initialize category buttons
        self.categories_buttons_initialize()

        # Frame for category-related elements
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

        # Frame to group custom text entry and output directory
        self.custom_text_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.custom_text_frame.grid(row=3, column=0, padx=10, pady=10)

        # Output Directory Browse Button
        self.output_directory_browse_button = ctk.CTkButton(self.custom_text_frame, text="Output Directory",
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

        # Frame to group miscellaneous buttons
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
        self.last_used_file_button = ctk.CTkButton(self.button_group_frame, text="Reload Last File",
                                                   command=self.load_last_used_file)
        self.last_used_file_button.grid(row=0, column=3, padx=10, pady=10)

        # Frame to display the last used file
        self.last_used_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.last_used_frame.grid(row=6, column=0, padx=5, pady=5)

        # Last Used File Label
        self.last_used_display_label = ctk.CTkLabel(self.last_used_frame, text="Last used file:")
        self.last_used_display_label.grid(row=0, column=0, padx=5, pady=5)

        # Last Used File Display
        self.last_used_display = ctk.CTkLabel(self.last_used_frame, text="")
        self.last_used_display.grid(row=0, column=1, padx=5, pady=5)

        # Frame to display messages
        self.message_label_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.message_label_frame.grid(row=7, column=0, padx=10, pady=10)

        # Message Label
        self.message_label = ctk.CTkLabel(self.message_label_frame, text="")
        self.message_label.grid(row=0, column=0, padx=10, pady=10)

        # Frame to group folder operations
        self.folder_operations_frame = ctk.CTkFrame(self.home_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.folder_operations_frame.grid(row=8, column=0, padx=10, pady=10)

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

        # "Move Text" checkbox with the initial state
        self.move_text_checkbox = ctk.CTkCheckBox(self.folder_operations_frame, text="Move Text",
                                                  variable=self.move_text_var,
                                                  onvalue=True, offvalue=False)
        self.move_text_checkbox.grid(row=0, column=3, padx=5, pady=5)

        # Variable to track the user's placement choice (prefix, suffix, or first_dash)
        self.placement_choice = ctk.StringVar()
        self.placement_choice.set(self.default_placement_var)  # Default to first_dash

        # Placement Label
        self.placement_label = ctk.CTkLabel(self.folder_operations_frame, text="Placement:")
        self.placement_label.grid(row=0, column=4, padx=5, pady=5)

        # Radio button for prefix
        self.prefix_radio = ctk.CTkRadioButton(self.folder_operations_frame, text="Prefix",
                                               variable=self.placement_choice,
                                               value="prefix")
        self.prefix_radio.grid(row=0, column=5, padx=5, pady=5)

        # Radio button for first_dash
        self.first_dash_radio = ctk.CTkRadioButton(self.folder_operations_frame, text="First Dash",
                                                   variable=self.placement_choice,
                                                   value="first_dash")
        self.first_dash_radio.grid(row=0, column=6, padx=5, pady=5)

        # Radio button for suffix
        self.suffix_radio = ctk.CTkRadioButton(self.folder_operations_frame, text="Suffix",
                                               variable=self.placement_choice,
                                               value="suffix")
        self.suffix_radio.grid(row=0, column=7, padx=5, pady=5)

        """
        category_window
        """
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

        self.coming_soon_label = ctk.CTkLabel(self.cat_top_frame, text="Coming Soon",
                                              font=ctk.CTkFont(size=15, weight="bold"))
        self.coming_soon_label.grid(row=1, column=0, padx=5, pady=5)

        """
        settings_window
        """
        # Create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # Top frame
        self.settings_top_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.settings_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Settings label
        self.settings_label = ctk.CTkLabel(self.settings_top_frame, text="Settings",
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.settings_label.grid(row=0, column=0, padx=5, pady=5, columnspan=5)

        # Checkbox to enable/disable open on drop behavior
        self.open_on_file_drop_switch = ctk.CTkSwitch(self.settings_top_frame, text="Open File on Drag and Drop",
                                                      variable=self.open_on_file_drop_var)
        self.open_on_file_drop_switch.grid(row=1, column=0, padx=10, pady=10)

        # Checkbox to enable/disable duplicate removal
        self.remove_duplicates_switch = ctk.CTkSwitch(self.settings_top_frame,
                                                      text="Remove Duplicates",
                                                      variable=self.remove_duplicates_var)
        self.remove_duplicates_switch.grid(row=1, column=1, padx=10, pady=10)

        # "Double check" checkbox with the initial state
        self.double_check_switch = ctk.CTkSwitch(self.settings_top_frame, text="Create Double Check Reminder",
                                                 variable=self.double_check_var)
        self.double_check_switch.grid(row=1, column=2, padx=10, pady=10)

        # "Activate Logging" checkbox with the initial state
        self.activate_logging_switch = ctk.CTkSwitch(self.settings_top_frame, text="Activate Logging",
                                                     variable=self.activate_logging_var)
        self.activate_logging_switch.grid(row=1, column=3, padx=10, pady=10)

        # Bind the callback function to the variable
        self.activate_logging_var.trace_add("write", self.handle_logging_activation)

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

        # Set default value for scaling
        self.scaling_optionemenu.set("100%")

        """
        Misc
        """
        # Select default frame
        self.select_frame_by_name("home")

    # Callback for updating the scroll region when the inner frame is configured
    def on_frame_configure(self, event=None):
        # Reset the scroll region to encompass the inner frame
        self.home_canvas.configure(scrollregion=self.home_canvas.bbox("all"))

    # Callback for updating the scrollable frame's width when the canvas is configured
    def on_canvas_configure(self, event):
        # Set the scrollable frame's width to match the canvas
        canvas_width = event.width - self.home_scrollbar.winfo_width()
        self.home_canvas.itemconfig(self.home_scrollable_frame_window, width=canvas_width)

    # Callback function to handle logging state
    def handle_logging_activation(self, *args):
        # If logging is true, call the logging_setup function
        if self.activate_logging_var.get():
            try:
                self.logging_setup()
            except OSError as e:
                print(f"Logging failed. Error: {e}")

    # Method to dynamically switch between frames based on the selected name
    def select_frame_by_name(self, name):
        # Set button color for the selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.add_remove_categories.configure(
            fg_color=("gray75", "gray25") if name == "add_remove_categories" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")

        # Show the selected frame and hide others
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

    """
    Event handlers for button clicks to switch frames
    """

    def home_button_event(self):
        self.select_frame_by_name("home")

    def add_remove_categories_event(self):
        self.select_frame_by_name("add_remove_categories")

    def settings_button_event(self):
        self.select_frame_by_name("settings")

    # Static methods for changing appearance mode and UI scaling
    @staticmethod
    def change_appearance_mode_event(new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    # Method to display messages with optional error formatting
    def show_message(self, message, error=False):
        if error:
            self.message_label.configure(text=message, text_color="red")
        else:
            self.message_label.configure(text=message, text_color="white")

    """
    Configuration
    """

    @staticmethod
    def load_configuration():
        # Load configuration settings using the core module
        return core.load_configuration()

    def logging_setup(self):
        # Setup logging
        core.logging_setup(self)

    """
    File Operations
    """

    def move_file_to_trash(self):
        # Move the selected file to the trash
        core.move_file_to_trash(self)

    def load_last_used_file(self):
        # Load the last used file and update the GUI
        core.load_last_used_file(self)

    def on_file_drop(self, event):
        # Handle the event when a file is dropped onto the application
        core.on_file_drop(self, event)

    def add_to_queue(self, category):
        # Add a category to the processing queue
        core.add_to_queue(self, category)

    def update_file_display(self):
        # Update the display with the currently selected file
        core.update_file_display(self)

    def undo_last(self):
        # Undo the last operation and update the GUI
        core.undo_last(self)

    def clear_selection(self):
        # Clear the selected file and update the GUI
        core.clear_selection(self)

    def browse_file(self):
        # Open a file dialog to browse and select a file
        core.browse_file(self)

    def browse_output_directory(self):
        # Open a dialog to browse and select an output directory
        core.browse_output_directory(self)

    def handle_rename_success(self, new_path):
        # Handle the success of the file renaming process
        core.handle_rename_success(self, new_path)

    """
    Category Management
    """

    def add_category(self):
        # Add a new category to the list and update the GUI
        core.add_category(self)

    def remove_category(self):
        # Remove a category from the list and update the GUI
        core.remove_category(self)

    def categories_buttons_initialize(self):
        # Initialize category-related buttons in the GUI
        core.categories_buttons_initialize(self)

    def refresh_category_buttons(self, sorted_categories=None):
        # Refresh the category buttons in the GUI
        core.refresh_category_buttons(self)

    def save_categories(self):
        # Save the current list of categories to the configuration
        core.save_categories(self)

    """
    File Renaming
    """

    def rename_files(self):
        # Rename the selected file(s) using the specified options and update the GUI
        core.rename_files(self)

    def construct_new_name(self, base_name, weighted_categories, custom_text, extension):
        # Construct a new file name based on provided parameters
        return core.construct_new_name(self, base_name, weighted_categories, custom_text, extension)

    @staticmethod
    def move_text(name):
        # Move text within a name according to specified rules
        return core.move_text(name)


if __name__ == "__main__":
    # Create an instance of the OCDFileRenamer application and start the main loop
    app = OCDFileRenamer()
    app.mainloop()
