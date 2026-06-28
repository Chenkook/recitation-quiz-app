import tkinter as tk
from tkinter import ttk
import os


class ProfileScreen(tk.Frame):
    def __init__(self, parent, managers):
        super().__init__(parent)
        self.parent = parent
        self.text_manager = managers["text_manager"]
        self.theme_manager = managers.get("theme_manager")
        self.badge_images = {}

        self._setup_ui()

    def _init_managers(self):
        from progress_tracker import ProgressTracker

        if not self.parent.managers.get("progress_tracker") and self.parent.current_user:
            self.parent.managers["progress_tracker"] = ProgressTracker(self.parent.current_user)

        self.progress_tracker = self.parent.managers.get("progress_tracker")

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self, padding=10)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.title_label = ttk.Label(
            self.header_frame,
            text="User Profile / 用户档案",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(side=tk.LEFT)

        self.back_button = ttk.Button(
            self.header_frame,
            text="Back / 返回",
            command=self._go_back
        )
        self.back_button.pack(side=tk.RIGHT)

        self.content_frame = ttk.Frame(self, padding=20)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.username_frame = ttk.LabelFrame(self.content_frame, text="User Info / 用户信息", padding=20)
        self.username_frame.pack(fill=tk.X, pady=10)

        self.username_label = ttk.Label(self.username_frame, text="Username:", font=("Arial", 14))
        self.username_label.pack(anchor="w")

        self.username_value = ttk.Label(self.username_frame, text="", font=("Arial", 16, "bold"))
        self.username_value.pack(anchor="w", pady=5)

        self.stats_frame = ttk.LabelFrame(self.content_frame, text="Learning Statistics / 学习统计", padding=20)
        self.stats_frame.pack(fill=tk.X, pady=10)

        self.stats_labels = []
        stats_items = [
            ("Total Quizzes / 测验总数", "total_quizzes"),
            ("Total Questions / 题目总数", "total_questions"),
            ("Total Correct / 正确总数", "total_correct"),
            ("Average Accuracy / 平均正确率", "avg_accuracy"),
            ("Total Stars / 总星星", "total_stars"),
            ("Current Streak / 当前连续", "current_streak"),
            ("Longest Streak / 最长连续", "longest_streak")
        ]

        for label_text, key in stats_items:
            frame = ttk.Frame(self.stats_frame)
            frame.pack(fill=tk.X, pady=5)

            lbl = ttk.Label(frame, text=label_text, width=30)
            lbl.pack(side=tk.LEFT)

            val = ttk.Label(frame, text="0", font=("Arial", 12, "bold"))
            val.pack(side=tk.RIGHT)

            self.stats_labels.append((key, val))

        self.badges_frame = ttk.LabelFrame(self.content_frame, text="Unlocked Badges / 已解锁徽章", padding=20)
        self.badges_frame.pack(fill=tk.X, pady=10)
        self.badges_canvas = tk.Canvas(self.badges_frame)
        self.badges_scrollbar = ttk.Scrollbar(self.badges_frame, orient=tk.HORIZONTAL, command=self.badges_canvas.xview)
        self.badges_inner_frame = ttk.Frame(self.badges_canvas)
        self.badges_inner_frame.bind("<Configure>", lambda e: self.badges_canvas.configure(scrollregion=self.badges_canvas.bbox("all")))
        self.badges_canvas.create_window((0, 0), window=self.badges_inner_frame, anchor="nw")
        self.badges_canvas.configure(xscrollcommand=self.badges_scrollbar.set)
        self.badges_canvas.pack(fill=tk.X, pady=5)
        self.badges_scrollbar.pack(fill=tk.X)

        self.practiced_frame = ttk.LabelFrame(self.content_frame, text="Practiced Texts / 已练习文本", padding=20)
        self.practiced_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.practiced_listbox = tk.Listbox(self.practiced_frame, font=("Arial", 12))
        self.practiced_listbox.pack(fill=tk.BOTH, expand=True)

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
        user = self.parent.current_user
        stats = self.progress_tracker.get_total_stats()

        self.username_value.config(text=user.username)

        for key, label in self.stats_labels:
            if key == "avg_accuracy":
                label.config(text=f"{stats.get(key, 0)}%")
            elif key == "current_streak" or key == "longest_streak":
                label.config(text=f"{getattr(user, key, 0)} days")
            elif key == "total_quizzes":
                label.config(text=str(getattr(user, key, 0)))
            elif key == "total_stars":
                label.config(text=str(stats.get(key, 0)))
            else:
                label.config(text=str(stats.get(key, 0)))

        self.practiced_listbox.delete(0, tk.END)
        practiced_texts = self.progress_tracker.get_practiced_texts()

        if not practiced_texts:
            self.practiced_listbox.insert(tk.END, "No texts practiced yet")
        else:
            for text_id in practiced_texts:
                text = self.text_manager.get_text_by_id(text_id)
                if text:
                    self.practiced_listbox.insert(tk.END, text.title)
                else:
                    self.practiced_listbox.insert(tk.END, text_id)

        for widget in self.badges_inner_frame.winfo_children():
            widget.destroy()

        from badge_manager import BadgeManager
        if not self.parent.managers.get("badge_manager"):
            self.parent.managers["badge_manager"] = BadgeManager(self.parent.current_user, self.parent.managers["data_dir"])
        badge_manager = self.parent.managers["badge_manager"]

        unlocked_badges = badge_manager.get_unlocked_badges()
        if not unlocked_badges:
            ttk.Label(self.badges_inner_frame, text="No badges unlocked yet").pack(pady=5)
        else:
            self.badge_images = {}
            for badge in unlocked_badges:
                img = self._load_badge_image(badge.badge_id)
                badge_item = ttk.Frame(self.badges_inner_frame, padding=5)
                badge_item.pack(side=tk.LEFT)
                if img:
                    self.badge_images[badge.badge_id] = img
                    ttk.Label(badge_item, image=img).pack()
                else:
                    ttk.Label(badge_item, text=badge.name.split("/")[0].strip(), font=("Arial", 10)).pack()
                ttk.Label(badge_item, text=badge.name.split("/")[1].strip() if "/" in badge.name else "", font=("Arial", 8)).pack()

        theme_manager = kwargs.get("theme_manager")
        if theme_manager:
            theme_manager.apply_theme_to_tk_widget(self.practiced_listbox, "listbox")
            if theme_manager not in getattr(self, '_theme_callbacks', []):
                theme_manager.register_callback(self._on_theme_change)
                self._theme_callbacks = [theme_manager]

    def _on_theme_change(self, colors):
        self.practiced_listbox.config(bg=colors["listbox"], fg=colors["listbox_fg"])

    def _go_back(self):
        self.parent.show_screen("library")