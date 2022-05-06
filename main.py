from fastapi import FastAPI, File, UploadFile, Response, status
import uvicorn

from repository import Repository

from typing import List

from db.db import ImageDao
from minIO.minIO import ImageMinioAccess


app = FastAPI()

image_dao = ImageDao('db/images_database.db')
image_minio_access = ImageMinioAccess("play.min.io",'Q3AM3UQ867SPQQA43P2F','zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG') #access_data
repo = Repository(image_dao,image_minio_access)

@app.get('/frames/{uuid}')
def display_list_of_images(response: Response, uuid:str):
    response.status_code, response = repo.show_list_of_images_by_uuid(uuid)
    return response

@app.get('/')
def root():
    return {"Greeting":"Hello"}

@app.post('/frames/')
def upload_images(response: Response, files: List[UploadFile] = File(...)):
    if 1 <= len(files) <= 3:
        response.status_code, response = repo.upload_images(files)
        return response
    else:
        response.status_code = status.HTTP_201_CREATED #другой код
        return {"Error": "Number of files should be < 3"}


@app.delete('/frames/{uuid}')
def remove_images(response: Response, uuid: str):
    response.status_code, response = repo.delete_images(uuid)
    return response

if __name__ == '__main__':
    uvicorn.run("main:app", host = '0.0.0.0', port=7000, debug=False)
