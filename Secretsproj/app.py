from flask import Flask, redirect
import requests
import boto3 
from botocore.exceptions import ClientError
import json
import os
from dotenv import load_dotenv
import logging
import sys

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

load_dotenv()

def get_secret():
    secret_name = os.getenv("SECRET_NAME")
    region_name = os.getenv("REGION_NAME")

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

@app.route("/")
def root():
    logger.info("Health check on root route /")
    return "OK", 200

@app.route("/health")
def health():
    logger.info("Health check on root route /health")
    return "OK", 200

@app.route("/getdog", methods=['GET'])
def get_random_dog():
    logger.info("Fetching a dog image from external API")
    try:
        secrets = get_secret()
        DOG_API_KEY = secrets["DOG_API_KEY"]
    except Exception as e:
        logger.error(f"Failed to load secret: {e}")
        return f"Error loading secret: {str(e)}", 500

    headers = {"x-api-key": DOG_API_KEY}
    response = requests.get(DOG_API_URL, headers=headers)
    
    if response.status_code != 200:
        logger.warning(f"Dog API returned {response.status_code}: {response.text}")
        return "Failed to get dog image", 500

    data = response.json()
    if data:
        image_url = data[0]["url"]
        logger.info(f"Redirecting to dog image: {image_url}")
        return redirect(image_url)
    else:
        logger.info("No dog image found in API response")
        return "No dog found 😢", 404

if __name__ == '__main__':
    app.run()
