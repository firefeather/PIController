import os
import requests
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from config import getCosConfig

class CosOper():
    def __init__(self):
        """
        读取配置文件，初始化变量
        """
        config = getCosConfig()
        self.secret_id = config['secret_id']
        self.secret_key = config['secret_key']
        self.cos_region = config['cos_region']
        self.bucket_name = config['bucket_name']
        config = CosConfig(Secret_id=self.secret_id, Secret_key=self.secret_key, Region=self.cos_region)
        self.cos_client = CosS3Client(config)

    def cos_upload(self, file ):
        """
        简单文件上传
        :param filename: object name
        :return:
        """
        response = None
        filename = file
        if file.startswith('http'):
            response = self.cos_client.put_object(
            Bucket=self.bucket_name,
            Body=requests.get(file).content,
            Key=file[file.index(':'):]
            )
        else:
            with open(file, 'rb') as fp:
                response = self.cos_client.put_object(
                Bucket=self.bucket_name,
                Body=fp,
                Key=file
                )
        return self.cos_get_upload_path(filename)

    def cos_get_upload_path(self, filename ):
        if filename.startswith('.'):
           filename=filename[filename.index('/'):]
        return 'https://{}.cos.{}.myqcloud.com{}'.format(self.bucket_name,self.cos_region,filename)
      
    def cos_upload_file(self, file, partsize=10, maxthread=5):
        """
        根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
        :param partsize:
        :param maxthread:
        :return:
        """
        response = None
        filename = file
        if file.startswith('http'):
            filename = file[file.index(':'):]
            # 下载到本地文件
            with open(filename, 'wb') as localfile:
                localfile.write(requests.request('get', file).content)
            # 进行上传
            response = self.cos_client.upload_file(
                Bucket=self.bucket_name,
                LocalFilePath=filename,
                Key=filename,
                PartSize=partsize,
                MAXThread=maxthread
            )
            # 删除本地文件
            if os.path.exists(filename):
                os.remove(filename)
        else:
            response = self.cos_client.upload_file(
                    Bucket=self.bucket_name,
                    LocalFilePath=file,
                    Key=file,
                    PartSize=partsize,
                    MAXThread=maxthread
                )
        return self.cos_get_upload_path(filename)

uploader = CosOper()

def uploadFile(filePath):
    return uploader.cos_upload_file(filePath)

if __name__ == '__main__':
    test_filename = './girl.jpg'
    # 普通上传
    # client.upload_file()
    # 高级上传
    result = CosOper().cos_upload_file(test_filename,)
    print(result)