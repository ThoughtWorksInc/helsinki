from pymongo import MongoClient


mongo = MongoClient()
db = mongo.helsinki
subscriptions = db.subscriptions


def save_subscription(email, topic):
    sub = {'email': email, 'topic': topic}
    subscriptions.insert_one(sub)


def get_subscriptions():
    return subscriptions.find()

