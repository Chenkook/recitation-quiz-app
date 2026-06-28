import json
import os
import re


class LearningText:
    def __init__(self, text_id, title, language, category, difficulty, content):
        self.text_id = text_id
        self.title = title
        self.language = language
        self.category = category
        self.difficulty = difficulty
        self.content = content

    def to_dict(self):
        return {
            "text_id": self.text_id,
            "title": self.title,
            "language": self.language,
            "category": self.category,
            "difficulty": self.difficulty,
            "content": self.content
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["text_id"],
            data["title"],
            data["language"],
            data["category"],
            data["difficulty"],
            data["content"]
        )

    def get_text_units(self):
        if self.language == "中文":
            return list(self.content)
        else:
            return re.findall(r"[\w']+|[^\w\s]", self.content)


class TextManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.texts_file = os.path.join(data_dir, "default_texts.json")
        self.texts = []
        self._load_texts()

    def _load_texts(self):
        if os.path.exists(self.texts_file):
            with open(self.texts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.texts = [LearningText.from_dict(t) for t in data.get("texts", [])]

    def get_all_texts(self):
        return self.texts

    def get_text_by_id(self, text_id):
        for text in self.texts:
            if text.text_id == text_id:
                return text
        return None

    def get_texts_by_category(self, category):
        return [t for t in self.texts if t.category == category]

    def get_texts_by_language(self, language):
        return [t for t in self.texts if t.language == language]

    def import_txt_file(self, file_path, title, category, difficulty=1):
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            return None

        language = "中文" if re.search(r"[\u4e00-\u9fff]", content) else "English"

        existing_ids = [t.text_id for t in self.texts]
        new_id = f"imported_{len(existing_ids) + 1}"
        while new_id in existing_ids:
            new_id = f"imported_{len(existing_ids) + 1}"

        new_text = LearningText(new_id, title, language, category, difficulty, content)
        self.texts.append(new_text)
        self._save_texts()
        return new_text

    def _save_texts(self):
        data = {"texts": [t.to_dict() for t in self.texts]}
        with open(self.texts_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_categories(self):
        return sorted(set(t.category for t in self.texts))

    def get_languages(self):
        return sorted(set(t.language for t in self.texts))