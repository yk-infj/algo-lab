"""
benchmark.py — Algo Lab のソートアルゴリズムを実測ベンチマークするスクリプト。

index.html では各アルゴリズムの理論計算量(Big-O)を表示しているが、
このスクリプトは同じ4アルゴリズムをPythonで再実装し、配列サイズを変えながら
実際の実行時間を計測することで、理論値が実測でも成り立つことを検証する。

使い方:
    pip install matplotlib
    python3 benchmark.py

出力:
    benchmark_result.csv   各サイズ・各アルゴリズムの実行時間(秒)
    benchmark_chart.png    サイズ vs 実行時間のグラフ(理論曲線との比較)
"""

import time
import random
import csv
import copy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heapify(arr, n, root):
    largest = root
    l, r = 2 * root + 1, 2 * root + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


ALGORITHMS = {
    "bubble": bubble_sort,
    "quick": quick_sort,
    "merge": merge_sort,
    "heap": heap_sort,
}

SIZES = [100, 300, 600, 1000, 1500, 2200, 3000]


def run_benchmark():
    results = {name: [] for name in ALGORITHMS}
    for size in SIZES:
        base = [random.randint(0, 100000) for _ in range(size)]
        for name, fn in ALGORITHMS.items():
            data = copy.deepcopy(base)
            start = time.perf_counter()
            fn(data)
            elapsed = time.perf_counter() - start
            results[name].append(elapsed)
            print(f"size={size:5d}  {name:8s}  {elapsed*1000:8.2f} ms")
    return results


def save_csv(results):
    with open("benchmark_result.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["size"] + list(ALGORITHMS.keys()))
        for i, size in enumerate(SIZES):
            writer.writerow([size] + [results[name][i] for name in ALGORITHMS])


def save_chart(results):
    plt.figure(figsize=(8, 5))
    colors = {"bubble": "#f2545b", "quick": "#f2a93c", "merge": "#4c7ef5", "heap": "#4ade80"}
    for name, times in results.items():
        plt.plot(SIZES, times, marker="o", label=name, color=colors.get(name))
    plt.xlabel("Array size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Algo Lab — Empirical sort performance")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("benchmark_chart.png", dpi=150)
    print("Saved benchmark_chart.png")


if __name__ == "__main__":
    results = run_benchmark()
    save_csv(results)
    save_chart(results)
