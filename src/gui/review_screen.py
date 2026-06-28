import tkinter as tk
from tkinter import ttk, messagebox


class ReviewScreen(tk.Frame):
    def __init__(self, parent, managers):
        super().__init__(parent)
        self.parent = parent
        self.text_manager = managers["text_manager"]
        self.theme_manager = managers.get("theme_manager")

        self._setup_ui()

    def _init_managers(self):
        from review_scheduler import ReviewScheduler

        if not self.parent.managers.get("review_scheduler") and self.parent.current_user:
            self.parent.managers["review_scheduler"] = ReviewScheduler(self.parent.current_user)

        self.review_scheduler = self.parent.managers.get("review_scheduler")

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self, padding=10)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.title_label = ttk.Label(
            self.header_frame,
            text="Review / 复习",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(side=tk.LEFT)

        self.back_button = ttk.Button(
            self.header_frame,
            text="Back / 返回",
            command=self._go_back
        )
        self.back_button.pack(side=tk.RIGHT)

        self.review_frame = ttk.LabelFrame(self, text="Texts Due for Review / 需要复习的文本", padding=20)
        self.review_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.review_frame.grid_columnconfigure(0, weight=1)

        self.review_tree = ttk.Treeview(self.review_frame, columns=("title", "language", "last_practiced", "days_overdue"))
        self.review_tree.heading("#0", text="No.")
        self.review_tree.heading("title", text="Title / 标题")
        self.review_tree.heading("language", text="Language / 语言")
        self.review_tree.heading("last_practiced", text="Last Practiced / 上次练习")
        self.review_tree.heading("days_overdue", text="Days Overdue / 逾期天数")

        self.review_tree.column("#0", width=50)
        self.review_tree.column("title", width=200)
        self.review_tree.column("language", width=100)
        self.review_tree.column("last_practiced", width=150)
        self.review_tree.column("days_overdue", width=100)

        self.review_tree.pack(fill=tk.BOTH, expand=True)

        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=2, column=0, sticky="ew", pady=10)

        self.practice_button = ttk.Button(
            self.action_frame,
            text="Practice Selected / 练习选中文本",
            command=self._practice_selected,
            state=tk.DISABLED
        )
        self.practice_button.pack(side=tk.RIGHT)

        self.review_tree.bind("<<TreeviewSelect>>", self._on_select)

    def update(self, **kwargs):
        self._init_managers()
        for item in self.review_tree.get_children():
            self.review_tree.delete(item)

        due_reviews = self.review_scheduler.get_due_reviews()

        if not due_reviews:
            self.review_tree.insert("", tk.END, text="1", values=("No texts due for review", "-", "-", "-"))
            self.title_label.config(text="Review - No texts due")
            return

        self.title_label.config(text=f"Review - {len(due_reviews)} texts due")

        for i, review in enumerate(due_reviews, 1):
            text = self.text_manager.get_text_by_id(review["text_id"])
            title = text.title if text else review["text_id"]
            language = text.language if text else "-"
            last_practiced = review["last_practiced_date"].isoformat() if review["last_practiced_date"] else "-"
            days_overdue = review["days_overdue"]

            self.review_tree.insert("", tk.END, text=str(i), values=(title, language, last_practiced, days_overdue))

    def _on_select(self, event):
        selection = self.review_tree.selection()
        if selection:
            self.practice_button.config(state=tk.NORMAL)
        else:
            self.practice_button.config(state=tk.DISABLED)

    def _practice_selected(self):
        selection = self.review_tree.selection()
        if not selection:
            messagebox.showwarning("Warning / 警告", "Please select a text first.\n请先选择一个文本。")
            return

        item = self.review_tree.item(selection[0])
        title = item["values"][0]

        texts = self.text_manager.get_all_texts()
        selected_text = None
        for text in texts:
            if text.title == title:
                selected_text = text
                break

        if selected_text:
            self.parent.show_screen("quiz", text=selected_text)
        else:
            messagebox.showerror("Error / 错误", "Text not found.\n文本未找到。")

    def _go_back(self):
        self.parent.show_screen("library")