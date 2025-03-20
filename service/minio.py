from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv

load_dotenv()

class MinioClient:
    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=os.getenv("MINIO_SECURE", "False").lower() == "true"
        )
        self.bucket = os.getenv("MINIO_BUCKET")
        
    def list_objects(self, prefix=""):
        """列出存储桶中的对象"""
        try:
            return self.client.list_objects(
                self.bucket,
                prefix=prefix,
                recursive=True
            )
        except S3Error as e:
            print(f"MinIO Error: {e}")
            return []
            
    def get_object(self, object_name):
        """获取对象内容"""
        try:
            response = self.client.get_object(
                self.bucket,
                object_name
            )
            return response.read().decode('utf-8')
        except S3Error as e:
            print(f"MinIO Error: {e}")
            return None
        finally:
            response.close()
            response.release_conn()

# 单例客户端实例
minio_client = MinioClient()