import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from user_profile import UserProfileManager
from text_manager import TextManager
from quiz_generator import QuizGenerator
from answer_checker import AnswerChecker
from progress_tracker import ProgressTracker
from review_scheduler import ReviewScheduler
from badge_manager import BadgeManager
from report_exporter import ReportExporter


class RecitationQuizApp:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(base_dir, "data")
        self.output_dir = os.path.join(base_dir, "output")

        self.user_manager = UserProfileManager(self.data_dir)
        self.user_manager.update_existing_users_password("123456")
        self.text_manager = TextManager(self.data_dir)
        self.quiz_generator = QuizGenerator()
        self.answer_checker = AnswerChecker()

        self.current_user = None
        self.progress_tracker = None
        self.review_scheduler = None
        self.badge_manager = None
        self.report_exporter = None

    def run(self):
        self._print_welcome()
        self._handle_user_profile()

        if not self.current_user:
            print("\nGoodbye!")
            return

        self._init_managers()

        while True:
            self._print_main_menu()
            choice = input("Enter your choice / 输入选择: ").strip()

            if choice == "1":
                self._start_quiz()
            elif choice == "2":
                self._view_text_library()
            elif choice == "3":
                self._view_profile()
            elif choice == "4":
                self._view_badges()
            elif choice == "5":
                self._view_review()
            elif choice == "6":
                self._import_text()
            elif choice == "7":
                self._export_report()
            elif choice == "8":
                self._save_and_exit()
                break
            else:
                print("Invalid choice. Please try again. / 无效选择，请重试。")

    def _print_welcome(self):
        print("=" * 50)
        print("Intelligent Recitation Quiz System")
        print("智能背诵测验系统")
        print("=" * 50)

    def _handle_user_profile(self):
        existing_users = self.user_manager.get_all_usernames()

        print("\n1. Create new profile / 创建新档案")
        print("2. Load existing profile / 读取已有档案")

        while True:
            choice = input("Enter choice / 输入选择 (1-2): ").strip()
            if choice in ["1", "2"]:
                break
            print("Invalid choice. / 无效选择。")

        if choice == "1":
            while True:
                username = input("Enter username / 输入用户名: ").strip()
                if username:
                    break
                print("Username cannot be empty. / 用户名不能为空。")

            user = self.user_manager.create_profile(username)
            if user:
                self.current_user = user
                print(f"\nProfile created successfully! Welcome, {username}!")
                print(f"档案创建成功！欢迎，{username}！")
            else:
                print("\nUsername already exists. Please try another.")
                print("用户名已存在，请尝试其他用户名。")
                self._handle_user_profile()

        else:
            if not existing_users:
                print("\nNo existing profiles. Creating new profile.")
                print("没有已有档案，创建新档案。")
                self._handle_user_profile()
                return

            print("\nExisting profiles / 已有档案:")
            for i, user in enumerate(existing_users, 1):
                print(f"{i}. {user}")

            while True:
                try:
                    idx = int(input("Enter profile number / 输入档案序号: ").strip()) - 1
                    if 0 <= idx < len(existing_users):
                        username = existing_users[idx]
                        self.current_user = self.user_manager.load_profile(username)
                        print(f"\nWelcome back, {username}!")
                        print(f"欢迎回来，{username}！")
                        break
                    else:
                        print("Invalid number. / 无效序号。")
                except ValueError:
                    print("Please enter a number. / 请输入数字。")

    def _init_managers(self):
        self.progress_tracker = ProgressTracker(self.current_user)
        self.review_scheduler = ReviewScheduler(self.current_user)
        self.badge_manager = BadgeManager(self.current_user, self.data_dir)
        self.report_exporter = ReportExporter(self.current_user, self.text_manager, self.output_dir)

    def _print_main_menu(self):
        print("\n" + "=" * 50)
        print(f"Welcome, {self.current_user.username}!")
        print(f"欢迎，{self.current_user.username}！")
        stars_display = "★" * min(self.current_user.stars, 10)
        if self.current_user.stars > 10:
            stars_display += "..."
        print(f"Streak: {self.current_user.current_streak} days | Stars: {stars_display}")
        print(f"连续学习: {self.current_user.current_streak} 天 | 星星: {stars_display}")
        print("=" * 50)
        print("Main Menu / 主菜单")
        print("1. Start Quiz / 开始测验")
        print("2. Text Library / 文本库")
        print("3. Profile / 用户档案")
        print("4. Badges / 徽章")
        print("5. Review / 复习")
        print("6. Import Text / 导入文本")
        print("7. Export Report / 导出报告")
        print("8. Save & Exit / 保存退出")

    def _view_text_library(self):
        texts = self.text_manager.get_all_texts()
        if not texts:
            print("\nNo texts available. / 暂无文本。")
            return

        print("\nText Library / 文本库")
        print("-" * 40)

        categories = self.text_manager.get_categories()
        for category in categories:
            print(f"\n[{category}]")
            cat_texts = self.text_manager.get_texts_by_category(category)
            for i, text in enumerate(cat_texts, 1):
                print(f"  {i}. {text.title} ({text.language}) - Difficulty: {text.difficulty}")

    def _start_quiz(self):
        texts = self.text_manager.get_all_texts()
        if not texts:
            print("\nNo texts available. Please import some texts first.")
            print("暂无文本，请先导入文本。")
            return

        print("\nSelect a text to practice / 选择要练习的文本:")
        for i, text in enumerate(texts, 1):
            print(f"{i}. {text.title} ({text.language}) - {text.category}")

        while True:
            try:
                idx = int(input("Enter text number / 输入文本序号: ").strip()) - 1
                if 0 <= idx < len(texts):
                    selected_text = texts[idx]
                    break
                else:
                    print("Invalid number. / 无效序号。")
            except ValueError:
                print("Please enter a number. / 请输入数字。")

        print(f"\nSelected: {selected_text.title}")
        print(f"选择: {selected_text.title}")

        print("\nSelect difficulty / 选择难度:")
        print("1. Easy / 简单 (20% blanks)")
        print("2. Medium / 中等 (40% blanks)")
        print("3. Hard / 困难 (60% blanks)")

        while True:
            try:
                difficulty = int(input("Enter difficulty (1-3): ").strip())
                if 1 <= difficulty <= 3:
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a number.")

        print(f"\nGenerating quiz for {selected_text.title}...")
        questions = self.quiz_generator.generate_quiz(selected_text, difficulty)

        if not questions:
            print("Could not generate quiz. / 无法生成测验。")
            return

        print(f"\nQuiz ready! {len(questions)} questions.")
        print(f"测验已生成！共 {len(questions)} 题。")
        print("=" * 50)

        mistakes = []

        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}:")
            print(f"题目 {i}:")
            print(question.prompt)

            user_answer = input("Your answer / 你的答案: ").strip()
            question.user_answer = user_answer

            is_correct = self.answer_checker.check_answer(user_answer, question.correct_answer, selected_text.language)
            question.is_correct = is_correct

            if is_correct:
                print("✓ Correct!")
            else:
                print(f"✗ Wrong. Correct answer: {question.correct_answer}")
                mistakes.append(f"Q{i}: Expected '{question.correct_answer}', got '{user_answer}'")

        correct_count, total_count, accuracy, stars = self.answer_checker.calculate_score(questions)

        print("\n" + "=" * 50)
        print("Quiz Results / 测验结果")
        print("=" * 50)
        print(f"Score: {accuracy}%")
        print(f"得分: {accuracy}%")
        print(f"Correct: {correct_count}/{total_count}")
        print(f"正确: {correct_count}/{total_count}")
        print(f"Stars earned: {'★' * stars}")
        print(f"获得星星: {'★' * stars}")

        self.progress_tracker.record_quiz(selected_text.text_id, accuracy, correct_count, total_count, mistakes, stars)
        self.review_scheduler.update_after_quiz(selected_text.text_id, accuracy)

        newly_unlocked = self.badge_manager.check_badges()
        if newly_unlocked:
            print("\n🎉 Congratulations! You unlocked new badges:")
            print("🎉 恭喜！你解锁了新徽章：")
            for badge in newly_unlocked:
                print(f"  ✓ {badge.name}")

        self.user_manager.save_profile(self.current_user)

    def _view_profile(self):
        stats = self.progress_tracker.get_total_stats()

        print("\n" + "=" * 50)
        print("User Profile / 用户档案")
        print("=" * 50)
        print(f"Username: {self.current_user.username}")
        print(f"用户名: {self.current_user.username}")
        print(f"\nLearning Statistics / 学习统计:")
        print(f"  Total Quizzes / 测验总数: {self.current_user.total_quizzes}")
        print(f"  Total Questions / 题目总数: {stats['total_questions']}")
        print(f"  Total Correct / 正确总数: {stats['total_correct']}")
        print(f"  Average Accuracy / 平均正确率: {stats['avg_accuracy']}%")
        print(f"  Total Stars / 总星星: {self.current_user.stars}")
        print(f"  Current Streak / 当前连续: {self.current_user.current_streak} days")
        print(f"  Longest Streak / 最长连续: {self.current_user.longest_streak} days")

        practiced_texts = self.progress_tracker.get_practiced_texts()
        print(f"\nPracticed Texts / 已练习文本: {len(practiced_texts)}")
        for text_id in practiced_texts:
            text = self.text_manager.get_text_by_id(text_id)
            if text:
                print(f"  - {text.title}")

    def _view_badges(self):
        all_badges = self.badge_manager.get_all_badges()
        unlocked_badges = self.badge_manager.get_unlocked_badges()

        print("\n" + "=" * 50)
        print("Badges / 徽章")
        print("=" * 50)
        print(f"Unlocked: {len(unlocked_badges)}/{len(all_badges)}")
        print(f"已解锁: {len(unlocked_badges)}/{len(all_badges)}")

        for badge in all_badges:
            status = "✓" if self.badge_manager.is_badge_unlocked(badge.badge_id) else "○"
            print(f"\n{status} {badge.name}")
            print(f"   Condition / 条件: {badge.condition}")

        next_badge = self.badge_manager.get_next_badge()
        if next_badge:
            print(f"\nNext badge to unlock / 下一个徽章: {next_badge.name}")

    def _view_review(self):
        due_reviews = self.review_scheduler.get_due_reviews()

        print("\n" + "=" * 50)
        print("Review / 复习")
        print("=" * 50)

        if due_reviews:
            print(f"Texts due for review / 需要复习的文本: {len(due_reviews)}")
            for i, review in enumerate(due_reviews, 1):
                text = self.text_manager.get_text_by_id(review["text_id"])
                title = text.title if text else review["text_id"]
                print(f"\n{i}. {title}")
                print(f"   Last practiced / 上次练习: {review['last_practiced_date']}")
                print(f"   Days overdue / 逾期天数: {review['days_overdue']}")
        else:
            print("No texts due for review. / 没有需要复习的文本。")
            print("Keep practicing to build your review schedule!")

    def _import_text(self):
        file_path = input("\nEnter TXT file path / 输入 TXT 文件路径: ").strip()

        if not os.path.exists(file_path):
            print("File not found. / 文件不存在。")
            return

        title = input("Enter text title / 输入文本标题: ").strip()
        if not title:
            print("Title cannot be empty. / 标题不能为空。")
            return

        category = input("Enter category / 输入分类: ").strip()
        if not category:
            category = "Custom"

        try:
            difficulty = int(input("Enter difficulty (1-3): ").strip())
            if difficulty < 1 or difficulty > 3:
                difficulty = 1
        except ValueError:
            difficulty = 1

        new_text = self.text_manager.import_txt_file(file_path, title, category, difficulty)

        if new_text:
            print(f"\nText imported successfully!")
            print(f"文本导入成功！")
            print(f"Title: {new_text.title}")
            print(f"Language: {new_text.language}")
            print(f"Category: {new_text.category}")
        else:
            print("\nFailed to import text. / 导入失败。")

    def _export_report(self):
        print("\nExport Report / 导出报告")
        print("1. Quiz Report / 测验报告")
        print("2. Badge Certificate / 徽章证书")
        print("3. Progress Summary / 进度汇总")

        while True:
            choice = input("Enter choice / 输入选择 (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                break
            print("Invalid choice. / 无效选择。")

        if choice == "1":
            records = self.progress_tracker.get_all_records()
            if not records:
                print("No quiz records to export. / 没有测验记录可导出。")
                return

            print("\nSelect a quiz record:")
            for i, record in enumerate(records, 1):
                text = self.text_manager.get_text_by_id(record.text_id)
                title = text.title if text else record.text_id
                print(f"{i}. {record.date} - {title} ({record.score}%)")

            while True:
                try:
                    idx = int(input("Enter record number: ").strip()) - 1
                    if 0 <= idx < len(records):
                        record = records[idx]
                        questions = []
                        filepath = self.report_exporter.export_quiz_report(record, questions)
                        print(f"\nReport exported to: {filepath}")
                        break
                except ValueError:
                    print("Please enter a number.")

        elif choice == "2":
            filepath = self.report_exporter.export_badge_certificate()
            print(f"\nBadge certificate exported to: {filepath}")

        elif choice == "3":
            filepath = self.report_exporter.export_progress_summary()
            print(f"\nProgress summary exported to: {filepath}")

    def _save_and_exit(self):
        self.user_manager.save_profile(self.current_user)
        print(f"\nProfile saved successfully!")
        print("档案保存成功！")
        print(f"Goodbye, {self.current_user.username}!")
        print(f"再见，{self.current_user.username}！")


if __name__ == "__main__":
    app = RecitationQuizApp()
    app.run()