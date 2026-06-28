import json
import os
from datetime import datetime, date


class UserProfile:
    def __init__(self, username):
        self.username = username
        self.current_streak = 0
        self.longest_streak = 0
        self.total_quizzes = 0
        self.stars = 0
        self.badges = []
        self.learning_records = []
        self.review_records = []
        self.last_practice_date = None

    def to_dict(self):
        return {
            "username": self.username,
            "current_streak": self.current_streak,
            "longest_streak": self.longest_streak,
            "total_quizzes": self.total_quizzes,
            "stars": self.stars,
            "badges": self.badges,
            "learning_records": self.learning_records,
            "review_records": self.review_records,
            "last_practice_date": self.last_practice_date.isoformat() if self.last_practice_date else None
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"])
        user.current_streak = data.get("current_streak", 0)
        user.longest_streak = data.get("longest_streak", 0)
        user.total_quizzes = data.get("total_quizzes", 0)
        user.stars = data.get("stars", 0)
        user.badges = data.get("badges", [])
        user.learning_records = data.get("learning_records", [])
        user.review_records = data.get("review_records", [])
        if data.get("last_practice_date"):
            user.last_practice_date = date.fromisoformat(data["last_practice_date"])
        return user

    def update_streak(self):
        today = date.today()
        if self.last_practice_date is None:
            self.current_streak = 1
        else:
            days_diff = (today - self.last_practice_date).days
            if days_diff == 1:
                self.current_streak += 1
            elif days_diff > 1:
                self.current_streak = 1
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        self.last_practice_date = today

    def add_quiz(self, stars_earned):
        self.total_quizzes += 1
        self.stars += stars_earned
        self.update_streak()

    def add_badge(self, badge_id):
        if badge_id not in self.badges:
            self.badges.append(badge_id)
            return True
        return False


class UserProfileManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self._ensure_dir()

    def _ensure_dir(self):
        os.makedirs(self.data_dir, exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump({"users": []}, f, ensure_ascii=False, indent=2)

    def create_profile(self, username):
        users = self._load_users()
        if any(u["username"] == username for u in users["users"]):
            return None
        user = UserProfile(username)
        users["users"].append(user.to_dict())
        self._save_users(users)
        return user

    def load_profile(self, username):
        users = self._load_users()
        for user_data in users["users"]:
            if user_data["username"] == username:
                return UserProfile.from_dict(user_data)
        return None

    def save_profile(self, user):
        users = self._load_users()
        for i, user_data in enumerate(users["users"]):
            if user_data["username"] == user.username:
                users["users"][i] = user.to_dict()
                self._save_users(users)
                return True
        users["users"].append(user.to_dict())
        self._save_users(users)
        return True

    def _load_users(self):
        with open(self.users_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_users(self, users):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def get_all_usernames(self):
        users = self._load_users()
        return [u["username"] for u in users["users"]]