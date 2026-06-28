import tkinter as tk
from tkinter import ttk, messagebox


class QuizScreen(tk.Frame):
    def __init__(self, parent, managers):
        super().__init__(parent)
        self.parent = parent
        self.quiz_generator = managers["quiz_generator"]
        self.answer_checker = managers["answer_checker"]
        self.text_manager = managers["text_manager"]
        self.theme_manager = managers.get("theme_manager")

        self.text = None
        self.questions = []
        self.current_question = 0
        self.user_answers = []
        self.difficulty = 1
        self.original_prompt = ""

        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.header_frame = ttk.Frame(self, padding=10)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        self.back_button = ttk.Button(
            self.header_frame,
            text="Back / 返回",
            command=self._go_back
        )
        self.back_button.pack(side=tk.LEFT)

        self.title_label = ttk.Label(
            self.header_frame,
            text="Quiz / 测验",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=20)

        self.progress_label = ttk.Label(self.header_frame, text="Progress: 0/0")
        self.progress_label.pack(side=tk.RIGHT)

        self.difficulty_frame = ttk.LabelFrame(self, text="Select Difficulty / 选择难度", padding=10)
        self.difficulty_frame.grid(row=1, column=0, sticky="ew", pady=10)

        self.difficulty_var = tk.IntVar(value=1)
        self.easy_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text="Easy / 简单 (20% blanks)",
            variable=self.difficulty_var,
            value=1
        )
        self.easy_radio.pack(side=tk.LEFT, padx=20)

        self.medium_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text="Medium / 中等 (40% blanks)",
            variable=self.difficulty_var,
            value=2
        )
        self.medium_radio.pack(side=tk.LEFT, padx=20)

        self.hard_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text="Hard / 困难 (60% blanks)",
            variable=self.difficulty_var,
            value=3
        )
        self.hard_radio.pack(side=tk.LEFT, padx=20)

        self.quiz_frame = ttk.LabelFrame(self, text="Question / 题目", padding=20)
        self.quiz_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        self.quiz_frame.grid_columnconfigure(0, weight=1)
        self.quiz_frame.grid_rowconfigure(1, weight=1)

        self.question_num_label = ttk.Label(self.quiz_frame, text="Question 1", font=("Arial", 14, "bold"))
        self.question_num_label.grid(row=0, column=0, sticky="w")

        self.prompt_text = tk.Text(self.quiz_frame, wrap=tk.WORD, height=8, font=("Arial", 14), state=tk.DISABLED)
        self.prompt_text.grid(row=1, column=0, sticky="nsew", pady=10)

        self.answer_frame = ttk.Frame(self.quiz_frame)
        self.answer_frame.grid(row=2, column=0, sticky="ew")

        self.answer_label = ttk.Label(self.answer_frame, text="Your Answer / 你的答案:")
        self.answer_label.pack(side=tk.LEFT)

        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(self.answer_frame, textvariable=self.answer_var, width=50, font=("Arial", 14))
        self.answer_entry.pack(side=tk.LEFT, padx=10)
        self.answer_entry.bind("<Return>", lambda e: self._submit_answer())

        self.action_frame = ttk.Frame(self)
        self.action_frame.grid(row=3, column=0, sticky="ew", pady=10)

        self.submit_button = ttk.Button(
            self.action_frame,
            text="Submit / 提交",
            command=self._submit_answer
        )
        self.submit_button.pack(side=tk.RIGHT)

        self.skip_button = ttk.Button(
            self.action_frame,
            text="Skip / 跳过",
            command=self._skip_question
        )
        self.skip_button.pack(side=tk.RIGHT, padx=5)

        self.start_button = ttk.Button(
            self.action_frame,
            text="Start Quiz / 开始测验",
            command=self._start_quiz
        )

    def update(self, **kwargs):
        self.text = kwargs.get("text")
        self.current_question = 0
        self.user_answers = []
        self.difficulty_var.set(1)

        self.title_label.config(text=f"Quiz: {self.text.title}")
        self.progress_label.config(text="Progress: 0/0")

        self.start_button.pack(side=tk.RIGHT, padx=5)
        self.submit_button.pack_forget()
        self.skip_button.pack_forget()

        self.easy_radio.config(state=tk.NORMAL)
        self.medium_radio.config(state=tk.NORMAL)
        self.hard_radio.config(state=tk.NORMAL)

        self.prompt_text.config(state=tk.NORMAL)
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert(tk.END, f"Ready to start quiz for:\n{self.text.title}\n\nSelect difficulty and click 'Start Quiz'.")
        self.prompt_text.config(state=tk.DISABLED)

        self.answer_var.set("")
        self.answer_entry.config(state=tk.DISABLED)

        theme_manager = kwargs.get("theme_manager")
        if theme_manager:
            theme_manager.apply_theme_to_tk_widget(self.prompt_text, "text")
            if theme_manager not in getattr(self, '_theme_callbacks', []):
                theme_manager.register_callback(self._on_theme_change)
                self._theme_callbacks = [theme_manager]

    def _on_theme_change(self, colors):
        self.prompt_text.config(bg=colors["text"], fg=colors["text_fg"], insertbackground=colors["fg"])

    def _start_quiz(self):
        self.difficulty = self.difficulty_var.get()
        self.questions = self.quiz_generator.generate_quiz(self.text, self.difficulty)

        if not self.questions:
            messagebox.showerror("Error / 错误", "Could not generate quiz.\n无法生成测验。")
            return

        self.start_button.pack_forget()
        self.submit_button.pack(side=tk.RIGHT)
        self.skip_button.pack(side=tk.RIGHT, padx=5)
        self.answer_entry.config(state=tk.NORMAL)

        self.easy_radio.config(state=tk.DISABLED)
        self.medium_radio.config(state=tk.DISABLED)
        self.hard_radio.config(state=tk.DISABLED)

        self._show_question()

    def _show_question(self):
        if self.current_question >= len(self.questions):
            self._finish_quiz()
            return

        question = self.questions[self.current_question]

        current_blank_num = question.blank_number
        total_blanks = question.total_blanks

        display_prompt = question.prompt

        for i in range(self.current_question):
            prev_question = self.questions[i]
            prev_blank_num = prev_question.blank_number
            prev_answer = self.user_answers[i] if i < len(self.user_answers) else ""
            
            if self.text.language == "中文":
                placeholder = f"【_{prev_blank_num}_】"
                if prev_answer:
                    display_prompt = display_prompt.replace(placeholder, prev_answer, 1)
            else:
                placeholder = f"[__{prev_blank_num}__]"
                if prev_answer:
                    display_prompt = display_prompt.replace(placeholder, prev_answer, 1)

        self.question_num_label.config(text=f"Question {self.current_question + 1}/{len(self.questions)}")
        self.progress_label.config(text=f"Progress: {self.current_question}/{len(self.questions)}")

        self.prompt_text.config(state=tk.NORMAL)
        self.prompt_text.delete("1.0", tk.END)
        self.prompt_text.insert(tk.END, display_prompt)
        self.prompt_text.config(state=tk.DISABLED)

        if self.text.language == "中文":
            self.answer_label.config(text=f"填写第 {current_blank_num} 个空:")
        else:
            self.answer_label.config(text=f"Fill blank #{current_blank_num}:")

        self.answer_var.set("")
        self.answer_entry.focus()

    def _submit_answer(self):
        if self.current_question >= len(self.questions):
            return

        answer = self.answer_var.get().strip()

        if not answer:
            messagebox.showwarning("Warning / 警告", "请输入答案。\nPlease enter an answer.")
            return

        if self.text.language == "中文":
            if len(answer) != 1:
                messagebox.showwarning("Warning / 警告", f"单字模式：请输入恰好一个汉字。\nSingle character mode: Please enter exactly 1 character.\n你输入了: {answer}")
                self.answer_var.set("")
                self.answer_entry.focus()
                return
            if not '\u4e00' <= answer <= '\u9fff':
                messagebox.showwarning("Warning / 警告", f"单字模式：请输入一个汉字。\nSingle character mode: Please enter a Chinese character.\n你输入了: {answer}")
                self.answer_var.set("")
                self.answer_entry.focus()
                return
        else:
            if " " in answer:
                messagebox.showwarning("Warning / 警告", f"单单词模式：请输入恰好一个单词。\nSingle word mode: Please enter exactly 1 word.\nYou entered: {answer}")
                self.answer_var.set("")
                self.answer_entry.focus()
                return
            if not answer.replace("'", "").isalpha():
                messagebox.showwarning("Warning / 警告", f"单单词模式：请输入有效的英文单词。\nSingle word mode: Please enter a valid English word.\nYou entered: {answer}")
                self.answer_var.set("")
                self.answer_entry.focus()
                return

        self.user_answers.append(answer)

        self.current_question += 1
        self._show_question()

    def _skip_question(self):
        self.user_answers.append("")
        self.current_question += 1
        self._show_question()

    def _finish_quiz(self):
        for i, question in enumerate(self.questions):
            user_answer = self.user_answers[i] if i < len(self.user_answers) else ""
            question.user_answer = user_answer
            question.is_correct = self.answer_checker.check_answer(user_answer, question.correct_answer, self.text.language)

        self.parent.show_screen("result", text=self.text, questions=self.questions, difficulty=self.difficulty)

    def _go_back(self):
        if messagebox.askyesno("Confirm / 确认", "Are you sure you want to quit the quiz?\nProgress will be lost.\n确定要退出测验吗？进度将丢失。"):
            self.parent.show_screen("library")