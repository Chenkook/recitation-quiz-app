# Intelligent Recitation Quiz System

## 智能背诵测验系统

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/liao/recitation-quiz-app)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A self-contained intelligent recitation quiz application that uses rule-based algorithms to generate practice tasks, check answers, track learning progress, recommend review, and motivate users through a simple profile and badge system.

本项目是一个本地运行的智能背诵测验系统，通过规则化算法生成练习任务、检查答案、记录学习进度、推荐复习，并通过用户档案和徽章系统提供学习激励。

## Features / 功能特性

- **User Profile**: Create and load learning profiles with streak tracking
- **Text Library**: Built-in texts and TXT import support (Chinese and English)
- **User Text Folder**: Dedicated folder for user-imported texts
- **Quiz Generation**: Fill-in-the-blank quizzes with progressive difficulty
- **Answer Checking**: Punctuation-ignored and case-insensitive answer validation
- **Single Character/Word Mode**: Input validation for single character (Chinese) or single word (English)
- **Progress Tracking**: Learning records, mistakes logging, and statistics
- **Review Scheduler**: Rule-based review recommendations with spaced repetition
- **Badge System**: 35 achievement badges across 9 categories for motivation
- **Dark Mode**: Light/dark theme switching
- **Report Export**: Quiz reports, badge certificates, and progress summaries

## Quick Start / 快速开始

### GUI Mode (Recommended)

```bash
cd recitation_quiz_app
python src/gui_launcher.py
```

### CLI Mode

```bash
cd recitation_quiz_app
python src/main.py
```

## Project Structure / 项目结构

```
recitation_quiz_app/
├── data/                    # Data files
│   ├── User Text/           # User-imported text files
│   ├── badges/              # Badge images (PNG)
│   ├── badges.json          # Badge definitions
│   ├── default_texts.json   # Built-in texts
│   └── users.json           # User profiles
├── src/                     # Source code
│   ├── gui/                 # GUI screens
│   │   ├── welcome.py       # Welcome screen (login/create profile)
│   │   ├── library.py       # Text library (browse, import, select)
│   │   ├── quiz_screen.py   # Quiz interface
│   │   ├── result.py        # Quiz results
│   │   ├── profile.py       # User profile
│   │   ├── badge_screen.py  # Badge collection
│   │   ├── review_screen.py # Review scheduler
│   │   └── main_window.py   # Main window manager
│   ├── gui_launcher.py      # GUI entry point
│   ├── main.py              # CLI entry point
│   ├── answer_checker.py    # Answer validation logic
│   ├── badge_manager.py     # Badge unlocking and management
│   ├── progress_tracker.py  # Learning statistics tracking
│   ├── quiz_generator.py    # Quiz generation algorithms
│   ├── report_exporter.py   # Report export functionality
│   ├── review_scheduler.py  # Review recommendation system
│   ├── text_manager.py      # Text loading and management
│   ├── theme_manager.py     # Light/dark theme management
│   └── user_profile.py      # User profile management
├── tests/                   # Unit tests
├── output/                  # Exported reports
│   ├── badges/              # Badge certificates
│   ├── quiz_reports/        # Individual quiz reports
│   └── stats/               # Learning statistics
└── docs/                    # Documentation
```

## Requirements / 环境要求

- Python 3.8+
- tkinter (built-in with Python)
- Pillow (for badge images)

## Installation / 安装

### From Source

```bash
git clone https://github.com/liao/recitation-quiz-app.git
cd recitation-quiz-app
pip install -e .
```

### Development Dependencies

```bash
pip install -e ".[dev]"
```

## Usage / 使用

```bash
# GUI Mode
recitation-quiz

# Or run directly
python src/gui_launcher.py

# CLI Mode
python src/main.py
```

## Testing / 测试

```bash
pytest tests/ -v
```

## Building / 打包

```bash
# Build source distribution
python -m build --sdist

# Build wheel
python -m build --wheel
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Version History

- **1.0.0** (2026-06-28) - Initial release with full features
  - User profile management
  - Text library with import support
  - Quiz generation and answer checking
  - Progress tracking and statistics
  - Review scheduler with spaced repetition
  - Badge system (35 badges across 9 categories)
  - Dark mode support
  - Report export functionality