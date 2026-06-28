# Testing Report / 测试报告

## 1. Testing Overview / 测试概述

This document describes the unit tests for the Intelligent Recitation Quiz System. The tests cover the core modules: Answer Checker, Quiz Generator, and Badge Manager.

本文档描述智能背诵测验系统的单元测试。测试覆盖核心模块：答案检查器、测验生成器和徽章管理器。

## 2. Test Environment / 测试环境

- Python Version: 3.8+
- Operating System: Windows
- Testing Framework: Built-in unittest

## 3. Test Cases / 测试用例

### 3.1 Answer Checker Tests

**File**: `tests/test_answer_checker.py`

| Test Name | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_check_answer_chinese` | 测试中文答案检查 | 正确答案返回True，错误答案返回False |
| `test_check_answer_english` | 测试英文答案检查（含大小写和拼写容错） | 忽略大小写，支持1个字符拼写容错 |
| `test_calculate_score` | 测试分数计算和星星奖励 | 根据正确率计算分数和星星 |

#### 3.1.1 test_check_answer_chinese

| Test Case | User Answer | Correct Answer | Language | Expected |
|-----------|-------------|----------------|----------|----------|
| 完全匹配 | 床 | 床 | 中文 | True |
| 完全匹配（多字） | 明月光 | 明月光 | 中文 | True |
| 错误答案 | 明 | 床 | 中文 | False |
| 长度不同 | 床前 | 床 | 中文 | False |
| 空答案 | "" | "" | 中文 | True |
| None答案 | None | "" | 中文 | True |
| 含标点 | 床前明月光， | 床前明月光 | 中文 | True |
| 含空格 | " 床前明月光 " | 床前明月光 | 中文 | True |

#### 3.1.2 test_check_answer_english

| Test Case | User Answer | Correct Answer | Language | Expected |
|-----------|-------------|----------------|----------|----------|
| 完全匹配 | hello | hello | English | True |
| 大写 | Hello | hello | English | True |
| 全大写 | HELLO | hello | English | True |
| 少1字符 | hell | hello | English | True |
| 1字符错误 | helo | hello | English | True |
| 多1字符 | hellow | hello | English | True |
| 完全不同 | world | hello | English | False |
| 含标点 | hello, | hello | English | True |
| 含空格 | "  hello  " | hello | English | True |

#### 3.1.3 test_calculate_score

| Test Case | Correct/Total | Accuracy | Expected Stars |
|-----------|--------------|----------|----------------|
| 全部正确 | 3/3 | 100% | 3 |
| 部分正确 | 2/3 | 66.7% | 1 |
| 全部错误 | 0/2 | 0% | 0 |
| 80%正确率 | 4/5 | 80% | 2 |

### 3.2 Quiz Generator Tests

**File**: `tests/test_quiz_generator.py`

| Test Name | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_generate_chinese_quiz` | 测试中文测验生成 | 生成有效题目，空白位置合理 |
| `test_generate_english_quiz` | 测试英文测验生成 | 生成有效题目，空白位置合理 |
| `test_difficulty_progression` | 测试难度递进 | 难度越高，空白数量越多 |
| `test_quiz_question_to_dict` | 测试题目序列化 | 正确转换为字典 |

#### 3.2.1 test_generate_chinese_quiz

- Input: Chinese text "床前明月光，疑是地上霜。"
- Expected: 生成1-6个题目（简单难度约20%空白）
- Each question contains "__" placeholder
- Correct answer is a single Chinese character

#### 3.2.2 test_generate_english_quiz

- Input: English text "Hello world, this is a test."
- Expected: 生成有效题目
- Each question contains "____" placeholder
- Correct answer is an English word

#### 3.2.3 test_difficulty_progression

- Input: Same text with different difficulties
- Expected: Easy <= Medium <= Hard blank count

### 3.3 Badge Manager Tests

**File**: `tests/test_badge_manager.py`

| Test Name | Description | Expected Result |
|-----------|-------------|-----------------|
| `test_first_spark_badge` | 测试初燃之星徽章解锁 | 完成第一次测验后解锁 |
| `test_streak_badges` | 测试连续打卡徽章 | 3天和7天连续后解锁 |
| `test_precision_master_badge` | 测试精准大师徽章 | 获得满分后解锁 |
| `test_memory_sprinter_badge` | 测试记忆冲刺者徽章 | 完成10次测验后解锁 |
| `test_text_explorer_badge` | 测试文本探索者徽章 | 练习5篇不同文本后解锁 |
| `test_get_next_badge` | 测试下一个徽章推荐 | 返回下一个未解锁的徽章 |

## 4. Test Execution / 测试执行

### 4.1 Running Tests

```bash
cd recitation_quiz_app

# Run all tests
python -m pytest tests/ -v

# Run individual test files
python tests/test_answer_checker.py
python tests/test_quiz_generator.py
python tests/test_badge_manager.py
```

### 4.2 Expected Test Results

| Test File | Expected Pass | Expected Fail |
|-----------|--------------|---------------|
| test_answer_checker.py | 3 | 0 |
| test_quiz_generator.py | 4 | 0 |
| test_badge_manager.py | 6 | 0 |
| **Total** | **13** | **0** |

## 5. Test Coverage / 测试覆盖

### 5.1 Module Coverage

| Module | Coverage | Description |
|--------|----------|-------------|
| AnswerChecker | High | 答案检查、标准化、分数计算 |
| QuizGenerator | High | 中文/英文测验生成、难度递进 |
| BadgeManager | High | 徽章解锁条件检查 |
| UserProfile | Medium | 通过其他模块测试间接覆盖 |
| TextManager | Medium | 通过其他模块测试间接覆盖 |
| ProgressTracker | Medium | 通过其他模块测试间接覆盖 |
| ReviewScheduler | Medium | 通过其他模块测试间接覆盖 |
| ReportExporter | Low | 需补充测试 |

### 5.2 Key Test Scenarios

- ✅ Chinese character-based answer checking
- ✅ English word-based answer checking with case insensitivity
- ✅ English spelling tolerance (1 character)
- ✅ Punctuation handling
- ✅ Score calculation with star rewards
- ✅ Quiz generation for Chinese texts
- ✅ Quiz generation for English texts
- ✅ Difficulty-based blank count
- ✅ Badge unlocking logic
- ✅ Streak tracking

## 6. Known Issues / 已知问题

- ReportExporter module lacks dedicated tests
- Integration tests for complete quiz flow needed
- Edge cases for very short texts need testing

## 7. Future Testing / 未来测试

- Add integration tests for complete user workflow
- Add tests for ReportExporter module
- Add tests for ReviewScheduler module
- Add performance tests for large text files
- Add error handling tests