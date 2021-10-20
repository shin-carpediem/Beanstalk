<img width="370" alt="a15defcc-e828-427d-89b6-073b21379819" src="https://user-images.githubusercontent.com/71208265/138083693-47ed5e6a-dd80-4bc7-857f-e20e889dd2e6.png">

<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat"> <img src="https://img.shields.io/badge/-Bootstrap-563D7C.svg?logo=bootstrap&style=flat"> <img src="https://img.shields.io/badge/-Sass-CC6699.svg?logo=sass&style=flat"> <img src="https://img.shields.io/badge/-Google%20Cloud-EEE.svg?logo=google-cloud&style=flat">

# beanstalk

https://beanstalk-test-prod-322412.an.r.appspot.com/

##### プライバシー・ポリシー

https://beanstalk-test-prod-322412.an.r.appspot.com/policy/

##### 利用規約

https://beanstalk-test-prod-322412.an.r.appspot.com/terms/

### 仕様

- テーブルに座る 1 人目の客の使用許可を店側が受け、2 人目以降の客は 1 人目の客が受ける。
- 店側が「お会計完了」のボタンをレジ終了時に押す事で、同一のテーブルに座る同一のタイミングのグループか別のタイミングのグループかを区別。
- 客側は画面操作後 5 時間はブラウザを閉じても画面が保存されている。
- 客側は画面操作後 5 時間は、お会計完了後にサイトにアクセスしても使用できない。

### 実現可能な事

##### お客様

- ログインなしで、自分の座っているテーブル番号を入力して使用開始可能です。
- 同じテーブルで食事中のお客様の全員の画面が、注文内容・伝票等が同期されます。
- 一度スマートフォンを閉まった場合も、操作後 5\*時間はテーブルの情報が保存されるので、再度ページにアクセスした際には情報が保持されています。

##### 店舗様

- お渡しする 4 桁の数字を入力してログインが可能です。
- 10 秒毎に受注画面が更新され、新しい注文があれば受注リストに表示されます。調理済みの注文内容は別ページに移動させられます。
- 利用中のテーブル毎の伝票が常に表示されます。テーブル番号で絞り込みが可能です。
- 日時で絞り込み、及びテーブルで絞り込みをしての売上管理ができます。初期設定では昨日〜当日の全てのテーブルに対しての売上が表示されています。絞り込みは操作後 5\*時間保持されます。
- 全機種（PC・タブレット・スマートフォン）に対応の画面です。
- 初期設定では 1 アカウントを作成しますが、ご要望に応じ 2 アカウント以上作成が可能です。全てのアカウントで同一の内容が表示され、変更は全てのアカウントに紐付きます。
- お客様が実際にご覧になっている画面と同一の画面から、カテゴリー・メニュー・飲み放題用プラン等全ての項目が作成できます。

\*ご要望に応じてカスタマイズ可能です。

#### 実現できない事及び禁止させていただいている事

##### お客様

- 注文がすでに店舗様に到達した後での注文内容の変更はできません。この場合、お客様から口頭で店舗様にお伝えするかつ、店舗様が受注画面から該当メニューの「状況」を「キャンセル」にする事で注文メニュー自体のキャンセルが可能です。その際お客様の注文履歴の該当メニューに「キャンセル」マークが付きます。

##### 店舗様

- なし

#### まだできない事&今後追加搭載したい機能

##### 客

- PayPay による決済機能と、その決済完了後に「オーダーストップ」が自動で為される事

##### 店

- 注文が来た際の通知音
- 「お会計完了」ボタンを押した際のスナップショット

Technology:

- App Engine
- Cloud SQL/MySQL
- Cloud Storage
- Selenium IDE

To go into virtual environment with Pipfile,

```
$ pipenv shell
```

To install package,

```
$ pipenv install hogehoge
```

To execute Pipfile each script,

```
$ pipenv run hogehoge
```

To exit from virtual environment,

```
$ exit
```

To optimize pip for lightsail,

```
pipenv lock -r > requirements.txt
```

To restart apache,

```
$ sudo /opt/bitnami/ctlscript.sh restart apache
```

https://qiita.com/CyberMergina/items/f889519e6be19c46f5f4
To enter MySQL on Lightsail,

```
$ mysql -u username -p -h endpoint
```

To exit from MySQL,

```
> exit
```

To check the Apache log,

```
$ /opt/bitnami/apache2/logs/access_log
```

```
$ /opt/bitnami/apache2/logs/error_log
```

### Google Cloud Platform

https://cloud.google.com/python/django/appengine?hl=ja#creating_a_cloud_sql_instance
To deploy, access to the CloudSQL/MySQL from local

```
$ python manage.py collectstatic
```

```
$ gcloud sql instances describe hogehoge
```

```
$ ./cloud_sql_proxy -instances="hoge:hoge:hoge"=tcp:3306
```

debug=False and switch database from SQlite3 to MySQL, then

```
$ python manage.py makemigrations
```

```
$ python manage.py migrate
```

```
$ gcloud app deploy
```

```
$ gcloud app browse
```

To exit from CloudSQL/MySQL,

```
> quit
```

if the MySQL port is still on process,

```
$ lsof -i:3306
```

or

```
$ sudo lsof -i -P | grep "LISTEN"
```

```
$ sudo kill <PID>
```

### 別プロジェクトにデプロイ

- [ ] Cloud SDK の設定を変更

```
$ gcloud init
```

- [ ] GCP にプロジェクトを定義した JSON ファイルの取得
      https://cloud.google.com/docs/authentication/getting-started#auth-cloud-implicit-python

- [ ] .env ファイルで読み込む JSON ファイル(GOOGLE_APPLICATION_CREDENTIALS)のパス、Cloud SQL、Cloud Storage の情報を変更
