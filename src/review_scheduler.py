from datetime import date, timedelta


class ReviewRecord:
    def __init__(self, text_id, last_practiced_date=None, next_review_date=None, review_status="pending"):
        self.text_id = text_id
        self.last_practiced_date = last_practiced_date
        self.next_review_date = next_review_date
        self.review_status = review_status

    def to_dict(self):
        return {
            "text_id": self.text_id,
            "last_practiced_date": self.last_practiced_date.isoformat() if self.last_practiced_date else None,
            "next_review_date": self.next_review_date.isoformat() if self.next_review_date else None,
            "review_status": self.review_status
        }

    @classmethod
    def from_dict(cls, data):
        record = cls(data["text_id"])
        if data.get("last_practiced_date"):
            record.last_practiced_date = date.fromisoformat(data["last_practiced_date"])
        if data.get("next_review_date"):
            record.next_review_date = date.fromisoformat(data["next_review_date"])
        record.review_status = data.get("review_status", "pending")
        return record


class ReviewScheduler:
    REVIEW_INTERVALS = [1, 3, 7, 14, 30]

    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.review_records = self._load_review_records()

    def _load_review_records(self):
        records = {}
        for record_data in self.user_profile.review_records:
            record = ReviewRecord.from_dict(record_data)
            records[record.text_id] = record
        return records

    def _save_review_records(self):
        self.user_profile.review_records = [r.to_dict() for r in self.review_records.values()]

    def update_after_quiz(self, text_id, accuracy):
        today = date.today()

        if text_id not in self.review_records:
            self.review_records[text_id] = ReviewRecord(text_id)

        record = self.review_records[text_id]
        record.last_practiced_date = today
        record.review_status = "completed"

        interval_index = min(int(accuracy // 20), len(self.REVIEW_INTERVALS) - 1)
        interval_days = self.REVIEW_INTERVALS[interval_index]
        record.next_review_date = today + timedelta(days=interval_days)

        self._save_review_records()

    def get_due_reviews(self):
        today = date.today()
        due_reviews = []

        for text_id, record in self.review_records.items():
            if record.next_review_date and record.next_review_date <= today:
                due_reviews.append({
                    "text_id": text_id,
                    "last_practiced_date": record.last_practiced_date,
                    "next_review_date": record.next_review_date,
                    "days_overdue": (today - record.next_review_date).days
                })

        due_reviews.sort(key=lambda x: x["days_overdue"], reverse=True)
        return due_reviews

    def get_review_status(self, text_id):
        if text_id not in self.review_records:
            return None
        return self.review_records[text_id].review_status

    def get_next_review_date(self, text_id):
        if text_id not in self.review_records:
            return None
        return self.review_records[text_id].next_review_date