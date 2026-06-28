import tkinter as tk
from tkinter import ttk, messagebox


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, managers):
        super().__init__(parent)
        self.parent = parent
        self.user_manager = managers["user_manager"]
        self.theme_manager = managers.get("theme_manager")

        self._setup_ui()

    def _setup_ui(self):
        self.container = ttk.Frame(self, padding=20)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(
            self.container,
            text="Intelligent Recitation Quiz System\n智能背诵测验系统",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=40)

        self.subtitle_label = ttk.Label(
            self.container,
            text="Start your learning journey!\n开启您的学习之旅！",
            font=("Arial", 14)
        )
        self.subtitle_label.pack(pady=20)

        self.mode_frame = ttk.LabelFrame(self.container, text="Select Mode / 选择模式", padding=20)
        self.mode_frame.pack(pady=20, fill=tk.X)

        self.create_button = ttk.Button(
            self.mode_frame,
            text="Create New Profile / 创建新档案",
            command=self._create_profile,
            width=30
        )
        self.create_button.pack(pady=10)

        self.load_button = ttk.Button(
            self.mode_frame,
            text="Load Existing Profile / 读取已有档案",
            command=self._load_profile,
            width=30
        )
        self.load_button.pack(pady=10)

        self.username_var = tk.StringVar()
        self.username_label = ttk.Label(self.container, text="Username / 用户名:")
        self.username_entry = ttk.Entry(self.container, textvariable=self.username_var, width=30)

        self.profile_listbox = tk.Listbox(self.container, height=5, width=40)

    def update(self, **kwargs):
        self.username_var.set("")
        if hasattr(self, 'username_label'):
            self.username_label.pack_forget()
            self.username_entry.pack_forget()
            self.profile_listbox.pack_forget()

        if hasattr(self, 'submit_btn'):
            self.submit_btn.destroy()
            delattr(self, 'submit_btn')

        if hasattr(self, 'load_btn'):
            self.load_btn.destroy()
            delattr(self, 'load_btn')

        theme_manager = kwargs.get("theme_manager")
        if theme_manager:
            theme_manager.apply_theme_to_tk_widget(self.profile_listbox, "listbox")
            if theme_manager not in getattr(self, '_theme_callbacks', []):
                theme_manager.register_callback(self._on_theme_change)
                self._theme_callbacks = [theme_manager]

    def _on_theme_change(self, colors):
        self.profile_listbox.config(bg=colors["listbox"], fg=colors["listbox_fg"])

    def _create_profile(self):
        self.username_label.pack(pady=10)
        self.username_entry.pack(pady=5)
        self.profile_listbox.pack_forget()

        if hasattr(self, 'load_btn'):
            self.load_btn.destroy()
            delattr(self, 'load_btn')

        if hasattr(self, 'submit_btn'):
            self.submit_btn.destroy()
            delattr(self, 'submit_btn')

        self.username_entry.focus()
        self.username_entry.bind("<Return>", lambda e: self._submit_create())

        submit_btn = ttk.Button(
            self.container,
            text="Create / 创建",
            command=self._submit_create
        )
        submit_btn.pack(pady=10)
        self.submit_btn = submit_btn

    def _submit_create(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("Warning / 警告", "Please enter a username.\n请输入用户名。")
            return

        user = self.user_manager.create_profile(username)
        if user:
            self.parent.current_user = user
            self.parent.managers["progress_tracker"] = None
            self.parent.managers["review_scheduler"] = None
            self.parent.managers["badge_manager"] = None
            self.parent.managers["report_exporter"] = None
            messagebox.showinfo("Success / 成功", f"Profile created!\nWelcome, {username}!\n档案创建成功！")
            self.parent.show_screen("library")
        else:
            messagebox.showerror("Error / 错误", "Username already exists.\n用户名已存在。")

    def _load_profile(self):
        users = self.user_manager.get_all_usernames()

        if not users:
            messagebox.showinfo("Info / 信息", "No profiles found.\nPlease create a new profile.\n没有找到档案，请创建新档案。")
            self._create_profile()
            return

        self.username_label.pack_forget()
        self.username_entry.pack_forget()

        if hasattr(self, 'submit_btn'):
            self.submit_btn.destroy()
            delattr(self, 'submit_btn')

        if hasattr(self, 'load_btn'):
            self.load_btn.destroy()
            delattr(self, 'load_btn')

        self.profile_listbox.delete(0, tk.END)
        for user in users:
            self.profile_listbox.insert(tk.END, user)

        self.profile_listbox.pack(pady=10)

        load_btn = ttk.Button(
            self.container,
            text="Load / 读取",
            command=self._submit_load
        )
        load_btn.pack(pady=10)
        self.load_btn = load_btn

        self.profile_listbox.bind("<Double-1>", lambda e: self._submit_load())

    def _submit_load(self):
        selection = self.profile_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning / 警告", "Please select a profile.\n请选择一个档案。")
            return

        username = self.profile_listbox.get(selection[0])
        user = self.user_manager.load_profile(username)

        if user:
            self.parent.current_user = user
            self.parent.managers["progress_tracker"] = None
            self.parent.managers["review_scheduler"] = None
            self.parent.managers["badge_manager"] = None
            self.parent.managers["report_exporter"] = None
            messagebox.showinfo("Success / 成功", f"Welcome back, {username}!\n欢迎回来！")
            self.parent.show_screen("library")
        else:
            messagebox.showerror("Error / 错误", "Failed to load profile.\n读取档案失败。")