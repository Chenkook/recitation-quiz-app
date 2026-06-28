import os
import json
from datetime import date, datetime


class ReportExporter:
    def __init__(self, user_profile, text_manager, output_dir="output"):
        self.user_profile = user_profile
        self.text_manager = text_manager
        self.output_dir = output_dir
        self.quiz_reports_dir = os.path.join(output_dir, "quiz_reports")
        self.badges_dir = os.path.join(output_dir, "badges")
        self.stats_dir = os.path.join(output_dir, "stats")
        self._ensure_dirs()

    def _ensure_dirs(self):
        os.makedirs(self.quiz_reports_dir, exist_ok=True)
        os.makedirs(self.badges_dir, exist_ok=True)
        os.makedirs(self.stats_dir, exist_ok=True)

    def export_quiz_report(self, quiz_result, questions):
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        today = date.today().isoformat()
        filename = f"quiz_report_{today}_{timestamp}_{quiz_result.text_id}.txt"
        filepath = os.path.join(self.quiz_reports_dir, filename)

        text = self.text_manager.get_text_by_id(quiz_result.text_id)
        text_title = text.title if text else quiz_result.text_id

        report_lines = [
            "=" * 50,
            "Quiz Report / 测验报告",
            "=" * 50,
            f"Date / 日期: {today}",
            f"Text / 文本: {text_title}",
            f"Score / 得分: {quiz_result.score}%",
            f"Correct / 正确: {quiz_result.correct_count}/{quiz_result.total_count}",
            f"Stars Earned / 获得星星: {'★' * quiz_result.stars_earned}",
            ""
        ]

        if questions and text:
            quiz_version = questions[0].prompt
            user_version = questions[0].prompt
            correct_version = questions[0].prompt

            for question in questions:
                blank_num = getattr(question, 'blank_number', 1)
                if text.language == "中文":
                    placeholder = f"【_{blank_num}_】"
                else:
                    placeholder = f"[__{blank_num}__]"
                
                user_answer = question.user_answer or ""
                correct_char = question.correct_answer

                if text.language == "中文":
                    if user_answer:
                        user_version = user_version.replace(placeholder, user_answer, 1)
                    else:
                        user_version = user_version.replace(placeholder, "_", 1)
                    correct_version = correct_version.replace(placeholder, correct_char, 1)
                else:
                    if user_answer:
                        user_version = user_version.replace(placeholder, user_answer, 1)
                    else:
                        user_version = user_version.replace(placeholder, "_" * len(correct_char), 1)
                    correct_version = correct_version.replace(placeholder, correct_char, 1)
        else:
            original_text = text.content if text else ""
            quiz_version = original_text
            user_version = original_text
            correct_version = original_text

        report_lines.extend([
            "--- Quiz / 测验题目 ---",
            quiz_version,
            "",
            "--- Your Answer / 你的答案 ---",
            user_version,
            "",
            "--- Correct Answer / 正确答案 ---",
            correct_version,
            "",
            "--- Question Details / 题目详情 ---",
            ""
        ])

        all_correct = True
        for i, question in enumerate(questions, 1):
            blank_num = getattr(question, 'blank_number', i)
            status = "✓ Correct" if question.is_correct else "✗ Wrong"
            if not question.is_correct:
                all_correct = False

            report_lines.extend([
                f"Blank #{blank_num}:",
                f"   Your answer / 你的答案: {question.user_answer or '未作答'}",
                f"   Correct answer / 正确答案: {question.correct_answer}",
                f"   Result / 结果: {status}",
                ""
            ])

        if all_correct:
            report_lines.extend([
                "--- All answers correct! / 全部回答正确！ ---",
                ""
            ])

        report_lines.append("=" * 50)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        self._update_cumulative_stats(quiz_result, questions)

        return filepath

    def _update_cumulative_stats(self, quiz_result, questions):
        stats_file = os.path.join(self.stats_dir, f"text_stats_{self.user_profile.username}.json")

        if os.path.exists(stats_file):
            with open(stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
        else:
            stats = {}

        text_id = quiz_result.text_id

        if text_id not in stats:
            stats[text_id] = {
                "text_id": text_id,
                "total_quizzes": 0,
                "total_correct": 0,
                "total_questions": 0,
                "avg_accuracy": 0,
                "blank_stats": {}
            }

        stats[text_id]["total_quizzes"] += 1
        stats[text_id]["total_correct"] += quiz_result.correct_count
        stats[text_id]["total_questions"] += quiz_result.total_count

        if stats[text_id]["total_questions"] > 0:
            stats[text_id]["avg_accuracy"] = round(
                (stats[text_id]["total_correct"] / stats[text_id]["total_questions"]) * 100, 1
            )

        for question in questions:
            char_index = getattr(question, 'char_index', 0)
            correct_char = question.correct_answer

            if char_index not in stats[text_id]["blank_stats"]:
                stats[text_id]["blank_stats"][char_index] = {
                    "correct_char": correct_char,
                    "correct": 0,
                    "wrong": 0,
                    "wrong_answers": []
                }

            if question.is_correct:
                stats[text_id]["blank_stats"][char_index]["correct"] += 1
            else:
                stats[text_id]["blank_stats"][char_index]["wrong"] += 1
                wrong_answer = question.user_answer or "未作答"
                if wrong_answer not in stats[text_id]["blank_stats"][char_index]["wrong_answers"]:
                    stats[text_id]["blank_stats"][char_index]["wrong_answers"].append(wrong_answer)

        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    def export_text_progress_report(self, text_id):
        stats_file = os.path.join(self.stats_dir, f"text_stats_{self.user_profile.username}.json")

        if not os.path.exists(stats_file):
            return None

        with open(stats_file, "r", encoding="utf-8") as f:
            stats = json.load(f)

        if text_id not in stats:
            return None

        text_stats = stats[text_id]
        text = self.text_manager.get_text_by_id(text_id)
        text_title = text.title if text else text_id

        today = date.today().isoformat()
        filename = f"text_progress_{text_id}_{today}.txt"
        filepath = os.path.join(self.quiz_reports_dir, filename)

        report_lines = [
            "=" * 60,
            "Text Progress Report / 文章学习进度报告",
            "=" * 60,
            f"Date / 日期: {today}",
            f"Text / 文本: {text_title}",
            f"Total Quizzes / 测验次数: {text_stats['total_quizzes']}",
            f"Total Correct / 正确总数: {text_stats['total_correct']}",
            f"Total Questions / 题目总数: {text_stats['total_questions']}",
            f"Average Accuracy / 平均正确率: {text_stats['avg_accuracy']}%",
            ""
        ]

        if text_stats["blank_stats"]:
            report_lines.extend([
                "--- Blank Statistics / 填空统计 ---",
                ""
            ])
            for char_index in sorted(text_stats["blank_stats"].keys()):
                blank = text_stats["blank_stats"][char_index]
                correct_char = blank.get("correct_char", "?")
                total = blank["correct"] + blank["wrong"]
                accuracy = round((blank["correct"] / total) * 100, 1) if total > 0 else 0
                report_lines.extend([
                    f"Position {char_index} (Correct: '{correct_char}'):",
                    f"   Correct / 正确: {blank['correct']}",
                    f"   Wrong / 错误: {blank['wrong']}",
                    f"   Accuracy / 正确率: {accuracy}%",
                    f"   Wrong Answers / 错误答案: {', '.join(blank['wrong_answers']) if blank['wrong_answers'] else 'None'}",
                    ""
                ])

        report_lines.append("=" * 60)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        return filepath

    def export_badge_certificate(self):
        today = date.today().isoformat()
        filename = f"badge_certificate_{self.user_profile.username}_{today}.txt"
        filepath = os.path.join(self.badges_dir, filename)

        unlocked_badges = []
        if hasattr(self.user_profile, 'badges'):
            unlocked_badges = self.user_profile.badges

        report_lines = [
            "=" * 60,
            "BADGE CERTIFICATE / 徽章证书",
            "=" * 60,
            f"Username / 用户名: {self.user_profile.username}",
            f"Date / 日期: {today}",
            f"Total Stars / 总星星: {self.user_profile.stars}",
            f"Current Streak / 当前连续: {self.user_profile.current_streak} days",
            f"Longest Streak / 最长连续: {self.user_profile.longest_streak} days",
            f"Total Quizzes / 测验总数: {self.user_profile.total_quizzes}",
            "",
            "--- Unlocked Badges / 已解锁徽章 ---",
            ""
        ]

        if unlocked_badges:
            for badge_id in unlocked_badges:
                report_lines.append(f"✓ {badge_id}")
        else:
            report_lines.append("No badges unlocked yet / 暂无解锁徽章")

        report_lines.extend([
            "",
            "=" * 60,
            "Keep learning and unlock more badges! / 继续学习，解锁更多徽章！",
            "=" * 60
        ])

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        return filepath

    def export_progress_summary(self):
        today = date.today().isoformat()
        filename = f"progress_summary_{self.user_profile.username}_{today}.txt"
        filepath = os.path.join(self.quiz_reports_dir, filename)

        total_questions = sum(r["total_count"] for r in self.user_profile.learning_records)
        total_correct = sum(r["correct_count"] for r in self.user_profile.learning_records)
        avg_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0

        report_lines = [
            "=" * 60,
            "Progress Summary / 学习进度汇总",
            "=" * 60,
            f"Username / 用户名: {self.user_profile.username}",
            f"Date / 日期: {today}",
            "",
            "--- Statistics / 统计数据 ---",
            f"Total Quizzes / 测验总数: {self.user_profile.total_quizzes}",
            f"Total Questions / 题目总数: {total_questions}",
            f"Total Correct / 正确总数: {total_correct}",
            f"Average Accuracy / 平均正确率: {avg_accuracy:.1f}%",
            f"Total Stars / 总星星: {self.user_profile.stars}",
            f"Current Streak / 当前连续: {self.user_profile.current_streak} days",
            f"Longest Streak / 最长连续: {self.user_profile.longest_streak} days",
            "",
            "--- Learning Records / 学习记录 ---",
            ""
        ]

        records = sorted(
            self.user_profile.learning_records,
            key=lambda r: r["date"],
            reverse=True
        )

        for i, record in enumerate(records[:10], 1):
            text = self.text_manager.get_text_by_id(record["text_id"])
            title = text.title if text else record["text_id"]
            report_lines.append(
                f"{i}. {record['date']} - {title}: {record['correct_count']}/{record['total_count']} ({record['score']}%)"
            )

        if len(records) > 10:
            report_lines.append(f"... and {len(records) - 10} more records")

        report_lines.append("=" * 60)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        return filepath