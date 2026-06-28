import tkinter as tk
from tkinter import ttk, messagebox


class ResultScreen(tk.Frame):
    def __init__(self, parent, managers):
        super().__init__(parent)
        self.parent = parent
        self.answer_checker = managers["answer_checker"]
        self.text_manager = managers["text_manager"]
        self.theme_manager = managers.get("theme_manager")

        self.text = None
        self.questions = []
        self.quiz_result = None
        self.badge_images = {}

    def _load_badge_image(self, badge_id):
        import os
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

    def _init_managers(self):
        from progress_tracker import ProgressTracker
        from review_scheduler import ReviewScheduler
        from badge_manager import BadgeManager

        if not self.parent.managers.get("progress_tracker") and self.parent.current_user:
            self.parent.managers["progress_tracker"] = ProgressTracker(self.parent.current_user)
            self.parent.managers["review_scheduler"] = ReviewScheduler(self.parent.current_user)
            self.parent.managers["badge_manager"] = BadgeManager(self.parent.current_user, self.parent.managers["data_dir"])

        self.progress_tracker = self.parent.managers.get("progress_tracker")
        self.review_scheduler = self.parent.managers.get("review_scheduler")
        self.badge_manager = self.parent.managers.get("badge_manager")

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self, padding=10)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.title_label = ttk.Label(
            self.header_frame,
            text="Quiz Results / 测验结果",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(side=tk.LEFT)

        self.back_button = ttk.Button(
            self.header_frame,
            text="Back to Library / 返回文本库",
            command=self._go_back
        )
        self.back_button.pack(side=tk.RIGHT)

        self.result_frame = ttk.LabelFrame(self, text="Results Summary / 结果汇总", padding=20)
        self.result_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.result_frame.grid_columnconfigure(0, weight=1)

        self.score_frame = ttk.Frame(self.result_frame)
        self.score_frame.pack(fill=tk.X, pady=10)

        self.score_label = ttk.Label(self.score_frame, text="Score: 0%", font=("Arial", 24, "bold"))
        self.score_label.pack(side=tk.LEFT)

        self.stars_label = ttk.Label(self.score_frame, text="Stars: ★★★", font=("Arial", 24))
        self.stars_label.pack(side=tk.RIGHT)

        self.details_frame = ttk.Frame(self.result_frame)
        self.details_frame.pack(fill=tk.X, pady=10)

        self.correct_label = ttk.Label(self.details_frame, text="Correct: 0/0")
        self.correct_label.pack(side=tk.LEFT, padx=20)

        self.accuracy_label = ttk.Label(self.details_frame, text="Accuracy: 0%")
        self.accuracy_label.pack(side=tk.LEFT, padx=20)

        self.badges_frame = ttk.LabelFrame(self.result_frame, text="New Badges / 新徽章", padding=10)
        self.badges_frame.pack(fill=tk.X, pady=10)
        self.badges_inner_frame = ttk.Frame(self.badges_frame)
        self.badges_inner_frame.pack(fill=tk.X)

        self.questions_frame = ttk.LabelFrame(self.result_frame, text="Questions / 题目详情", padding=10)
        self.questions_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.questions_text = tk.Text(self.questions_frame, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED)
        self.questions_text.pack(fill=tk.BOTH, expand=True)

        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=2, column=0, sticky="ew", pady=10)

        self.retry_button = ttk.Button(
            self.action_frame,
            text="Retry / 再试一次",
            command=self._retry
        )
        self.retry_button.pack(side=tk.RIGHT, padx=5)

        self.home_button = ttk.Button(
            self.action_frame,
            text="Home / 首页",
            command=self._go_back
        )
        self.home_button.pack(side=tk.RIGHT)

    def update(self, **kwargs):
        self._init_managers()
        if not hasattr(self, 'result_frame'):
            self._setup_ui()

        self.text = kwargs.get("text")
        self.questions = kwargs.get("questions", [])

        correct_count, total_count, accuracy, stars = self.answer_checker.calculate_score(self.questions)

        mistakes = []
        for i, question in enumerate(self.questions, 1):
            if not question.is_correct:
                mistakes.append(f"Q{i}: Expected '{question.correct_answer}', got '{question.user_answer}'")

        difficulty = kwargs.get("difficulty", 1)
        self.quiz_result = self.progress_tracker.record_quiz(
            self.text.text_id, accuracy, correct_count, total_count, mistakes, stars, difficulty
        )
        self.review_scheduler.update_after_quiz(self.text.text_id, accuracy)

        newly_unlocked = self.badge_manager.check_badges()

        self.score_label.config(text=f"Score: {accuracy}%")
        self.stars_label.config(text=f"Stars: {'★' * stars}")
        self.correct_label.config(text=f"Correct: {correct_count}/{total_count}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy}%")

        for widget in self.badges_inner_frame.winfo_children():
            widget.destroy()

        if newly_unlocked:
            self.badge_images = {}
            for badge in newly_unlocked:
                img = self._load_badge_image(badge.badge_id)
                badge_item = ttk.Frame(self.badges_inner_frame, padding=5)
                badge_item.pack(side=tk.LEFT)
                if img:
                    self.badge_images[badge.badge_id] = img
                    ttk.Label(badge_item, image=img).pack()
                else:
                    ttk.Label(badge_item, text="✓", font=("Arial", 20)).pack()
                ttk.Label(badge_item, text=badge.name, font=("Arial", 10)).pack()
        else:
            ttk.Label(self.badges_inner_frame, text="No new badges unlocked").pack(pady=5)

        self.questions_text.config(state=tk.NORMAL)
        self.questions_text.delete("1.0", tk.END)

        if self.questions:
            quiz_version = self.questions[0].prompt
            user_version = self.questions[0].prompt
            correct_version = self.questions[0].prompt

            for question in self.questions:
                blank_num = question.blank_number
                if self.text.language == "中文":
                    placeholder = f"【_{blank_num}_】"
                else:
                    placeholder = f"[__{blank_num}__]"
                
                user_answer = question.user_answer or ""
                correct_char = question.correct_answer

                if self.text.language == "中文":
                    if user_answer:
                        user_version = user_version.replace(placeholder, user_answer, 1)
                    else:
                        user_version = user_version.replace(placeholder, "_", 1)
                    correct_version = correct_version.replace(placeholder, correct_char, 1)
                else:
                    if user_answer:
                        user_version = user_version.replace(placeholder, user_answer, 1)
                    else:
                        user_version = user_version.replace(placeholder, "_" * len(correct_char), 1)
                    correct_version = correct_version.replace(placeholder, correct_char, 1)
        else:
            quiz_version = self.text.content
            user_version = self.text.content
            correct_version = self.text.content

        self.questions_text.insert(tk.END, "--- Quiz / 测验题目 ---\n")
        self.questions_text.insert(tk.END, f"{quiz_version}\n\n")

        self.questions_text.insert(tk.END, "--- Your Answer / 你的答案 ---\n")
        self.questions_text.insert(tk.END, f"{user_version}\n\n")

        self.questions_text.insert(tk.END, "--- Correct Answer / 正确答案 ---\n")
        self.questions_text.insert(tk.END, f"{correct_version}\n\n")

        self.questions_text.insert(tk.END, "--- Question Details / 题目详情 ---\n\n")

        all_correct = True
        for i, question in enumerate(self.questions, 1):
            blank_num = question.blank_number
            status = "✓ Correct" if question.is_correct else "✗ Wrong"
            if not question.is_correct:
                all_correct = False

            self.questions_text.insert(tk.END, f"Blank #{blank_num}:\n")
            self.questions_text.insert(tk.END, f"  Your answer: {question.user_answer or 'Not answered'}\n")
            self.questions_text.insert(tk.END, f"  Correct answer: {question.correct_answer}\n")
            self.questions_text.insert(tk.END, f"  Result: {status}\n\n")

        if all_correct:
            self.questions_text.insert(tk.END, "--- All answers correct! / 全部回答正确！ ---\n")

        self.questions_text.config(state=tk.DISABLED)

        self.parent.managers["user_manager"].save_profile(self.parent.current_user)

        self._export_quiz_report()

        theme_manager = kwargs.get("theme_manager")
        if theme_manager:
            theme_manager.apply_theme_to_tk_widget(self.questions_text, "text")
            if theme_manager not in getattr(self, '_theme_callbacks', []):
                theme_manager.register_callback(self._on_theme_change)
                self._theme_callbacks = [theme_manager]

    def _on_theme_change(self, colors):
        self.questions_text.config(bg=colors["text"], fg=colors["text_fg"], insertbackground=colors["fg"])

    def _export_quiz_report(self):
        from report_exporter import ReportExporter

        if not self.parent.managers.get("report_exporter"):
            self.parent.managers["report_exporter"] = ReportExporter(
                self.parent.current_user,
                self.text_manager,
                self.parent.managers["data_dir"]
            )

        filepath = self.parent.managers["report_exporter"].export_quiz_report(
            self.quiz_result, self.questions
        )
        print(f"Quiz report exported to: {filepath}")

    def _retry(self):
        self.parent.show_screen("quiz", text=self.text)

    def _go_back(self):
        self.parent.show_screen("library")