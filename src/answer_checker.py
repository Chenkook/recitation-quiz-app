import re


class AnswerChecker:
    def __init__(self):
        self.punctuation = "，。！？、；：“”‘’（）《》【】,.!?;:'\"()[]{}<> "

    def check_answer(self, user_answer, correct_answer, language="中文"):
        user_normalized = self._normalize_answer(user_answer, language)
        correct_normalized = self._normalize_answer(correct_answer, language)

        if user_normalized == correct_normalized:
            return True

        if language == "English":
            return self._check_similarity(user_normalized, correct_normalized)

        return False

    def _normalize_answer(self, answer, language):
        if answer is None:
            return ""

        answer = str(answer).strip()

        for p in self.punctuation:
            answer = answer.replace(p, "")

        if language == "English":
            answer = answer.lower()

        return answer

    def _check_similarity(self, user, correct):
        if len(correct) == 0:
            return len(user) == 0

        if len(user) == len(correct) and user != correct:
            differences = sum(1 for a, b in zip(user, correct) if a != b)
            return differences <= 1

        if abs(len(user) - len(correct)) <= 1:
            if len(user) < len(correct):
                user, correct = correct, user

            for i in range(len(user)):
                if user[:i] + user[i+1:] == correct:
                    return True

        return False

    def calculate_score(self, questions):
        total = len(questions)
        if total == 0:
            return 0, 0, 0, 0

        correct_count = sum(1 for q in questions if q.is_correct)
        accuracy = (correct_count / total) * 100
        stars = self._calculate_stars(accuracy)

        return correct_count, total, round(accuracy, 1), stars

    def _calculate_stars(self, accuracy):
        if accuracy >= 100:
            return 3
        elif accuracy >= 80:
            return 2
        elif accuracy >= 60:
            return 1
        else:
            return 0