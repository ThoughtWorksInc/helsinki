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

