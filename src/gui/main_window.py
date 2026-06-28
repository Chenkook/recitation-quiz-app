import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    def __init__(self, managers):
        super().__init__()
        self.managers = managers
        self.screens = {}
        self.current_screen = None
        self.theme_manager = None

        self.title("Intelligent Recitation Quiz System")
        self.geometry("800x600")
        self.minsize(600, 450)

        if managers:
            self.set_managers(managers)

    def set_managers(self, managers):
        self.managers = managers
        self.theme_manager = managers.get("theme_manager")
        self._create_screens()
        self._create_theme_toggle()

    def _create_screens(self):
        from .welcome import WelcomeScreen
        from .library import LibraryScreen
        from .quiz_screen import QuizScreen
        from .result import ResultScreen
        from .profile import ProfileScreen
        from .badge_screen import BadgeScreen
        from .review_screen import ReviewScreen

        self.screens["welcome"] = WelcomeScreen(self, self.managers)
        self.screens["library"] = LibraryScreen(self, self.managers)
        self.screens["quiz"] = QuizScreen(self, self.managers)
        self.screens["result"] = ResultScreen(self, self.managers)
        self.screens["profile"] = ProfileScreen(self, self.managers)
        self.screens["badge"] = BadgeScreen(self, self.managers)
        self.screens["review"] = ReviewScreen(self, self.managers)

    def _create_theme_toggle(self):
        self.theme_toggle = ttk.Button(
            self,
            text="🌙 Night Mode",
            command=self._toggle_theme
        )
        self.theme_toggle.pack(side=tk.TOP, anchor=tk.E, padx=10, pady=5)

    def _toggle_theme(self):
        if self.theme_manager:
            self.theme_manager.toggle_theme()
            self.theme_toggle.config(text="☀️ Light Mode" if self.theme_manager.is_dark else "🌙 Night Mode")

    def show_screen(self, screen_name, **kwargs):
        if self.current_screen:
            self.current_screen.pack_forget()

        screen = self.screens.get(screen_name)
        if screen:
            kwargs["theme_manager"] = self.theme_manager
            screen.update(**kwargs)
            screen.pack(fill=tk.BOTH, expand=True)
            self.current_screen = screen

    def run(self):
        self.show_screen("welcome")
        self.mainloop()