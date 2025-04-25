from flask import Flask, redirect
import requests
import boto3 
from botocore.exceptions import ClientError
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_secret():

    secret_name = os.getenv("SECRET_NAME")
    region_name = os.getenv("REGION_NAME")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return json.loads(get_secret_value_response['SecretString'])
    except ClientError as e:
        raise e

app = Flask(__name__)
DOG_API_URL = "https://api.thedogapi.com/v1/images/search"
DOG_API_KEY = get_secret()["DOG_API_KEY"]

@app.route('/', methods=['GET'])
def get_random_dog():
    headers = {
        "x-api-key": DOG_API_KEY
    }

    response = requests.get(DOG_API_URL, headers=headers)
    data = response.json()

    if data:
        image_url = data[0]["url"]
        return redirect(image_url)
    else:
        return "No dog found 😢", 404

if __name__ == '__main__':
    app.run()