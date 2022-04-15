import sqlite3
import uuid

class ImageDao:

    def __init__(self,db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS inbox(
                    UUID NOT NULL,
                    file_name NOT NULL,
                    date_time  NOT NULL);""")
        self.connection.commit()
    
    def insert_images(self,files, date_time):
        cursor = self.connection.cursor()
        query = """INSERT INTO inbox (UUID,file_name,date_time) VALUES (?,?,?);"""
        newuuid = str(uuid.uuid4()) 
        for file in files:
            params = (newuuid, file.filename, date_time)
            cursor.execute(query, params)
        self.connection.commit()
        cursor.close()
        return newuuid

    def delete_images(self,uuid):
        cursor = self.connection.cursor()
        query = """DELETE FROM inbox WHERE UUID = ?;"""
        cursor.execute(query, (uuid, ))
        self.connection.commit()
        cursor.close()
        

    def list_of_images_by_uuid(self, uuid):
        cursor = self.connection.cursor()
        query = """SELECT * FROM inbox WHERE UUID = ?;"""
        data = cursor.execute(query, (uuid, ))
        self.connection.commit()
        return data.fetchall()