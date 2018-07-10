# boostnumpy_lifegame
Boost.numpy を使って、numpy で高速にライフゲームを実装してみる。

実行環境
-----
- Python3
- numpy
- OpenCV
- Boost 1.67


設定
-----
- CELL_SIZE : セルの個数。100 にすると 100 x 100 で実行。
- DISPLAY_CELL_RATIO : 1つのセルの大きさ。CELL_SIZE が小さい時に大きくして表示すると見やすい。
- MUTATE_RATIO : 指定された割合でセルを反転させる。


内容
-----
### only_python
- 速度比較用に Python3 版を作成した。  
実行するだけで動かせる。qで終了。
```sh
$ python3 lifegame.py
```

### boost_numpy
Boost.numpy 実装版。実行にはビルドが必要。  
  
ビルドについては、CMakeLists.txt が /opt/boost_1.67.0 に Boost があること前提で書かれているので、場合によっては修正する。
```sh
$ mkdir build
$ cd build
$ cmake -DCMAKE_BUILD_TYPE=Release ..
$ make
```

実行は only_python の場合と同じ。
```sh
$ python3 lifegame.py
```

