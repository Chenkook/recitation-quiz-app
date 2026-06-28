import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from quiz_generator import QuizGenerator
from text_manager import LearningText


def test_generate_chinese_quiz():
    generator = QuizGenerator()

    text = LearningText(
        text_id="test_cn",
        title="Test Chinese",
        language="中文",
        category="Test",
        difficulty=1,
        content="床前明月光，疑是地上霜。"
    )

    questions = generator.generate_quiz(text, difficulty=1)
    assert len(questions) > 0
    assert len(questions) <= 6

    for q in questions:
        assert "【_" in q.prompt
        assert len(q.correct_answer) == 1
        assert q.correct_answer in text.content
        assert hasattr(q, 'blank_number')
        assert hasattr(q, 'total_blanks')

    questions_hard = generator.generate_quiz(text, difficulty=3)
    assert len(questions_hard) >= len(questions)


def test_generate_english_quiz():
    generator = QuizGenerator()

    text = LearningText(
        text_id="test_en",
        title="Test English",
        language="English",
        category="Test",
        difficulty=1,
        content="Hello world, this is a test."
    )

    questions = generator.generate_quiz(text, difficulty=1)
    assert len(questions) > 0

    for q in questions:
        assert "[__" in q.prompt
        assert q.correct_answer in text.content
        assert hasattr(q, 'blank_number')
        assert hasattr(q, 'total_blanks')

    questions_hard = generator.generate_quiz(text, difficulty=3)
    assert len(questions_hard) >= len(questions)


def test_difficulty_progression():
    generator = QuizGenerator()

    text = LearningText(
        text_id="test_diff",
        title="Test Difficulty",
        language="中文",
        category="Test",
        difficulty=1,
        content="白日依山尽，黄河入海流。欲穷千里目，更上一层楼。"
    )

    questions_easy = generator.generate_quiz(text, difficulty=1)
    questions_medium = generator.generate_quiz(text, difficulty=2)
    questions_hard = generator.generate_quiz(text, difficulty=3)

    assert len(questions_easy) <= len(questions_medium)
    assert len(questions_medium) <= len(questions_hard)


def test_quiz_question_to_dict():
    from quiz_generator import QuizQuestion

    q = QuizQuestion("q1", "____ world", "hello", user_answer="user_answer", is_correct=True)
    q_dict = q.to_dict()

    assert q_dict["question_id"] == "q1"
    assert q_dict["prompt"] == "____ world"
    assert q_dict["correct_answer"] == "hello"
    assert q_dict["user_answer"] == "user_answer"
    assert q_dict["is_correct"] == True
    assert q_dict["blank_number"] == 1
    assert q_dict["total_blanks"] == 1
    assert q_dict["char_index"] == 0

    q2 = QuizQuestion("q2", "prompt", "answer")
    q2_dict = q2.to_dict()
    assert q2_dict["user_answer"] is None
    assert q2_dict["is_correct"] is None


if __name__ == "__main__":
    test_generate_chinese_quiz()
    print("test_generate_chinese_quiz passed!")

    test_generate_english_quiz()
    print("test_generate_english_quiz passed!")

    test_difficulty_progression()
    print("test_difficulty_progression passed!")

    test_quiz_question_to_dict()
    print("test_quiz_question_to_dict passed!")

    print("\nAll tests passed!")