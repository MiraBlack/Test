from minio import Minio
import io

class ImageMinioAccess:

    def __init__(self, endpoint, access_key, secret_key): 
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = Minio(endpoint = self.endpoint,
                            access_key = self.access_key,
                            secret_key = self.secret_key)

    

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
