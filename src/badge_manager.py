import json
import os
from datetime import datetime


class Badge:
    def __init__(self, badge_id, name, description, category, condition, unlocked_date=None):
        self.badge_id = badge_id
        self.name = name
        self.description = description
        self.category = category
        self.condition = condition
        self.unlocked_date = unlocked_date

    def to_dict(self):
        return {
            "badge_id": self.badge_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "condition": self.condition,
            "unlocked_date": self.unlocked_date.isoformat() if self.unlocked_date else None
        }

    @classmethod
    def from_dict(cls, data):
        badge = cls(
            data["badge_id"],
            data["name"],
            data.get("description", ""),
            data.get("category", ""),
            data["condition"]
        )
        if data.get("unlocked_date"):
            badge.unlocked_date = data["unlocked_date"]
        return badge


class BadgeManager:
    DEFAULT_BADGES = [
        {"badge_id": "first_spark", "name": "First Spark / 初燃之星", "description": "Complete your first quiz.", "category": "Journey", "condition": "Complete your first quiz."},
        {"badge_id": "rising_ember", "name": "Rising Ember / 渐燃之火", "description": "Complete 5 quizzes.", "category": "Journey", "condition": "Complete 5 quizzes."},
        {"badge_id": "memory_sprinter", "name": "Memory Sprinter / 记忆冲刺者", "description": "Complete 10 quizzes.", "category": "Journey", "condition": "Complete 10 quizzes."},
        {"badge_id": "dedicated_learner", "name": "Dedicated Learner / 勤学者", "description": "Complete 50 quizzes.", "category": "Journey", "condition": "Complete 50 quizzes."},
        {"badge_id": "master_of_recitation", "name": "Master of Recitation / 背诵大师", "description": "Complete 100 quizzes.", "category": "Journey", "condition": "Complete 100 quizzes."},
        
        {"badge_id": "three_day_flame", "name": "Three-Day Flame / 三日微焰", "description": "Maintain a 3-day learning streak.", "category": "Streak", "condition": "Maintain a 3-day learning streak."},
        {"badge_id": "seven_day_scholar", "name": "Seven-Day Scholar / 七日学者", "description": "Maintain a 7-day learning streak.", "category": "Streak", "condition": "Maintain a 7-day learning streak."},
        {"badge_id": "half_month_guardian", "name": "Half-Month Guardian / 半月守护者", "description": "Maintain a 15-day learning streak.", "category": "Streak", "condition": "Maintain a 15-day learning streak."},
        {"badge_id": "monthly_keeper", "name": "Monthly Keeper / 月度守护者", "description": "Maintain a 30-day learning streak.", "category": "Streak", "condition": "Maintain a 30-day learning streak."},
        {"badge_id": "hundred_day_legend", "name": "Hundred-Day Legend / 百日传说", "description": "Maintain a 100-day learning streak.", "category": "Streak", "condition": "Maintain a 100-day learning streak."},
        {"badge_id": "eternal_flame", "name": "Eternal Flame / 永恒之焰", "description": "Maintain a 365-day learning streak.", "category": "Streak", "condition": "Maintain a 365-day learning streak."},
        
        {"badge_id": "bright_beginning", "name": "Bright Beginning / 初露光芒", "description": "Collect 10 stars.", "category": "Star", "condition": "Collect 10 stars."},
        {"badge_id": "shining_learner", "name": "Shining Learner / 闪耀学者", "description": "Collect 50 stars.", "category": "Star", "condition": "Collect 50 stars."},
        {"badge_id": "constellation_builder", "name": "Constellation Builder / 星辰构筑者", "description": "Collect 100 stars.", "category": "Star", "condition": "Collect 100 stars."},
        {"badge_id": "galaxy_explorer", "name": "Galaxy Explorer / 银河探索者", "description": "Collect 300 stars.", "category": "Star", "condition": "Collect 300 stars."},
        {"badge_id": "celestial_master", "name": "Celestial Master / 星穹大师", "description": "Collect 1000 stars.", "category": "Star", "condition": "Collect 1000 stars."},
        
        {"badge_id": "text_explorer", "name": "Text Explorer / 文本探索者", "description": "Practice 5 different texts.", "category": "Mastery", "condition": "Practice 5 different texts."},
        {"badge_id": "library_wanderer", "name": "Library Wanderer / 文库漫游者", "description": "Practice 20 different texts.", "category": "Mastery", "condition": "Practice 20 different texts."},
        {"badge_id": "knowledge_collector", "name": "Knowledge Collector / 知识收藏家", "description": "Practice 50 different texts.", "category": "Mastery", "condition": "Practice 50 different texts."},
        
        {"badge_id": "precision_master", "name": "Precision Master / 精准大师", "description": "Score 100% once.", "category": "Perfect", "condition": "Score 100% once."},
        {"badge_id": "perfect_duo", "name": "Perfect Duo / 双连满分", "description": "Achieve two perfect scores in a row.", "category": "Perfect", "condition": "Achieve two perfect scores in a row."},
        {"badge_id": "unbreakable_accuracy", "name": "Unbreakable Accuracy / 百发百中", "description": "Achieve five perfect scores.", "category": "Perfect", "condition": "Achieve five perfect scores."},
        
        {"badge_id": "faithful_reader", "name": "Faithful Reader / 专注读者", "description": "Practice the same text 5 times.", "category": "Persistence", "condition": "Practice the same text 5 times."},
        {"badge_id": "patient_scholar", "name": "Patient Scholar / 潜心学者", "description": "Practice the same text 10 times.", "category": "Persistence", "condition": "Practice the same text 10 times."},
        {"badge_id": "text_guardian", "name": "Text Guardian / 文本守护者", "description": "Practice the same text 20 times.", "category": "Persistence", "condition": "Practice the same text 20 times."},
        {"badge_id": "memory_artisan", "name": "Memory Artisan / 记忆工匠", "description": "Master one text with 20 successful attempts.", "category": "Persistence", "condition": "Master one text with 20 successful attempts."},
        
        {"badge_id": "easy_beginner", "name": "Easy Beginner / 初级挑战者", "description": "Earn 3 stars in Easy mode.", "category": "Difficulty", "condition": "Earn 3 stars in Easy mode."},
        {"badge_id": "normal_challenger", "name": "Normal Challenger / 进阶挑战者", "description": "Earn 3 stars in Medium mode.", "category": "Difficulty", "condition": "Earn 3 stars in Medium mode."},
        {"badge_id": "hard_conqueror", "name": "Hard Conqueror / 困难征服者", "description": "Earn 3 stars in Hard mode.", "category": "Difficulty", "condition": "Earn 3 stars in Hard mode."},
        {"badge_id": "ultimate_challenger", "name": "Ultimate Challenger / 终极挑战者", "description": "Earn 3 stars in all three difficulty levels.", "category": "Difficulty", "condition": "Earn 3 stars in all three difficulty levels."},
        
        {"badge_id": "never_forget", "name": "Never Forget / 温故知新", "description": "Complete your first scheduled review.", "category": "Review", "condition": "Complete your first scheduled review."},
        {"badge_id": "memory_keeper", "name": "Memory Keeper / 记忆守护者", "description": "Complete 10 review sessions.", "category": "Review", "condition": "Complete 10 review sessions."},
        {"badge_id": "review_veteran", "name": "Review Veteran / 复习达人", "description": "Complete 50 review sessions.", "category": "Review", "condition": "Complete 50 review sessions."},
        
        {"badge_id": "night_owl", "name": "Night Owl / 夜读者", "description": "Complete a quiz after 10:00 PM.", "category": "Special", "condition": "Complete a quiz after 10:00 PM."},
        {"badge_id": "early_bird", "name": "Early Bird / 晨读者", "description": "Complete a quiz before 7:00 AM.", "category": "Special", "condition": "Complete a quiz before 7:00 AM."},
        {"badge_id": "marathon_learner", "name": "Marathon Learner / 马拉松学习者", "description": "Finish 10 quizzes in one day.", "category": "Special", "condition": "Finish 10 quizzes in one day."},
        {"badge_id": "comeback_hero", "name": "Comeback Hero / 王者归来", "description": "Return after being inactive for 30 days.", "category": "Special", "condition": "Return after being inactive for 30 days."}
    ]

    def __init__(self, user_profile, data_dir="data"):
        self.user_profile = user_profile
        self.data_dir = data_dir
        self.badges_file = os.path.join(data_dir, "badges.json")
        self.all_badges = self._load_badges()

    def _load_badges(self):
        badges = {}
        for badge_data in self.DEFAULT_BADGES:
            badge = Badge.from_dict(badge_data)
            badges[badge.badge_id] = badge

        if os.path.exists(self.badges_file):
            with open(self.badges_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for badge_data in data.get("badges", []):
                    badge = Badge.from_dict(badge_data)
                    badges[badge.badge_id] = badge
        return badges

    def check_badges(self):
        newly_unlocked = []
        
        streak_counts = self._get_streak_counts()
        star_count = self._get_star_count()
        unique_texts = self._get_unique_text_count()
        perfect_count = self._get_perfect_count()
        text_practice_counts = self._get_text_practice_counts()
        difficulty_stars = self._get_difficulty_stars()
        review_count = self._get_review_count()
        quiz_times = self._get_quiz_times()
        today_quiz_count = self._get_today_quiz_count()
        last_active_date = self._get_last_active_date()

        badge_conditions = {
            "first_spark": lambda: self.user_profile.total_quizzes >= 1,
            "rising_ember": lambda: self.user_profile.total_quizzes >= 5,
            "memory_sprinter": lambda: self.user_profile.total_quizzes >= 10,
            "dedicated_learner": lambda: self.user_profile.total_quizzes >= 50,
            "master_of_recitation": lambda: self.user_profile.total_quizzes >= 100,
            
            "three_day_flame": lambda: streak_counts.get(3, 0) >= 1,
            "seven_day_scholar": lambda: streak_counts.get(7, 0) >= 1,
            "half_month_guardian": lambda: streak_counts.get(15, 0) >= 1,
            "monthly_keeper": lambda: streak_counts.get(30, 0) >= 1,
            "hundred_day_legend": lambda: streak_counts.get(100, 0) >= 1,
            "eternal_flame": lambda: streak_counts.get(365, 0) >= 1,
            
            "bright_beginning": lambda: star_count >= 10,
            "shining_learner": lambda: star_count >= 50,
            "constellation_builder": lambda: star_count >= 100,
            "galaxy_explorer": lambda: star_count >= 300,
            "celestial_master": lambda: star_count >= 1000,
            
            "text_explorer": lambda: unique_texts >= 5,
            "library_wanderer": lambda: unique_texts >= 20,
            "knowledge_collector": lambda: unique_texts >= 50,
            
            "precision_master": lambda: perfect_count >= 1,
            "perfect_duo": lambda: self._check_consecutive_perfect(2),
            "unbreakable_accuracy": lambda: perfect_count >= 5,
            
            "faithful_reader": lambda: any(count >= 5 for count in text_practice_counts.values()),
            "patient_scholar": lambda: any(count >= 10 for count in text_practice_counts.values()),
            "text_guardian": lambda: any(count >= 20 for count in text_practice_counts.values()),
            "memory_artisan": lambda: any(count >= 20 for count in text_practice_counts.values()),
            
            "easy_beginner": lambda: difficulty_stars.get(1, 0) >= 3,
            "normal_challenger": lambda: difficulty_stars.get(2, 0) >= 3,
            "hard_conqueror": lambda: difficulty_stars.get(3, 0) >= 3,
            "ultimate_challenger": lambda: difficulty_stars.get(1, 0) >= 3 and difficulty_stars.get(2, 0) >= 3 and difficulty_stars.get(3, 0) >= 3,
            
            "never_forget": lambda: review_count >= 1,
            "memory_keeper": lambda: review_count >= 10,
            "review_veteran": lambda: review_count >= 50,
            
            "night_owl": lambda: any(t.hour >= 22 for t in quiz_times),
            "early_bird": lambda: any(t.hour < 7 for t in quiz_times),
            "marathon_learner": lambda: today_quiz_count >= 10,
            "comeback_hero": lambda: self._check_comeback(last_active_date)
        }

        for badge_id, condition in badge_conditions.items():
            if badge_id not in self.user_profile.badges and condition():
                self.user_profile.add_badge(badge_id)
                newly_unlocked.append(self.all_badges.get(badge_id))
        return newly_unlocked

    def _get_streak_counts(self):
        counts = {}
        max_streak = max(self.user_profile.current_streak, self.user_profile.longest_streak)
        for threshold in [3, 7, 15, 30, 100, 365]:
            if max_streak >= threshold:
                counts[threshold] = counts.get(threshold, 0) + 1
        return counts

    def _get_star_count(self):
        return sum(r.get('stars_earned', r.get('stars', 0)) for r in self.user_profile.learning_records)

    def _get_unique_text_count(self):
        return len(set(r.get('text_id') for r in self.user_profile.learning_records if r.get('text_id')))

    def _get_perfect_count(self):
        return sum(1 for r in self.user_profile.learning_records if r.get('score', 0) >= 100)

    def _check_consecutive_perfect(self, count):
        consecutive = 0
        for r in self.user_profile.learning_records:
            if r.get('score', 0) >= 100:
                consecutive += 1
                if consecutive >= count:
                    return True
            else:
                consecutive = 0
        return False

    def _get_text_practice_counts(self):
        counts = {}
        for r in self.user_profile.learning_records:
            text_id = r.get('text_id')
            if text_id:
                counts[text_id] = counts.get(text_id, 0) + 1
        return counts

    def _get_difficulty_stars(self):
        stars = {1: 0, 2: 0, 3: 0}
        for r in self.user_profile.learning_records:
            difficulty = r.get('difficulty', 1)
            star_count = r.get('stars', 0)
            if difficulty in stars and star_count > stars[difficulty]:
                stars[difficulty] = star_count
        return stars

    def _get_review_count(self):
        return len([r for r in self.user_profile.learning_records if r.get('is_review', False)])

    def _get_quiz_times(self):
        times = []
        for r in self.user_profile.learning_records:
            timestamp = r.get('timestamp')
            if timestamp:
                try:
                    times.append(datetime.fromisoformat(timestamp))
                except:
                    pass
        return times

    def _get_today_quiz_count(self):
        today = datetime.now().date()
        count = 0
        for r in self.user_profile.learning_records:
            timestamp = r.get('timestamp')
            if timestamp:
                try:
                    quiz_date = datetime.fromisoformat(timestamp).date()
                    if quiz_date == today:
                        count += 1
                except:
                    pass
        return count

    def _get_last_active_date(self):
        if not self.user_profile.learning_records:
            return None
        last_date = None
        for r in self.user_profile.learning_records:
            timestamp = r.get('timestamp')
            if timestamp:
                try:
                    record_date = datetime.fromisoformat(timestamp).date()
                    if last_date is None or record_date > last_date:
                        last_date = record_date
                except:
                    pass
        return last_date

    def _check_comeback(self, last_active_date):
        if last_active_date is None:
            return False
        days_since = (datetime.now().date() - last_active_date).days
        return days_since >= 30

    def get_unlocked_badges(self):
        unlocked = []
        for badge_id in self.user_profile.badges:
            if badge_id in self.all_badges:
                badge = self.all_badges[badge_id]
                unlocked.append(badge)
        return unlocked

    def get_all_badges(self):
        return list(self.all_badges.values())

    def get_badge_by_id(self, badge_id):
        return self.all_badges.get(badge_id)

    def is_badge_unlocked(self, badge_id):
        return badge_id in self.user_profile.badges

    def get_next_badge(self):
        priority_order = [
            "first_spark", "rising_ember", "memory_sprinter", "dedicated_learner", "master_of_recitation",
            "three_day_flame", "seven_day_scholar", "half_month_guardian", "monthly_keeper", "hundred_day_legend", "eternal_flame",
            "bright_beginning", "shining_learner", "constellation_builder", "galaxy_explorer", "celestial_master",
            "text_explorer", "library_wanderer", "knowledge_collector",
            "precision_master", "perfect_duo", "unbreakable_accuracy",
            "faithful_reader", "patient_scholar", "text_guardian", "memory_artisan",
            "easy_beginner", "normal_challenger", "hard_conqueror", "ultimate_challenger",
            "never_forget", "memory_keeper", "review_veteran",
            "night_owl", "early_bird", "marathon_learner", "comeback_hero"
        ]
        for badge_id in priority_order:
            if badge_id not in self.user_profile.badges:
                return self.all_badges.get(badge_id)
        return None

    def get_badges_by_category(self, category):
        return [badge for badge in self.all_badges.values() if badge.category == category]
