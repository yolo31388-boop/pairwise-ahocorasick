import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ac import ACAutomaton  # noqa: E402


def test_single_pattern():
    a = ACAutomaton()
    a.build(["abc"])
    assert a.find("xxabcxx") == [("abc", 2, 5)]


def test_multiple_patterns():
    a = ACAutomaton()
    a.build(["he", "she"])
    # ushers: u s h e r s -> "she"@(1,4) 与 "he"@(2,4) 重叠
    r = a.find("ushers")
    assert ("she", 1, 4) in r
    assert ("he", 2, 4) in r
    assert len(r) == 2


def test_overlapping_matches():
    a = ACAutomaton()
    a.build(["ab", "bab"])
    r = a.find("abab")
    assert r == [("ab", 0, 2), ("bab", 1, 4), ("ab", 2, 4)]


def test_classic_ushers_full():
    a = ACAutomaton()
    a.build(["he", "she", "his", "hers"])
    r = a.find("ushers")
    assert ("she", 1, 4) in r
    assert ("he", 2, 4) in r
    assert ("hers", 2, 6) in r     # 跨 fail 链命中更长模式


def test_repeated_overlapping():
    a = ACAutomaton()
    a.build(["aa"])
    assert a.find("aaaa") == [("aa", 0, 2), ("aa", 1, 3), ("aa", 2, 4)]


def test_no_match():
    a = ACAutomaton()
    a.build(["xyz"])
    assert a.find("abcdef") == []


def test_empty_text():
    a = ACAutomaton()
    a.build(["a", "ab"])
    assert a.find("") == []


def test_single_char_pattern():
    a = ACAutomaton()
    a.build(["a", "b"])
    r = a.find("ab")
    assert r == [("a", 0, 1), ("b", 1, 2)]


def test_duplicate_patterns():
    a = ACAutomaton()
    a.build(["ab", "ab"])
    r = a.find("ab")
    assert r.count(("ab", 0, 2)) == 2     # 重复模式各命中一次


def test_stats_fields():
    a = ACAutomaton()
    a.build(["ab", "abc", "bc"])
    st = a.stats()
    assert set(st.keys()) >= {"patterns", "nodes", "depth"}
    assert st["patterns"] == 3
    assert st["nodes"] >= 5              # 根 + ab + abc + bc 前缀共享
    assert st["depth"] == 3              # 最长模式 3


def test_long_text_linear():
    a = ACAutomaton()
    a.build(["cat", "dog"])
    text = "catdog" * 500
    r = a.find(text)
    assert len(r) == 1000                # cat 与 dog 各 500 次
