"""AC 自动机（Aho-Corasick）多模式匹配。

模型：
- build(patterns)：把所有模式插入 Trie；BFS 构建 fail 指针；
  节点 output 列表记录在该节点终结的模式索引，并沿 fail 链
  继承可达的输出（标准 output 传递）。
- find(text)：线性扫描文本（O(len))，走 Trie + fail 回退，
  返回全部命中 [(pattern, start, end)...]（含重叠命中）。
"""
from __future__ import annotations


class ACAutomaton:
    def __init__(self):
        # nodes[i] = {"children": {ch: idx}, "fail": int, "output": [pattern_idx]}
        self.nodes: list[dict] = []
        self.patterns: list[str] = []

    # -------------------------------------------------- 接口
    def build(self, patterns: list[str]) -> None:
        """构建 AC 自动机（Trie + fail 指针）。"""
        raise NotImplementedError

    def find(self, text: str) -> list:
        """返回全部命中 [(pattern, start, end)...]，含重叠。"""
        raise NotImplementedError

    def stats(self) -> dict:
        """返回 {patterns, nodes, depth}。"""
        raise NotImplementedError
