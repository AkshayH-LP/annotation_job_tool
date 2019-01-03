import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import boto3




class s3_handler():

    def __init__(self):

        ### Initialize the Boto3 session on s3 with credentials
        session = boto3.Session(
            aws_access_key_id='',
            aws_secret_access_key='', 
            region_name = 'us-west-2')
        self.s3_resource = session.resource('s3')
        self.first_bucket_name = 'taxonomies-lp'

    def upload_to_s3(self, first_file_name):

        ### Upload the file mentioned by its file_name to s3

        self.s3_resource.Object(self.first_bucket_name, first_file_name).upload_file(
        Filename=first_file_name)

    def get_file_link(self, first_file_name):

        ### Get the Object url link of the uploaded files from s3

        bucket_location = boto3.client('s3').get_bucket_location(Bucket=self.first_bucket_name)
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location['LocationConstraint'], self.first_bucket_name, first_file_name)
        return object_url