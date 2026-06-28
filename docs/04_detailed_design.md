# Detailed Design / 详细设计

## 1. Data Model / 数据模型

### 1.1 UserProfile / 用户档案

| Field | Type | Description |
|-------|------|-------------|
| username | str | 用户名 |
| current_streak | int | 当前连续学习天数 |
| longest_streak | int | 最长连续学习天数 |
| total_quizzes | int | 完成测验总数 |
| stars | int | 获得星星总数 |
| badges | list | 已解锁徽章列表 |
| learning_records | list | 学习记录列表 |
| last_practice_date | date | 上次练习日期 |

### 1.2 LearningText / 学习文本

| Field | Type | Description |
|-------|------|-------------|
| text_id | str | 文本唯一标识 |
| title | str | 标题 |
| language | str | 语言 (中文/English) |
| category | str | 分类 |
| difficulty | int | 难度级别 |
| content | str | 文本内容 |

### 1.3 QuizQuestion / 测验题目

| Field | Type | Description |
|-------|------|-------------|
| question_id | str | 题目唯一标识 |
| prompt | str | 题目提示（含空白） |
| correct_answer | str | 正确答案 |
| user_answer | str | 用户答案 |
| is_correct | bool | 是否正确 |

### 1.4 QuizResult / 测验结果

| Field | Type | Description |
|-------|------|-------------|
| text_id | str | 关联文本标识 |
| date | date | 测验日期 |
| score | float | 得分 |
| correct_count | int | 正确数量 |
| total_count | int | 总题数 |
| mistakes | list | 错误记录列表 |
| stars_earned | int | 本次获得星星数 |

### 1.5 Badge / 徽章

| Field | Type | Description |
|-------|------|-------------|
| badge_id | str | 徽章唯一标识 |
| name | str | 徽章名称 |
| condition | str | 解锁条件 |
| unlocked_date | date | 解锁日期 |

### 1.6 ReviewRecord / 复习记录

| Field | Type | Description |
|-------|------|-------------|
| text_id | str | 关联文本标识 |
| last_practiced_date | date | 上次练习日期 |
| next_review_date | date | 下次复习日期 |
| review_status | str | 复习状态 |

## 2. Class Design / 类设计

### 2.1 UserProfile Class

**File**: `src/user_profile.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(username)` | username: str | None | 初始化用户档案 |
| `to_dict()` | None | dict | 转换为字典 |
| `from_dict(data)` | data: dict | UserProfile | 从字典创建 |
| `update_streak()` | None | None | 更新连续学习天数 |
| `add_quiz(stars_earned)` | stars_earned: int | None | 添加测验记录 |
| `add_badge(badge_id)` | badge_id: str | bool | 添加徽章 |

### 2.2 UserProfileManager Class

**File**: `src/user_profile.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(data_dir)` | data_dir: str | None | 初始化管理器 |
| `create_profile(username)` | username: str | UserProfile | 创建新档案 |
| `load_profile(username)` | username: str | UserProfile | 加载档案 |
| `save_profile(user)` | user: UserProfile | bool | 保存档案 |
| `get_all_usernames()` | None | list | 获取所有用户名 |

### 2.3 LearningText Class

**File**: `src/text_manager.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(text_id, title, language, category, difficulty, content)` | various | None | 初始化文本 |
| `to_dict()` | None | dict | 转换为字典 |
| `from_dict(data)` | data: dict | LearningText | 从字典创建 |
| `get_text_units()` | None | list | 获取文本单位 |

### 2.4 TextManager Class

**File**: `src/text_manager.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(data_dir)` | data_dir: str | None | 初始化管理器 |
| `get_all_texts()` | None | list | 获取所有文本 |
| `get_text_by_id(text_id)` | text_id: str | LearningText | 根据ID获取文本 |
| `get_texts_by_category(category)` | category: str | list | 按分类获取文本 |
| `get_texts_by_language(language)` | language: str | list | 按语言获取文本 |
| `import_txt_file(file_path, title, category, difficulty)` | various | LearningText | 导入TXT文件 |
| `get_categories()` | None | list | 获取所有分类 |
| `get_languages()` | None | list | 获取所有语言 |

### 2.5 QuizQuestion Class

**File**: `src/quiz_generator.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(question_id, prompt, correct_answer, user_answer, is_correct)` | various | None | 初始化题目 |
| `to_dict()` | None | dict | 转换为字典 |
| `from_dict(data)` | data: dict | QuizQuestion | 从字典创建 |

### 2.6 QuizGenerator Class

