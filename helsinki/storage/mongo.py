import os
from pymongo import MongoClient
from helsinki.logger.logs import get_logger

logger = get_logger()


try:
    mongo = MongoClient(host=os.getenv('MONGO_PORT_27017_TCP_ADDR', 'localhost'))
    db = mongo.helsinki
    subscriptions = db.subscriptions
    meta = db.meta
except Exception as e:
    logger.error('Could not connect to mongoDB: %s' % e)
    raise e


def save_subscription(email, topic):
    sub = {'email': email, 'topic': topic, '_id': email.lower()}
    subscriptions.insert_one(sub)


def get_subscriptions():
    return subscriptions.find()


def save_last_modified_time(last_modified_time):
    lmt = {'name': 'last_modified_time', 'value': last_modified_time}
    logger.debug("Saving last modified time: %s" % last_modified_time)
    meta.replace_one({'name': 'last_modified_time'}, lmt, True)


def get_last_modified_time():
    entry = meta.find_one({'name': 'last_modified_time'})
    if entry:
        return entry.get('value')
