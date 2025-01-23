# parimana

parimanaは、公営競技で、各出走者の能力が投票者からどう見積もられているか、公表されているオッズから算出します。
加えて、各投票券の的中確率と払戻金の期待値も計算します。

このリポジトリは https://parimana.net で公開予定のサービスのソースコードです。


## PC で動かす

### 必要ソフトウェア
* Docker
* Docker Compose

### 使い方

#### 起動

以下のコマンドで起動します。

```bash
docker compose up -d
```

ブラウザで http://localhost:8607/ にアクセスしてください。

しばらく待つと直近4日間の開催のレースカレンダーの取得がおわり、レースを選択できるようになります。
「オッズ取得＆計算」ボタンで レースオッズの取得と計算を行います。


#### 計算結果などのファイル
`.storage` 配下に作られます。
どんどん作られますが消されませんので、ジャマになりましたら随時消してください。


#### コマンドラインから操作

起動している状態でレースURL（例: "https://race.netkeiba.com/odds/index.html?race_id=202305021211" =2020年有馬記念）を指定して

```bash
docker compose exec command parimana analyse "https://race.netkeiba.com/odds/index.html?race_id=202305021211"
```

とすると指定したレースIDのオッズを収集して計算を行います。


```bash
docker compose exec command parimana analyse "https://race.netkeiba.com/odds/index.html?race_id=202305021211" -w
```

と -w フラグをつけると `.storage/out` 配下に 計算結果の excel,htmlファイルが作られます。


```bash
docker compose exec command parimana analyse -h
```

でそのほかに指定できるオプションが表示されます。


#### 終了
```
docker compose down
```
