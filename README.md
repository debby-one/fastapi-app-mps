# FastAPI アプリケーション

このリポジトリには、FastAPI を使用して構築されたシンプルな Web アプリケーションが含まれています。PostgreSQL データベースに接続し、テストデータを操作するエンドポイントを提供します。

## 目次

- [プロジェクト概要](#プロジェクト概要)
- [前提条件](#前提条件)
- [セットアップ](#セットアップ)
- [Docker Compose を使用した実行](#docker-compose-を使用した実行)
- [マルチアーキテクチャ Docker イメージのビルドと Docker Hub へのプッシュ](#マルチアーキテクチャ-docker-イメージのビルドと-docker-hub-へのプッシュ)
- [アプリケーションへのアクセス](#アプリケーションへのアクセス)
- [API エンドポイント](#api-エンドポイント)
- [アプリケーションの停止](#アプリケーションの停止)

## プロジェクト概要

このアプリケーションは、以下の機能を提供します。

- FastAPI を使用した RESTful API
- SQLAlchemy を使用した PostgreSQL データベースとの連携
- `users` および `test_data` テーブルのデータ操作
- Docker および Docker Compose を使用したコンテナ化

## 前提条件

このプロジェクトを実行するには、以下のツールがシステムにインストールされている必要があります。

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## セットアップ

1.  **リポジトリのクローン**

    ```bash
    git clone https://github.com/your-username/fastapi-app.git # あなたのリポジトリURLに置き換えてください
    cd fastapi-app
    ```

2.  **テストデータ初期化スクリプトの作成**

    PostgreSQL データベースにテストデータを挿入するための SQL スクリプトを作成します。`init_test_data.sql`という名前でファイルを作成し、以下の内容を記述してください。

    ```sql
    -- init_test_data.sql
    CREATE TABLE IF NOT EXISTS test_data (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        value INTEGER NOT NULL
    );

    DO $$
    BEGIN
        FOR i IN 1..1000 LOOP
            INSERT INTO test_data (name, value) VALUES (CONCAT('TestName_', i), i * 10);
        END LOOP;
    END $$;
    ```

    **注意:** このファイルは、`docker-compose.yml`と同じディレクトリに配置してください。

## Docker Compose を使用した実行

このアプリケーションは Docker Compose を使用して、FastAPI アプリケーションと PostgreSQL データベースの両方をコンテナとして起動します。

1.  **Docker Compose の起動**

    ```bash
    docker-compose up -d --build
    ```

    -   `-d`: バックグラウンドでコンテナを実行します。
    -   `--build`: イメージが存在しない場合、または `Dockerfile` が変更された場合にイメージを再ビルドします。

    これにより、`fastapi-app` サービスと `abcdb` サービスが起動します。

2.  **コンテナのログの確認**

    アプリケーションが正常に起動したことを確認するには、以下のコマンドでログを確認できます。

    ```bash
    docker-compose logs fastapi-app
    docker-compose logs abcdb
    ```

## マルチアーキテクチャ Docker イメージのビルドと Docker Hub へのプッシュ

`docker buildx` を使用して、`linux/amd64` (x86_64) と `linux/arm64` (M1/M2/M3 Mac のネイティブアーキテクチャ) の両方に対応するマルチアーキテクチャ Docker イメージをビルドし、Docker Hub にプッシュできます。

1.  **`docker buildx` の確認とビルダーの作成**

    ```bash
    docker buildx version
    docker buildx create --name mybuilder --use
    ```

2.  **Docker Hub へのログイン**

    ```bash
    docker login
    ```

    プロンプトが表示されたら、Docker Hub のユーザー名とパスワードを入力します。

3.  **マルチアーキテクチャイメージのビルドとプッシュ**

    以下のコマンドを実行して、イメージをビルドし、Docker Hub にプッシュします。`[your_dockerhub_username]` をあなたの Docker Hub ユーザー名に置き換えてください。

    ```bash
    docker buildx build --platform linux/amd64,linux/arm64 -t [your_dockerhub_username]/fastapi-app --push .
    ```

    これにより、指定されたプラットフォーム用のイメージがビルドされ、Docker Hub のあなたのリポジトリにプッシュされます。

## アプリケーションへのアクセス

アプリケーションが起動したら、以下の URL でアクセスできます。

-   **FastAPI ドキュメント (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
-   **FastAPI Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API エンドポイント

以下のエンドポイントが利用可能です。

-   `/users/`: ユーザー情報を取得します。
-   `/test_data/`: テストデータを取得します (1000行のダミーデータが含まれています)。

## アプリケーションの停止

アプリケーションを停止し、関連するコンテナ、ネットワーク、ボリュームを削除するには、以下のコマンドを実行します。

```bash
docker-compose down
```
