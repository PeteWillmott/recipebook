import os, sys
import pymongo
from app import app, hrs_to_mins
from flask_pymongo import PyMongo

MONGO_URI = ""

def test_home(self):
    time_hrs = 3
    result = self.app.get(hrs_to_mins(time_hrs))
    self.assertEqual(result, 180)
