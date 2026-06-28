import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from answer_checker import AnswerChecker


def test_check_answer_chinese():
    checker = AnswerChecker()

    assert checker.check_answer("床", "床", "中文") == True
    assert checker.check_answer("明月光", "明月光", "中文") == True
    assert checker.check_answer("明", "床", "中文") == False
    assert checker.check_answer("床前", "床", "中文") == False
    assert checker.check_answer("", "", "中文") == True
    assert checker.check_answer(None, "", "中文") == True

    assert checker.check_answer("床前明月光", "床前明月光", "中文") == True
    assert checker.check_answer("床前明月光，", "床前明月光", "中文") == True
    assert checker.check_answer(" 床前明月光 ", "床前明月光", "中文") == True


def test_check_answer_english():
    checker = AnswerChecker()

    assert checker.check_answer("hello", "hello", "English") == True
    assert checker.check_answer("Hello", "hello", "English") == True
    assert checker.check_answer("HELLO", "hello", "English") == True
    assert checker.check_answer("hell", "hello", "English") == True
    assert checker.check_answer("helo", "hello", "English") == True
    assert checker.check_answer("hellow", "hello", "English") == True
    assert checker.check_answer("world", "hello", "English") == False
    assert checker.check_answer("hello,", "hello", "English") == True
    assert checker.check_answer("  hello  ", "hello", "English") == True


def test_calculate_score():
    checker = AnswerChecker()

    from quiz_generator import QuizQuestion

    questions_all_correct = [
        QuizQuestion("q1", "____ world", "hello", user_answer="hello", is_correct=True),
        QuizQuestion("q2", "Hello ____", "world", user_answer="world", is_correct=True),
        QuizQuestion("q3", "____ ____", "hello world", user_answer="hello world", is_correct=True),
    ]
    correct, total, accuracy, stars = checker.calculate_score(questions_all_correct)
    assert correct == 3
    assert total == 3
    assert accuracy == 100.0
    assert stars == 3

    questions_mixed = [
        QuizQuestion("q1", "____ world", "hello", user_answer="hello", is_correct=True),
        QuizQuestion("q2", "Hello ____", "world", user_answer="wrong", is_correct=False),
        QuizQuestion("q3", "____ ____", "hello world", user_answer="hello world", is_correct=True),
    ]
    correct, total, accuracy, stars = checker.calculate_score(questions_mixed)
    assert correct == 2
    assert total == 3
    assert accuracy == 66.7
    assert stars == 1

    questions_all_wrong = [
        QuizQuestion("q1", "____ world", "hello", user_answer="wrong1", is_correct=False),
        QuizQuestion("q2", "Hello ____", "world", user_answer="wrong2", is_correct=False),
    ]
    correct, total, accuracy, stars = checker.calculate_score(questions_all_wrong)
    assert correct == 0
    assert total == 2
    assert accuracy == 0.0
    assert stars == 0

    questions_eighty_percent = [
        QuizQuestion("q1", "q1", "a", user_answer="a", is_correct=True),
        QuizQuestion("q2", "q2", "b", user_answer="b", is_correct=True),
        QuizQuestion("q3", "q3", "c", user_answer="c", is_correct=True),
        QuizQuestion("q4", "q4", "d", user_answer="d", is_correct=True),
        QuizQuestion("q5", "q5", "e", user_answer="wrong", is_correct=False),
    ]
    correct, total, accuracy, stars = checker.calculate_score(questions_eighty_percent)
    assert correct == 4
    assert total == 5
    assert accuracy == 80.0
    assert stars == 2


if __name__ == "__main__":
    test_check_answer_chinese()
    print("test_check_answer_chinese passed!")

    test_check_answer_english()
    print("test_check_answer_english passed!")

    test_calculate_score()
    print("test_calculate_score passed!")

    print("\nAll tests passed!")