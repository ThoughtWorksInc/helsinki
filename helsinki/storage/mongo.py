import os
from pymongo import MongoClient
import logging
import uuid

logger = logging.getLogger('helsinki_log')


try:
    mongo = MongoClient(host=os.getenv('MONGO_PORT_27017_TCP_ADDR', 'localhost'))
    db = mongo.helsinki
    subscriptions = db.subscriptions
    meta = db.meta
except Exception as e:
    logger.error('Could not connect to mongoDB: %s' % e)
    raise e


def save_subscription(email, topic):
    sub = subscriptions.find_one({'_id': email.lower()})
    if sub:
        subscriptions.replace_one({'_id': email.lower()},
                                  {'email': email,
                                   'topic': topic,
                                   '_id': email.lower(),
                                   'unsubscribe_id': sub.get('unsubscribe_id')},
                                  True)
    else:
        subscriptions.insert_one({'email': email,
                                  'topic': topic,
                                  '_id': email.lower(),
                                  'unsubscribe_id': uuid.uuid1()})


def delete_subscription(unsubscribe_id):
    doc = subscriptions.find_one({'unsubscribe_id': unsubscribe_id})
    delete_result = subscriptions.delete_one({'unsubscribe_id': unsubscribe_id})
    return doc


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
