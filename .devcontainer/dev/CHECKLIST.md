# 統合 devcontainer の動作確認メモ

`dev` コンテナを新しく作ったときや、定義・土台の Dockerfile を変えたときに使う確認手順です。

## 前提

- back / front / infra の3つに分かれていた開発コンテナのうち、back と front を1つにまとめたものが `dev` です。
- 定義は `devcontainer.json` と `compose.yaml`、それに features のバージョンを固定する `devcontainer-lock.json`（初回ビルドで生成）です。作業ブランチは `feature/unified-devcontainer` でした。
- infra コンテナは別に残しています。back / front コンテナは、「確認が済んだあと」の手順で片付けるまで併存します。
- 土台は `back/Dockerfile` の `vscode-devcontainer` ステージ（Python + Chromium + Poetry）。Node 20、Terraform 1.10.3、AWS CLI、GitHub CLI、Claude Code は features で追加しています。
- ホストの `~/.aws`、`~/.ssh`、`docker.sock` は意図的にマウントしていません。
- features のインストールと `onCreateCommand` は、VS Code で開いたときに初めて走ります。`docker compose` でビルドと起動ができても、それだけでは確認になりません。
- 2026-11-22 に、1〜10 を確認済みです（11 と 12 は未確認）。

## 開き方

VS Code のコマンドパレットで「Dev Containers: Reopen in Container」を実行し、`Dev Container` を選びます。

既存の back / front コンテナが動いたままでも開けます。ただしポート 5005 / 5173 が重なるので、VS Code が別のローカルポートに振り替えることがあります。

## 1. ビルドが通るか

- [ ] features のインストールでエラーにならず、コンテナが開く

失敗した場合は、どの feature で止まったかをログで確認します。可能性が高いのは Node（`python:3.11-slim` ベースへの導入）です。

## 2. ツールが入っているか

```bash
python --version        # 3.11 系
poetry --version        # 1.7.1
node --version          # v20 系
npm --version
terraform version       # 1.10.3
aws --version
gh --version
claude --version
chromium --version
chromedriver --version
```

## 3. ユーザーとマウント

```bash
whoami                          # vscode
ls -ld ~/.aws ~/.claude         # どちらも vscode 所有（onCreateCommand の結果）
echo $CLAUDE_CONFIG_DIR         # /home/vscode/.claude
ls /var/run/docker.sock         # 「存在しない」が正しい
ls ~/.ssh                       # known_hosts だけなら正しい（鍵があってはいけない）
```

`~/.ssh/known_hosts` は、コンテナ作成時に VS Code がホストからコピーします。

## 4. git

```bash
cd /workspace
git status
ssh -T git@github.com   # 「Hi <ユーザー名>!」と出れば、SSH エージェントの転送が効いている
```

`ssh -T` が失敗する場合は、ホスト側で SSH エージェントに鍵が載っているかを確認します。

## 5. back

```bash
cd /workspace/back
poetry install
poetry run pytest
poetry run flake8 --extend-exclude .venv
python -c "import socket; socket.create_connection(('task-db', 6379), 2); print('redis ok')"
```

venv がプロジェクト内（`back/.venv`）にあり、`.flake8` に除外の設定がないため、`--extend-exclude .venv` を付けないと依存パッケージまで検査します。2026-11-22 時点では、W292（ファイル末尾の改行なし）が2件出ます。コンテナとは関係ありません。

## 6. front

```bash
cd /workspace/front
npm ci
npm run lint
npm run build.dev
```

2026-11-22 時点では、`npm run lint` は失敗します。eslint を v9 に上げたのに、設定が旧形式の `.eslintrc.cjs` のままだからです（v9 には `eslint.config.js` が必要）。コンテナとは関係ありません。

## 7. parimana 本体の動作

ここが本題です。実際のサイトからオッズを取得するので、ネットワークと Chromium の両方が要ります。

### 7-1. コマンドラインで1レース分析する

```bash
cd /workspace/back
poetry run parimana analyse "https://race.netkeiba.com/odds/index.html?race_id=202305021211" -w
```

- [ ] オッズの取得（Chromium / chromedriver の起動を含む）がエラーなく終わる
- [ ] 計算結果と推奨が端末に表示される
- [ ] `back/.storage/out/` に Excel と HTML（chance / box_plot / mds）が出力される

