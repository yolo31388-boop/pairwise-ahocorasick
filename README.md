# Pair-wise GSB 基线：AC 自动机多模式匹配

题目（feature 迭代）：实现 Aho-Corasick 多模式匹配引擎（Trie + fail 指针 + 线性扫描）。

- 骨架：`ac.py`（ACAutomaton 方法均 `raise NotImplementedError`）
- 验收：`python -m pytest tests/test_ac.py -q` 全绿
- 约束：只 import 标准库；必须真实构建 fail 指针（禁止每模式单独 find 后汇总）
