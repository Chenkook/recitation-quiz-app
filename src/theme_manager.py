import tkinter as tk
from tkinter import ttk


class ThemeManager:
    LIGHT_COLORS = {
        "bg": "#ffffff",
        "fg": "#000000",
        "frame": "#f5f5f5",
        "text": "#ffffff",
        "text_fg": "#000000",
        "button": "#e0e0e0",
        "button_fg": "#000000",
        "entry": "#ffffff",
        "entry_fg": "#000000",
        "listbox": "#ffffff",
        "listbox_fg": "#000000",
        "highlight": "#4a90d9",
        "success": "#2ecc71",
        "error": "#e74c3c",
        "warning": "#f39c12"
    }

    DARK_COLORS = {
        "bg": "#1a1a2e",
        "fg": "#e0e0e0",
        "frame": "#16213e",
        "text": "#0f3460",
        "text_fg": "#e0e0e0",
        "button": "#533483",
        "button_active": "#7a5fa0",
        "button_fg": "#e0e0e0",
        "entry": "#0f3460",
        "entry_fg": "#e0e0e0",
        "listbox": "#0f3460",
        "listbox_fg": "#e0e0e0",
        "highlight": "#7c9aff",
        "success": "#50fa7b",
        "error": "#ff5555",
        "warning": "#ffb86c"
    }

    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(root)
        self.is_dark = False
        self.callbacks = []
        self._setup_styles()

    def _setup_styles(self):
        self.style.theme_use("clam")

        self.style.configure(".",
                            background=self.LIGHT_COLORS["bg"],
                            foreground=self.LIGHT_COLORS["fg"],
                            fieldbackground=self.LIGHT_COLORS["entry"])

        self.style.configure("TFrame", background=self.LIGHT_COLORS["frame"])
        self.style.configure("TLabel", background=self.LIGHT_COLORS["frame"], foreground=self.LIGHT_COLORS["fg"])
        self.style.configure("TButton", background=self.LIGHT_COLORS["button"], foreground=self.LIGHT_COLORS["button_fg"])
        self.style.map("TButton",
                       background=[("active", "#d0d0d0")],
                       foreground=[("active", "#000000")])
        self.style.configure("TEntry", fieldbackground=self.LIGHT_COLORS["entry"], foreground=self.LIGHT_COLORS["entry_fg"])
        self.style.configure("TRadiobutton", background=self.LIGHT_COLORS["frame"], foreground=self.LIGHT_COLORS["fg"])
        self.style.configure("TLabelframe", background=self.LIGHT_COLORS["frame"])
        self.style.configure("TLabelframe.Label", background=self.LIGHT_COLORS["frame"], foreground=self.LIGHT_COLORS["fg"])
        self.style.configure("TScrollbar", background=self.LIGHT_COLORS["button"])
        self.style.configure("Treeview",
                             background=self.LIGHT_COLORS["listbox"],
                             foreground=self.LIGHT_COLORS["listbox_fg"],
                             fieldbackground=self.LIGHT_COLORS["listbox"])
        self.style.configure("Treeview.Heading",
                             background=self.LIGHT_COLORS["button"],
                             foreground=self.LIGHT_COLORS["button_fg"])

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        colors = self.DARK_COLORS if self.is_dark else self.LIGHT_COLORS

        self.style.configure(".",
                            background=colors["bg"],
                            foreground=colors["fg"],
                            fieldbackground=colors["entry"])

        self.style.configure("TFrame", background=colors["frame"])
        self.style.configure("TLabel", background=colors["frame"], foreground=colors["fg"])
        self.style.configure("TButton", background=colors["button"], foreground=colors["button_fg"])
        if self.is_dark:
            self.style.map("TButton",
                           background=[("active", colors["button_active"])],
                           foreground=[("active", colors["button_fg"])])
        else:
            self.style.map("TButton",
                           background=[("active", "#d0d0d0")],
                           foreground=[("active", "#000000")])
        self.style.configure("TEntry", fieldbackground=colors["entry"], foreground=colors["entry_fg"])
        self.style.configure("TRadiobutton", background=colors["frame"], foreground=colors["fg"])
        self.style.configure("TLabelframe", background=colors["frame"])
        self.style.configure("TLabelframe.Label", background=colors["frame"], foreground=colors["fg"])
        self.style.configure("TScrollbar", background=colors["button"])
        self.style.configure("Treeview",
                             background=colors["listbox"],
                             foreground=colors["listbox_fg"],
                             fieldbackground=colors["listbox"])
        self.style.configure("Treeview.Heading",
                             background=colors["button"],
                             foreground=colors["button_fg"])

        self.root.config(bg=colors["bg"])

        for callback in self.callbacks:
            callback(colors)

    def register_callback(self, callback):
        self.callbacks.append(callback)

    def get_color(self, color_name):
        colors = self.DARK_COLORS if self.is_dark else self.LIGHT_COLORS
        return colors.get(color_name, "#ffffff")

    def apply_theme_to_tk_widget(self, widget, widget_type):
        colors = self.DARK_COLORS if self.is_dark else self.LIGHT_COLORS
        if widget_type == "text":
            widget.config(bg=colors["text"], fg=colors["text_fg"], insertbackground=colors["fg"])
        elif widget_type == "listbox":
            widget.config(bg=colors["listbox"], fg=colors["listbox_fg"])
        elif widget_type == "canvas":
            widget.config(bg=colors["frame"])