**File**: `src/quiz_generator.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__()` | None | None | 初始化生成器 |
| `generate_quiz(text, difficulty)` | text: LearningText, difficulty: int | list | 生成测验题目 |
| `_generate_chinese_quiz(units, text, difficulty)` | various | list | 生成中文测验 |
| `_generate_english_quiz(units, text, difficulty)` | various | list | 生成英文测验 |
| `_get_blank_count(difficulty, total_units)` | difficulty: int, total_units: int | int | 计算空白数量 |

### 2.7 AnswerChecker Class

**File**: `src/answer_checker.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__()` | None | None | 初始化检查器 |
| `check_answer(user_answer, correct_answer, language)` | various | bool | 检查答案正确性 |
| `_normalize_answer(answer, language)` | answer: str, language: str | str | 标准化答案 |
| `_check_similarity(user, correct)` | user: str, correct: str | bool | 检查相似度 |
| `calculate_score(questions)` | questions: list | tuple | 计算分数和星星 |
| `_calculate_stars(accuracy)` | accuracy: float | int | 计算星星数量 |

### 2.8 ProgressTracker Class

**File**: `src/progress_tracker.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(user_profile)` | user_profile: UserProfile | None | 初始化追踪器 |
| `record_quiz(text_id, score, correct_count, total_count, mistakes, stars_earned)` | various | QuizResult | 记录测验结果 |
| `get_progress_by_text(text_id)` | text_id: str | list | 获取文本进度 |
| `get_all_records()` | None | list | 获取所有记录 |
| `get_total_stats()` | None | dict | 获取统计数据 |
| `get_practiced_texts()` | None | set | 获取已练习文本 |
| `get_mistakes(text_id)` | text_id: str | list | 获取错误记录 |

### 2.9 ReviewScheduler Class

**File**: `src/review_scheduler.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(user_profile)` | user_profile: UserProfile | None | 初始化调度器 |
| `update_after_quiz(text_id, accuracy)` | text_id: str, accuracy: float | None | 更新复习计划 |
| `get_due_reviews()` | None | list | 获取到期复习 |
| `get_review_status(text_id)` | text_id: str | str | 获取复习状态 |
| `get_next_review_date(text_id)` | text_id: str | date | 获取下次复习日期 |

### 2.10 BadgeManager Class

**File**: `src/badge_manager.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(user_profile, data_dir)` | various | None | 初始化管理器 |
| `check_badges()` | None | list | 检查并解锁徽章 |
| `get_unlocked_badges()` | None | list | 获取已解锁徽章 |
| `get_all_badges()` | None | list | 获取所有徽章 |
| `get_badge_by_id(badge_id)` | badge_id: str | Badge | 根据ID获取徽章 |
| `is_badge_unlocked(badge_id)` | badge_id: str | bool | 检查徽章是否解锁 |
| `get_next_badge()` | None | Badge | 获取下一个徽章 |

### 2.11 ReportExporter Class

**File**: `src/report_exporter.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(user_profile, text_manager, output_dir)` | various | None | 初始化导出器 |
| `export_quiz_report(quiz_result, questions)` | various | str | 导出测验报告 |
| `export_badge_certificate()` | None | str | 导出徽章证书 |
| `export_progress_summary()` | None | str | 导出进度汇总 |

## 3. Algorithm Design / 算法设计

### 3.1 Quiz Generation

1. **Identify text units** (Chinese: characters, English: words)
2. **Determine blank count** based on difficulty (20%, 40%, 60%)
3. **Randomly select valid positions** (exclude punctuation and spaces)
4. **Replace selected units with numbered blanks**:
   - Chinese format: `【_1_】` for the first blank, `【_2_】` for the second, etc.
   - English format: `[__1__]` for the first blank, `[__2__]` for the second, etc.
5. **Generate question objects** with blank positions tracked
6. **Process from right to left** to avoid position shifts during replacement

**Example Output:**
- Chinese: `床前【_1_】光，疑【_2_】地上【_3_】`
- English: `Hello [__1__]! [__2__] are you?`

**Single-fill Mode:**
- Each quiz session presents one blank at a time
- User fills one character (Chinese) or one word (English) per submission
- Filled answers are displayed in the text as the user progresses
- Current blank number is clearly indicated in the UI

### 3.2 Answer Checking

1. Normalize user and correct answers
2. Remove punctuation from both answers
3. Convert to lowercase for English
4. Compare normalized answers
5. Apply fuzzy matching for English (1 character tolerance)

### 3.3 Score Calculation

| Accuracy | Stars |
|----------|-------|
| >= 100% | 3 |
| >= 80% | 2 |
| >= 60% | 1 |
| < 60% | 0 |

### 3.4 Review Scheduling

