# Readme

## 概要

`IBM Cloud Code Engine` を利用した動画変換 (MP4 to HLS) を自動化するプログラムです。

所定の `IBM Cloud Object Storage` (COS) の `Bucket` にアップロードされた MP4 ファイルを HLS 形式に変換し、別の `Bucket` にアップロードします。

## 利用するリソース

- `IBM Cloud Code Engine`
	- `ce-transcoder`
		- 動画変換用のCode Engine プロジェクト
	- `build-transcoder`
		- 動画変換用コンテナイメージのビルド
	- `job-transcoder`
		- 動画変換処理のジョブ
	- `sub-transcoder`
		- 動画変換処理をトリガーするサブスクリプション
- `IBM Cloud Object Storage`
	- `cos-transcoder`
		- 動画変換用のObject Storageサービスインスタンス
	- `mp4-video`
		- 変換元のMP4ファイルを配置するバケット
	- `his-video`
		- 変換後のHLSファイルを配置するバケット
- `IBM Cloud Container Registry`
	- `noggy33`
		- 変換処理を行うコンテナイメージを配置するネームスペース
	- `transcoder`
		- 動画変換を行うコンテナイメージ

## IBM Cloud にツールをデプロイする

### 1. `COS` バケットを作成する

1.1. `CLI` に `Object Storage` 用のプラグインをインストールする
~~~
ibmcloud plugin install cloud-object-storage
~~~

1.2. プラグインがインストールされたことを確認する
~~~
ibmcloud plugin show cloud-object-storage
~~~

1.3. `COS` のサービスインスタンスを作成する
~~~
ibmcloud resource service-instance-create cos-transcoder cloud-object-storage lite global
~~~

1.4. 利用するサービスインスタンスの `CRN` を確認する
~~~
ibmcloud resource service-instance cos-transcoder
~~~

1.5. プラグインにサービスインスタンスの `CRN` を設定する
~~~
ibmcloud cos config crn --crn [crn] --force
~~~

1.6. 入力用バケットを作成する
~~~
ibmcloud cos bucket-create -bucket mp4-video
~~~

1.7. 出力用バケットを作成する
~~~
ibmcloud cos bucket-create -bucket hls-video
~~~

1.8. バケットが作成されたことを確認する
~~~
ibmcloud cos buckets
~~~


### 2. `Code Engine`のプロジェクトを作成する

2.1. `CLI` に `Code Engine` 用のプラグインをインストールする
~~~
ibmcloud plugin install code-engine
~~~

2.2. プラグインがインストールされたことを確認する
~~~
ibmcloud plugin show code-engine
~~~

2.3. `Code Engine` のプロジェクトを作成する
~~~
ibmcloud ce project create --name ce-transcoder
~~~

2.4. プロジェクトが作成されたことを確認する
~~~
ibmcloud ce project list
~~~


### 3. `Code Engine` に `Notifications Manager` のロールを割り当てる

3.1. `Code Engine` プロジェクトを選択する
~~~
ibmcloud ce project select -n ce-transcoder
~~~

3.2. `Notification Manager` ロールを割り当てる
~~~
ibmcloud iam authorization-policy-create codeengine cloud-object-storage "Notifications Manager" --source-service-instance-name ce-transcoder --target-service-instance-name cos-transcoder
~~~

3.3. ロールが割り当てられたことを確認する
~~~
ibmcloud iam authorization-policies
~~~


### 4. 動画変換用のアプリケーションコードを作成する

4.1. 必要に応じてコードを変更する


### 5. プライベートレジストリを作成する

5.1. `CLI` に `Container Registry` 用のプラグインをインストールする
~~~
ibmcloud plugin install container-registry -r 'IBM Cloud'
~~~

5.2. コンテナレジストリのリージョンを設定する
~~~
ibmcloud cr region-set jp-tok
~~~

5.3. ビルドイメージを追加するネームスペースをコンテナレジストリに作成する
~~~
ibmcloud cr namespace-add noggy33
~~~


### 6. ビルドを作成する

6.1. `Code Engine` のプロジェクトを選択する
~~~
ibmcloud ce project select -n ce-transcoder
~~~

6.2. ビルドを作成する
~~~
ibmcloud ce build create --name build-transcoder --src https://github.com/noggy33/ce-transcoder --cm master --rs ce-default-icr-jp-tok --image jp.icr.io/noggy33/transcoder --sz small
~~~

6.3. ビルドを作成する
~~~
ibmcloud ce buildrun submit --build build-transcoder
~~~

6.4. ビルドの実行結果を確認する
~~~
ibmcloud ce buildrun get -n [build id]
~~~


### 7. `Code Engine`のジョブを作成する

7.1. ジョブを作成する
~~~
ibmcloud ce job create --name job-transcoder --env-cm cos-api-conf --env-sec cos-api-key --es 2G --memory 4G --cpu 2 --rs ce-default-icr-jp-tok --image jp.icr.io/noggy33/transcoder
~~~

7.2. ジョブが作成されたことを確認する
~~~
ibmcloud ce jobrun list
~~~


### 8. `Code Engine`のサブスクリプションを作成する

8.1. バケットの変更のサブスクリプションを設定する
~~~
ibmcloud ce subscription cos create --name sub-transcoder --destination-type job --destination job-transcoder --bucket test433151 --event-type write
~~~

8.2. サブスクリプションが作成されたことを確認する
~~~
ibmcloud ce subscription cos get -n sub-transcoder
~~~


## ジョブを実行する

1. `COS` の `mp4-video` に 変換元となる MP4 ファイルをアップロードする

ブラウザで `mp4-video` バケットにアクセスし、 MP4 ファイルをアップロードする

2. ジョブが自動的に実行されたことを確認する

```
ibmcloud ce jobrun list
```

3. ジョブの状態を確認する

```
ibmcloud ce jobrun get --name [job id]
```

4. ジョブ インスタンスの情報を確認する

```
ibmcloud ce jobrun logs --instance [job instance id]
```

5. ジョブが成功したことを確認し、出力された　HLS ファイルを確認する

ブラウザで `hls-video` バケットにアクセスし、 HLS ファイルが格納されていることを確認する。

## ローカル環境でテストする

1. Github からコードをクローンする。
```
git clone https://github.com/noggy33/ce-transcoder.git
```


2. ディレクトリを移動する。
```
cd ce-transcode
```


3. テスト用の環境変数を '.env' ファイルに書き込む。

変数の値は各自の環境に合わせて入力してください。

```
cat << EOF > .env
COS_ENDPOINT=[COS ENDPOINT]
COS_AUTH_ENDPOINT=[COS AUTH ENDPOINT]
COS_RESOURCE_CRN=[COS RESOURCE CRN]
COS_BUCKET_LOCATION=[COS STORAGE CLASS]
COS_API_KEY_ID=[API KEY]
EOF
```
有効な *COS ENDPOINT* は、 [このページ](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-endpoints) で確認できます。

有効な *COS STORAGE CLASS* は、 [このページ](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-classes) で確認できます。


4. テスト用のイベントを '.event' ファイルに書き込む。
```
cat << EOF > .event
CE_DATA={"bucket":"[BUCKET NAME]","key":"[ITEM NAME]"}  
EOF
```


5. テスト用のMP4ファイルを IBM Cloud Object Storage に配置する。

`.event` ファイルで指定した *[BUCKET_NAME]* と *[ITEM_NAME]* に合致するように配置すること


6. コンテナを起動し、変換処理を実行する。
```
sudo docker build -t video-convert:latest .
sudo docker run -it --rm --env-file=./.env --env-file=./.event video-convert:latest
```