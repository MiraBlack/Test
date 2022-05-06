import sqlite3

class ImageDao:

    def __init__(self,db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS inbox(
                    UUID NOT NULL,
                    file_name NOT NULL,
                    date_time  NOT NULL);""")
        self.connection.commit()
    
    def insert_images(self, files, date_time, uuid):
        cursor = self.connection.cursor()
        query = """INSERT INTO inbox (UUID,file_name,date_time) VALUES (?,?,?);"""
        for file in files:
            params = (uuid, file.filename, date_time)
            cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def delete_images(self,uuid):
        cursor = self.connection.cursor()
        query = """DELETE FROM inbox WHERE UUID = ?;"""
        cursor.execute(query, (uuid, ))
        self.connection.commit()
        cursor.close()
        
    def list_of_images_by_uuid(self, uuid):
        cursor = self.connection.cursor()
        query = """SELECT * FROM inbox WHERE UUID = ?;"""
        list_of_images = cursor.execute(query, (uuid, ))
        self.connection.commit()
        return list_of_images.fetchall()
