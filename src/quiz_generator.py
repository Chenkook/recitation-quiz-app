import random
import re


class QuizQuestion:
    def __init__(self, question_id, prompt, correct_answer, blank_number=1, total_blanks=1, char_index=0, user_answer=None, is_correct=None):
        self.question_id = question_id
        self.prompt = prompt
        self.correct_answer = correct_answer
        self.blank_number = blank_number
        self.total_blanks = total_blanks
        self.char_index = char_index
        self.user_answer = user_answer
        self.is_correct = is_correct

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "prompt": self.prompt,
            "correct_answer": self.correct_answer,
            "blank_number": self.blank_number,
            "total_blanks": self.total_blanks,
            "char_index": self.char_index,
            "user_answer": self.user_answer,
            "is_correct": self.is_correct
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question_id"],
            data["prompt"],
            data["correct_answer"],
            data.get("blank_number", 1),
            data.get("total_blanks", 1),
            data.get("char_index", 0),
            data.get("user_answer"),
            data.get("is_correct")
        )


class QuizGenerator:
    def __init__(self):
        self.question_counter = 0

    def generate_quiz(self, text, difficulty=1):
        questions = []
        units = text.get_text_units()

        if text.language == "中文":
            questions = self._generate_chinese_quiz(units, text, difficulty)
        else:
            questions = self._generate_english_quiz(units, text, difficulty)

        return questions

    def _generate_chinese_quiz(self, units, text, difficulty):
        questions = []
        content = text.content
        chars = list(content)

        punctuation = "，。！？、；：“”‘’（）《》【】"
        blank_count = self._get_blank_count(difficulty, len(chars))

        valid_indices = [
            i for i, char in enumerate(chars)
            if char not in punctuation and not char.isspace()
        ]

        if len(valid_indices) < blank_count:
            blank_count = len(valid_indices)

        selected_indices = random.sample(valid_indices, min(blank_count, len(valid_indices)))
        selected_indices.sort()

        blank_chars = chars.copy()
        for i, idx in enumerate(selected_indices):
            blank_chars[idx] = f"【_{i+1}_】"

        full_prompt = "".join(blank_chars)

        for i, idx in enumerate(selected_indices):
            self.question_counter += 1
            correct_char = chars[idx]

            question = QuizQuestion(
                question_id=f"q_{self.question_counter}",
                prompt=full_prompt,
                correct_answer=correct_char,
                blank_number=i + 1,
                total_blanks=len(selected_indices),
                char_index=idx
            )
            questions.append(question)

        return questions

    def _generate_english_quiz(self, units, text, difficulty):
        questions = []
        content = text.content

        words = re.findall(r"\b[\w']+\b", content)

        word_positions = []
        current_pos = 0
        for word in words:
            pos = content.find(word, current_pos)
            if pos != -1:
                word_positions.append((pos, pos + len(word), word))
                current_pos = pos + len(word)

        blank_count = self._get_blank_count(difficulty, len(words))

        if len(word_positions) < blank_count:
            blank_count = len(word_positions)

        selected_positions = random.sample(word_positions, min(blank_count, len(word_positions)))
        selected_positions.sort(key=lambda x: x[0])

        blanked_content = content
        for i in reversed(range(len(selected_positions))):
            start, end, word = selected_positions[i]
            original_index = i + 1
            blank_label = f"[__{original_index}__]"
            blanked_content = blanked_content[:start] + blank_label + blanked_content[end:]

        full_prompt = blanked_content

        for i, (start, end, word) in enumerate(selected_positions):
            self.question_counter += 1

            question = QuizQuestion(
                question_id=f"q_{self.question_counter}",
                prompt=full_prompt,
                correct_answer=word,
                blank_number=i + 1,
                total_blanks=len(selected_positions),
                char_index=start
            )
            questions.append(question)

        return questions

    def _get_blank_count(self, difficulty, total_units):
        base_ratio = {
            1: 0.2,
            2: 0.4,
            3: 0.6
        }
        ratio = base_ratio.get(difficulty, 0.3)
        return max(1, int(total_units * ratio))