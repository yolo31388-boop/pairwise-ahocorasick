"""AC 自动机（Aho-Corasick）多模式匹配，支持通配符与动态增删。

模型：
- 普通模式（不含 * 和 ?）构建 Trie + BFS fail 指针，AC 匹配。
- 通配模式：'*' 匹配任意长度字符序列（含 0），'?' 匹配恰好 1 个
  任意字符；按 * 分段 + 段窗口匹配（最短匹配，首尾锚定语义见
  tests）。
- build(patterns) / add_pattern(p) / remove_pattern(p) 动态维护；
  find(text) 返回全部命中 [(pattern, start, end)...] 按
  (start, end, 插入序) 排序；feed(ch) 流式（普通模式）。
- stats()：{patterns, nodes, depth, max_fail_chain}。
"""
from __future__ import annotations


class ACAutomaton:
    def __init__(self):
        # nodes[i] = {"children": {ch: idx}, "fail": int, "output": [pattern_idx]}
        self.nodes: list[dict] = []
        self.patterns: list[str] = []
        self._cur = 0
        self._pos = 0

    # -------------------------------------------------- 接口
    def build(self, patterns: list[str]) -> None:
        """构建（空模式忽略；含 * 或 ? 的模式按通配处理）。"""
        raise NotImplementedError

    def add_pattern(self, pattern: str) -> None:
        """增量追加单个模式并重建（空模式忽略）。"""
        raise NotImplementedError

    def remove_pattern(self, pattern: str) -> bool:
        """删除第一次出现的该模式并重建；不存在返回 False。"""
        raise NotImplementedError

    def find(self, text: str) -> list:
        """一次性匹配，返回全部命中 [(pattern, start, end)...]。"""
        raise NotImplementedError

    def feed(self, ch: str) -> list:
        """流式输入一个字符（普通模式），返回本位置触发的新命中。"""
        raise NotImplementedError

    def reset(self) -> None:
        """重置流式匹配状态。"""
        raise NotImplementedError

    def stats(self) -> dict:
        """返回 {patterns, nodes, depth, max_fail_chain}。"""
        raise NotImplementedError