1. Determine interval based on accuracy:
   - 0-19%: 1 day
   - 20-39%: 1 day
   - 40-59%: 3 days
   - 60-79%: 7 days
   - 80-99%: 14 days
   - 100%: 30 days
2. Calculate next review date
3. Store in review records

### 3.5 Badge Unlocking

#### 🌱 Journey Badges / 学习旅程

| Badge ID | Condition |
|----------|-----------|
| first_spark | total_quizzes >= 1 |
| rising_ember | total_quizzes >= 5 |
| memory_sprinter | total_quizzes >= 10 |
| dedicated_learner | total_quizzes >= 50 |
| master_of_recitation | total_quizzes >= 100 |

#### 🔥 Streak Badges / 连续学习

| Badge ID | Condition |
|----------|-----------|
| three_day_flame | current_streak >= 3 |
| seven_day_scholar | current_streak >= 7 |
| half_month_guardian | current_streak >= 15 |
| monthly_keeper | current_streak >= 30 |
| hundred_day_legend | current_streak >= 100 |
| eternal_flame | current_streak >= 365 |

#### ⭐ Star Collection / 星星收集

| Badge ID | Condition |
|----------|-----------|
| bright_beginning | total_stars >= 10 |
| shining_learner | total_stars >= 50 |
| constellation_builder | total_stars >= 100 |
| galaxy_explorer | total_stars >= 300 |
| celestial_master | total_stars >= 1000 |

#### 📖 Text Mastery / 文本精通

| Badge ID | Condition |
|----------|-----------|
| text_explorer | practiced 5+ different texts |
| library_wanderer | practiced 20+ different texts |
| knowledge_collector | practiced 50+ different texts |

#### 🏆 Perfect Performance / 高分表现

| Badge ID | Condition |
|----------|-----------|
| precision_master | any record with score >= 100 |
| perfect_duo | two consecutive perfect scores |
| unbreakable_accuracy | five perfect scores total |

#### 📚 Persistence on One Text / 专注精神

| Badge ID | Condition |
|----------|-----------|
| faithful_reader | same text practiced 5 times |
| patient_scholar | same text practiced 10 times |
| text_guardian | same text practiced 20 times |
| memory_artisan | same text mastered (20 successful attempts) |

#### 🎯 Difficulty Badges / 难度挑战

| Badge ID | Condition |
|----------|-----------|
| easy_beginner | 3 stars in Easy mode |
| normal_challenger | 3 stars in Medium mode |
| hard_conqueror | 3 stars in Hard mode |
| ultimate_challenger | 3 stars in all difficulty levels |

#### 🔄 Review Badges / 复习习惯

| Badge ID | Condition |
|----------|-----------|
| never_forget | completed first scheduled review |
| memory_keeper | completed 10 review sessions |
| review_veteran | completed 50 review sessions |

#### 🌟 Special Badges / 隐藏成就

| Badge ID | Condition |
|----------|-----------|
| night_owl | complete quiz after 10:00 PM |
| early_bird | complete quiz before 7:00 AM |
| marathon_learner | finish 10 quizzes in one day |
| comeback_hero | return after 30 days inactive |

## 4. File Structure / 文件结构

```
recitation_quiz_app/
├── data/
│   ├── default_texts.json
│   ├── users.json
│   └── badges.json
├── src/
│   ├── main.py
│   ├── gui_launcher.py
│   ├── user_profile.py
│   ├── text_manager.py
│   ├── quiz_generator.py
│   ├── answer_checker.py
│   ├── progress_tracker.py
│   ├── review_scheduler.py
│   ├── badge_manager.py
│   ├── report_exporter.py
│   └── gui/
│       ├── main_window.py
│       ├── welcome.py
│       ├── library.py
│       ├── quiz_screen.py
│       ├── result.py
│       ├── profile.py
│       ├── badge_screen.py
│       └── review_screen.py
├── tests/
│   ├── test_answer_checker.py
│   ├── test_quiz_generator.py
│   └── test_badge_manager.py
├── output/
│   ├── quiz_reports/
│   └── badges/
└── docs/
    ├── 01_requirement_analysis.md
    ├── 02_use_case_analysis.md
    ├── 03_system_architecture.md
    ├── 04_detailed_design.md
    ├── 05_testing_report.md
    └── 06_user_manual.md
```

## 5. GUI Design / 图形界面设计

### 5.1 GUI Architecture

The GUI layer is built using Python's built-in tkinter library. It follows a screen-based architecture where each screen is a separate class extending `tk.Frame`. The `MainWindow` class acts as the central controller, managing screen transitions and sharing managers between screens.

**Architecture Pattern:**
- MainWindow (central controller)
- Screen classes (WelcomeScreen, LibraryScreen, etc.)
- Managers are passed to each screen for business logic

