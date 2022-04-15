import json
from fastapi import status
from datetime import datetime

class Repository:

    def __init__(self,image_dao,image_minio_access,files=None):
        self.image_dao = image_dao
        self.image_minio_access = image_minio_access
        self.response = ''
        self.status_code = 200

    def check_uuid_for_delete(self,uuid):
        cursor = self.image_dao.connection.cursor()
        query = """SELECT * FROM inbox WHERE UUID = ?;"""
        data = cursor.execute(query, (uuid, ))
        if data.fetchone() is None:
            self.status_code = status.HTTP_404_NOT_FOUND
            self.response = {"Error": "No such UUID or data"}
        else:
            bucket_name = datetime.strptime(data.fetchone()[2],'%Y-%m-%d %H:%M:%S.%f') 
            bucket_name = bucket_name.strftime("%Y%m%d")
            list_of_images = self.image_dao.list_of_images_by_uuid(uuid)
            for images_data in list_of_images:
                uuid = images_data [0]
                image = images_data[1]
                self.image_minio_access.delete_images(image, uuid, bucket_name)
            self.image_dao.delete_images(uuid)
            self.status_code = status.HTTP_200_OK
            self.response = {"Status":"All images was deleted from DB and minIO"}
        return self.status_code, self.response

    def check_uuid_for_display(self,uuid):
        cursor = self.image_dao.connection.cursor()
        query = """SELECT * FROM inbox WHERE UUID = ?;"""
        data = cursor.execute(query, (uuid, ))
        if data.fetchall() is None:
            self.status_code = status.HTTP_404_NOT_FOUND
            self.response = {"Error":"No such UUID or data"}
        else:
            data = self.image_dao.list_of_images_by_uuid(uuid)
            self.response = {"Images":data}
            self.status_code = status.HTTP_200_OK
        return self.status_code, self.response


    def check_images(self,files):
        for file in files:
            if file.filename.endswith('.jpeg'):
                continue
            else:
                self.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                self.response = {"Error":"Some files is not jpeg"}
                return self.status_code, self.response
        date_time = datetime.today() 
        bucket_name = date_time.strftime('%Y%m%d')
        uuid = self.image_dao.insert_images(files,date_time)      
        self.image_minio_access.insert_images(files, bucket_name, uuid)
        added_images = self.image_dao.list_of_images_by_uuid(uuid)
        self.response = {"Status":"All images were added to DB and minIO", "Images":added_images}
        return self.status_code, self.response




    




