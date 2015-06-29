from es import index_decisions
from decisions import get_municipal_actions, get_decisions, number_of_decisions, last_modified_time
import logging


page_size = 50
logger = logging.getLogger('helsinki_log')


def import_decision_data_page(page_no):
    decisions = get_decisions(page_size, page_no * page_size)
    municipal_actions = get_municipal_actions(decisions)
    index_decisions(municipal_actions)
    return decisions


def should_continue_to_index(number_of_pages, current_page, last_decisions_count, previous_lmt, lmt):
    if previous_lmt and lmt <= previous_lmt:
        logger.debug("Stopping indexing as decisions have already been indexed, %s %s" % (previous_lmt, lmt))
        return False
    elif last_decisions_count < page_size:
        return False
    elif number_of_pages > 0:
        return current_page < number_of_pages - 1
    return True


def import_decision_data(save_last_modified_fn, get_last_modified_fn, number_of_pages=-1):
    page_no = 0
    mongo_lmt = get_last_modified_fn()
    decisions = import_decision_data_page(page_no)
    lmt = last_modified_time(decisions)
    decision_count = number_of_decisions(decisions)
    save_last_modified_fn(lmt)
    while should_continue_to_index(number_of_pages, page_no, decision_count, mongo_lmt, lmt):
        page_no += 1
        decisions = import_decision_data_page(page_no)
        decision_count = number_of_decisions(decisions)
        lmt = last_modified_time(decisions)