### 5.2 GUI Classes

#### 5.2.1 MainWindow Class

**File**: `src/gui/main_window.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(managers)` | managers: dict | None | 初始化主窗口 |
| `show_screen(screen_name, **kwargs)` | screen_name: str | None | 切换到指定屏幕 |
| `run()` | None | None | 启动主循环 |

#### 5.2.2 WelcomeScreen Class

**File**: `src/gui/welcome.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(parent, managers)` | various | None | 初始化欢迎屏幕 |
| `_create_profile()` | None | None | 创建新档案 |
| `_load_profile()` | None | None | 加载已有档案 |

#### 5.2.3 LibraryScreen Class

**File**: `src/gui/library.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(parent, managers)` | various | None | 初始化文本库屏幕 |
| `_select_text()` | None | None | 选择文本 |
| `_start_quiz()` | None | None | 开始测验 |
| `_import_text()` | None | None | 导入文本 |

#### 5.2.4 QuizScreen Class

**File**: `src/gui/quiz_screen.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(parent, managers)` | various | None | 初始化测验屏幕 |
| `_start_quiz()` | None | None | 开始测验 |
| `_show_question()` | None | None | 显示题目 |
| `_submit_answer()` | None | None | 提交答案 |
| `_finish_quiz()` | None | None | 完成测验 |

**Quiz Interaction Design / 测验交互设计**

**5.2.4.1 Blank Numbering / 空编号显示**

- Each blank position in the quiz is assigned a unique number (1, 2, 3, ...)
- For Chinese texts: Each character position that needs to be filled is numbered
- For English texts: Each word position that needs to be filled is numbered
- Display format: `__1__`, `__2__`, `__3__` etc.
- Example (Chinese): `床前__1__光，疑__2__地上__3__`
- Example (English): `Hello __1__! __2__ are you?`

**5.2.4.2 Current Blank Indication / 当前填空提示**

- When displaying each question, the system clearly indicates which blank number the user is currently filling
- The label shows: `Fill blank #X / 填写第 X 个空:`
- The current blank is displayed with special formatting in the text

**5.2.4.3 Answer Validation / 答案验证**

**Chinese Mode / 中文模式:**
- User must enter exactly 1 Chinese character per blank
- If user enters 0 characters: Show warning "Please enter an answer"
- If user enters more than 1 character: Show warning "Single character mode: Please enter exactly 1 character"
- Invalid input does not advance to next question; input field is cleared and focus remains

**English Mode / 英文模式:**
- User must enter exactly 1 word per blank (no spaces allowed)
- If user enters 0 characters: Show warning "Please enter an answer"
- If user enters multiple words (contains space): Show warning "Single word mode: Please enter exactly 1 word"
- Invalid input does not advance to next question; input field is cleared and focus remains

**5.2.4.4 Answer Display After Submission / 提交后答案显示**

- After a valid answer is submitted and the user advances to the next question:
- The previously filled blank is replaced with the user's answer in the display text
- The current blank is highlighted with its number
- Other unfilled blanks remain as numbered placeholders
- Example progression:
  - Question 1: `床前__1__光，疑__2__地上__3__` → User enters "明"
  - Question 2: `床前明光，疑__2__地上__3__` → User enters "是"
  - Question 3: `床前明光，疑是地上__3__` → User enters "霜"

#### 5.2.5 ResultScreen Class

**File**: `src/gui/result.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(parent, managers)` | various | None | 初始化结果屏幕 |
| `_retry()` | None | None | 重试测验 |
| `_go_back()` | None | None | 返回文本库 |

#### 5.2.6 ProfileScreen Class

**File**: `src/gui/profile.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(parent, managers)` | various | None | 初始化档案屏幕 |
| `_go_back()` | None | None | 返回文本库 |

#### 5.2.7 BadgeScreen Class

**File**: `src/gui/badge_screen.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(parent, managers)` | various | None | 初始化徽章屏幕 |
| `_export_certificate()` | None | None | 导出证书 |
| `_go_back()` | None | None | 返回文本库 |

#### 5.2.8 ReviewScreen Class

**File**: `src/gui/review_screen.py`

| Method | Input | Output | Description |
|--------|-------|--------|-------------|
| `__init__(parent, managers)` | various | None | 初始化复习屏幕 |
| `_practice_selected()` | None | None | 练习选中文本 |
| `_go_back()` | None | None | 返回文本库 |

### 5.3 GUI Launcher

**File**: `src/gui_launcher.py`

The GUI entry point that initializes all managers and starts the MainWindow.

```python
python src/gui_launcher.py
```