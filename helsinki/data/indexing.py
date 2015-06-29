from helsinki.data.es import index_decisions
from helsinki.data.decisions import get_municipal_actions, get_decisions, number_of_decisions, last_modified_time
from helsinki.storage.mongo import save_last_modified_time, get_last_modified_time
from helsinki.logger.logs import get_logger


page_size = 50


def import_decision_data_page(page_no):
    decisions = get_decisions(page_size, page_no * page_size)
    municipal_actions = get_municipal_actions(decisions)
    index_decisions(municipal_actions)
    return decisions


def should_continue_to_index(number_of_pages, current_page, last_decisions_count, previous_lmt, lmt):
    if previous_lmt and lmt <= previous_lmt:
        get_logger().debug("Stopping indexing as decisions have already been indexed, %s %s" % (previous_lmt, lmt))
        return False
    elif last_decisions_count < page_size:
        return False
    elif number_of_pages > 0:
        return current_page < number_of_pages - 1
    return True


def import_decision_data(number_of_pages=-1):
    page_no = 0
    mongo_lmt = get_last_modified_time()
    decisions = import_decision_data_page(page_no)
    lmt = last_modified_time(decisions)
    decision_count = number_of_decisions(decisions)
    save_last_modified_time(lmt)
    while should_continue_to_index(number_of_pages, page_no, decision_count, mongo_lmt, lmt):
        page_no += 1
        decisions = import_decision_data_page(page_no)
        decision_count = number_of_decisions(decisions)
        lmt = last_modified_time(decisions)
