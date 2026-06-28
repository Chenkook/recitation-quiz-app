import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.simpledialog
import os


class LibraryScreen(tk.Frame):
    def __init__(self, parent, managers):
        super().__init__(parent)
        self.parent = parent
        self.text_manager = managers["text_manager"]
        self.theme_manager = managers.get("theme_manager")

        self.selected_text = None
        self.text_stats = {}
        self._setup_ui()

    def _init_managers(self):
        from progress_tracker import ProgressTracker
        from review_scheduler import ReviewScheduler
        from badge_manager import BadgeManager
        from report_exporter import ReportExporter

        if not self.parent.managers.get("progress_tracker") and self.parent.current_user:
            self.parent.managers["progress_tracker"] = ProgressTracker(self.parent.current_user)
            self.parent.managers["review_scheduler"] = ReviewScheduler(self.parent.current_user)
            self.parent.managers["badge_manager"] = BadgeManager(self.parent.current_user, self.parent.managers.get("data_dir", "data"))
            self.parent.managers["report_exporter"] = ReportExporter(
                self.parent.current_user,
                self.text_manager,
                self.parent.managers.get("output_dir", "output")
            )

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self, padding=10)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.title_label = ttk.Label(
            self.header_frame,
            text="Text Library / 文本库",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(side=tk.LEFT)

        self.logout_button = ttk.Button(
            self.header_frame,
            text="Logout / 退出",
            command=self._logout
        )
        self.logout_button.pack(side=tk.RIGHT)

        self.profile_button = ttk.Button(
            self.header_frame,
            text="Profile / 档案",
            command=lambda: self.parent.show_screen("profile")
        )
        self.profile_button.pack(side=tk.RIGHT, padx=5)

        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.grid(row=1, column=0, sticky="nsew")

        self.list_frame = ttk.Frame(self.main_frame)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.text_tree = ttk.Treeview(self.list_frame, columns=("title", "count", "accuracy"), show="headings", height=15)
        self.text_tree.heading("title", text="Text / 文本", command=lambda: self._sort_tree("title"))
        self.text_tree.heading("count", text="Practice / 练习 ↑", command=lambda: self._sort_tree("count"))
        self.text_tree.heading("accuracy", text="Accuracy / 正确率", command=lambda: self._sort_tree("accuracy"))

        self.text_tree.column("title", width=300, stretch=True)
        self.text_tree.column("count", width=80, anchor="center")
        self.text_tree.column("accuracy", width=100, anchor="center")

        self.text_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.text_tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_tree.configure(yscrollcommand=self.scrollbar.set)

        self.text_tree.bind("<Double-1>", lambda e: self._select_text())

        self.sort_column = "count"
        self.sort_ascending = True

        self.detail_frame = ttk.LabelFrame(self.main_frame, text="Text Details / 文本详情", padding=10, width=350)
        self.detail_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self.detail_frame.pack_propagate(False)
        self.detail_frame.grid_rowconfigure(5, weight=1)

        self.detail_title = ttk.Label(self.detail_frame, text="Title: ", font=("Arial", 14, "bold"))
        self.detail_title.pack(anchor="w", pady=5)

        self.detail_language = ttk.Label(self.detail_frame, text="Language: ")
        self.detail_language.pack(anchor="w", pady=5)

        self.detail_category = ttk.Label(self.detail_frame, text="Category: ")
        self.detail_category.pack(anchor="w", pady=5)

        self.detail_difficulty = ttk.Label(self.detail_frame, text="Difficulty: ")
        self.detail_difficulty.pack(anchor="w", pady=5)

        self.detail_quiz_count = ttk.Label(self.detail_frame, text="Practice Count: ")
        self.detail_quiz_count.pack(anchor="w", pady=5)

        self.detail_accuracy = ttk.Label(self.detail_frame, text="Accuracy: ")
        self.detail_accuracy.pack(anchor="w", pady=5)

        self.detail_content = tk.Text(self.detail_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)
        self.detail_content.pack(fill=tk.BOTH, expand=True, pady=5)

        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=2, column=0, sticky="ew", pady=10)

        self.start_quiz_button = ttk.Button(
            self.action_frame,
            text="Start Quiz / 开始测验",
            command=self._start_quiz,
            state=tk.DISABLED
        )
        self.start_quiz_button.pack(side=tk.LEFT, padx=5)

        self.import_button = ttk.Button(
            self.action_frame,
            text="Import Text / 导入文本",
            command=self._import_text
        )
        self.import_button.pack(side=tk.LEFT, padx=5)

        self.review_button = ttk.Button(
            self.action_frame,
            text="Review / 复习",
            command=lambda: self.parent.show_screen("review")
        )
        self.review_button.pack(side=tk.LEFT, padx=5)

        self.badges_button = ttk.Button(
            self.action_frame,
            text="Badges / 徽章",
            command=lambda: self.parent.show_screen("badge")
        )
        self.badges_button.pack(side=tk.LEFT, padx=5)

    def update(self, **kwargs):
        self._init_managers()
        self._load_text_stats()
        self._refresh_text_list()

        theme_manager = kwargs.get("theme_manager")
        if theme_manager:
            theme_manager.apply_theme_to_tk_widget(self.detail_content, "text")
            if theme_manager not in getattr(self, '_theme_callbacks', []):
                theme_manager.register_callback(self._on_theme_change)
                self._theme_callbacks = [theme_manager]

    def _on_theme_change(self, colors):
        self.detail_content.config(bg=colors["text"], fg=colors["text_fg"], insertbackground=colors["fg"])

    def _load_text_stats(self):
        self.text_stats = {}
        if not self.parent.current_user:
            return

        import os
        import json

        stats_dir = os.path.join(self.parent.managers.get("output_dir", "output"), "stats")
        stats_file = os.path.join(stats_dir, f"text_stats_{self.parent.current_user.username}.json")

        if os.path.exists(stats_file):
            with open(stats_file, "r", encoding="utf-8") as f:
                self.text_stats = json.load(f)

    def _refresh_text_list(self):
        for item in self.text_tree.get_children():
            self.text_tree.delete(item)

        texts = self.text_manager.get_all_texts()

        if not texts:
            self.start_quiz_button.config(state=tk.DISABLED)
            return

        texts_with_stats = []
        for text in texts:
            stats = self.text_stats.get(text.text_id, {})
            quiz_count = stats.get("total_quizzes", 0)
            accuracy = stats.get("avg_accuracy", 0)
            title_display = f"{text.title} ({text.language}) - {text.category}"
            texts_with_stats.append({
                "text": text,
                "title": title_display,
                "count": quiz_count,
                "accuracy": accuracy
            })

        if self.sort_column == "title":
            texts_with_stats.sort(key=lambda x: x["title"], reverse=not self.sort_ascending)
        elif self.sort_column == "count":
            texts_with_stats.sort(key=lambda x: x["count"], reverse=not self.sort_ascending)
        elif self.sort_column == "accuracy":
            texts_with_stats.sort(key=lambda x: x["accuracy"], reverse=not self.sort_ascending)

        for item in texts_with_stats:
            text = item["text"]
            count_display = str(item["count"]) if item["count"] > 0 else "-"
            accuracy_display = f"{item['accuracy']}%" if item["accuracy"] > 0 else "-"

            self.text_tree.insert("", tk.END, values=(item["title"], count_display, accuracy_display), iid=text.text_id)

    def _sort_tree(self, column):
        if self.sort_column == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column
            self.sort_ascending = True

        arrow_up = " ↑"
        arrow_down = " ↓"
        arrow_none = ""

        self.text_tree.heading("title", text=f"Text / 文本{arrow_up if (self.sort_column == 'title' and self.sort_ascending) else arrow_down if (self.sort_column == 'title' and not self.sort_ascending) else arrow_none}", command=lambda: self._sort_tree("title"))
        self.text_tree.heading("count", text=f"Practice / 练习{arrow_up if (self.sort_column == 'count' and self.sort_ascending) else arrow_down if (self.sort_column == 'count' and not self.sort_ascending) else arrow_none}", command=lambda: self._sort_tree("count"))
        self.text_tree.heading("accuracy", text=f"Accuracy / 正确率{arrow_up if (self.sort_column == 'accuracy' and self.sort_ascending) else arrow_down if (self.sort_column == 'accuracy' and not self.sort_ascending) else arrow_none}", command=lambda: self._sort_tree("accuracy"))

        self._refresh_text_list()

    def _select_text(self):
        selection = self.text_tree.selection()
        if not selection:
            return

        text_id = selection[0]
        texts = self.text_manager.get_all_texts()
        for text in texts:
            if text.text_id == text_id:
                self.selected_text = text
                self._show_text_details()
                self.start_quiz_button.config(state=tk.NORMAL)
                break

    def _show_text_details(self):
        if not self.selected_text:
            return

        self.detail_title.config(text=f"Title: {self.selected_text.title}")
        self.detail_language.config(text=f"Language: {self.selected_text.language}")
        self.detail_category.config(text=f"Category: {self.selected_text.category}")
        self.detail_difficulty.config(text=f"Difficulty: {'★' * self.selected_text.difficulty}")

        stats = self.text_stats.get(self.selected_text.text_id, {})
        quiz_count = stats.get("total_quizzes", 0)
        accuracy = stats.get("avg_accuracy", 0)

        if quiz_count > 0:
            self.detail_quiz_count.config(text=f"Practice Count / 练习次数: {quiz_count}")
            self.detail_accuracy.config(text=f"Accuracy / 正确率: {accuracy}%")
        else:
            self.detail_quiz_count.config(text=f"Practice Count / 练习次数: Not practiced yet")
            self.detail_accuracy.config(text=f"Accuracy / 正确率: N/A")

        self.detail_content.config(state=tk.NORMAL)
        self.detail_content.delete("1.0", tk.END)
        self.detail_content.insert(tk.END, self.selected_text.content)
        self.detail_content.config(state=tk.DISABLED)

    def _start_quiz(self):
        if not self.selected_text:
            messagebox.showwarning("Warning / 警告", "Please select a text first.\n请先选择一个文本。")
            return

        self.parent.show_screen("quiz", text=self.selected_text)

    def _import_text(self):
        user_text_dir = os.path.join(self.parent.managers.get("data_dir", "data"), "User Text")
        os.makedirs(user_text_dir, exist_ok=True)

        file_path = filedialog.askopenfilename(
            title="Select TXT File / 选择 TXT 文件",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialdir=user_text_dir
        )

        if not file_path:
            return

        title = tk.simpledialog.askstring("Input / 输入", "Enter text title / 输入文本标题:")
        if not title:
            return

        category = tk.simpledialog.askstring("Input / 输入", "Enter category / 输入分类:", initialvalue="Custom")
        if not category:
            category = "Custom"

        difficulty = tk.simpledialog.askinteger("Input / 输入", "Enter difficulty (1-3) / 输入难度:", minvalue=1, maxvalue=3)
        if difficulty is None:
            difficulty = 1

        new_text = self.text_manager.import_txt_file(file_path, title, category, difficulty)

        if new_text:
            messagebox.showinfo("Success / 成功", f"Text imported successfully!\n文本导入成功！\nTitle: {new_text.title}")
            self._refresh_text_list()
        else:
            messagebox.showerror("Error / 错误", "Failed to import text.\n导入失败。")

    def _logout(self):
        self.parent.current_user = None
        self.parent.show_screen("welcome")