ワーカーを介さずその場で実行されるので、スクレイピングと計算だけを切り分けて確認できます。Chromium まわりで失敗する場合は、まずここで再現します。

### 7-2. 画面から一通り動かす

ターミナルを3つ使います。

```bash
# 1: ワーカー（起動時にレースカレンダーの取得が走る）
cd /workspace/back && poetry run parimana worker

# 2: Web API（5005 番）
cd /workspace/back && poetry run parimana web

# 3: フロントの開発サーバー（5173 番）
cd /workspace/front && npm run dev
```

- [ ] `http://localhost:5005/docs` で API の一覧が開く
- [ ] `http://localhost:5173` で画面が開く
- [ ] しばらく待つと、直近の開催のレースを選択できるようになる（ワーカーと Redis が動いている証拠）
- [ ] レースを選んで「オッズ取得＆計算」を押すと、進捗が表示され、結果のグラフと表が出る
- [ ] 画面を再読み込みしても、計算済みの結果が表示される（`back/.storage/store/` に保存されている）

データの保存先は、起動したディレクトリからの相対パス（`.storage/`）です。必ず `back/` で起動します。

## 8. IaC

```bash
cd /workspace
terraform fmt -check -recursive infra ci_cd
cd infra/iac/env/prod
export TF_DATA_DIR=$(mktemp -d)
terraform init -backend=false
terraform validate
```

`TF_DATA_DIR` を一時ディレクトリに向けるのは、infra コンテナで作った `.terraform/` に S3 バックエンドの設定が残っているためです。そのままだと `-backend=false` を付けても資格情報を探しに行き、失敗します。

2026-11-22 時点では、`fmt -check` が9ファイルで通りません（`=` の位置がずれているだけ）。コンテナとは関係ありません。

資格情報なしでできるのはここまでです。`plan` と `apply` は infra コンテナか CI/CD で行います。

## 9. Claude Code

- [ ] ターミナルで `claude` を起動してログインできる
- [ ] VS Code の Claude Code 拡張のパネルが開く
- [ ] `ls -a ~/.claude` に `.claude.json` がある（ボリューム内に保存されている）

ホスト側のメモリと会話履歴は引き継がれません。作業パスが `/home/wsluser/git/parimana` から `/workspace` に変わるためです。

## 10. AWS と GitHub

```bash
aws configure                 # 読み取り中心の弱い資格情報を入れる
aws sts get-caller-identity
gh auth login                 # リビルドのたびに必要（意図どおり）
```

管理者権限の資格情報は、このコンテナには入れません。

## 11. リビルドしても残るか

「Dev Containers: Rebuild Container」を実行したあとで確認します。

- [ ] `claude` が再ログインなしで使える
- [ ] `aws sts get-caller-identity` がそのまま通る
- [ ] `gh auth status` は未ログインに戻っている

## 12. エディタ

ルート（`/workspace`）を開くので、`back/.vscode/settings.json` は読まれません。次の点で困ったら、`devcontainer.json` の `customizations.vscode.settings` に必要な分だけ足します。

- [ ] Python のインタープリタに `back/.venv` が選ばれる
- [ ] flake8 が `back/.flake8`（1行 88 文字）に従っている
- [ ] テストエクスプローラーが `back/tests` を見つける
- [ ] front の `.tsx` で eslint が動く

足す候補は `python.defaultInterpreterPath`、`python.testing.cwd`、`flake8.cwd`、`black-formatter.cwd`、`eslint.workingDirectories` です。

## 確認が済んだあと

1. `devcontainer.json`、`compose.yaml`、`devcontainer-lock.json` と、このメモをコミットする。
2. 既存の back / front コンテナを片付ける。
   - `.devcontainer/back/`、`.devcontainer/front/`、`.devcontainer/compose.yaml` を削除
   - `front/Dockerfile` の `vscode-devcontainer` ステージを削除
   - ホストで `docker compose -p parimana_devcontainer down` を実行して、古いコンテナを止める
3. Poetry から uv へ移行する（別作業）。`back/Dockerfile` の `poetry` ステージを差し替えてリビルドすれば、このコンテナも uv になります。

infra コンテナは、`ci_cd` の構築など強い権限が要る作業用に残します。
