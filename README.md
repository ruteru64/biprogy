# biprogy

# 営業時の話題提案サービス(仮)

## 概要

- 前回の営業で話したことを入力しておくと，次回営業の際に話題デッキを作成してくれるサービス

## 処理フロー

- 前回話したことを入力する -> 入力単語をデータベースに入れる -> 次回営業時に機械学習にかけて類似単語を生成 -> UI にトランプの手札チックに表示 -> twilio の virtual 背景を話題をもとに変更
- オプション
  - 手札を選択したらネットから話題をとってくる機能
  - 手札を見せるのにイイ感じのアニメーションをつける
  - 初回営業でも普遍的な話題を表示

## アーキテクチャ

- バックエンド

  - Python, djngo

- フロントエンド

  - djngo, JSDOM, HTML

- データベース

  - SQLLite

- テクニカルサポート
  - twilio

