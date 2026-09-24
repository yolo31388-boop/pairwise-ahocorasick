# Pair-wise GSB 基线：AC 自动机（通配符 + 动态增删 + 流式）

题目（feature 迭代）：实现 Aho-Corasick 多模式匹配引擎，支持通配符模式（* / ?）、动态 add/remove 与流式输入。

- 骨架：`ac.py`（ACAutomaton 方法均 `raise NotImplementedError`）
- 验收：`python -m pytest tests/test_ac.py -q` 全绿
- 约束：只 import 标准库；必须真实构建 fail 指针（禁止每模式单独 find 后汇总）
