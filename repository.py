from fastapi import status
from datetime import datetime
import uuid

class Repository:

    def __init__(self,image_dao,image_minio_access,files=None):
        self.image_dao = image_dao
        self.image_minio_access = image_minio_access

    def delete_images_from_db(self,uuid):
        self.image_dao.delete_images(uuid)

    def delete_images_from_minio(self, uuid, list_of_images, bucket_name):
        for images_data in list_of_images:
            uuid = images_data [0]
            image = images_data[1]
            self.image_minio_access.delete_images(image, uuid, bucket_name)

    def delete_images(self, uuid):
        if self.check_data_availability(uuid) == False:
            status_code = status.HTTP_404_NOT_FOUND
            response = {"Error":"No such UUID/data"}
            return status_code, response
        else:
            list_of_images = self.image_dao.list_of_images_by_uuid(uuid) 
            bucket_name = self.get_bucket_name(list_of_images) 

            self.delete_images_from_minio(uuid, list_of_images, bucket_name)
            self.delete_images_from_db(uuid)

            status_code = status.HTTP_200_OK
            response = {"Status":"All images was deleted from DB and minIO"}
            return status_code, response

#---------------------------------------------------
    def upload_images_to_db(self,files, date_time, uuid):
        self.image_dao.insert_images(files, date_time, uuid)
        uploaded_files = self.image_dao.list_of_images_by_uuid(uuid)
        return uploaded_files #лишний запрос?

    def upload_images_to_minio(self, files, uuid, date_time):
        bucket_name = self.make_new_bucket_name(date_time)
        self.image_minio_access.insert_images(files, bucket_name, uuid)

    def upload_images(self, files):
        if self.check_images_validity(files) == False:
            status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            response = {"Error":"Some files is not jpeg"}
            return status_code, response

        uuid = self.newuuid()
        date_time = datetime.today()

        self.upload_images_to_minio(files, uuid, date_time)
        added_images = self.upload_images_to_db(files, date_time, uuid)

        status_code = status.HTTP_200_OK
        response = {"Status":"All images were added to DB and minIO", "Images": added_images}
        return status_code, response

#--------------------------
    def get_bucket_name(self, data_image):
        print(data_image)
        bucket_name = datetime.strptime(data_image[0][2],'%Y-%m-%d %H:%M:%S.%f') 
        bucket_name = bucket_name.strftime("%Y%m%d")
        return bucket_name

    def show_list_of_images_by_uuid(self, uuid):
        list_of_images = self.image_dao.list_of_images_by_uuid(uuid)
        if len(list_of_images) !=0:
            status_code = status.HTTP_200_OK
            response = {"Images":list_of_images}
        else:
            status_code = status.HTTP_404_NOT_FOUND
            response = {"Error":"No such UUID/data"}
        return status_code, response

    def newuuid(self):
        newuuid = str(uuid.uuid4())
        return newuuid
 
    def check_data_availability(self,uuid):
        data = self.image_dao.list_of_images_by_uuid(uuid)
        print(data)
        if len(data) == 0:
            return False

    def check_images_validity(self,files):
        for file in files:
            if file.filename.endswith('.jpeg'):
                continue
            else:
                return False

    def make_new_bucket_name(self, date_time):
        date_time = datetime.today() 
        bucket_name = date_time.strftime('%Y%m%d')
        return bucket_name

    


    



