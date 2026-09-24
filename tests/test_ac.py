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
    assert ("hers", 2, 6) in r


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
    assert r.count(("ab", 0, 2)) == 2


def test_stats_fields():
    a = ACAutomaton()
    a.build(["ab", "abc", "bc"])
    st = a.stats()
    assert set(st.keys()) >= {"patterns", "nodes", "depth",
                              "max_fail_chain"}
    assert st["patterns"] == 3
    assert st["nodes"] >= 5
    assert st["depth"] == 3
    assert st["max_fail_chain"] >= 1


def test_long_text_linear():
    a = ACAutomaton()
    a.build(["cat", "dog"])
    r = a.find("catdog" * 500)
    assert len(r) == 1000


def test_streaming_feed():
    a = ACAutomaton()
    a.build(["he", "she"])
    got = []
    for ch in "ushers":
        got.extend(a.feed(ch))
    assert len(got) == 2
    assert ("she", 1, 4) in got
    assert ("he", 2, 4) in got


def test_feed_matches_find():
    a = ACAutomaton()
    a.build(["ab", "bab", "a"])
    text = "ababxab"
    a.reset()
    whole = a.find(text)
    a.reset()
    stream = []
    for ch in text:
        stream.extend(a.feed(ch))
    assert stream == whole


def test_feed_incremental():
    a = ACAutomaton()
    a.build(["ab", "b"])
    a.reset()
    assert a.feed("a") == []
    assert a.feed("b") == [("ab", 0, 2), ("b", 1, 2)]
    assert a.feed("c") == []
    assert a.feed("b") == [("b", 3, 4)]


def test_many_patterns():
    pats = ["k%04d" % i for i in range(1000)]
    a = ACAutomaton()
    a.build(pats)
    r = a.find("xxk0001xk0500xk0999xx")
    assert ("k0001", 2, 7) in r
    assert ("k0500", 8, 13) in r
    assert ("k0999", 14, 19) in r
    assert len(r) == 3


def test_fail_chain_max():
    a = ACAutomaton()
    a.build(["abcd", "bcd", "cd", "d"])
    assert a.stats()["max_fail_chain"] >= 3


def test_reset_isolation():
    a = ACAutomaton()
    a.build(["ab"])
    a.reset()
    a.feed("x")
    a.reset()
    got = [a.feed(c) for c in "ab"]
    assert got == [[], [("ab", 0, 2)]]


def test_chinese_patterns():
    a = ACAutomaton()
    a.build(["你好", "世界"])
    r = a.find("你好世界你好")
    assert r == [("你好", 0, 2), ("世界", 2, 4), ("你好", 4, 6)]


def test_add_pattern_incremental():
    a = ACAutomaton()
    a.build(["he", "she"])
    a.add_pattern("hers")
    r = a.find("ushers")
    assert ("she", 1, 4) in r
    assert ("he", 2, 4) in r
    assert ("hers", 2, 6) in r


def test_add_pattern_overlap():
    a = ACAutomaton()
    a.build(["ab"])
    a.add_pattern("bab")
    assert a.find("abab") == [("ab", 0, 2), ("bab", 1, 4), ("ab", 2, 4)]


def test_add_pattern_then_more():
    a = ACAutomaton()
    a.build(["he"])
    a.add_pattern("she")
    a.add_pattern("his")
    a.add_pattern("hers")
    r = a.find("ushers")
    assert ("she", 1, 4) in r
    assert ("he", 2, 4) in r
    assert ("hers", 2, 6) in r


def test_empty_pattern_ignored():
    a = ACAutomaton()
    a.build(["", "ab"])
    a.add_pattern("")
    assert a.find("ab") == [("ab", 0, 2)]
    assert a.stats()["patterns"] == 1


def test_long_overlap_pattern():
    a = ACAutomaton()
    a.build(["a" * 50])
    r = a.find("a" * 1000)
    assert len(r) == 951


