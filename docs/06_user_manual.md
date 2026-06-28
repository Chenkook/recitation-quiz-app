# User Manual / 用户手册

## 1. Introduction / 介绍

The Intelligent Recitation Quiz System is a self-contained application designed to help users memorize texts through interactive quizzes. It supports both Chinese and English texts, provides progressive difficulty levels, and tracks learning progress with a badge system.

智能背诵测验系统是一个本地运行的应用程序，旨在通过互动测验帮助用户记忆文本。它支持中文和英文文本，提供递进式难度级别，并通过徽章系统跟踪学习进度。

## 2. Installation / 安装

### 2.1 Requirements

- Python 3.8 or higher
- No external dependencies required

### 2.2 Installation Steps

1. Download or clone the project files
2. Navigate to the project directory:

```bash
cd recitation_quiz_app
```

3. Run the application:

```bash
python src/main.py
```

## 3. Quick Start / 快速开始

### 3.1 First Launch

When you launch the application for the first time:

1. Select option "1" to create a new profile
2. Enter a username
3. You will be taken to the main menu

### 3.2 Main Menu Options

| Option | Description |
|--------|-------------|
| 1 | Start Quiz / 开始测验 |
| 2 | Text Library / 文本库 |
| 3 | Profile / 用户档案 |
| 4 | Badges / 徽章 |
| 5 | Review / 复习 |
| 6 | Import Text / 导入文本 |
| 7 | Export Report / 导出报告 |
| 8 | Save & Exit / 保存退出 |

## 4. Using the System / 使用系统

### 4.1 Starting a Quiz

1. From the main menu, select option "1" - Start Quiz
2. Select a text from the list by entering the number
3. Select difficulty:
   - 1 = Easy (20% blanks)
   - 2 = Medium (40% blanks)
   - 3 = Hard (60% blanks)
4. Answer each question by typing the missing character/word
5. After completing all questions, view your results

### 4.2 Understanding Quiz Results

After completing a quiz, you will see:

- **Score**: Your accuracy percentage
- **Correct**: Number of correct answers
- **Stars**: Stars earned (0-3)
  - 3 stars: 100% accuracy
  - 2 stars: 80%+ accuracy
  - 1 star: 60%+ accuracy
  - 0 stars: Below 60% accuracy
- **New Badges**: Any badges unlocked during this session

### 4.3 Text Library

Select option "2" to browse available texts:

- Texts are grouped by category
- Each text shows its title, language, and difficulty level

### 4.4 Importing Custom Texts

1. Select option "6" - Import Text
2. Enter the file path to your TXT file
3. Enter a title for the text
4. Enter a category (or press Enter for "Custom")
5. Enter difficulty (1-3)

**Supported formats**: Plain text (.txt) files encoded in UTF-8

### 4.5 Viewing Profile

Select option "3" to view your profile:

- Username
- Total quizzes completed
- Total questions answered
- Average accuracy
- Total stars earned
- Current and longest streak
- Practiced texts

### 4.6 Badges

Select option "4" to view badges:

| Badge | Description | Condition |
|-------|-------------|-----------|
| First Spark / 初燃之星 | Complete first quiz | 完成第一次测验 |
| Three-Day Flame / 三日微焰 | 3-day streak | 连续学习3天 |
| Seven-Day Scholar / 七日学者 | 7-day streak | 连续学习7天 |
| Precision Master / 精准大师 | Score 100% | 获得一次满分 |
| Memory Sprinter / 记忆冲刺者 | 10 quizzes | 完成10次测验 |
| Text Explorer / 文本探索者 | 5 different texts | 练习5篇不同文本 |

### 4.7 Review

Select option "5" to view texts due for review:

- Texts are sorted by days overdue
- Review intervals are based on your quiz accuracy

### 4.8 Exporting Reports

Select option "7" to export reports:

1. **Quiz Report**: Detailed report of a specific quiz
2. **Badge Certificate**: Certificate showing all earned badges
3. **Progress Summary**: Summary of your overall learning progress

Reports are saved to the `output/` directory.

## 5. Tips and Tricks / 提示与技巧

### 5.1 Effective Learning

- Start with Easy difficulty to build confidence
- Practice regularly to maintain your streak
- Review texts when they become due
- Try different texts to earn the Text Explorer badge

### 5.2 Answer Tips

- Chinese: Enter exactly one character per blank
- English: Answers are case-insensitive
- Punctuation is ignored, so you can skip commas and periods

### 5.3 Streak Tips

- Practice at least once per day to maintain your streak
- Your streak resets after 2+ days without practice
- Aim for the Seven-Day Scholar badge!

## 6. Troubleshooting / 故障排除

### 6.1 Common Issues

**Q: The application doesn't start**

A: Make sure you have Python 3.8+ installed and are running from the correct directory.

**Q: Chinese characters don't display correctly**

A: Ensure your terminal supports UTF-8 encoding. On Windows, use `chcp 65001` before running the application.

**Q: Imported texts don't appear**

A: Check that the file path is correct and the file is encoded in UTF-8.

**Q: Progress isn't saved**

A: Always use option "8" to save and exit properly.

### 6.2 Data Location

All data is stored locally in the `data/` directory:

- `users.json`: User profiles and progress
- `default_texts.json`: Built-in and imported texts
- `badges.json`: Badge definitions

## 7. FAQ / 常见问题

**Q: Can I use this offline?**

A: Yes! The system runs entirely offline with no external dependencies.

**Q: How many users can use the system?**

A: Multiple users can create separate profiles by choosing different usernames.

**Q: Can I delete my profile?**

A: Yes, manually delete your entry from `data/users.json`.

**Q: What happens if I lose my data files?**

A: Your progress will be lost. We recommend backing up the `data/` directory periodically.

## 8. Contact / 联系方式

For support or feedback, please contact the developer:

- **Name / 姓名**: Liao Chenkuo
- **Email / 邮箱**: littlekook@163.com