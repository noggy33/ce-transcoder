# from cos import CloudObjectStorage, COSError
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import ffmpeg
import os

# Get from Configmap on Kubernetes
COS_ENDPOINT = os.getenv('COS_ENDPOINT')
COS_AUTH_ENDPOINT = os.getenv('COS_AUTH_ENDPOINT')
COS_RESOURCE_CRN = os.getenv('COS_RESOURCE_CRN')
COS_BUCKET_LOCATION = os.getenv('COS_BUCKET_LOCATION')

# Get from Secrets on Kubernetes
COS_API_KEY_ID = os.getenv('COS_API_KEY_ID')

# Work dirs
INPUT_PATH = "./input/"
OUTPUT_PATH = "./output/"

# Create resourceS
cos = ibm_boto3.resource("s3",
  ibm_api_key_id=COS_API_KEY_ID,
  ibm_service_instance_id=COS_RESOURCE_CRN,
  ibm_auth_endpoint=COS_AUTH_ENDPOINT,
  config=Config(signature_version="oauth"),
  endpoint_url=COS_ENDPOINT
)

# Download Origin Video from COS
def download_item(bucket_name, item_name):

    # 入力元のディレクトリが存在しない場合は作成する
    try:
        if not os.path.exists(INPUT_PATH):
            os.mkdir(INPUT_PATH)
            print("Created Input Directory: {0}".format(INPUT_PATH))

    except Exception as e:
        print("Failed to create INPUT DIRECTORY - {0}".format(e))

    # 変換元となるファイルのダウンロードする先を設定する
    file_path = INPUT_PATH + item_name.split("/")[-1]

    # 変換元となるファイルをダウンロードする
    print("Downloading item from bucket: {0}, key: {1}, path: {2}".format(bucket_name, item_name, file_path))
    try:
        cos.Object(bucket_name, item_name).download_file(file_path)
        print("Download succeed !!")

    except ClientError as be:
        print("CLIENT ERROR: {0}¥n".format(be))

    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))


# Convert origin MP4 to HLS format.
def convert_item(input_file):
    
    # 出力先のディレクトリが存在しない場合は作成する
    try:
        if not os.path.exists(OUTPUT_PATH):
            os.mkdir(OUTPUT_PATH)
            print("Created Output Directory: {0}".format(OUTPUT_PATH))

    except Exception as e:
        print("Faild to create OUTPUT DIRECTORY: {0}".format(e))

    # Input Stream を作成する
    input_stream = ffmpeg.input(input_file, f='mp4')

    # 出力先ファイルを設定する
    video_name = input_file.split("/")[-1].split(".")[0]
    output_name = OUTPUT_PATH + video_name + ".m3u8"
    seg_name = OUTPUT_PATH + video_name + "%3d.ts"

    # Output Stream をもとに変換処理を行う
    output_stream = ffmpeg.output(
        input_stream, 
        output_name, 
        format='hls', 
        start_number=0, 
        hls_time=10, 
        hls_segment_filename = seg_name, 
        hls_list_size=0)
    ffmpeg.run(output_stream)


if __name__ == "__main__":

    bucket_name = "test433151"
    item_name = "test.mp4"

    # 1. Download MP4 file
    download_item(bucket_name, item_name)

    # 2. comvert MP4 to HLS
    input_file = INPUT_PATH + item_name
    convert_item(input_file)

    # 3. Upload HLS file
    # 4. Delete MP4 & HLS

    print ("hoge")