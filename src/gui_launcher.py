import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from user_profile import UserProfileManager
from text_manager import TextManager
from quiz_generator import QuizGenerator
from answer_checker import AnswerChecker
from theme_manager import ThemeManager
from gui.main_window import MainWindow


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "output")

    user_manager = UserProfileManager(data_dir)
    text_manager = TextManager(data_dir)
    quiz_generator = QuizGenerator()
    answer_checker = AnswerChecker()

    app = MainWindow(None)

    theme_manager = ThemeManager(app)

    managers = {
        "user_manager": user_manager,
        "text_manager": text_manager,
        "quiz_generator": quiz_generator,
        "answer_checker": answer_checker,
        "theme_manager": theme_manager,
        "data_dir": data_dir,
        "output_dir": output_dir,
        "progress_tracker": None,
        "review_scheduler": None,
        "badge_manager": None,
        "report_exporter": None
    }

    app.set_managers(managers)
    app.run()


if __name__ == "__main__":
    main()