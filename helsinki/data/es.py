import os
from elasticsearch import Elasticsearch
import logging
import time
import dateutil.parser

import decisions
from date_format import friendly_day, friendly_date

logger = logging.getLogger('helsinki_log')

try:
    logger.info('Attempt to connect to elasticsearch')
    es = Elasticsearch([{'host': os.getenv('ELASTICSEARCH_PORT_9200_TCP_ADDR',
                                           'localhost')}])
except Exception as e:
    logger.error('Could not connect to elasticsearch: %s' % e)
    raise e


def configure():
    if not es.indices.exists(index='decisions'):
        try:
            logger.debug("Creating indexes")
            es.indices.delete('decisions', ignore=[400, 404])
            es.indices.create(
                index="decisions",
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                        "analysis": {
                            "analyzer": {
                                "default": {
                                    "tokenizer": "finnish",
                                    "filter": ["lowercase", "voikkoFilter"]
                                }
                            },
                            "filter": {
                                "voikkoFilter": {
                                    "type": "voikko"
                                }
                            }
                        }
                    },
                    "mappings": decisions.DECISION_MAPPING},
                ignore=400
            )
        except Exception as e:
            logger.error("Could not set up indexes: %s" % e)
            raise e
    else:
        logger.debug("Decisions index already exists")


def index_decision(decision):
    try:
        es.index(
            index="decisions",
            doc_type="decision_data",
            body=decision,
            id=decision.get("id")
        )
    except:
        logger.warning("Error when indexing: %s" % decision)
        pass


def index_decisions(municipal_actions):
    map(index_decision, municipal_actions)


def _source_with_id(raw_result):
    source = raw_result.get('_source')
    id = raw_result.get('_id')
    source['id'] = id
    return source


def _source_with_friendly_day(raw_result):
    last_modified_time = raw_result.get('origin_last_modified_time')
    raw_result['friendly_day'] = friendly_day(last_modified_time)
    raw_result['friendly_date'] = friendly_date(last_modified_time)
    return raw_result


def last_modified_time_as_float(result):
    date = dateutil.parser.parse(result.get('origin_last_modified_time'))
    return time.mktime(date.timetuple())


def sort_by_last_modified_time(results):
    return sorted(results, key=last_modified_time_as_float, reverse=True)


class ElasticSearchApi:

    def find_decisions(self, criteria):
        results = es.search(
            index="decisions",
            body={"query": {"multi_match": {"query": criteria,
                                            "type": "most_fields",
                                            "fields": decisions.SEARCH_FIELDS}}}
        )
        hits = results.get("hits")
        results = [_source_with_friendly_day(_source_with_id(hit)) for hit in hits.get("hits")]
        return sort_by_last_modified_time(results)

    def find_decision(self, id):
        result = es.get(
            index="decisions",
            doc_type="decision_data",
            id=id,
            ignore=[404]
        )
        if result.get('found'):
            return _source_with_id(result)
