# Readme

## IBM Cloud にツールをデプロイする



## ローカル環境でテストする

### 1. Github からコードをクローンする。

```
git clone https://github.com/noggy33/ce-transcoder.git
```


### 2. ディレクトリを移動する。

```
cd ce-transcode
```


### 3. テスト用の環境変数を '.env' ファイルに書き込む。

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


### 4. テスト用のイベントを '.event' ファイルに書き込む。

```
cat << EOF > .event
CE_DATA={"bucket":"[BUCKET NAME]","key":"[ITEM NAME]"}  
EOF
```


### 5. テスト用のMP4ファイルを IBM Cloud Object Storage に配置する。

`.event` ファイルで指定した *[BUCKET_NAME]* と *[ITEM_NAME]* に合致するように配置すること


### 6. コンテナを起動し、変換処理を実行する。

```
sudo docker build -t video-convert:latest .
sudo docker run -it --rm --env-file=./.env --env-file=./.event video-convert:latest
```