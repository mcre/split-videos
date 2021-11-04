split-videos
=======================

動画ファイルを、指定した秒数より短くなるように分割します。

## 環境

* Docker

## 使い方

`./input` 以下に動画ファイルを配置しておきます。複数配置してもサブフォルダ以下に配置してもかまいません。

```
docker build -t ffmpeg-python .  # 最初の一度だけ実行
docker run --rm -v $(pwd):$(pwd) -w $(pwd) ffmpeg-python /bin/sh -c "python main.py 600"  # 600秒で分割する場合
```

`./output`に動画ファイルが出力されます。
指定した秒数ごとに分割されるわけではなく、上限を超えた場合にすべての動画が同じ秒数になるように分割されます。
動画がMetadataとしてdateを持っている場合は、2つ目以降のデータはそれ以前の動画の経過秒数を足した時間で更新されます。

## 連絡先

* [twitter: @m_cre](https://twitter.com/m_cre)

## License

* MIT
  + see LICENSE
