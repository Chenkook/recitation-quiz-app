import tkinter as tk
from tkinter import ttk
import os


class BadgeScreen(tk.Frame):
    def __init__(self, parent, managers):
        super().__init__(parent)
        self.parent = parent
        self.theme_manager = managers.get("theme_manager")
        self.badge_images = {}

        self._setup_ui()

    def _init_managers(self):
        from badge_manager import BadgeManager

        if not self.parent.managers.get("badge_manager") and self.parent.current_user:
            self.parent.managers["badge_manager"] = BadgeManager(self.parent.current_user, self.parent.managers["data_dir"])

        self.badge_manager = self.parent.managers.get("badge_manager")

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self, padding=10)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.title_label = ttk.Label(
            self.header_frame,
            text="Badges / 徽章",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(side=tk.LEFT)

        self.back_button = ttk.Button(
            self.header_frame,
            text="Back / 返回",
            command=self._go_back
        )
        self.back_button.pack(side=tk.RIGHT)

        self.badge_frame = ttk.LabelFrame(self, text="All Badges / 所有徽章", padding=20)
        self.badge_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.badge_frame.grid_columnconfigure(0, weight=1)
        self.badge_frame.grid_rowconfigure(0, weight=1)

        self.badge_canvas = tk.Canvas(self.badge_frame)
        self.badge_scrollbar = ttk.Scrollbar(self.badge_frame, orient=tk.VERTICAL, command=self.badge_canvas.yview)
        self.badge_inner_frame = ttk.Frame(self.badge_canvas)
        self.badge_inner_frame.bind("<Configure>", lambda e: self.badge_canvas.configure(scrollregion=self.badge_canvas.bbox("all")))
        self.badge_canvas.create_window((0, 0), window=self.badge_inner_frame, anchor="nw")
        self.badge_canvas.configure(yscrollcommand=self.badge_scrollbar.set)
        self.badge_canvas.grid(row=0, column=0, sticky="nsew")
        self.badge_scrollbar.grid(row=0, column=1, sticky="ns")

        self.next_badge_frame = ttk.LabelFrame(self, text="Next Badge / 下一个徽章", padding=20)
        self.next_badge_frame.grid(row=2, column=0, sticky="ew", pady=10)

        self.next_badge_label = ttk.Label(self.next_badge_frame, text="", font=("Arial", 14))
        self.next_badge_label.pack()

        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=3, column=0, sticky="ew", pady=10)

        self.export_button = ttk.Button(
            self.action_frame,
            text="Export Certificate / 导出证书",
            command=self._export_certificate
        )
        self.export_button.pack(side=tk.RIGHT)

    def _load_badge_image(self, badge_id):
        data_dir = self.parent.managers.get("data_dir", "data")
        badge_images_dir = os.path.join(data_dir, "badges")
        possible_names = [
            f"{badge_id}.png",
            f"{badge_id.capitalize()}.png",
            f"{badge_id.replace('_', ' ')}.png",
            f"{badge_id.replace('_', '').lower()}.png",
            f"{badge_id.replace('_', '').capitalize()}.png"
        ]
        for name in possible_names:
            filepath = os.path.join(badge_images_dir, name)
            if os.path.exists(filepath):
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(filepath)
                    img = img.resize((64, 64), Image.LANCZOS)
                    return ImageTk.PhotoImage(img)
                except:
                    return None
        return None

    def update(self, **kwargs):
        self._init_managers()

        for widget in self.badge_inner_frame.winfo_children():
            widget.destroy()

        all_badges = self.badge_manager.get_all_badges()
        unlocked_count = 0

        self.badge_images = {}

        for badge in all_badges:
            is_unlocked = self.badge_manager.is_badge_unlocked(badge.badge_id)
            if is_unlocked:
                unlocked_count += 1

            badge_item = ttk.Frame(self.badge_inner_frame, padding=5)
            badge_item.pack(fill=tk.X, pady=2)

            left_frame = ttk.Frame(badge_item)
            left_frame.pack(side=tk.LEFT)

            img = self._load_badge_image(badge.badge_id)
            if img:
                self.badge_images[badge.badge_id] = img
                ttk.Label(left_frame, image=img).pack()
            else:
                status_icon = "✓" if is_unlocked else "○"
                ttk.Label(left_frame, text=status_icon, font=("Arial", 20)).pack()

            right_frame = ttk.Frame(badge_item)
            right_frame.pack(side=tk.LEFT, padx=10)

            name_label = ttk.Label(right_frame, text=badge.name, font=("Arial", 12, "bold" if is_unlocked else ""))
            name_label.pack(anchor="w")

            condition_label = ttk.Label(right_frame, text=f"Condition: {badge.condition}", font=("Arial", 10))
            condition_label.pack(anchor="w")

            if not is_unlocked:
                condition_label.config(foreground="#888888")
                name_label.config(foreground="#888888")

        self.title_label.config(text=f"Badges ({unlocked_count}/{len(all_badges)})")

        next_badge = self.badge_manager.get_next_badge()
        if next_badge:
            self.next_badge_label.config(text=f"Next badge to unlock: {next_badge.name}")
        else:
            self.next_badge_label.config(text="🎉 Congratulations! You've unlocked all badges!")

        theme_manager = kwargs.get("theme_manager")
        if theme_manager:
            theme_manager.apply_theme_to_tk_widget(self.badge_canvas, "canvas")
            if theme_manager not in getattr(self, '_theme_callbacks', []):
                theme_manager.register_callback(self._on_theme_change)
                self._theme_callbacks = [theme_manager]

    def _on_theme_change(self, colors):
        self.badge_canvas.config(bg=colors["frame"])

    def _export_certificate(self):
        from report_exporter import ReportExporter

        if not self.parent.managers.get("report_exporter"):
            self.parent.managers["report_exporter"] = ReportExporter(
                self.parent.current_user,
                self.parent.managers["text_manager"],
                self.parent.managers["output_dir"]
            )

        filepath = self.parent.managers["report_exporter"].export_badge_certificate()
        tk.messagebox.showinfo("Success / 成功", f"Certificate exported to:\n{filepath}")

    def _go_back(self):
        self.parent.show_screen("library")