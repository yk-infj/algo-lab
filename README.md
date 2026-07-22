# Algo Lab

![CI](https://github.com/<ユーザー名>/algo-lab/actions/workflows/ci.yml/badge.svg)

ソートアルゴリズムと経路探索アルゴリズムをブラウザ上でリアルタイムに可視化するインタラクティブ・デモです。GitHub Pages で即座に公開でき、URL一つで動くデモを見せられます。

## デモの見せ方

- **Sort タブ**: Bubble / Quick / Merge / Heap の4アルゴリズムをバーの動きで比較。比較回数・swap数・経過時間をライブ表示。
- **Pathfind タブ**: BFS / Dijkstra / A* の3アルゴリズムをグリッド上で可視化。壁をドラッグで描画し、探索の広がり方の違いを体感できる。
- 各アルゴリズムの計算量（Big-O）を画面下部に常時表示。

## 使っている技術

- Vanilla JavaScript（フレームワーク非依存、依存関係ゼロ）
- CSS Grid / Flexbox によるレイアウト
- 非同期処理(async/await)によるステップ実行アニメーション
- Python + matplotlib（`benchmark.py`）による実測ベンチマーク

## 実行方法

`index.html` をブラウザで開くだけ。ビルド不要。

```bash
# ローカルで開く
open index.html

# もしくは GitHub Pages で公開
# Settings > Pages > Branch: main / root で有効化
```

## benchmark.py — 理論値を実測で検証する

`index.html` は各アルゴリズムの理論計算量(Big-O)を表示するだけだが、
`benchmark.py` は同じ4アルゴリズムをPythonで再実装し、配列サイズを
100〜3000まで変化させながら実際の実行時間を計測する。

```bash
pip install matplotlib
python3 benchmark.py
```

`benchmark_chart.png`（実測グラフ）と `benchmark_result.csv`（生データ）が
生成される。Bubble Sortだけが指数的に遅くなっていく様子が一目でわかり、
フロントのビジュアライザーで見た「動き」が実測データでも裏付けられる。

## benchmark.html — ブラウザでPythonをその場で実行する

`benchmark.py` と同じロジックを、[Pyodide](https://pyodide.org/)(CPythonを
WebAssemblyにコンパイルしたランタイム)でブラウザ上でそのまま実行するページ。
サーバーもインストールも不要で、GitHub Pagesの `benchmark.html` を開くだけで
「Pythonが実際に動いている画面」をターミナル風の出力とライブグラフで見せられる。

## CI — GitHub Actions

`main` への push / PR のたびに自動で以下を実行する(`.github/workflows/ci.yml`)。

1. `pytest tests/` — 4アルゴリズムが正しくソートできているかを検証(空配列・単一要素・重複・逆順・ランダム配列など)
2. `python benchmark.py` — ベンチマーク自体が壊れていないかの回帰テストを兼ねて実行
3. 生成された `benchmark_chart.png` / `benchmark_result.csv` をActionsのArtifactとして保存

ローカルでテストだけ実行したい場合:

```bash
pip install pytest matplotlib
python -m pytest tests/ -v
```

## 今後の拡張案

- [ ] 挿入ソート・選択ソートの追加
- [ ] 迷路自動生成機能
- [ ] モバイル向けタッチ操作の最適化
