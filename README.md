# AI Linqs コーポレートサイト v3

`SPEC.md` をデザイン規則の唯一の参照元として作成しました。HTML・CSS・JavaScript は `index.html` に集約し、外部ライブラリは使用していません。Google Fonts の Inter 400/500/600、Noto Sans JP 400/500 を読み込みます。

## 作成ファイル

- `index.html`
- `assets/future-morning.jpg` および下記画像一覧の追加8枚（生成画像、1200 × 800、JPEG）
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
- 追加8枚：組み込み画像生成ツールで生成し、ツールの保存先から `assets/` へコピー後、Pillow で JPEG・1200 × 800 に変換しました。全画像250,000バイト未満です。生成ツールの作業フォルダー外への自動保存とコピー元の読み取りは、今回のユーザー指示で許可されています。コピー元の変更・削除は行っていません。
- `photo` ダミー8箇所はすべて画像に置換済みです。事例3枚は実在企業の実写ではなく、実写が届くまでの仮画像です。ストック写真は使用していません。

### 追加画像一覧

容量は 1 KB = 1,000 bytes で記載しています。全画像3:2、1200 × 800です。

| ファイル | 場面 | 形式 | 寸法 | 容量 |
| --- | --- | --- | --- | --- |
| `assets/future-noon.jpg` | 昼の業務 | JPEG | 1200 × 800 | 153.4 KB |
| `assets/future-evening.jpg` | 窓辺で計画する経営者 | JPEG | 1200 × 800 | 164.6 KB |
| `assets/service-training.jpg` | 社内研修 | JPEG | 1200 × 800 | 172.2 KB |
| `assets/service-aistaff.jpg` | 業務レポートの確認 | JPEG | 1200 × 800 | 160.0 KB |
| `assets/service-app.jpg` | 倉庫でのタブレット利用 | JPEG | 1200 × 800 | 159.1 KB |
| `assets/case-01.jpg` | 物流・配車事務所（仮） | JPEG | 1200 × 800 | 159.2 KB |
| `assets/case-02.jpg` | 車両サービス職場（仮） | JPEG | 1200 × 800 | 177.4 KB |
| `assets/case-03.jpg` | 経営会議（仮） | JPEG | 1200 × 800 | 168.3 KB |

使用した生成プロンプト（組み込みツール、CLI/API フォールバック不使用）：

> Generate one photorealistic natural corporate website photograph, landscape 3:2 approximately 1200x800. Japanese SME office, morning: a Japanese manager in their 40s reading an organized morning report on a tablet beside a colleague in their 30s. Bright natural light, calm white and blue palette. AI represented only by the ordinary tablet. No text, logos, watermarks, signs, robots or humanoid light. Deliver image data only, do not write any files outside the user's ai-linqs-site-v3 workspace. Intended asset assets/future-morning.jpg.

## 今回の修正と検証

- 追加8画像を目視し、文字・ロゴ・透かし・ロボット・発光する人型がないことを確認。`service-aistaff` の初回生成は画面に小さな数字らしき表示があったため再生成し、文字のない抽象的なレポート画面を採用しました。
- 各画像の保存直後と最終確認で、パス・JPEG形式・1200 × 800・250,000バイト未満をPillowとファイルサイズで検証しました。
- 8つのダミーを `<img class="photo" width="1200" height="800" loading="lazy" decoding="async" alt="">` に置換。既存の `.photo` の角丸16pxと object-fit:cover を使用しています。
- `.mini>li>span:first-child` に `white-space:nowrap; flex:0 0 32px; width:32px` を設定。番号の列が縮まず、01等が分割されません。本文側には `min-width:0` を設定しました。
- `@media(max-width:767px)` で `.test-badge{display:none}` とし、モバイルではバッジと本文・固定CTAが重ならないようにしました。これは今回のユーザー指定によるモバイル時の例外です。
- 変更前後を照合し、index.html の変更が8画像の置換と上記CSS修正だけであることを確認しました。HTMLタグ対応・重複ID・画像属性・リンクを再検査しています。
- 色・角丸の全使用値は変更前と同一。影・グラデーション等の追加はありません。実ブラウザー検証については下記の既存制約が残ります。

### 追加画像の生成プロンプト

全8枚に使用した共通指示：

