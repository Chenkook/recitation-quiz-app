# System Architecture / 系统架构

## 1. Architecture Overview / 架构概述

The system adopts a modular object-oriented architecture. Each module has one clear responsibility, which supports high cohesion and low coupling.

系统采用模块化、面向对象架构。每个模块负责一类明确任务，以体现高内聚、低耦合。

## 2. Overall Workflow / 总体流程

```
User Interface → User Profile Manager → Text Manager → Quiz Generator → Answer Checker → Progress Tracker → Review Scheduler → Badge Manager → Report Exporter

用户界面 → 用户档案管理 → 文本管理 → 测验生成 → 答案检查 → 学习进度记录 → 复习调度 → 徽章管理 → 报告导出
```

## 3. Module Descriptions / 模块描述

### 3.1 User Interface / 用户界面

**Responsibility**: Displays screens and collects user input

**职责**: 展示界面并收集用户输入

- Welcome screen
- Profile creation/loading
- Text library browsing
- Quiz interface
- Result display
- Badge page
- Review page

### 3.2 User Profile Manager / 用户档案管理模块

**Responsibility**: Creates, loads, updates, and saves user profiles

**职责**: 创建、读取、更新并保存用户档案

- Create new profile
- Load existing profile
- Save profile data
- Update streak information

### 3.3 Text Manager / 文本管理模块

**Responsibility**: Loads built-in texts and imported TXT files

**职责**: 读取内置文本和用户导入文件

- Load default texts from JSON
- Import external TXT files
- Categorize texts
- Manage text metadata

### 3.4 Quiz Generator / 测验生成模块

**Responsibility**: Generates fill-in-the-blank questions according to language and difficulty

**职责**: 按语言和难度生成填空测验

- Chinese character-based blanks
- English word-based blanks
- Difficulty-based blank count
- Random blank selection

### 3.5 Answer Checker / 答案检查模块

**Responsibility**: Normalizes answers, ignores punctuation, checks correctness, and calculates scores

**职责**: 标准化答案、忽略标点、判断正确性并计算分数

- Punctuation removal
- Case normalization (English)
- Fuzzy matching for spelling tolerance
- Score and star calculation

### 3.6 Progress Tracker / 学习进度记录模块

**Responsibility**: Stores quiz results, mistakes, dates, streaks, and learned texts

**职责**: 存储测验结果、错误、日期、连续学习天数和已学文本

- Record quiz results
- Track mistakes
- Calculate statistics
- Manage learning history

### 3.7 Review Scheduler / 复习调度模块

**Responsibility**: Uses rule-based intervals to recommend review

**职责**: 使用规则化时间间隔推荐复习

- Track last practice date
- Calculate next review date
- Identify overdue reviews
- Prioritize review items

### 3.8 Badge Manager / 徽章管理模块

**Responsibility**: Checks and unlocks badges based on progress

**职责**: 根据学习进度检查并解锁徽章

- Load badge definitions
- Check badge conditions
- Unlock earned badges
- Track badge status

### 3.9 Report Exporter / 报告导出模块

**Responsibility**: Exports quiz reports or simple badge certificates

**职责**: 导出测验报告或简单徽章证书

- Generate quiz reports
- Export badge certificates
- Create progress summaries
- Save reports to output directory

## 4. Data Flow Diagram / 数据流图

```
[User]
  │
  ▼
[User Interface]
  │
  ├──► [User Profile Manager] ◄──► [data/users.json]
  │
  ├──► [Text Manager] ◄──► [data/default_texts.json]
  │
  ├──► [Quiz Generator]
  │
  ├──► [Answer Checker]
  │
  ├──► [Progress Tracker]
  │
  ├──► [Review Scheduler]
  │
  ├──► [Badge Manager] ◄──► [data/badges.json]
  │
  └──► [Report Exporter] ► [output/]
```

## 5. Module Interaction / 模块交互

### 5.1 Quiz Flow

1. User selects text → Text Manager loads text
2. User selects difficulty → Quiz Generator creates questions
3. User answers questions → Answer Checker validates answers
4. Results calculated → Progress Tracker records results
5. Badge conditions checked → Badge Manager unlocks badges
6. Review scheduled → Review Scheduler sets next review date

### 5.2 Data Persistence

- User profiles stored in `data/users.json`
- Texts stored in `data/default_texts.json`
- Badge definitions stored in `data/badges.json`
- Reports exported to `output/` directory