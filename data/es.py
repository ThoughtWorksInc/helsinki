from elasticsearch import Elasticsearch


es = Elasticsearch()


def configure():
  try:
    es.indices.delete('decisions', ignore=[400,404])
    es.indices.create(
        index="decisions",
        body={
          "settings": {"number_of_shards": 1, "number_of_replicas": 0},
          "mappings": {
            "decision_data": {
              "properties": {
                "subject": {
                  "type": "string",
                  "analyzer": "finnish"
                  }
                }
              }
            }
          },
        ignore=400
        )
  except Exception as e:
    print "Could not set up indexes: ", e
    pass


def index_decision(decision):
  try:
    es.index(
        index="decisions",
        doc_type="decision_data",
        body=decision,
        id=decision.get("id")
        )
  except:
    print "Error when indexing: %s" % decision
    pass


def find_decisions(criteria):
  results = es.search(
      index="decisions",
      body={"query": {"query_string": {"query": criteria, "default_field": "subject"}}}
      )
  hits = results.get("hits")
  return [hit.get("_source") for hit in hits.get("hits")]

