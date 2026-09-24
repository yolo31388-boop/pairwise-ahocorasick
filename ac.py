"""AC 自动机（Aho-Corasick）多模式匹配，支持流式逐字符输入。

模型：
- build(patterns)：Trie + BFS fail 指针 + output 沿 fail 链传递。
- find(text)：一次性匹配，返回全部命中 [(pattern, start, end)...]。
- feed(ch)：流式逐字符输入，只返回本字符位置触发的新命中；
  内部状态（当前节点、位置游标）跨调用保持。
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
        """构建 AC 自动机（Trie + fail 指针）。"""
        raise NotImplementedError

    def find(self, text: str) -> list:
        """一次性匹配，返回全部命中 [(pattern, start, end)...]。"""
        raise NotImplementedError

    def feed(self, ch: str) -> list:
        """流式输入一个字符，返回本位置触发的新命中。"""
        raise NotImplementedError

    def reset(self) -> None:
        """重置流式匹配状态（当前节点与位置）。"""
        raise NotImplementedError

    def stats(self) -> dict:
        """返回 {patterns, nodes, depth, max_fail_chain}。"""
        raise NotImplementedError