def test_big_text_linear():
    pats = ["cat", "dog"] + ["k%04d" % i for i in range(998)]
    a = ACAutomaton()
    a.build(pats)
    r = a.find("catdog" * 8333)
    assert len(r) == 8333 * 2


def test_hit_order_insertion():
    a = ACAutomaton()
    a.build(["ab", "b"])
    assert a.find("ab") == [("ab", 0, 2), ("b", 1, 2)]


def test_unicode_mixed():
    a = ACAutomaton()
    a.build(["中文", "en", "中英混合"])
    r = a.find("xx中文en中英混合")
    assert ("中文", 2, 4) in r
    assert ("en", 4, 6) in r
    assert ("中英混合", 6, 10) in r


# ---------------- v4 新增：通配符与删除 ----------------

def test_wildcard_star_middle():
    a = ACAutomaton()
    a.build(["a*b"])
    assert a.find("axxxb") == [("a*b", 0, 5)]
    assert a.find("ab") == [("a*b", 0, 2)]       # * 匹配 0 字符


def test_wildcard_star_prefix():
    a = ACAutomaton()
    a.build(["*end"])
    # * 匹配 "xx"，整体跨度 (0,5)
    assert a.find("xxend") == [("*end", 0, 5)]


def test_wildcard_star_suffix():
    a = ACAutomaton()
    a.build(["start*"])
    assert a.find("startxx") == [("start*", 0, 7)]


def test_wildcard_qmark():
    a = ACAutomaton()
    a.build(["a?b"])
    assert a.find("aXb") == [("a?b", 0, 3)]
    assert a.find("ab") == []                     # ? 必须占一个字符


def test_wildcard_multi_star():
    a = ACAutomaton()
    a.build(["a*b*c"])
    assert a.find("aXbYc") == [("a*b*c", 0, 5)]


def test_wildcard_plain_mix():
    a = ACAutomaton()
    a.build(["ab", "a*b"])
    r = a.find("ab")
    assert r == [("ab", 0, 2), ("a*b", 0, 2)]


def test_wildcard_unicode():
    a = ACAutomaton()
    a.build(["中*文"])
    assert a.find("中间夹文") == [("中*文", 0, 4)]


def test_wildcard_no_match():
    a = ACAutomaton()
    a.build(["a*b"])
    assert a.find("acX") == []
    assert a.find("bxax") == []                   # b 在 a 前，不匹配


def test_wildcard_star_only():
    a = ACAutomaton()
    a.build(["*"])
    assert a.find("abc") == [("*", 0, 3)]


def test_remove_pattern():
    a = ACAutomaton()
    a.build(["ab", "b"])
    assert a.remove_pattern("b") is True
    assert a.find("ab") == [("ab", 0, 2)]
    assert a.stats()["patterns"] == 1


def test_remove_then_add():
    a = ACAutomaton()
    a.build(["ab", "b"])
    a.remove_pattern("ab")
    a.add_pattern("a")
    r = a.find("ab")
    assert ("b", 1, 2) in r
    assert ("a", 0, 1) in r
    assert ("ab", 0, 2) not in r


def test_remove_nonexistent():
    a = ACAutomaton()
    a.build(["ab"])
    assert a.remove_pattern("xyz") is False
    assert a.find("ab") == [("ab", 0, 2)]


def test_remove_duplicate():
    a = ACAutomaton()
    a.build(["ab", "ab"])
    a.remove_pattern("ab")
    r = a.find("ab")
    assert r.count(("ab", 0, 2)) == 1


def test_remove_wildcard():
    a = ACAutomaton()
    a.build(["a*b", "ab"])
    a.remove_pattern("a*b")
    assert a.find("axxb") == []
    assert a.find("ab") == [("ab", 0, 2)]


def test_combined_incremental():
    a = ACAutomaton()
    a.build(["he"])
    a.add_pattern("a?c")
    a.add_pattern("she")
    a.remove_pattern("he")
    r = a.find("ushersaxc")
    assert ("she", 1, 4) in r
    assert ("a?c", 6, 9) in r
    assert ("he", 2, 4) not in r
