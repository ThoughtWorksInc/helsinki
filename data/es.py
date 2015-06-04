from elasticsearch import Elasticsearch


es = Elasticsearch()


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

