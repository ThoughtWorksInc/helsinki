from es import configure, index_decisions
from decisions import get_municipal_actions


def import_decision_data():
    configure()
    decisions = get_decisions()
    municipal_actions = get_municipal_actions(decisions)
    index_decisions(municipal_actions)
