from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import boto3
import os

aws_access_key = os.environ.get("AWS_ACCESS_KEY")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
s3 = boto3.resource("s3", 
                    aws_access_key_id=aws_access_key, 
                    aws_secret_access_key=aws_secret_access_key)

def get_data():
    obj = s3.Object("drew-cse-4207", "lab2/movie_data.json")
    body = obj.get()['Body'].read()
    json_data = json.loads(body)
    return json_data

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {"message": "Hello World from FastAPI!"})

@app.get("/movies")
def get_movies(request: Request):
    data = get_data()
    return templates.TemplateResponse(request, "movies.html", {"movies": data["results"]})
