from es import index_decisions
from decisions import get_municipal_actions, get_decisions, number_of_decisions

page_size = 50

def import_decision_data_page(page_no):
    decisions = get_decisions(page_size, page_no*page_size)
    municipal_actions = get_municipal_actions(decisions)
    index_decisions(municipal_actions)
    return number_of_decisions(decisions)

def should_continue_to_index(number_of_pages, current_page, last_decisions_count):
    if last_decisions_count < page_size:
        return False
    if number_of_pages > 0:
        return current_page < number_of_pages - 1
    return True

def import_decision_data(number_of_pages = -1):
    page_no = 0
    decision_count = import_decision_data_page(page_no)
    while should_continue_to_index(number_of_pages, page_no, decision_count):
        page_no += 1
        decision_count = import_decision_data_page(page_no)
