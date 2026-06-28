# Use Case Analysis / 用例分析

## 1. Main Actor / 主要参与者

The main actor is the **Learner** (学习者). The learner interacts with the system by loading a profile, selecting or importing a text, completing quizzes, viewing results, and reviewing previous learning materials.

主要参与者是学习者。学习者通过读取档案、选择或导入文本、完成测验、查看结果和复习历史材料与系统交互。

## 2. Use Case List / 用例列表

### 2.1 Create or Load Profile / 创建或读取档案

| Item | Description |
|------|-------------|
| User Action | Enter username / 输入用户名 |
| System Response | Load existing data or create new profile / 读取已有数据或创建新档案 |

### 2.2 Select Text / 选择文本

| Item | Description |
|------|-------------|
| User Action | Choose built-in text or import TXT / 选择内置文本或导入 TXT |
| System Response | Load text content and metadata / 读取文本内容和元数据 |

### 2.3 Start Quiz / 开始测验

| Item | Description |
|------|-------------|
| User Action | Choose practice mode and difficulty / 选择练习模式和难度 |
| System Response | Generate missing-word or missing-character questions / 生成缺词或缺字题 |

### 2.4 Submit Answers / 提交答案

| Item | Description |
|------|-------------|
| User Action | Type missing words or characters / 输入缺失单词或汉字 |
| System Response | Check answers and record mistakes / 检查答案并记录错误 |

### 2.5 View Report / 查看报告

| Item | Description |
|------|-------------|
| User Action | Finish quiz / 完成测验 |
| System Response | Show score, mistakes, stars, and suggestions / 显示分数、错误、星星和建议 |

### 2.6 Review Reminder / 复习提醒

| Item | Description |
|------|-------------|
| User Action | Open app later / 之后再次打开系统 |
| System Response | Recommend due texts based on review rules / 根据复习规则推荐文本 |

### 2.7 View Achievements / 查看成就

| Item | Description |
|------|-------------|
| User Action | Open profile or badge page / 打开档案或徽章页面 |
| System Response | Display streaks, badges, total quizzes, and learned texts / 展示连续天数、徽章、总测验数和已学文本 |

## 3. Use Case Diagram Summary / 用例图概述

```
Learner ──► Create/Load Profile
Learner ──► Select Text
Learner ──► Start Quiz
Learner ──► Submit Answers
Learner ──► View Report
Learner ──► Review Reminder
Learner ──► View Achievements
```

## 4. User Workflow / 用户流程

```
First launch
    ↓
Create or Load Profile
    ↓
Welcome Page
    ↓
Choose Text (Text Library)
    ↓
Generate Quiz
    ↓
Answer Questions
    ↓
Receive Report (Result Page)
    ↓
Update Progress
    ↓
Unlock Badge (if applicable)
    ↓
Return Home
```

## 5. Business Rules / 业务规则

### 5.1 Quiz Rules

- For Chinese texts, blanks are individual characters
- 中文文本以汉字为单位生成空白
- For English texts, blanks are complete words
- 英文文本以完整单词为单位生成空白
- Difficulty controls blank count: Easy (20%), Medium (40%), Hard (60%)
- 难度控制空白数量：简单(20%)、中等(40%)、困难(60%)

### 5.2 Answer Rules

- Punctuation is ignored when checking answers
- 检查答案时忽略标点
- English answers are case-insensitive
- 英文答案不区分大小写
- Minor spelling tolerance for English (1 character difference)
- 英文支持轻微拼写容错（1个字符差异）

### 5.3 Streak Rules

- Streak increases by 1 for consecutive days of practice
- 连续练习天数增加连续打卡数
- Streak resets to 1 after a gap of 2+ days
- 间隔超过1天，连续打卡重置为1

### 5.4 Review Rules

- Review intervals: 1, 3, 7, 14, 30 days based on accuracy
- 根据正确率确定复习间隔：1天、3天、7天、14天、30天

### 5.5 Badge Rules

| Badge | Condition |
|-------|-----------|
| First Spark | Complete first quiz |
| Three-Day Flame | 3-day streak |
| Seven-Day Scholar | 7-day streak |
| Precision Master | Score 100% once |
| Memory Sprinter | Complete 10 quizzes |
| Text Explorer | Practice 5 different texts |