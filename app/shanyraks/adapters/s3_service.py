from typing import BinaryIO

import boto3


class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def upload_file(self, id: str, file: BinaryIO, filename: str):
        bucket = "leila.bekturgan1-bucket"
        filekey = f"shanyraks/{id}/{filename}"
        
        self.s3.upload_fileobj(file, bucket, filekey)
        
        bucket_location = boto3.client("s3").get_bucket_location(
            Bucket=bucket
        )
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location["LocationConstraint"], bucket, filekey
        )
        
        return object_url
    
    def delete_file(self, id: str, filename: str):
        bucket = "leila.bekturgan1-bucket"
        filekey = f"shanyraks/{id}/{filename}"
        
        self.s3.delete_object(Bucket=bucket, Key=filekey)
