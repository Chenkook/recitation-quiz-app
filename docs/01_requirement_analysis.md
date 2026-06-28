# Requirement Analysis / 需求分析

## 1. Why the System Exists / 系统开发原因

The system exists because memorization and recitation often become repetitive and passive. Learners may reread materials many times without active recall. This system turns text memorization into an interactive process with feedback, review, and visible learning progress.

开发本系统的原因在于，背诵和记忆过程常常容易变得重复、被动。学习者可能反复阅读材料，却缺少主动回忆。本系统将文本记忆转化为带反馈、复习和进度可视化的互动过程。

## 2. Target Users / 目标用户

- Students who need to memorize poems, classical texts, vocabulary passages, speeches, or definitions
- 需要背诵诗歌、古文、词汇段落、演讲片段或定义的学生
- Teachers who want a lightweight tool to turn texts into practice quizzes
- 希望将文本快速转化为练习测验的教师
- Language learners who need repeated recall practice
- 需要进行反复回忆训练的语言学习者

## 3. Core User Needs / 核心用户需求

- Users need a simple way to load texts and start practice quickly
- 用户需要一种简单方式快速读取文本并开始练习
- Users need feedback on correctness and mistakes
- 用户需要看到正确率和错误内容反馈
- Users need motivation to continue practicing over time
- 用户需要持续练习的激励机制
- Users need local records so that their learning history can build up gradually
- 用户需要本地记录，让学习历史逐步积累

## 4. Functional Requirements / 功能需求

### 4.1 User Management

- Create or load a user learning profile
- 创建或读取用户学习档案

### 4.2 Learning Materials

- Load built-in learning texts
- 读取内置学习文本
- Import external TXT files
- 支持导入外部 TXT 文件

### 4.3 Quiz System

- Generate quizzes by hiding Chinese characters or English words
- 通过隐藏中文汉字或英文单词生成测验

### 4.4 Answer Checking

- Check answers automatically and calculate scores
- 自动检查答案并计算分数

### 4.5 Learning Records

- Save learning records, mistakes, scores, and dates locally
- 本地保存学习记录、错误、分数和日期

### 4.6 Motivation System

- Show stars, streaks, badges, and review reminders
- 展示星星、连续打卡、徽章和复习提醒

### 4.7 Report Export

- Export a simple report or badge certificate
- 导出简单学习报告或徽章证书

## 5. Non-functional Requirements / 非功能需求

- The system should run offline without external API dependence
- 系统应能离线运行，不依赖外部 API
- The architecture should be object-oriented and modular
- 系统架构应采用面向对象和模块化设计
- The interface should be simple and easy to use
- 界面应简洁、易用
- The project should be easy to test, maintain, and extend
- 项目应便于测试、维护和扩展
- Data should be stored in readable local files such as JSON or TXT
- 数据应存储在 JSON 或 TXT 等可读本地文件中

## 6. Design Scope / 设计范围

### In Scope / 本版本包含

| Feature | Description |
|---------|-------------|
| User profile creation and loading | 用户档案创建与读取 |
| Built-in text library and TXT import | 内置文本库与 TXT 导入 |
| Fill-in-the-blank and progressive recitation quizzes | 填空与递进式背诵测验 |
| Answer checking with punctuation ignored | 忽略标点的答案检查 |
| Stars, streaks, and simple badges | 星星、连续打卡与简单徽章 |
| Local progress storage and report export | 本地进度存储与报告导出 |

### Out of Scope / 本版本暂不包含

| Feature | Description |
|---------|-------------|
| Speech or audio recognition | 语音或音频识别 |
| External LLM or cloud API calls | 外部大语言模型或云端 API |
| Complex online account system | 复杂联网账号系统 |
| Advanced graphical game system | 复杂图形化游戏系统 |
| Mobile app synchronization | 移动端同步 |
| Large-scale database deployment | 大型数据库部署 |