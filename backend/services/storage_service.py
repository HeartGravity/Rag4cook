# backend/services/storage_service.py
import os
import uuid
import logging
from minio import Minio
from fastapi import UploadFile

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        # 实际使用时建议将这些配置放入 config.py 或环境变量中
        self.endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.secure = os.getenv("MINIO_SECURE", "False").lower() == "true"
        self.bucket_name = "howtocook-recipes"
        
        try:
            self.client = Minio(
                self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure
            )
            # 确保存储桶存在
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"创建了新的 MinIO Bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"MinIO 初始化失败: {e}")
            self.client = None

    async def upload_file(self, file: UploadFile, sub_folder: str = "") -> str:
        """上传文件到 MinIO 并返回访问 URL"""
        if not self.client:
            logger.warning("MinIO 未就绪，跳过上传逻辑，返回本地 mock 路径。")
            return f"http://mock-storage/{sub_folder}/{file.filename}"

        try:
            file_extension = os.path.splitext(file.filename)[1]
            # 生成唯一文件名防止冲突
            unique_filename = f"{uuid.uuid4().hex}{file_extension}"
            object_name = f"{sub_folder}/{unique_filename}" if sub_folder else unique_filename
            
            # 读取文件内容
            file_data = await file.read()
            import io
            data_stream = io.BytesIO(file_data)
            
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data_stream,
                length=len(file_data),
                content_type=file.content_type
            )
            
            # 简单的 URL 拼接 (根据实际代理/网关配置修改)
            protocol = "https" if self.secure else "http"
            url = f"{protocol}://{self.endpoint}/{self.bucket_name}/{object_name}"
            return url
        except Exception as e:
            logger.error(f"文件上传失败: {e}")
            raise e
        finally:
            await file.seek(0) # 重置指针以便后续读取

storage_service = StorageService()