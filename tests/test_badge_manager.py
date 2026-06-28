import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from badge_manager import BadgeManager
from user_profile import UserProfile


def test_first_spark_badge():
    user = UserProfile("test_user")
    badge_manager = BadgeManager(user, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))

    assert badge_manager.is_badge_unlocked("first_spark") == False

    user.total_quizzes = 1
    newly_unlocked = badge_manager.check_badges()

    assert len(newly_unlocked) == 1
    assert newly_unlocked[0].badge_id == "first_spark"
    assert badge_manager.is_badge_unlocked("first_spark") == True


def test_streak_badges():
    user = UserProfile("test_user")
    badge_manager = BadgeManager(user, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))

    user.current_streak = 1
    newly_unlocked = badge_manager.check_badges()
    assert badge_manager.is_badge_unlocked("three_day_flame") == False

    user.current_streak = 3
    newly_unlocked = badge_manager.check_badges()
    assert len(newly_unlocked) >= 1
    assert badge_manager.is_badge_unlocked("three_day_flame") == True

    user.current_streak = 7
    newly_unlocked = badge_manager.check_badges()
    assert len(newly_unlocked) >= 1
    assert badge_manager.is_badge_unlocked("seven_day_scholar") == True


def test_precision_master_badge():
    user = UserProfile("test_user")
    badge_manager = BadgeManager(user, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))

    assert badge_manager.is_badge_unlocked("precision_master") == False

    user.learning_records = [
        {"text_id": "text1", "score": 80},
        {"text_id": "text2", "score": 100},
    ]
    newly_unlocked = badge_manager.check_badges()

    assert len(newly_unlocked) >= 1
    assert badge_manager.is_badge_unlocked("precision_master") == True


def test_memory_sprinter_badge():
    user = UserProfile("test_user")
    badge_manager = BadgeManager(user, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))

    assert badge_manager.is_badge_unlocked("memory_sprinter") == False

    user.total_quizzes = 10
    newly_unlocked = badge_manager.check_badges()

    assert len(newly_unlocked) >= 1
    assert badge_manager.is_badge_unlocked("memory_sprinter") == True


def test_text_explorer_badge():
    user = UserProfile("test_user")
    badge_manager = BadgeManager(user, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))

    assert badge_manager.is_badge_unlocked("text_explorer") == False

    user.learning_records = [
        {"text_id": "text1"},
        {"text_id": "text2"},
        {"text_id": "text3"},
        {"text_id": "text4"},
        {"text_id": "text5"},
    ]
    newly_unlocked = badge_manager.check_badges()

    assert len(newly_unlocked) >= 1
    assert badge_manager.is_badge_unlocked("text_explorer") == True


def test_get_next_badge():
    user = UserProfile("test_user")
    badge_manager = BadgeManager(user, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))

    next_badge = badge_manager.get_next_badge()
    assert next_badge is not None
    assert next_badge.badge_id == "first_spark"

    user.total_quizzes = 1
    user.badges = ["first_spark"]
    badge_manager = BadgeManager(user, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))

    next_badge = badge_manager.get_next_badge()
    assert next_badge is not None
    assert next_badge.badge_id == "rising_ember"


if __name__ == "__main__":
    test_first_spark_badge()
    print("test_first_spark_badge passed!")

    test_streak_badges()
    print("test_streak_badges passed!")

    test_precision_master_badge()
    print("test_precision_master_badge passed!")

    test_memory_sprinter_badge()
    print("test_memory_sprinter_badge passed!")

    test_text_explorer_badge()
    print("test_text_explorer_badge passed!")

    test_get_next_badge()
    print("test_get_next_badge passed!")

    print("\nAll tests passed!")