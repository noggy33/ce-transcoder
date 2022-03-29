# 環境の準備



# local run
cd video-convert
cat << EOF > .env
COS_ENDPOINT=<COS ENDPOINT>
COS_AUTH_ENDPOINT=<COS AUTH ENDPOINT>
COS_RESOURCE_CRN=<COS RESOURCE CRN>
COS_BUCKET_LOCATION=<COS STORAGE CLASS >
COS_API_KEY_ID=<API KEY>
EOF
* <COS ENDPOINT> It can see in follow page.
https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-endpoints
* <COS STORAGE CLASS > It can see in follow page.
https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-classes 

sudo docker build -t video-convert:latest .
sudo docker run -it --rm --env-file=./.env video-convert:latest