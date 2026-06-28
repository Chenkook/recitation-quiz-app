from datetime import date, datetime


class QuizResult:
    def __init__(self, text_id, score, correct_count, total_count, mistakes, stars_earned, difficulty=1):
        self.text_id = text_id
        self.date = date.today()
        self.timestamp = datetime.now().isoformat()
        self.score = score
        self.correct_count = correct_count
        self.total_count = total_count
        self.mistakes = mistakes
        self.stars_earned = stars_earned
        self.difficulty = difficulty

    def to_dict(self):
        return {
            "text_id": self.text_id,
            "date": self.date.isoformat(),
            "timestamp": self.timestamp,
            "score": self.score,
            "correct_count": self.correct_count,
            "total_count": self.total_count,
            "mistakes": self.mistakes,
            "stars_earned": self.stars_earned,
            "difficulty": self.difficulty
        }

    @classmethod
    def from_dict(cls, data):
        result = cls(
            data["text_id"],
            data["score"],
            data["correct_count"],
            data["total_count"],
            data.get("mistakes", []),
            data["stars_earned"],
            data.get("difficulty", 1)
        )
        if data.get("date"):
            result.date = date.fromisoformat(data["date"])
        if data.get("timestamp"):
            result.timestamp = data["timestamp"]
        return result


class ProgressTracker:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def record_quiz(self, text_id, score, correct_count, total_count, mistakes, stars_earned, difficulty=1):
        result = QuizResult(text_id, score, correct_count, total_count, mistakes, stars_earned, difficulty)
        self.user_profile.learning_records.append(result.to_dict())
        self.user_profile.add_quiz(stars_earned)
        return result

    def get_progress_by_text(self, text_id):
        records = [
            QuizResult.from_dict(r)
            for r in self.user_profile.learning_records
            if r["text_id"] == text_id
        ]
        return records

    def get_all_records(self):
        return [QuizResult.from_dict(r) for r in self.user_profile.learning_records]

    def get_total_stats(self):
        records = self.get_all_records()
        if not records:
            return {
                "total_quizzes": 0,
                "total_questions": 0,
                "total_correct": 0,
                "avg_accuracy": 0,
                "total_stars": 0
            }

        total_quizzes = len(records)
        total_questions = sum(r.total_count for r in records)
        total_correct = sum(r.correct_count for r in records)
        avg_accuracy = (total_correct / total_questions) * 100 if total_questions > 0 else 0
        total_stars = sum(r.stars_earned for r in records)

        return {
            "total_quizzes": total_quizzes,
            "total_questions": total_questions,
            "total_correct": total_correct,
            "avg_accuracy": round(avg_accuracy, 1),
            "total_stars": total_stars
        }

    def get_practiced_texts(self):
        text_ids = set(r["text_id"] for r in self.user_profile.learning_records)
        return text_ids

    def get_mistakes(self, text_id=None):
        all_mistakes = []
        for record_data in self.user_profile.learning_records:
            if text_id and record_data["text_id"] != text_id:
                continue
            if "mistakes" in record_data:
                all_mistakes.extend(record_data["mistakes"])
        return all_mistakes