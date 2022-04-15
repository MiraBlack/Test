from minio import Minio
import io
from db.db import ImageDao

class ImageMinioAccess:

    def __init__(self): 
        self.client = Minio(endpoint = 'play.min.io',
        access_key = 'Q3AM3UQ867SPQQA43P2F',
        secret_key = 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG')


    def insert_images(self, files, bucket_name, uuid):
        if self.client.bucket_exists(bucket_name) is False:
            self.client.make_bucket(bucket_name)
        with io.BytesIO() as f:
            for file in files:
                f.write(file.file.read())
                f.seek(0)
                self.client.put_object(bucket_name, "-".join((uuid, file.filename.replace(".jpeg",".jpg"))), f, f.getbuffer().nbytes, content_type="image/jpg")


    def delete_images(self, image, uuid, bucket_name):
        self.client.remove_object(bucket_name, "-".join((uuid, image.replace(".jpeg",".jpg"))))