> Use case: photorealistic-natural. Create one landscape 3:2 photograph, approximately 1200x800, for a Japanese small/mid-size company website. Match the visual style of a bright natural-light Japanese office editorial photo, realistic skin texture, calm white and blue palette, restrained candid professional atmosphere. People are Japanese employees including ages 30–50. AI appears only as ordinary screens or tablets beside people. No text anywhere, no letters, no numbers, no logos, no watermarks, no company names, no signage, no robots, no glowing humanoids. All papers, clothing, boxes and devices unbranded. 

各場面の指示：

- `future-noon.jpg`: Employees focused independently on their own work at desks, midday office.
- `future-evening.jpg`: A Japanese company president in their 50s calmly thinking and planning by a large window, late afternoon with bright natural daylight.
- `service-training.jpg`: Small in-house training session of four Japanese employees in their 30s to 50s around a table with a laptop, attentive collaborative atmosphere.
- `service-aistaff.jpg`: An office worker reviewing an organized report on a monitor. Screen contains only clean abstract blue chart shapes and rows, absolutely no letters, numerals or text.
- `service-app.jpg`: A Japanese worker on a tidy warehouse shop floor using a tablet, shelves with completely unmarked boxes.
- `case-01.jpg`: Japanese logistics trucking dispatch office, dispatch staff at desks with monitors, unmarked trucks subtly visible through window, no signage or company names.
- `case-02.jpg`: Two Japanese mobility vehicle service company staff sharing a tablet in a clean vehicle workshop, an unbranded vehicle softly out of focus behind them.
- `case-03.jpg`: A meeting room where three Japanese managers in their 30s to 50s review simple abstract charts on a screen. Screen only blue bars and lines without any text or numerals.

`service-aistaff.jpg` 最終採用版の再生成プロンプト：

> Use case: photorealistic-natural. Create one landscape 3:2 photograph, approximately 1200x800, for a Japanese small/mid-size company website. Match the visual style of a bright natural-light Japanese office editorial photo, realistic skin texture, calm white and blue palette, restrained candid professional atmosphere. People are Japanese employees including ages 30–50. AI appears only as ordinary screens or tablets beside people. No text anywhere, no letters, no numbers, no logos, no watermarks, no company names, no signage, no robots, no glowing humanoids. All papers, clothing, boxes and devices unbranded. Scene: A Japanese office worker aged 40 reviewing a very simple organized report on a monitor in a bright white and blue office. The monitor MUST show exactly SIX LARGE SOLID BLUE RECTANGLES on a plain white screen arranged in two columns and three rows, nothing else: NO CHART AXES, NO tick marks, NO legends, NO table cells, NO tiny text, NO pseudo-writing, NO numerals, NO icons. The six solid rectangles are a purely abstract representation of an organized report. All keyboards out of focus or obscured, no visible printing on anything. Medium wide editorial photograph, calm concentration.

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

画像生成は既存1枚＋今回追加8枚で完了しました。画像生成ツールの外部自動保存は今回の指示で許可されています。

上記 Chrome 起動失敗により、3画面幅の実描画による横スクロール検証は実施できていません。

## 公開前に外す・決めるもの

- 検証完了後、検索公開する場合は `<meta name="robots" content="noindex,nofollow">` を外す。
- 「テスト版 v3」の表示は github.io・ローカルの幅768px以上限定。本番ドメインでは非表示になるが、正式公開時には表示要素・判定コードの撤去も検討する。
- 会社情報、数値・出典、料金未設定箇所、実績の掲載許諾、お客様の声の同意を確認する。要確認表記は確認前に消さない。
- 生成画像を確認し、特に事例写真は掲載許諾を得た実写へ差し替える。
- Chrome 等で390px・768px・1440pxの横スクロール、小窓・メニュー・追従 CTA、キーボード操作、LINE 遷移を実機確認する。

JavaScript 無効時、LINE CTA はすべて `#contact` へ移動し、QR コードを利用できます。詳細小窓の開閉には JavaScript が必要です。


## 追記（2026-09-27）

- `future-*`・`service-*`・`case-*` の 9 枚は Codex の画像生成で作った仮の画像。事例（`case-01〜03`）は実在の各社の写真ではないため、サイト上に「※ 写真はイメージです。」と表記している。看板前の実写が届いたら差し替え、表記を外す
- 公開前に確認：事例3社の掲載許諾と社名表記、`[要確認]` の出典、設立年、ロゴデータ、社長の写真
