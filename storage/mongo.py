import os
from pymongo import MongoClient


mongo = MongoClient(host=os.getenv('MONGO_PORT_27017_TCP_ADDR', 'localhost'))
db = mongo.helsinki
subscriptions = db.subscriptions


def save_subscription(email, topic):
    sub = {'email': email, 'topic': topic, '_id': email.lower()}
    subscriptions.insert_one(sub)


def get_subscriptions():
    return subscriptions.find()
