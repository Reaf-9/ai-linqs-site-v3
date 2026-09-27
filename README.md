# AI Linqs コーポレートサイト v3

`SPEC.md` をデザイン規則の唯一の参照元として作成しました。HTML・CSS・JavaScript は `index.html` に集約し、外部ライブラリは使用していません。Google Fonts の Inter 400/500/600、Noto Sans JP 400/500 を読み込みます。

## 作成ファイル

- `index.html`
- `assets/future-morning.jpg`（生成画像、1200 × 800、JPEG）
- `README.md`

既存の `SPEC.md`、既存画像、v2 ファイルは変更していません。git コマンド・ファイル削除は実行していません。

## 構成・コピー

セクションの順序と ID は次のとおりです。

`hero` → `philosophy` → `future` → `loss` → `consult` → `reasons` → `service` → `lineup` → `works` → `process` → `faq` → `company` → `contact`

固定ヘッダー、スマートフォン用メニュー、現在地表示、LINE CTA、スマートフォンの追従 CTA、フッターを実装しています。詳細小窓は `detail-training`、`detail-aistaff`、`privacy` の3つです。FAQ は8問の `<details>` です。

日本語コピーは `../ai-linqs-site-v2/index.html` から移植し、新規文言 A/B/C と SPEC が指定する UI 文言を使用しています。図解だけに存在した文言、要確認・料金未設定の表記、3件の `[要確認]` HTML コメントも残しています。Mission / Vision / Value、STEP、Q. / A. などの英字ラベルは、日本語ラベルの指定に合わせて除いています。会社名とプライバシーポリシー本文は維持しています。

サービスの「詳しく見る」は、研修・AI社員については指定の小窓を開き、社内アプリについては同じカード内に残した詳細図解へ移動します。

## 画像の出どころ

- ヒーロー：提供済みの `assets/key-visual.jpg` を `<img>` で参照。ファイルは加工・再生成していません。
- サイン：提供済みの `assets/signature-dark.png`。
- QR：提供済みの `assets/line-qr.png`。
- favicon：提供済みの `favicon-32.png`、`favicon-192.png`、`favicon-180.png`。
- `assets/future-morning.jpg`：組み込み画像生成ツールで生成。返却された画像データを作業フォルダー内で JPEG・1200 × 800 に変換して保存しました。実在企業の実写ではありません。
- 残る8箇所：SPEC の `photo` ダミーを使用。背景 `#EDF1F9`、文字 `#9798A1`・13px、角丸16px、比率3:2。ストック写真のダウンロードはしていません。

ダミー対象：`future-noon.jpg`、`future-evening.jpg`、`service-training.jpg`、`service-aistaff.jpg`、`service-app.jpg`、`case-01.jpg`、`case-02.jpg`、`case-03.jpg`。HTML の各 `data-asset` 属性に対応ファイル名を記録しています。画像を用意した際は該当ダミーを `<img class="photo">` に差し替えてください。

使用した生成プロンプト（組み込みツール、CLI/API フォールバック不使用）：

> Generate one photorealistic natural corporate website photograph, landscape 3:2 approximately 1200x800. Japanese SME office, morning: a Japanese manager in their 40s reading an organized morning report on a tablet beside a colleague in their 30s. Bright natural light, calm white and blue palette. AI represented only by the ordinary tablet. No text, logos, watermarks, signs, robots or humanoid light. Deliver image data only, do not write any files outside the user's ai-linqs-site-v3 workspace. Intended asset assets/future-morning.jpg.

## CSS の全色・角丸

CSS から値を抽出し、すべて SPEC の許可値に一致することを確認しました。

| 種別 | 使用値 |
| --- | --- |
| HEX | `#FFFFFF`、`#EDF1F9`、`#327AFA`、`#0F0F11`、`#616267`、`#9798A1` |
| RGBA | `rgba(15,15,17,.1)`（区切り）、`rgba(15,15,17,.5)`（小窓の背面） |
| border-radius | `4px`、`12px`、`16px`、`24px`、`32px`、`9999px` |

グラデーション、box-shadow、text-shadow、文字のフチ、光彩、波形・斜めの区切りは追加していません。提供済み画像自体に含まれる色・表現はそのままです。動きはボタン等の0.3秒の色変更のみで、prefers-reduced-motion では無効になります。

## 検証結果

- 13セクションの順序・ID：一致。
- HTML のタグ対応、重複 ID、ページ内リンク、参照画像：問題なし。
- v2 の日本語テキストノード：英字ラベルの除去を除き、欠落なし。
- 詳細小窓2件・プライバシーポリシー：空白を正規化した表示テキストが v2 と一致。
- FAQ：8問。要確認 HTML コメント：3件すべて維持。
- CSS：上記の全色・角丸を抽出して許可値と照合済み。インラインスタイルなし。
- JavaScript：構文確認済み。DOM モックで LINE の URL・新規タブ設定、ローカルのテスト印、ヒーロー通過後の追従 CTA、contact での非表示、ナビ現在地、メニュー開閉を確認。
- 390px・768px・1440px の実ブラウザーでの横スクロール確認：**未確認**。Google Chrome 154.0.8037.57 は存在しますが、headless 起動が通常・`--no-sandbox` の両方で終了コード134となりました。ブラウザープロファイルの保存先は v3 内に指定しましたが、そのディレクトリが作成される前に終了しています。スクリーンショットおよび実ブラウザーでのクリック操作も未確認です。DOM モックの確認は実描画検証の代替ではありません。

## SPEC を厳密に満たせなかった点

1. 9枚すべての画像生成は完了していません。生成機能はあり1枚成功しましたが、作業フォルダー外へ保存しないようプロンプトで指定しても、ツールが `$CODEX_HOME/generated_images/` に自動保存したと返答しました。ユーザー指定の書き込み範囲をこれ以上超えないため、追加8枚の生成を止め、許可されたダミー表示を採用しました。外部保存ファイルをこちらから読み取り・削除する操作は行っていません。ただし最初の1枚については、ツールの自動保存により「v3 の外へ書き込まない」という条件を満たせませんでした。
2. 上記 Chrome 起動失敗により、3画面幅の実描画による横スクロール検証は実施できていません。

## 公開前に外す・決めるもの

- 検証完了後、検索公開する場合は `<meta name="robots" content="noindex,nofollow">` を外す。
- 「テスト版 v3」の表示は github.io・ローカル限定。本番ドメインでは非表示になるが、正式公開時には表示要素・判定コードの撤去も検討する。
- 会社情報、数値・出典、料金未設定箇所、実績の掲載許諾、お客様の声の同意を確認する。要確認表記は確認前に消さない。
- 生成画像・ダミーを確認し、特に事例写真は掲載許諾を得た実写へ差し替える。
- Chrome 等で390px・768px・1440pxの横スクロール、小窓・メニュー・追従 CTA、キーボード操作、LINE 遷移を実機確認する。

JavaScript 無効時、LINE CTA はすべて `#contact` へ移動し、QR コードを利用できます。詳細小窓の開閉には JavaScript が必要です。
