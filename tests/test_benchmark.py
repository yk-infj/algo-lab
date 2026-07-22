"""
test_benchmark.py — benchmark.py の各ソート関数が正しくソートできているかを検証する。

CI (GitHub Actions) からは `pytest` コマンドで自動実行される。
"""

import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark import bubble_sort, quick_sort, merge_sort, heap_sort, ALGORITHMS


ALL_SORTERS = [bubble_sort, quick_sort, merge_sort, heap_sort]


def test_empty_array():
    for sort_fn in ALL_SORTERS:
        assert sort_fn([]) == []


def test_single_element():
    for sort_fn in ALL_SORTERS:
        assert sort_fn([42]) == [42]


def test_already_sorted():
    data = [1, 2, 3, 4, 5]
    for sort_fn in ALL_SORTERS:
        assert sort_fn(data.copy()) == [1, 2, 3, 4, 5]


def test_reverse_sorted():
    data = [5, 4, 3, 2, 1]
    for sort_fn in ALL_SORTERS:
        assert sort_fn(data.copy()) == [1, 2, 3, 4, 5]


def test_duplicates():
    data = [3, 1, 2, 3, 1, 2, 3]
    for sort_fn in ALL_SORTERS:
        assert sort_fn(data.copy()) == sorted(data)


def test_random_arrays_match_builtin_sorted():
    random.seed(42)
    for _ in range(20):
        data = [random.randint(-500, 500) for _ in range(random.randint(1, 200))]
        expected = sorted(data)
        for sort_fn in ALL_SORTERS:
            assert sort_fn(data.copy()) == expected, f"{sort_fn.__name__} failed"


def test_all_algorithms_registered():
    # index.html 側のセレクトボックスと名前がずれていないかの防止線
    assert set(ALGORITHMS.keys()) == {"bubble", "quick", "merge", "heap"}
