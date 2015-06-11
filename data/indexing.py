from es import configure, index_decisions
from decisions import get_municipal_actions


def import_decision_data():
    configure()
    municipal_actions = get_municipal_actions()
    index_decisions(municipal_actions)
