from django.db import models

# Create your models here.
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['feed_ranking_db']
collection = db['reviews']