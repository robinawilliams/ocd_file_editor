import customtkinter as ctk  # Customtkinter for a modern gui
from tkinterdnd2 import DND_FILES, TkinterDnD  # Drag-and-drop functionality
import sys  # Handling standard error and output redirects
import atexit  # Module for registering functions to be called when the program is closing
import logging  # Logging module for capturing log messages
from tkinter import messagebox  # Tkinter module for GUI message boxes
import core  # Main logic for the program


class OCDFileRenamer(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        # Call the __init__ method of the parent class (TkinterDnD) with the given arguments
        super().__init__(*args, **kwargs)

        # Determine TkinterDnD version and store it in the TkdndVersion attribute
        # noinspection PyProtectedMember
        self.TkdndVersion = TkinterDnD._require(self)

        # Set the window title
        self.title("O.C.D. File Editor")

        # Initialize instance variables for selected files, output directories, queue, and last used files
        self.file_renamer_selected_file = ""
        self.file_renamer_last_used_file = ""
        self.output_directory = ""
        self.queue = []
        self.name_normalizer_selected_file = ""
        self.name_normalizer_last_used_file = ""
        self.name_normalizer_output_directory = ""
        self.video_editor_selected_file = ""
        self.video_editor_last_used_file = ""
        self.video_editor_output_directory = ""
        self.add_artist = ""
        self.remove_artist = ""
        self.no_go_name = ""

        # Initialize the standard output and error variables (Fix for MoviePy overriding user's logging choice)
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # Initialize configuration file variable
        self.config_file_path = ""

        # Initialize Main GUI elements
        # TODO Housekeeping Note: Some attributes are initialized as None and later assigned specific GUI elements
        self.navigation_frame = None
        self.navigation_frame_label = None
        self.file_renamer_button = None
        self.name_normalizer_button = None
        self.video_editor_button = None
        self.add_remove_button = None
        self.settings_button = None

        # Initialize OCD File Renamer GUI elements
        self.file_renamer_frame = None
        self.file_renamer_canvas = None
        self.file_renamer_scrollbar = None
        self.file_renamer_scrollable_frame = None
        self.file_renamer_scrollable_frame_window = None
        self.file_renamer_top_frame = None
        self.browse_file_button = None
        self.file_display_text = None
        self.file_display_entry = None
        self.button_frame = None
        self.category_frame = None
        self.add_category_button = None
        self.category_entry = None
        self.weight_label = None
        self.weight_var = None
        self.weight_entry = None
        self.remove_category_button = None
        self.remove_category_entry = None
        self.no_go_label_frame = None
        self.no_go_label = None
        self.no_go_entry_frame = None
        self.add_no_go_button = None
        self.add_no_go_name_entry = None
        self.custom_text_frame = None
        self.output_directory_browse_button = None
        self.output_directory_entry = None
        self.custom_text_entry = None
        self.rename_button = None
        self.button_group_frame = None
        self.undo_button = None
        self.clear_button = None
        self.trash_button = None
        self.file_renamer_last_used_file_button = None
        self.last_used_frame = None
        self.last_used_display_label = None
        self.last_used_display = None
        self.file_renamer_message_label_frame = None
        self.file_renamer_message_label = None
        self.folder_operations_frame = None
        self.reset_output_directory_checkbox = None
        self.suggest_output_directory_checkbox = None
        self.move_up_directory_checkbox = None
        self.move_text_checkbox = None
        self.send_to_module_frame = None
        self.send_to_video_editor_button = None
        self.send_to_name_normalizer_button = None
        self.placement_frame = None
        self.placement_label = None
        self.placement_choice = None
        self.prefix_radio = None
        self.special_character_radio = None
        self.suffix_radio = None

        # Initialize Name Normalizer GUI elements
        self.name_normalizer_frame = None
        self.name_normalizer_top_frame = None
        self.name_normalizer_label = None
        self.checkbox_frame1 = None
        self.nn_browse_button = None
        self.nn_path_entry = None
        self.tail_checkbox = None
        self.remove_all_symbols_checkbox = None
        self.remove_most_symbols_checkbox = None
        self.remove_numbers_checkbox = None
        self.checkbox_frame2 = None
        self.remove_new_checkbox = None
        self.remove_dash_checkbox = None
        self.remove_endash_checkbox = None
        self.remove_emdash_checkbox = None
        self.remove_hashtag_checkbox = None
        self.checkbox_frame3 = None
        self.remove_ampersand_checkbox = None
        self.remove_at_checkbox = None
        self.remove_underscore_checkbox = None
        self.remove_comma_checkbox = None
        self.remove_dollar_checkbox = None
        self.checkbox_frame4 = None
        self.title_checkbox = None
        self.remove_single_quote_checkbox = None
        self.remove_double_quote_checkbox = None
        self.remove_colon_checkbox = None
        self.remove_semicolon_checkbox = None
        self.remove_percent_checkbox = None
        self.remove_caret_checkbox = None
        self.checkbox_frame5 = None
        self.remove_asterisk_checkbox = None
        self.remove_parenthesis_checkbox = None
        self.remove_plus_checkbox = None
        self.remove_equal_checkbox = None
        self.remove_curly_brace_checkbox = None
        self.remove_square_bracket_checkbox = None
        self.checkbox_frame6 = None
        self.remove_pipe_checkbox = None
        self.remove_backslash_checkbox = None
        self.remove_angle_bracket_checkbox = None
        self.remove_question_mark_checkbox = None
        self.checkbox_frame7 = None
        self.remove_parenthesis_trail_checkbox = None
        self.remove_hashtag_trail_checkbox = None
        self.checkbox_frame8 = None
        self.remove_double_space_checkbox = None
        self.artist_search_checkbox = None
        self.deep_walk_checkbox = None
        self.reset_checkbox = None
        self.output_directory_frame = None
        self.browse_move_directory_button = None
        self.move_directory_entry = None
        self.normalize_folder_frame = None
        self.normalize_preview_button = None
        self.normalize_button = None
        self.send_to_module_frame1 = None
        self.send_to_file_renamer_button1 = None
        self.send_to_video_editor_button1 = None
        self.clear_name_normalizer_selection_button = None
        self.name_normalizer_last_used_file_button = None
        self.name_normalizer_message_label_frame = None
        self.name_normalizer_message_label = None

        # Initialize Video Editor GUI elements
        self.video_editor_frame = None
        self.video_editor_top_frame = None
        self.video_editor_label = None
        self.browse_input_method_button = None
        self.input_method_entry = None
        self.rotation_frame = None
        self.rotation_label = None
        self.rotation_var = None
        self.left_radio = None
        self.right_radio = None
        self.flip_radio = None
        self.no_rotation_radio = None
        self.decibel_frame = None
        self.decibel_label = None
        self.decibel_var = None
        self.decibel_entry = None
        self.audio_normalization_frame = None
        self.audio_normalization_label = None
        self.audio_normalization_var = None
        self.audio_normalization_entry = None
        self.trim_frame = None
        self.trim_label = None
        self.minute_var = None
        self.minute_entry = None
        self.colon_label = None
        self.second_var = None
        self.second_entry = None
        self.video_editor_output_directory_frame = None
        self.browse_video_editor_output_directory_button = None
        self.video_editor_output_directory_entry = None
        self.process_video_editor_frame = None
        self.clear_video_editor_selection_button = None
        self.video_editor_last_used_file_button = None
        self.process_video_edits_button = None
        self.video_editor_checkbox_frame = None
        self.remove_successful_lines_checkbox = None
        self.reset_video_checkbox = None
        self.video_editor_message_label_frame = None
        self.video_editor_message_label = None
        self.send_to_module_frame2 = None
        self.send_to_file_renamer_button = None
        self.send_to_name_normalizer_button1 = None

        # Initialize Add/Remove GUI elements
        self.add_remove_frame = None
        self.add_remove_top_frame = None
        self.artist_label = None
        self.add_remove_artist_entry_frame = None
        self.add_artist_entry = None
        self.add_artist_button = None
        self.remove_artist_entry = None
        self.remove_artist_button = None
        self.clear_artist_frame = None
        self.clear_artist_button = None
        self.reset_artist_frame = None
        self.reset_artist_checkbox = None
        self.category_label_frame = None
        self.category_label = None
        self.add_remove_label_frame = None
        self.add_remove_label = None

        # Initialize Settings GUI elements
        self.settings_frame = None
        self.settings_top_frame = None
        self.settings_label = None
        self.switch_frame = None
        self.open_on_file_drop_switch = None
        self.remove_duplicates_switch = None
        self.double_check_switch = None
        self.activate_logging_switch = None
        self.suppress_switch = None
        self.show_messageboxes_switch = None
        self.confirmation_frame = None
        self.show_confirmation_messageboxes_switch = None
        self.fallback_confirmation_label = None
        self.true_radio = None
        self.false_radio = None
        self.gui_settings_frame = None
        self.appearance_mode_label = None
        self.appearance_mode_menu = None
        self.scaling_label = None
        self.scaling_optionemenu = None
        self.master_entry_frame = None
        self.initial_directory_frame = None
        self.browse_initial_directory_button = None
        self.initial_directory_entry = None
        self.browse_initial_output_directory_button = None
        self.initial_output_directory_entry = None
        self.double_check_reminder_directory_frame = None
        self.browse_double_check_reminder_directory_button = None
        self.double_check_reminder_directory_entry = None
        self.browse_no_go_reminder_directory_button = None
        self.no_go_reminder_directory_entry = None
        self.artist_directory_frame = None
        self.browse_artist_directory_button = None
        self.artist_directory_entry = None
        self.browse_artist_file_button = None
        self.artist_file_entry = None
        self.configuration_file_frame = None
        self.open_configuration_file_button = None
        self.configuration_file_entry = None
        self.open_log_file_button = None
        self.log_file_entry = None

        # Read settings from the configuration file and assign them to instance variables
        (move_text_var, initial_directory, artist_directory, double_check_directory, categories_file,
         geometry, reset_output_directory_var, suggest_output_directory_var, move_up_directory_var,
         open_on_file_drop_var, remove_duplicates_var, default_placement_var, special_character_var,
         double_check_var, activate_logging_var, file_renamer_log, column_numbers, default_weight,
         file_extensions, remove_all_symbols_var, tail_var, remove_parenthesis_trail_var,
         remove_hashtag_trail_var, remove_new_var, remove_dash_var, remove_endash_var, remove_emdash_var,
         remove_ampersand_var, remove_at_var, remove_underscore_var, remove_comma_var, remove_single_quote_var,
         remove_double_quote_var, title_var, reset_var, initial_output_directory, artist_file, default_frame,
         artist_file_search_var, deep_walk_var, default_decibel, default_audio_normalization,
         remove_successful_lines_var, default_rotation_var, remove_double_space_var, remove_colon_var,
         remove_semicolon_var, remove_percent_var, remove_caret_var, remove_dollar_var, remove_asterisk_var,
         remove_plus_var, remove_equal_var, remove_curly_brace_var, remove_square_bracket_var, remove_pipe_var,
         remove_backslash_var, remove_angle_bracket_var, remove_question_mark_var, remove_parenthesis_var,
         remove_hashtag_var, show_messageboxes_var, show_confirmation_messageboxes_var, fallback_confirmation_var,
         valid_extensions, suppress_var, reset_video_entries_var, reset_artist_entries_var, remove_most_symbols_var,
         remove_number_var, default_minute, default_second, no_go_directory) = (
            self.load_configuration())

        # Filepaths Directories - Set instance variables with the values from the configuration file
        self.initial_directory = initial_directory
        self.initial_output_directory = initial_output_directory
        self.double_check_directory = double_check_directory
        self.no_go_directory = no_go_directory
        self.artist_directory = artist_directory
        self.artist_file = artist_file
        self.categories_file = categories_file

        # Variables and window geometry - Set instance variables with the values from the configuration file
        self.geometry(geometry)
        self.column_numbers = int(column_numbers)
        self.default_weight = default_weight
        self.default_decibel = default_decibel
        self.default_audio_normalization = default_audio_normalization
        self.default_minute = default_minute
        self.default_second = default_second
        self.default_frame = default_frame
        self.file_renamer_log = file_renamer_log
        self.default_placement_var = default_placement_var
        self.special_character_var = special_character_var
        self.reset_output_directory_var = ctk.BooleanVar(value=reset_output_directory_var)
        self.suggest_output_directory_var = ctk.BooleanVar(value=suggest_output_directory_var)
        self.move_up_directory_var = ctk.BooleanVar(value=move_up_directory_var)
        self.move_text_var = ctk.BooleanVar(value=move_text_var)
        self.open_on_file_drop_var = ctk.BooleanVar(value=open_on_file_drop_var)
        self.remove_duplicates_var = ctk.BooleanVar(value=remove_duplicates_var)
        self.double_check_var = ctk.BooleanVar(value=double_check_var)
        self.activate_logging_var = ctk.BooleanVar(value=activate_logging_var)
        self.suppress_var = ctk.BooleanVar(value=suppress_var)
        self.show_messageboxes_var = ctk.BooleanVar(value=show_messageboxes_var)
        self.show_confirmation_messageboxes_var = ctk.BooleanVar(value=show_confirmation_messageboxes_var)
        self.fallback_confirmation_var = ctk.BooleanVar(value=fallback_confirmation_var)
        self.file_extensions = file_extensions
        self.valid_extensions = valid_extensions

        # Name Normalizer - Set instance variables with the values from the configuration file
        self.remove_all_symbols_var = ctk.BooleanVar(value=remove_all_symbols_var)
        self.remove_most_symbols_var = ctk.BooleanVar(value=remove_most_symbols_var)
        self.remove_number_var = ctk.BooleanVar(value=remove_number_var)
        self.tail_var = ctk.BooleanVar(value=tail_var)
        self.remove_parenthesis_trail_var = ctk.BooleanVar(value=remove_parenthesis_trail_var)
        self.remove_parenthesis_var = ctk.BooleanVar(value=remove_parenthesis_var)
        self.remove_hashtag_trail_var = ctk.BooleanVar(value=remove_hashtag_trail_var)
        self.remove_hashtag_var = ctk.BooleanVar(value=remove_hashtag_var)
        self.remove_new_var = ctk.BooleanVar(value=remove_new_var)
        self.remove_dash_var = ctk.BooleanVar(value=remove_dash_var)
        self.remove_endash_var = ctk.BooleanVar(value=remove_endash_var)
        self.remove_emdash_var = ctk.BooleanVar(value=remove_emdash_var)
        self.remove_ampersand_var = ctk.BooleanVar(value=remove_ampersand_var)
        self.remove_at_var = ctk.BooleanVar(value=remove_at_var)
        self.remove_underscore_var = ctk.BooleanVar(value=remove_underscore_var)
        self.remove_comma_var = ctk.BooleanVar(value=remove_comma_var)
        self.remove_single_quote_var = ctk.BooleanVar(value=remove_single_quote_var)
        self.remove_double_quote_var = ctk.BooleanVar(value=remove_double_quote_var)
        self.remove_colon_var = ctk.BooleanVar(value=remove_colon_var)
        self.remove_semicolon_var = ctk.BooleanVar(value=remove_semicolon_var)
        self.remove_percent_var = ctk.BooleanVar(value=remove_percent_var)
        self.remove_caret_var = ctk.BooleanVar(value=remove_caret_var)
        self.remove_dollar_var = ctk.BooleanVar(value=remove_dollar_var)
        self.remove_asterisk_var = ctk.BooleanVar(value=remove_asterisk_var)
        self.remove_plus_var = ctk.BooleanVar(value=remove_plus_var)
        self.remove_equal_var = ctk.BooleanVar(value=remove_equal_var)
        self.remove_curly_brace_var = ctk.BooleanVar(value=remove_curly_brace_var)
        self.remove_square_bracket_var = ctk.BooleanVar(value=remove_square_bracket_var)
        self.remove_pipe_var = ctk.BooleanVar(value=remove_pipe_var)
        self.remove_backslash_var = ctk.BooleanVar(value=remove_backslash_var)
        self.remove_angle_bracket_var = ctk.BooleanVar(value=remove_angle_bracket_var)
        self.remove_question_mark_var = ctk.BooleanVar(value=remove_question_mark_var)
        self.remove_double_space_var = ctk.BooleanVar(value=remove_double_space_var)
        self.title_var = ctk.BooleanVar(value=title_var)
        self.artist_file_search_var = ctk.BooleanVar(value=artist_file_search_var)
        self.reset_var = ctk.BooleanVar(value=reset_var)
        self.reset_video_entries_var = ctk.BooleanVar(value=reset_video_entries_var)
        self.reset_artist_entries_var = ctk.BooleanVar(value=reset_artist_entries_var)
        self.deep_walk_var = ctk.BooleanVar(value=deep_walk_var)

        # Video Editor - Set instance variables with the values from the configuration file
        self.remove_successful_lines_var = ctk.BooleanVar(value=remove_successful_lines_var)
        self.default_rotation_var = default_rotation_var

        # Enable drag-and-drop functionality for files
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_file_drop)

        # Initial check for activate logging state prior to application launch
        self.handle_logging_activation()

        # Register the cleanup method to be called on program exit
        atexit.register(self.cleanup_on_exit)

        # Initialize frame name to default frame
        self.frame_name = self.default_frame

        # Create the GUI elements
        self.create_gui()

    def create_gui(self):
        # Set up grid layout with 1 row and 2 columns, configuring weights for resizing
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation frame (Buttons on the left hand side)
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)  # Index number is responsible for floating

        # Create label for the navigation frame
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  O.C.D. \nFile Editor",
                                                   compound="left",
                                                   font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=5, pady=5)

        # Create file renamer button with specific styling and command
        self.file_renamer_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                 text="File Renamer",
                                                 fg_color="transparent", text_color=("gray10", "gray90"),
                                                 hover_color=("gray70", "gray30"),
                                                 anchor="w", command=self.file_renamer_button_event)
        self.file_renamer_button.grid(row=1, column=0, sticky="ew")

        # Create button for Name Normalizer with specific styling and command
        self.name_normalizer_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                    border_spacing=10, text="Name Normalizer",
                                                    fg_color="transparent", text_color=("gray10", "gray90"),
                                                    hover_color=("gray70", "gray30"),
                                                    anchor="w",
                                                    command=self.name_normalizer_button_event)
        self.name_normalizer_button.grid(row=2, column=0, sticky="ew")

        # Create button for Video Editor with specific styling and command
        self.video_editor_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                 border_spacing=10, text="Video Editor",
                                                 fg_color="transparent", text_color=("gray10", "gray90"),
                                                 hover_color=("gray70", "gray30"),
                                                 anchor="w",
                                                 command=self.video_editor_button_event)
        self.video_editor_button.grid(row=3, column=0, sticky="ew")

        # Create Add/Remove button with specific styling and command
        self.add_remove_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                               text="Add/Remove",
                                               fg_color="transparent", text_color=("gray10", "gray90"),
                                               hover_color=("gray70", "gray30"),
                                               anchor="w",
                                               command=self.add_remove_button_event)
        self.add_remove_button.grid(row=4, column=0, sticky="ew")

        # Create Settings button with specific styling and command
        self.settings_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                             text="Settings",
                                             fg_color="transparent", text_color=("gray10", "gray90"),
                                             hover_color=("gray70", "gray30"),
                                             anchor="w",
                                             command=self.settings_button_event)
        self.settings_button.grid(row=5, column=0, sticky="ew")

        """
        file_renamer_window
        """
        # Create file renamer frame
        self.file_renamer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.file_renamer_frame.grid(row=0, column=1, sticky="nsew")
        self.file_renamer_frame.grid_columnconfigure(0, weight=1)
        self.file_renamer_frame.grid_rowconfigure(0, weight=1)

        # Create a canvas and a scrollbar
        self.file_renamer_canvas = ctk.CTkCanvas(self.file_renamer_frame, highlightthickness=0)
        self.file_renamer_scrollbar = ctk.CTkScrollbar(self.file_renamer_frame, command=self.file_renamer_canvas.yview)
        self.file_renamer_canvas.configure(yscrollcommand=self.file_renamer_scrollbar.set)

        # Set default background color based on system mode
        self.update_background_color()

        # Place the canvas and the scrollbar in the grid
        self.file_renamer_canvas.grid(row=0, column=0, sticky="nsew")
        self.file_renamer_scrollbar.grid(row=0, column=1, sticky="ns")

        # Create a frame inside the canvas for scrollable content
        self.file_renamer_scrollable_frame = ctk.CTkFrame(self.file_renamer_canvas, corner_radius=0,
                                                          bg_color="transparent")
        self.file_renamer_scrollable_frame_window = (self.file_renamer_canvas.create_window(
            (0, 0),
            window=self.file_renamer_scrollable_frame,
            anchor="nw"))

        # Bind canvas and frame for scrolling functionality
        self.file_renamer_canvas.bind('<Configure>', self.on_canvas_configure)
        self.file_renamer_scrollable_frame.bind('<Configure>', self.on_frame_configure)

        # Top frame in the file renamer window
        self.file_renamer_top_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.file_renamer_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Browse file button
        self.browse_file_button = ctk.CTkButton(self.file_renamer_top_frame, text="Browse File",
                                                command=self.browse_input)
        self.browse_file_button.grid(row=0, column=0, padx=5)

        # Selected File Display
        self.file_display_text = ctk.StringVar()
        self.file_display_text.set("Select a file using the 'Browse File' button or drag and drop it into the "
                                   "program...")
        self.file_display_entry = ctk.CTkEntry(self.file_renamer_top_frame, width=890,
                                               textvariable=self.file_display_text)
        self.file_display_entry.grid(row=0, column=1, padx=5)

        # Categories button frame
        self.button_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, padx=10, pady=5)

        # Initialize category buttons
        self.categories_buttons_initialize()

        # Frame to group custom text entry and output directory
        self.custom_text_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                              fg_color="transparent")
        self.custom_text_frame.grid(row=2, column=0, padx=10)

        # Output Directory Browse Button
        self.output_directory_browse_button = ctk.CTkButton(self.custom_text_frame,
                                                            text="Output Directory",
                                                            command=self.browse_output_directory)
        self.output_directory_browse_button.grid(row=0, column=0, padx=5, pady=5)

        # Output Directory Entry
        self.output_directory_entry = ctk.CTkEntry(self.custom_text_frame, width=360)
        self.output_directory_entry.grid(row=0, column=1, padx=5, pady=5)

        # Custom Text Entry
        self.custom_text_entry = ctk.CTkEntry(self.custom_text_frame, width=360)
        self.custom_text_entry.insert(0, "Enter your custom text here...")
        self.custom_text_entry.grid(row=0, column=2, padx=10, pady=10)

        # Rename File Button
        self.rename_button = ctk.CTkButton(self.custom_text_frame, text="Rename File",
                                           command=self.rename_files)
        self.rename_button.grid(row=0, column=3, padx=5, pady=5)

        # Frame to group miscellaneous buttons
        self.button_group_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                               fg_color="transparent")
        self.button_group_frame.grid(row=3, column=0, padx=10)

        # Undo Button
        self.undo_button = ctk.CTkButton(self.button_group_frame, text="Undo", command=self.undo_last)
        self.undo_button.grid(row=0, column=0, padx=10, pady=10)

        # Clear Button
        self.clear_button = ctk.CTkButton(self.button_group_frame, text="Clear",
                                          command=lambda: self.clear_selection(frame_name="file_renamer_window"))
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)

        # Move to Trash Button
        self.trash_button = ctk.CTkButton(self.button_group_frame, text="Move to Trash",
                                          command=self.move_file_to_trash)
        self.trash_button.grid(row=0, column=2, padx=10, pady=10)

        # Select File Renamer Last Used File Button
        self.file_renamer_last_used_file_button = ctk.CTkButton(self.button_group_frame, text="Reload Last File",
                                                                command=self.load_last_used_file)
        self.file_renamer_last_used_file_button.grid(row=0, column=3, padx=10, pady=10)

        # Frame to display the last used file
        self.last_used_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.last_used_frame.grid(row=4, column=0, padx=5)

        # Last Used File Label
        self.last_used_display_label = ctk.CTkLabel(self.last_used_frame, text="Last used file:")
        self.last_used_display_label.grid(row=0, column=0, padx=5, pady=5)

        # Last Used File Display
        self.last_used_display = ctk.CTkLabel(self.last_used_frame, text="")
        self.last_used_display.grid(row=0, column=1, padx=5, pady=5)

        # Frame to display messages
        self.file_renamer_message_label_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                                             fg_color="transparent")
        self.file_renamer_message_label_frame.grid(row=5, column=0, padx=10)

        # Message Label
        self.file_renamer_message_label = ctk.CTkLabel(self.file_renamer_message_label_frame, text="")
        self.file_renamer_message_label.grid(row=0, column=0, padx=10, pady=10)

        # Frame to group placement frame
        self.placement_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0, fg_color="transparent")
        self.placement_frame.grid(row=6, column=0, padx=10, pady=10)

        # Placement Label
        self.placement_label = ctk.CTkLabel(self.placement_frame, text="Placement:")
        self.placement_label.grid(row=0, column=0, padx=10)

        # Variable to track the user's placement choice (prefix, suffix, or special_character)
        self.placement_choice = ctk.StringVar()
        self.placement_choice.set(self.default_placement_var)

        # Radio button for prefix
        self.prefix_radio = ctk.CTkRadioButton(self.placement_frame, text="Prefix",
                                               variable=self.placement_choice,
                                               value="prefix")
        self.prefix_radio.grid(row=0, column=1, padx=10)

        # Radio button for special_character
        self.special_character_radio = ctk.CTkRadioButton(self.placement_frame,
                                                          text=f"Special Character: {self.special_character_var}",
                                                          variable=self.placement_choice,
                                                          value="special_character")
        self.special_character_radio.grid(row=0, column=2, padx=10)

        # Radio button for suffix
        self.suffix_radio = ctk.CTkRadioButton(self.placement_frame, text="Suffix",
                                               variable=self.placement_choice,
                                               value="suffix")
        self.suffix_radio.grid(row=0, column=3, padx=10)

        # Frame to group folder operations
        self.folder_operations_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame, corner_radius=0,
                                                    fg_color="transparent")
        self.folder_operations_frame.grid(row=7, column=0, padx=10)

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

        # Checkbox to enable/disable move text between - and __-__
        self.move_text_checkbox = ctk.CTkCheckBox(self.folder_operations_frame, text="Move Text",
                                                  variable=self.move_text_var)
        self.move_text_checkbox.grid(row=0, column=3, padx=5, pady=5)

        # Send to Module frame
        self.send_to_module_frame = ctk.CTkFrame(self.file_renamer_scrollable_frame,
                                                 corner_radius=0,
                                                 fg_color="transparent")
        self.send_to_module_frame.grid(row=8, column=0, padx=5)

        # Send to Video Editor button
        self.send_to_video_editor_button = ctk.CTkButton(self.send_to_module_frame, text="Send to Video Editor",
                                                         command=lambda: self.send_to_module(
                                                             destination="video_editor_module"))
        self.send_to_video_editor_button.grid(row=0, column=0, padx=10, pady=10)

        # Send to Name Normalizer button
        self.send_to_name_normalizer_button = ctk.CTkButton(self.send_to_module_frame,
                                                            text="Send to Name Normalizer",
                                                            command=lambda: self.send_to_module(
                                                                destination="name_normalizer_module"))
        self.send_to_name_normalizer_button.grid(row=0, column=1, padx=10, pady=10)

        """
        name_normalizer_window
        """
        # Create Name Normalizer frame
        self.name_normalizer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.name_normalizer_frame.grid_columnconfigure(0, weight=1)

        # Name Normalizer Label
        self.name_normalizer_label = ctk.CTkLabel(self.name_normalizer_frame, text="Name Normalizer",
                                                  font=ctk.CTkFont(size=15, weight="bold"))
        self.name_normalizer_label.grid(row=0, column=0, padx=10, pady=10)

        # Name Normalizer Top frame
        self.name_normalizer_top_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                                      fg_color="transparent")
        self.name_normalizer_top_frame.grid(row=1, column=0, padx=10, pady=5)

        # Browse button
        self.nn_browse_button = ctk.CTkButton(self.name_normalizer_top_frame, text="Browse",
                                              command=self.browse_input)
        self.nn_browse_button.grid(row=0, column=0, padx=5, pady=5)

        # Path Entry
        self.nn_path_entry = ctk.CTkEntry(self.name_normalizer_top_frame, width=890)
        self.nn_path_entry.insert(0, "Select a folder or file to normalize using the 'Browse' button...")
        self.nn_path_entry.grid(row=0, column=1, padx=10, pady=10)

        # Button Frame 1
        self.checkbox_frame1 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame1.grid(row=2, column=0, padx=10, pady=5)

        # Checkbox to enable/disable Append '__-__ ' to the file name
        self.tail_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                             text="Append '__-__ '",
                                             variable=self.tail_var)
        self.tail_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove all symbols ,;:@$%^&#*+=(){}[]|\<>'"?_-–—
        self.remove_all_symbols_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                                           text="Remove all symbols",
                                                           variable=self.remove_all_symbols_var)
        self.remove_all_symbols_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove most symbols ,;:@$%^&*+={}[]|\<>"?-–—
        self.remove_most_symbols_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                                            text="Remove most symbols",
                                                            variable=self.remove_most_symbols_var)
        self.remove_most_symbols_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable reset entries
        self.remove_numbers_checkbox = ctk.CTkCheckBox(self.checkbox_frame1,
                                                       text="Remove numbers",
                                                       variable=self.remove_number_var)
        self.remove_numbers_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Button Frame 2
        self.checkbox_frame2 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame2.grid(row=3, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove new
        self.remove_new_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                   text="Remove new",
                                                   variable=self.remove_new_var)
        self.remove_new_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove dashes
        self.remove_dash_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                    text="Remove dashes",
                                                    variable=self.remove_dash_var)
        self.remove_dash_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove endashes
        self.remove_endash_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                      text="Remove endashes",
                                                      variable=self.remove_endash_var)
        self.remove_endash_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove emdashes
        self.remove_emdash_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                      text="Remove emdashes",
                                                      variable=self.remove_emdash_var)
        self.remove_emdash_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove hashtags
        self.remove_hashtag_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                       text="Remove hashtags",
                                                       variable=self.remove_hashtag_var)
        self.remove_hashtag_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Checkbox to enable/disable remove commas
        self.remove_comma_checkbox = ctk.CTkCheckBox(self.checkbox_frame2,
                                                     text="Remove commas",
                                                     variable=self.remove_comma_var)
        self.remove_comma_checkbox.grid(row=0, column=5, padx=10, pady=10)

        # Button Frame 3
        self.checkbox_frame3 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame3.grid(row=4, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove ampersands
        self.remove_ampersand_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                         text="Remove ampersands",
                                                         variable=self.remove_ampersand_var)
        self.remove_ampersand_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove @
        self.remove_at_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                  text="Remove @",
                                                  variable=self.remove_at_var)
        self.remove_at_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove underscores
        self.remove_underscore_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                          text="Remove underscores",
                                                          variable=self.remove_underscore_var)
        self.remove_underscore_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove single quotes
        self.remove_single_quote_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                            text="Remove single quotes",
                                                            variable=self.remove_single_quote_var)
        self.remove_single_quote_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove double quotes
        self.remove_double_quote_checkbox = ctk.CTkCheckBox(self.checkbox_frame3,
                                                            text="Remove double quotes",
                                                            variable=self.remove_double_quote_var)
        self.remove_double_quote_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Button Frame 4
        self.checkbox_frame4 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame4.grid(row=5, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove dollars
        self.remove_dollar_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                      text="Remove dollars",
                                                      variable=self.remove_dollar_var)
        self.remove_dollar_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove colons
        self.remove_colon_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                     text="Remove colons",
                                                     variable=self.remove_colon_var)
        self.remove_colon_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable semicolons
        self.remove_semicolon_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                         text="Remove semicolons",
                                                         variable=self.remove_semicolon_var)
        self.remove_semicolon_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove percents
        self.remove_percent_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                       text="Remove percents",
                                                       variable=self.remove_percent_var)
        self.remove_percent_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove carets
        self.remove_caret_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                     text="Remove carets",
                                                     variable=self.remove_caret_var)
        self.remove_caret_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Checkbox to enable/disable remove plus signs
        self.remove_plus_checkbox = ctk.CTkCheckBox(self.checkbox_frame4,
                                                    text="Remove plus signs",
                                                    variable=self.remove_plus_var)
        self.remove_plus_checkbox.grid(row=0, column=5, padx=10, pady=10)

        # Button Frame 5
        self.checkbox_frame5 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame5.grid(row=6, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove asterisks
        self.remove_asterisk_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                        text="Remove asterisks",
                                                        variable=self.remove_asterisk_var)
        self.remove_asterisk_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove parenthesis
        self.remove_parenthesis_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                           text="Remove parenthesis",
                                                           variable=self.remove_parenthesis_var)
        self.remove_parenthesis_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove angle brackets
        self.remove_angle_bracket_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                             text="Remove angle brackets",
                                                             variable=self.remove_angle_bracket_var)
        self.remove_angle_bracket_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove curly braces
        self.remove_curly_brace_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                           text="Remove curly braces",
                                                           variable=self.remove_curly_brace_var)
        self.remove_curly_brace_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable remove square brackets
        self.remove_square_bracket_checkbox = ctk.CTkCheckBox(self.checkbox_frame5,
                                                              text="Remove square brackets",
                                                              variable=self.remove_square_bracket_var)
        self.remove_square_bracket_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Button Frame 6
        self.checkbox_frame6 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame6.grid(row=7, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove pipes
        self.remove_pipe_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                    text="Remove pipes",
                                                    variable=self.remove_pipe_var)
        self.remove_pipe_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove backslashes
        self.remove_backslash_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                         text="Remove backslashes",
                                                         variable=self.remove_backslash_var)
        self.remove_backslash_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable remove equal signs
        self.remove_equal_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                     text="Remove equal signs",
                                                     variable=self.remove_equal_var)
        self.remove_equal_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable remove question marks
        self.remove_question_mark_checkbox = ctk.CTkCheckBox(self.checkbox_frame6,
                                                             text="Remove question marks",
                                                             variable=self.remove_question_mark_var)
        self.remove_question_mark_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Button Frame 7
        self.checkbox_frame7 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame7.grid(row=8, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove parenthesis and trailing text
        self.remove_parenthesis_trail_checkbox = ctk.CTkCheckBox(self.checkbox_frame7,
                                                                 text="Remove text following the first '('",
                                                                 variable=self.remove_parenthesis_trail_var)
        self.remove_parenthesis_trail_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable remove hashtag and trailing text
        self.remove_hashtag_trail_checkbox = ctk.CTkCheckBox(self.checkbox_frame7,
                                                             text="Remove text following the first '#'",
                                                             variable=self.remove_hashtag_trail_var)
        self.remove_hashtag_trail_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Button Frame 8
        self.checkbox_frame8 = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                            fg_color="transparent")
        self.checkbox_frame8.grid(row=9, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove double spaces
        self.remove_double_space_checkbox = ctk.CTkCheckBox(self.checkbox_frame8,
                                                            text="Remove double spaces",
                                                            variable=self.remove_double_space_var)
        self.remove_double_space_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable Titlefy the name
        self.title_checkbox = ctk.CTkCheckBox(self.checkbox_frame8,
                                              text="Titlefy the name",
                                              variable=self.title_var)
        self.title_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Checkbox to enable/disable Artist Search
        self.artist_search_checkbox = ctk.CTkCheckBox(self.checkbox_frame8,
                                                      text="Artist Search",
                                                      variable=self.artist_file_search_var)
        self.artist_search_checkbox.grid(row=0, column=2, padx=10, pady=10)

        # Checkbox to enable/disable include subdirectories
        self.deep_walk_checkbox = ctk.CTkCheckBox(self.checkbox_frame8,
                                                  text="Include subdirectories",
                                                  variable=self.deep_walk_var)
        self.deep_walk_checkbox.grid(row=0, column=3, padx=10, pady=10)

        # Checkbox to enable/disable reset entries
        self.reset_checkbox = ctk.CTkCheckBox(self.checkbox_frame8,
                                              text="Reset entries",
                                              variable=self.reset_var)
        self.reset_checkbox.grid(row=0, column=4, padx=10, pady=10)

        # Output directory move frame
        self.output_directory_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.output_directory_frame.grid(row=10, column=0, padx=10, pady=5)

        # Browse move directory folder button
        self.browse_move_directory_button = ctk.CTkButton(self.output_directory_frame, text="Output Directory",
                                                          command=self.browse_output_directory)
        self.browse_move_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Move directory entry
        self.move_directory_entry = ctk.CTkEntry(self.output_directory_frame, width=890)
        self.move_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Normalize Folder frame
        self.normalize_folder_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.normalize_folder_frame.grid(row=11, column=0, padx=10, pady=5)

        # Clear Name Normalizer Selection Button
        self.clear_name_normalizer_selection_button = ctk.CTkButton(self.normalize_folder_frame,
                                                                    text="Clear",
                                                                    command=lambda: self.clear_selection(
                                                                        frame_name="name_normalizer_window"))
        self.clear_name_normalizer_selection_button.grid(row=0, column=0, padx=10, pady=10)

        # Select Name Normalizer Last Used File Button
        self.name_normalizer_last_used_file_button = ctk.CTkButton(self.normalize_folder_frame,
                                                                   text="Reload Last File",
                                                                   command=self.load_last_used_file)
        self.name_normalizer_last_used_file_button.grid(row=0, column=1, padx=10, pady=10)

        # Normalize Preview button
        self.normalize_preview_button = ctk.CTkButton(self.normalize_folder_frame, text="Preview",
                                                      command=lambda: self.process_name_normalizer(mode="preview"))
        self.normalize_preview_button.grid(row=0, column=2, padx=5, pady=5)

        # Normalize button
        self.normalize_button = ctk.CTkButton(self.normalize_folder_frame, text="Normalize",
                                              command=lambda: self.process_name_normalizer(mode="action"))
        self.normalize_button.grid(row=0, column=3, padx=5, pady=5)

        # Send to Module frame
        self.send_to_module_frame1 = ctk.CTkFrame(self.name_normalizer_frame,
                                                  corner_radius=0,
                                                  fg_color="transparent")
        self.send_to_module_frame1.grid(row=12, column=0, padx=5)

        # Send to File Renamer button
        self.send_to_file_renamer_button1 = ctk.CTkButton(self.send_to_module_frame1, text="Send to File Renamer",
                                                          command=lambda: self.send_to_module(
                                                              destination="file_renamer_module"))
        self.send_to_file_renamer_button1.grid(row=0, column=0, padx=10, pady=10)

        # Send to Video Editor button
        self.send_to_video_editor_button1 = ctk.CTkButton(self.send_to_module_frame1, text="Send to Video Editor",
                                                          command=lambda: self.send_to_module(
                                                              destination="video_editor_module"))
        self.send_to_video_editor_button1.grid(row=0, column=1, padx=10, pady=10)

        # Frame to display messages on the Name Normalizer frame
        self.name_normalizer_message_label_frame = ctk.CTkFrame(self.name_normalizer_frame, corner_radius=0,
                                                                fg_color="transparent")
        self.name_normalizer_message_label_frame.grid(row=13, column=0, padx=10)

        # Name Normalizer message Label
        self.name_normalizer_message_label = ctk.CTkLabel(self.name_normalizer_message_label_frame, text="")
        self.name_normalizer_message_label.grid(row=0, column=0, padx=10, pady=10)

        """
        video_editor_window
        """
        # Create Video Editor frame
        self.video_editor_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.video_editor_frame.grid_columnconfigure(0, weight=1)

        # Video Editor Label
        self.video_editor_label = ctk.CTkLabel(self.video_editor_frame, text="Video Editor",
                                               font=ctk.CTkFont(size=15, weight="bold"))
        self.video_editor_label.grid(row=0, column=0, padx=10, pady=10)

        # Video Editor Top frame
        self.video_editor_top_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.video_editor_top_frame.grid(row=1, column=0, padx=10, pady=5)

        # Video Editor browse input method button
        self.browse_input_method_button = ctk.CTkButton(self.video_editor_top_frame, text="Browse",
                                                        command=self.browse_input)
        self.browse_input_method_button.grid(row=0, column=0, padx=5, pady=5)

        # Input method entry for a file, directory, or .txt containing a line delimited list of files to process
        self.input_method_entry = ctk.CTkEntry(self.video_editor_top_frame, width=890)
        self.input_method_entry.insert(0, "Select a video to edit using the 'Browse' button...")
        self.input_method_entry.grid(row=0, column=1, padx=10, pady=10)

        # Rotation frame
        self.rotation_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                           fg_color="transparent")
        self.rotation_frame.grid(row=3, column=0, padx=10, pady=5)

        # Rotate Video label
        self.rotation_label = ctk.CTkLabel(self.rotation_frame, text="Rotate Video:")
        self.rotation_label.grid(row=0, column=0, padx=10, pady=5)

        # Variable to store rotation option
        self.rotation_var = ctk.StringVar()
        self.rotation_var.set(self.default_rotation_var)

        # Left rotation radio button
        self.left_radio = ctk.CTkRadioButton(self.rotation_frame, text="Left", variable=self.rotation_var, value="left")
        self.left_radio.grid(row=0, column=1, padx=10, pady=5)

        # Right rotation radio button
        self.right_radio = ctk.CTkRadioButton(self.rotation_frame, text="Right", variable=self.rotation_var,
                                              value="right")
        self.right_radio.grid(row=0, column=2, padx=10, pady=5)

        # Flip rotation radio button
        self.flip_radio = ctk.CTkRadioButton(self.rotation_frame, text="Flip", variable=self.rotation_var,
                                             value="flip")
        self.flip_radio.grid(row=0, column=3, padx=10, pady=5)

        # None rotation radio button
        self.no_rotation_radio = ctk.CTkRadioButton(self.rotation_frame, text="None", variable=self.rotation_var,
                                                    value="none")
        self.no_rotation_radio.grid(row=0, column=4, padx=10, pady=5)

        # Decibel frame
        self.decibel_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                          fg_color="transparent")
        self.decibel_frame.grid(row=4, column=0, padx=10, pady=5)

        # Increase Audio (dB) label
        self.decibel_label = ctk.CTkLabel(self.decibel_frame, text="Increase Audio (dB):")
        self.decibel_label.grid(row=0, column=0, padx=10, pady=5)

        # Initialize decibel variable
        self.decibel_var = ctk.StringVar()
        self.decibel_var.set(self.default_decibel)

        # Trace the changes in the StringVar
        self.decibel_var.trace_add("write", lambda *args: self.validate_entry(
            self.decibel_var,
            self.default_decibel,
            desired_type=float))

        # Decibel entry
        self.decibel_entry = ctk.CTkEntry(self.decibel_frame, textvariable=self.decibel_var, width=50)
        self.decibel_entry.grid(row=0, column=1, padx=10, pady=10)

        # Audio Normalization frame
        self.audio_normalization_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                      fg_color="transparent")
        self.audio_normalization_frame.grid(row=5, column=0, padx=10, pady=5)

        # Normalize Audio label
        self.audio_normalization_label = ctk.CTkLabel(self.audio_normalization_frame, text="Normalize Audio:")
        self.audio_normalization_label.grid(row=0, column=0, padx=10, pady=5)

        # Initialize audio normalization variable
        self.audio_normalization_var = ctk.StringVar()
        self.audio_normalization_var.set(self.default_audio_normalization)

        # Trace the changes in the StringVar
        self.audio_normalization_var.trace_add("write",
                                               lambda *args: self.validate_entry(
                                                   self.audio_normalization_var,
                                                   self.default_audio_normalization,
                                                   desired_type=float))

        # Audio Normalization entry
        self.audio_normalization_entry = ctk.CTkEntry(self.audio_normalization_frame,
                                                      textvariable=self.audio_normalization_var,
                                                      width=50)
        self.audio_normalization_entry.grid(row=0, column=1, padx=10, pady=10)

        # Trim frame
        self.trim_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                       fg_color="transparent")
        self.trim_frame.grid(row=6, column=0, padx=10, pady=5)

        # Trim label
        self.trim_label = ctk.CTkLabel(self.trim_frame, text="Trim (Minutes:Seconds):")
        self.trim_label.grid(row=0, column=0, padx=10, pady=5)

        # Initialize minute variable
        self.minute_var = ctk.StringVar()
        self.minute_var.set(self.default_minute)

        # Trace the changes in the StringVar
        self.minute_var.trace_add("write", lambda *args: self.validate_entry(
            self.minute_var,
            self.default_minute,
            desired_type=int))

        # Minute entry
        self.minute_entry = ctk.CTkEntry(self.trim_frame, textvariable=self.minute_var, width=50)
        self.minute_entry.grid(row=0, column=1, padx=10, pady=10)

        # Trim label
        self.colon_label = ctk.CTkLabel(self.trim_frame, text=":")
        self.colon_label.grid(row=0, column=2)

        # Initialize second variable
        self.second_var = ctk.StringVar()
        self.second_var.set(self.default_second)

        # Trace the changes in the StringVar
        self.second_var.trace_add("write", lambda *args: self.validate_entry(
            self.second_var,
            self.default_second,
            desired_type=int))

        # Second entry
        self.second_entry = ctk.CTkEntry(self.trim_frame, textvariable=self.second_var, width=50)
        self.second_entry.grid(row=0, column=3, padx=10, pady=10)

        # Video Editor Output directory frame
        self.video_editor_output_directory_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                                fg_color="transparent")
        self.video_editor_output_directory_frame.grid(row=8, column=0, padx=10, pady=5)

        # Browse video editor output directory folder button
        self.browse_video_editor_output_directory_button = ctk.CTkButton(self.video_editor_output_directory_frame,
                                                                         text="Output Directory",
                                                                         command=self.browse_output_directory)
        self.browse_video_editor_output_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Video editor output directory entry
        self.video_editor_output_directory_entry = ctk.CTkEntry(self.video_editor_output_directory_frame, width=890)
        self.video_editor_output_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Process video editor frame
        self.process_video_editor_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                       fg_color="transparent")
        self.process_video_editor_frame.grid(row=9, column=0, padx=10, pady=5)

        # Clear process video editor Button
        self.clear_video_editor_selection_button = ctk.CTkButton(self.process_video_editor_frame,
                                                                 text="Clear",
                                                                 command=lambda: self.clear_selection(
                                                                     frame_name="video_editor_window"))
        self.clear_video_editor_selection_button.grid(row=0, column=0, padx=10, pady=10)

        # Select Video Editor Last Used File Button
        self.video_editor_last_used_file_button = ctk.CTkButton(self.process_video_editor_frame,
                                                                text="Reload Last File",
                                                                command=self.load_last_used_file)
        self.video_editor_last_used_file_button.grid(row=0, column=1, padx=10, pady=10)

        # Process video button
        self.process_video_edits_button = ctk.CTkButton(self.process_video_editor_frame, text="Process video(s)",
                                                        command=self.process_video_edits)
        self.process_video_edits_button.grid(row=0, column=2, padx=5, pady=5)

        # Frame to display messages on the video editor frame
        self.send_to_module_frame2 = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                  fg_color="transparent")
        self.send_to_module_frame2.grid(row=10, column=0, padx=10)

        # Send to File Renamer button
        self.send_to_file_renamer_button = ctk.CTkButton(self.send_to_module_frame2, text="Send to File Renamer",
                                                         command=lambda: self.send_to_module(
                                                             destination="file_renamer_module"))
        self.send_to_file_renamer_button.grid(row=0, column=0, padx=10, pady=10)

        # Send to Name Normalizer button
        self.send_to_name_normalizer_button1 = ctk.CTkButton(self.send_to_module_frame2,
                                                             text="Send to Name Normalizer",
                                                             command=lambda: self.send_to_module(
                                                                 destination="name_normalizer_module"))
        self.send_to_name_normalizer_button1.grid(row=0, column=1, padx=10, pady=10)

        # Video editor checkbox frame
        self.video_editor_checkbox_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                        fg_color="transparent")
        self.video_editor_checkbox_frame.grid(row=11, column=0, padx=10, pady=5)

        # Checkbox to enable/disable remove successful lines
        self.remove_successful_lines_checkbox = ctk.CTkCheckBox(self.video_editor_checkbox_frame,
                                                                text="Remove successful lines from input file",
                                                                variable=self.remove_successful_lines_var)
        self.remove_successful_lines_checkbox.grid(row=0, column=0, padx=10, pady=10)

        # Checkbox to enable/disable reset video editor entries
        self.reset_video_checkbox = ctk.CTkCheckBox(self.video_editor_checkbox_frame,
                                                    text="Reset entries",
                                                    variable=self.reset_video_entries_var)
        self.reset_video_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Frame to display messages on the video editor frame
        self.video_editor_message_label_frame = ctk.CTkFrame(self.video_editor_frame, corner_radius=0,
                                                             fg_color="transparent")
        self.video_editor_message_label_frame.grid(row=12, column=0, padx=10)

        # Video editor message Label
        self.video_editor_message_label = ctk.CTkLabel(self.video_editor_message_label_frame, text="")
        self.video_editor_message_label.grid(row=0, column=0, padx=10, pady=10)

        """
        add_remove_window
        """
        # Create Add/Remove frame
        self.add_remove_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.add_remove_frame.grid_columnconfigure(0, weight=1)

        # Artist Label
        self.artist_label = ctk.CTkLabel(self.add_remove_frame, text="Artist",
                                         font=ctk.CTkFont(size=15, weight="bold"))
        self.artist_label.grid(row=0, column=0, padx=10, pady=10)

        # Add/Remove Top frame
        self.add_remove_top_frame = ctk.CTkFrame(self.add_remove_frame, corner_radius=0,
                                                 fg_color="transparent")
        self.add_remove_top_frame.grid(row=1, column=0, padx=10, pady=5)

        # Add and remove artist list frame
        self.add_remove_artist_entry_frame = ctk.CTkFrame(self.add_remove_top_frame, corner_radius=0,
                                                          fg_color="transparent")
        self.add_remove_artist_entry_frame.grid(row=0, column=0, padx=10, pady=10)

        # Add artist button
        self.add_artist_button = ctk.CTkButton(self.add_remove_artist_entry_frame, text="Add Artist",
                                               command=self.add_artist_to_file)
        self.add_artist_button.grid(row=0, column=0, padx=5)

        # Add artist entry
        self.add_artist_entry = ctk.CTkEntry(self.add_remove_artist_entry_frame, width=370)
        self.add_artist_entry.grid(row=0, column=1, padx=5)

        # Remove artist button
        self.remove_artist_button = ctk.CTkButton(self.add_remove_artist_entry_frame, text="Remove Artist",
                                                  command=self.remove_artist_from_file)
        self.remove_artist_button.grid(row=0, column=2, padx=5, pady=5)

        # Remove artist entry
        self.remove_artist_entry = ctk.CTkEntry(self.add_remove_artist_entry_frame, width=370)
        self.remove_artist_entry.grid(row=0, column=3, padx=5)

        # Frame for clear artist button
        self.clear_artist_frame = ctk.CTkFrame(self.add_remove_top_frame, corner_radius=0,
                                               fg_color="transparent")
        self.clear_artist_frame.grid(row=1, column=0, padx=10)

        # Clear Button
        self.clear_artist_button = ctk.CTkButton(self.clear_artist_frame,
                                                 text="Clear",
                                                 command=lambda: self.clear_selection(frame_name="add_remove_window"))
        self.clear_artist_button.grid(row=0, column=0, padx=10, pady=10)

        # Frame for reset artist checkbox
        self.reset_artist_frame = ctk.CTkFrame(self.add_remove_top_frame, corner_radius=0,
                                               fg_color="transparent")
        self.reset_artist_frame.grid(row=2, column=0, padx=10, pady=10)

        # Checkbox to enable/disable reset artist entries
        self.reset_artist_checkbox = ctk.CTkCheckBox(self.reset_artist_frame,
                                                     text="Reset entries",
                                                     variable=self.reset_artist_entries_var)
        self.reset_artist_checkbox.grid(row=0, column=1, padx=10, pady=10)

        # Frame for add/remove category elements
        self.category_label_frame = ctk.CTkFrame(self.add_remove_top_frame, corner_radius=0, fg_color="transparent")
        self.category_label_frame.grid(row=3, column=0, padx=10, pady=10)

        # Category Label
        self.category_label = ctk.CTkLabel(self.category_label_frame, text="Category",
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.category_label.grid(row=0, column=0, padx=10, pady=10)

        self.category_frame = ctk.CTkFrame(self.add_remove_top_frame, corner_radius=0, fg_color="transparent")
        self.category_frame.grid(row=4, column=0, padx=10, pady=10)

        # Add Category Button
        self.add_category_button = ctk.CTkButton(self.category_frame, text="Add Category", command=self.add_category)
        self.add_category_button.grid(row=0, column=0, padx=5)

        # Add Category Entry
        self.category_entry = ctk.CTkEntry(self.category_frame, width=310)
        self.category_entry.grid(row=0, column=1, padx=5)

        # Weight Label
        self.weight_label = ctk.CTkLabel(self.category_frame, text="Weight:")
        self.weight_label.grid(row=0, column=2, padx=5)

        # Initialize weight variable
        self.weight_var = ctk.StringVar()
        self.weight_var.set(self.default_weight)

        # Trace the changes in the StringVar
        self.weight_var.trace_add("write", lambda *args: self.validate_entry(
            self.weight_var,
            self.default_weight,
            desired_type=int))

        # Weight Entry
        self.weight_entry = ctk.CTkEntry(self.category_frame, textvariable=self.weight_var, width=35)
        self.weight_entry.grid(row=0, column=3, padx=5)

        # Remove Category Button
        self.remove_category_button = ctk.CTkButton(self.category_frame, text="Remove Category",
                                                    command=self.remove_category)
        self.remove_category_button.grid(row=0, column=4, padx=5)

        # Remove Category Entry
        self.remove_category_entry = ctk.CTkEntry(self.category_frame, width=310)
        self.remove_category_entry.grid(row=0, column=5, padx=5)

        # NO-GO label frame
        self.no_go_label_frame = ctk.CTkFrame(self.add_remove_top_frame, corner_radius=0,
                                              fg_color="transparent")
        self.no_go_label_frame.grid(row=5, column=0, padx=10, pady=10)

        # NO-GO label
        self.no_go_label = ctk.CTkLabel(self.no_go_label_frame, text="NO GO",
                                        font=ctk.CTkFont(size=15, weight="bold"))
        self.no_go_label.grid(row=0, column=0, padx=10, pady=10)

        # NO-GO frame
        self.no_go_entry_frame = ctk.CTkFrame(self.add_remove_top_frame, corner_radius=0,
                                              fg_color="transparent")
        self.no_go_entry_frame.grid(row=6, column=0, padx=10, pady=10)

        # Add NO-GO button
        self.add_no_go_button = ctk.CTkButton(self.no_go_entry_frame, text="Add NO GO",
                                              command=self.no_go_creation)
        self.add_no_go_button.grid(row=0, column=0, padx=5)

        # Add NO-GO entry
        self.add_no_go_name_entry = ctk.CTkEntry(self.no_go_entry_frame, width=370)
        self.add_no_go_name_entry.grid(row=0, column=1, padx=5)

        # Frame to display messages on the add/remove frame
        self.add_remove_label_frame = ctk.CTkFrame(self.add_remove_top_frame, corner_radius=0,
                                                   fg_color="transparent")
        self.add_remove_label_frame.grid(row=12, column=0, padx=10)

        # Add/Remove Label
        self.add_remove_label = ctk.CTkLabel(self.add_remove_label_frame, text="")
        self.add_remove_label.grid(row=0, column=0, padx=10, pady=10)

        """
        settings_window
        """
        # Create settings frame
        self.settings_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # Settings top frame
        self.settings_top_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.settings_top_frame.grid(row=0, column=0, padx=10, pady=10)

        # Settings label
        self.settings_label = ctk.CTkLabel(self.settings_top_frame, text="Settings",
                                           font=ctk.CTkFont(size=15, weight="bold"))
        self.settings_label.grid(row=0, column=0, padx=5, pady=5, columnspan=5)

        # Switch frame
        self.switch_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.switch_frame.grid(row=1, column=0, padx=10, pady=10)

        # Switch to enable/disable open on drop behavior
        self.open_on_file_drop_switch = ctk.CTkSwitch(self.switch_frame, text="Open File on Drag and Drop",
                                                      variable=self.open_on_file_drop_var)
        self.open_on_file_drop_switch.grid(row=0, column=0, padx=10, pady=10)

        # Switch to enable/disable remove duplicates
        self.remove_duplicates_switch = ctk.CTkSwitch(self.switch_frame,
                                                      text="Remove Duplicates",
                                                      variable=self.remove_duplicates_var)
        self.remove_duplicates_switch.grid(row=0, column=1, padx=10, pady=10)

        # Switch to enable/disable create double check reminder
        self.double_check_switch = ctk.CTkSwitch(self.switch_frame, text="Create Double Check Reminder",
                                                 variable=self.double_check_var)
        self.double_check_switch.grid(row=0, column=2, padx=10, pady=10)

        # Switch to enable/disable activate logging
        self.activate_logging_switch = ctk.CTkSwitch(self.switch_frame, text="Activate Logging",
                                                     variable=self.activate_logging_var)
        self.activate_logging_switch.grid(row=1, column=0, padx=10, pady=10)

        # Bind the callback function to the activate logging variable
        self.activate_logging_var.trace_add("write", self.handle_logging_activation)

        # Switch to enable/disable suppress standard outputs/errors
        self.suppress_switch = ctk.CTkSwitch(self.switch_frame, text="Suppress Standard Output/Error",
                                             variable=self.suppress_var)
        self.suppress_switch.grid(row=1, column=1, padx=10, pady=10)

        # Switch to enable/disable show messageboxes
        self.show_messageboxes_switch = ctk.CTkSwitch(self.switch_frame, text="Show Messageboxes",
                                                      variable=self.show_messageboxes_var)
        self.show_messageboxes_switch.grid(row=1, column=2, padx=10, pady=10)

        # Confirmation frame
        self.confirmation_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.confirmation_frame.grid(row=2, column=0, padx=10)

        # Switch to enable/disable show confirmation messageboxes
        self.show_confirmation_messageboxes_switch = ctk.CTkSwitch(self.confirmation_frame,
                                                                   text="Show Confirmation Messageboxes",
                                                                   variable=self.show_confirmation_messageboxes_var)
        self.show_confirmation_messageboxes_switch.grid(row=0, column=0, padx=10, pady=10)

        # Fallback confirmation state when confirmation messageboxes are suppressed
        self.fallback_confirmation_label = ctk.CTkLabel(self.confirmation_frame, text="Fallback confirmation state:")
        self.fallback_confirmation_label.grid(row=0, column=1, padx=10, pady=5)

        # Fallback true radio button
        self.true_radio = ctk.CTkRadioButton(self.confirmation_frame, text="True",
                                             variable=self.fallback_confirmation_var, value=True)
        self.true_radio.grid(row=0, column=2, padx=10, pady=5)

        # Fallback false radio button
        self.false_radio = ctk.CTkRadioButton(self.confirmation_frame, text="False",
                                              variable=self.fallback_confirmation_var,
                                              value=False)
        self.false_radio.grid(row=0, column=3, padx=10, pady=5)

        # GUI settings frame
        self.gui_settings_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.gui_settings_frame.grid(row=3, column=0, padx=10, pady=10)

        # Select light or dark label
        self.appearance_mode_label = ctk.CTkLabel(self.gui_settings_frame, text="Appearance:")
        self.appearance_mode_label.grid(row=0, column=0, padx=10, pady=10)

        # Select light or dark mode
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.gui_settings_frame,
                                                      values=["Light", "Dark"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=0, column=1, padx=10, pady=10)

        # Set default value for appearance
        self.appearance_mode_menu.set("Dark")

        # Select scaling label
        self.scaling_label = ctk.CTkLabel(self.gui_settings_frame, text="UI Scaling:")
        self.scaling_label.grid(row=1, column=0, padx=10, pady=10)

        # Select scaling level
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.gui_settings_frame,
                                                     values=["70%", "80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=1, column=1, padx=10, pady=10)

        # Set default value for scaling
        self.scaling_optionemenu.set("100%")

        # Master Entry frame
        self.master_entry_frame = ctk.CTkFrame(self.settings_frame, corner_radius=0, fg_color="transparent")
        self.master_entry_frame.grid(row=4, column=0, padx=10, pady=10)

        # Initial Directory frame
        self.initial_directory_frame = ctk.CTkFrame(self.master_entry_frame, corner_radius=0, fg_color="transparent")
        self.initial_directory_frame.grid(row=0, column=0, padx=10, pady=10)

        # Browse Initial Directory button
        self.browse_initial_directory_button = ctk.CTkButton(self.initial_directory_frame, text="Initial Directory",
                                                             command=self.browse_initial_directory)
        self.browse_initial_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Initial Directory entry
        self.initial_directory_entry = ctk.CTkEntry(self.initial_directory_frame, width=855)
        self.initial_directory_entry.insert(0, self.initial_directory)
        self.initial_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browse Initial Output Directory button
        self.browse_initial_output_directory_button = ctk.CTkButton(self.initial_directory_frame,
                                                                    text="Initial Output Directory",
                                                                    command=self.browse_initial_output_directory)
        self.browse_initial_output_directory_button.grid(row=1, column=0, padx=5, pady=5)

        # Initial Directory entry
        self.initial_output_directory_entry = ctk.CTkEntry(self.initial_directory_frame, width=855)
        self.initial_output_directory_entry.insert(0, self.initial_output_directory)
        self.initial_output_directory_entry.grid(row=1, column=1, padx=10, pady=10)

        # Double Check Directory frame
        self.double_check_reminder_directory_frame = ctk.CTkFrame(self.master_entry_frame, corner_radius=0,
                                                                  fg_color="transparent")
        self.double_check_reminder_directory_frame.grid(row=1, column=0, padx=10, pady=10)

        # Browse Double Check Reminder Directory button
        self.browse_double_check_reminder_directory_button = ctk.CTkButton(self.double_check_reminder_directory_frame,
                                                                           text="Double Check Reminder Directory",
                                                                           command=self.
                                                                           browse_double_check_reminder_directory)
        self.browse_double_check_reminder_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Double Check Reminder entry
        self.double_check_reminder_directory_entry = ctk.CTkEntry(self.double_check_reminder_directory_frame, width=775)
        self.double_check_reminder_directory_entry.insert(0, self.double_check_directory)
        self.double_check_reminder_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browse NO GO Reminder Directory button
        self.browse_no_go_reminder_directory_button = ctk.CTkButton(self.double_check_reminder_directory_frame,
                                                                    text="NO GO Directory",
                                                                    command=self.browse_no_go_directory)
        self.browse_no_go_reminder_directory_button.grid(row=1, column=0, padx=5, pady=5)

        # NO GO Reminder entry
        self.no_go_reminder_directory_entry = ctk.CTkEntry(self.double_check_reminder_directory_frame, width=775)
        self.no_go_reminder_directory_entry.insert(0, self.no_go_directory)
        self.no_go_reminder_directory_entry.grid(row=1, column=1, padx=10, pady=10)

        # Artist directory frame
        self.artist_directory_frame = ctk.CTkFrame(self.master_entry_frame, corner_radius=0, fg_color="transparent")
        self.artist_directory_frame.grid(row=2, column=0, padx=10, pady=10)

        # Browse Artist Directory button
        self.browse_artist_directory_button = ctk.CTkButton(self.artist_directory_frame, text="Artist Directory",
                                                            command=self.browse_artist_directory)
        self.browse_artist_directory_button.grid(row=0, column=0, padx=5, pady=5)

        # Artist Directory entry
        self.artist_directory_entry = ctk.CTkEntry(self.artist_directory_frame, width=890)
        self.artist_directory_entry.insert(0, self.artist_directory)
        self.artist_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browse Artist File button
        self.browse_artist_file_button = ctk.CTkButton(self.artist_directory_frame, text="Artist File",
                                                       command=self.browse_artist_file)
        self.browse_artist_file_button.grid(row=1, column=0, padx=5, pady=5)

        # Artist File entry
        self.artist_file_entry = ctk.CTkEntry(self.artist_directory_frame, width=890)
        self.artist_file_entry.insert(0, self.artist_file)
        self.artist_file_entry.grid(row=1, column=1, padx=10, pady=10)

        # Configuration File Frame
        self.configuration_file_frame = ctk.CTkFrame(self.master_entry_frame, corner_radius=0,
                                                     fg_color="transparent")
        self.configuration_file_frame.grid(row=3, column=0, padx=10, pady=10)

        # Browse Configuration File button
        self.open_configuration_file_button = ctk.CTkButton(self.configuration_file_frame, text="Open Config File",
                                                            command=lambda: self.open_file(
                                                                self.config_file_path))
        self.open_configuration_file_button.grid(row=0, column=0, padx=5)

        # Configuration File entry
        self.configuration_file_entry = ctk.CTkEntry(self.configuration_file_frame, width=890)
        self.configuration_file_entry.insert(0, self.config_file_path)
        self.configuration_file_entry.grid(row=0, column=1, padx=10, pady=10)

        # Browse Log button
        self.open_log_file_button = ctk.CTkButton(self.configuration_file_frame, text="Open Log File",
                                                  command=lambda: self.open_file(
                                                      self.file_renamer_log))
        self.open_log_file_button.grid(row=1, column=0, padx=5)

        # log File entry
        self.log_file_entry = ctk.CTkEntry(self.configuration_file_frame, width=890)
        self.log_file_entry.insert(0, self.file_renamer_log)
        self.log_file_entry.grid(row=1, column=1, padx=10, pady=10)

        """
        Misc
        """
        # Select default frame
        self.select_frame_by_name(self.default_frame)

    # Callback for updating the scroll region when the inner frame is configured
    def on_frame_configure(self, event=None):
        # Reset the scroll region to encompass the inner frame
        self.file_renamer_canvas.configure(scrollregion=self.file_renamer_canvas.bbox("all"))

    # Callback for updating the scrollable frame's width when the canvas is configured
    def on_canvas_configure(self, event):
        # Set the scrollable frame's width to match the canvas
        canvas_width = event.width - self.file_renamer_scrollbar.winfo_width()
        self.file_renamer_canvas.itemconfig(self.file_renamer_scrollable_frame_window, width=canvas_width)

    # Callback function to handle logging state
    def handle_logging_activation(self, *args):
        # If logging is true, call the logging_setup function
        if self.activate_logging_var.get():
            try:
                self.logging_setup()
            except OSError as e:
                print(f"Logging failed. Error: {e}")
        else:
            # If logging is false, call the stop_logging function
            self.stop_logging()

    # Method called on exit for cleanup operations
    def cleanup_on_exit(self):
        # Stop logging if currently running
        if self.activate_logging_var.get():
            self.stop_logging()

    # Method to dynamically switch between frames based on the selected name
    def select_frame_by_name(self, frame_name):
        # Set button color for the selected button
        self.file_renamer_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "file_renamer_window" else "transparent")
        self.name_normalizer_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "name_normalizer_window" else "transparent")
        self.video_editor_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "video_editor_window" else "transparent")
        self.add_remove_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "add_remove_window" else "transparent")
        self.settings_button.configure(
            fg_color=("gray75", "gray25") if frame_name == "settings_window" else "transparent")

        # Show the selected frame and hide others, set the active frame_name
        if frame_name == "file_renamer_window":
            self.file_renamer_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.file_renamer_frame.grid_forget()
        if frame_name == "name_normalizer_window":
            self.name_normalizer_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.name_normalizer_frame.grid_forget()
        if frame_name == "video_editor_window":
            self.video_editor_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.video_editor_frame.grid_forget()
        if frame_name == "add_remove_window":
            self.add_remove_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.add_remove_frame.grid_forget()
        if frame_name == "settings_window":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
            self.frame_name = frame_name
        else:
            self.settings_frame.grid_forget()

    """
    Event handlers for button clicks to switch frames
    """

    def file_renamer_button_event(self):
        self.select_frame_by_name("file_renamer_window")

    def name_normalizer_button_event(self):
        self.select_frame_by_name("name_normalizer_window")

    def video_editor_button_event(self):
        self.select_frame_by_name("video_editor_window")

    def add_remove_button_event(self):
        self.select_frame_by_name("add_remove_window")

    def settings_button_event(self):
        self.select_frame_by_name("settings_window")

    def update_background_color(self):
        # Update canvas background color based on the current appearance mode
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            self.file_renamer_canvas.configure(bg='#dbdbdb')
        elif current_mode == "Dark":
            self.file_renamer_canvas.configure(bg='#2B2B2B')

    # Method for changing appearance mode (Light or Dark)
    def change_appearance_mode_event(self, new_appearance_mode):
        # Update background color when appearance mode changes
        ctk.set_appearance_mode(new_appearance_mode)
        self.update_background_color()

    # Method for changing UI scaling
    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    """
    Messaging
    """

    def update_text_color(self):
        # Update text color based on the current appearance mode
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Light":
            self.file_renamer_message_label.configure(text_color="#000000")
            self.name_normalizer_message_label.configure(text_color="#000000")
            self.video_editor_message_label.configure(text_color="#000000")
            self.add_remove_label.configure(text_color="#000000")
        elif current_mode == "Dark":
            self.file_renamer_message_label.configure(text_color="#FFFFFF")
            self.name_normalizer_message_label.configure(text_color="#FFFFFF")
            self.video_editor_message_label.configure(text_color="#FFFFFF")
            self.add_remove_label.configure(text_color="#FFFFFF")

    # Method to display messages with optional error formatting
    def show_message(self, message, error=False, frame_name=None):
        # Update text color when displaying a message
        self.update_text_color()

        # Display the message with optional error formatting on the actively selected frame
        if frame_name == "file_renamer_window":
            labels = [self.file_renamer_message_label]
        elif frame_name == "name_normalizer_window":
            labels = [self.name_normalizer_message_label]
        elif frame_name == "video_editor_window":
            labels = [self.video_editor_message_label]
        elif frame_name == "add_remove_window":
            labels = [self.add_remove_label]
        else:
            # Default to all frame labels if no frame name is passed
            labels = [self.file_renamer_message_label, self.name_normalizer_message_label,
                      self.video_editor_message_label, self.add_remove_label]

        # Truncate the message after x characters for GUI friendly formatting.
        truncated_message = f"{message[:115]}..." if len(message) > 115 else message

        for label in labels:
            if error:
                label.configure(text=truncated_message, text_color="#FF0000")  # Red text for errors
            else:
                label.configure(text=truncated_message)

    @staticmethod
    def validate_entry(var, default_value, desired_type):
        # Ensure the value is of the desired type
        current_value = var.get()

        if desired_type == int:
            # Check if the value is an integer
            if not current_value.isdigit():
                try:
                    # Try to convert the value to an integer
                    int_value = int(current_value)
                    var.set(int_value)
                except ValueError:
                    # If conversion to integer fails, set it to the default value
                    var.set(default_value)
        elif desired_type == float:
            # Check if the value is a float
            try:
                float_value = float(current_value)
                var.set(float_value)
            except ValueError:
                # If conversion to float fails, set it to the default value
                var.set(default_value)
        else:
            # If the desired type is neither int nor float, set it to the default value
            var.set(default_value)

    def log_and_show(self, message, create_messagebox=False, error=False, not_logging=False):
        """
        Method to check logging state, log if applicable, and show a messagebox.

        Parameters:
        - message: The message to be logged and displayed.
        - frame_name: The name of the frame where the message should be displayed.
        - create_messagebox: Boolean indicating whether to create and display a messagebox.
        - error: Boolean indicating whether the message is an error message.
        - not_logging: Boolean indicating whether to skip logging.
        """
        # Check logging state and log message if applicable
        if not not_logging and self.activate_logging_var.get():
            logging_function = logging.error if error else logging.info
            logging_function(message)

        # Check messagebox state and display messageboxes if applicable
        if self.show_messageboxes_var.get():
            messagebox_function = messagebox.showerror if error else messagebox.showinfo
            if create_messagebox:
                messagebox_function("Error" if error else "Info", message)
            else:
                # Display the message on the applicable frame if messageboxes are enabled but none were created
                self.show_message(message, error=error, frame_name=self.frame_name)
        else:
            # Display the message on the applicable frame if messageboxes are disabled
            self.show_message(message, error=error, frame_name=self.frame_name)

    def ask_confirmation(self, title, message):
        # Method to check logging state and show a messagebox.
        core.ask_confirmation(self, title, message)

    """
    Configuration
    """

    def load_configuration(self):
        # Load configuration settings using the core module
        return core.load_configuration(self)

    def logging_setup(self):
        # Setup logging
        core.logging_setup(self)

    def stop_logging(self):
        # Stop logging
        core.stop_logging(self)

    def redirect_output(self):
        # Redirect output (Fix for MoviePy overriding user's logging choice)
        core.redirect_output(self)

    """
    File Operations
    """

    def move_file_to_trash(self):
        # Move the selected file to the trash
        core.move_file_to_trash(self)

    def double_check_reminder(self, new_path):
        # Create double check reminders
        core.double_check_reminder(self, new_path)

    def load_last_used_file(self):
        # Load the last used file and update the GUI
        core.load_last_used_file(self)

    def send_to_module(self, destination):
        # Send the input to another module
        core.send_to_module(self, destination)

    def on_file_drop(self, event):
        # Handle the event when a file is dropped onto the application
        core.on_file_drop(self, event)

    def open_file(self, file_to_open):
        # Open a file using the default system program
        core.open_file(self, file_to_open)

    def add_to_queue(self, category):
        # Add a category to the processing queue
        core.add_to_queue(self, category)

    def update_file_display(self):
        # Update the display with the currently selected file
        core.update_file_display(self)

    def undo_last(self):
        # Undo the last operation and update the GUI
        core.undo_last(self)

    def clear_selection(self, frame_name):
        # Clear the selected file and update the GUI
        core.clear_selection(self, frame_name)

    def browse_artist_file(self):
        # Open a dialog to browse and select a file containing a line delimited list of artists
        core.browse_artist_file(self)

    def browse_artist_directory(self):
        # Open a dialog to browse and select a directory to use for the artist search
        core.browse_artist_directory(self)

    def browse_initial_directory(self):
        # Open a dialog to browse and select the initial directory when the user browses location
        core.browse_initial_directory(self)

    def browse_initial_output_directory(self):
        # Open a dialog to browse and select the initial directory when the user browses output location
        core.browse_initial_output_directory(self)

    def browse_double_check_reminder_directory(self):
        # Open a dialog to browse and select a directory to save the double check reminders in
        core.browse_double_check_reminder_directory(self)

    def browse_no_go_directory(self):
        # Open a dialog to browse and select a directory to save the NO-GO reminders in
        core.browse_no_go_directory(self)

    def browse_input(self):
        # Open a file dialog to browse and select a file
        core.browse_input(self)

    def browse_output_directory(self):
        # Open a dialog to browse and select an output directory
        core.browse_output_directory(self)

    def suggest_output_directory(self):
        # Suggest an output directory matching an artist name
        return core.suggest_output_directory(self)

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

    def create_category_button(self, category):
        return core.create_category_button(self, category)

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

    """
    Name Normalizer
    """

    def remove_artist_duplicates_from_filename(self, file_name):
        # Remove duplicate artists from the filename
        return core.remove_artist_duplicates_from_filename(self, file_name)

    def preview_name(self, file_path):
        # Preview rename files
        return core.preview_name(self, file_path)

    def rename_and_move_file(self, file_path):
        # Rename files and move files to a specified directory
        core.rename_and_move_file(self, file_path)

    def process_name_normalizer(self, mode):
        # Perform various name normalization operations on certain files within a specified folder
        core.process_name_normalizer(self, mode)

    """
    Video Editor
    """

    def get_non_conflicting_filename(self, path):
        # Generate a non-conflicting filename
        return core.get_non_conflicting_filename(self, path)

    def remove_successful_line_from_file(self, file_path, line_to_remove):
        # Method to remove a successful line from a file.
        core.remove_successful_line_from_file(self, file_path, line_to_remove)

    def rotate_video(self, clip, rotation_angle):
        # Method to rotate a video clip by a specified angle.
        return core.rotate_video(self, clip, rotation_angle)

    def increase_volume(self, clip, increase_db):
        # Method to increase the volume of a video clip by a specified dB value.
        return core.increase_volume(self, clip, increase_db)

    def normalize_audio(self, clip, volume_multiplier):
        # Method to normalize the audio of a video clip by applying a volume multiplier.
        return core.normalize_audio(self, clip, volume_multiplier)

    def trim_video(self, clip, total_time):
        # Method to trim a video by a specified time value.
        return core.trim_video(self, clip, total_time)

    def process_video_edits(self):
        # Method to process video edits based on user inputs.
        core.process_video_edits(self)

    """
    add_remove_window
    """

    def add_artist_to_file(self):
        # Add artists to the artist file
        core.add_artist_to_file(self)

    def remove_artist_from_file(self):
        # Remove artists from the artist file
        core.remove_artist_from_file(self)

    def no_go_creation(self):
        # Create a NO-GO file
        core.no_go_creation(self)


if __name__ == "__main__":
    # Create an instance of the OCDFileRenamer application and start the main loop
    app = OCDFileRenamer()
    app.mainloop()
